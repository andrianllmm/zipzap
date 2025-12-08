from typing import TypeVar

from zipzap.ds.array import Array
from zipzap.ds.maps.map import Map

K = TypeVar("K")
V = TypeVar("V")


class Hashmap(Map[K, V]):
    """An abstract hashmap storing key-value pairs."""

    def __init__(self, slots: int = 101) -> None:
        self._table: Array = Array(slots)
        self._slots: int = slots
        self._size: int = 0

    def _hash_code(self, key: K) -> int:
        """Compute an integer hash code for a string key."""
        if isinstance(key, str):
            # For strings, use polynomial rolling hash
            hash_val = 0
            p = 31
            for c in key:
                hash_val = hash_val * p + ord(c)
            return hash_val
        elif isinstance(key, int):
            # For integers, use the integer itself
            return key
        else:
            # Fallback: use Python's built-in hash
            return hash(key)

    def _compress(self, hash_code: int) -> int:
        """Compress a hash code to a valid index in the table."""
        return hash_code % self._slots

    def _hash_index(self, key: K) -> int:
        """Convenience method to get the final table index for a key."""
        return self._compress(self._hash_code(key))

    def __len__(self) -> int:
        return self._size
