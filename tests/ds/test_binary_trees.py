from typing import Type

import pytest

from zipzap.ds.trees.binary_tree import BinaryTree
from zipzap.ds.trees.linked_binary_tree import LinkedBinaryTree


@pytest.fixture(params=[LinkedBinaryTree])
def BinaryTreeClass(request) -> Type[BinaryTree]:
    return request.param


def test_empty_tree(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()
    assert tree.is_empty()
    assert len(tree) == 0
    assert tree.root() is None


def test_add_root(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()
    pos = tree.add_root("root")

    assert tree.root() == pos
    assert tree.is_root(pos)

    assert not tree.is_empty()
    assert len(tree) == 1
    assert tree.num_children(pos) == 0
    assert tree.depth(pos) == 0
    assert tree.height(pos) == 0


def test_add_children(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()
    root = tree.add_root("root")
    left = tree.add_left(root, "left")
    right = tree.add_right(root, "right")

    assert tree.left(root) == left
    assert tree.right(root) == right

    children = list(tree.children(root))
    assert children == [left, right]

    assert tree.sibling(left) == right
    assert tree.sibling(right) == left

    assert tree.is_leaf(left)
    assert tree.is_leaf(right)

    assert len(tree) == 3
    assert tree.num_children(root) == 2
    assert tree.depth(left) == 1
    assert tree.depth(right) == 1
    assert tree.height(root) == 1


def test_replace(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()

    root = tree.add_root("root")
    old = tree.replace(root, "new_root")
    assert old == "root"
    assert root.element() == "new_root"


def test_delete_root(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()

    root = tree.add_root("root")

    val = tree.delete(root)
    assert val == "root"
    assert tree.root() is None
    assert tree.is_empty()
    assert len(tree) == 0


def test_delete_leaf(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()
    root = tree.add_root("root")
    left = tree.add_left(root, "left")
    right = tree.add_right(root, "right")

    val = tree.delete(left)
    assert val == "left"
    assert tree.left(root) is None
    assert tree.num_children(root) == 1
    assert len(tree) == 2

    val = tree.delete(right)
    assert val == "right"
    assert tree.right(root) is None
    assert tree.num_children(root) == 0
    assert len(tree) == 1


def test_delete_node_with_one_child(BinaryTreeClass):
    tree: BinaryTree[str] = BinaryTreeClass()
    root = tree.add_root("root")
    left = tree.add_left(root, "left")
    tree.add_left(left, "left_left")

    val = tree.delete(left)
    assert val == "left"

    new_left = tree.left(root)
    assert new_left is not None
    assert new_left.element() == "left_left"
    assert tree.parent(new_left) == root
    assert tree.num_children(root) == 1
    assert len(tree) == 2


def test_attach_trees(BinaryTreeClass):
    tree1: BinaryTree[str] = BinaryTreeClass()
    tree2: BinaryTree[str] = BinaryTreeClass()
    tree3: BinaryTree[str] = BinaryTreeClass()

    root1 = tree1.add_root("root1")
    tree2_root = tree2.add_root("root2")
    tree3_root = tree3.add_root("root3")

    leaf1 = tree1.add_left(root1, "leaf1")
    tree2.add_left(tree2_root, "leaf2")
    tree3.add_right(tree3_root, "leaf3")

    tree1.attach(leaf1, tree2, tree3)

    left1 = tree1.left(root1)
    assert left1 is not None and left1.element() == "leaf1"

    left_child = tree1.left(left1)
    right_child = tree1.right(left1)

    assert left_child is not None and left_child.element() == "root2"
    assert right_child is not None and right_child.element() == "root3"

    left_grandchild = tree1.left(left_child)
    right_grandchild = tree1.right(right_child)

    assert left_grandchild is not None and left_grandchild.element() == "leaf2"
    assert right_grandchild is not None and right_grandchild.element() == "leaf3"

    assert tree2.is_empty()
    assert tree3.is_empty()


def test_traversals(BinaryTreeClass):
    tree = BinaryTreeClass()
    r = tree.add_root("r")
    a = tree.add_left(r, "a")
    tree.add_right(r, "b")
    tree.add_left(a, "c")
    tree.add_right(a, "d")

    inorder_vals = [p.element() for p in tree.positions()]
    assert inorder_vals == ["c", "a", "d", "r", "b"]

    preorder_vals = [p.element() for p in tree.preorder()]
    assert preorder_vals == ["r", "a", "c", "d", "b"]

    postorder_vals = [p.element() for p in tree.postorder()]
    assert postorder_vals == ["c", "d", "a", "b", "r"]

    level_vals = [p.element() for p in tree.level_order()]
    assert level_vals == ["r", "a", "b", "c", "d"]
