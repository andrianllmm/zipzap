from __future__ import annotations

from typing import Generator


class BitStream:
    """Stores bits in a bytearray with most significant bit (MSB) first per byte."""

    def __init__(self, bits: str | list[int] | "BitStream" | None = None) -> None:
        """Initialize the BitStream optionally from bits."""
        self._bytes: bytearray = bytearray()  # Stores the bytes containing bits
        self._bit_len: int = 0  # Total number of bits in the BitStream

        # Initialize from bits if provided
        if bits is not None:
            self.extend(bits)

    def append(self, bit: int | str) -> "BitStream":
        """Append a single bit (0 or 1) to the BitStream."""
        # Convert string to int if necessary
        if isinstance(bit, str):
            bit = int(bit)

        # Validate bit
        if bit not in (0, 1):
            raise ValueError("Bit must be 0 or 1")

        # Determine byte and bit index in that byte
        byte_idx = self._bit_len // 8
        bit_idx = self._bit_len % 8

        # Start a new byte if at the beginning of a byte
        if bit_idx == 0:
            self._bytes.append(0)

        # Store bit into the target byte.
        #   Bits are written in big-endian order; 1st bit goes into the most significant position (7).
        #   Shift (<<) the bit to MSB so it lands at the correct position.
        #   Set (|) the bit into the byte.
        self._bytes[byte_idx] |= bit << (7 - bit_idx)

        # Increment total bit count
        self._bit_len += 1

        # Return self for chaining
        return self

    def extend(self, bits: str | list[int] | "BitStream") -> "BitStream":
        """Append multiple bits to the BitStream."""
        # Append each bit individually
        for b in bits:
            self.append(b)

        # Return self for chaining
        return self

    def to_bytearray(self) -> bytearray:
        """Return the BitStream as a bytearray (last byte may be partially filled)."""
        return self._bytes.copy()

    @classmethod
    def from_bytearray(
        cls, data: bytearray, bit_length: int | None = None
    ) -> "BitStream":
        """Create a BitStream from a bytearray and optional bit length."""
        bs = cls()
        bs._bytes = data.copy()
        bs._bit_len = len(data) * 8 if bit_length is None else bit_length
        return bs

    def copy(self) -> "BitStream":
        """Return a new BitStream with the same bits."""
        new_bs = BitStream()
        new_bs._bytes = self._bytes.copy()
        new_bs._bit_len = self._bit_len
        return new_bs

    def __len__(self) -> int:
        """Return the total number of bits in the BitStream."""
        return self._bit_len

    def __iter__(self) -> Generator[int, None, None]:
        """Iterate over each bit in the BitStream (0 or 1)."""
        for i in range(self._bit_len):
            yield self[i]

    def __getitem__(self, idx: int) -> int:
        """Return the bit at the given index (0-based)."""
        if not (0 <= idx < self._bit_len):
            raise IndexError("BitStream index out of range")

        # Determine byte and bit index
        byte_idx = idx // 8
        bit_idx = idx % 8

        # Extract the bit at the given index
        #   Bits are read in big-endian order; 1st bit is at the most significant position (7).
        #   Shift (>>) the bit to the LSB so it lands at the correct position,
        #   Mask (& 1) to keep only that single bit.
        return (self._bytes[byte_idx] >> (7 - bit_idx)) & 1

    def __eq__(self, other: object) -> bool:
        """Check equality between two BitStreams."""
        if not isinstance(other, BitStream):
            return False
        if self._bit_len != other._bit_len:
            return False
        return all(a == b for a, b in zip(self, other))

    def __hash__(self) -> int:
        """Compute a hash based on the bits in the BitStream."""
        return hash(tuple(self))

    def __str__(self) -> str:
        """Return a string representation of the bits (e.g., '1010')."""
        return "".join(str(b) for b in self)

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"{self.__class__.__name__}({str(self)})"
