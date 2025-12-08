from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator, Optional, TypeVar

from zipzap.ds.deques.linked_deque import LinkedDeque
from zipzap.ds.position import Position

T = TypeVar("T")


class Tree(ABC, Generic[T]):
    """Abstract tree structure."""

    @abstractmethod
    def root(self) -> Optional[Position]:
        """Return the root position of the tree (None if empty)."""
        ...

    @abstractmethod
    def parent(self, p: Position) -> Optional[Position]:
        """Return the position of the parent of p (None if p is root)."""
        ...

    @abstractmethod
    def num_children(self, p: Position) -> int:
        """Return the number of children of p."""
        ...

    @abstractmethod
    def children(self, p: Position) -> Iterator[Position]:
        """Generate an iterator over the children of p."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of positions in the tree."""
        ...

    def is_empty(self) -> bool:
        """Return True if the tree has no positions."""
        return len(self) == 0

    def is_root(self, p: Position) -> bool:
        """Return True if p is the root of the tree."""
        return self.root() == p

    def is_leaf(self, p: Position) -> bool:
        """Return True if p is a leaf node (has no children)."""
        return self.num_children(p) == 0

    def depth(self, p: Optional[Position]) -> int:
        """Return the depth of position p (distance from root)."""
        if p is None:
            raise ValueError("Cannot compute depth of None")
        return 0 if self.is_root(p) else 1 + self.depth(self.parent(p))

    def height(self, p: Optional[Position] = None) -> int:
        """Return the height of the subtree rooted at p (or entire tree if p is None)."""
        if p is None:
            p = self.root()
            if p is None:
                raise ValueError("Cannot compute height of empty tree")
        return (
            0 if self.is_leaf(p) else 1 + max(self.height(c) for c in self.children(p))
        )

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over all items in the tree."""
        for p in self.positions():
            yield p.element()

    def positions(self) -> Iterator[Position]:
        """Return an iterator over all positions in the tree."""
        return self.preorder()

    def preorder(self) -> Iterator[Position]:
        """Generate a pre-order (depth-first) iteration of positions."""
        root = self.root()
        if root is not None:
            yield from self._preorder(root)

    def _preorder(self, p: Position) -> Iterator[Position]:
        yield p
        for c in self.children(p):
            yield from self._preorder(c)

    def postorder(self) -> Iterator[Position]:
        """Generate a post-order (depth-first) iteration of positions."""
        root = self.root()
        if root is not None:
            yield from self._postorder(root)

    def _postorder(self, p: Position) -> Iterator[Position]:
        for c in self.children(p):
            yield from self._postorder(c)
        yield p

    def level_order(self) -> Iterator[Position]:
        """Generate a level-order (breadth-first) iteration of positions."""
        root = self.root()
        if root is None:
            return

        queue = LinkedDeque[Position]()
        queue.add_last(root)
        while queue:
            p = queue.delete_first()
            if p is None:
                continue
            yield p
            for c in self.children(p):
                queue.add_last(c)
