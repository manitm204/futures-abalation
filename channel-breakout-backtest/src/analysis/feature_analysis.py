"""Feature-value distribution comparison between winning and losing trades.

Operates on a trades table joined with the feature values recorded at signal
time (e.g. fvg_size_atr_multiple, atr, sb_window) -- this module does not
recompute features, it only summarizes columns already present.
"""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class FeatureComparison:
    feature: str
    n_winners: int
    n_losers: int
    winner_median: float
    loser_median: float
    winner_mean: float
    loser_mean: float


def compare_winners_vs_losers(trades: pl.DataFrame, *, feature_col: str, pnl_col: str = "realized_pnl") -> FeatureComparison | None:
    winners = trades.filter(pl.col(pnl_col) > 0).drop_nulls(feature_col)
    losers = trades.filter(pl.col(pnl_col) <= 0).drop_nulls(feature_col)
    if winners.is_empty() or losers.is_empty():
        return None
    return FeatureComparison(
        feature=feature_col,
        n_winners=winners.height, n_losers=losers.height,
        winner_median=float(winners[feature_col].median()), loser_median=float(losers[feature_col].median()),
        winner_mean=float(winners[feature_col].mean()), loser_mean=float(losers[feature_col].mean()),
    )


def window_performance_breakdown(trades: pl.DataFrame, *, window_col: str = "window", pnl_col: str = "realized_pnl") -> pl.DataFrame:
    return (
        trades.group_by(window_col)
        .agg(
            pl.len().alias("n_trades"),
            pl.col(pnl_col).sum().alias("net_pnl"),
            (pl.col(pnl_col) > 0).mean().alias("win_rate"),
        )
        .sort(window_col)
    )
