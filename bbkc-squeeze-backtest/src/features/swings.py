"""N-bar symmetric fractal swing highs/lows, with explicit confirmation delay.

A pivot at bar index i (left=L, right=R bars) requires bars i-L..i-1 and
i+1..i+R to be known. It cannot be considered AVAILABLE until bar i+R closes.
Every swing therefore carries both:
  - pivot_ts: the pivot bar's open timestamp (when the price extreme occurred)
  - availability_ts: bar[i+R].bar_close_ts (when the pivot becomes usable)

Consumers (liquidity levels, market-structure checks) MUST filter on
availability_ts <= current processing timestamp, never on pivot_ts -- a pivot is
never retroactively available before its right-side bars have closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import polars as pl

TieHandling = Literal["first", "last", "reject"]


@dataclass(frozen=True)
class SwingConfig:
    left_bars: int = 5
    right_bars: int = 5
    timeframe: str = "1min"
    min_prominence_points: float = 0.0
    tie_handling: TieHandling = "reject"
    max_age_bars: int | None = None


def _is_swing_high(highs: list[float], i: int, left: int, right: int, tie: TieHandling) -> bool:
    window = highs[i - left : i] + highs[i + 1 : i + 1 + right]
    pivot = highs[i]
    if tie == "reject":
        return all(pivot > v for v in window)
    if tie == "first":
        # pivot qualifies if no earlier-in-window bar exceeds it and no bar strictly exceeds it
        return all(pivot >= v for v in window) and any(pivot > v for v in window)
    # "last": mirror of "first", pivot wins ties against the left side only
    left_win = highs[i - left : i]
    right_win = highs[i + 1 : i + 1 + right]
    return all(pivot >= v for v in left_win) and all(pivot > v for v in right_win)


def _is_swing_low(lows: list[float], i: int, left: int, right: int, tie: TieHandling) -> bool:
    window = lows[i - left : i] + lows[i + 1 : i + 1 + right]
    pivot = lows[i]
    if tie == "reject":
        return all(pivot < v for v in window)
    if tie == "first":
        return all(pivot <= v for v in window) and any(pivot < v for v in window)
    left_win = lows[i - left : i]
    right_win = lows[i + 1 : i + 1 + right]
    return all(pivot <= v for v in left_win) and all(pivot < v for v in right_win)


def detect_swings(df: pl.DataFrame, *, config: SwingConfig) -> pl.DataFrame:
    """`df` must be single-symbol/timeframe, ascending-sorted, with columns
    high/low/bar_open_ts/bar_close_ts."""
    n = df.height
    L, R = config.left_bars, config.right_bars
    if n < L + R + 1:
        return _empty_swing_frame()

    high = df["high"].to_list()
    low = df["low"].to_list()
    open_ts = df["bar_open_ts"].to_list()
    close_ts = df["bar_close_ts"].to_list()
    symbol = df["symbol"][0] if "symbol" in df.columns else None

    records: list[dict] = []
    for i in range(L, n - R):
        if _is_swing_high(high, i, L, R, config.tie_handling):
            prominence = high[i] - max(high[i - L : i] + high[i + 1 : i + 1 + R])
            if prominence >= config.min_prominence_points:
                records.append(
                    {
                        "swing_id": f"swh_{symbol}_{config.timeframe}_{i}",
                        "symbol": symbol,
                        "timeframe": config.timeframe,
                        "kind": "high",
                        "price": high[i],
                        "pivot_ts": open_ts[i],
                        "availability_ts": close_ts[i + R],
                        "source_row_index": i,
                        "left_bars": L,
                        "right_bars": R,
                    }
                )
        if _is_swing_low(low, i, L, R, config.tie_handling):
            prominence = min(low[i - L : i] + low[i + 1 : i + 1 + R]) - low[i]
            if prominence >= config.min_prominence_points:
                records.append(
                    {
                        "swing_id": f"swl_{symbol}_{config.timeframe}_{i}",
                        "symbol": symbol,
                        "timeframe": config.timeframe,
                        "kind": "low",
                        "price": low[i],
                        "pivot_ts": open_ts[i],
                        "availability_ts": close_ts[i + R],
                        "source_row_index": i,
                        "left_bars": L,
                        "right_bars": R,
                    }
                )

    return pl.DataFrame(records) if records else _empty_swing_frame()


def _empty_swing_frame() -> pl.DataFrame:
    schema = {
        "swing_id": pl.Utf8, "symbol": pl.Utf8, "timeframe": pl.Utf8, "kind": pl.Utf8,
        "price": pl.Float64, "pivot_ts": pl.Datetime("us", "UTC"),
        "availability_ts": pl.Datetime("us", "UTC"), "source_row_index": pl.Int64,
        "left_bars": pl.Int64, "right_bars": pl.Int64,
    }
    return pl.DataFrame(schema=schema)


def available_swings_as_of(swings: pl.DataFrame, as_of_ts) -> pl.DataFrame:
    """The only sanctioned way to query swings for use in signal/execution logic:
    filters strictly on availability_ts, never pivot_ts."""
    if swings.is_empty():
        return swings
    return swings.filter(pl.col("availability_ts") <= as_of_ts)
