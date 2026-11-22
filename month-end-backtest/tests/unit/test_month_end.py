"""Treasury month-end long (day session only): the month-end day count against the NYSE calendar,
the strike-time switch, the 08:00-17:00 bar window, entries / exits, the event filters, early
closes and gaps, the placebo day mask, integrity checks (and that they catch tampered trades),
look-ahead truncation, the grid / lattice / local moves and the market config."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_ME_V1, LATTICE_ME_V2
from src.data.calendars import TradingCalendar
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_me, perturbations_me
from src.experiments.me_grid import AXES_ME_V1, AXES_ME_V2, me_grid_v1, me_grid_v2
from src.experiments.me_integrity import check_sim_integrity, independent_rank, truncation_invariance
from src.strategies.month_end.backtest import (
    EOD_EXIT,
    STOP_EXIT,
    TIME_EXIT,
    MEData,
    MEParams,
    me_day_bars,
    month_end_rank,
    simulate_month_end,
)
from src.strategies.month_end.config import FOMC_DAYS, MonthEndV1Config, MonthEndV2Config, auction_days, exit_minutes, hhmm_minutes
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 1 / 64
P = MEParams("ZN", "1min", window=3, entry_min=8 * 60 + 20, exit_rule="strike", event_filter="none")
CAL = TradingCalendar()


def _p(**kw) -> MEParams:
    return replace(P, **kw)


def _bars(start=date(2020, 11, 2), end=date(2021, 3, 5), seed=0, vol=0.02, first="07:00", last="17:59",
          drop: set[tuple[date, int]] | None = None, stop_at: dict[date, int] | None = None,
          extra_days: tuple[date, ...] = ()) -> pl.DataFrame:
    """1-minute ZN-like bars on NYSE trading days (+ `extra_days`) from `first` to `last` NY
    (inclusive), random walk. `drop` removes (date, NY minute) bars; `stop_at` ends a day's bars
    early (an early close)."""
    rng = np.random.default_rng(seed)
    h0, m0 = map(int, first.split(":"))
    h1, m1 = map(int, last.split(":"))
    days = sorted(set(CAL.trading_days(start, end)) | set(extra_days))
    rows, px = [], 135.0
    for d in days:
        t_end = min(h1 * 60 + m1, (stop_at or {}).get(d, 10 ** 6))
        for t in range(h0 * 60 + m0, t_end + 1):
            if drop and (d, t) in drop:
                continue
            ny = datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)
            o = px
            c = px + float(rng.normal(0, vol))
            rows.append({"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
                         "open": o, "high": max(o, c) + TICK, "low": min(o, c) - TICK, "close": c,
                         "volume": 100, "price_adjustment": 0.0})
            px = c
    df = pl.DataFrame(rows)
    return df.with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _data(**kw) -> MEData:
    return MEData(me_day_bars(_bars(**kw)))


def _trade_days(d: MEData, s) -> list[date]:
    return [d.day_list[int(d.sess[e])] for e in s.entry_idx]


# --- calendar ------------------------------------------------------------------------------------

@pytest.mark.parametrize("day,rank", [
    (date(2020, 12, 31), 1), (date(2020, 12, 30), 2), (date(2020, 12, 24), 5), (date(2021, 1, 29), 1),
    (date(2021, 1, 27), 3), (date(2021, 1, 18), 0),          # MLK day: not an NYSE trading day
    (date(2024, 3, 28), 1), (date(2018, 3, 29), 1),          # Good Friday was the month's last weekday
    (date(2024, 11, 29), 1), (date(2026, 10, 30), 1),
])
def test_month_end_rank_known_days(day, rank):
    assert month_end_rank([day])[0] == rank
    assert independent_rank([day])[0] == rank


def test_rank_uses_the_whole_month_even_when_data_stops_early():
    # Data ending mid-month must not move the month-end: 2021-01-15 is 10 trading days before the end.
    assert month_end_rank([date(2021, 1, 15)])[0] == 10


def test_strike_time_switches_in_january_2021():
    assert exit_minutes("strike", date(2020, 12, 31)) == 15 * 60
    assert exit_minutes("strike", date(2021, 1, 29)) == 16 * 60
    assert exit_minutes("15:00", date(2021, 1, 29)) == 15 * 60
    assert exit_minutes("16:00", date(2020, 12, 31)) == 16 * 60


def test_event_calendars_load():
    auc = auction_days()
    assert len(auc) > 700 and date(2021, 1, 28) in auc       # 7-year note auction
    assert date(2021, 1, 27) in FOMC_DAYS and date(2026, 10, 28) in FOMC_DAYS


# --- execution -----------------------------------------------------------------------------------

def test_day_window_drops_bars_outside_08_to_17():
    b = me_day_bars(_bars(start=date(2021, 1, 4), end=date(2021, 1, 6)))
    tod = (b["bar_open_ts_ny"].dt.hour().cast(pl.Int32) * 60 + b["bar_open_ts_ny"].dt.minute().cast(pl.Int32)).to_numpy()
    assert tod.min() == 8 * 60 and tod.max() == 17 * 60 - 1


def test_trades_on_last_n_days_with_entry_open_and_strike_exit():
    d = _data()
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    days = _trade_days(d, s)
    assert days[:3] == [date(2020, 11, 25), date(2020, 11, 27), date(2020, 11, 30)]
    assert date(2020, 12, 31) in days and date(2021, 1, 29) in days and len(days) == 4 * 3
    for i, day in enumerate(days):
        e, x = int(s.entry_idx[i]), int(s.exit_idx[i])
        assert d.tod[e] == 8 * 60 + 20 and s.entry_px[i] == pytest.approx(d.open[e] + TICK)
        assert d.tod[x] == exit_minutes("strike", day) - 1               # the bar that closes at the strike
        assert s.exit_px[i] == pytest.approx(d.close[x] - TICK) and s.exit_reason[i] == TIME_EXIT
        assert (s.side == 1).all()


def test_window_and_entry_time():
    d = _data()
    for w in (1, 2, 5, 6):
        s = simulate_month_end(d, _p(window=w, entry_min=14 * 60, exit_rule="16:00"), exec_config=FUT,
                               starting_equity=1e6)
        assert len(s.entry_idx) == 4 * w
        assert (d.tod[s.entry_idx] == 14 * 60).all() and (d.tod[s.exit_idx] == 16 * 60 - 1).all()


def test_event_filters_skip_fomc_and_auction_days():
    d = _data()
    base = set(_trade_days(d, simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)))
    fomc = set(_trade_days(d, simulate_month_end(d, _p(event_filter="skip_fomc"), exec_config=FUT, starting_equity=1e6)))
    both = set(_trade_days(d, simulate_month_end(d, _p(event_filter="skip_fomc_auction"), exec_config=FUT,
                                                 starting_equity=1e6)))
    assert base - fomc == {date(2021, 1, 27)}
    auc = auction_days()
    assert both == {x for x in fomc if x not in auc} and len(both) < len(fomc)


def test_early_close_exits_at_the_last_bar():
    d = _data(stop_at={date(2020, 11, 27): 13 * 60 + 14})          # the bars stop at 13:14 ET
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    i = _trade_days(d, s).index(date(2020, 11, 27))
    assert s.exit_reason[i] == EOD_EXIT and d.tod[s.exit_idx[i]] == 13 * 60 + 14
    s2 = simulate_month_end(d, _p(entry_min=14 * 60), exec_config=FUT, starting_equity=1e6)
    assert date(2020, 11, 27) not in _trade_days(d, s2)             # no bar at 14:00: day skipped


def test_gap_at_entry_time_skips_the_day():
    gap = {(date(2020, 12, 30), t) for t in range(8 * 60 + 20, 8 * 60 + 27)}
    d = _data(drop=gap)
    days = _trade_days(d, simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6))
    assert date(2020, 12, 30) not in days and date(2020, 12, 31) in days
    small = {(date(2020, 12, 30), t) for t in range(8 * 60 + 20, 8 * 60 + 23)}
    d2 = _data(drop=small)
    s2 = simulate_month_end(d2, P, exec_config=FUT, starting_equity=1e6)
    i = _trade_days(d2, s2).index(date(2020, 12, 30))
    assert d2.tod[s2.entry_idx[i]] == 8 * 60 + 23                     # 3 minutes late is allowed


def test_non_nyse_days_never_trade():
    d = _data(extra_days=(date(2021, 1, 18),))
    assert d.rank[d.day_list.index(date(2021, 1, 18))] == 0
    s = simulate_month_end(d, _p(window=5), exec_config=FUT, starting_equity=1e6)
    assert date(2021, 1, 18) not in _trade_days(d, s)


def test_stop_exits_at_first_touch_with_worse_fill():
    d = _data(vol=0.05, seed=3)
    p = _p(window=6, stop_pct=0.05)
    s = simulate_month_end(d, p, exec_config=FUT, starting_equity=1e6)
    stops = np.flatnonzero(s.exit_reason == STOP_EXIT)
    assert len(stops) > 0
    for i in stops:
        e, x = int(s.entry_idx[i]), int(s.exit_idx[i])
        stop = d.open[e] * (1 - 0.05 / 100)
        assert s.stop_level[i] == pytest.approx(stop)
        assert d.low[x] <= stop and (d.low[e:x] > stop).all()          # first touch
        assert s.exit_px[i] == pytest.approx(min(d.open[x], stop) - TICK)
    assert check_sim_integrity(s, d, FUT, p) == []
    none = simulate_month_end(d, _p(window=6), exec_config=FUT, starting_equity=1e6)
    assert np.isnan(none.stop_level).all() and STOP_EXIT not in set(none.exit_reason)


def test_integrity_catches_moved_stops():
    d = _data(vol=0.05, seed=3)
    p = _p(window=6, stop_pct=0.05)
    s = simulate_month_end(d, p, exec_config=FUT, starting_equity=1e6)
    t = replace(s, stop_level=s.stop_level * 0.99)
    assert "stop_not_per_rule" in check_sim_integrity(t, d, FUT, p)
    i = int(np.flatnonzero(s.exit_reason == STOP_EXIT)[0])
    t = replace(s, exit_px=s.exit_px.copy())
    t.exit_px[i] += 1.0                                                 # a stop filled far above the stop
    assert "stop_fill_better_than_rule" in check_sim_integrity(t, d, FUT, p)


def test_position_is_unlevered_whole_contracts():
    d = _data()
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    contracts = s.quantity / 1000
    assert np.allclose(contracts, np.round(contracts)) and (contracts >= 1).all()
    assert (s.quantity * s.entry_px <= 1e6 * 1.2).all()


def test_placebo_day_mask_replaces_the_calendar():
    d = _data()
    mask = np.zeros(len(d.days), dtype=bool)
    mask[[3, 10, 20]] = True
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6, day_mask=mask)
    assert [int(d.sess[e]) for e in s.entry_idx] == [3, 10, 20]


# --- integrity -----------------------------------------------------------------------------------

def test_integrity_clean_on_the_grid():
    d = _data(start=date(2020, 9, 1), end=date(2021, 6, 30), seed=1)
    for ce in me_grid_v1(("ZN",))[::23]:
        s = simulate_month_end(d, ce.config, exec_config=FUT, starting_equity=1e6)
        assert len(s.entry_idx) > 0
        assert check_sim_integrity(s, d, FUT, ce.config) == [], ce.config


def test_integrity_catches_tampered_trades():
    d = _data()
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    assert check_sim_integrity(s, d, FUT, P) == []

    t = replace(s, entry_idx=s.entry_idx.copy(), signal_idx=s.signal_idx.copy(), entry_base=s.entry_base.copy())
    t.entry_idx[1] += 2
    t.signal_idx[1] += 2
    t.entry_base[1] = d.open[t.entry_idx[1]]
    assert "entry_not_per_rule" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, side=s.side.copy())
    t.side[0] = -1
    assert "not_long" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, entry_px=s.entry_px.copy())
    t.entry_px[1] = d.open[s.entry_idx[1]] - TICK
    assert "entry_fill_better_than_market" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, exit_idx=s.exit_idx.copy())
    t.exit_idx[1] += 3
    assert "time_exit_not_per_rule" in check_sim_integrity(t, d, FUT, P)

    keep = np.arange(len(s.entry_idx)) != 2
    fields = ("signal_idx", "entry_idx", "exit_idx", "decision_idx", "quantity", "entry_px", "exit_px",
              "entry_commission", "realized_pnl", "forced_close", "exit_reason", "entry_base", "side", "stop_level")
    t = replace(s, **{k: getattr(s, k)[keep] for k in fields})
    assert "trade_skipped_while_flat" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, quantity=s.quantity * 100)
    assert "position_exceeds_equity" in check_sim_integrity(t, d, FUT, P)

    # A trade on a day outside the window: shift trade 0 to the same clock 5 sessions earlier.
    t = replace(s, entry_idx=s.entry_idx.copy(), signal_idx=s.signal_idx.copy(), exit_idx=s.exit_idx.copy(),
                entry_base=s.entry_base.copy(), entry_px=s.entry_px.copy())
    sess = int(d.sess[s.entry_idx[0]]) - 5
    e = int(d.day_start_idx[sess]) + int(s.entry_idx[0] - d.day_start_idx[d.sess[s.entry_idx[0]]])
    t.entry_idx[0] = t.signal_idx[0] = e
    t.exit_idx[0] = e + int(s.exit_idx[0] - s.entry_idx[0])
    t.entry_base[0], t.entry_px[0] = d.open[e], d.open[e] + TICK
    assert "day_not_eligible" in check_sim_integrity(t, d, FUT, P)


def test_integrity_catches_trades_on_filtered_days():
    d = _data()
    s = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    assert "event_filter_violated" in check_sim_integrity(s, d, FUT, _p(event_filter="skip_fomc"))


def test_no_lookahead_under_truncation():
    b = me_day_bars(_bars(start=date(2020, 9, 1), end=date(2021, 6, 30), seed=2))
    for p in (P, _p(window=5, entry_min=12 * 60, exit_rule="16:00", event_filter="skip_fomc_auction", stop_pct=0.25),
              _p(window=1, exit_rule="15:00")):
        assert truncation_invariance(b, p, exec_config=FUT, cut_fracs=(0.3, 0.55, 0.8, 0.97)) == []


def test_stress_knobs():
    d = _data()
    base = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6)
    late = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6, entry_delay_bars=1)
    assert (late.entry_idx == base.entry_idx + 1).all()
    miss = simulate_month_end(d, P, exec_config=FUT, starting_equity=1e6, missed_entry_frac=0.5, stress_seed=1)
    assert 0 < len(miss.entry_idx) < len(base.entry_idx)


# --- grid, lattice, local moves, config ----------------------------------------------------------

def test_grid_size_and_lattice():
    g = me_grid_v1(("ZN",))
    assert len(g) == 972 and len({c.config_id for c in g}) == 972
    for ax, vals in LATTICE_ME_V1.ordered.items():
        assert set(vals) == set(AXES_ME_V1[ax])


def test_local_and_random_perturbations():
    cfg = load_funnel_config(ROOT / "configs/funnel/me_funnel_zn_v1.yaml")
    lc = cfg.parameter_stability.local
    moves = dict(local_perturbations_me(_p(entry_min=10 * 60, stop_pct=0.25), lc))
    assert set(moves) == {"entry=09:30", "entry=10:30", "exit_shift=-15min", "exit_shift=+15min",
                          "window=2", "window=4", "stop_pct=0.15", "stop_pct=0.35"}
    low = dict(local_perturbations_me(_p(window=1), lc))
    assert set(low) == {"entry=08:00", "entry=08:50", "exit_shift=-15min", "exit_shift=+15min", "window=2"}
    d = _data()
    for _, mp in moves.items():
        s = simulate_month_end(d, mp, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, mp) == []
    ps = perturbations_me(_p(entry_min=10 * 60, stop_pct=0.25), config_id="x", base_seed=1,
                          pcfg=cfg.parameter_stability.perturbation)
    assert len(ps) == 20 and all(q.entry_min != 10 * 60 and q.exit_shift != 0 and q.window == 3 for q in ps)
    assert all(0.2 <= q.stop_pct <= 0.3 and q.stop_pct != 0.25 for q in ps)


def test_funnel_config_and_family_wiring():
    cfg = load_funnel_config(ROOT / "configs/funnel/me_funnel_zn_v1.yaml")
    assert cfg.strategy == "month_end_v1" and cfg.symbol == "ZN" and cfg.confidence.transfer_symbol == "ZB"
    assert family_for(cfg).simulate is simulate_month_end
    d = _data()
    ce = me_grid_v1(("ZN",))[0]
    rec, rets = build_dev_record(ce, d, fcfg=cfg, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) == len(d.days)


def test_config_rejects_off_grid_values():
    with pytest.raises(Exception):
        MonthEndV1Config(symbol="ZN", window=7)
    with pytest.raises(Exception):
        MonthEndV1Config(symbol="ZN", stop="1.0")
    with pytest.raises(Exception):
        MonthEndV1Config(symbol="ZN", entry="09:30")
    with pytest.raises(Exception):
        MonthEndV1Config(symbol="ZN", exit="17:00")



# --- v2: turn of the month (ES) ------------------------------------------------------------------

def test_v2_grid_size_validity_and_lattice():
    g = me_grid_v2(("ES",))
    assert len(g) == 4864 and len({c.config_id for c in g}) == 4864
    assert all(c.config.window + c.config.first_days >= 1 for c in g)
    assert all(hhmm_minutes(c.config.exit) > hhmm_minutes(c.config.entry) for c in g)
    for ax, vals in LATTICE_ME_V2.ordered.items():
        assert set(vals) == set(AXES_ME_V2[ax])


@pytest.mark.parametrize("day,first", [(date(2021, 1, 4), 1), (date(2021, 1, 5), 2), (date(2021, 2, 1), 1),
                                       (date(2021, 1, 19), 11), (date(2021, 1, 18), 0)])
def test_first_day_rank(day, first):
    assert month_end_rank([day], from_start=True)[0] == first
    assert independent_rank([day], from_start=True)[0] == first


def test_v2_trades_both_sides_of_the_turn():
    d = _data()
    p = _p(window=1, first_days=2, entry_min=hhmm_minutes("09:30"), exit_rule="16:00")
    s = simulate_month_end(d, p, exec_config=FUT, starting_equity=1e6)
    days = _trade_days(d, s)
    assert days[:5] == [date(2020, 11, 2), date(2020, 11, 3), date(2020, 11, 30), date(2020, 12, 1), date(2020, 12, 2)]
    assert date(2020, 12, 31) in days and date(2021, 1, 4) in days and date(2021, 1, 5) in days
    assert date(2021, 1, 6) not in days and date(2020, 12, 30) not in days
    assert check_sim_integrity(s, d, FUT, p) == []
    only_first = _p(window=0, first_days=1, entry_min=hhmm_minutes("10:00"), exit_rule="12:00")
    s2 = simulate_month_end(d, only_first, exec_config=FUT, starting_equity=1e6)
    assert all(d.rank_start[int(d.sess[e])] == 1 for e in s2.entry_idx)
    assert (d.tod[s2.exit_idx] == 12 * 60 - 1).all()
    with pytest.raises(ValueError):
        simulate_month_end(d, _p(window=0, first_days=0), exec_config=FUT, starting_equity=1e6)


def test_v2_integrity_on_grid_sample_and_truncation():
    d = _data(start=date(2020, 9, 1), end=date(2021, 6, 30), seed=4)
    for ce in me_grid_v2(("ES",))[::97]:
        s = simulate_month_end(d, ce.config, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, ce.config) == [], ce.config
    b = me_day_bars(_bars(start=date(2020, 9, 1), end=date(2021, 6, 30), seed=5))
    p = _p(window=2, first_days=3, entry_min=hhmm_minutes("13:00"), exit_rule="15:30", stop_pct=0.5)
    assert truncation_invariance(b, p, exec_config=FUT, cut_fracs=(0.3, 0.55, 0.8, 0.97)) == []


def test_v2_integrity_catches_first_days_violation():
    d = _data()
    p = _p(window=1, first_days=2, entry_min=hhmm_minutes("09:30"), exit_rule="16:00")
    s = simulate_month_end(d, p, exec_config=FUT, starting_equity=1e6)
    assert "day_not_eligible" in check_sim_integrity(s, d, FUT, replace(p, first_days=0))


def test_v2_local_moves_and_config():
    cfg = load_funnel_config(ROOT / "configs/funnel/me_funnel_es_v2.yaml")
    assert cfg.strategy == "month_end_v2" and cfg.symbol == "ES" and cfg.confidence.transfer_symbol == "NQ"
    lc = cfg.parameter_stability.local
    moves = dict(local_perturbations_me(_p(window=0, first_days=1, entry_min=hhmm_minutes("10:00")), lc))
    assert "window=1" in moves and "first_days=2" in moves and "first_days=0" not in moves
    moves2 = dict(local_perturbations_me(_p(window=2, first_days=1), lc))
    assert {"window=1", "window=3", "first_days=0", "first_days=2"} <= set(moves2)
    c = MonthEndV2Config(symbol="ES", window=0, first_days=3, entry="09:30", exit="16:00", stop="1.00")
    assert c.stop_pct_value == 1.0
    with pytest.raises(Exception):
        MonthEndV2Config(symbol="ES", entry="08:20")
