"""Cash/equity/position bookkeeping.

Enforces: one open position per symbol (no pyramiding, no overlapping trades)
by construction -- `open_position` raises if a position is already open for
that symbol, rather than silently allowing a second one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from src.engine.events import EquityPoint, Fill, Side, Trade


@dataclass
class OpenPosition:
    trade: Trade
    symbol: str
    side: Side
    quantity: int
    entry_price: float


class Portfolio:
    def __init__(self, starting_equity: float) -> None:
        self.cash = starting_equity
        self.starting_equity = starting_equity
        self._open_positions: dict[str, OpenPosition] = {}
        self.closed_trades: list[Trade] = []
        self.equity_curve: list[EquityPoint] = []

    def has_open_position(self, symbol: str) -> bool:
        return symbol in self._open_positions

    def open_position(self, trade: Trade) -> None:
        if trade.symbol in self._open_positions:
            raise ValueError(
                f"Attempted to open a second position in {trade.symbol} while one is "
                "already open -- non-overlapping-position invariant violated."
            )
        fill = trade.entry_fill
        notional = fill.fill_price * fill.quantity
        cost = fill.commission
        if trade.side == "long":
            self.cash -= notional + cost
        else:
            # short: receive proceeds from the sale, commission still a cost
            self.cash += notional - cost
        self._open_positions[trade.symbol] = OpenPosition(
            trade=trade, symbol=trade.symbol, side=trade.side, quantity=fill.quantity, entry_price=fill.fill_price
        )

    def close_position(self, symbol: str, exit_fill: Fill, exit_reason, config) -> Trade:
        pos = self._open_positions.pop(symbol)
        trade = pos.trade
        trade.exit_fill = exit_fill
        trade.exit_reason = exit_reason

        entry_notional = pos.entry_price * pos.quantity
        exit_notional = exit_fill.fill_price * exit_fill.quantity

        if pos.side == "long":
            self.cash += exit_notional - exit_fill.commission
            gross_pnl = exit_notional - entry_notional
        else:
            self.cash -= exit_notional + exit_fill.commission
            gross_pnl = entry_notional - exit_notional

        total_commission = trade.entry_fill.commission + exit_fill.commission
        trade.commission_total = total_commission
        trade.slippage_cost_total = (
            trade.entry_fill.slippage_points * trade.entry_fill.quantity
            + exit_fill.slippage_points * exit_fill.quantity
        )
        trade.realized_pnl = gross_pnl - total_commission
        stop_distance = abs(pos.entry_price - trade.stop_price)
        trade.realized_r = trade.realized_pnl / (stop_distance * pos.quantity) if stop_distance > 0 else None

        self.closed_trades.append(trade)
        return trade

    def mark_to_market(self, ts: datetime, prices: dict[str, float]) -> EquityPoint:
        position_value = 0.0
        for sym, pos in self._open_positions.items():
            px = prices.get(sym, pos.entry_price)
            if pos.side == "long":
                position_value += px * pos.quantity
            else:
                # short position value contribution: unrealized P&L relative to entry
                position_value += (pos.entry_price - px) * pos.quantity + pos.entry_price * pos.quantity

        equity = self.cash + position_value if self._open_positions else self.cash
        point = EquityPoint(ts=ts, cash=self.cash, position_value=position_value, equity=equity)
        self.equity_curve.append(point)
        return point

    @property
    def current_equity(self) -> float:
        return self.equity_curve[-1].equity if self.equity_curve else self.cash
