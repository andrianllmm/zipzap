from typing import Generic, Optional, TypeVar, cast

from zipzap.ds.position import Position
from zipzap.ds.trees.binary_tree import BinaryTree

T = TypeVar("T")


class BTNode(Generic[T]):
    """Node class for LinkedBinaryTree."""

    __slots__ = ("_element", "_parent", "_left", "_right")

    def __init__(
        self,
        element: T,
        parent: Optional["BTNode"] = None,
        left: Optional["BTNode"] = None,
        right: Optional["BTNode"] = None,
    ):
        self._element = element
        self._parent = parent
        self._left = left
        self._right = right


class BTPosition(Position, Generic[T]):
    """Position class for LinkedBinaryTree."""

    __slots__ = ("_container", "_node")

    def __init__(self, container: "LinkedBinaryTree", node: "BTNode"):
        self._container = container
        self._node = node

    def element(self) -> T:
        return self._node._element

    def __eq__(self, other):
        return type(other) is type(self) and other._node is self._node


class LinkedBinaryTree(BinaryTree[T]):
    """Linked representation of a binary tree structure."""

    def __init__(self):
        self._root = None
        self._size = 0

    def root(self) -> Optional[Position]:
        if self._root is None:
            return None
        return self._make_position(self._root)

    def parent(self, p: Position) -> Optional[Position]:
        node = self._validate(p)
        if node._parent is None:
            return None
        return self._make_position(node._parent)

    def left(self, p: Position) -> Optional[Position]:
        node = self._validate(p)
        if node._left is None:
            return None
        return self._make_position(node._left)

    def right(self, p: Position) -> Optional[Position]:
        node = self._validate(p)
        if node._right is None:
            return None
        return self._make_position(node._right)

    def add_root(self, e: T) -> Position:
        if self._root is not None:
            raise ValueError("Root exists")

        self._size = 1
        self._root = BTNode(e)
        return self._make_position(self._root)

    def add_left(self, p: Position, e: T) -> Position:
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Left child exists")

        self._size += 1
        node._left = BTNode(e, node)  # node is its parent
        return self._make_position(node._left)

    def add_right(self, p: Position, e: T) -> Position:
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Right child exists")

        self._size += 1
        node._right = BTNode(e, node)  # node is its parent
        return self._make_position(node._right)

    def replace(self, p: Position, e: T) -> T:
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def delete(self, p: Position) -> T:
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError("Position has two children")

        child = node._left if node._left else node._right

        if child is not None:
            child._parent = node._parent  # child's grandparent becomes parent

        if node is self._root:
            self._root = child  # child becomes root
        else:
            parent = node._parent
            assert parent is not None
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child

        self._size -= 1
        node._parent = node  # convention for deprecated node
        return node._element

    def attach(self, p: Position, t1: BinaryTree, t2: BinaryTree) -> None:
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError("position must be leaf")
        if not isinstance(t1, LinkedBinaryTree) or not isinstance(t2, LinkedBinaryTree):
            raise TypeError("Trees must be of type LinkedBinaryTree")
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Tree types must match")

        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            # attached t1 as left subtree of node
            assert t1._root is not None
            t1._root._parent = node
            node._left = t1._root
            t1._root = None  # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():
            # attached t2 as right subtree of node
            assert t2._root is not None
            t2._root._parent = node
            node._right = t2._root
            t2._root = None  # set t2 instance to empty
            t2._size = 0

    def __len__(self):
        return self._size

    def _validate(self, p: Position) -> "BTNode":
        """Return associated node, if position is valid."""
        if not isinstance(p, BTPosition):
            raise TypeError("p must be proper LBTPosition type")
        p = cast(BTPosition, p)
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node: BTNode) -> Position:
        """Return Position instance for given node (or None if no node)."""
        return BTPosition(self, node)
