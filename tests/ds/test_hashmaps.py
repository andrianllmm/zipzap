import pytest
from typing import Type

from zipzap.ds.maps.probe_hashmap import ProbeHashmap
from zipzap.ds.maps.map import Map


@pytest.fixture(params=[ProbeHashmap])
def hashmap_class(request) -> Type[Map]:
    return request.param


def test_empty_map(hashmap_class):
    m: Map = hashmap_class()
    assert len(m) == 0
    assert m.is_empty()
    assert m.get("x") is None
    assert list(m.entries()) == []
    assert list(m.keys()) == []
    assert list(m.values()) == []


def test_put_and_get_single(hashmap_class):
    m: Map = hashmap_class()
    assert m.put("a", 1) is None
    assert len(m) == 1
    assert not m.is_empty()
    assert m.get("a") == 1
    assert list(m.keys()) == ["a"]
    assert list(m.values()) == [1]


def test_put_and_get_multiple(hashmap_class):
    m: Map = hashmap_class()
    m.put("a", 1)
    m.put("b", 2)
    m.put("c", 3)
    assert len(m) == 3
    assert m.get("a") == 1
    assert m.get("b") == 2
    assert m.get("c") == 3
    assert sorted(m.keys()) == ["a", "b", "c"]
    assert sorted(m.values()) == [1, 2, 3]


def test_put_overwrite(hashmap_class):
    m: Map = hashmap_class()
    m.put("a", 1)
    old = m.put("a", 2)
    assert old == 1
    assert m.get("a") == 2
    assert len(m) == 1


def test_remove_existing(hashmap_class):
    m: Map = hashmap_class()
    m.put("x", 5)
    removed = m.remove("x")
    assert removed == 5
    assert m.get("x") is None
    assert len(m) == 0


def test_remove_missing(hashmap_class):
    m: Map = hashmap_class()
    assert m.remove("nope") is None
    assert len(m) == 0


def test_remove_does_not_break_search(hashmap_class):
    m: Map = hashmap_class()
    m.put("a", 1)
    m.put("b", 2)
    m.put("c", 3)

    m.remove("b")

    assert m.get("a") == 1
    assert m.get("c") == 3  # search must pass through
    assert m.get("b") is None


def test_collision_handling(hashmap_class):
    m: Map = hashmap_class()

    # These often collide in simple hash setups
    m.put("a", 1)
    m.put("b", 2)
    m.put("aa", 3)
    m.put("bb", 4)

    assert m.get("a") == 1
    assert m.get("b") == 2
    assert m.get("aa") == 3
    assert m.get("bb") == 4


def test_full_table(hashmap_class):
    m: Map = hashmap_class(slots=5)

    items = [(f"k{i}", i) for i in range(20)]
    for k, v in items:
        m.put(k, v)

    for k, v in items:
        assert m.get(k) == v

    assert len(m) == len(items)
    assert not m.is_empty()
