"""Fair Value Gap detection (3-bar, fully-completed-bar definition).

For consecutive completed bars 1, 2, 3 (bar_i is the i-th bar of the FVG, in
ascending time order):
  Bullish FVG: bar_1.high < bar_3.low   (gap between bar1 high and bar3 low)
  Bearish FVG: bar_1.low  > bar_3.high  (gap between bar3 high and bar1 low)

Anti-look-ahead invariant (tested explicitly): an FVG formed by bars at row
indices (i, i+1, i+2) cannot be known/confirmed before bar i+2 CLOSES. Its
`confirmation_ts` is therefore bar_3's bar_close_ts, and no code may treat the
FVG as existing at any timestamp earlier than that.

`annotate_touches` performs a forward scan over subsequent bars to fill in
diagnostic-only fields (first touch / midpoint touch / full fill). These fields
are for post-hoc analysis (e.g. "how quickly do FVGs typically fill") and MUST
NOT be used by live/causal signal or execution logic to decide whether a gap is
still tradeable as of a given bar -- that decision must independently re-derive
mitigation status using only bars up to and including the bar being processed
(see src/strategies/ict_silver_bullet/signals.py once implemented).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import polars as pl

Direction = Literal["bullish", "bearish"]


@dataclass(frozen=True)
class FvgConfig:
    timeframe: str
    min_points: float = 0.0
    min_bps: float = 0.0
    min_atr_multiple: float = 0.0
    max_age_bars: int | None = None
    entry_rule: Literal["proximal", "midpoint", "distal", "first_touch"] = "midpoint"
    full_mitigation_invalidates: bool = True
    partial_mitigation_invalidates: bool = False
    require_entry_within_window: bool = True


def detect_fvgs(df: pl.DataFrame, *, config: FvgConfig, calendar_window_col: str = "sb_window") -> pl.DataFrame:
    """Detect 3-bar FVGs in a single-symbol, single-timeframe, ascending-sorted
    bar frame (must already have `atr` and `sb_window`/`session_date_ny` columns
    from the ATR and sessions feature steps for size-filtering and metadata).
    Returns one row per detected FVG (before applying min-size filters -- those
    are applied here as a strict filter, recorded via `config`, not silently).
    """
    n = df.height
    if n < 3:
        return _empty_fvg_frame()

    high = df["high"].to_list()
    low = df["low"].to_list()
    open_ts = df["bar_open_ts"].to_list()
    close_ts = df["bar_close_ts"].to_list()
    atr = df["atr"].to_list() if "atr" in df.columns else [None] * n
    session_date = df["session_date_ny"].to_list() if "session_date_ny" in df.columns else [None] * n
    window = df[calendar_window_col].to_list() if calendar_window_col in df.columns else [None] * n
    symbol = df["symbol"][0] if "symbol" in df.columns and n > 0 else None
    timeframe = config.timeframe

    records: list[dict] = []
    for i in range(n - 2):
        b1_high, b1_low = high[i], low[i]
        b3_high, b3_low = high[i + 2], low[i + 2]

        direction: Direction | None = None
        gap_bottom = gap_top = None
        if b1_high < b3_low:
            direction = "bullish"
            gap_bottom, gap_top = b1_high, b3_low
        elif b1_low > b3_high:
            direction = "bearish"
            gap_bottom, gap_top = b3_high, b1_low

        if direction is None:
            continue

        size_points = gap_top - gap_bottom
        atr_at_confirmation = atr[i + 2]

        if size_points < config.min_points:
            continue
        midpoint_ref = (gap_top + gap_bottom) / 2
        size_bps = (size_points / midpoint_ref) * 10_000 if midpoint_ref else 0.0
        if size_bps < config.min_bps:
            continue
        if atr_at_confirmation and config.min_atr_multiple > 0:
            if size_points < config.min_atr_multiple * atr_at_confirmation:
                continue
        elif config.min_atr_multiple > 0 and not atr_at_confirmation:
            continue  # ATR not warmed up: cannot evaluate the filter, reject rather than guess

        midpoint = (gap_top + gap_bottom) / 2
        # proximal = the edge price re-touches FIRST on a retracement (nearer to
        # where price already traveled to); distal = the far edge (deeper fill).
        # Bullish FVG forms during an up-move -- price is above the gap at
        # confirmation and would retrace DOWN into it, touching the TOP first.
        # Bearish is the mirror: price retraces UP into the gap, touching the
        # BOTTOM first.
        proximal = gap_top if direction == "bullish" else gap_bottom
        distal = gap_bottom if direction == "bullish" else gap_top

        records.append(
            {
                "fvg_id": f"fvg_{symbol}_{timeframe}_{i}",
                "symbol": symbol,
                "timeframe": timeframe,
                "direction": direction,
                "bar1_open_ts": open_ts[i],
                "bar2_open_ts": open_ts[i + 1],
                "bar3_open_ts": open_ts[i + 2],
                "confirmation_ts": close_ts[i + 2],
                "gap_bottom": gap_bottom,
                "gap_top": gap_top,
                "midpoint": midpoint,
                "proximal": proximal,
                "distal": distal,
                "size_points": size_points,
                "size_bps": size_bps,
                "size_atr_multiple": (size_points / atr_at_confirmation) if atr_at_confirmation else None,
                "source_row_index": i,
                "session_date_ny": session_date[i + 2],
                "sb_window": window[i + 2],
                "age_bars_at_confirmation": 0,
            }
        )

    return pl.DataFrame(records) if records else _empty_fvg_frame()


def _empty_fvg_frame() -> pl.DataFrame:
    schema = {
        "fvg_id": pl.Utf8, "symbol": pl.Utf8, "timeframe": pl.Utf8, "direction": pl.Utf8,
        "bar1_open_ts": pl.Datetime("us", "UTC"), "bar2_open_ts": pl.Datetime("us", "UTC"),
        "bar3_open_ts": pl.Datetime("us", "UTC"), "confirmation_ts": pl.Datetime("us", "UTC"),
        "gap_bottom": pl.Float64, "gap_top": pl.Float64, "midpoint": pl.Float64,
        "proximal": pl.Float64, "distal": pl.Float64, "size_points": pl.Float64,
        "size_bps": pl.Float64, "size_atr_multiple": pl.Float64, "source_row_index": pl.Int64,
        "session_date_ny": pl.Date, "sb_window": pl.Utf8, "age_bars_at_confirmation": pl.Int64,
    }
    return pl.DataFrame(schema=schema)


def annotate_touches(fvg_df: pl.DataFrame, bars_df: pl.DataFrame) -> pl.DataFrame:
    """POST-HOC ONLY (see module docstring). Forward-scans bars after each FVG's
    confirmation to find first touch / midpoint touch / full-fill timestamps."""
    if fvg_df.is_empty():
        return fvg_df.with_columns(
            pl.lit(None, dtype=pl.Datetime("us", "UTC")).alias("first_touch_ts"),
            pl.lit(None, dtype=pl.Datetime("us", "UTC")).alias("midpoint_touch_ts"),
            pl.lit(None, dtype=pl.Datetime("us", "UTC")).alias("full_fill_ts"),
        )

    bar_open = bars_df["bar_open_ts"].to_list()
    bar_high = bars_df["high"].to_list()
    bar_low = bars_df["low"].to_list()

    first_touch, midpoint_touch, full_fill = [], [], []
    for row in fvg_df.iter_rows(named=True):
        direction = row["direction"]
        proximal, midpoint, distal = row["proximal"], row["midpoint"], row["distal"]
        start_idx = row["source_row_index"] + 3  # first bar strictly after confirmation
        ft = mt = ff = None
        for j in range(start_idx, len(bar_open)):
            h, l = bar_high[j], bar_low[j]
            touches_proximal = l <= proximal <= h if direction == "bullish" else l <= proximal <= h
            reaches_proximal = (l <= proximal) if direction == "bullish" else (h >= proximal)
            reaches_midpoint = (l <= midpoint) if direction == "bullish" else (h >= midpoint)
            reaches_distal = (l <= distal) if direction == "bullish" else (h >= distal)
            if ft is None and reaches_proximal:
                ft = bar_open[j]
            if mt is None and reaches_midpoint:
                mt = bar_open[j]
            if ff is None and reaches_distal:
                ff = bar_open[j]
            if ft is not None and mt is not None and ff is not None:
                break
        first_touch.append(ft)
        midpoint_touch.append(mt)
        full_fill.append(ff)

    return fvg_df.with_columns(
        pl.Series("first_touch_ts", first_touch, dtype=pl.Datetime("us", "UTC")),
        pl.Series("midpoint_touch_ts", midpoint_touch, dtype=pl.Datetime("us", "UTC")),
        pl.Series("full_fill_ts", full_fill, dtype=pl.Datetime("us", "UTC")),
    )
