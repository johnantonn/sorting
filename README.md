# sorting-algos

Educational implementations of common sorting algorithms in Python, plus a small
benchmark harness that estimates **mean wall-clock time per run** with a
**95% confidence band** around that mean (see [IMPLEMENTATION.md](IMPLEMENTATION.md)
for methodology).

## Goals

- Provide **correct, readable** versions of classic sorts plus **heap sort** and the
  interpreter’s **Timsort** baseline (`list.sort`).
- Lock correctness in with **`pytest`** (random vectors, structured edge cases,
  stability checks where relevant, counting-sort preconditions).
- Run repeatable **timing experiments** on **bounded random integers** so
  **counting sort** stays well-defined alongside comparison-based routines.

## Requirements

- **Python** 3.12+
- **[uv](https://docs.astral.sh/uv/)** for an isolated environment and dependency
  management (a `.venv` is created in this repo).

```bash
cd sorting_algos
uv sync
```

## Run tests

```bash
uv run pytest
```

## Run the benchmark

The harness times each `(algorithm, n)` pair for `--runs` independent trials on the
**same** random vector (fair comparison for a fixed size). It writes a CSV and a
log–log plot with **bootstrap percentile bands** around the mean time.

```bash
uv run python -m sorting_algos.benchmark --sizes 64,128,256,512 --runs 40 --seed 42 --output-dir artifacts
```

Artifacts (default `artifacts/`, gitignored):

- `benchmark_results.csv` — one row per algorithm and `n`
- `benchmark_plot.png` — mean seconds vs `n` with error bars

**Headless / CI:** plotting uses the **Agg** backend and sets `MPLCONFIGDIR` to
`.mplconfig/` under the repo when unset, so matplotlib can cache fonts without
assuming a writable home directory.

## Results (fill in after you run locally)

Timing is **machine-dependent**. After running the command above on your hardware,
paste a short summary here (e.g. relative ordering at the largest `n`, or attach
`artifacts/benchmark_plot.png` when sharing the repo).

| n    | Fastest (this machine) | Notes |
|------|-------------------------|-------|
| …    | …                       | …     |

Interpretation: error bars reflect **uncertainty in the mean runtime** across the
`--runs` trials (bootstrap over **independent** timings), not simultaneous
comparison intervals between algorithms.

## Layout

| Path | Purpose |
|------|---------|
| `src/sorting_algos/sorts/` | Algorithm implementations |
| `src/sorting_algos/benchmark/` | CLI + plotting |
| `tests/` | Pytest suite |
