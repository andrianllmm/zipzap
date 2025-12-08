from typing import TypeVar

from zipzap.ds.array import Array
from zipzap.ds.entry import Entry
from zipzap.ds.priority_queues.priority_queue import PriorityQueue
from zipzap.exceptions import Empty

K = TypeVar("K")
V = TypeVar("V")


class HeapPriorityQueue(PriorityQueue[K, V]):
    """A binary heap implementation of a min-oriented priority queue."""

    def __init__(self, capacity: int = 64):
        self._data: Array[Entry[K, V]] = Array(capacity)
        self._size = 0

    def add(self, key: K, value: V) -> None:
        if self._size >= self._data.capacity:
            self._data.resize(self._data.capacity * 2)

        self._data[self._size] = Entry(key, value)
        self._upheap(self._size)
        self._size += 1

    def min(self) -> Entry[K, V]:
        if self.is_empty():
            raise Empty("Priority queue is empty.")

        item = self._data[self._root()]
        assert item is not None
        return item

    def remove_min(self) -> Entry[K, V]:
        if self.is_empty():
            raise Empty("Priority queue is empty.")

        self._swap(0, self._size - 1)
        item = self._item(self._size - 1)
        self._data[self._size - 1] = None
        self._size -= 1
        self._downheap(self._root())
        return item

    def _upheap(self, j: int) -> None:
        """Restore the heap property of the subtree rooted at j."""
        # Stop if root reached (no parent)
        if j == self._root():
            return

        # Move j up if it is smaller than its parent
        p = self._parent(j)
        if self._item(j) < self._item(p):
            self._swap(j, p)
            self._upheap(p)

    def _downheap(self, j: int) -> None:
        """Restore the heap property of the subtree rooted at j."""
        # Stop if no children (check left only since tree is complete)
        if not self._has_left(j):
            return

        # Get the smaller child
        left = self._left(j)
        small_child = left
        if self._has_right(j):
            right = self._right(j)
            if self._item(right) < self._item(left):
                small_child = right

        # Move j down if it is greater than its smaller child
        if self._item(small_child) < self._item(j):
            self._swap(j, small_child)
            self._downheap(small_child)

    def _item(self, j: int) -> Entry[K, V]:
        """Helper method to get the item at valid index j."""
        item = self._data[j]
        if item is None:
            raise ValueError("Item has not been set")
        return item

    def _root(self) -> int:
        """Get the root index with zero-based indexing."""
        return 0

    def _parent(self, j: int) -> int:
        """Get the parent index of j."""
        return (j - 1) // 2

    def _left(self, j: int) -> int:
        """Get the left child index of j."""
        return 2 * j + 1

    def _right(self, j: int) -> int:
        """Get the right child index of j."""
        return 2 * j + 2

    def _has_left(self, j: int) -> bool:
        """Return True if j has a left child."""
        return self._left(j) < self._size

    def _has_right(self, j: int) -> bool:
        """Return True if j has a right child."""
        return self._right(j) < self._size

    def _swap(self, i: int, j: int) -> None:
        """Swap the elements at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def __len__(self) -> int:
        return self._size
