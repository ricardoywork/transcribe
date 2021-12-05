from abc import ABC, abstractmethod
import re


class AbstractTokenizer(ABC):
    @abstractmethod
    def tokenize(self, s: str) -> list[str]:
        """
        Return a list of words from s.
        """


class SimpleTokenizer(AbstractTokenizer):
    def __init__(self) -> None:
        self.pattern = re.compile(r"\S+")

    def tokenize(self, s: str) -> list[str]:
        return self.pattern.findall(s)
