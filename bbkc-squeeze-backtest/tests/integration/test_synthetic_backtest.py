"""End-to-end deterministic synthetic-dataset test for the execution engine.

Every expected value here is hand-computed from the config's known formulas
(risk-based sizing, commission schedule, slippage bps) rather than just
asserting "it ran" -- this is what the project spec calls out as required
before trusting any real backtest result.
"""

from datetime import datetime, timedelta, timezone

import polars as pl
import pytest

from src.engine.events import ExitReason, OrderType
from src.engine.simulator import TradeIntent, run_backtest_single_symbol
from src.utils.config_models import ExecutionConfig

BASE = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)
CFG = ExecutionConfig()  # $100k equity, 0.25% risk, $0.005/share commission ($1 min), 1bp market/stop slippage


def _bars_df(ohlc: list[tuple[float, float, float, float]]) -> pl.DataFrame:
    n = len(ohlc)
    open_ts = [BASE + timedelta(minutes=i) for i in range(n)]
    close_ts = [t + timedelta(minutes=1) for t in open_ts]
    o, h, l, c = zip(*ohlc)
    return pl.DataFrame(
        {
            "symbol": ["SPY"] * n,
            "bar_open_ts": open_ts, "bar_close_ts": close_ts,
            "open": [float(x) for x in o], "high": [float(x) for x in h],
            "low": [float(x) for x in l], "close": [float(x) for x in c],
        }
    )


def test_single_long_trade_hand_computed_pnl() -> None:
    # bar0: signal confirms at its close (14:31) -> entry fills at bar1's open.
    # bar3: high=106 reaches target=105 -> exits there (target hit before stop).
    bars = _bars_df(
        [
            (100, 101, 99, 100.5),      # bar0: confirmation bar
            (100.5, 102, 100, 101.5),   # bar1: entry fills at open=100.5
            (101.5, 103, 101, 102.5),   # bar2: no exit
            (102.5, 106, 102, 105),     # bar3: target (105) touched, stop (98) not touched
            (105, 106, 104, 105.5),     # bar4
        ]
    )
    intent = TradeIntent(
        signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
        submission_ts=bars["bar_close_ts"][0],  # == bar1's open_ts
        stop_price=98.0, target_price=105.0,
        entry_order_type=OrderType.MARKET,
    )
    result = run_backtest_single_symbol(bars, [intent], config=CFG)

    assert len(result.trades) == 1
    assert len(result.rejections) == 0
    trade = result.trades[0]

    # --- hand-computed expected values ---
    entry_raw_price = 100.5
    entry_slippage_bps = CFG.slippage_bps_market
    expected_entry_price = entry_raw_price * (1 + entry_slippage_bps / 10_000)
    # sizing: risk = 100_000 * 0.0025 = 250; stop_distance = 100.5 - 98.0 = 2.5
    # raw_qty = 250 / 2.5 = 100 -> floor -> 100 shares
    expected_qty = 100
    expected_entry_commission = max(expected_qty * CFG.commission_per_share, CFG.commission_minimum)  # 1.0

    assert trade.quantity == expected_qty
    assert trade.entry_fill.fill_price == pytest.approx(expected_entry_price, rel=1e-9)
    assert trade.entry_fill.commission == pytest.approx(expected_entry_commission)

    # target exit: no adverse slippage by default (slippage_bps_limit_adverse=0.0)
    expected_exit_price = 105.0
    expected_exit_commission = max(expected_qty * CFG.commission_per_share, CFG.commission_minimum)  # 1.0

    assert trade.exit_reason == ExitReason.TAKE_PROFIT
    assert trade.exit_fill.fill_price == pytest.approx(expected_exit_price)
    assert trade.exit_fill.commission == pytest.approx(expected_exit_commission)

    expected_gross_pnl = (expected_exit_price - expected_entry_price) * expected_qty
    expected_net_pnl = expected_gross_pnl - (expected_entry_commission + expected_exit_commission)
    assert trade.realized_pnl == pytest.approx(expected_net_pnl, rel=1e-9)

    expected_stop_distance = abs(entry_raw_price - 98.0)  # note: R is measured off intended stop, not fill price... see below
    # realized_r uses ENTRY FILL price (post-slippage) vs stop, per portfolio.py
    expected_r_stop_distance = abs(trade.entry_fill.fill_price - 98.0)
    expected_r = trade.realized_pnl / (expected_r_stop_distance * expected_qty)
    assert trade.realized_r == pytest.approx(expected_r, rel=1e-9)

    # --- equity bookkeeping sanity ---
    expected_final_cash = 100_000.0 + expected_net_pnl
    assert result.portfolio.cash == pytest.approx(expected_final_cash, rel=1e-9)


