"""Runner for the channel-breakout grid: backtests each variant with the custom
trailing-channel backtester and records per-split metrics.

Reuses the per-split metric helpers and RunMeta from ablation_runner (both are
strategy-agnostic -- they operate on engine Trade / EquityPoint objects), and
the spawn-pool pattern (Polars deadlocks under fork; see ASSUMPTIONS.md).
ChannelData (precomputed indicators) is built once per timeframe per worker and
cached, so the thousands of configs sharing a timeframe don't re-aggregate it.
"""

from __future__ import annotations

import multiprocessing
import tempfile
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import polars as pl

from src.engine.metrics import compute_metrics
from src.experiments.ablation_runner import RunMeta, _compact, _split_metrics
from src.experiments.channel_grid import ConfigEntry
from src.strategies.channel_breakout.backtest import ChannelData, run_channel_backtest
from src.utils.serialization import atomic_write_json, read_json


def _result_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / f"{config_id}.json"


def _error_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / "errors" / f"{config_id}.json"


def run_one_config(ce: ConfigEntry, data: ChannelData, *, meta: RunMeta, results_dir: Path) -> dict:
    start = time.time()
    cfg = ce.config
    result_path = _result_path(results_dir, meta.experiment_id, ce.config_id)
    try:
        trades, equity = run_channel_backtest(
            data, cfg, exec_config=meta.execution_config,
            starting_equity=meta.execution_config.starting_equity,
        )
        full = compute_metrics(trades, equity, starting_equity=meta.execution_config.starting_equity)
        splits = _split_metrics(trades, equity, meta)

        flat: dict = {"full_" + k: v for k, v in _compact(full, n_years=1.0).items()}
        for sname, sm in splits.items():
            for k, v in sm.items():
                flat[f"{sname}_{k}"] = v

        result = {
            "config_id": ce.config_id, "experiment_id": meta.experiment_id, "status": "ok",
            "strategy": "channel_breakout", "runtime_seconds": time.time() - start,
            "config": cfg.model_dump(mode="json"),
            "exit_lookback": cfg.exit_lookback,
            "n_trades": len(trades), "metrics": flat,
        }
        atomic_write_json(result_path, result)
        return result
    except Exception as exc:  # noqa: BLE001
        atomic_write_json(
            _error_path(results_dir, meta.experiment_id, ce.config_id),
            {"config_id": ce.config_id, "error": str(exc), "traceback": traceback.format_exc()},
        )
        result = {"config_id": ce.config_id, "experiment_id": meta.experiment_id, "status": "failed",
                  "config": cfg.model_dump(mode="json"), "error": str(exc)}
        atomic_write_json(result_path, result)
        return result


# --- spawn-safe worker plumbing ---
_PATHS: dict[str, str] = {}
_DATA: dict[str, ChannelData] = {}
_ATR_PERIOD = 14


def _init_worker(paths: dict[str, str], atr_period: int) -> None:
    global _PATHS, _DATA, _ATR_PERIOD
    _PATHS = dict(paths)
    _DATA = {}
    _ATR_PERIOD = atr_period


def _data_for(timeframe: str) -> ChannelData:
    if timeframe not in _DATA:
        _DATA[timeframe] = ChannelData(pl.read_parquet(_PATHS[timeframe]), atr_period=_ATR_PERIOD)
    return _DATA[timeframe]


def _run_worker(ce: ConfigEntry, *, meta: RunMeta, results_dir: Path) -> dict:
    return run_one_config(ce, _data_for(ce.config.timeframe), meta=meta, results_dir=results_dir)


def run_channel_experiment(
    grid: list[ConfigEntry],
    frames: dict[str, pl.DataFrame],
    *,
    meta: RunMeta,
    results_dir: Path,
    atr_period: int = 14,
    force: bool = False,
    n_workers: int = 1,
) -> list[dict]:
    """`frames` maps timeframe -> bars. Resumable (skips existing result JSON)."""
    pending: list[ConfigEntry] = []
    results: list[dict] = []
    for ce in grid:
        rp = _result_path(results_dir, meta.experiment_id, ce.config_id)
        if not force and rp.exists():
            results.append(read_json(rp))
        else:
            pending.append(ce)
    if not pending:
        return results

    if n_workers <= 1:
        data = {tf: ChannelData(df, atr_period=atr_period) for tf, df in frames.items()}
        for ce in pending:
            results.append(run_one_config(ce, data[ce.config.timeframe], meta=meta, results_dir=results_dir))
        return results

    with tempfile.TemporaryDirectory() as td:
        paths: dict[str, str] = {}
        for tf, df in frames.items():
            p = str(Path(td) / f"{tf}.parquet")
            df.write_parquet(p)
            paths[tf] = p
        ctx = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(
            max_workers=n_workers, mp_context=ctx, initializer=_init_worker, initargs=(paths, atr_period)
        ) as ex:
            futs = {ex.submit(_run_worker, ce, meta=meta, results_dir=results_dir): ce for ce in pending}
            for fut in as_completed(futs):
                results.append(fut.result())
    return results
