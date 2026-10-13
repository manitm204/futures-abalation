"""Re-backtest every config once and capture the compact per-config payload the
funnel needs: development / validation / holdout metrics, the development
trades-by-year counts, and the development monthly net-return series (for the
bootstrap p-value and the dedup correlation). One pass, spawn-parallel, with
ChannelData cached per timeframe per worker.
"""

from __future__ import annotations

import multiprocessing
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import polars as pl

from src.engine.metrics import compute_metrics
from src.experiments.ablation_runner import RunMeta, _split_metrics
from src.experiments.channel_grid import ConfigEntry
from src.experiments.validation import ChronologicalSplit
from src.strategies.channel_breakout.backtest import ChannelData, run_channel_backtest


def _dev_month_grid(split: ChronologicalSplit) -> list[tuple[int, int]]:
    months, y, m = [], split.development_start.year, split.development_start.month
    end = (split.development_end.year, split.development_end.month)
    while (y, m) <= end:
        months.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return months


def _dev_series(trades, split: ChronologicalSplit, starting_equity: float):
    months = _dev_month_grid(split)
    pnl = {mm: 0.0 for mm in months}
    by_year: dict[int, int] = {}
    s, e = split.development_start, split.development_end
    for t in trades:
        if t.entry_fill is None:
            continue
        d = t.entry_fill.fill_ts.date()
        if s <= d <= e:
            pnl[(d.year, d.month)] = pnl.get((d.year, d.month), 0.0) + (t.realized_pnl or 0.0)
            by_year[d.year] = by_year.get(d.year, 0) + 1
    monthly = [pnl[mm] / starting_equity for mm in months]
    return monthly, {str(y): c for y, c in by_year.items()}  # str keys -> parquet-safe struct


def build_record(ce: ConfigEntry, data: ChannelData, *, meta: RunMeta) -> dict:
    cfg = ce.config
    eq0 = meta.execution_config.starting_equity
    trades, equity = run_channel_backtest(data, cfg, exec_config=meta.execution_config, starting_equity=eq0)
    full = compute_metrics(trades, equity, starting_equity=eq0)  # noqa: F841 (kept for parity/debug)
    splits = _split_metrics(trades, equity, meta)
    monthly, by_year = _dev_series(trades, meta.split, eq0)
    d, v, ho = splits["development"], splits["validation"], splits["holdout"]
    return {
        "config_id": ce.config_id, **cfg.model_dump(mode="json"), "exit_lookback": cfg.exit_lookback,
        "dev_n_trades": d["n_trades"], "dev_trades_by_year": by_year,
        "dev_net_return": d["net_return_pct"], "dev_profit_factor": d["profit_factor"], "dev_sharpe": d["sharpe"],
        "val_net_return": v["net_return_pct"], "val_sharpe": v["sharpe"], "val_n_trades": v["n_trades"],
        "holdout_net_return": ho["net_return_pct"], "holdout_sharpe": ho["sharpe"], "holdout_n_trades": ho["n_trades"],
        "monthly_returns": monthly,
    }


# --- spawn plumbing ---
_PATHS: dict[str, str] = {}
_DATA: dict[str, ChannelData] = {}
_META: RunMeta | None = None
_ATR = 14


def _init(paths, meta, atr):
    global _PATHS, _DATA, _META, _ATR
    _PATHS, _DATA, _META, _ATR = dict(paths), {}, meta, atr


def _data_for(tf: str) -> ChannelData:
    if tf not in _DATA:
        _DATA[tf] = ChannelData(pl.read_parquet(_PATHS[tf]), atr_period=_ATR)
    return _DATA[tf]


def _worker(ce: ConfigEntry) -> dict:
    assert _META is not None
    return build_record(ce, _data_for(ce.config.timeframe), meta=_META)


def build_records(
    grid: list[ConfigEntry], frames: dict[str, pl.DataFrame], *, meta: RunMeta,
    atr_period: int = 14, n_workers: int = 1,
) -> list[dict]:
    if n_workers <= 1:
        data = {tf: ChannelData(df, atr_period=atr_period) for tf, df in frames.items()}
        return [build_record(ce, data[ce.config.timeframe], meta=meta) for ce in grid]

    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for tf, df in frames.items():
            p = str(Path(td) / f"{tf}.parquet")
            df.write_parquet(p)
            paths[tf] = p
        ctx = multiprocessing.get_context("spawn")
        out: list[dict] = []
        with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx,
                                 initializer=_init, initargs=(paths, meta, atr_period)) as ex:
            futs = [ex.submit(_worker, ce) for ce in grid]
            for f in as_completed(futs):
                out.append(f.result())
    return out
