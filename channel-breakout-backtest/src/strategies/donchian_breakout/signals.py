"""Vectorized Donchian breakout signal generation.

Causality: the channel for bar t is built from the `lookback` bars strictly
*before* t (a `.shift(1)` after the rolling window), so a breakout detected at
t never peeks at t's own extreme relative to the channel. A detected breakout is
confirmed at t's close; the resulting intent's `submission_ts` is t's
`bar_close_ts`, so the engine fills it at the next bar's open -- no look-ahead.

Everything downstream (sizing, fills, exits, portfolio) is the shared engine; a
"signal" row here is only a proposal and may still be rejected by the simulator
(e.g. invalid stop geometry after the real fill, or a position already open).
"""

from __future__ import annotations

import polars as pl

from src.features.atr import wilder_atr
from src.strategies.donchian_breakout.config import DonchianBreakoutConfig


def _breakout_price_expr(kind: str, *, side: str) -> pl.Expr:
    """The price of the just-closed bar compared against the channel to confirm
    a breakout. Long uses the up-side price, short the down-side price."""
    if kind == "close":
        return pl.col("close")
    if kind == "typical":
        return (pl.col("high") + pl.col("low") + pl.col("close")) / 3.0
    if kind == "wick":
        return pl.col("high") if side == "long" else pl.col("low")
    raise ValueError(f"Unknown breakout_price kind: {kind!r}")


def generate_signals(
    bars: pl.DataFrame, *, config: DonchianBreakoutConfig, config_id: str
) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Returns (signals, rejected). `bars` is a single symbol/timeframe frame,
    sorted ascending by bar_open_ts, regular-session only (as produced by
    src/data/aggregation.aggregate_bars)."""
    if bars.is_empty():
        return bars.clear(), bars.clear()

    lookback = config.channel_lookback
    df = wilder_atr(bars.sort("bar_open_ts"), period=config.atr_period)

    # Channel over the `lookback` bars strictly before the current bar.
    df = df.with_columns(
        pl.col("high").rolling_max(window_size=lookback).shift(1).alias("channel_high"),
        pl.col("low").rolling_min(window_size=lookback).shift(1).alias("channel_low"),
    )
    df = df.with_columns(
        ((pl.col("channel_high") + pl.col("channel_low")) / 2.0).alias("channel_mid")
    )

    # Optional trend filter: SMA over the last `ma_period` bars (inclusive).
    ma_period = config.trend_filter_ma_period
    if ma_period is not None:
        df = df.with_columns(pl.col("close").rolling_mean(window_size=ma_period).alias("trend_sma"))
    else:
        df = df.with_columns(pl.lit(None, dtype=pl.Float64).alias("trend_sma"))

    # Session close timestamp (eod cutoff) and last-bar-of-session flag.
    session_close = df.group_by("session_date_ny").agg(
        pl.col("bar_close_ts").max().alias("session_close_ts")
    )
    df = df.join(session_close, on="session_date_ny", how="left")
    df = df.with_columns(
        (pl.col("session_date_ny").shift(-1) != pl.col("session_date_ny"))
        .fill_null(True)
        .alias("is_last_bar_of_session")
    )

    long_price = _breakout_price_expr(config.breakout_price, side="long")
    short_price = _breakout_price_expr(config.breakout_price, side="short")

    trend_ok_long = pl.lit(True) if ma_period is None else (pl.col("close") > pl.col("trend_sma"))
    trend_ok_short = pl.lit(True) if ma_period is None else (pl.col("close") < pl.col("trend_sma"))

    long_sig = (
        (long_price > pl.col("channel_high"))
        & pl.col("channel_high").is_not_null()
        & trend_ok_long
    )
    short_sig = (
        (short_price < pl.col("channel_low"))
        & pl.col("channel_low").is_not_null()
        & trend_ok_short
    )
    if not config.allow_short:
        short_sig = pl.lit(False)

    df = df.with_columns(
        pl.when(long_sig).then(pl.lit("long"))
        .when(short_sig).then(pl.lit("short"))
        .otherwise(pl.lit(None))
        .alias("direction")
    )

    # Keep only bars that fired a signal AND leave room to enter intraday.
    sig = df.filter(pl.col("direction").is_not_null() & ~pl.col("is_last_bar_of_session"))
    if sig.is_empty():
        return bars.clear(), bars.clear()

    # Entry reference = signal-bar close (actual fill is next bar open; the
    # simulator re-validates stop geometry against the real fill).
    entry_ref = pl.col("close")

    k = config.stop_atr_multiple  # None for channel_mid
    if k is not None:
        stop_px = (
            pl.when(pl.col("direction") == "long")
            .then(entry_ref - k * pl.col("atr"))
            .otherwise(entry_ref + k * pl.col("atr"))
        )
    else:
        stop_px = pl.col("channel_mid")

    r = config.target_r_multiple  # None for "none"
    risk = (entry_ref - stop_px).abs()
    if r is not None:
        target_px = (
            pl.when(pl.col("direction") == "long")
            .then(entry_ref + r * risk)
            .otherwise(entry_ref - r * risk)
        )
    else:
        target_px = pl.lit(None, dtype=pl.Float64)

    sig = sig.with_columns(
        stop_px.alias("stop_price"),
        target_px.alias("target_price"),
        entry_ref.alias("entry_ref_price"),
    )

    # Require a usable stop (positive risk, correct side) and defined ATR when needed.
    geom_ok = (
        pl.when(pl.col("direction") == "long")
        .then(pl.col("stop_price") < pl.col("entry_ref_price"))
        .otherwise(pl.col("stop_price") > pl.col("entry_ref_price"))
    )
    needs_atr = k is not None
    sig = sig.filter(geom_ok & pl.col("stop_price").is_not_null())
    if needs_atr:
        sig = sig.filter(pl.col("atr").is_not_null())
    if sig.is_empty():
        return bars.clear(), bars.clear()

    max_holding = config.max_holding_bars
    signals = sig.select(
        (
            pl.lit(config.symbol) + "_" + pl.lit(config.timeframe) + "_"
            + pl.col("bar_open_ts").dt.epoch("s").cast(pl.Utf8)
        ).alias("signal_id"),
        pl.lit(config_id).alias("config_id"),
        pl.lit(config.symbol).alias("symbol"),
        pl.col("direction"),
        pl.col("bar_close_ts").alias("submission_ts"),
        pl.col("entry_ref_price"),
        pl.col("stop_price"),
        pl.col("target_price"),
        pl.col("session_close_ts").alias("time_exit_ts"),
        pl.lit(max_holding, dtype=pl.Int64).alias("max_holding_bars"),
        pl.col("session_date_ny").alias("session_date"),
    )

    rejected = bars.clear()  # the simulator records fill-time rejections; none pre-filtered here
    return signals, rejected
