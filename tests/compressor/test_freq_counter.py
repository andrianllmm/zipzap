from zipzap.compressor.freq_counter import FreqCounter


def test_empty_string():
    counter = FreqCounter("")
    assert counter.is_empty()
    assert len(counter) == 0
    assert list(counter.entries()) == []


def test_single_character():
    counter = FreqCounter("a")
    assert counter.get("a") == 1
    assert counter.get("b") is None


def test_unique_characters():
    text = "abc"
    counter = FreqCounter(text)
    for c in text:
        assert counter.get(c) == 1
    assert counter.get("d") is None


def test_repeated_characters():
    text = "aabbcbcaa"
    counter = FreqCounter(text)
    assert counter.get("a") == 4
    assert counter.get("b") == 3
    assert counter.get("c") == 2


def test_non_alpha_characters():
    text = "1!@#$%^&*()"
    counter = FreqCounter(text)
    assert counter.get("1") == 1
    assert counter.get("!") == 1
    assert counter.get("@") == 1
    assert counter.get("#") == 1
    assert counter.get("$") == 1
    assert counter.get("%") == 1
    assert counter.get("^") == 1
    assert counter.get("&") == 1
    assert counter.get("*") == 1
    assert counter.get("(") == 1
    assert counter.get(")") == 1