def test_stop_loss_exit_hand_computed() -> None:
    bars = _bars_df(
        [
            (100, 101, 99, 100.5),
            (100.5, 101, 100, 100.8),   # entry fills at open=100.5
            (100.8, 101, 97, 98.5),     # low=97 breaches stop=99 -> stop exit
        ]
    )
    intent = TradeIntent(
        signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
        submission_ts=bars["bar_close_ts"][0],
        stop_price=99.0, target_price=110.0,
    )
    result = run_backtest_single_symbol(bars, [intent], config=CFG)
    trade = result.trades[0]
    assert trade.exit_reason == ExitReason.STOP_LOSS

    expected_exit_raw = 99.0  # not gapped (open=100.8 > stop=99)
    expected_exit_price = expected_exit_raw * (1 - CFG.slippage_bps_stop / 10_000)
    assert trade.exit_fill.fill_price == pytest.approx(expected_exit_price, rel=1e-9)
    assert trade.realized_pnl < 0  # stopped out for a loss


def test_non_overlapping_positions_enforced() -> None:
    bars = _bars_df([(100, 101, 99, 100.5)] * 10)
    intents = [
        TradeIntent(
            signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
            submission_ts=bars["bar_close_ts"][0], stop_price=98.0, target_price=110.0,
        ),
        TradeIntent(
            signal_id="sig2", config_id="cfg1", symbol="SPY", side="long",
            submission_ts=bars["bar_close_ts"][1], stop_price=98.0, target_price=110.0,
        ),
    ]
    result = run_backtest_single_symbol(bars, intents, config=CFG)
    # sig1 opens and never exits within the flat data (target/stop never touched) ->
    # forced-closed at data end; sig2 arrives while sig1's position window overlaps
    # only if sig1 is still open when sig2 is processed. With flat bars neither stop
    # nor target trigger, so sig1 remains open through the whole series and sig2
    # must be rejected for overlap.
    assert len(result.rejections) == 1
    assert result.rejections[0].reason == "position_already_open"
    assert len(result.trades) == 1


def test_invalid_stop_geometry_rejected() -> None:
    bars = _bars_df([(100, 101, 99, 100.5), (100.5, 101, 100, 100.8)])
    # long trade with stop ABOVE the entry price -- invalid geometry
    intent = TradeIntent(
        signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
        submission_ts=bars["bar_close_ts"][0], stop_price=105.0, target_price=110.0,
    )
    result = run_backtest_single_symbol(bars, [intent], config=CFG)
    assert len(result.trades) == 0
    assert result.rejections[0].reason == "invalid_stop_geometry"


def test_equity_curve_is_populated_not_empty() -> None:
    """Regression test: the simulator must call portfolio.mark_to_market so
    equity_curve is non-empty and metrics.py's daily-return-based Sharpe/Sortino/
    drawdown can actually be computed. Found via Phase 8 report generation,
    where every config's Sharpe was silently None because equity_curve stayed
    empty for the entire history of this project until this fix."""
    bars = _bars_df(
        [
            (100, 101, 99, 100.5),
            (100.5, 102, 100, 101.5),
            (101.5, 103, 101, 102.5),
            (102.5, 106, 102, 105),
            (105, 106, 104, 105.5),
        ]
    )
    intent = TradeIntent(
        signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
        submission_ts=bars["bar_close_ts"][0], stop_price=98.0, target_price=105.0,
    )
    result = run_backtest_single_symbol(bars, [intent], config=CFG)
    assert len(result.portfolio.equity_curve) >= 2  # at least an initial point plus one after the trade closes


def test_forced_close_at_data_end_when_no_exit_triggers() -> None:
    bars = _bars_df([(100, 101, 99, 100.5), (100.5, 101, 100, 100.8), (100.8, 101, 100.5, 100.9)])
    intent = TradeIntent(
        signal_id="sig1", config_id="cfg1", symbol="SPY", side="long",
        submission_ts=bars["bar_close_ts"][0], stop_price=50.0, target_price=200.0,
    )
    result = run_backtest_single_symbol(bars, [intent], config=CFG)
    trade = result.trades[0]
    assert trade.exit_reason == ExitReason.SESSION_EXIT
    assert trade.exit_fill.fill_ts == bars["bar_close_ts"][-1]
