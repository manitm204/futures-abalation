"""One account balance shared by several strategies: 0.75x per trade, 1.0x cap."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from src.experiments.shared_account import share_account
from src.strategies.mean_reversion.backtest import STOP_EXIT, TIME_EXIT, CostModel, SimResult
from src.utils.config_models import ExecutionConfig

FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=0.0, slippage_ticks_stop=0.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
DATA = SimpleNamespace(price_adj=np.zeros(100), bar_open=np.datetime64("2024-01-02T14:00") + np.arange(100) * np.timedelta64(60, "m"))


def _sim(entries, exits, entry_px, exit_px, reasons=None):
    k = len(entries)
    a = lambda v, t=float: np.asarray(v, dtype=t)  # noqa: E731
    return SimResult(trades=[], equity_curve=[], signal_idx=a(entries, np.int64) - 1, entry_idx=a(entries, np.int64),
                     exit_idx=a(exits, np.int64), decision_idx=a(exits, np.int64) - 1, quantity=np.ones(k),
                     entry_px=a(entry_px), exit_px=a(exit_px), entry_commission=np.zeros(k), realized_pnl=np.zeros(k),
                     forced_close=np.zeros(k, dtype=bool),
                     exit_reason=np.asarray(reasons or [TIME_EXIT] * k, dtype=object), stop_level=np.full(k, np.nan))


def test_second_trade_gets_the_remaining_quarter():
    costs = CostModel.for_symbol(FUT, "ES")  # 3900 x $50 = $195k per contract
    a = _sim([10, 50], [20, 60], [3900.0, 3900.0], [3910.0, 3900.0])
    b = _sim([15], [25], [3900.0], [3890.0])
    r = share_account([a, b], DATA, costs, 1_000_000, per_trade=0.75, cap=1.0)
    # A: 0.75 x $1M -> 3 contracts ($585k). B opens while A is open: min($750k, $1M - $585k) -> 2 contracts.
    assert r.contracts[0].tolist() == [3, 3] and r.contracts[1].tolist() == [2]
    assert r.trimmed[1].tolist() == [True] and r.trimmed[0].tolist() == [False, False]
    assert r.sims[0].realized_pnl[0] == 10 * 3 * 50 - 2 * 3 * 2.5
    assert r.sims[1].realized_pnl[0] == -10 * 2 * 50 - 2 * 2 * 2.5


def test_same_bar_open_exit_frees_capital_but_stop_does_not():
    costs = CostModel.for_symbol(FUT, "ES")
    a = _sim([10], [15], [3900.0], [3900.0])
    b = _sim([15], [20], [3900.0], [3900.0])
    assert share_account([a, b], DATA, costs, 1_000_000).contracts[1].tolist() == [3]
    a_stop = _sim([10], [15], [3900.0], [3800.0], [STOP_EXIT])
    assert share_account([a_stop, b], DATA, costs, 1_000_000, bar_minutes=60).contracts[1].tolist() == [2]


def test_different_bar_sizes_ordered_by_clock_time():
    costs = CostModel.for_symbol(FUT, "ES")
    t0 = np.datetime64("2024-01-02T14:30")
    m15 = SimpleNamespace(price_adj=np.zeros(100), bar_open=t0 + np.arange(100) * np.timedelta64(15, "m"))
    h1 = SimpleNamespace(price_adj=np.zeros(100), bar_open=t0 + np.arange(100) * np.timedelta64(60, "m"))
    a = _sim([2], [4], [3900.0], [3900.0])   # 1h: in 16:30, out at 18:30's open
    b = _sim([12], [14], [3900.0], [3900.0])  # 15m: in 17:30 while the 1h trade is open
    c = _sim([16], [20], [3900.0], [3900.0])  # 15m: in 18:30, the moment the 1h trade exits
    bc = _sim([12, 16], [14, 20], [3900.0] * 2, [3900.0] * 2)
    r = share_account([a, bc], [h1, m15], costs, 1_000_000, bar_minutes=[60, 15])
    assert r.contracts[1].tolist() == [2, 3]


def test_trade_skipped_when_less_than_one_contract_left():
    costs = CostModel.for_symbol(FUT, "ES")  # 7400 x $50 = $370k; 2 contracts use $740k, $260k left < $370k
    a = _sim([10], [20], [7400.0], [7400.0])
    b = _sim([12], [18], [7400.0], [7400.0])
    r = share_account([a, b], DATA, costs, 1_000_000)
    assert r.contracts[1].tolist() == [0] and len(r.sims[1].entry_idx) == 0
