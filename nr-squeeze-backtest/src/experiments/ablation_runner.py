"""Strategy-generic ablation runner: backtests a full grid of variants and
records per-split (development / validation / holdout) metrics for each.

Why a sibling of runner.py rather than an edit of it: runner.py is hard-wired to
SilverBulletStrategy and computes a single whole-period Metrics per config. This
runner (a) resolves the strategy by name from the registry (spawn-safe -- a
forked/spawned worker re-imports and re-registers it), (b) selects the right
pre-aggregated bar frame per config's (symbol, timeframe), and (c) computes
metrics separately on the development/validation/holdout slices of a SINGLE
backtest. Keeping it separate leaves the working ICT pipeline and its tests
untouched.

The `spawn` ProcessPool + once-per-worker data load pattern is reused verbatim
from runner.py for the reason documented there (Polars' native thread pool
deadlocks under fork; and passing big frames per-task re-pickles them every
time). See ASSUMPTIONS.md "parallel search hung for hours".
"""

from __future__ import annotations

import multiprocessing
import tempfile
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import polars as pl

import src.strategies.donchian_breakout  # noqa: F401 -- registers "donchian_breakout"
from src.engine.events import EquityPoint, Trade
from src.engine.metrics import compute_metrics
from src.engine.simulator import run_backtest_single_symbol
from src.experiments.grid import GridConfig
from src.experiments.validation import ChronologicalSplit
from src.strategies.registry import get_strategy
from src.utils.config_models import ExecutionConfig
from src.utils.serialization import atomic_write_json, read_json

SPLIT_NAMES = ("development", "validation", "holdout")


@dataclass
class RunMeta:
    experiment_id: str
    code_version: str
    strategy_name: str
    execution_config: ExecutionConfig
    split: ChronologicalSplit


def _result_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / f"{config_id}.json"


def _error_path(results_dir: Path, experiment_id: str, config_id: str) -> Path:
    return results_dir / f"experiment_id={experiment_id}" / "errors" / f"{config_id}.json"


def _split_bounds(split: ChronologicalSplit) -> dict[str, tuple[date, date]]:
    return {
        "development": (split.development_start, split.development_end),
        "validation": (split.validation_start, split.validation_end),
        "holdout": (split.holdout_start, split.holdout_end),
    }


def _years(start: date, end: date) -> float:
    return max((end - start).days / 365.25, 1e-9)


def _compact(m, *, n_years: float) -> dict:
    """A small, JSON-friendly slice of Metrics for one split, plus trades/year."""
    return {
        "n_trades": m.n_trades,
        "trades_per_year": m.n_trades / n_years,
        "net_return_pct": m.total_return_pct,
        "sharpe": m.sharpe_ratio,
        "profit_factor": m.profit_factor,
        "win_rate": m.win_rate,
        "max_dd": m.max_drawdown_pct,
        "expectancy": m.expectancy_per_trade,
        "avg_r": m.avg_realized_r,
        "net_pnl": m.net_pnl,
    }


def _split_metrics(
    trades: list[Trade], equity_curve: list[EquityPoint], meta: RunMeta
) -> dict[str, dict]:
    """Run compute_metrics on each chronological split of a single backtest.

    A trade is attributed to the split of its ENTRY timestamp. Each split's
    returns/Sharpe/drawdown are computed on that split's equity points, with the
    split's starting equity taken as the equity just before the window begins
    (global starting equity for the first split) -- so each split reads as a
    self-contained period, which is what an honest out-of-sample comparison
    requires.
    """
    eq = sorted(equity_curve, key=lambda p: p.ts)
    bounds = _split_bounds(meta.split)
    g0 = meta.execution_config.starting_equity

    out: dict[str, dict] = {}
    for name in SPLIT_NAMES:
        start, end = bounds[name]
        s_trades = [t for t in trades if t.entry_fill and start <= t.entry_fill.fill_ts.date() <= end]
        s_points = [p for p in eq if start <= p.ts.date() <= end]
        prior = [p.equity for p in eq if p.ts.date() < start]
        start_equity = prior[-1] if prior else g0
        m = compute_metrics(s_trades, s_points, starting_equity=start_equity)
        out[name] = _compact(m, n_years=_years(start, end))
    return out


