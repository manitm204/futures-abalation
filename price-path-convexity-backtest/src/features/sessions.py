"""Session and Silver Bullet window labeling.

Silver Bullet windows (per project convention, confirmed with the user before
implementation): three predefined, non-optimized categorical windows, all
America/New_York, half-open [start, end):
  - london: 03:00-04:00
  - ny_am:  10:00-11:00
  - ny_pm:  14:00-15:00

These are recorded on every bar/setup/signal so later analysis can compare
window profitability -- they are NOT continuously optimized minute-by-minute.
"""

from __future__ import annotations

import polars as pl

from src.utils.config_models import DEFAULT_SILVER_BULLET_WINDOWS, SilverBulletWindow


def label_windows(
    df: pl.DataFrame,
    windows: tuple[SilverBulletWindow, ...] = DEFAULT_SILVER_BULLET_WINDOWS,
    *,
    ts_col: str = "bar_open_ts_ny",
) -> pl.DataFrame:
    """Add an `sb_window` column (Utf8, null if the bar's open falls in no window).

    A bar belongs to a window based on its OPEN time only (half-open [start,end)),
    consistent with the bar-open-labeled convention used throughout the framework.
    If windows overlap (not the case for the defaults) the first match wins.
    """
    expr = pl.lit(None, dtype=pl.Utf8)
    for w in reversed(windows):
        t = pl.col(ts_col).dt.time()
        in_window = (t >= w.start) & (t < w.end)
        expr = pl.when(in_window).then(pl.lit(w.name)).otherwise(expr)
    return df.with_columns(expr.alias("sb_window"))


def label_regular_session(df: pl.DataFrame) -> pl.DataFrame:
    """Pass-through helper: `is_regular_session` is already set by normalization;
    this exists so strategy code has one place to reference session filters."""
    return df
