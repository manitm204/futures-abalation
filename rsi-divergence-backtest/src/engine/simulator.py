"""Single-symbol event-driven backtest loop.

Strategy-agnostic: consumes a list of `TradeIntent` (produced by a strategy's
signal/order-creation logic -- e.g. src/strategies/ict_silver_bullet -- once
that layer resolves stop/target prices and entry rules) plus the symbol's bar
series, and produces filled trades, rejections, and an equity curve. Nothing
in this module knows about FVGs, sweeps, or any ICT concept; new strategies
plug in by producing TradeIntents, not by modifying this file.

Chronology: intents are processed in ascending `submission_ts` order. An
intent's entry order can only use bars with `bar_open_ts >= submission_ts`
(the first tradable event at/after the signal was confirmed) -- never earlier.
Non-overlap is enforced by Portfolio.open_position raising if a position is
already open; the simulator catches that as a rejection rather than a crash.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from datetime import datetime

import polars as pl

from src.engine.events import ExitReason, Fill, Order, OrderPurpose, OrderStatus, OrderType, Side, Trade
from src.engine.fills import BarWindow, _apply_slippage, _commission, resolve_exit, simulate_entry_fill
from src.engine.portfolio import Portfolio
from src.engine.sizing import compute_position_size
from src.utils.config_models import ExecutionConfig


@dataclass(frozen=True)
class TradeIntent:
    signal_id: str
    config_id: str
    symbol: str
    side: Side
    submission_ts: datetime
    stop_price: float
    entry_order_type: OrderType = OrderType.MARKET
    entry_limit_price: float | None = None
    entry_expiration_ts: datetime | None = None
    target_price: float | None = None
    time_exit_ts: datetime | None = None
    time_exit_reason: ExitReason = ExitReason.SESSION_EXIT
    window: str | None = None
    max_holding_bars: int | None = None


@dataclass
class Rejection:
    signal_id: str
    symbol: str
    reason: str
    ts: datetime


@dataclass
class BacktestResult:
    trades: list[Trade] = field(default_factory=list)
    rejections: list[Rejection] = field(default_factory=list)
    portfolio: Portfolio | None = None


def _bar_window_from_df(df: pl.DataFrame) -> BarWindow:
    ext_col = "is_extended_hours" if "is_extended_hours" in df.columns else None
    return BarWindow(
        open_ts=df["bar_open_ts"].to_list(),
        close_ts=df["bar_close_ts"].to_list(),
        open=df["open"].to_list(),
        high=df["high"].to_list(),
        low=df["low"].to_list(),
        close=df["close"].to_list(),
        is_extended_hours=df[ext_col].to_list() if ext_col else [False] * df.height,
    )


def run_backtest_single_symbol(
    bars_df: pl.DataFrame,
    intents: list[TradeIntent],
    *,
    config: ExecutionConfig,
    starting_equity: float | None = None,
) -> BacktestResult:
    symbol_values = bars_df["symbol"].unique().to_list() if "symbol" in bars_df.columns else []
    if len(symbol_values) > 1:
        raise ValueError(f"run_backtest_single_symbol expects one symbol, got {symbol_values}")

    equity = starting_equity if starting_equity is not None else config.starting_equity
    portfolio = Portfolio(starting_equity=equity)
    bw = _bar_window_from_df(bars_df)
    open_ts_list = bw.open_ts
    result = BacktestResult(portfolio=portfolio)

    if open_ts_list:
        portfolio.mark_to_market(open_ts_list[0], {})

    order_seq = 0
    # Each intent is fully resolved (entry through exit) before the next intent is
    # considered, since this simulator processes one symbol's non-overlapping
    # positions sequentially rather than stepping bar-by-bar across concurrent
    # positions. That means `portfolio.has_open_position` reflects LOOP ORDER, not
    # real time -- by the time intent2 is examined, intent1's position has already
    # been closed in the dict even if intent1's real exit timestamp is AFTER
    # intent2's submission_ts. Overlap must therefore be judged against the actual
    # exit timestamp of the last-processed position for this symbol, not dict
    # presence.
    busy_until_by_symbol: dict[str, datetime] = {}

    for intent in sorted(intents, key=lambda x: x.submission_ts):
        busy_until = busy_until_by_symbol.get(intent.symbol)
        if busy_until is not None and intent.submission_ts < busy_until:
            result.rejections.append(
                Rejection(signal_id=intent.signal_id, symbol=intent.symbol, reason="position_already_open", ts=intent.submission_ts)
            )
            continue

        start_idx = bisect.bisect_left(open_ts_list, intent.submission_ts)
        if start_idx >= len(open_ts_list):
            result.rejections.append(
                Rejection(signal_id=intent.signal_id, symbol=intent.symbol, reason="no_bars_after_submission", ts=intent.submission_ts)
            )
            continue

        # Provisional entry price estimate for sizing purposes: next bar's open
        # (market) or the limit price (limit). Actual fill may differ slightly
        # due to slippage; sizing uses the intended price, consistent with
        # "size before you know the exact fill" real-world constraint.
        provisional_price = intent.entry_limit_price if intent.entry_order_type == OrderType.LIMIT else bw.open[start_idx]
        sizing = compute_position_size(
            equity=portfolio.current_equity, entry_price=provisional_price, stop_price=intent.stop_price, config=config
        )
        if not sizing.accepted:
            result.rejections.append(
                Rejection(signal_id=intent.signal_id, symbol=intent.symbol, reason=f"sizing_rejected:{sizing.rejection_reason}", ts=intent.submission_ts)
            )
            continue

        order_seq += 1
        entry_order = Order(
            order_id=f"entry_{intent.signal_id}_{order_seq}",
            symbol=intent.symbol, side=intent.side, purpose=OrderPurpose.ENTRY,
            order_type=intent.entry_order_type, quantity=sizing.quantity,
            submitted_ts=intent.submission_ts, limit_price=intent.entry_limit_price,
            expiration_ts=intent.entry_expiration_ts,
        )
        entry_fill, entry_order = simulate_entry_fill(entry_order, bw, start_idx, config=config)
        if entry_fill is None:
            result.rejections.append(
                Rejection(signal_id=intent.signal_id, symbol=intent.symbol, reason="entry_not_filled_expired", ts=intent.submission_ts)
            )
            continue

        stop_geom_ok = (intent.stop_price < entry_fill.fill_price) if intent.side == "long" else (intent.stop_price > entry_fill.fill_price)
        if not stop_geom_ok:
            result.rejections.append(
                Rejection(signal_id=intent.signal_id, symbol=intent.symbol, reason="invalid_stop_geometry", ts=intent.submission_ts)
            )
            continue

        trade = Trade(
            trade_id=f"trade_{intent.signal_id}", config_id=intent.config_id, symbol=intent.symbol,
            side=intent.side, entry_order_id=entry_order.order_id, entry_fill=entry_fill,
            quantity=entry_fill.quantity, stop_price=intent.stop_price, target_price=intent.target_price,
            entry_signal_id=intent.signal_id, window=intent.window,
        )
        portfolio.open_position(trade)

        entry_idx = bisect.bisect_left(open_ts_list, entry_fill.fill_ts)
        exit_search_start = entry_idx + 1

        effective_time_exit_ts = intent.time_exit_ts
        if intent.max_holding_bars is not None:
            max_idx = min(entry_idx + intent.max_holding_bars, len(open_ts_list) - 1)
            holding_cutoff = open_ts_list[max_idx]
            if effective_time_exit_ts is None or holding_cutoff < effective_time_exit_ts:
                effective_time_exit_ts = holding_cutoff

        exit_result = None
        if exit_search_start < len(open_ts_list):
            exit_result = resolve_exit(
                bw, exit_search_start, side=intent.side, quantity=entry_fill.quantity,
                stop_price=intent.stop_price, target_price=intent.target_price,
                time_exit_ts=effective_time_exit_ts, time_exit_reason=intent.time_exit_reason,
                config=config, order_id=f"exit_{intent.signal_id}_{order_seq}", symbol=intent.symbol,
            )

        if exit_result is None:
            # Forced close at the last available bar -- data ends with position open.
            last_idx = len(open_ts_list) - 1
            exit_action = "sell" if intent.side == "long" else "buy"
            px = _apply_slippage(
                bw.close[last_idx], side=intent.side, action=exit_action, bps=config.slippage_bps_market,
                extended_hours=bw.is_extended_hours[last_idx], config=config,
            )
            exit_fill = Fill(
                order_id=f"exit_{intent.signal_id}_{order_seq}_forced", symbol=intent.symbol, side=intent.side,
                quantity=entry_fill.quantity, fill_price=px, fill_ts=bw.close_ts[last_idx],
                commission=_commission(entry_fill.quantity, config), slippage_points=0.0,
                bar_open_ts=bw.open_ts[last_idx],
            )
            trade.holding_bars = last_idx - entry_idx
            portfolio.close_position(intent.symbol, exit_fill, ExitReason.SESSION_EXIT, config)
            busy_until_by_symbol[intent.symbol] = exit_fill.fill_ts
            portfolio.mark_to_market(exit_fill.fill_ts, {})
        else:
            trade.intrabar_ambiguous = exit_result.intrabar_ambiguous
            trade.holding_bars = exit_result.exit_idx - entry_idx
            portfolio.close_position(intent.symbol, exit_result.fill, exit_result.reason, config)
            busy_until_by_symbol[intent.symbol] = exit_result.fill.fill_ts
            portfolio.mark_to_market(exit_result.fill.fill_ts, {})

        result.trades.append(trade)

    return result
