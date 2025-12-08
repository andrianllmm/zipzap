from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional, TypeVar

from zipzap.ds.position import Position
from zipzap.ds.trees.tree import Tree

T = TypeVar("T")


class BinaryTree(Tree[T], ABC):
    """Abstract base binary tree structure."""

    @abstractmethod
    def left(self, p: Position) -> Optional[Position]:
        """Return the left child of position p (None if no left child)."""
        ...

    @abstractmethod
    def right(self, p: Position) -> Optional[Position]:
        """Return the right child of position p (None if no right child)."""
        ...

    @abstractmethod
    def add_root(self, e: T) -> Position:
        """Place element e at the root of an empty tree and return new Position."""
        ...

    @abstractmethod
    def add_left(self, p: Position, e: T) -> Position:
        """Create a new left child for Position p, storing element e."""
        ...

    @abstractmethod
    def add_right(self, p: Position, e: T) -> Position:
        """Create a new right child for Position p, storing element e."""
        ...

    @abstractmethod
    def replace(self, p: Position, e: T) -> T:
        """Replace the element at position p with e, and return old element."""
        ...

    @abstractmethod
    def delete(self, p: Position) -> T:
        """Delete the node at Position p, and replace it with its child, if any."""
        ...

    @abstractmethod
    def attach(self, p: Position, t1: BinaryTree, t2: BinaryTree) -> None:
        """Attach trees t1 and t2, respectively, as the left and right subtrees of the external Position p.

        As a side effect, set t1 and t2 to empty.
        """
        ...

    def sibling(self, p: Position) -> Optional[Position]:
        """Return the sibling of Position p (None if no sibling)."""
        parent = self.parent(p)
        if parent is None:
            return None  # root has no sibling
        if p == self.left(parent):
            return self.right(parent)  # may be None
        return self.left(parent)  # may be None

    def children(self, p: Position) -> Iterator[Position]:
        """Generate an iteration of Position p's children (left then right)."""
        left = self.left(p)
        right = self.right(p)
        if left is not None:
            yield left
        if right is not None:
            yield right

    def num_children(self, p: Position) -> int:
        count = 0
        if self.left(p) is not None:
            count += 1
        if self.right(p) is not None:
            count += 1
        return count

    def positions(self) -> Iterator[Position]:
        return self.inorder()

    def inorder(self) -> Iterator[Position]:
        """Generate an inorder iteration of positions in the tree."""
        root = self.root()
        if root is not None:
            yield from self._inorder(root)

    def _inorder(self, p: Position) -> Iterator[Position]:
        """Recursive helper for inorder traversal of subtree rooted at p."""
        left = self.left(p)
        right = self.right(p)
        if left is not None:
            yield from self._inorder(left)
        yield p
        if right is not None:
            yield from self._inorder(right)
