import pytest
from zipzap.ds.linked_list_nodes import DLLNode, LinkedNode, SLLNode


def test_item_property():
    node1 = LinkedNode()
    with pytest.raises(ValueError):
        _ = node1.item
    node1.item = 10
    assert node1.item == 10
    node2 = LinkedNode(5)
    assert node2.item == 5


def test_sllnode_links():
    node1 = SLLNode(1)
    node2 = SLLNode(2)
    assert node1.next is None
    node1.next = node2
    assert node1.next is node2


def test_dllnode_links():
    node1 = DLLNode(1)
    node2 = DLLNode(2)
    assert node1.next is None
    assert node1.prev is None
    node1.next = node2
    node2.prev = node1
    assert node1.next is node2
    assert node2.prev is node1
