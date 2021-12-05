from dataclasses import dataclass, field


MAX_EPISODE_TIME = 1e10


@dataclass
class IntervalData:
    ini: float
    end: float


@dataclass
class TokenizedTranscription(IntervalData):
    text: str


@dataclass
class Transcription(IntervalData):
    text: str
    tokenized_transcriptions: list[TokenizedTranscription] = field(default_factory=list)


@dataclass
class Episode:
    id: str
    transcriptions: list[Transcription] = field(default_factory=list)
