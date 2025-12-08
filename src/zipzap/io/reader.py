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
            freq_table = ProbeHashmap[str, int]()

            # Read number of unique characters
            num_chars_bytes = f.read(ZzConfig.NUM_CHARS_SIZE)
            if len(num_chars_bytes) < ZzConfig.NUM_CHARS_SIZE:
                raise ValueError("Invalid .zz file header")
            num_chars = int.from_bytes(num_chars_bytes, "big")

            # Read frequency table
            for _ in range(num_chars):
                char_len_bytes = f.read(ZzConfig.CHAR_LEN_SIZE)
                if len(char_len_bytes) < ZzConfig.CHAR_LEN_SIZE:
                    raise ValueError("Invalid .zz file header")

                char_len = int.from_bytes(char_len_bytes, "big")
                char_bytes = f.read(char_len)
                if len(char_bytes) < char_len:
                    raise ValueError("Invalid .zz file header")

                char = char_bytes.decode("utf-8")

                freq_bytes = f.read(ZzConfig.FREQ_SIZE)
                if len(freq_bytes) < ZzConfig.FREQ_SIZE:
                    raise ValueError("Invalid .zz file header")
                freq = int.from_bytes(freq_bytes, "big")

                freq_table.put(char, freq)

            # Read bit length
            bit_length_bytes = f.read(ZzConfig.BIT_LEN_SIZE)
            if len(bit_length_bytes) < ZzConfig.BIT_LEN_SIZE:
                raise ValueError("Invalid .zz file: missing bit length")
            bit_length = int.from_bytes(bit_length_bytes, "big")

            # Read encoded bytes
            encoded_bytes = f.read()
            encoded = BitStream.from_bytearray(
                bytearray(encoded_bytes), bit_length=bit_length
            )

            return encoded, freq_table
