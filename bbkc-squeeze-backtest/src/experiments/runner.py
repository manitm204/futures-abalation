"""Runs a batch of sampled SilverBulletConfigs against a symbol's bar data,
producing per-config signals/trades/metrics with checkpointing (resumable),
per-config failure isolation, and optional multi-process parallelism.

Result layout (per spec's recommended partitioning):
  runs/results/experiment_id=<id>/config_id=<cid>.json   (metrics + status)
  runs/trades/experiment_id=<id>/config_id=<cid>.parquet
  runs/signals/experiment_id=<id>/config_id=<cid>.parquet
  runs/results/experiment_id=<id>/errors/config_id=<cid>.txt  (failures, isolated)

Resume: a config whose result JSON already exists with status "ok" or "failed"
is skipped on re-run unless `force=True`. This is what lets an interrupted
~10,000-config search continue rather than restart.
"""

from __future__ import annotations

import multiprocessing
import tempfile
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from src.engine.metrics import compute_metrics
from src.engine.simulator import run_backtest_single_symbol
from src.experiments.sampler import SampledConfig
from src.strategies.ict_silver_bullet.strategy import SilverBulletStrategy
from src.utils.config_models import ExecutionConfig
from src.utils.serialization import atomic_write_json, read_json


@dataclass
class RunMeta:
    experiment_id: str
    code_version: str
    data_manifest_hashes: dict[str, str]
    execution_config: ExecutionConfig


def _result_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / f"{config_id}.json"


def _error_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / "errors" / f"{config_id}.txt"


# Set once per worker PROCESS via ProcessPoolExecutor's initializer, not passed
# through each task submission. Passing a large DataFrame as a per-task argument
# means concurrent.futures pickles and pipes a full copy of it to a worker for
# EVERY task -- for an 842k-row/8-year history and hundreds of configs, this
# turned a ~2-3 hour parallel run into an apparent multi-hour hang (found
# running the actual 400-config SPY pilot). Reading the data once per worker at
# pool startup instead means each task submission only carries the lightweight
# SampledConfig/RunMeta.
_WORKER_BARS: pl.DataFrame | None = None


def _init_worker(bars_path: str) -> None:
    global _WORKER_BARS
    _WORKER_BARS = pl.read_parquet(bars_path)


def _run_one_config_worker(
    sampled: SampledConfig, *, meta: RunMeta, results_dir: Path, trades_dir: Path, signals_dir: Path
) -> dict:
    assert _WORKER_BARS is not None, "_init_worker must run before any task is submitted"
    return run_one_config(
        sampled, _WORKER_BARS, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir
    )


def _trades_path(trades_dir: Path, experiment_id: str, config_id: str) -> Path:
    return trades_dir / f"experiment_id={experiment_id}" / f"{config_id}.parquet"


def _signals_path(signals_dir: Path, experiment_id: str, config_id: str) -> Path:
    return signals_dir / f"experiment_id={experiment_id}" / f"{config_id}.parquet"


