from typing import Optional

from zipzap.compressor.freq_counter import FreqCounter
from zipzap.ds.maps.map import Map
from zipzap.ds.priority_queues.heap_priority_queue import HeapPriorityQueue
from zipzap.ds.trees.linked_binary_tree import LinkedBinaryTree


class HuffmanNode:
    """Node class for HuffmanTree."""

    def __init__(self, freq: int, char: Optional[str] = None):
        self.freq = freq
        self.char = char  # None for internal nodes

    def __lt__(self, other: "HuffmanNode"):
        return self.freq < other.freq


class HuffmanTree(LinkedBinaryTree[HuffmanNode]):
    """Pure tree representation for Huffman coding."""

    ...


class HuffmanTreeBuilder:
    """Builds HuffmanTree from text or frequency table."""

    @staticmethod
    def from_text(text: str) -> HuffmanTree:
        """Build HuffmanTree from text."""
        freq_counter = FreqCounter(text)
        return HuffmanTreeBuilder.from_freq_table(freq_counter)

    @staticmethod
    def from_freq_table(freq_table: Map[str, int]) -> HuffmanTree:
        """Build HuffmanTree from frequency table."""
        # Convert frequency table to list of nodes
        nodes = [HuffmanNode(f, c) for c, f in freq_table.entries()]

        return HuffmanTreeBuilder.from_nodes(nodes)

    @staticmethod
    def from_nodes(nodes: list[HuffmanNode]) -> HuffmanTree:
        """Build HuffmanTree from list of nodes."""
        pq = HeapPriorityQueue[int, HuffmanTree](256)

        # Create tree for each node
        for node in nodes:
            tree = HuffmanTree()
            tree.add_root(node)
            pq.add(node.freq, tree)

        # Merge trees until only one remains
        while len(pq) > 1:
            e1, e2 = pq.remove_min(), pq.remove_min()
            t1, t2 = e1.value, e2.value
            combined_freq = e1.key + e2.key
            new_tree = HuffmanTree()
            root_pos = new_tree.add_root(HuffmanNode(combined_freq))
            new_tree.attach(root_pos, t1, t2)
            pq.add(combined_freq, new_tree)

        # Return the remaining tree
        return pq.remove_min().value if not pq.is_empty() else HuffmanTree()
