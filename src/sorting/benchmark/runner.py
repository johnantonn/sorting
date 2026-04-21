from __future__ import annotations

import argparse
import csv
import os
import time
from dataclasses import dataclass
from pathlib import Path

# Headless plotting + writable cache when the home directory is not writable (e.g. CI/sandbox).
_repo_root = Path(__file__).resolve().parents[3]
_mpl_dir = _repo_root / ".mplconfig"
_mpl_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_mpl_dir))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sorting import default_key_upper_exclusive, make_benchmark_sorters, registered_sorter_names


@dataclass(frozen=True)
class BenchmarkConfig:
    sizes: tuple[int, ...]
    runs: int
    seed: int
    output_dir: Path
    bootstrap_resamples: int = 2000

    @property
    def rng(self) -> np.random.Generator:
        return np.random.default_rng(self.seed)


def _bootstrap_ci_mean(samples: np.ndarray, n_boot: int, rng: np.random.Generator) -> tuple[float, float]:
    """Percentile bootstrap interval for the mean (95%)."""
    x = np.asarray(samples, dtype=np.float64)
    n = len(x)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        m = float(x[0])
        return m, m
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_means = x[idx].mean(axis=1)
    low, high = np.percentile(boot_means, [2.5, 97.5])
    return float(low), float(high)


def _random_bounded_ints(n: int, upper_exclusive: int, rng: np.random.Generator) -> list[int]:
    return [int(x) for x in rng.integers(0, upper_exclusive, size=n, endpoint=False)]


def _time_once(sort_fn, data: list) -> float:
    arr = list(data)
    t0 = time.perf_counter()
    sort_fn(arr)
    return time.perf_counter() - t0


def run_benchmark(config: BenchmarkConfig) -> list[dict]:
    """Run all registered sorters for each size; return rows with stats."""
    rows: list[dict] = []
    boot_rng = np.random.default_rng(config.seed + 7919)

    for n in config.sizes:
        ku = default_key_upper_exclusive(n)
        sorters = make_benchmark_sorters(n)
        data = _random_bounded_ints(n, ku, config.rng)

        for name in registered_sorter_names():
            sort_fn = sorters[name]
            samples = [_time_once(sort_fn, data) for _ in range(config.runs)]
            arr = np.asarray(samples)
            mean_s = float(arr.mean())
            lo, hi = _bootstrap_ci_mean(arr, config.bootstrap_resamples, boot_rng)
            rows.append(
                {
                    "algorithm": name,
                    "n": n,
                    "mean_seconds": mean_s,
                    "ci_low": lo,
                    "ci_high": hi,
                    "runs": config.runs,
                }
            )
    return rows


def _write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _plot(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    present = {r["algorithm"] for r in rows}
    # One series per algorithm, ordered like the public benchmark registry so the legend matches docs.
    algorithms = [a for a in registered_sorter_names() if a in present]
    for a in sorted(present - set(algorithms)):
        algorithms.append(a)
    dataset_sizes_n = sorted({r["n"] for r in rows})
    by_alg = {a: {r["n"]: r for r in rows if r["algorithm"] == a} for a in algorithms}

    fig, ax = plt.subplots(figsize=(11, 6))
    for name in algorithms:
        means = [by_alg[name][n]["mean_seconds"] for n in dataset_sizes_n]
        lows = [by_alg[name][n]["ci_low"] for n in dataset_sizes_n]
        highs = [by_alg[name][n]["ci_high"] for n in dataset_sizes_n]
        errs = [
            [max(0.0, m - lo), max(0.0, hi - m)]
            for m, lo, hi in zip(means, lows, highs, strict=True)
        ]
        yerr = np.array(errs).T
        ax.errorbar(
            dataset_sizes_n,
            means,
            yerr=yerr,
            marker="o",
            capsize=3,
            label=name,
            linewidth=1.2,
        )

    ax.set_xlabel("Dataset size N")
    ax.set_ylabel("Mean runtime (seconds)")
    ax.set_title(
        "Mean runtime vs dataset size N — all sorting implementations\n"
        "(log–log, bounded random integers; error bars: 95% bootstrap CI for the mean)"
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark sorting implementations.")
    parser.add_argument(
        "--sizes",
        type=str,
        default="32,64,128,256,512,1024,2048,4096,8192",
        help="Comma-separated dataset sizes N to benchmark (default: powers of two from 32 through 8192)",
    )
    parser.add_argument("--runs", type=int, default=40, help="Repeated timing runs per (algorithm, n)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducible inputs")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts"),
        help="Directory for CSV and PNG (default: %(default)s)",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=2000, help="Bootstrap resamples for CI")
    args = parser.parse_args(argv)

    sizes = tuple(int(x.strip()) for x in args.sizes.split(",") if x.strip())
    if any(n <= 0 for n in sizes):
        raise SystemExit("all sizes must be positive")

    config = BenchmarkConfig(
        sizes=sizes,
        runs=args.runs,
        seed=args.seed,
        output_dir=args.output_dir,
        bootstrap_resamples=args.bootstrap_resamples,
    )
    rows = run_benchmark(config)
    csv_path = args.output_dir / "benchmark_results.csv"
    png_path = args.output_dir / "benchmark_plot.png"
    _write_csv(rows, csv_path)
    _plot(rows, png_path)
    print(f"Wrote {csv_path}")
    print(f"Wrote {png_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
