from zipzap.ds.maps.probe_hashmap import ProbeHashmap


class FreqCounter(ProbeHashmap[str, int]):
    """Counts the frequency of each character in a string. Maps characters to their frequency."""

    def __init__(self, text: str):
        super().__init__(256)
        for c in text:
            current = self.get(c) or 0
            self.put(c, current + 1)
