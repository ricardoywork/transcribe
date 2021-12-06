from index.indexer import BinarySearchTranscriptionIndex
from index.tokenizer import SimpleTokenizer

index = BinarySearchTranscriptionIndex(SimpleTokenizer())
with open('episode_1.txt', 'r', encoding='utf8') as fh:
    index.add('episode_1', fh.read(), episode_length=13*60+57)


def retrieve_segment_transcript(episode_id: str, start_time: float, end_time: float) -> str:
    return index.search(episode_id, start_time, end_time)


def test_case_1() -> None:
    retrieved = retrieve_segment_transcript("episode_1", 21, 24)
    actual = "Everybody really just about literally everybody was growing Red Delicious."
    assert retrieved == actual


def test_case_2() -> None:
    """
    Explanation of this test case.

    The following is the text from 8:00 to 8:04, i.e. from 480 to 484 seconds.
        when the honeycrisp finally get to the store, they do great

    This means that 11 words are spread across 4 seconds. Hence, we should return
    5.5 words corresponding to the 2 seconds of transcript requested. Since,
    half a word doesn't make sense, we will round up and return 6 words.
    """
    retrieved = retrieve_segment_transcript("episode_1", 480, 482)
    actual = "when the honeycrisp finally get to"
    assert retrieved == actual


if __name__ == "__main__":
    test_case_1()
    test_case_2()
