from typing import Optional, Literal, Sequence

from model import IntervalData


def _search_ge(
    v: Sequence[IntervalData], field: Literal["ini", "end"], value: float
) -> Optional[int]:
    l = 0
    r = len(v) - 1

    feasible_idx = None

    while l <= r:
        i = (l + r) // 2
        if v[i].__getattribute__(field) >= value:
            feasible_idx = i
            r = i - 1
        else:
            l = i + 1

    return feasible_idx


def _search_le(
    v: Sequence[IntervalData], field: Literal["ini", "end"], value: float
) -> Optional[int]:
    l = 0
    r = len(v) - 1

    feasible_idx = None

    while l <= r:
        i = (l + r) // 2
        if v[i].__getattribute__(field) <= value:
            feasible_idx = i
            l = i + 1
        else:
            r = i - 1

    return feasible_idx


def search_ini_ge(v: Sequence[IntervalData], value: float) -> Optional[int]:
    return _search_ge(v, "ini", value)


def search_end_ge(v: Sequence[IntervalData], value: float) -> Optional[int]:
    return _search_ge(v, "end", value)


def search_ini_le(v: Sequence[IntervalData], value: float) -> Optional[int]:
    return _search_le(v, "ini", value)


def search_end_le(v: Sequence[IntervalData], value: float) -> Optional[int]:
    return _search_le(v, "end", value)
