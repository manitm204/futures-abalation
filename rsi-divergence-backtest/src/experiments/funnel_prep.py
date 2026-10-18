"""Backtest plumbing for the screening funnel.

`build_dev_records` re-backtests every grid config ONCE on development-only
bars (data physically truncated at the development end, so nothing later can
leak in) and captures, per config: stage-1 integrity issues, the full stage-2/3/5
metric set from the daily mark-to-market series, and the daily return vector
(kept for the whole universe: dedup correlation and the DSR's effective-trial /
Sharpe-dispersion estimates need the broad search, not only survivors).

`run_jobs` executes arbitrary single-config backtests (stress scenarios,
perturbations, validation, transfer) over the same spawn-safe worker pool.
"""

from __future__ import annotations

import multiprocessing
import tempfile
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl

from src.analysis.daily_performance import daily_equity, window_metrics
from src.experiments.funnel_config import FunnelConfig
from src.experiments import integrity as mr_integrity
from src.experiments import rsi_integrity
from src.strategies.mean_reversion.backtest import (
    MRData,
    MRParams,
    scale_variable_costs,
    simulate_mean_reversion,
)
from src.strategies.rsi_divergence.backtest import RSIData, RSIParams, simulate_rsi_divergence
from src.utils.config_models import ExecutionConfig


@dataclass(frozen=True)
class Family:
    """Strategy-family plumbing: data object, simulator, per-sim integrity check,
    and the exit reasons counted into each record (`full_n_<reason>s`)."""

    data_cls: type
    simulate: object
    check: object
    exit_reasons: tuple[str, ...]


FAMILIES = {
    "mean_reversion": Family(MRData, simulate_mean_reversion, mr_integrity.check_sim_integrity,
                             ("z_exit", "time_exit", "stop_exit")),
    "rsi_divergence": Family(RSIData, simulate_rsi_divergence, rsi_integrity.check_sim_integrity,
                             ("stop_exit", "target_exit", "time_exit")),
}


def family_for(fcfg: FunnelConfig) -> Family:
    """The YAML's `strategy` -> its family (mean_reversion_v2 is the mean_reversion family)."""
    name = "mean_reversion" if fcfg.strategy.startswith("mean_reversion") else fcfg.strategy
    if name not in FAMILIES:
        raise ValueError(f"Unknown strategy {fcfg.strategy!r}; expected one of {sorted(FAMILIES)}")
    return FAMILIES[name]

PARAM_KEYS = ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
              "max_hold", "trend_filter")


def flatten_metrics(prefix: str, m: dict) -> dict:
    """Flatten per-year dicts to `{prefix}{name}_{year}` columns (parquet-friendly)."""
    out = {}
    for k, v in m.items():
        if isinstance(v, dict):
            for y, x in v.items():
                out[f"{prefix}{k}_{y}"] = x
        elif k == "flags":
            out[f"{prefix}flags"] = ";".join(v)
        else:
            out[f"{prefix}{k}"] = v
    return out


@dataclass(frozen=True)
class Job:
    key: str
    params: MRParams | RSIParams
    window_start: date
    window_end: date
    cost_multiplier: float = 1.0
    entry_delay_bars: int = 0
    missed_entry_frac: float = 0.0
    seed: int = 0
    return_series: bool = False


def _metric_kwargs(fcfg: FunnelConfig) -> dict:
    return {"periods_per_year": fcfg.metrics.periods_per_year,
            "risk_free_rate_annual": fcfg.metrics.risk_free_rate_annual,
            "top_trades_k": fcfg.time_stability.top_trades_k,
            "top_trades_frac": fcfg.time_stability.top_trades_frac}


def build_dev_record(ce, data, *, fcfg: FunnelConfig,
                     exec_config: ExecutionConfig) -> tuple[dict, np.ndarray]:
    """`ce`: a grid ConfigEntry (mr_grid or rsi_grid); `data`: the family's data object."""
    cfg = ce.config
    fam = family_for(fcfg)
    eq0 = exec_config.starting_equity
    sim = fam.simulate(data, cfg, exec_config=exec_config, starting_equity=eq0)
    eq = daily_equity(sim, data, eq0)
    dev = fcfg.data.development
    m, rets = window_metrics(sim, data, eq, start=dev.start, end=dev.end, starting_equity=eq0,
                             **_metric_kwargs(fcfg))
    rec = {"config_id": ce.config_id, **cfg.model_dump(mode="json"),
           "integrity_issues": ";".join(fam.check(sim, data, exec_config, cfg)),
           **{f"full_n_{k}s": int((sim.exit_reason == k).sum()) for k in fam.exit_reasons},
           **flatten_metrics("dev_", m)}
    return rec, rets.astype(np.float32)


