"""Performance metrics computed from a closed-trade list and a daily equity curve.

Sharpe/Sortino are computed from a DAILY return series (resampled from the
equity curve), not from per-trade returns -- annualizing per-trade returns
directly conflates trade frequency with volatility and is a known way to get
a badly wrong Sharpe. Annualization factor and risk-free rate are explicit,
documented parameters, not silent defaults buried in a formula.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Trade

TRADING_DAYS_PER_YEAR = 252


@dataclass
class Metrics:
    n_signals: int | None
    n_trades: int
    fill_rate: float | None
    rejection_rate: float | None
    n_long: int
    n_short: int
    gross_pnl: float
    net_pnl: float
    total_return_pct: float
    annualized_return_pct: float | None
    sharpe_ratio: float | None
    sortino_ratio: float | None
    max_drawdown_pct: float
    calmar_ratio: float | None
    win_rate: float
    loss_rate: float
    avg_win: float | None
    avg_loss: float | None
    payoff_ratio: float | None
    avg_realized_r: float | None
    median_realized_r: float | None
    profit_factor: float | None
    expectancy_per_trade: float | None
    exposure_pct: float | None
    avg_holding_bars: float | None
    commission_total: float
    slippage_cost_total: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    intrabar_ambiguous_count: int
    by_window: dict = field(default_factory=dict)
    by_symbol: dict = field(default_factory=dict)
    by_direction: dict = field(default_factory=dict)
    by_exit_reason: dict = field(default_factory=dict)


def _daily_returns(equity_curve: list[EquityPoint]) -> np.ndarray:
    if len(equity_curve) < 2:
        return np.array([])
    df = pl.DataFrame({"ts": [p.ts for p in equity_curve], "equity": [p.equity for p in equity_curve]})
    df = df.with_columns(pl.col("ts").dt.date().alias("d")).group_by("d", maintain_order=True).agg(
        pl.col("equity").last()
    ).sort("d")
    equities = df["equity"].to_numpy()
    if len(equities) < 2:
        return np.array([])
    return np.diff(equities) / equities[:-1]


def _max_drawdown(equity_curve: list[EquityPoint]) -> float:
    if not equity_curve:
        return 0.0
    equities = np.array([p.equity for p in equity_curve])
    running_max = np.maximum.accumulate(equities)
    drawdowns = (equities - running_max) / running_max
    return float(drawdowns.min()) if len(drawdowns) else 0.0


def _consecutive(flags: list[bool]) -> int:
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


def compute_metrics(
    trades: list[Trade],
    equity_curve: list[EquityPoint],
    *,
    starting_equity: float,
    n_signals: int | None = None,
    n_rejections: int | None = None,
    risk_free_rate_annual: float = 0.0,
) -> Metrics:
    n_trades = len(trades)
    wins = [t for t in trades if (t.realized_pnl or 0) > 0]
    losses = [t for t in trades if (t.realized_pnl or 0) < 0]

    gross_pnl = sum((t.realized_pnl or 0) + t.commission_total for t in trades)
    net_pnl = sum((t.realized_pnl or 0) for t in trades)
    commission_total = sum(t.commission_total for t in trades)
    slippage_total = sum(t.slippage_cost_total for t in trades)

    final_equity = equity_curve[-1].equity if equity_curve else starting_equity + net_pnl
    total_return_pct = (final_equity - starting_equity) / starting_equity if starting_equity else 0.0

    daily_rets = _daily_returns(equity_curve)
    sharpe = sortino = annualized_return = None
    if len(daily_rets) > 1:
        mean_daily_rf = risk_free_rate_annual / TRADING_DAYS_PER_YEAR
        excess = daily_rets - mean_daily_rf
        std = excess.std(ddof=1)
        sharpe = float((excess.mean() / std) * math.sqrt(TRADING_DAYS_PER_YEAR)) if std > 0 else None
        downside = excess[excess < 0]
        downside_std = downside.std(ddof=1) if len(downside) > 1 else 0.0
        sortino = float((excess.mean() / downside_std) * math.sqrt(TRADING_DAYS_PER_YEAR)) if downside_std > 0 else None
        n_days = len(daily_rets) + 1
        years = n_days / TRADING_DAYS_PER_YEAR
        if years > 0 and (1 + total_return_pct) > 0:
            annualized_return = (1 + total_return_pct) ** (1 / years) - 1

    max_dd = _max_drawdown(equity_curve)
    calmar = (annualized_return / abs(max_dd)) if (annualized_return is not None and max_dd < 0) else None

    win_rate = len(wins) / n_trades if n_trades else 0.0
    loss_rate = len(losses) / n_trades if n_trades else 0.0
    avg_win = sum(t.realized_pnl for t in wins) / len(wins) if wins else None
    avg_loss = sum(t.realized_pnl for t in losses) / len(losses) if losses else None
    payoff_ratio = (avg_win / abs(avg_loss)) if (avg_win is not None and avg_loss not in (None, 0)) else None

    r_values = [t.realized_r for t in trades if t.realized_r is not None]
    avg_r = float(np.mean(r_values)) if r_values else None
    median_r = float(np.median(r_values)) if r_values else None

    gross_profit = sum(t.realized_pnl for t in wins) if wins else 0.0
    gross_loss = abs(sum(t.realized_pnl for t in losses)) if losses else 0.0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else None

    expectancy = net_pnl / n_trades if n_trades else None

    holding_bars = [t.holding_bars for t in trades if t.holding_bars is not None]
    avg_holding = float(np.mean(holding_bars)) if holding_bars else None

    win_flags = [(t.realized_pnl or 0) > 0 for t in trades]
    loss_flags = [(t.realized_pnl or 0) < 0 for t in trades]

    def _group(keyfn) -> dict:
        groups: dict = {}
        for t in trades:
            k = keyfn(t)
            groups.setdefault(k, []).append(t)
        out = {}
        for k, ts in groups.items():
            pnl = sum(x.realized_pnl or 0 for x in ts)
            out[k] = {"n_trades": len(ts), "net_pnl": pnl, "win_rate": sum(1 for x in ts if (x.realized_pnl or 0) > 0) / len(ts)}
        return out

    return Metrics(
        n_signals=n_signals,
        n_trades=n_trades,
        fill_rate=(n_trades / n_signals) if n_signals else None,
        rejection_rate=(n_rejections / n_signals) if (n_signals and n_rejections is not None) else None,
        n_long=sum(1 for t in trades if t.side == "long"),
        n_short=sum(1 for t in trades if t.side == "short"),
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        total_return_pct=total_return_pct,
        annualized_return_pct=annualized_return,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        max_drawdown_pct=max_dd,
        calmar_ratio=calmar,
        win_rate=win_rate,
        loss_rate=loss_rate,
        avg_win=avg_win,
        avg_loss=avg_loss,
        payoff_ratio=payoff_ratio,
        avg_realized_r=avg_r,
        median_realized_r=median_r,
        profit_factor=profit_factor,
        expectancy_per_trade=expectancy,
        exposure_pct=None,  # requires bar-level position tracking; left to analysis layer
        avg_holding_bars=avg_holding,
        commission_total=commission_total,
        slippage_cost_total=slippage_total,
        max_consecutive_wins=_consecutive(win_flags),
        max_consecutive_losses=_consecutive(loss_flags),
        intrabar_ambiguous_count=sum(1 for t in trades if t.intrabar_ambiguous),
        by_window=_group(lambda t: t.window),
        by_symbol=_group(lambda t: t.symbol),
        by_direction=_group(lambda t: t.side),
        by_exit_reason=_group(lambda t: t.exit_reason.value if t.exit_reason else None),
    )
