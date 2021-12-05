# pylint: disable=W0621
import pytest

from index.tokenizer import SimpleTokenizer


@pytest.fixture
def simple_tokenizer() -> SimpleTokenizer:
    return SimpleTokenizer()


def test_simple_tokenizer_should_split_simple_text(
    simple_tokenizer: SimpleTokenizer,
) -> None:
    v = "this is a test."
    assert simple_tokenizer.tokenize(v) == ["this", "is", "a", "test."]


def test_simple_tokenizer_should_split_text_with_multiple_spaces(
    simple_tokenizer: SimpleTokenizer,
) -> None:
    v = "    this  is        a test.    "
    assert simple_tokenizer.tokenize(v) == ["this", "is", "a", "test."]
