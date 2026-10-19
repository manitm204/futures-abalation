"""Market-structure shift (MSS) detection after a liquidity sweep.

Following a downside sweep (bullish reversal context), an MSS is a break of the
most recently AVAILABLE confirmed swing high in the up direction. Following an
upside sweep (bearish reversal context), an MSS is a break of the most recently
available confirmed swing low, downward.

Causal guarantee: only swings whose availability_ts is <= the sweep's
confirmation_ts are eligible as "the most recently available" reference swing --
a swing cannot be broken by reference to a pivot the market didn't know about yet.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass
from typing import Literal

import polars as pl

BreakMode = Literal["wick", "close"]


@dataclass(frozen=True)
class MarketStructureConfig:
    required: bool = True
    break_mode: BreakMode = "close"
    max_bars_after_sweep: int = 10
    require_displacement: bool = False
    displacement_col: str = "displacement_body_atr"


MSS_SCHEMA = {
    "mss_id": pl.Utf8, "symbol": pl.Utf8, "sweep_id": pl.Utf8, "direction": pl.Utf8,
    "reference_swing_id": pl.Utf8, "reference_price": pl.Float64,
    "reference_availability_ts": pl.Datetime("us", "UTC"),
    "break_bar_open_ts": pl.Datetime("us", "UTC"), "break_price": pl.Float64,
    "bars_after_sweep": pl.Int64,
}


def _empty_mss() -> pl.DataFrame:
    return pl.DataFrame(schema=MSS_SCHEMA)


def detect_market_structure_shifts(
    bars: pl.DataFrame, sweeps: pl.DataFrame, swings: pl.DataFrame, *, config: MarketStructureConfig
) -> pl.DataFrame:
    if bars.is_empty() or sweeps.is_empty() or swings.is_empty():
        return _empty_mss()

    open_ts = bars["bar_open_ts"].to_list()
    high = bars["high"].to_list()
    low = bars["low"].to_list()
    close = bars["close"].to_list()
    symbol = bars["symbol"][0] if "symbol" in bars.columns else None
    n = bars.height

    # Pre-split and pre-sort swings by kind once, so each sweep's "most recently
    # available matching-kind swing" lookup is a bisect instead of a fresh Polars
    # .filter()+.sort() call -- per-call Polars overhead dominates when this runs
    # once per sweep across thousands of sweeps in a multi-year backtest.
    swings_sorted = swings.sort("availability_ts")
    swings_by_kind: dict[str, tuple[list, list, list]] = {}
    for kind in ("high", "low"):
        k = swings_sorted.filter(pl.col("kind") == kind)
        swings_by_kind[kind] = (
            k["availability_ts"].to_list(), k["price"].to_list(), k["swing_id"].to_list()
        )

    def _latest_available_swing(kind: str, as_of_ts):
        avail_list, price_list, id_list = swings_by_kind[kind]
        idx = bisect.bisect_right(avail_list, as_of_ts) - 1
        if idx < 0:
            return None
        return price_list[idx], id_list[idx], avail_list[idx]

    records: list[dict] = []
    for sweep in sweeps.iter_rows(named=True):
        conf_ts = sweep["confirmation_ts"]
        start_idx = bisect.bisect_left(open_ts, conf_ts)
        if start_idx >= n:
            continue

        want_swing_kind = "high" if sweep["direction"] == "bullish" else "low"
        ref_lookup = _latest_available_swing(want_swing_kind, conf_ts)
        if ref_lookup is None:
            continue
        ref_price, ref_swing_id, ref_availability_ts = ref_lookup

        end_idx = min(start_idx + config.max_bars_after_sweep, n)
        for j in range(start_idx, end_idx):
            if config.require_displacement:
                disp_col = config.displacement_col
                if disp_col in bars.columns and bars[disp_col][j] is not True:
                    continue
            if sweep["direction"] == "bullish":
                broke = (high[j] > ref_price) if config.break_mode == "wick" else (close[j] > ref_price)
                break_price = high[j] if config.break_mode == "wick" else close[j]
            else:
                broke = (low[j] < ref_price) if config.break_mode == "wick" else (close[j] < ref_price)
                break_price = low[j] if config.break_mode == "wick" else close[j]

            if broke:
                records.append(
                    {
                        "mss_id": f"mss_{symbol}_{sweep['sweep_id']}",
                        "symbol": symbol,
                        "sweep_id": sweep["sweep_id"],
                        "direction": sweep["direction"],
                        "reference_swing_id": ref_swing_id,
                        "reference_price": ref_price,
                        "reference_availability_ts": ref_availability_ts,
                        "break_bar_open_ts": open_ts[j],
                        "break_price": break_price,
                        "bars_after_sweep": j - start_idx,
                    }
                )
                break

    return pl.DataFrame(records, schema=MSS_SCHEMA) if records else _empty_mss()
