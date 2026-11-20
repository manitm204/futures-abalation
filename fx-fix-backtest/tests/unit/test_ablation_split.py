"""_split_metrics attributes a single backtest's trades/equity to the correct
chronological split by entry timestamp."""

from __future__ import annotations

from datetime import datetime, timezone

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.experiments.ablation_runner import RunMeta, _split_metrics
from src.experiments.validation import DEFAULT_SPLIT
from src.utils.config_models import DEFAULT_EXECUTION_CONFIG


def _trade(entry: datetime, pnl: float) -> Trade:
    fill = Fill(order_id="o", symbol="SPY", side="long", quantity=1, fill_price=100.0,
                fill_ts=entry, commission=0.0, slippage_points=0.0, bar_open_ts=entry)
    t = Trade(trade_id="t", config_id="c", symbol="SPY", side="long", entry_order_id="o",
              entry_fill=fill, quantity=1, stop_price=99.0, target_price=101.0)
    t.realized_pnl = pnl
    t.realized_r = pnl
    t.exit_fill = fill
    t.exit_reason = ExitReason.TAKE_PROFIT
    return t


def _meta() -> RunMeta:
    return RunMeta(experiment_id="x", code_version="v", strategy_name="donchian_breakout",
                   execution_config=DEFAULT_EXECUTION_CONFIG, split=DEFAULT_SPLIT)


def test_trades_attributed_to_split_by_entry_date():
    # DEFAULT_SPLIT: dev 2018-2022, validation 2023-2024, holdout 2025-2026.
    trades = [
        _trade(datetime(2019, 6, 1, tzinfo=timezone.utc), 10.0),   # dev
        _trade(datetime(2021, 6, 1, tzinfo=timezone.utc), 20.0),   # dev
        _trade(datetime(2023, 6, 1, tzinfo=timezone.utc), -5.0),   # validation
        _trade(datetime(2025, 6, 1, tzinfo=timezone.utc), 7.0),    # holdout
    ]
    eq = [
        EquityPoint(ts=datetime(2019, 6, 1, tzinfo=timezone.utc), cash=0, position_value=0, equity=100_010),
        EquityPoint(ts=datetime(2021, 6, 1, tzinfo=timezone.utc), cash=0, position_value=0, equity=100_030),
        EquityPoint(ts=datetime(2023, 6, 1, tzinfo=timezone.utc), cash=0, position_value=0, equity=100_025),
        EquityPoint(ts=datetime(2025, 6, 1, tzinfo=timezone.utc), cash=0, position_value=0, equity=100_032),
    ]
    out = _split_metrics(trades, eq, _meta())
    assert out["development"]["n_trades"] == 2
    assert out["validation"]["n_trades"] == 1
    assert out["holdout"]["n_trades"] == 1


def test_empty_trades_give_zero_everywhere():
    out = _split_metrics([], [], _meta())
    assert all(out[s]["n_trades"] == 0 for s in ("development", "validation", "holdout"))
