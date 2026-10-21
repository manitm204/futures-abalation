"""Run the channel-breakout ablation grid (default: SPY).

Usage:
  python scripts/run_channel_ablation.py --experiment-id channel_v1 --n-workers 12

Grid (Cartesian): timeframe {5min,15min,1h} x entry_lookback {10..120} x
exit_ratio {0.25..1.0} x buffer_atr {0..0.5} x init_stop {off,1.5,2,3} x
confirm {1,2} x trend_filter {8 options} = 24,576 variants/symbol.

Resumable; run build_ablation_report.py afterwards for findings.
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
from src.experiments.ablation_runner import RunMeta
from src.experiments.channel_grid import AXES, channel_grid, variants_per_symbol
from src.experiments.channel_runner import run_channel_experiment
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
        raise FileNotFoundError(f"No 1-min parquet for {symbol} under {base}")
    return pl.concat([pl.read_parquet(f) for f in files]).sort("bar_open_ts")


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    symbols: list[str] = typer.Option(["SPY"]),
    timeframes: list[str] = typer.Option(list(AXES["timeframe"])),
    years: list[int] = typer.Option(None),
    n_workers: int = typer.Option(1),
    force: bool = typer.Option(False),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    results_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "results"),
    manifests_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "manifests"),
) -> None:
    configure_logging()
    t0 = time.time()

    frames: dict[str, pl.DataFrame] = {}
    for symbol in symbols:
        one = _load_1min(clean_root, symbol, years)
        for tf in timeframes:
            frames[tf] = aggregate_bars(one, timeframe=tf)
            logger.info("frame_ready", symbol=symbol, timeframe=tf, bars=frames[tf].height)
        break  # single-symbol frames keyed by timeframe; default run is SPY-only

    grid = [ce for ce in channel_grid(tuple(symbols)) if ce.config.timeframe in set(timeframes)]
    logger.info("grid_built", n_variants=len(grid), per_symbol=variants_per_symbol())

    meta = RunMeta(
        experiment_id=experiment_id, code_version=_git_commit(),
        strategy_name="channel_breakout", execution_config=DEFAULT_EXECUTION_CONFIG, split=DEFAULT_SPLIT,
    )

    manifests_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        manifests_dir / f"ablation_{experiment_id}.json",
        {
            "experiment_id": experiment_id, "strategy": "channel_breakout",
            "symbols": symbols, "timeframes": timeframes, "years": years,
            "n_variants": len(grid), "axes": {k: list(v) for k, v in AXES.items()},
            "code_version": meta.code_version, "started_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    results = run_channel_experiment(
        grid, frames, meta=meta, results_dir=results_dir, force=force, n_workers=n_workers,
    )
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] == "failed")
    logger.info("channel_ablation_complete", experiment_id=experiment_id, total=len(results),
                ok=ok, failed=failed, elapsed_s=round(time.time() - t0, 1))


if __name__ == "__main__":
    app()
