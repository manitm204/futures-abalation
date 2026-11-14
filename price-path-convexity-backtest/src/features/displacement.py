"""Displacement rules.

Each rule is independently enabled, configured, and recorded as its own column
-- per spec, these are never combined into an undocumented composite score.
All rules are causal: they only use the bar(s) they're evaluated on and prior
bars, never future bars.
"""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class DisplacementConfig:
    enable_true_range_atr: bool = True
    true_range_atr_threshold: float = 1.5

    enable_body_atr: bool = True
    body_atr_threshold: float = 1.0

    enable_run_body_sum_atr: bool = False
    run_body_sum_atr_threshold: float = 2.0
    run_lookback_bars: int = 3

    enable_close_location: bool = False
    close_location_threshold: float = 0.7  # close within top/bottom X% of the bar's range

    enable_min_consecutive_directional: bool = False
    min_consecutive_directional_bars: int = 2

    enable_volume_confirmation: bool = False
    volume_multiple_of_avg: float = 1.5
    volume_avg_lookback_bars: int = 20


def compute_displacement_flags(df: pl.DataFrame, *, config: DisplacementConfig, atr_col: str = "atr") -> pl.DataFrame:
    """Adds one boolean column per ENABLED rule (disabled rules get an all-null
    column so downstream code can tell "not evaluated" apart from "evaluated,
    false"), plus the raw metrics each rule is based on.
    """
    body = (pl.col("close") - pl.col("open"))
    true_range = pl.col("high") - pl.col("low")  # intra-bar range; ATR-relative TR already exists as a feature
    direction = pl.when(body > 0).then(1).when(body < 0).then(-1).otherwise(0)

    out = df.with_columns(
        body.alias("_body"),
        true_range.alias("_bar_range"),
        direction.alias("_direction"),
    )

    if config.enable_true_range_atr:
        out = out.with_columns(
            (pl.col("_bar_range") / pl.col(atr_col)).alias("tr_atr_ratio"),
        ).with_columns(
            (pl.col("tr_atr_ratio") >= config.true_range_atr_threshold).alias("displacement_true_range_atr")
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_true_range_atr"))

    if config.enable_body_atr:
        out = out.with_columns(
            (pl.col("_body").abs() / pl.col(atr_col)).alias("body_atr_ratio"),
        ).with_columns(
            (pl.col("body_atr_ratio") >= config.body_atr_threshold).alias("displacement_body_atr")
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_body_atr"))

    if config.enable_run_body_sum_atr:
        n = config.run_lookback_bars
        signed_body = pl.col("_body")
        run_sum = signed_body.rolling_sum(window_size=n)
        out = out.with_columns((run_sum.abs() / pl.col(atr_col)).alias("run_body_sum_atr_ratio")).with_columns(
            (pl.col("run_body_sum_atr_ratio") >= config.run_body_sum_atr_threshold).alias(
                "displacement_run_body_sum_atr"
            )
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_run_body_sum_atr"))

    if config.enable_close_location:
        rng = pl.col("_bar_range")
        close_loc_up = pl.when(rng > 0).then((pl.col("close") - pl.col("low")) / rng).otherwise(None)
        out = out.with_columns(close_loc_up.alias("close_location")).with_columns(
            (
                (pl.col("close_location") >= config.close_location_threshold)
                | (pl.col("close_location") <= (1 - config.close_location_threshold))
            ).alias("displacement_close_location")
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_close_location"))

    if config.enable_min_consecutive_directional:
        d = out["_direction"].to_list()
        n_bars = len(d)
        run_len = [0] * n_bars
        for i in range(n_bars):
            if i == 0 or d[i] == 0 or d[i] != d[i - 1]:
                run_len[i] = 1 if d[i] != 0 else 0
            else:
                run_len[i] = run_len[i - 1] + 1
        flag = [rl >= config.min_consecutive_directional_bars for rl in run_len]
        out = out.with_columns(
            pl.Series("consecutive_directional_bars", run_len, dtype=pl.Int64),
            pl.Series("displacement_min_consecutive_directional", flag, dtype=pl.Boolean),
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_min_consecutive_directional"))

    if config.enable_volume_confirmation:
        avg_vol = pl.col("volume").rolling_mean(window_size=config.volume_avg_lookback_bars).shift(1)
        out = out.with_columns((pl.col("volume") / avg_vol).alias("volume_ratio_to_avg")).with_columns(
            (pl.col("volume_ratio_to_avg") >= config.volume_multiple_of_avg).alias("displacement_volume_confirmation")
        )
    else:
        out = out.with_columns(pl.lit(None, dtype=pl.Boolean).alias("displacement_volume_confirmation"))

    return out.drop(["_body", "_bar_range", "_direction"])
