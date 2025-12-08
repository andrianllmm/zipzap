from zipzap.compressor.freq_counter import FreqCounter
from zipzap.compressor.huffman_tree import HuffmanTreeBuilder
from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.probe_hashmap import ProbeHashmap
from zipzap.ds.maps.map import Map
from zipzap.ds.position import Position


class HuffmanEncoder:
    """Encodes text using Huffman coding and stores only the frequency table."""

    def __init__(self, text: str):
        self.text = text
        self.freq_table: Map[str, int] = FreqCounter(text)

        self.tree = HuffmanTreeBuilder.from_freq_table(self.freq_table)
        self.root = self.tree.root()

        self.codebook: Map[str, BitStream] = self._generate_codebook()

    def encode(self, text: str) -> BitStream:
        """Encode the original text using the codebook."""
        bits = BitStream()
        for c in text:
            if code := self.codebook.get(c):
                bits.extend(code)
        return bits

    def _generate_codebook(self) -> Map[str, BitStream]:
        """Generate mapping of character to BitStream codes using."""
        codebook = ProbeHashmap[str, BitStream]()

        root = self.root
        if root is None:
            return codebook

        # If only one character, return a single code
        if self.tree.is_leaf(root):
            node = root.element()
            codebook.put(node.char, BitStream("0"))
            return codebook

        def _traverse(pos: Position, prefix: BitStream):
            """Helper to traverse tree and populate codebook."""
            node = pos.element()

            # Leaf means we've reached a character
            if self.tree.is_leaf(pos):
                codebook.put(node.char, prefix)
                return

            left = self.tree.left(pos)
            if left:
                new_prefix = prefix.copy()
                new_prefix.append(0)
                _traverse(left, new_prefix)

            right = self.tree.right(pos)
            if right:
                new_prefix = prefix.copy()
                new_prefix.append(1)
                _traverse(right, new_prefix)

        _traverse(root, BitStream())

        return codebook


class HuffmanDecoder:
    """Decodes Huffman-encoded data by walking the tree directly."""

    def __init__(self, freq_table: Map[str, int]):
        self.freq_table = freq_table
        self.tree = HuffmanTreeBuilder.from_freq_table(freq_table)
        self.root = self.tree.root()

    def decode(self, encoded: BitStream) -> str:
        """Decode by traversing the Huffman tree bit-by-bit."""

        root = self.root

        # Return empty string if tree is empty
        if root is None:
            return ""

        # Repeat the root character if tree has only one node
        if self.tree.is_leaf(root):
            char = root.element().char
            return char * len(encoded)

        decoded_chars = []
        node = root

        for bit in encoded:
            # Move down the tree
            if bit == 0:
                next_node = self.tree.left(node)
            else:
                next_node = self.tree.right(node)

            if next_node is None:
                # This should never happen in a valid Huffman tree
                raise RuntimeError("Invalid Huffman bitstream: reached a None node.")

            node = next_node

            # If leaf, emit and reset to root
            if self.tree.is_leaf(node):
                decoded_chars.append(node.element().char)
                node = root

        return "".join(decoded_chars)
