from abc import ABC, abstractmethod
from typing import Generic, Iterator, Optional, TypeVar

from zipzap.ds.entry import Entry

K = TypeVar("K")
V = TypeVar("V")


class Map(ABC, Generic[K, V]):
    """Abstract map storing key-value pairs."""

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """Return the value associated with key, or None if absent."""
        ...

    @abstractmethod
    def put(self, key: K, value: V) -> Optional[V]:
        """Associate value with key. Return the previous value if present, else None."""
        ...

    @abstractmethod
    def remove(self, key: K) -> Optional[V]:
        """Remove the item associated with key. Return its value if present, else None."""
        ...

    @abstractmethod
    def entries(self) -> Iterator[Entry[K, V]]:
        """Return an iterator over all entries."""
        ...

    def keys(self) -> Iterator[K]:
        """Return an iterator over the keys."""
        for entry in self.entries():
            yield entry.key

    def values(self) -> Iterator[V]:
        """Return an iterator over the values."""
        for entry in self.entries():
            yield entry.value

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items."""
        ...

    def is_empty(self) -> bool:
        """Return True if the map contains no items."""
        return len(self) == 0

    def __repr__(self) -> str:
        items = ", ".join(
            f"{repr(entry.key)}: {repr(entry.value)}" for entry in self.entries()
        )
        return f"{self.__class__.__name__}({{{items}}})"

    def __str__(self) -> str:
        items = ", ".join(f"{entry.key}: {entry.value}" for entry in self.entries())
        return f"{{{items}}}"
