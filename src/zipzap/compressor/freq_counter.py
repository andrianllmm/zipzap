from zipzap.ds.maps.probe_hashmap import ProbeHashmap


class FreqCounter(ProbeHashmap[str, int]):
    """Counts the frequency of each character in a string. Maps characters to their frequency."""

    def __init__(self, text: str):
        super().__init__(256)
        for c in text:
            if self.get(c) is None:
                self.put(c, 1)
            else:
                current_count = self.get(c)
                assert current_count is not None
                self.put(c, current_count + 1)
