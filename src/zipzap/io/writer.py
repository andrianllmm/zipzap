from pathlib import Path

from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.io.config import ZzConfig


class ZzWriter:
    """Writes compressed data to a .zz file."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        # Ensure file exists and parent directories exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, freq_table: Map[str, int], encoded: BitStream) -> None:
        data = encoded.to_bytearray()
        bit_len = len(encoded)

        with self.file_path.open("wb") as f:
            # Number of unique characters
            f.write(len(freq_table).to_bytes(ZzConfig.NUM_CHARS_SIZE, "big"))

            # Write frequency table
            for char, freq in freq_table.entries():
                char_bytes = char.encode("utf-8")
                char_len = len(char_bytes)
                if char_len > 65535:
                    raise ValueError(f"Character too long to encode: {char}")

                f.write(char_len.to_bytes(ZzConfig.CHAR_LEN_SIZE, "big"))
                f.write(char_bytes)
                f.write(freq.to_bytes(ZzConfig.FREQ_SIZE, "big"))

            # Write bit length of encoded data
            f.write(bit_len.to_bytes(ZzConfig.BIT_LEN_SIZE, "big"))

            # Write encoded bytes
            f.write(data)
