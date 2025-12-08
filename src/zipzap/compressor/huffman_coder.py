from zipzap.compressor.code_lengths import compute_code_lengths
from zipzap.compressor.codebook import compute_codebook
from zipzap.compressor.freq_counter import FreqCounter
from zipzap.compressor.huffman_tree import HuffmanTreeBuilder
from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.ds.maps.probe_hashmap import ProbeHashmap


class HuffmanEncoder:
    """Encodes text to Huffman-encoded data."""

    def __init__(self, text: str):
        self.text = text
        self.freq_table = FreqCounter(text)
        self.tree = HuffmanTreeBuilder.from_freq_table(self.freq_table)
        self.code_lengths = compute_code_lengths(self.tree)
        self.codebook = compute_codebook(self.code_lengths)

    def encode(self, text: str) -> BitStream:
        bits = BitStream()
        for c in text:
            if code := self.codebook.get(c):
                bits.extend(code)
        return bits


class HuffmanDecoder:
    """Decodes Huffman-encoded data to text."""

    def __init__(self, code_lengths: Map[str, int]):
        self.code_lengths = code_lengths
        self.codebook = compute_codebook(code_lengths)
        self.inverse_codebook = ProbeHashmap[BitStream, str]()
        for char, code in self.codebook.entries():
            self.inverse_codebook.put(code, char)

    def decode(self, encoded: BitStream) -> str:
        result = []
        acc = BitStream()  # accumulate bits

        for bit in encoded:
            acc.append(bit)
            if char := self.inverse_codebook.get(acc):
                result.append(char)
                acc = BitStream()  # reset accumulator

        if len(acc) > 0:
            raise ValueError(
                "Encoded bitstream has leftover bits that do not match any code"
            )

        return "".join(result)
