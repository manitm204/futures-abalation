"""Fill simulation mechanics.

Chronology rule enforced throughout: an order submitted at time T can only be
filled using bars whose bar_open_ts is strictly after the bar that produced the
signal at T (i.e. `start_idx` passed in must already point at the first bar
eligible to fill against -- callers are responsible for that, and simulator.py
is the only caller). Nothing here peeks at bars before `start_idx`.

Same-bar stop/target collision: since OHLC bars don't reveal intrabar path,
when both are touched in one bar we cannot know which happened first. Default
resolution is `stop_first` (conservative). `discard_ambiguous` still returns a
result (using stop_first pricing) but flags `intrabar_ambiguous=True` so callers
can exclude the trade from headline results per that sensitivity mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.engine.events import ExitReason, Fill, Order, OrderStatus, OrderType, Side
from src.utils.config_models import ExecutionConfig


def _apply_slippage(price: float, *, side: Side, action: str, bps: float, extended_hours: bool, config: ExecutionConfig) -> float:
    """`action` is "buy" or "sell" for the ORDER's direction of trade (not the
    position side) -- adverse slippage always makes the fill worse for the trader.
    """
    multiplier = config.extended_hours_slippage_multiplier if extended_hours else 1.0
    effective_bps = bps * multiplier
    adj = price * (effective_bps / 10_000)
    return price + adj if action == "buy" else price - adj


def _commission(quantity: int, config: ExecutionConfig) -> float:
    return max(quantity * config.commission_per_share, config.commission_minimum)


@dataclass(frozen=True)
class BarWindow:
    """Minimal columnar view of the bars an entry/exit search operates over,
    to avoid re-slicing a Polars frame repeatedly inside hot loops."""

    open_ts: list[datetime]
    close_ts: list[datetime]
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]
    is_extended_hours: list[bool]


def simulate_entry_fill(
    order: Order, bars: BarWindow, start_idx: int, *, config: ExecutionConfig
) -> tuple[Fill | None, Order]:
    """Attempt to fill `order` starting at `bars[start_idx]` (must be the first
    bar strictly after the order was submitted). Returns (Fill or None, updated
    Order with a terminal status if filled/expired)."""
    action = "buy" if order.side == "long" else "sell"
    n = len(bars.open_ts)

    if order.order_type == OrderType.MARKET:
        if start_idx >= n:
            order.status = OrderStatus.EXPIRED
            return None, order
        px = bars.open[start_idx]
        slip_bps = config.slippage_bps_market
        fill_price = _apply_slippage(
            px, side=order.side, action=action, bps=slip_bps,
            extended_hours=bars.is_extended_hours[start_idx], config=config,
        )
        fill = Fill(
            order_id=order.order_id, symbol=order.symbol, side=order.side, quantity=order.quantity,
            fill_price=fill_price, fill_ts=bars.open_ts[start_idx],
            commission=_commission(order.quantity, config), slippage_points=abs(fill_price - px),
            bar_open_ts=bars.open_ts[start_idx],
        )
        order.status = OrderStatus.FILLED
        return fill, order

    if order.order_type == OrderType.LIMIT:
        limit = order.limit_price
        assert limit is not None
        for j in range(start_idx, n):
            if order.expiration_ts is not None and bars.open_ts[j] >= order.expiration_ts:
                order.status = OrderStatus.EXPIRED
                return None, order
            trades_through = (bars.low[j] <= limit) if action == "buy" else (bars.high[j] >= limit)
            if trades_through:
                fill_price = _apply_slippage(
                    limit, side=order.side, action=action, bps=config.slippage_bps_limit_adverse,
                    extended_hours=bars.is_extended_hours[j], config=config,
                )
                fill = Fill(
                    order_id=order.order_id, symbol=order.symbol, side=order.side, quantity=order.quantity,
                    fill_price=fill_price, fill_ts=bars.open_ts[j],
                    commission=_commission(order.quantity, config), slippage_points=abs(fill_price - limit),
                    bar_open_ts=bars.open_ts[j],
                )
                order.status = OrderStatus.FILLED
                return fill, order
        order.status = OrderStatus.EXPIRED
        return None, order

    raise ValueError(f"Unsupported entry order type: {order.order_type}")


@dataclass(frozen=True)
class ExitResult:
    exit_idx: int
    fill: Fill
    reason: ExitReason
    intrabar_ambiguous: bool


def resolve_exit(
    bars: BarWindow,
    start_idx: int,
    *,
    side: Side,
    quantity: int,
    stop_price: float,
    target_price: float | None,
    time_exit_ts: datetime | None,
    time_exit_reason: ExitReason,
    config: ExecutionConfig,
    order_id: str,
    symbol: str,
) -> ExitResult | None:
    """Walk forward from `bars[start_idx]` looking for the first bar where the
    position's stop, target, or time-based exit condition is satisfied."""
    n = len(bars.open_ts)
    exit_action = "sell" if side == "long" else "buy"  # closing a long = sell, closing a short = buy to cover

    for j in range(start_idx, n):
        if time_exit_ts is not None and bars.open_ts[j] >= time_exit_ts:
            px = bars.open[j]
            fill = Fill(
                order_id=order_id, symbol=symbol, side=side, quantity=quantity,
                fill_price=px, fill_ts=bars.open_ts[j], commission=_commission(quantity, config),
                slippage_points=0.0, bar_open_ts=bars.open_ts[j],
            )
            return ExitResult(exit_idx=j, fill=fill, reason=time_exit_reason, intrabar_ambiguous=False)

        touched_stop = (bars.low[j] <= stop_price) if side == "long" else (bars.high[j] >= stop_price)
        touched_target = (
            (target_price is not None)
            and ((bars.high[j] >= target_price) if side == "long" else (bars.low[j] <= target_price))
        )

        if touched_stop and touched_target:
            ambiguous = True
            take = config.intrabar_collision_mode
            reason = ExitReason.TAKE_PROFIT if take == "target_first" else ExitReason.STOP_LOSS
            trigger_price = target_price if take == "target_first" else stop_price
        elif touched_stop:
            ambiguous = False
            reason = ExitReason.STOP_LOSS
            trigger_price = stop_price
        elif touched_target:
            ambiguous = False
            reason = ExitReason.TAKE_PROFIT
            trigger_price = target_price
        else:
            continue

        if reason == ExitReason.STOP_LOSS:
            gapped = (bars.open[j] < stop_price) if side == "long" else (bars.open[j] > stop_price)
            base_price = bars.open[j] if gapped else stop_price
            fill_price = _apply_slippage(
                base_price, side=side, action=exit_action, bps=config.slippage_bps_stop,
                extended_hours=bars.is_extended_hours[j], config=config,
            )
        else:
            fill_price = _apply_slippage(
                trigger_price, side=side, action=exit_action, bps=config.slippage_bps_limit_adverse,
                extended_hours=bars.is_extended_hours[j], config=config,
            )

        fill = Fill(
            order_id=order_id, symbol=symbol, side=side, quantity=quantity,
            fill_price=fill_price, fill_ts=bars.open_ts[j], commission=_commission(quantity, config),
            slippage_points=abs(fill_price - trigger_price), bar_open_ts=bars.open_ts[j],
            intrabar_ambiguous=ambiguous,
        )
        return ExitResult(exit_idx=j, fill=fill, reason=reason, intrabar_ambiguous=ambiguous)

    return None