def run_one_config(
    sampled: SampledConfig,
    bars: pl.DataFrame,
    *,
    meta: RunMeta,
    results_dir: Path,
    trades_dir: Path,
    signals_dir: Path,
) -> dict:
    start = time.time()
    result_path = _result_path(results_dir, meta.experiment_id, sampled.config_id)

    try:
        strategy = SilverBulletStrategy(sampled.config)
        strategy.validate_config()
        features = strategy.compute_features({sampled.config.entry_timeframe: bars})
        signals, rejected = strategy.generate_signals(features)

        intents = [strategy.create_entry_order(row) for row in signals.iter_rows(named=True)]
        intents = [i for i in intents if i is not None]

        backtest = run_backtest_single_symbol(bars, intents, config=meta.execution_config)
        metrics = compute_metrics(
            backtest.trades, backtest.portfolio.equity_curve,
            starting_equity=meta.execution_config.starting_equity,
            n_signals=signals.height, n_rejections=len(backtest.rejections),
        )

        if not signals.is_empty():
            atomic_write_json(_signals_path(signals_dir, meta.experiment_id, sampled.config_id).with_suffix(".json"), signals.to_dicts())
        if backtest.trades:
            trades_df = pl.DataFrame(
                [
                    {
                        "trade_id": t.trade_id, "symbol": t.symbol, "side": t.side,
                        "entry_ts": t.entry_fill.fill_ts, "entry_price": t.entry_fill.fill_price,
                        "exit_ts": t.exit_fill.fill_ts if t.exit_fill else None,
                        "exit_price": t.exit_fill.fill_price if t.exit_fill else None,
                        "quantity": t.quantity, "realized_pnl": t.realized_pnl, "realized_r": t.realized_r,
                        "exit_reason": t.exit_reason.value if t.exit_reason else None,
                        "window": t.window, "intrabar_ambiguous": t.intrabar_ambiguous,
                    }
                    for t in backtest.trades
                ]
            )
            trades_path = _trades_path(trades_dir, meta.experiment_id, sampled.config_id)
            trades_path.parent.mkdir(parents=True, exist_ok=True)
            trades_df.write_parquet(trades_path)

        result = {
            "config_id": sampled.config_id,
            "experiment_id": meta.experiment_id,
            "status": "ok",
            "seed": sampled.seed,
            "code_version": meta.code_version,
            "data_manifest_hashes": meta.data_manifest_hashes,
            "runtime_seconds": time.time() - start,
            "config": sampled.config.model_dump(mode="json"),
            "n_signals": signals.height,
            "n_trades": len(backtest.trades),
            "n_rejections": len(backtest.rejections),
            "metrics": vars(metrics),
        }
        atomic_write_json(result_path, result)
        return result

    except Exception as exc:  # noqa: BLE001 -- per-config isolation is the whole point
        error_path = _error_path(results_dir, meta.experiment_id, sampled.config_id)
        atomic_write_json(
            error_path.with_suffix(".json"),
            {"config_id": sampled.config_id, "error": str(exc), "traceback": traceback.format_exc()},
        )
        result = {
            "config_id": sampled.config_id,
            "experiment_id": meta.experiment_id,
            "status": "failed",
            "seed": sampled.seed,
            "code_version": meta.code_version,
            "runtime_seconds": time.time() - start,
            "error": str(exc),
        }
        atomic_write_json(result_path, result)
        return result


def run_experiment(
    sampled_configs: list[SampledConfig],
    bars: pl.DataFrame,
    *,
    meta: RunMeta,
    results_dir: Path,
    trades_dir: Path,
    signals_dir: Path,
    force: bool = False,
    n_workers: int = 1,
) -> list[dict]:
    """Runs every config in `sampled_configs`, skipping ones whose result already
    exists (resume) unless `force=True`. Returns the list of result dicts (loaded
    from disk for skipped configs, freshly computed for the rest).
    """
    pending: list[SampledConfig] = []
    results: list[dict] = []

    for sc in sampled_configs:
        rp = _result_path(results_dir, meta.experiment_id, sc.config_id)
        if not force and rp.exists():
            results.append(read_json(rp))
        else:
            pending.append(sc)

    if not pending:
        return results

    if n_workers <= 1:
        for sc in pending:
            results.append(
                run_one_config(sc, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
            )
    else:
        with tempfile.TemporaryDirectory() as td:
            bars_path = str(Path(td) / "bars.parquet")
            bars.write_parquet(bars_path)
            # Polars keeps a native (Rust) thread pool alive in the parent process
            # the moment it's imported/used. The default "fork" start method only
            # duplicates the calling thread, not that pool -- a forked worker
            # inherits a half-copied, permanently-deadlocked thread pool, so ANY
            # Polars operation in the child (e.g. pl.read_parquet in _init_worker)
            # hangs forever waiting on a mutex whose owning thread doesn't exist in
            # the child. This is the actual root cause of the multi-hour "hang"
            # seen running the real 400-config SPY pilot -- reproduced directly and
            # confirmed by isolating a minimal repro. "spawn" starts each worker as
            # a fresh interpreter instead, avoiding the inherited-thread-pool state
            # entirely.
            ctx = multiprocessing.get_context("spawn")
            with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx, initializer=_init_worker, initargs=(bars_path,)) as executor:
                futures = {
                    executor.submit(
                        _run_one_config_worker, sc, meta=meta, results_dir=results_dir,
                        trades_dir=trades_dir, signals_dir=signals_dir,
                    ): sc
                    for sc in pending
                }
                for fut in as_completed(futures):
                    results.append(fut.result())

    return results
