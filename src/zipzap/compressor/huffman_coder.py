from zipzap.compressor.freq_counter import FreqCounter
from zipzap.compressor.huffman_tree import HuffmanTreeBuilder
from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.ds.maps.probe_hashmap import ProbeHashmap
from zipzap.ds.position import Position


class HuffmanCoderBase:
    """Shared helper methods for Huffman encoding and decoding."""

    @staticmethod
    def _generate_codebook(freq_table: Map[str, int]) -> Map[str, BitStream]:
        """Builds HuffmanTree and returns char -> BitStream mapping."""
        tree = HuffmanTreeBuilder.from_freq_table(freq_table)
        codebook = ProbeHashmap[str, BitStream]()

        # Return empty codebook if tree is empty
        root = tree.root()
        if root is None:
            return codebook

        # Return codebook with single character if tree has only one node
        if tree.is_leaf(root):
            node = root.element()
            codebook.put(node.char, BitStream("0"))
            return codebook

        def traverse(pos: Position, prefix: BitStream):
            """Recursively traverse tree to populate codebook."""
            if pos is None:
                return
            node = pos.element()
            # Reached leaf node, add prefix to codebook
            if tree.is_leaf(pos) and node.char is not None:
                codebook.put(node.char, prefix)
            else:
                # Traverse left and right children, appending "0" or "1" to the prefix
                left_pos = tree.left(pos)
                if left_pos:
                    traverse(left_pos, BitStream(prefix).append(0))
                right_pos = tree.right(pos)
                if right_pos:
                    traverse(right_pos, BitStream(prefix).append(1))

        traverse(root, BitStream())
        return codebook

    @staticmethod
    def _reverse_codebook(codes: Map[str, BitStream]) -> Map[BitStream, str]:
        """Reverse a codebook: BitStream -> character."""
        rev = ProbeHashmap[BitStream, str]()
        for k, v in codes.entries():
            rev.put(v, k)
        return rev


class HuffmanEncoder(HuffmanCoderBase):
    """Encodes text using Huffman coding."""

    def __init__(self, text: str):
        self.freq_table: Map[str, int] = FreqCounter(text)
        self.codebook: Map[str, BitStream] = self._generate_codebook(self.freq_table)

    def encode(self, text: str) -> BitStream:
        """Return encoded bitstream for text."""
        bits = BitStream()
        for c in text:
            code = self.codebook.get(c)
            if code:
                bits.extend(code)
        return bits


class HuffmanDecoder(HuffmanCoderBase):
    """Decodes Huffman-encoded bitstreams."""

    def __init__(self, freq_table: Map[str, int]):
        self.freq_table: Map[str, int] = freq_table
        self.codebook: Map[str, BitStream] = self._generate_codebook(freq_table)
        self.rev_codebook: Map[BitStream, str] = self._reverse_codebook(self.codebook)

    def decode(self, encoded: BitStream) -> str:
        """Return decoded text from encoded bitstream."""
        decoded = ""
        buffer = BitStream()
        for bit in encoded:
            buffer.append(bit)
            if c := self.rev_codebook.get(buffer):
                decoded += c
                buffer = BitStream()
        return decoded
