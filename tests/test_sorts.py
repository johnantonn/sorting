from __future__ import annotations

import copy
import random

import pytest

from sorting_algos.sorts import (
    bubble_sort,
    counting_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    timsort,
)

COMPARISON_AND_BASELINE = [
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    timsort,
]

STABLE_SORTS = [bubble_sort, insertion_sort, merge_sort, timsort]


def _rand_int_list(n: int, rng: random.Random) -> list[int]:
    return [rng.randint(-1000, 1000) for _ in range(n)]


@pytest.mark.parametrize("sort_fn", COMPARISON_AND_BASELINE)
@pytest.mark.parametrize("n", [0, 1, 2, 3, 7, 32, 64])
@pytest.mark.parametrize("seed", [0, 1, 13])
def test_random_integers(sort_fn, n, seed):
    rng = random.Random(seed)
    data = _rand_int_list(n, rng)
    expected = sorted(data)
    arr = copy.copy(data)
    random.seed(seed + 17)
    sort_fn(arr)
    assert arr == expected


@pytest.mark.parametrize("sort_fn", COMPARISON_AND_BASELINE)
def test_structured_inputs(sort_fn):
    cases = [
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5],
        [7, 7, 7],
        [2, 2, 1, 1, 3, 3],
    ]
    for data in cases:
        arr = copy.copy(data)
        random.seed(12345)
        sort_fn(arr)
        assert arr == sorted(data)


def test_counting_sort_random():
    rng = random.Random(0)
    for n in [0, 1, 5, 50]:
        for upper in [5, 20, 256]:
            data = [rng.randrange(0, upper) for _ in range(n)]
            expected = sorted(data)
            arr = copy.copy(data)
            counting_sort(arr, upper)
            assert arr == expected


def test_counting_sort_empty():
    arr: list[int] = []
    counting_sort(arr)
    assert arr == []


def test_counting_sort_infers_upper():
    arr = [3, 0, 2, 1]
    counting_sort(arr)
    assert arr == [0, 1, 2, 3]


def test_counting_sort_rejects_invalid():
    with pytest.raises(ValueError, match="0 <="):
        counting_sort([1, -1], 10)
    with pytest.raises(ValueError, match="0 <="):
        counting_sort([10], 10)
    with pytest.raises(TypeError):
        counting_sort([1.0, 1.0], 3)  # type: ignore[list-item]


def test_merge_sort_stability():
    items = [(2, 0), (1, 0), (1, 1), (3, 0), (1, 2)]
    arr = list(items)
    merge_sort(arr)
    assert arr == [(1, 0), (1, 1), (1, 2), (2, 0), (3, 0)]


def test_timsort_stability():
    items = [(2, "a"), (1, "x"), (1, "y")]
    arr = list(items)
    timsort(arr)
    assert arr == [(1, "x"), (1, "y"), (2, "a")]


@pytest.mark.parametrize("sort_fn", STABLE_SORTS)
def test_stability_equal_keys(sort_fn):
    items = [(0, 2), (0, 1), (0, 0)]
    arr = list(reversed(items))
    sort_fn(arr)
    assert arr == [(0, 0), (0, 1), (0, 2)]


def test_benchmark_factory_matches_keys():
    from sorting_algos import default_key_upper_exclusive, make_benchmark_sorters

    n = 100
    k = default_key_upper_exclusive(n)
    rng = random.Random(7)
    data = [rng.randrange(0, k) for _ in range(n)]
    expected = sorted(data)
    for name, fn in make_benchmark_sorters(n).items():
        a = copy.copy(data)
        fn(a)
        assert a == expected, name

