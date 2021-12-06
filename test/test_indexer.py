import pytest

from index.indexer import (
    time_transcript_generator,
    ini_end_transcript_generator,
    BinarySearchTranscriptionIndex,
)
from index.tokenizer import SimpleTokenizer


def test_time_transcript_generator_should_not_yield_if_content_is_empty() -> None:
    content = ""
    assert len(list(x for x in time_transcript_generator(content))) == 0


def test_time_transcript_generator_should_yield_correct_time_in_seconds() -> None:
    content = """0:00
    a
    
    0:01
    b
    
    1:01
    c
    
    10:01
    d
    
    100:12
    e
    """

    values = time_transcript_generator(content)

    v = next(values)
    assert v == (0, "a")

    v = next(values)
    assert v == (1, "b")

    v = next(values)
    assert v == (61, "c")

    v = next(values)
    assert v == (601, "d")

    v = next(values)
    assert v == (6012, "e")


def test_time_transcript_generator_should_ignore_lines_if_necessary() -> None:
    content = """
    
    0:00
    First
    
    
    1:00
    Second
    
    
    
    
    2:00
    Third
    
    
    
    Transcribed by https://url
    
    """

    values = list(v for v in time_transcript_generator(content))

    assert len(values) == 3
    assert values[0] == (0, "First")
    assert values[1] == (60, "Second")
    assert values[2] == (120, "Third")


def test_ini_end_transcript_generator_should_yield_nothing_if_content_is_empty() -> None:
    content = ""
    values = list(v for v in ini_end_transcript_generator(content, episode_length=1))
    assert len(values) == 0


def test_ini_end_transcript_generator_should_yield_single_value() -> None:
    content = """0:11
    Single line
    """
    values = list(v for v in ini_end_transcript_generator(content, 20))
    assert len(values) == 1
    assert values[0] == (11, 20, "Single line")


def test_ini_end_transcript_generator_should_yield_two_values() -> None:
    content = """0:11
    Single line
    
    0:22
    Second line
    """
    values = list(v for v in ini_end_transcript_generator(content, 30))
    assert len(values) == 2
    assert values[0] == (11, 22, "Single line")
    assert values[1] == (22, 30, "Second line")


def test_indexer_add_should_work() -> None:
    index = BinarySearchTranscriptionIndex(SimpleTokenizer())

    content = """0:01
    a b c
    
    0:04
    d e f
    """

    index.add(episode_id="an identifier", content=content, episode_length=7)

    assert len(index.episodes) == 1
    assert index.episodes["an identifier"].transcriptions[0].text == "a b c"
    assert index.episodes["an identifier"].transcriptions[0].ini == pytest.approx(1)
    assert index.episodes["an identifier"].transcriptions[0].end == pytest.approx(4)

    tokenized_transcriptions = (
        index.episodes["an identifier"].transcriptions[0].tokenized_transcriptions
    )

    assert tokenized_transcriptions[0].text == "a"
    assert tokenized_transcriptions[0].ini == pytest.approx(1)
    assert tokenized_transcriptions[0].end == pytest.approx(2)

    assert tokenized_transcriptions[1].text == "b"
    assert tokenized_transcriptions[1].ini == pytest.approx(2)
    assert tokenized_transcriptions[1].end == pytest.approx(3)

    assert tokenized_transcriptions[2].text == "c"
    assert tokenized_transcriptions[2].ini == pytest.approx(3)
    assert tokenized_transcriptions[2].end == pytest.approx(4)

    assert index.episodes["an identifier"].transcriptions[1].text == "d e f"
    assert index.episodes["an identifier"].transcriptions[1].ini == pytest.approx(4)
    assert index.episodes["an identifier"].transcriptions[1].end == pytest.approx(7)

    tokenized_transcriptions = (
        index.episodes["an identifier"].transcriptions[1].tokenized_transcriptions
    )

    assert tokenized_transcriptions[0].text == "d"
    assert tokenized_transcriptions[0].ini == pytest.approx(4)
    assert tokenized_transcriptions[0].end == pytest.approx(5)

    assert tokenized_transcriptions[1].text == "e"
    assert tokenized_transcriptions[1].ini == pytest.approx(5)
    assert tokenized_transcriptions[1].end == pytest.approx(6)

    assert tokenized_transcriptions[2].text == "f"
    assert tokenized_transcriptions[2].ini == pytest.approx(6)
    assert tokenized_transcriptions[2].end == pytest.approx(7)


def test_build_content_from_more_than_one_segment_should_work() -> None:
    content = """0:00
        0 1 2 3
        
        0:04
        4 5 6 7
        
        0:08
        8 9 10 11
        
        0:12
        12 13 14 15
        """

    index = BinarySearchTranscriptionIndex(SimpleTokenizer())
    index.add("episode_1", content, episode_length=16)

    assert index.search("episode_1", 0, 1) == "0"
    assert index.search("episode_1", 1, 3) == "1 2"
    assert index.search("episode_1", 3, 5) == "3 4"
    assert index.search("episode_1", 3, 8) == "3 4 5 6 7"
    assert index.search("episode_1", 2, 13) == "2 3 4 5 6 7 8 9 10 11 12"
    assert index.search("episode_1", 6, 9) == "6 7 8"
