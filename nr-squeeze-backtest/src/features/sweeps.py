"""Liquidity sweep detection.

A sweep = price trades beyond a known (already AVAILABLE, per its
availability_ts) liquidity level, then closes back on the original side within
K completed bars.

  Bullish reversal context (sweep of a low): a bar's low trades below the
  level, and within K bars (inclusive of the same bar) the CLOSE reclaims
  above the level.
  Bearish reversal context (sweep of a high): a bar's high trades above the
  level, and within K bars the close reclaims below the level.

Only levels whose availability_ts is at or before the penetration bar's
bar_open_ts are eligible -- a level cannot be swept before it exists.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass
from typing import Literal

import numpy as np
import polars as pl

SweepDirection = Literal["bullish", "bearish"]

# A level with no age limit remains eligible for the rest of the dataset, which
# for a multi-year backtest means detect_sweeps' per-level scan window grows
# without bound as levels accumulate -- O(n_levels x n_bars) becomes
# computationally infeasible at full-history scale (see ASSUMPTIONS.md). A
# level going stale after roughly a day-and-a-half of 1-min bars is also more
# faithful to ICT liquidity-sweep practice, where sweeps of long-forgotten
# levels aren't the setups being described. Callers that genuinely want
# unbounded age can still pass max_level_age_bars=None explicitly.
DEFAULT_MAX_LEVEL_AGE_BARS = 500


@dataclass(frozen=True)
class SweepConfig:
    eligible_level_types: tuple[str, ...] = ("prior_session_low", "prior_session_high", "swing_low", "swing_high")
    min_penetration_points: float = 0.0
    max_penetration_points: float | None = None
    min_penetration_atr_multiple: float = 0.0
    max_penetration_atr_multiple: float | None = None
    k_bars: int = 3
    timeframe: str = "1min"
    max_level_age_bars: int | None = DEFAULT_MAX_LEVEL_AGE_BARS
    allow_repeated_sweeps: bool = False


SWEEP_SCHEMA = {
    "sweep_id": pl.Utf8, "symbol": pl.Utf8, "timeframe": pl.Utf8, "direction": pl.Utf8,
    "level_id": pl.Utf8, "level_type": pl.Utf8, "level_price": pl.Float64,
    "penetration_bar_open_ts": pl.Datetime("us", "UTC"), "penetration_price": pl.Float64,
    "penetration_points": pl.Float64, "confirmation_ts": pl.Datetime("us", "UTC"),
    "bars_to_reclaim": pl.Int64,
}


def _empty_sweeps() -> pl.DataFrame:
    return pl.DataFrame(schema=SWEEP_SCHEMA)


def detect_sweeps(
    bars: pl.DataFrame, levels: pl.DataFrame, *, config: SweepConfig, atr_col: str = "atr"
) -> pl.DataFrame:
    """`bars`: single-symbol ascending-sorted with high/low/close/bar_open_ts/atr.
    `levels`: liquidity levels (src/features/liquidity.py schema).
    """
    if bars.is_empty() or levels.is_empty():
        return _empty_sweeps()

    eligible = levels.filter(pl.col("type").is_in(config.eligible_level_types))
    if eligible.is_empty():
        return _empty_sweeps()

    n = bars.height
    open_ts = bars["bar_open_ts"].to_list()  # used for bisect + timestamp output
    high_arr = bars["high"].to_numpy()
    low_arr = bars["low"].to_numpy()
    close_arr = bars["close"].to_numpy()
    atr_arr = bars[atr_col].to_numpy() if atr_col in bars.columns else np.full(n, np.nan)
    symbol = bars["symbol"][0] if "symbol" in bars.columns else None

    records: list[dict] = []
    swept_level_ids: set[str] = set()

    for lvl in eligible.iter_rows(named=True):
        level_price = lvl["price"]
        level_avail = lvl["availability_ts"]
        is_high_type = "high" in lvl["type"]
        direction: SweepDirection = "bearish" if is_high_type else "bullish"

        # Bound the scan to [start_idx, end_idx): a level cannot be swept before
        # it's available (bisect finds the first eligible bar directly, instead
        # of linear-scanning from bar 0), and goes stale after max_level_age_bars
        # bars (bounds the otherwise-unbounded per-level scan window).
        start_idx = bisect.bisect_left(open_ts, level_avail)
        if start_idx >= n:
            continue
        end_idx = n if config.max_level_age_bars is None else min(start_idx + config.max_level_age_bars, n)
        if end_idx <= start_idx:
            continue

        # Vectorized candidate filtering: only bars that actually penetrate the
        # level are worth the more detailed (K-bar reclaim, ATR-filter) checks
        # below, and penetrations are typically a small fraction of the window.
        if is_high_type:
            candidate_mask = high_arr[start_idx:end_idx] > level_price
        else:
            candidate_mask = low_arr[start_idx:end_idx] < level_price
        candidate_idxs = np.nonzero(candidate_mask)[0] + start_idx

        for i in candidate_idxs:
            i = int(i)
            if not config.allow_repeated_sweeps and lvl["level_id"] in swept_level_ids:
                break

            penetration_points = (high_arr[i] - level_price) if is_high_type else (level_price - low_arr[i])
            if penetration_points < config.min_penetration_points:
                continue
            if config.max_penetration_points is not None and penetration_points > config.max_penetration_points:
                continue
            a = atr_arr[i]
            if a and not np.isnan(a):
                pen_atr = penetration_points / a
                if pen_atr < config.min_penetration_atr_multiple:
                    continue
                if config.max_penetration_atr_multiple is not None and pen_atr > config.max_penetration_atr_multiple:
                    continue

            confirmation_ts = None
            bars_to_reclaim = None
            for j in range(i, min(i + config.k_bars, n)):
                reclaimed = (close_arr[j] < level_price) if is_high_type else (close_arr[j] > level_price)
                if reclaimed:
                    confirmation_ts = open_ts[j]
                    bars_to_reclaim = j - i
                    break

            if confirmation_ts is None:
                continue  # not reclaimed within K bars -- no sweep confirmed

            records.append(
                {
                    "sweep_id": f"swp_{symbol}_{lvl['level_id']}_{i}",
                    "symbol": symbol,
                    "timeframe": config.timeframe,
                    "direction": direction,
                    "level_id": lvl["level_id"],
                    "level_type": lvl["type"],
                    "level_price": level_price,
                    "penetration_bar_open_ts": open_ts[i],
                    "penetration_price": float(high_arr[i]) if is_high_type else float(low_arr[i]),
                    "penetration_points": penetration_points,
                    "confirmation_ts": confirmation_ts,
                    "bars_to_reclaim": bars_to_reclaim,
                }
            )
            swept_level_ids.add(lvl["level_id"])
            if not config.allow_repeated_sweeps:
                break

    return pl.DataFrame(records, schema=SWEEP_SCHEMA) if records else _empty_sweeps()
