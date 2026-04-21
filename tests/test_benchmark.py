from __future__ import annotations

from pathlib import Path

import pytest

from sorting.benchmark.runner import BenchmarkConfig, run_benchmark


def test_run_benchmark_returns_rows():
    cfg = BenchmarkConfig(
        sizes=(8, 16),
        runs=3,
        seed=0,
        output_dir=Path("."),
        bootstrap_resamples=100,
    )
    rows = run_benchmark(cfg)
    assert len(rows) == 8 * 2  # eight sorters × two sizes
    assert {r["algorithm"] for r in rows} == set(
        [
            "bubble_sort",
            "insertion_sort",
            "selection_sort",
            "merge_sort",
            "quick_sort",
            "heap_sort",
            "counting_sort",
            "timsort",
        ]
    )


@pytest.mark.parametrize("bad", ["0", "-1", "10,-5"])
def test_cli_rejects_invalid_sizes(bad):
    from sorting.benchmark.runner import main

    with pytest.raises(SystemExit):
        main(["--sizes", bad])
