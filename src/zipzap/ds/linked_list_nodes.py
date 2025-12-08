from __future__ import annotations

from abc import ABC
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class LinkedNode(ABC, Generic[T]):
    """A node in a linked list."""

    __slots__ = ("_item",)

    def __init__(self, item: Optional[T] = None):
        self._item = item

    @property
    def item(self) -> T:
        if self._item is None:
            raise ValueError("Item has not been set")
        return self._item

    @item.setter
    def item(self, value: T) -> None:
        self._item = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(item={repr(self.item)})"

    def __str__(self) -> str:
        return str(self.item)


class SLLNode(LinkedNode[T]):
    """A node in a singly-linked list."""

    __slots__ = ("_next",)

    def __init__(self, item: Optional[T] = None):
        super().__init__(item)
        self._next: Optional[SLLNode[T]] = None

    @property
    def next(self) -> Optional[SLLNode[T]]:
        return self._next

    @next.setter
    def next(self, node: Optional[SLLNode[T]]) -> None:
        self._next = node


class DLLNode(LinkedNode[T]):
    """A node in a doubly-linked list."""

    __slots__ = ("_next", "_prev")

    def __init__(self, item: Optional[T] = None):
        super().__init__(item)
        self._next: Optional[DLLNode[T]] = None
        self._prev: Optional[DLLNode[T]] = None

    @property
    def next(self) -> Optional[DLLNode[T]]:
        return self._next

    @next.setter
    def next(self, node: Optional[DLLNode[T]]) -> None:
        self._next = node

    @property
    def prev(self) -> Optional[DLLNode[T]]:
        return self._prev

    @prev.setter
    def prev(self, node: Optional[DLLNode[T]]) -> None:
        self._prev = node
