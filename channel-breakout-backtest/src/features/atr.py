"""Causal Wilder ATR.

ATR_t is computable using only bars up to and including bar t (its own high/low/close
and the prior bar's close) -- no future information. Warm-up: the first `period` bars
have no ATR (null); ATR is first defined at the bar where `period` True Range values
have accumulated, seeded as their simple average (standard Wilder initialization),
then smoothed recursively:  ATR_t = ATR_{t-1} + (TR_t - ATR_{t-1}) / period.
"""

from __future__ import annotations

import polars as pl


def true_range(df: pl.DataFrame) -> pl.DataFrame:
    prev_close = pl.col("close").shift(1)
    # max_horizontal ignores nulls by default, which would silently fall back to
    # (high-low) for the first bar instead of leaving true_range undefined. The
    # first bar has no prior close, so its TR must be explicitly null, not guessed.
    tr = pl.when(prev_close.is_null()).then(None).otherwise(
        pl.max_horizontal(
            pl.col("high") - pl.col("low"),
            (pl.col("high") - prev_close).abs(),
            (pl.col("low") - prev_close).abs(),
        )
    )
    return df.with_columns(tr.alias("true_range"))


def wilder_atr(df: pl.DataFrame, *, period: int = 14) -> pl.DataFrame:
    """Add `atr` (Float64, null during warm-up) and `atr_warmup_complete` (Boolean)
    columns. `df` must be a single symbol/timeframe, sorted ascending by bar_open_ts.
    """
    if period < 1:
        raise ValueError(f"ATR period must be >= 1, got {period}")

    df = true_range(df)
    tr = df["true_range"].to_list()
    n = len(tr)
    atr: list[float | None] = [None] * n

    if n >= period:
        # First TR value (bar 0) has no prior close, so it is not a valid TR for
        # seeding; Wilder's seed uses the first `period` TR values starting from
        # bar index 1 (the first bar with a defined true range).
        first_valid = 1 if tr and tr[0] is None else 0
        seed_end = first_valid + period
        if seed_end <= n and all(v is not None for v in tr[first_valid:seed_end]):
            seed = sum(tr[first_valid:seed_end]) / period
            atr[seed_end - 1] = seed
            prev = seed
            for i in range(seed_end, n):
                prev = prev + (tr[i] - prev) / period
                atr[i] = prev

    warmup_complete = [v is not None for v in atr]
    return df.with_columns(
        pl.Series("atr", atr, dtype=pl.Float64),
        pl.Series("atr_warmup_complete", warmup_complete, dtype=pl.Boolean),
    )
