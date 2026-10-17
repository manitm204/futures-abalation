"""Run the full Donchian-breakout ablation study.

Loads cleaned 1-minute bars, aggregates them to each timeframe on the fly,
enumerates the full factorial of strategy variants, backtests each once over the
whole history, and records per-split (development/validation/holdout) metrics.

Usage:
  python scripts/run_ablation.py --experiment-id donchian_v1 --n-workers 6
  python scripts/run_ablation.py --experiment-id smoke --symbols SPY \
      --timeframes 15min --years 2021 --n-workers 1   # quick smoke run

Resumable: re-running the same --experiment-id skips completed variants (use
--force to recompute). Run build_ablation_report.py afterwards for findings.
"""

from __future__ import annotations

import glob
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import typer

from src.data.aggregation import aggregate_bars
from src.experiments.ablation_runner import RunMeta, run_ablation
from src.experiments.grid import AXES, donchian_grid, variants_per_symbol
from src.experiments.validation import DEFAULT_SPLIT
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


def _load_1min(clean_root: Path, symbol: str, years: list[int] | None) -> pl.DataFrame:
    base = clean_root / f"symbol={symbol}" / "timeframe=1min"
    files = sorted(base.rglob("*.parquet"))
    if years:
        files = [f for f in files if any(f"year={y}" in str(f) for y in years)]
    if not files:
        raise FileNotFoundError(f"No 1-min parquet for {symbol} under {base} (years={years})")
    return pl.concat([pl.read_parquet(f) for f in files]).sort("bar_open_ts")


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    symbols: list[str] = typer.Option(["SPY", "QQQ"]),
    timeframes: list[str] = typer.Option(list(AXES["timeframe"]), help="Restrict the timeframe axis (default: all)"),
    years: list[int] = typer.Option(None, help="Restrict to these calendar years (default: all available)"),
    n_workers: int = typer.Option(1),
    force: bool = typer.Option(False),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    results_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "results"),
    trades_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "trades"),
    manifests_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "manifests"),
) -> None:
    configure_logging()
    t0 = time.time()

    # Aggregate every (symbol, timeframe) frame once, up front.
    frames: dict[str, pl.DataFrame] = {}
    for symbol in symbols:
        one_min = _load_1min(clean_root, symbol, years)
        for tf in timeframes:
            frames[f"{symbol}|{tf}"] = aggregate_bars(one_min, timeframe=tf)
            logger.info("frame_ready", symbol=symbol, timeframe=tf, bars=frames[f"{symbol}|{tf}"].height)

    grid = [gc for gc in donchian_grid(tuple(symbols)) if gc.config.timeframe in set(timeframes)]
    logger.info("grid_built", n_variants=len(grid), per_symbol=variants_per_symbol(), symbols=symbols, timeframes=timeframes)

    meta = RunMeta(
        experiment_id=experiment_id,
        code_version=_git_commit(),
        strategy_name="donchian_breakout",
        execution_config=DEFAULT_EXECUTION_CONFIG,
        split=DEFAULT_SPLIT,
    )

    manifests_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        manifests_dir / f"ablation_{experiment_id}.json",
        {
            "experiment_id": experiment_id, "strategy": "donchian_breakout",
            "symbols": symbols, "timeframes": timeframes, "years": years,
            "n_variants": len(grid), "axes": {k: list(v) for k, v in AXES.items()},
            "split": {
                "development": [DEFAULT_SPLIT.development_start.isoformat(), DEFAULT_SPLIT.development_end.isoformat()],
                "validation": [DEFAULT_SPLIT.validation_start.isoformat(), DEFAULT_SPLIT.validation_end.isoformat()],
                "holdout": [DEFAULT_SPLIT.holdout_start.isoformat(), DEFAULT_SPLIT.holdout_end.isoformat()],
            },
            "code_version": meta.code_version,
            "started_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    results = run_ablation(
        grid, frames, meta=meta, results_dir=results_dir, trades_dir=trades_dir,
        force=force, n_workers=n_workers,
    )
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] == "failed")
    logger.info("ablation_complete", experiment_id=experiment_id, total=len(results), ok=ok, failed=failed, elapsed_s=round(time.time() - t0, 1))


if __name__ == "__main__":
    app()
