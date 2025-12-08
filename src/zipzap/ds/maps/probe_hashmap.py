from typing import Iterator, Optional, TypeVar

from zipzap.ds.array import Array
from zipzap.ds.entry import Entry
from zipzap.ds.maps.hashmap import Hashmap

K = TypeVar("K")
V = TypeVar("V")


class Tombstone:
    """Represents a deleted bucket."""

    ...


TOMBSTONE = Tombstone()


class ProbeHashmap(Hashmap[K, V]):
    """Hashmap implementation using open addressing."""

    def __init__(self, slots: int = 211) -> None:
        super().__init__(slots)
        # Specify array contents type (for type checking)
        self._table: Array[Entry[K, V] | Tombstone | None] = Array(slots)

    def _probe(self, key: K, i: int) -> int:
        """Probe function using double hashing."""
        return i * self._hash2(key)

    def _hash2(self, key: K) -> int:
        """Secondary hash function for probing."""
        q = self._slots - 2  # q < N
        return q - (self._hash_index(key) % q)

    def get(self, key: K) -> Optional[V]:
        start_index = self._hash_index(key)
        index = start_index
        i = 0  # Number of probes

        while True:
            entry = self._table[index]

            # Key not found
            if entry is None:
                return None

            # Key found
            elif (
                entry is not TOMBSTONE and isinstance(entry, Entry) and entry.key == key
            ):
                return entry.value

            i += 1
            index = self._compress(start_index + self._probe(key, i))

            if index == start_index:
                return None  # Full cycle, key not found

    def put(self, key: K, value: V) -> Optional[V]:
        if self._size == self._slots:
            self._expand()

        start_index = self._hash_index(key)
        index = start_index
        first_tombstone = None
        i = 0

        while True:
            entry = self._table[index]

            # Key not found
            if entry is None:
                # Insert at first tombstone if available, else here
                target_index = first_tombstone if first_tombstone is not None else index
                self._table[target_index] = Entry(key, value)
                self._size += 1
                return None

            # First tombstone found
            elif entry is TOMBSTONE and first_tombstone is None:
                # Remember first tombstone for possible reuse
                first_tombstone = index

            # Key found
            elif isinstance(entry, Entry) and entry.key == key:
                # Update value
                old_value = entry.value
                entry.value = value
                return old_value

            i += 1
            index = self._compress(start_index + self._probe(key, i))

            if index == start_index:
                return None  # Full cycle, key not found (table full)

    def remove(self, key: K) -> Optional[V]:
        start_index = self._hash_index(key)
        index = start_index
        i = 0

        while True:
            entry = self._table[index]

            # Key not found
            if entry is None:
                return None

            # Key found
            elif (
                entry is not TOMBSTONE and isinstance(entry, Entry) and entry.key == key
            ):
                # Mark entry as tombstone
                old_value = entry.value
                self._table[index] = TOMBSTONE
                self._size -= 1
                return old_value

            i += 1
            index = self._compress(start_index + self._probe(key, i))

            if index == start_index:
                return None  # Full cycle, key not found

    def entries(self) -> Iterator[Entry[K, V]]:
        # Traverse each bucket
        for i in range(self._table.capacity):
            entry = self._table[i]
            if entry is not TOMBSTONE and isinstance(entry, Entry):
                yield entry

    def _expand(self):
        """Helper method to expand table when full."""
        old_table = self._table
        old_slots = self._slots

        # Double size of table
        self._slots = 2 * old_slots + 1
        self._table = Array(self._slots)
        self._size = 0

        # Copy old table entries to new table
        for i in range(old_slots):
            entry = old_table[i]
            if entry is not TOMBSTONE and isinstance(entry, Entry):
                self.put(entry.key, entry.value)
