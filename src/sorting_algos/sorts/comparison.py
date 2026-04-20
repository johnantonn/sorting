from __future__ import annotations

import random


def bubble_sort(arr: list) -> None:
    """In-place bubble sort. Θ(n²) time, O(1) extra space. Stable."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break


def insertion_sort(arr: list) -> None:
    """In-place insertion sort. O(n²) worst case, O(n) best (sorted). Stable."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def selection_sort(arr: list) -> None:
    """In-place selection sort. Θ(n²) time. Not stable."""
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]


def merge_sort(arr: list) -> None:
    """Top-down merge sort in Θ(n log n) time with Θ(n) auxiliary space. Stable."""
    n = len(arr)
    if n <= 1:
        return

    aux = [0] * n

    def merge(lo: int, mid: int, hi: int) -> None:
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if aux[i] <= aux[j]:
                arr[k] = aux[i]
                i += 1
            else:
                arr[k] = aux[j]
                j += 1
            k += 1
        while i < mid:
            arr[k] = aux[i]
            i += 1
            k += 1
        while j < hi:
            arr[k] = aux[j]
            j += 1
            k += 1

    def sort_range(lo: int, hi: int) -> None:
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort_range(lo, mid)
        sort_range(mid, hi)
        for i in range(lo, hi):
            aux[i] = arr[i]
        merge(lo, mid, hi)

    sort_range(0, n)


def _partition_lomuto(arr: list, lo: int, hi: int) -> int:
    """Partition `arr[lo:hi]` with pivot at `lo`; returns final pivot index."""
    pivot = arr[lo]
    i = lo + 1
    for j in range(lo + 1, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[lo], arr[i - 1] = arr[i - 1], arr[lo]
    return i - 1


def quick_sort(arr: list) -> None:
    """In-place quicksort with random pivot (Lomuto partition).

    Expected O(n log n) time; worst case O(n²). Not stable.

    Uses the global :mod:`random` generator so test code can ``random.seed(...)``
    for deterministic runs.
    """
    def qsort(lo: int, hi: int) -> None:
        if hi - lo <= 1:
            return
        pivot_idx = random.randrange(lo, hi)
        arr[lo], arr[pivot_idx] = arr[pivot_idx], arr[lo]
        p = _partition_lomuto(arr, lo, hi)
        qsort(lo, p)
        qsort(p + 1, hi)

    qsort(0, len(arr))


def _sift_down(arr: list, start: int, end: int) -> None:
    root = start
    while True:
        child = root * 2 + 1
        if child >= end:
            break
        if child + 1 < end and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break


def heap_sort(arr: list) -> None:
    """In-place heapsort. Θ(n log n) time, O(1) extra space. Not stable."""
    n = len(arr)
    if n <= 1:
        return
    for start in range((n - 2) // 2, -1, -1):
        _sift_down(arr, start, n)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)
