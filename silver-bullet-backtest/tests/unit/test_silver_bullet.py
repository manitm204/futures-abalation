"""Silver Bullet: session bars, a hand-built sweep -> FVG -> limit fill, the stop / target / window
rules, the sweep and liquidity-target requirements, the independent integrity check on many
configs (and that it catches tampered trades), look-ahead truncation, the grid / lattice / local
moves and the market config."""

from __future__ import annotations

import itertools
from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_SB_V1
from src.data.calendars import TradingCalendar
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_robustness import local_perturbations_sb, perturbations_sb
from src.experiments.sb_grid import AXES_SB_V1, sb_grid_v1
from src.experiments.sb_integrity import check_sim_integrity, independent_plan, truncation_invariance
from src.strategies.silver_bullet.backtest import (
    STOP_EXIT,
    TARGET_EXIT,
    TIME_EXIT,
    SBData,
    SBParams,
    planned_trades,
    sb_bars,
    set_tick,
    simulate_silver_bullet,
)
from src.strategies.silver_bullet.config import SilverBulletV1Config
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.25
CAL = TradingCalendar()
P = SBParams("NQ", "1min", window="10-11", fvg_min=0.0, disp=1.5, entry="prox", stop="struct",
             target_kind="r", target_r=2.0, sweep=True)


def _p(**kw) -> SBParams:
    return replace(P, **kw)


def _row(ny: datetime, d: date, o, h, lo, c) -> dict:
    return {"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
            "open": float(o), "high": float(h), "low": float(lo), "close": float(c), "volume": 100,
            "price_adjustment": 0.0}


def _frame(rows) -> pl.DataFrame:
    return pl.DataFrame(rows).with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _session_minutes(d: date):
    """(NY datetime) for every Globex minute of session d: 18:00 the evening before .. 16:59."""
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
            jump = float(rng.normal(0, 6 * v)) if rng.random() < 0.04 else 0.0  # displacement bars
            c = round((px + float(rng.normal(0, v)) + jump) / TICK) * TICK
            wh = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            wl = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            rows.append(_row(ny, d, o, max(o, c) + wh, min(o, c) - wl, c))
            px = c
    return _frame(rows)


FLAT = (100, 100.5, 99.5, 100)
SETUP = {  # last session: swing low 09:50, sweep 10:00, bullish FVG 10:05-10:07, fill 10:08
    "09:50": (100, 100.5, 98.0, 100),
    "10:00": (100, 100.0, 97.0, 98.5),
    "10:06": (100, 103.0, 100.0, 103.0),
    "10:07": (103, 104.0, 102.0, 103.5),
    "10:08": (103, 103.0, 101.5, 102.0),
}


def _flat_bars(special: dict[str, tuple] | None = None, n_days: int = 3) -> pl.DataFrame:
    days = CAL.trading_days(date(2021, 3, 1), date(2021, 3, 31))[:n_days]
    rows = []
    for k, d in enumerate(days):
        for ny in _session_minutes(d):
            key = f"{ny.hour:02d}:{ny.minute:02d}"
            bar = special[key] if (k == len(days) - 1 and special and key in special
                                   and ny.date() == d) else FLAT
            rows.append(_row(ny, d, *bar))
    return _frame(rows)


@pytest.fixture(scope="module")
def setup_data() -> SBData:
    return SBData(sb_bars(_flat_bars(SETUP)))


@pytest.fixture(scope="module")
def rand_data() -> SBData:
    return SBData(sb_bars(_random_bars()))


