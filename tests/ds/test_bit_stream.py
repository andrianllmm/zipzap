import pytest

from zipzap.ds.bits.bit_stream import BitStream


def test_append_single_bit():
    bs = BitStream()
    bs.append(1)
    assert list(bs) == [1]
    bs.append(0)
    assert list(bs) == [1, 0]


def test_append_invalid_bit():
    bs = BitStream()
    with pytest.raises(ValueError):
        bs.append(2)
    with pytest.raises(ValueError):
        bs.append(-1)
    with pytest.raises(ValueError):
        bs.append("2")


def test_extend():
    bs3 = BitStream()
    bs3.extend("101")
    assert list(bs3) == [1, 0, 1]

    bs4 = BitStream()
    bs4.extend([0, 1, 0])
    assert list(bs4) == [0, 1, 0]

    bs3 = BitStream("101")
    bs4 = BitStream()
    bs4.extend(bs3)
    assert list(bs4) == [1, 0, 1]


def test_to_bytearray():
    bs = BitStream("101")  # 3 bits
    data = bs.to_bytearray()
    # The last byte should be padded to 8 bits (shifted left)
    assert data[0] == 0b10100000

    bs2 = BitStream("11110000")
    data2 = bs2.to_bytearray()
    # No padding required
    assert data2[0] == 0b11110000


def test_from_bytearray():
    # bit length less than 8
    data = bytearray([0b10100000])
    bs = BitStream.from_bytearray(data, 3)
    assert list(bs) == [1, 0, 1]

    # bit length multiple of 8
    data2 = bytearray([0b11110000, 0b10101010])
    bs2 = BitStream.from_bytearray(data2)
    assert list(bs2) == [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]


def test_len_calculation():
    bs = BitStream("1010101")
    assert len(bs) == 7
    bs.append(0)
    assert len(bs) == 8


def test_iter():
    s = "1011"
    bs = BitStream(s)
    # Check that iterating over BitStream gives the correct bits
    assert list(bs) == [int(c) for c in s]


def test_indexing():
    bs = BitStream("1011")

    # Test each index individually
    assert bs[0] == 1
    assert bs[1] == 0
    assert bs[2] == 1
    assert bs[3] == 1

    # Test out-of-bounds access
    with pytest.raises(IndexError):
        _ = bs[4]
    with pytest.raises(IndexError):
        _ = bs[-1]  # negative indexing is not supported


def test_equality_and_hash():
    bs1 = BitStream("101")
    bs2 = BitStream("101")
    bs3 = BitStream("111")
    assert bs1 == bs2
    assert bs1 != bs3
    assert hash(bs1) == hash(bs2)
    assert hash(bs1) != hash(bs3)


def test_str():
    bs = BitStream("101")
    assert str(bs) == "101"
