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

    def write(self, encoded: BitStream, code_lengths: Map[str, int]) -> None:
        data = encoded.to_bytearray()
        bit_len = len(encoded)

        with self.file_path.open("wb") as f:
            # Write number of unique characters
            f.write(len(code_lengths).to_bytes(ZzConfig.NUM_CHARS_SIZE, "big"))

            # Write code lengths
            for char, code_len in code_lengths.entries():
                char_bytes = char.encode("utf-8")
                f.write(len(char_bytes).to_bytes(ZzConfig.CHAR_LEN_SIZE, "big"))
                f.write(char_bytes)
                f.write(code_len.to_bytes(ZzConfig.CODE_LEN_SIZE, "big"))

            # Write bit length and encoded data
            f.write(bit_len.to_bytes(ZzConfig.BIT_LEN_SIZE, "big"))
            f.write(data)
