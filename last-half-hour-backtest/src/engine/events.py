"""Core typed events: orders, fills, positions, trades.

These are the vocabulary the rest of the engine (fills.py, portfolio.py,
simulator.py) is built from. Kept as plain dataclasses (not pydantic) since
they're created at high frequency during simulation and mutated in place
(order status transitions), unlike the frozen config models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal

Side = Literal["long", "short"]


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderPurpose(str, Enum):
    ENTRY = "entry"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    TIME_EXIT = "time_exit"
    WINDOW_EXIT = "window_exit"
    SESSION_EXIT = "session_exit"


class OrderStatus(str, Enum):
    PENDING = "pending"
    FILLED = "filled"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ExitReason(str, Enum):
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    TIME_EXIT = "time_exit"
    WINDOW_EXIT = "window_exit"
    SESSION_EXIT = "session_exit"


@dataclass
class Order:
    order_id: str
    symbol: str
    side: Side
    purpose: OrderPurpose
    order_type: OrderType
    quantity: int
    submitted_ts: datetime
    limit_price: float | None = None
    stop_price: float | None = None
    expiration_ts: datetime | None = None
    status: OrderStatus = OrderStatus.PENDING
    rejection_reason: str | None = None
    linked_trade_id: str | None = None


@dataclass
class Fill:
    order_id: str
    symbol: str
    side: Side
    quantity: int
    fill_price: float
    fill_ts: datetime
    commission: float
    slippage_points: float
    bar_open_ts: datetime
    intrabar_ambiguous: bool = False


@dataclass
class Trade:
    trade_id: str
    config_id: str
    symbol: str
    side: Side
    entry_order_id: str
    entry_fill: Fill
    quantity: int
    stop_price: float
    target_price: float | None
    entry_signal_id: str | None = None
    exit_fill: Fill | None = None
    exit_reason: ExitReason | None = None
    realized_pnl: float | None = None
    realized_r: float | None = None
    commission_total: float = 0.0
    slippage_cost_total: float = 0.0
    intrabar_ambiguous: bool = False
    window: str | None = None
    holding_bars: int | None = None

    @property
    def is_open(self) -> bool:
        return self.exit_fill is None


@dataclass
class EquityPoint:
    ts: datetime
    cash: float
    position_value: float
    equity: float
