import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator
from typing import Optional

from index.binary_search import search_ini_le, search_end_ge
from index.tokenizer import AbstractTokenizer
from model import (
    Transcription,
    TokenizedTranscription,
    Episode,
    MAX_EPISODE_TIME,
)

EPSILON = 1e-10


class InvalidContentError(Exception):
    pass


class TranscriptParserState(Enum):
    TIMESTAMP = 0
    TRANSCRIPT = 1


TIME_PATTERN = re.compile(r"(?:(\d+):)?(\d+):(\d\d)")


def process_time(t: str) -> Optional[int]:
    """
    Return the timestamp in seconds. The input format is `h:m:ss` or `m:ss`.
    """
    m = TIME_PATTERN.match(t)
    if m is None:
        return None

    if m.group(1) is None:
        hours = 0
    else:
        hours = int(m.group(1))
    minutes = int(m.group(2))
    seconds = int(m.group(3))
    if seconds > 60:
        raise InvalidContentError(f"Invalid time format: {t}")
    return hours * 3600 + minutes * 60 + seconds


def time_transcript_generator(content: str) -> Iterator[tuple[float, str]]:
    """
    Yield the tuple (timestamp in seconds from the beginning of the episode for the first word,
    transcript).
    """
    lines = content.split("\n")

    expected_state: TranscriptParserState = TranscriptParserState.TIMESTAMP

    i = 0
    n = len(lines)

    time_in_seconds = None
    while i < n:
        line = lines[i].strip()
        i += 1
        if line == "":
            continue
        if expected_state == TranscriptParserState.TIMESTAMP:
            time_in_seconds = process_time(line)
            if time_in_seconds is not None:
                expected_state = TranscriptParserState.TRANSCRIPT
        else:
            if line != "":
                if time_in_seconds is None:
                    raise InvalidContentError
                yield time_in_seconds, line
                expected_state = TranscriptParserState.TIMESTAMP
                time_in_seconds = None


def ini_end_transcript_generator(
    content: str, episode_length: float = MAX_EPISODE_TIME
) -> Iterator[tuple[float, float, str]]:
    """
    Yield the tuple(start time, end time, transcript) for content. The start time for an episode
    i is the end time for episode i-1. The last episode has end time = episode_length.
    """
    v = time_transcript_generator(content)

    try:
        previous = next(v)
    except StopIteration:
        return

    while True:
        try:
            current = next(v)
        except StopIteration:
            break

        yield previous[0], current[0], previous[1]
        previous = current

    yield previous[0], episode_length, previous[1]


class AbstractTranscriptionIndex(ABC):
    @abstractmethod
    def search(self, episode_id: str, ini: float, end: float) -> str:
        """
        Return the segment of transcript between ini -> end for the episode corresponding
        episode_id.
        """

    @abstractmethod
    def add(self, episode_id: str, content: str, episode_length: float = MAX_EPISODE_TIME) -> None:
        """
        Index the content from transcript for episode identified by episode_id. The format is:

        timestamp
        transcript
        blank line
        """


class BinarySearchTranscriptionIndex(AbstractTranscriptionIndex):
    def __init__(self, tokenizer: AbstractTokenizer):
        self.episodes: dict[str, Episode] = {}
        self.tokenizer = tokenizer

    def add(
        self, episode_id: str, content: str, episode_length: float = MAX_EPISODE_TIME
    ) -> None:
        ep = Episode(id=episode_id)

        for ini, end, raw_transcription in ini_end_transcript_generator(
            content, episode_length=episode_length
        ):
            t = Transcription(
                ini=ini + EPSILON, end=end - EPSILON, text=raw_transcription
            )
            tokens = self.tokenizer.tokenize(raw_transcription)
            n = len(tokens)
            for i in range(n):
                if end == MAX_EPISODE_TIME:
                    t.tokenized_transcriptions.append(
                        TokenizedTranscription(ini=ini, end=ini, text=tokens[i])
                    )
                else:
                    time_per_token = (end - ini) / n
                    t.tokenized_transcriptions.append(
                        TokenizedTranscription(
                            ini=ini + i * time_per_token + EPSILON,
                            end=(ini + (i + 1) * time_per_token) - EPSILON,
                            text=tokens[i],
                        )
                    )
            ep.transcriptions.append(t)

        self.episodes[episode_id] = ep

    def search(self, episode_id: str, ini: float, end: float) -> str:
        if episode_id not in self.episodes or ini == end:
            return ""

        ep = self.episodes[episode_id]
        v = []
        idx_ini = search_end_ge(ep.transcriptions, ini)
        idx_end = search_ini_le(ep.transcriptions, end)
        if idx_ini is None or idx_end is None:
            return ""
        for i in range(idx_ini, idx_end + 1):
            token_idx_ini = search_end_ge(
                ep.transcriptions[i].tokenized_transcriptions, ini
            )
            token_idx_end = search_ini_le(
                ep.transcriptions[i].tokenized_transcriptions, end
            )
            if token_idx_ini is not None and token_idx_end is not None:
                for j in range(token_idx_ini, token_idx_end + 1):
                    v.append(ep.transcriptions[i].tokenized_transcriptions[j].text)
        return " ".join(v)
