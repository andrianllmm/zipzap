from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from zipzap.ds.entry import Entry

K = TypeVar("K")
V = TypeVar("V")


class PriorityQueue(ABC, Generic[K, V]):
    """Abstract priority queue storing key-value pairs."""

    @abstractmethod
    def add(self, key: K, value: V) -> None:
        """Add a new key-value pair."""
        ...

    @abstractmethod
    def min(self) -> Entry[K, V]:
        """Return the entry with the smallest key without removing it (error if empty)."""
        ...

    @abstractmethod
    def remove_min(self) -> Entry[K, V]:
        """Remove and return the entry with the smallest key (error if empty)."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items."""
        ...

    def is_empty(self) -> bool:
        """Return True if the queue has no items."""
        return len(self) == 0
