from __future__ import annotations


def timsort(arr: list) -> None:
    """Sort `arr` in-place using Python's Timsort (list.sort).

    This is a thin wrapper around the interpreter's stable, highly optimized
    hybrid merge/insertion sort.
    """
    arr.sort()
