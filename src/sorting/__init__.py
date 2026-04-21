"""Sorting algorithms, benchmarks, and tests."""

from __future__ import annotations

from typing import Callable

from sorting.sorts import (
    bubble_sort,
    counting_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    timsort,
)


def _counting_with_k(k: int) -> Callable[[list], None]:
    def sort_fn(a: list) -> None:
        counting_sort(a, k)

    return sort_fn


def default_key_upper_exclusive(n: int) -> int:
    """Exclusive upper bound on keys for bounded-int benchmarks (same as plan default)."""
    return max(256, n)


def make_benchmark_sorters(
    n: int,
    *,
    key_upper_exclusive: Callable[[int], int] | None = None,
) -> dict[str, Callable[[list], None]]:
    """Return one callable per algorithm for input size `n`.

    ``counting_sort`` is bound to ``k = key_upper_exclusive(n)`` so random data
    can be drawn from ``range(k)``.
    """
    ku = key_upper_exclusive or default_key_upper_exclusive
    k = ku(n)
    return {
        "bubble_sort": bubble_sort,
        "insertion_sort": insertion_sort,
        "selection_sort": selection_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort,
        "heap_sort": heap_sort,
        "counting_sort": _counting_with_k(k),
        "timsort": timsort,
    }


def registered_sorter_names() -> tuple[str, ...]:
    """Algorithms included in the default benchmark study."""
    return (
        "bubble_sort",
        "insertion_sort",
        "selection_sort",
        "merge_sort",
        "quick_sort",
        "heap_sort",
        "counting_sort",
        "timsort",
    )


__all__ = [
    "bubble_sort",
    "counting_sort",
    "default_key_upper_exclusive",
    "heap_sort",
    "insertion_sort",
    "make_benchmark_sorters",
    "merge_sort",
    "quick_sort",
    "registered_sorter_names",
    "selection_sort",
    "timsort",
]
