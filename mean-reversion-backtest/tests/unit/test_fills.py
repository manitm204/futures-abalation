from datetime import datetime, timedelta, timezone

import pytest

from src.engine.events import ExitReason, Order, OrderPurpose, OrderStatus, OrderType
from src.engine.fills import BarWindow, resolve_exit, simulate_entry_fill
from src.utils.config_models import ExecutionConfig

BASE = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)


def _window(ohlc: list[tuple[float, float, float, float]], *, extended: list[bool] | None = None) -> BarWindow:
    n = len(ohlc)
    open_ts = [BASE + timedelta(minutes=i) for i in range(n)]
    close_ts = [t + timedelta(minutes=1) for t in open_ts]
    o, h, l, c = zip(*ohlc)
    return BarWindow(
        open_ts=open_ts, close_ts=close_ts,
        open=[float(x) for x in o], high=[float(x) for x in h],
        low=[float(x) for x in l], close=[float(x) for x in c],
        is_extended_hours=extended or [False] * n,
    )


def _order(**kwargs) -> Order:
    defaults = dict(
        order_id="o1", symbol="SPY", side="long", purpose=OrderPurpose.ENTRY,
        order_type=OrderType.MARKET, quantity=10, submitted_ts=BASE,
    )
    defaults.update(kwargs)
    return Order(**defaults)


CFG = ExecutionConfig()


def test_market_entry_fills_at_next_bar_open_with_adverse_slippage() -> None:
    bars = _window([(100, 101, 99, 100.5), (102, 103, 101, 102.5)])
    order = _order(order_type=OrderType.MARKET, side="long", quantity=10)
    fill, updated = simulate_entry_fill(order, bars, start_idx=1, config=CFG)
    assert fill is not None
    assert updated.status == OrderStatus.FILLED
    # buy at open=102, 1bp adverse slippage -> price slightly ABOVE 102
    assert fill.fill_price > 102.0
    assert fill.fill_price == pytest.approx(102.0 * 1.0001, rel=1e-6)


def test_market_entry_short_side_slippage_direction() -> None:
    bars = _window([(100, 101, 99, 100.5), (102, 103, 101, 102.5)])
    order = _order(order_type=OrderType.MARKET, side="short", quantity=10)
    fill, _ = simulate_entry_fill(order, bars, start_idx=1, config=CFG)
    # selling short: adverse slippage means WORSE (lower) fill price than 102
    assert fill.fill_price < 102.0


def test_limit_entry_fills_only_when_price_trades_through() -> None:
    bars = _window([(100, 100.5, 99.5, 100), (99, 99.5, 98, 99.2), (98.5, 99, 97.5, 98)])
    order = _order(order_type=OrderType.LIMIT, side="long", limit_price=98.5, quantity=10)
    fill, updated = simulate_entry_fill(order, bars, start_idx=0, config=CFG)
    assert fill is not None
    assert updated.status == OrderStatus.FILLED
    assert fill.fill_ts == bars.open_ts[1]  # first bar whose low <= 98.5
    assert fill.fill_price == 98.5  # no price improvement, exactly at limit (0 adverse slippage default)


def test_limit_entry_no_price_improvement_even_if_bar_gaps_through() -> None:
    # bar gaps well below the limit price -- fill must still be exactly at limit, not the better gap price
    bars = _window([(90, 90.5, 85, 89)])
    order = _order(order_type=OrderType.LIMIT, side="long", limit_price=95.0, quantity=10)
    fill, _ = simulate_entry_fill(order, bars, start_idx=0, config=CFG)
    assert fill.fill_price == 95.0


def test_limit_entry_expires_without_fill() -> None:
    bars = _window([(100, 100.5, 99.5, 100), (100, 100.5, 99.5, 100)])
    expiration = bars.open_ts[1]
    order = _order(order_type=OrderType.LIMIT, side="long", limit_price=50.0, expiration_ts=expiration, quantity=10)
    fill, updated = simulate_entry_fill(order, bars, start_idx=0, config=CFG)
    assert fill is None
    assert updated.status == OrderStatus.EXPIRED


def test_stop_exit_fills_at_stop_price_when_not_gapped() -> None:
    bars = _window([(100, 100.5, 98, 99)])  # low=98 breaches stop=99
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=99.0, target_price=None,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result is not None
    assert result.reason == ExitReason.STOP_LOSS
    # sell at stop with adverse slippage -> slightly below 99
    assert result.fill.fill_price < 99.0
    assert result.fill.fill_price == pytest.approx(99.0 * 0.9999, rel=1e-6)


def test_stop_exit_gap_fills_at_open_not_stop_price() -> None:
    # opens BELOW the stop (gapped through) -- must fill at open, not at the stale stop price
    bars = _window([(95, 96, 94, 95.5)])
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=99.0, target_price=None,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.STOP_LOSS
    # base price should be the gapped-through open (95), not 99, then adverse slippage applied
    assert result.fill.fill_price < 95.0
    assert result.fill.fill_price == pytest.approx(95.0 * 0.9999, rel=1e-6)


def test_target_exit_fills_exactly_at_target_no_improvement() -> None:
    bars = _window([(100, 105, 99.5, 104)])  # high=105 reaches target=103
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=90.0, target_price=103.0,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.TAKE_PROFIT
    assert result.fill.fill_price == 103.0  # default 0 adverse slippage on limit-style target fill


def test_same_bar_collision_defaults_to_stop_first() -> None:
    # both stop (95) and target (105) touched in the same bar
    bars = _window([(100, 106, 94, 100)])
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=95.0, target_price=105.0,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.STOP_LOSS
    assert result.intrabar_ambiguous is True


def test_same_bar_collision_target_first_mode() -> None:
    cfg = ExecutionConfig(intrabar_collision_mode="target_first")
    bars = _window([(100, 106, 94, 100)])
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=95.0, target_price=105.0,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=cfg,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.TAKE_PROFIT
    assert result.intrabar_ambiguous is True


def test_time_exit_triggers_at_cutoff_bar_open() -> None:
    bars = _window([(100, 101, 99, 100.5), (102, 103, 101, 102.5), (104, 105, 103, 104.5)])
    cutoff = bars.open_ts[2]
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=0.0, target_price=None,
        time_exit_ts=cutoff, time_exit_reason=ExitReason.WINDOW_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.WINDOW_EXIT
    assert result.fill.fill_ts == cutoff
    assert result.fill.fill_price == bars.open[2]


def test_short_side_stop_and_target_directions() -> None:
    bars = _window([(100, 102, 98, 99)])  # high=102 breaches short stop=101
    result = resolve_exit(
        bars, 0, side="short", quantity=10, stop_price=101.0, target_price=90.0,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result.reason == ExitReason.STOP_LOSS
    # covering a short at stop with adverse slippage -> fill price ABOVE 101
    assert result.fill.fill_price > 101.0


def test_no_exit_when_neither_stop_nor_target_touched() -> None:
    bars = _window([(100, 100.5, 99.5, 100.2)])
    result = resolve_exit(
        bars, 0, side="long", quantity=10, stop_price=90.0, target_price=110.0,
        time_exit_ts=None, time_exit_reason=ExitReason.SESSION_EXIT, config=CFG,
        order_id="x", symbol="SPY",
    )
    assert result is None