def _idx(data: SBData, hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    last = data.day_start_idx[-1]
    return int(last + np.flatnonzero(data.tod[last:] == h * 60 + m)[0])


def test_sb_bars_keep_evening_and_day_to_16(setup_data):
    d = setup_data
    tods = set(d.tod.tolist())
    assert 18 * 60 in tods and 15 * 60 + 59 in tods
    assert not any(16 * 60 <= t < 18 * 60 for t in tods)
    s = d.day_start_idx[-1]
    assert d.tod[s] == 18 * 60  # a session starts with the evening before


def test_hand_built_long_struct_2r(setup_data):
    d = setup_data
    sim = simulate_silver_bullet(d, P, exec_config=FUT, starting_equity=1e6)
    assert len(sim.entry_idx) == 1
    m, e, x = int(sim.signal_idx[0]), int(sim.entry_idx[0]), int(sim.exit_idx[0])
    assert (m, e, x) == (_idx(d, "10:07"), _idx(d, "10:08"), _idx(d, "10:59"))
    assert sim.side[0] == 1 and sim.entry_base[0] == 102.0 and sim.entry_px[0] == 102.0  # limit, open 103 above
    assert sim.stop_level[0] == pytest.approx(97.0 - 2 * TICK)  # swept extreme - 2 ticks
    assert sim.target_level[0] == pytest.approx(102.0 + 2 * (102.0 - 96.5))
    assert sim.exit_reason[0] == TIME_EXIT and sim.exit_px[0] == pytest.approx(100.0 - TICK)
    assert check_sim_integrity(sim, d, FUT, P) == []


def test_ce_entry_fvg_stop_and_atr_floor(setup_data):
    d = setup_data
    p = _p(entry="ce", stop="fvg", target_kind="none", target_r=None)
    sim = simulate_silver_bullet(d, p, exec_config=FUT, starting_equity=1e6)
    lim = (100.5 + 102.0) / 2
    # 10:08's low (101.5) does not trade through the midpoint; 10:09 opens below it -> filled at its open
    assert sim.entry_base[0] == lim and sim.entry_idx[0] == _idx(d, "10:09") and sim.entry_px[0] == 100.0
    atr = d.atr[_idx(d, "10:05")]
    raw = lim - (100.5 - 2 * TICK)
    assert sim.stop_level[0] == pytest.approx(lim - max(raw, atr))
    assert np.isnan(sim.target_level[0])
    assert check_sim_integrity(sim, d, FUT, p) == []


def test_sweep_requirement_and_liquidity_target_skip(setup_data):
    d = setup_data
    # no swing high above the limit in the session -> liq target skips the only setup
    sim = simulate_silver_bullet(d, _p(target_kind="liq", target_r=None), exec_config=FUT, starting_equity=1e6)
    assert len(sim.entry_idx) == 0
    # without the sweep bar, sweep=yes finds nothing but sweep=no still trades
    nd = SBData(sb_bars(_flat_bars({k: v for k, v in SETUP.items() if k not in ("09:50", "10:00")})))
    assert len(simulate_silver_bullet(nd, P, exec_config=FUT, starting_equity=1e6).entry_idx) == 0
    sim2 = simulate_silver_bullet(nd, _p(sweep=False), exec_config=FUT, starting_equity=1e6)
    assert len(sim2.entry_idx) == 1
    # struct stop without a sweep: the 10 bars ending at bar 1 (all flat lows 99.5)
    assert sim2.stop_level[0] == pytest.approx(102.0 - max(102.0 - (99.5 - 2 * TICK), nd.atr[_idx(nd, "10:05")]))


def test_window_and_displacement_filters(setup_data):
    d = setup_data
    for w in ("14-15", "03-04", "p11-12", "p1230-1330"):
        assert len(simulate_silver_bullet(d, _p(window=w), exec_config=FUT, starting_equity=1e6).entry_idx) == 0
    assert len(simulate_silver_bullet(d, _p(window="kz"), exec_config=FUT, starting_equity=1e6).entry_idx) == 1
    big = _p(disp=10.0)  # the middle bar's true range is 3 points
    assert len(simulate_silver_bullet(d, big, exec_config=FUT, starting_equity=1e6).entry_idx) == 0
    assert len(simulate_silver_bullet(d, _p(fvg_min=50.0), exec_config=FUT, starting_equity=1e6).entry_idx) == 0


def test_stop_first_and_target_trade_through():
    # after the fill, a bar reaching both the stop and the target is a stop
    both = {**SETUP, "10:09": (102, 200.0, 90.0, 100)}
    d = SBData(sb_bars(_flat_bars(both)))
    sim = simulate_silver_bullet(d, P, exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] == STOP_EXIT and sim.exit_idx[0] == _idx(d, "10:09")
    # a target touched exactly does not fill; one tick through does, at the target
    tgt = 102.0 + 2 * 5.5
    d2 = SBData(sb_bars(_flat_bars({**SETUP, "10:09": (102, tgt, 101, 102), "10:10": (102, tgt + TICK, 101, 102)})))
    s2 = simulate_silver_bullet(d2, P, exec_config=FUT, starting_equity=1e6)
    assert s2.exit_reason[0] == TARGET_EXIT and s2.exit_idx[0] == _idx(d2, "10:10") and s2.exit_px[0] == tgt
    for s, dd in ((sim, d), (s2, d2)):
        assert check_sim_integrity(s, dd, FUT, P) == []


def test_limit_needs_trade_through():
    d = SBData(sb_bars(_flat_bars({**SETUP, "10:08": (103, 103.0, 102.0, 102.5)})))  # touches 102, not through
    sim = simulate_silver_bullet(d, P, exec_config=FUT, starting_equity=1e6)
    assert len(sim.entry_idx) == 1 and sim.entry_idx[0] > _idx(d, "10:08")  # filled later (flat bars go to 99.5)


@pytest.mark.parametrize("window", ["10-11", "kz", "03-04", "p1230-1330"])
def test_integrity_clean_on_random_data(rand_data, window):
    n_trades = 0
    for sw, tg, st, en in itertools.product(["yes", "no"], ["2R", "liq", "none"], ["fvg", "struct"], ["prox", "ce"]):
        cfg = SilverBulletV1Config(symbol="NQ", window=window, sweep=sw, target=tg, stop=st, entry=en,
                                   fvg_min="0.0", disp="1.0")
        sim = simulate_silver_bullet(rand_data, cfg, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(sim, rand_data, FUT, cfg) == []
        n_trades += len(sim.entry_idx)
    assert n_trades >= 50
    # the grid-fixed choices moved by stage 4 are audited too
    for kw in ({"swing": 4}, {"swing": 6}, {"max_age": 20}, {"max_age": 40}):
        p = _p(window=window, disp=1.0, sweep=False, **kw)
        sim = simulate_silver_bullet(rand_data, p, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(sim, rand_data, FUT, p) == []


def test_integrity_catches_tampering(rand_data):
    p = _p(window="kz", disp=1.0, sweep=False)
    sim = simulate_silver_bullet(rand_data, p, exec_config=FUT, starting_equity=1e6)
    assert len(sim.entry_idx) >= 5
    bad = replace(sim, stop_level=sim.stop_level + 1.0)
    assert "stop_not_per_rule" in check_sim_integrity(bad, rand_data, FUT, p)
    bad = replace(sim, entry_px=sim.entry_px - sim.side * 1.0)
    assert "entry_fill_better_than_rule" in check_sim_integrity(bad, rand_data, FUT, p)
    bad = replace(sim, entry_idx=sim.entry_idx + 1)
    assert "entry_not_per_rule" in check_sim_integrity(bad, rand_data, FUT, p)
    keep = np.arange(len(sim.entry_idx)) != 2
    dropped = replace(sim, **{f: getattr(sim, f)[keep] for f in (
        "signal_idx", "entry_idx", "exit_idx", "decision_idx", "quantity", "entry_px", "exit_px",
        "entry_commission", "realized_pnl", "forced_close", "exit_reason", "entry_base", "side",
        "stop_level", "target_level")})
    assert "trade_skipped_while_flat" in check_sim_integrity(dropped, rand_data, FUT, p)


def test_independent_plan_matches_planned_trades(rand_data):
    set_tick(rand_data, FUT, "NQ")
    for p in (_p(window="kz", disp=1.0, sweep=False), _p(window="03-04", disp=1.0, target_kind="liq", target_r=None)):
        a = planned_trades(rand_data, p)
        b = independent_plan(rand_data, p, TICK)
        assert [int(x) for x in a["m"]] == [t[0] for t in b]
        assert [int(x) for x in a["e"]] == [t[1] for t in b]


def test_truncation_invariance():
    bars = sb_bars(_random_bars(end=date(2021, 2, 12), seed=3))
    for p in (_p(window="kz", disp=1.0, sweep=False, target_kind="liq", target_r=None), _p(window="10-11", disp=1.0)):
        assert truncation_invariance(bars, p, exec_config=FUT) == []


def test_grid_lattice_and_moves():
    grid = sb_grid_v1(("NQ",))
    assert len(grid) == 1728 == np.prod([len(v) for v in AXES_SB_V1.values()])
    assert len({g.config_id for g in grid}) == 1728
    assert set(LATTICE_SB_V1.fixed) == {"symbol", "window", "sweep"}
    lcfg = load_funnel_config(ROOT / "configs/funnel/sb_funnel_nq_v1.yaml").parameter_stability.local
    labels = [m for m, _ in local_perturbations_sb(P, lcfg)]
    assert labels == ["fvg_min=0.25", "disp=1.25", "disp=1.75", "target=1.5R", "target=2.5R",
                      "swing=4", "swing=6", "max_age=20", "max_age=40"]
    liq = _p(target_kind="liq", target_r=None)
    assert not any(m.startswith("target") for m, _ in local_perturbations_sb(liq, lcfg))
    pc = load_funnel_config(ROOT / "configs/funnel/sb_funnel_nq_v1.yaml").parameter_stability.perturbation
    ps = perturbations_sb(P, config_id="x", base_seed=1, pcfg=pc)
    assert len(ps) == pc.n_per_config and all(q.window == P.window and q.sweep == P.sweep for q in ps)


def test_market_config():
    f = load_funnel_config(ROOT / "configs/funnel/sb_funnel_nq_v1.yaml")
    assert f.strategy == "silver_bullet_v1" and f.symbol == "NQ" and f.confidence.transfer_symbol == "ES"
