"""FVG after displacement: a hand-built gap traded with it (limit) and against it (stop order) and
at market, the window / midnight / VWAP / displacement filters, stops, targets and the hold exit,
the independent integrity check on many configs (and that it catches tampered trades), look-ahead
truncation, the grid / lattice / local moves and the market config."""

from __future__ import annotations

import itertools
from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_FV_V1
from src.data.calendars import TradingCalendar
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_robustness import local_perturbations_fv, perturbations_fv
from src.experiments.fv_grid import AXES_FV_V1, fv_grid_v1
from src.experiments.fv_integrity import check_sim_integrity, independent_plan, truncation_invariance
from src.strategies.fvg.backtest import (
    STOP_EXIT,
    TARGET_EXIT,
    TIME_EXIT,
    FVData,
    FVParams,
    fv_bars,
    planned_trades,
    simulate_fvg,
)
from src.strategies.fvg.config import FvgV1Config
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.25
CAL = TradingCalendar()
P = FVParams("NQ", "1min", window="rth", mode="with", disp=1.5, fvg_min=0.0, vwap=False, entry="prox", wait=15,
             stop_kind="struct", stop_mult=None, target_r=2.0, hold=30)
CFG = load_funnel_config(ROOT / "configs/funnel/fv_funnel_nq_v1.yaml")


def _p(**kw) -> FVParams:
    return replace(P, **kw)


def _row(ny: datetime, d: date, o, h, lo, c, v=100) -> dict:
    return {"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
            "open": float(o), "high": float(h), "low": float(lo), "close": float(c), "volume": v,
            "price_adjustment": 0.0}


def _frame(rows) -> pl.DataFrame:
    return pl.DataFrame(rows).with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _session_minutes(d: date):
    prev = d - timedelta(days=1)
    for t in range(18 * 60, 24 * 60):
        yield datetime(prev.year, prev.month, prev.day, t // 60, t % 60, tzinfo=NY)
    for t in range(0, 17 * 60):
        yield datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)


def _random_bars(start=date(2021, 1, 4), end=date(2021, 3, 31), seed=0, vol=2.0) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    rows, px = [], 13000.0
    for d in CAL.trading_days(start, end):
        for ny in _session_minutes(d):
            m = ny.hour * 60 + ny.minute
            v = vol * (2.5 if 570 <= m < 960 else 1.0)
            o = px
            jump = float(rng.normal(0, 6 * v)) if rng.random() < 0.04 else 0.0
            c = round((px + float(rng.normal(0, v)) + jump) / TICK) * TICK
            wh = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            wl = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            rows.append(_row(ny, d, o, max(o, c) + wh, min(o, c) - wl, c, int(rng.integers(50, 500))))
            px = c
    return _frame(rows)


FLAT = (100, 100.5, 99.5, 100)
GAP = {  # last session: bullish gap 10:05-10:07 = [100.5, 102], retrace 10:08
    "10:06": (100, 103.0, 100.0, 103.0),
    "10:07": (103, 104.0, 102.0, 103.5),
    "10:08": (103, 103.0, 101.5, 102.0),
}


def _flat_bars(special=None, n_days: int = 3) -> pl.DataFrame:
    days = CAL.trading_days(date(2021, 3, 1), date(2021, 3, 31))[:n_days]
    rows = []
    for k, d in enumerate(days):
        for ny in _session_minutes(d):
            key = f"{ny.hour:02d}:{ny.minute:02d}"
            bar = special[key] if (k == len(days) - 1 and special and key in special and ny.date() == d) else FLAT
            rows.append(_row(ny, d, *bar))
    return _frame(rows)


@pytest.fixture(scope="module")
def gap_data() -> FVData:
    return FVData(fv_bars(_flat_bars(GAP)))


@pytest.fixture(scope="module")
def rand_data() -> FVData:
    return FVData(fv_bars(_random_bars()))


