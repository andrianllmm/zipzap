from __future__ import annotations

from typing import TypeVar

from zipzap.ds.deques.deque import Deque
from zipzap.ds.linked_list_nodes import DLLNode
from zipzap.exceptions import Empty


T = TypeVar("T")


class LinkedDeque(Deque[T]):
    """Linked list implementation of a deque."""

    def __init__(self):
        self.size: int = 0

        self.header = DLLNode[T](None)
        self.trailer = DLLNode[T](None)

        self.header.next = self.trailer
        self.trailer.prev = self.header

    def add_first(self, item):
        new_node = DLLNode(item)
        first = self.header.next
        assert first is not None

        new_node.prev = self.header
        new_node.next = first

        first.prev = new_node
        self.header.next = new_node

        self.size += 1

    def add_last(self, item):
        new_node = DLLNode(item)
        last = self.trailer.prev
        assert last is not None

        new_node.next = self.trailer
        new_node.prev = last

        last.next = new_node
        self.trailer.prev = new_node

        self.size += 1

    def delete_first(self):
        if self.is_empty():
            raise Empty("Deque is empty")

        to_remove = self.header.next
        assert to_remove is not None and to_remove.next is not None
        self.header.next = to_remove.next
        to_remove.next.prev = self.header

        to_remove.next = None
        to_remove.prev = None

        self.size -= 1

        return to_remove.item

    def delete_last(self):
        if self.is_empty():
            raise Empty("Deque is empty")

        to_remove = self.trailer.prev
        assert to_remove is not None and to_remove.prev is not None
        self.trailer.prev = to_remove.prev
        to_remove.prev.next = self.trailer

        to_remove.next = None
        to_remove.prev = None

        self.size -= 1

        return to_remove.item

    def first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        first = self.header.next
        assert first is not None
        return first.item

    def last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        last = self.trailer.prev
        assert last is not None
        return last.item

    def __len__(self):
        return self.size

    def __str__(self):
        items = []
        node = self.header.next
        while node is not None and node != self.trailer:
            items.append(repr(node.item))
            node = node.next
        return "[" + ", ".join(items) + "]"

    def __repr__(self):
        nodes = []
        node = self.header.next
        while node is not None and node != self.trailer:
            nodes.append(f"{repr(node)}")
            node = node.next
        return f"{self.__class__.__name__}({', '.join(nodes)})"
