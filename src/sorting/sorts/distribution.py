from __future__ import annotations


def counting_sort(arr: list[int], upper_exclusive: int | None = None) -> None:
    """Stable counting sort for non-negative integers strictly less than `upper_exclusive`.

    Parameters
    ----------
    arr :
        List of integers to sort in-place (`arr[:] = sorted(arr)` semantics).
    upper_exclusive :
        One past the maximum allowed value (keys must satisfy ``0 <= x < upper_exclusive``).
        If omitted, set to ``max(arr) + 1`` (list must be non-empty).

    Complexity
    ----------
    Time O(n + k), extra space O(k), where k = `upper_exclusive`.
    """
    n = len(arr)
    if n == 0:
        return

    if upper_exclusive is None:
        upper_exclusive = max(arr) + 1

    if upper_exclusive <= 0:
        raise ValueError("upper_exclusive must be positive when arr is non-empty")

    freq = [0] * upper_exclusive
    for x in arr:
        if not isinstance(x, int):
            raise TypeError("counting_sort requires integral keys")
        if x < 0 or x >= upper_exclusive:
            raise ValueError(
                f"all values must satisfy 0 <= x < {upper_exclusive}, got {x!r}"
            )
        freq[x] += 1

    starts = [0] * upper_exclusive
    run = 0
    for i in range(upper_exclusive):
        starts[i] = run
        run += freq[i]

    output = [0] * n
    for x in arr:
        pos = starts[x]
        output[pos] = x
        starts[x] += 1

    arr[:] = output
