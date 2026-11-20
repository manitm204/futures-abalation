from datetime import datetime, timedelta, timezone

import pytest

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.engine.metrics import compute_metrics

BASE = datetime(2024, 1, 2, tzinfo=timezone.utc)


def _fill(price: float, qty: int, commission: float = 1.0) -> Fill:
    return Fill(
        order_id="o", symbol="SPY", side="long", quantity=qty, fill_price=price,
        fill_ts=BASE, commission=commission, slippage_points=0.0, bar_open_ts=BASE,
    )


def _trade(pnl: float, r: float, side: str = "long", window: str = "ny_am", exit_reason=ExitReason.TAKE_PROFIT) -> Trade:
    t = Trade(
        trade_id=f"t{pnl}", config_id="c1", symbol="SPY", side=side,
        entry_order_id="e", entry_fill=_fill(100, 10), quantity=10,
        stop_price=99.0, target_price=101.0, window=window,
    )
    t.exit_fill = _fill(101, 10)
    t.exit_reason = exit_reason
    t.realized_pnl = pnl
    t.realized_r = r
    t.commission_total = 2.0
    t.holding_bars = 5
    return t


def test_win_rate_and_loss_rate() -> None:
    trades = [_trade(100, 1.0), _trade(-50, -1.0), _trade(200, 2.0), _trade(-30, -0.5)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.n_trades == 4
    assert m.win_rate == 0.5
    assert m.loss_rate == 0.5


def test_net_pnl_and_profit_factor() -> None:
    trades = [_trade(100, 1.0), _trade(-50, -1.0)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.net_pnl == pytest.approx(50.0)
    assert m.profit_factor == pytest.approx(100 / 50)


def test_avg_win_avg_loss_payoff_ratio() -> None:
    trades = [_trade(100, 1.0), _trade(200, 2.0), _trade(-50, -1.0)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.avg_win == pytest.approx(150.0)
    assert m.avg_loss == pytest.approx(-50.0)
    assert m.payoff_ratio == pytest.approx(3.0)


def test_expectancy_per_trade() -> None:
    trades = [_trade(100, 1.0), _trade(-50, -1.0)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.expectancy_per_trade == pytest.approx((100 - 50) / 2)


def test_avg_and_median_realized_r() -> None:
    trades = [_trade(100, 1.0), _trade(200, 3.0), _trade(-50, -1.0)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.avg_realized_r == pytest.approx((1.0 + 3.0 - 1.0) / 3)
    assert m.median_realized_r == pytest.approx(1.0)


def test_max_consecutive_wins_and_losses() -> None:
    trades = [_trade(10, 1), _trade(10, 1), _trade(-10, -1), _trade(10, 1), _trade(-10, -1), _trade(-10, -1), _trade(-10, -1)]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.max_consecutive_wins == 2
    assert m.max_consecutive_losses == 3


def test_max_drawdown_from_equity_curve() -> None:
    curve = [
        EquityPoint(ts=BASE, cash=100_000, position_value=0, equity=100_000),
        EquityPoint(ts=BASE + timedelta(days=1), cash=110_000, position_value=0, equity=110_000),
        EquityPoint(ts=BASE + timedelta(days=2), cash=88_000, position_value=0, equity=88_000),
        EquityPoint(ts=BASE + timedelta(days=3), cash=99_000, position_value=0, equity=99_000),
    ]
    m = compute_metrics([], curve, starting_equity=100_000)
    # peak 110,000 -> trough 88,000 -> dd = (88000-110000)/110000
    assert m.max_drawdown_pct == pytest.approx((88_000 - 110_000) / 110_000)


def test_total_return_pct() -> None:
    curve = [
        EquityPoint(ts=BASE, cash=100_000, position_value=0, equity=100_000),
        EquityPoint(ts=BASE + timedelta(days=1), cash=105_000, position_value=0, equity=105_000),
    ]
    m = compute_metrics([], curve, starting_equity=100_000)
    assert m.total_return_pct == pytest.approx(0.05)


def test_by_window_grouping() -> None:
    trades = [_trade(100, 1.0, window="ny_am"), _trade(-50, -1.0, window="ny_pm"), _trade(50, 0.5, window="ny_am")]
    m = compute_metrics(trades, [], starting_equity=100_000)
    assert m.by_window["ny_am"]["n_trades"] == 2
    assert m.by_window["ny_am"]["net_pnl"] == pytest.approx(150.0)
    assert m.by_window["ny_pm"]["n_trades"] == 1


def test_fill_rate_and_rejection_rate() -> None:
    trades = [_trade(100, 1.0)]
    m = compute_metrics(trades, [], starting_equity=100_000, n_signals=4, n_rejections=3)
    assert m.fill_rate == pytest.approx(0.25)
    assert m.rejection_rate == pytest.approx(0.75)


def test_empty_trades_does_not_crash() -> None:
    m = compute_metrics([], [], starting_equity=100_000)
    assert m.n_trades == 0
    assert m.win_rate == 0.0
    assert m.profit_factor is None
    assert m.avg_win is None
