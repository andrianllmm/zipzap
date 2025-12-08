from typing import Type

import pytest

from zipzap.ds.entry import Entry
from zipzap.ds.priority_queues.heap_priority_queue import HeapPriorityQueue
from zipzap.ds.priority_queues.priority_queue import PriorityQueue
from zipzap.exceptions import Empty


@pytest.fixture(params=[HeapPriorityQueue])
def PriorityQueueClass(request) -> Type[PriorityQueue]:
    return request.param


def test_empty_queue(PriorityQueueClass):
    pq: PriorityQueue[int, str] = PriorityQueueClass()
    assert pq.is_empty()
    assert len(pq) == 0
    with pytest.raises(Empty):
        pq.min()
    with pytest.raises(Empty):
        pq.remove_min()


def test_add_and_min(PriorityQueueClass):
    pq: PriorityQueue[int, str] = PriorityQueueClass()
    items = [(5, "five"), (2, "two"), (8, "eight"), (1, "one")]
    for k, v in items:
        pq.add(k, v)

    assert not pq.is_empty()
    assert len(pq) == len(items)

    e = pq.min()
    assert isinstance(e, Entry)
    assert e.key == 1
    assert e.value == "one"

    assert len(pq) == len(items)


def test_remove_min(PriorityQueueClass):
    pq: PriorityQueue[int, str] = PriorityQueueClass()
    items = [(5, "five"), (2, "two"), (8, "eight"), (1, "one")]
    for k, v in items:
        pq.add(k, v)

    keys_in_order = sorted(k for k, _ in items)
    values_in_order = [v for _, v in sorted(items, key=lambda x: x[0])]

    result_keys: list[int] = []
    result_values: list[str] = []

    while not pq.is_empty():
        entry = pq.remove_min()
        result_keys.append(entry.key)
        result_values.append(entry.value)

    assert result_keys == keys_in_order
    assert result_values == values_in_order
    assert pq.is_empty()
    assert len(pq) == 0


def test_duplicate_keys(PriorityQueueClass):
    pq: PriorityQueue[int, str] = PriorityQueueClass()
    pq.add(3, "three_a")
    pq.add(1, "one")
    pq.add(3, "three_b")

    e1 = pq.remove_min()
    assert e1.key == 1
    e2 = pq.remove_min()
    assert e2.key == 3
    e3 = pq.remove_min()
    assert e3.key == 3
