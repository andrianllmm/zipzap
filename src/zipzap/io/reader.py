from pathlib import Path

from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.ds.maps.probe_hashmap import ProbeHashmap
from zipzap.io.config import ZzConfig


class ZzReader:
    """Reads compressed data from a .zz file."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        # Ensure file exists
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def read(self) -> tuple[BitStream, Map[str, int]]:
        with self.file_path.open("rb") as f:
            code_lengths = ProbeHashmap[str, int]()

            # Read number of unique characters
            num_chars = int.from_bytes(f.read(ZzConfig.NUM_CHARS_SIZE), "big")

            # Read code lengths
            for _ in range(num_chars):
                char_len = int.from_bytes(f.read(ZzConfig.CHAR_LEN_SIZE), "big")
                char = f.read(char_len).decode("utf-8")
                code_len = int.from_bytes(f.read(ZzConfig.CODE_LEN_SIZE), "big")
                code_lengths.put(char, code_len)

            # Read bit length and encoded data
            bit_len = int.from_bytes(f.read(ZzConfig.BIT_LEN_SIZE), "big")
            data = bytearray(f.read())
            encoded = BitStream.from_bytearray(data, bit_len)

            return encoded, code_lengths