def _idx(data, hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    last = data.day_start_idx[-1]
    return int(last + np.flatnonzero(data.tod[last:] == h * 60 + m)[0])


def _sim(d, p):
    return simulate_fvg(d, p, exec_config=FUT, starting_equity=1e6)


def test_with_limit_struct_2r_hold(gap_data):
    d = gap_data
    s = _sim(d, P)
    assert len(s.entry_idx) == 1 and s.side[0] == 1
    assert (s.signal_idx[0], s.entry_idx[0]) == (_idx(d, "10:07"), _idx(d, "10:08"))
    assert s.entry_base[0] == 102.0 and s.entry_px[0] == 102.0          # limit, open 103 above
    atr = d.atr[_idx(d, "10:05")]
    dist = max(102.0 - (99.5 - 2 * TICK), atr)                           # three bars' low 99.5 (flat 10:05)
    assert s.stop_level[0] == pytest.approx(102.0 - dist)
    assert s.target_level[0] == pytest.approx(102.0 + 2 * dist)
    assert s.exit_reason[0] == TIME_EXIT and s.exit_idx[0] == _idx(d, "10:37")  # 30 minutes from 10:08
    assert check_sim_integrity(s, d, FUT, P) == []


def test_against_is_a_stop_order_short(gap_data):
    d = gap_data
    p = _p(mode="against")
    s = _sim(d, p)
    assert len(s.entry_idx) == 1 and s.side[0] == -1 and s.entry_idx[0] == _idx(d, "10:08")
    assert s.entry_px[0] == pytest.approx(102.0 - TICK)                 # touch, filled at level, stop slippage
    assert s.stop_level[0] == pytest.approx(102.0 + max(104.0 + 2 * TICK - 102.0, d.atr[_idx(d, "10:05")]))
    assert check_sim_integrity(s, d, FUT, p) == []


def test_mkt_entry_and_atr_stop(gap_data):
    d = gap_data
    p = _p(entry="mkt", wait=0, stop_kind="atr", stop_mult=3.0, target_r=None)
    s = _sim(d, p)
    assert s.entry_idx[0] == _idx(d, "10:08") and s.entry_px[0] == 103.0 + TICK
    atr = d.atr[_idx(d, "10:05")]
    assert s.entry_base[0] == 103.0 and s.stop_level[0] == pytest.approx(103.0 - 3.0 * atr)
    assert np.isnan(s.target_level[0])
    assert check_sim_integrity(s, d, FUT, p) == []


def test_filters(gap_data):
    d = gap_data
    assert len(_sim(d, _p(window="pm")).entry_idx) == 0
    assert len(_sim(d, _p(window="am")).entry_idx) == 1
    assert len(_sim(d, _p(disp=10.0)).entry_idx) == 0                   # middle bar's true range is 3
    assert len(_sim(d, _p(fvg_min=50.0)).entry_idx) == 0
    # flat volume: VWAP ~ 100; bar 3 closes at 103.5 above it -> a long passes, a short does not
    assert len(_sim(d, _p(vwap=True)).entry_idx) == 1
    assert len(_sim(d, _p(vwap=True, mode="against")).entry_idx) == 0


def test_gap_across_midnight_is_not_a_setup():
    special = {"23:59": (100, 100.5, 99.5, 100), "00:00": (100, 103, 100, 103), "00:01": (103, 104, 102, 103.5)}
    days = CAL.trading_days(date(2021, 3, 1), date(2021, 3, 31))[:3]
    rows = []
    for k, dd in enumerate(days):
        for ny in _session_minutes(dd):
            key = f"{ny.hour:02d}:{ny.minute:02d}"
            rows.append(_row(ny, dd, *(special.get(key, FLAT) if k == 2 else FLAT)))
    d = FVData(fv_bars(_frame(rows)))
    assert len(_sim(d, _p(entry="mkt", wait=0)).entry_idx) == 0
    assert independent_plan(d, _p(entry="mkt", wait=0), TICK) == []


def test_stop_first_target_trade_through_and_limit_through():
    d = FVData(fv_bars(_flat_bars({**GAP, "10:09": (102, 200.0, 50.0, 100)})))
    s = _sim(d, P)
    assert s.exit_reason[0] == STOP_EXIT and s.exit_idx[0] == _idx(d, "10:09")
    tgt = float(_sim(FVData(fv_bars(_flat_bars(GAP))), P).target_level[0])
    d2 = FVData(fv_bars(_flat_bars({**GAP, "10:09": (102, tgt, 101, 102), "10:10": (102, tgt + TICK, 101, 102)})))
    s2 = _sim(d2, P)
    assert s2.exit_reason[0] == TARGET_EXIT and s2.exit_idx[0] == _idx(d2, "10:10") and s2.exit_px[0] == tgt
    d3 = FVData(fv_bars(_flat_bars({**GAP, "10:08": (103, 103.0, 102.0, 102.5)})))   # touches, not through
    assert _sim(d3, P).entry_idx[0] > _idx(d3, "10:08")
    for ss, dd in ((s, d), (s2, d2)):
        assert check_sim_integrity(ss, dd, FUT, P) == []


@pytest.mark.parametrize("window,mode", [("rth", "with"), ("rth", "against"), ("am", "with"), ("pm", "against")])
def test_integrity_clean_on_random_data(rand_data, window, mode):
    n = 0
    for entry, stop, tgt, vw in itertools.product(["prox", "ce", "mkt"], ["struct", "a1.5"], ["1R", "none"], ["off", "on"]):
        cfg = FvgV1Config(symbol="NQ", window=window, mode=mode, disp="1.0", entry=entry,
                          wait=0 if entry == "mkt" else 15, stop=stop, target=tgt, vwap=vw, hold=30)
        s = _sim(rand_data, cfg)
        assert check_sim_integrity(s, rand_data, FUT, cfg) == []
        n += len(s.entry_idx)
    assert n >= 100


def test_integrity_catches_tampering(rand_data):
    p = _p(disp=1.0)
    s = _sim(rand_data, p)
    assert len(s.entry_idx) >= 5
    assert "stop_not_per_rule" in check_sim_integrity(replace(s, stop_level=s.stop_level + 1.0), rand_data, FUT, p)
    assert "entry_fill_better_than_rule" in check_sim_integrity(
        replace(s, entry_px=s.entry_px - s.side * 1.0), rand_data, FUT, p)
    assert "entry_not_per_rule" in check_sim_integrity(replace(s, entry_idx=s.entry_idx + 1), rand_data, FUT, p)
    keep = np.arange(len(s.entry_idx)) != 2
    dropped = replace(s, **{f: getattr(s, f)[keep] for f in (
        "signal_idx", "entry_idx", "exit_idx", "decision_idx", "quantity", "entry_px", "exit_px",
        "entry_commission", "realized_pnl", "forced_close", "exit_reason", "entry_base", "side",
        "stop_level", "target_level")})
    assert "trade_skipped_while_flat" in check_sim_integrity(dropped, rand_data, FUT, p)


def test_independent_plan_matches(rand_data):
    for p in (_p(disp=1.0, mode="against", entry="ce"), _p(disp=1.0, entry="mkt", wait=0, vwap=True)):
        a = planned_trades(rand_data, p, TICK)
        b = independent_plan(rand_data, p, TICK)
        assert [int(x) for x in a["e"]] == [t[1] for t in b] and len(b) > 5


def test_truncation_invariance():
    bars = fv_bars(_random_bars(end=date(2021, 2, 12), seed=3))
    for p in (_p(disp=1.0), _p(disp=1.0, mode="against", entry="mkt", wait=0, hold=60)):
        assert truncation_invariance(bars, p, exec_config=FUT) == []


def test_grid_lattice_and_moves():
    grid = fv_grid_v1(("NQ",))
    assert len(grid) == 24192 and len({g.config_id for g in grid}) == 24192
    assert all((g.config.entry == "mkt") == (g.config.wait == 0) for g in grid)
    assert set(LATTICE_FV_V1.fixed) == {"symbol", "window", "mode", "vwap", "entry"}
    assert "wait" in AXES_FV_V1
    lcfg = CFG.parameter_stability.local
    labels = [m for m, _ in local_perturbations_fv(_p(stop_kind="atr", stop_mult=1.5), lcfg)]
    assert labels == ["disp=1.25", "disp=1.75", "fvg_min=0.25", "wait=10", "wait=20", "stop=a1", "stop=a2",
                      "target=1.5R", "target=2.5R", "hold=25", "hold=35"]
    mk = [m for m, _ in local_perturbations_fv(_p(entry="mkt", wait=0, target_r=None), lcfg)]
    assert not any(m.startswith(("wait", "target", "stop")) for m in mk)
    ps = perturbations_fv(P, config_id="x", base_seed=1, pcfg=CFG.parameter_stability.perturbation)
    assert len(ps) == CFG.parameter_stability.perturbation.n_per_config
    assert all(q.window == P.window and q.mode == P.mode and q.entry == P.entry for q in ps)


def test_market_config():
    assert CFG.strategy == "fvg_v1" and CFG.symbol == "NQ" and CFG.confidence.transfer_symbol == "ES"
