from zipzap.compressor.huffman_tree import HuffmanTree
from zipzap.ds.maps.map import Map
from zipzap.ds.maps.probe_hashmap import ProbeHashmap


def compute_code_lengths(tree: HuffmanTree) -> Map[str, int]:
    """Return a map of character to code length."""
    code_lengths = ProbeHashmap[str, int]()

    def dfs(node, depth):
        if node.element().char is not None:
            code_lengths.put(node.element().char, depth)
            return
        children = list(tree.children(node))
        for child in children:
            dfs(child, depth + 1)

    if not tree.is_empty():
        dfs(tree.root(), 0)

    return code_lengths
