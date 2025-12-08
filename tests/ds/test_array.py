import pytest
from zipzap.ds.array import Array


def test_initialization():
    arr = Array()
    for i in range(arr.capacity):
        assert arr[i] is None


def test_initialization_custom_capacity():
    arr = Array(10)
    assert arr.capacity == 10
    for i in range(arr.capacity):
        assert arr[i] is None


def test_initialization_invalid_capacity():
    with pytest.raises(ValueError):
        Array(0)
    with pytest.raises(ValueError):
        Array(-1)


def test_get_set_item():
    arr = Array(5)
    arr[0] = 1
    arr[2] = 2
    arr[4] = 3
    assert arr[0] == 1
    assert arr[2] == 2
    assert arr[4] == 3


def test_index_out_of_bounds():
    arr = Array(3)
    with pytest.raises(IndexError):
        arr[-1]
    with pytest.raises(IndexError):
        arr[3]
    with pytest.raises(IndexError):
        arr[-1] = "a"
    with pytest.raises(IndexError):
        arr[3] = "b"


def test_resize_grow():
    arr = Array(3)
    arr[0] = "a"
    arr[1] = "b"
    arr.resize(5)
    assert arr.capacity == 5
    assert arr[0] == "a"
    assert arr[1] == "b"
    for i in range(3, 5):
        assert arr[i] is None


def test_resize_shrink():
    arr = Array(3)
    arr[0] = "a"
    arr[1] = "b"
    arr.resize(1)
    assert arr.capacity == 1
    assert arr[0] == "a"
    with pytest.raises(IndexError):
        arr[1]
