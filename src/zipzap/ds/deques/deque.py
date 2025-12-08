from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Deque(ABC, Generic[T]):
    """Abstract deque storing items."""

    @abstractmethod
    def add_first(self, item: T) -> None:
        """Add an item to the front of the deque."""
        ...

    @abstractmethod
    def add_last(self, item: T) -> None:
        """Add an item to the back of the deque."""
        ...

    @abstractmethod
    def delete_first(self) -> T:
        """Remove and return the first item in the deque (error if empty)."""
        ...

    @abstractmethod
    def delete_last(self) -> T:
        """Remove and return the last item in the deque (error if empty)."""
        ...

    @abstractmethod
    def first(self) -> T:
        """Return the first item in the deque (error if empty)."""
        ...

    @abstractmethod
    def last(self) -> T:
        """Return the last item in the deque (error if empty)."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items in the deque."""
        ...

    def is_empty(self) -> bool:
        """Return True if the deque is does not contain any items."""
        return len(self) == 0
