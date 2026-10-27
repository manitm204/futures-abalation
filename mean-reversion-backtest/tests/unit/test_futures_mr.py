"""Futures support for the mean-reversion funnel: roll back-adjustment, the
futures cost model, and best-k dedup representatives."""

from __future__ import annotations

from datetime import datetime, timezone

import polars as pl
import pytest

from src.data.futures import back_adjust, drop_sessions, illiquid_sessions
from src.experiments.funnel import select_representatives
from src.experiments.mr_grid import mr_grid_v3
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs
from src.utils.config_models import ExecutionConfig

FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=2.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)


def _raw(prices, ids):
    t0 = datetime(2024, 3, 12, 23, 58, tzinfo=timezone.utc)
    return pl.DataFrame({
        "ts_event": [t0.replace(minute=58 + i) if i < 2 else datetime(2024, 3, 13, 0, i - 2, tzinfo=timezone.utc)
                     for i in range(len(prices))],
        "instrument_id": ids, "open": prices, "high": prices, "low": prices, "close": prices,
        "volume": [1] * len(prices),
    })


def test_back_adjust_removes_roll_gap_and_keeps_latest_contract_raw():
    df = _raw([100.0, 101.0, 111.0, 112.0], [1, 1, 2, 2])
    out, log = back_adjust(df)
    assert out["close"].to_list() == [110.0, 111.0, 111.0, 112.0]
    assert out["price_adjustment"].to_list() == [10.0, 10.0, 0.0, 0.0]
    assert log == [{"ts": str(df["ts_event"][2]), "to_instrument_id": 2, "gap_points": 10.0}]


def test_back_adjust_accumulates_multiple_rolls():
    df = _raw([100.0, 105.0, 103.0, 110.0], [1, 2, 2, 3])
    out, _ = back_adjust(df)
    # gaps: +5 at bar 1 (close 100 -> open 105), +7 at bar 3 (close 103 -> open 110)
    assert out["price_adjustment"].to_list() == [12.0, 7.0, 7.0, 0.0]


def test_futures_cost_model_ticks_commission_and_whole_contracts():
    c = CostModel.for_symbol(FUT, "ES")
    assert c.fill(5000.0, "buy") == 5000.25
    assert c.fill(5000.0, "sell", stop=True) == 4999.5
    # $1M at 5000 x $50 = $250k/contract -> 3 contracts (4 would need $1M + commission)
    q = c.size(1_000_000, 5000.25 + 900, 5000.25)  # adjusted price ignored for sizing
    assert q == 3 * 50
    assert c.commission(q) == 7.5


def test_scale_variable_costs_scales_futures_fields():
    s = scale_variable_costs(FUT, 2.0)
    assert (s.commission_per_contract, s.slippage_ticks_market, s.slippage_ticks_stop) == (5.0, 2.0, 4.0)


def test_equity_cost_model_unchanged():
    ec = ExecutionConfig()
    c = CostModel.for_symbol(ec, "SPY")
    assert c.fill(100.0, "buy") == pytest.approx(100.01)
    assert c.commission(10) == 1.0


def test_v3_grid_size():
    assert len(mr_grid_v3(("ES",))) == 46_080


def test_select_representatives_keeps_best_k_per_cluster():
    recs = [{"config_id": f"c{i}", "neighbor_median_sharpe": s, "n_profitable_years": 5, "dev_sharpe": s}
            for i, s in enumerate([1.0, 0.9, 0.8, 0.7])]
    cluster_of = {"c0": 0, "c1": 0, "c2": 0, "c3": 1}
    reps = select_representatives(recs, cluster_of, k=2)
    assert [r["config_id"] for r in reps] == ["c0", "c1", "c3"]
    assert [r["config_id"] for r in select_representatives(recs, cluster_of)] == ["c0", "c3"]


def test_illiquid_sessions_flags_stale_expiring_contract_day_and_drop_unflags_it():
    from datetime import date, timedelta
    days = [date(2018, 1, 1) + timedelta(days=i) for i in range(10)]
    vols = [1000] * 9 + [10]   # last day: 1% of normal volume
    df = pl.DataFrame({"session_date_ny": days, "is_regular_session": [True] * 10,
                       "is_extended_hours": [False] * 10, "volume": vols, "instrument_id": [1] * 10})
    hit = illiquid_sessions(df, min_volume_frac=0.05)
    assert hit["session_date_ny"].to_list() == [days[-1]]
    out = drop_sessions(df, hit["session_date_ny"].to_list())
    assert out["is_regular_session"].to_list() == [True] * 9 + [False]
    assert out["is_extended_hours"][-1]


