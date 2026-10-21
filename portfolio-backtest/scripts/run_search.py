"""Sample a parameter search and run it against a symbol's clean 1-min data.

Usage:
  python scripts/run_search.py --symbol SPY --n 200 --seed 42 --experiment-id exp001

This does NOT download or validate data -- run build_clean_data.py first.
Resumable: re-running with the same --experiment-id skips already-completed
configs (see src/experiments/runner.py). Use --force to recompute everyone.
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import typer

from src.experiments.runner import RunMeta, run_experiment
from src.experiments.sampler import sample_configs
from src.experiments.spaces import DEFAULT_SILVER_BULLET_SPACE
from src.utils.config_models import DEFAULT_EXECUTION_CONFIG
from src.utils.logging import configure_logging, get_logger
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()
logger = get_logger(__name__)


def _git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5)
        return out.stdout.strip() if out.returncode == 0 else "no_git_repo"
    except Exception:
        return "no_git_repo"


@app.command()
def main(
    symbol: str = typer.Option(...),
    timeframe: str = typer.Option("1min"),
    n: int = typer.Option(200, help="Number of configs to sample (spec target: ~10,000 for the full study)"),
    seed: int = typer.Option(42),
    experiment_id: str = typer.Option(...),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    results_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "results"),
    trades_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "trades"),
    signals_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "signals"),
    manifests_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "manifests"),
    n_workers: int = typer.Option(1),
    force: bool = typer.Option(False),
) -> None:
    configure_logging()

    base = clean_root / f"symbol={symbol}" / f"timeframe={timeframe}"
    bars = pl.concat([pl.read_parquet(p) for p in sorted(base.rglob("*.parquet"))]).sort("bar_open_ts")
    logger.info("data_loaded", symbol=symbol, timeframe=timeframe, rows=bars.height)

    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=n, seed=seed)
    logger.info("configs_sampled", n_requested=n, n_unique=len(samples))

    meta = RunMeta(
        experiment_id=experiment_id, code_version=_git_commit(),
        data_manifest_hashes={f"{symbol}_{timeframe}": "see runs/manifests"},
        execution_config=DEFAULT_EXECUTION_CONFIG,
    )

    manifests_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        manifests_dir / f"experiment_{experiment_id}.json",
        {
            "experiment_id": experiment_id, "symbol": symbol, "timeframe": timeframe,
            "n_configs_requested": n, "n_configs_sampled": len(samples), "seed": seed,
            "code_version": meta.code_version, "started_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    results = run_experiment(
        samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir,
        signals_dir=signals_dir, force=force, n_workers=n_workers,
    )
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] == "failed")
    logger.info("search_complete", experiment_id=experiment_id, total=len(results), ok=ok, failed=failed)


if __name__ == "__main__":
    app()
