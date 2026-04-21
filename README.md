# sorting

Educational Python implementations of common **comparison-based** sorts (bubble, insertion, selection, merge, quick, heap), **distribution** counting sort on bounded non-negative integers, and a **Timsort** baseline via `list.sort()`. The package ships with **pytest** coverage and a **benchmark CLI** that plots mean wall-clock time versus dataset size with **95% bootstrap intervals** on the mean (see [IMPLEMENTATION.md](IMPLEMENTATION.md) for methodology).

> **Status:** Personal / portfolio archive — **not actively maintained** beyond occasional tidying. Tooling should still be straightforward on modern Python.

## How to run

Install in editable mode from the repo root (`pip install -e .` or `pip install -e ".[dev]"` if defined), then run **`pytest`** from the repository root. For benchmarks, use the CLI under `src/sorting/benchmark/` (see [IMPLEMENTATION.md](IMPLEMENTATION.md) for flags and output paths).

## Overview

- **`src/sorting/sorts/`** — Pure-Python sorters with a small, consistent contract: each routine sorts a list **in place** (except where noted in tests).
- **`src/sorting/benchmark/`** — Repeatable timings: one random bounded-int vector per **N**, `--runs` independent timings per algorithm on fresh copies, CSV + log–log PNG output.
- **`tests/`** — Property-style checks (random inputs), edge cases, stability where applicable, counting-sort key bounds.

Benchmarks use `k = max(256, N)` and draw keys from `0 … k − 1` so counting sort and comparison sorts see the **same** inputs for each `(N, seed)`.

## Algorithms: time and space complexity

Worst-case bounds unless otherwise noted. **n** is the number of elements; **k** is the counting-sort key universe size (`upper_exclusive`). This project’s benchmark sets **k** comparable to **n** (at least 256), so counting sort behaves as **O(n)** time and **O(n)** extra space for those runs.

| Implementation | Time complexity | Space complexity (auxiliary) |
|----------------|-----------------|------------------------------|
| `bubble_sort` | O(n²) worst and average; **O(n)** best (already sorted, with early exit) | **O(1)** |
| `insertion_sort` | O(n²) worst/average; **O(n)** best (sorted input) | **O(1)** |
| `selection_sort` | **Θ(n²)** | **O(1)** |
| `merge_sort` | **Θ(n log n)** | **Θ(n)** |
| `quick_sort` (random pivot) | **O(n log n)** expected; **O(n²)** worst | **O(log n)** stack typical; **O(n)** worst case |
| `heap_sort` | **Θ(n log n)** | **O(1)** |
| `counting_sort` | **Θ(n + k)** | **Θ(k)** |
| `timsort` (`list.sort`) | **O(n log n)** worst; often **O(n)** on partially ordered data | **O(n)** worst case auxiliary |

## Benchmark results and findings

Results below are from a full default run on this machine: sizes **32 … 8192** (powers of two), **`runs = 40`**, **`seed = 42`**, outputs in **`artifacts/`** (`benchmark_results.csv`, `benchmark_plot.png`). Numbers are **mean seconds per sort** (single-threaded; your hardware will differ).

At **N = 8192**, mean runtimes were ordered as follows (fastest first):

| Algorithm | Mean time (s) | Notes |
|-----------|---------------|--------|
| `timsort` | ~6.5 × 10⁻⁴ | Highly optimized C implementation; baseline for “production” Python. |
| `counting_sort` | ~1.3 × 10⁻³ | Best asymptotics here because **k** tracks **n**; linear passes dominate. |
| `quick_sort` | ~8.7 × 10⁻³ | Good average case on random data; Lomuto partition + random pivot. |
| `merge_sort` | ~1.3 × 10⁻² | Stable Θ(n log n); extra Θ(n) memory. |
| `heap_sort` | ~1.4 × 10⁻² | In-place Θ(n log n), larger constant factors than merge/tim in practice here. |
| `selection_sort` | ~8.8 × 10⁻¹ | Θ(n²) swaps not dominating; still costly at 8K. |
| `insertion_sort` | ~9.5 × 10⁻¹ | Θ(n²); faster than bubble on random data in this run. |
| `bubble_sort` | ~2.1 | Slowest: Θ(n²) with high constant work per comparison. |

**Takeaways:** On bounded random integers at large **N**, **O(n log n)** sorts cluster in the **~10 ms** range (here), **counting sort** is competitive when **k** is modest, **Timsort** wins overall, and **quadratic** algorithms become impractical (seconds per run at 8K). The log–log plot separates **n²** slopes from **n log n** clearly as **N** grows.

Interpretation: error bars in the plot reflect **uncertainty in the mean** of `--runs` trials, not simultaneous comparison intervals between algorithms.

## Requirements

- **Python** 3.12+
- **[uv](https://docs.astral.sh/uv/)** for an isolated environment and dependency management (a `.venv` is created in this repo).

```bash
cd sorting
uv sync
```

## Run tests

```bash
uv run python -m pytest
```

## Run the benchmark

Pass **several dataset sizes** `N` via `--sizes` (comma-separated). For each `N`, the harness builds one random list of length `N`, then times **every** sorting implementation for `--runs` trials on a **fresh copy** of that list. Results are saved as a table and as a **single figure**: **mean runtime (y) vs dataset size N (x)** with **one curve per algorithm**. Both axes use a **log** scale by default so \(n^2\) and \(n \log n\) regimes are easier to read.

```bash
uv run python -m sorting.benchmark --sizes 32,64,128,256,512,1024 --runs 40 --seed 42 --output-dir artifacts
```

(Omit `--sizes` to use the built-in progression from 32 up through **8192** (8K). Quadratic sorts at the largest sizes can take a long time; use a smaller `--sizes` list or fewer `--runs` for a quick trial.)

Artifacts (default `artifacts/`, gitignored):

- `benchmark_results.csv` — one row per `(algorithm, N)`
- `benchmark_plot.png` — **runtime vs N** for every sort, with bootstrap error bars on the mean

**Headless / CI:** plotting uses the **Agg** backend and sets `MPLCONFIGDIR` to `.mplconfig/` under the repo when unset, so matplotlib can cache fonts without assuming a writable home directory.

## Layout

| Path | Purpose |
|------|---------|
| `src/sorting/sorts/` | Algorithm implementations |
| `src/sorting/benchmark/` | CLI + plotting |
| `tests/` | Pytest suite |