def test_v8_grid_size():
    from src.experiments.mr_grid import mr_grid_v8
    assert len(mr_grid_v8(("RTY",))) == 84_672


def test_v9_grid_size():
    from src.experiments.mr_grid import mr_grid_v9
    assert len(mr_grid_v9(("CL",))) == 17_280


def test_v10_v11_grid_sizes():
    from src.experiments.mr_grid import mr_grid_v10, mr_grid_v11
    assert len(mr_grid_v10(("ES",))) == 864
    assert len(mr_grid_v11(("ES",))) == 6_804
    assert {e.config.mean_type for e in mr_grid_v11(("ES",))} == {"sma"}


def test_v12_v13_grid_sizes():
    from src.experiments.mr_grid import mr_grid_v12, mr_grid_v13
    assert len(mr_grid_v12(("NQ",))) == 1_152
    assert len(mr_grid_v13(("NQ",))) == 3_456
    assert {e.config.mean_type for e in mr_grid_v13(("NQ",))} == {"sma", "ema"}
    assert {e.config.stop_atr_multiple for e in mr_grid_v13(("NQ",))} == {"none", "1.5", "2.0"}



def test_v14_v15_grid_sizes():
    from src.experiments.mr_grid import mr_grid_v14, mr_grid_v15
    assert len(mr_grid_v14(("YM",))) == 17_280
    assert len(mr_grid_v15(("YM",))) == 23_328
    assert {e.config.stop_atr_multiple for e in mr_grid_v14(("YM",))} == {"none", "1.3", "1.8"}
    assert {e.config.stop_atr_value for e in mr_grid_v15(("YM",))} == {None, 0.75, 1.5}
    assert {e.config.entry_confirmation for e in mr_grid_v15(("YM",))} == {"none", "positive_bar_return"}


def test_v16_v17_grid_sizes():
    from src.experiments.mr_grid import mr_grid_v16, mr_grid_v17
    assert len(mr_grid_v16(("RTY",))) == 13_608
    assert len(mr_grid_v17(("RTY",))) == 8_640
    assert {e.config.exit_z for e in mr_grid_v16(("RTY",))} == {-1.0, 0.0, 1.0}
    assert {e.config.stop_atr_value for e in mr_grid_v17(("RTY",))} == {None, 1.5, 2.0, 2.5}


def test_v18_grid_size():
    from src.experiments.mr_grid import mr_grid_v18
    grid = mr_grid_v18(("CL",))
    assert len(grid) == 16_128
    assert {e.config.entry_confirmation for e in grid} == {"positive_bar_return"}
    assert {e.config.stop_atr_value for e in grid} == {None, 1.0, 1.5, 2.0}


def test_v19_v20_grid_sizes():
    from src.experiments.mr_grid import mr_grid_v19, mr_grid_v20
    assert len(mr_grid_v19(("GC",))) == 21_504
    assert len(mr_grid_v20(("GC",))) == 17_280
    assert {e.config.max_holding_bars for e in mr_grid_v19(("GC",))} == {5, 8, 10, 14}
    assert {e.config.entry_confirmation for e in mr_grid_v20(("GC",))} == {"none", "positive_bar_return"}

def test_v21_grid_size():
    from src.experiments.mr_grid import mr_grid_v21
    grid = mr_grid_v21(("6E",))
    assert len(grid) == 24_000
    assert {e.config.entry_z for e in grid} == {-1.5, -1.75, -2.0, -2.25, -2.5}
    assert {e.config.stop_atr_value for e in grid} == {None, 1.5, 2.0, 2.5}


def test_random_intervals_hit_target_exposure_without_overlap():
    import numpy as np
    from src.experiments.random_entry import random_intervals
    rng = np.random.default_rng(0)
    n = 10_000
    covers = []
    for _ in range(200):
        iv = random_intervals(n, 0.07, rng)
        occ = np.zeros(n, dtype=int)
        for s, h in iv:
            assert 3 <= h <= 10 and s >= 0 and s + h < n
            occ[s:s + h + 1] += 1
        assert occ.max() <= 1                      # no overlapping trades
        covers.append(occ.sum() / n)
    assert abs(np.mean(covers) - 0.07) < 0.002     # unbiased time in market
