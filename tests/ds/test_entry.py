from zipzap.ds.entry import Entry


def test_initialization():
    e = Entry("a", 10)
    assert e.key == "a"
    assert e.value == 10


def test_iter():
    e = Entry("a", 10)
    key, value = e
    assert key == "a"
    assert value == 10


def test_comparisons():
    e1 = Entry(1, "a")
    e2 = Entry(2, "b")
    e3 = Entry(1, "c")

    assert e1 < e2
    assert e2 > e1
    assert e1 == e3
    assert e1 != e2

    e4 = Entry(4, "d")
    assert e4 != 4
