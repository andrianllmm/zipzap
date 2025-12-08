from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.ds.maps.probe_hashmap import ProbeHashmap


def compute_codebook(code_lengths: Map[str, int]) -> Map[str, BitStream]:
    """Return canonical Huffman codes as BitStream given code lengths."""
    # Sort symbols by (length, then character)
    sorted_symbols = sorted(code_lengths.entries(), key=lambda x: (x.value, x.key))

    codes = ProbeHashmap[str, BitStream]()
    code = 0
    prev_len = 0

    for char, length in sorted_symbols:
        # Shift left if length increased
        code <<= length - prev_len
        # Convert code integer to binary string, pad with zeros to match length
        code_bits = format(code, f"0{length}b")
        # Store as BitStream
        codes.put(char, BitStream(code_bits))
        # Increment code for next symbol
        code += 1
        prev_len = length

    return codes
