from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Array(Generic[T]):
    """A fixed-size array."""

    def __init__(self, capacity: int = 16) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._items: list[Optional[T]] = [None] * capacity
        self._capacity = capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    def __getitem__(self, index: int) -> Optional[T]:
        if not 0 <= index < self._capacity:
            raise IndexError("Index out of bounds")
        return self._items[index]

    def __setitem__(self, index: int, value: Optional[T]) -> None:
        if not 0 <= index < self._capacity:
            raise IndexError("Index out of bounds")
        self._items[index] = value

    def resize(self, new_capacity: int) -> None:
        """Resize to new_capacity, keeping as many items as fit."""
        if new_capacity <= 0:
            raise ValueError("Capacity must be positive")

        new_items: list[Optional[T]] = [None] * new_capacity
        # Copy as many items as will fit
        for i in range(min(self._capacity, new_capacity)):
            new_items[i] = self._items[i]

        self._items = new_items
        self._capacity = new_capacity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(capacity={self._capacity}, items={self._items!r})"

    def __str__(self) -> str:
        return f"[{', '.join(repr(x) for x in self._items)}]"
