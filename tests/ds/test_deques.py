import pytest
from zipzap.ds.deques.linked_deque import LinkedDeque
from zipzap.exceptions import Empty


@pytest.fixture(params=[LinkedDeque])
def DequeClass(request):
    return request.param


def test_empty_deque(DequeClass):
    dq = DequeClass()
    assert dq.is_empty()
    assert len(dq) == 0


def test_add(DequeClass):
    dq = DequeClass()

    dq.add_first(10)
    assert dq.first() == 10
    dq.add_first(20)
    assert dq.first() == 20
    assert len(dq) == 2

    dq.add_last(30)
    assert dq.last() == 30
    dq.add_last(40)
    assert dq.last() == 40
    assert len(dq) == 4


def test_delete(DequeClass):
    dq = DequeClass()
    dq.add_first(10)
    dq.add_last(20)
    dq.add_last(30)

    assert dq.delete_first() == 10
    assert len(dq) == 2
    assert dq.first() == 20

    assert dq.delete_last() == 30
    assert len(dq) == 1
    assert dq.first() == 20


def test_delete_on_empty(DequeClass):
    dq = DequeClass()
    with pytest.raises(Empty):
        dq.delete_first()
    with pytest.raises(Empty):
        dq.delete_last()
    with pytest.raises(Empty):
        dq.first()
    with pytest.raises(Empty):
        dq.last()


def test_len_and_is_empty(DequeClass):
    dq = DequeClass()
    assert dq.is_empty()
    dq.add_first(1)
    assert not dq.is_empty()
    assert len(dq) == 1
    dq.delete_first()
    assert dq.is_empty()
    assert len(dq) == 0
