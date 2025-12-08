import pytest
from zipzap.compressor.huffman_tree import HuffmanTreeBuilder, HuffmanNode


def test_empty_text():
    tree = HuffmanTreeBuilder.from_text("")
    assert tree.root() is None
    assert tree.is_empty()
    assert len(tree) == 0


def test_single_character_text():
    tree = HuffmanTreeBuilder.from_text("a")
    root = tree.root()
    assert root is not None
    node = root.element()
    assert isinstance(node, HuffmanNode)
    assert node.char == "a"
    assert node.freq == 1
    assert tree.left(root) is None
    assert tree.right(root) is None


def test_two_character_text():
    text = "ab"
    tree = HuffmanTreeBuilder.from_text(text)
    root = tree.root()
    assert root is not None
    node = root.element()
    # Root should have combined frequency
    assert node.freq == 2
    # Root should have two children
    left = tree.left(root)
    right = tree.right(root)
    assert left is not None
    assert right is not None
    left_node = left.element()
    right_node = right.element()
    assert {left_node.char, right_node.char} == {"a", "b"}
    assert {left_node.freq, right_node.freq} == {1, 1}


def test_huffman_structure():
    text = "aaabbbbcccdde"
    tree = HuffmanTreeBuilder.from_text(text)
    root = tree.root()
    assert root is not None
    # Root frequency equals total characters
    assert root.element().freq == len(text)

    _check_node(tree, root)


def _check_node(tree, pos):
    """Helper to validate internal node frequencies sum to children's frequencies"""
    left = tree.left(pos)
    right = tree.right(pos)
    if left and right:
        node_freq = pos.element().freq
        children_freq = left.element().freq + right.element().freq
        assert node_freq == children_freq
        _check_node(tree, left)
        _check_node(tree, right)
    elif left or right:
        # Should not have only one child in Huffman tree
        pytest.fail("Huffman tree node has only one child")
