from index.binary_search import (
    search_ini_ge,
    search_ini_le,
    search_end_ge,
    search_end_le,
)
from model import IntervalData


def test_search_ini_le_should_return_the_largest_value_that_satisfies_the_inequality() -> None:
    v = [
        IntervalData(ini=-2.0, end=-1.0),
        IntervalData(ini=-1.0, end=0.0),
        IntervalData(ini=1.0, end=2.0),
        IntervalData(ini=2.0, end=-3.0),
    ]

    assert search_ini_le(v, 4) == 3
    assert search_ini_le(v, 2.5) == 3
    assert search_ini_le(v, 1.5) == 2
    assert search_ini_le(v, 1) == 2
    assert search_ini_le(v, 0.2) == 1
    assert search_ini_le(v, -0.5) == 1
    assert search_ini_le(v, -1.5) == 0
    assert search_ini_le(v, -1.99) == 0
    assert search_ini_le(v, -2) == 0
    assert search_ini_le(v, -2.000001) is None
    assert search_ini_le(v, float("-inf")) is None


def test_search_ini_le_should_return_the_same_value_for_each_position() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    for i in range(100):
        assert search_ini_le(v, float(i)) == i


def test_search_ini_le_should_work_for_negative_values() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(-100, 1)]
    for i in range(-100, 1):
        assert search_ini_le(v, float(i)) == 100 + i


def test_search_ini_le_should_return_none_if_invalid_value() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    idx = search_ini_le(v, value=-0.00001)
    assert idx is None


def test_search_ini_le_should_return_the_last_element_if_value_is_greater_than_list() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    idx = search_ini_le(v, value=101)
    assert idx == 99


def test_search_ini_ge_should_return_the_smallest_value_that_satisfies_the_inequality() -> None:
    v = [
        IntervalData(ini=-3.1, end=-3),
        IntervalData(ini=-2.1, end=-1.0),
        IntervalData(ini=-0.2, end=0.0),
        IntervalData(ini=0.3, end=1.2),
        IntervalData(ini=1.2, end=2.0),
        IntervalData(ini=10.0, end=11.0),
    ]

    assert search_ini_ge(v, -4) == 0
    assert search_ini_ge(v, -3.2) == 0
    assert search_ini_ge(v, -2.1) == 1
    assert search_ini_ge(v, -2.01) == 2
    assert search_ini_ge(v, -0.19) == 3
    assert search_ini_ge(v, -0.001) == 3
    assert search_ini_ge(v, 0.34) == 4
    assert search_ini_ge(v, 1.2) == 4
    assert search_ini_ge(v, 8.0) == 5
    assert search_ini_ge(v, 9.0) == 5
    assert search_ini_ge(v, 10.0) == 5
    assert search_ini_ge(v, 11.00001) is None


def test_search_ini_ge_should_return_the_same_value_for_each_position() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    for i in range(100):
        assert search_ini_ge(v, float(i)) == i


def test_search_ini_ge_should_work_for_negative_values() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(-100, 1)]
    for i in range(-100, 1):
        assert search_ini_ge(v, float(i)) == 100 + i


def test_search_ini_ge_should_return_none_if_invalid_value() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    idx = search_ini_ge(v, value=100.1)
    assert idx is None


def test_search_ini_ge_should_return_the_first_element_if_value_is_smaller_than_list() -> None:
    v = [IntervalData(ini=float(i), end=float(i + 1)) for i in range(100)]
    idx = search_ini_ge(v, value=-1.0)
    assert idx == 0


def test_search_ini_ge_and_search_end_ge_should_return_the_same_idx_if_they_are_equal() -> None:
    v = [IntervalData(ini=float(i), end=float(i)) for i in range(-100, 100)]

    for i in range(-100, 100):
        assert search_ini_ge(v, i) == search_end_ge(v, i)
        assert search_ini_ge(v, i + 0.1) == search_end_ge(v, i + 0.1)
        assert search_ini_ge(v, i - 0.1) == search_end_ge(v, i - 0.1)


def test_search_ini_le_and_search_end_le_should_return_the_same_idx_if_they_are_equal() -> None:
    v = [IntervalData(ini=float(i), end=float(i)) for i in range(-100, 100)]

    for i in range(-100, 100):
        assert search_ini_le(v, i) == search_end_le(v, i)
        assert search_ini_le(v, i + 0.1) == search_end_le(v, i + 0.1)
        assert search_ini_le(v, i - 0.1) == search_end_le(v, i - 0.1)


def test_all_searches_should_work_if_list_contains_same_value() -> None:
    v = [IntervalData(ini=1, end=1) for i in range(100)]
    assert search_ini_ge(v, 0) == 0
    assert search_ini_ge(v, 2) is None

    assert search_ini_le(v, 0) is None
    assert search_ini_le(v, 2) == 99
