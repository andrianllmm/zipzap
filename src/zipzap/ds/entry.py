from typing import Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Entry(Generic[K, V]):
    """A key-value pair."""

    __slots__ = ("key", "value")

    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def __iter__(self) -> Iterator:
        yield self.key
        yield self.value

    def __lt__(self, other: "Entry") -> bool:
        return self.key < other.key

    def __gt__(self, other: "Entry") -> bool:
        return self.key > other.key

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entry) and self.key == other.key

    def __ne__(self, other: object) -> bool:
        return not self == other