def run_job(job: Job, data, *, fcfg: FunnelConfig, exec_config: ExecutionConfig) -> dict:
    fam = family_for(fcfg)
    ec = scale_variable_costs(exec_config, job.cost_multiplier) if job.cost_multiplier != 1.0 else exec_config
    eq0 = exec_config.starting_equity
    sim = fam.simulate(data, job.params, exec_config=ec, starting_equity=eq0,
                           entry_delay_bars=job.entry_delay_bars,
                           missed_entry_frac=job.missed_entry_frac, stress_seed=job.seed)
    eq = daily_equity(sim, data, eq0)
    m, rets = window_metrics(sim, data, eq, start=job.window_start, end=job.window_end,
                             starting_equity=eq0, **_metric_kwargs(fcfg))
    out = {"key": job.key, "metrics": m, "integrity_issues": fam.check(sim, data, ec, job.params)}
    if job.return_series:
        out["returns"] = rets.astype(np.float32)
        out["intervals"] = list(zip((data.ts[i] for i in sim.entry_idx), (data.ts[i] for i in sim.exit_idx)))
    return out


# --- spawn plumbing (Polars' thread pool deadlocks under fork) ---
_PATHS: dict[str, str] = {}
_DATA: dict[str, MRData | RSIData] = {}
_CTX: dict = {}


def _dkey(symbol: str, tf: str) -> str:
    return f"{symbol}|{tf}"


def _init(paths, fcfg, exec_config):
    global _PATHS, _DATA, _CTX
    _PATHS, _DATA, _CTX = dict(paths), {}, {"fcfg": fcfg, "exec": exec_config}


def _data_for(symbol: str, tf: str):
    k = _dkey(symbol, tf)
    if k not in _DATA:
        _DATA[k] = family_for(_CTX["fcfg"]).data_cls(pl.read_parquet(_PATHS[k]))
    return _DATA[k]


def _record_worker(ce):
    return build_dev_record(ce, _data_for(ce.config.symbol, ce.config.timeframe),
                            fcfg=_CTX["fcfg"], exec_config=_CTX["exec"])


def _job_worker(job: Job):
    return run_job(job, _data_for(job.params.symbol, job.params.timeframe),
                   fcfg=_CTX["fcfg"], exec_config=_CTX["exec"])


def _pool_map(fn, items, frames, *, fcfg, exec_config, n_workers, chunksize=16):
    """frames: {"SYMBOL|tf": bars}. Order of results matches `items`."""
    if n_workers <= 1 or len(items) < 8:
        _init({}, fcfg, exec_config)
        for k, df in frames.items():
            _DATA[k] = family_for(fcfg).data_cls(df)
        return [fn(it) for it in items]
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for k, df in frames.items():
            p = str(Path(td) / f"{k.replace('|', '_')}.parquet")
            df.write_parquet(p)
            paths[k] = p
        ctx = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx, initializer=_init,
                                 initargs=(paths, fcfg, exec_config)) as ex:
            return list(ex.map(fn, items, chunksize=chunksize))


def build_dev_records(grid: list, frames: dict[str, pl.DataFrame], *, fcfg: FunnelConfig,
                      exec_config: ExecutionConfig, n_workers: int = 1) -> tuple[list[dict], np.ndarray]:
    res = _pool_map(_record_worker, grid, frames, fcfg=fcfg, exec_config=exec_config, n_workers=n_workers)
    records = [r for r, _ in res]
    lengths = {len(x) for _, x in res}
    if len(lengths) != 1:
        raise RuntimeError(f"Daily return vectors differ in length across configs: {lengths}")
    return records, np.vstack([x for _, x in res])


def run_jobs(jobs: list[Job], frames: dict[str, pl.DataFrame], *, fcfg: FunnelConfig,
             exec_config: ExecutionConfig, n_workers: int = 1) -> dict[str, dict]:
    if not jobs:
        return {}
    res = _pool_map(_job_worker, jobs, frames, fcfg=fcfg, exec_config=exec_config, n_workers=n_workers,
                    chunksize=4)
    return {r["key"]: r for r in res}