def run_one_config(
    gc: GridConfig,
    bars: pl.DataFrame,
    *,
    meta: RunMeta,
    results_dir: Path,
    trades_dir: Path,
) -> dict:
    start = time.time()
    result_path = _result_path(results_dir, meta.experiment_id, gc.config_id)
    try:
        strategy = get_strategy(meta.strategy_name)(gc.config)
        strategy.validate_config()
        features = strategy.compute_features({gc.config.timeframe: bars})
        signals, _ = strategy.generate_signals(features)

        intents = [strategy.create_entry_order(r) for r in signals.iter_rows(named=True)]
        intents = [i for i in intents if i is not None]

        bt = run_backtest_single_symbol(bars, intents, config=meta.execution_config)

        full = compute_metrics(
            bt.trades, bt.portfolio.equity_curve,
            starting_equity=meta.execution_config.starting_equity,
            n_signals=signals.height, n_rejections=len(bt.rejections),
        )
        splits = _split_metrics(bt.trades, bt.portfolio.equity_curve, meta)

        # Flat metrics dict so src/analysis/rankings.top_n and
        # parameter_analysis.categorical_enrichment work unchanged.
        flat: dict = {"full_" + k: v for k, v in _compact(full, n_years=1.0).items()}
        for sname, sm in splits.items():
            for k, v in sm.items():
                flat[f"{sname}_{k}"] = v

        if bt.trades:
            trades_df = pl.DataFrame(
                [
                    {
                        "trade_id": t.trade_id, "symbol": t.symbol, "side": t.side,
                        "entry_ts": t.entry_fill.fill_ts, "entry_price": t.entry_fill.fill_price,
                        "exit_ts": t.exit_fill.fill_ts if t.exit_fill else None,
                        "exit_price": t.exit_fill.fill_price if t.exit_fill else None,
                        "realized_pnl": t.realized_pnl, "realized_r": t.realized_r,
                        "exit_reason": t.exit_reason.value if t.exit_reason else None,
                    }
                    for t in bt.trades
                ]
            )
            tp = trades_dir / f"experiment_id={meta.experiment_id}" / f"{gc.config_id}.parquet"
            tp.parent.mkdir(parents=True, exist_ok=True)
            trades_df.write_parquet(tp)

        result = {
            "config_id": gc.config_id,
            "experiment_id": meta.experiment_id,
            "status": "ok",
            "code_version": meta.code_version,
            "strategy": meta.strategy_name,
            "runtime_seconds": time.time() - start,
            "config": gc.config.model_dump(mode="json"),
            "n_signals": signals.height,
            "n_trades": len(bt.trades),
            "n_rejections": len(bt.rejections),
            "metrics": flat,
        }
        atomic_write_json(result_path, result)
        return result

    except Exception as exc:  # noqa: BLE001 -- per-config isolation
        atomic_write_json(
            _error_path(results_dir, meta.experiment_id, gc.config_id),
            {"config_id": gc.config_id, "error": str(exc), "traceback": traceback.format_exc()},
        )
        result = {
            "config_id": gc.config_id, "experiment_id": meta.experiment_id,
            "status": "failed", "runtime_seconds": time.time() - start,
            "config": gc.config.model_dump(mode="json"), "error": str(exc),
        }
        atomic_write_json(result_path, result)
        return result


# --- Parallel worker plumbing (spawn-safe; see module docstring) ---

_WORKER_PATHS: dict[str, str] = {}
_WORKER_CACHE: dict[str, pl.DataFrame] = {}


def _key(symbol: str, timeframe: str) -> str:
    return f"{symbol}|{timeframe}"


def _init_worker(paths: dict[str, str]) -> None:
    global _WORKER_PATHS, _WORKER_CACHE
    _WORKER_PATHS = dict(paths)
    _WORKER_CACHE = {}


def _worker_bars(symbol: str, timeframe: str) -> pl.DataFrame:
    k = _key(symbol, timeframe)
    if k not in _WORKER_CACHE:
        _WORKER_CACHE[k] = pl.read_parquet(_WORKER_PATHS[k])
    return _WORKER_CACHE[k]


def _run_one_worker(gc: GridConfig, *, meta: RunMeta, results_dir: Path, trades_dir: Path) -> dict:
    bars = _worker_bars(gc.config.symbol, gc.config.timeframe)
    return run_one_config(gc, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir)


def run_ablation(
    grid: list[GridConfig],
    frames: dict[str, pl.DataFrame],
    *,
    meta: RunMeta,
    results_dir: Path,
    trades_dir: Path,
    force: bool = False,
    n_workers: int = 1,
) -> list[dict]:
    """Run every variant in `grid`. `frames` maps "SYMBOL|TIMEFRAME" -> bars.
    Resumable: a variant whose result JSON exists is skipped unless force=True."""
    pending: list[GridConfig] = []
    results: list[dict] = []
    for gc in grid:
        rp = _result_path(results_dir, meta.experiment_id, gc.config_id)
        if not force and rp.exists():
            results.append(read_json(rp))
        else:
            pending.append(gc)

    if not pending:
        return results

    if n_workers <= 1:
        for gc in pending:
            bars = frames[_key(gc.config.symbol, gc.config.timeframe)]
            results.append(run_one_config(gc, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir))
        return results

    with tempfile.TemporaryDirectory() as td:
        paths: dict[str, str] = {}
        for k, df in frames.items():
            p = str(Path(td) / f"{k.replace('|', '_')}.parquet")
            df.write_parquet(p)
            paths[k] = p
        ctx = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(
            max_workers=n_workers, mp_context=ctx, initializer=_init_worker, initargs=(paths,)
        ) as ex:
            futures = {
                ex.submit(_run_one_worker, gc, meta=meta, results_dir=results_dir, trades_dir=trades_dir): gc
                for gc in pending
            }
            for fut in as_completed(futures):
                results.append(fut.result())
    return results
