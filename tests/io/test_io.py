import os
import tempfile

from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.probe_hashmap import ProbeHashmap
from zipzap.io.reader import ZzReader
from zipzap.io.writer import ZzWriter


def test_write_read_simple_bits():
    code_lengths = ProbeHashmap[str, int]()
    code_lengths.put("a", 2)
    code_lengths.put("b", 3)

    bits = BitStream([0, 1, 1, 0, 1, 0, 0, 1, 1])  # 9 bits, last byte partially filled

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        writer = ZzWriter(tmp_path)
        writer.write(bits, code_lengths)

        reader = ZzReader(tmp_path)
        read_bits, read_code_lengths = reader.read()

        # Compare code lengths
        for k, v in code_lengths.entries():
            assert read_code_lengths.get(k) == v

        # Compare bits
        assert len(read_bits) == len(bits)
        for i, bit in enumerate(bits):
            assert read_bits[i] == bit
    finally:
        os.remove(tmp_path)


def test_write_read_empty_bitstream():
    code_lengths = ProbeHashmap[str, int]()
    code_lengths.put("x", 1)

    bits = BitStream()  # empty

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        writer = ZzWriter(tmp_path)
        writer.write(bits, code_lengths)

        reader = ZzReader(tmp_path)
        read_bits, read_code_lengths = reader.read()

        assert len(read_bits) == 0
        assert read_code_lengths.get("x") == 1
    finally:
        os.remove(tmp_path)


def test_write_read_multibyte_characters():
    code_lengths = ProbeHashmap[str, int]()
    code_lengths.put("🚀", 2)
    code_lengths.put("你", 3)

    bits = BitStream([1, 0, 1, 1, 0, 0])  # 6 bits

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        writer = ZzWriter(tmp_path)
        writer.write(bits, code_lengths)

        reader = ZzReader(tmp_path)
        read_bits, read_code_lengths = reader.read()

        assert len(read_bits) == len(bits)
        for i, bit in enumerate(bits):
            assert read_bits[i] == bit

        for k, v in code_lengths.entries():
            assert read_code_lengths.get(k) == v
    finally:
        os.remove(tmp_path)


def test_write_read_large_bitstream():
    code_lengths = ProbeHashmap[str, int]()
    code_lengths.put("a", 1)

    # 1000 bits
    bits = BitStream([i % 2 for i in range(1000)])

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        writer = ZzWriter(tmp_path)
        writer.write(bits, code_lengths)

        reader = ZzReader(tmp_path)
        read_bits, read_code_lenghts = reader.read()

        assert len(read_bits) == len(bits)
        for i, bit in enumerate(bits):
            assert read_bits[i] == bit
        assert read_code_lenghts.get("a") == 1
    finally:
        os.remove(tmp_path)
