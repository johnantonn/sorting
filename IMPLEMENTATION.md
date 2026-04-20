# Implementation notes

This document records algorithm choices, complexity, pitfalls, and natural
extensions. The code favors **clarity** over micro-optimizations.

## Comparison-based sorts

### Bubble sort

- **Idea:** Repeatedly swap adjacent out-of-order pairs; early exit when a pass
  makes no swap.
- **Complexity:** Θ(n²) worst/average, **O(n)** best when already sorted (with the
  early stop).
- **Stable:** Yes (only adjacent swaps among unequal keys).

### Insertion sort

- **Idea:** Grow a sorted prefix; insert each next element by shifting larger
  elements right.
- **Complexity:** Θ(n²) worst case, **O(n)** best on sorted input.
- **Stable:** Yes.

### Selection sort

- **Idea:** Select the minimum of the unsuffix and swap into place.
- **Complexity:** Θ(n²) time, O(1) extra space.
- **Stable:** Not stable as implemented (swap can reorder equal keys). A
  stable variant exists but is less common.

### Merge sort

- **Idea:** Divide range, sort halves recursively, merge sorted halves using an
  auxiliary buffer.
- **Complexity:** Θ(n log n) time, **Θ(n)** extra space for the buffer.
- **Stable:** Yes (`<=` tie-break when merging preserves left-half order).

### Quick sort

- **Idea:** Partition around a **pivot**; recurse on subranges.
- **Implementation:** **Lomuto** partition with **random pivot** selection (via the
  global `random` module) so `random.seed(...)` yields reproducible tests.
- **Complexity:** **Expected** O(n log n); **worst** O(n²) (rare with random
  pivot on adversarial data still possible in theory).
- **Stable:** No.
- **Extensions:** **3-way partition** (Dutch national flag) improves duplicate-heavy
  inputs; **median-of-three** pivots reduce bad splits on structured data.

### Heap sort

- **Idea:** Build a max-heap, repeatedly extract the maximum to the end.
- **Complexity:** Θ(n log n) time, O(1) extra space besides the input.
- **Stable:** No in typical array formulations.

### Timsort (baseline)

- **`timsort`** is `list.sort()` — Python’s highly optimized **adaptive** hybrid of
  merge and insertion sort with many special cases for real-world data. It is the
  default reference **not** because it is a teaching implementation, but because it
  represents what production Python uses.

## Distribution sort

### Counting sort

- **Preconditions:** Keys are **non-negative integers** strictly less than
  `upper_exclusive`, or omit `upper_exclusive` and the implementation uses
  `max(arr) + 1` (requires non-empty `arr`).
- **Complexity:** **O(n + k)** time, **O(k)** auxiliary space where `k = upper_exclusive`.
- **Stable:** Yes (the copy-back phase preserves the order of equal keys when
  populated left-to-right).
- **Pitfalls:**
  - **Memory:** If keys span `0 … 10⁹` but `n` is small, **k** explodes — use
    radix sort or comparison sorts instead.
  - **Semantics:** Not applicable to arbitrary floats or unbounded integers without
    discretization.

The benchmark sets `k = max(256, n)` and draws values from `range(k)` so every
algorithm (including counting sort) sees the **same** input distribution for a
given `(n, seed)`.

## Benchmarking methodology

For each `n`, one random vector is built from bounded integers. Each sort is run
`runs` times on a **fresh copy** of that vector — timings are **independent** of
one another and use `time.perf_counter()`.

The reported interval is a **bootstrap percentile band (2.5ᵗʰ–97.5ᵗʰ)** over
resampled means of those runtimes (default 2000 resamples). This approximates a
**95% uncertainty range for the expected (mean) time** under i.i.d. assumptions.

**Alternative:** a **Student’s t** interval on the `runs` samples is another
standard choice; it assumes approximate normality of runtimes. Profiling noise is
often heavy-tailed; bootstrap is robust enough for exploratory comparisons.

**Interpretation:** Bars compare **average** performance on one synthetic
distribution; they do not prove ranking on all inputs (Timsort’s adaptivity is
hidden in a single random vector per `n`).

## Extensions

- **Radix / bucket sort** for integers with large span but fixed width.
- **Intro sort** (quicksort with depth limit, fallback to heap sort) for O(n log n)
  worst case while staying cache-friendly.
- **Parallel merge sort** for large arrays (not covered here).
