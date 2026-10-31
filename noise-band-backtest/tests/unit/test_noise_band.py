"""Noise-band breakout: band definition and causality, execution rules (next-open fills,
session-close exit, shorts, re-arming, stops), stress knobs, grid, lattice, local
perturbations and funnel plumbing."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import polars as pl
import pytest

from src.analysis.daily_performance import daily_equity
from src.analysis.neighborhood import LATTICE_NB_V1, neighbor_ids
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import FAMILIES, family_for
from src.experiments.funnel_robustness import local_perturbations_nb, perturbations_nb
from src.experiments.nb_grid import (AXES_V1, AXES_V2, AXES_V3, AXES_V4, nb_grid, nb_grid_v2, nb_grid_v3, nb_grid_v4,
                                    variants_per_symbol)
from src.experiments.nb_integrity import check_sim_integrity, truncation_invariance
from src.strategies.noise_band.backtest import NBData, NBParams, simulate_noise_band
from src.strategies.noise_band.config import NoiseBandConfig, NoiseBandV4Config
from src.utils.config_models import ExecutionConfig
from tests.unit.test_funnel_integrity import _bars

EC = ExecutionConfig()
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
P = NBParams("SPY", "15min", band_lookback=5, band_mult=1.0, check_minutes=30, anchor="open_prev_close",
             trail="band_vwap", direction="both")
CONFIGS = "configs/funnel"


def _walk(n_days=40, per_day=26, seed=0, drift=0.0):
    """Random-walk 15-min sessions (09:30-16:00 NY) with a session-level trend."""
    rng = np.random.default_rng(seed)
    days = []
    px = 100.0
    for _ in range(n_days):
        mu = drift + rng.normal(0, 0.15)  # trending days create breakouts both ways
        steps = rng.normal(mu, 0.3, per_day)
        days.append(list(px + np.cumsum(steps)))
        px = days[-1][-1] + rng.normal(0, 0.3)
    return _bars(days).with_columns(pl.lit(1000).alias("volume"))


def _sim(bars, p=P, ec=EC, **kw):
    data = NBData(bars)
    return data, simulate_noise_band(data, p, exec_config=ec, starting_equity=1e5, **kw)


def _p(**kw) -> NBParams:
    return NBParams(**{**P.__dict__, **kw})


# --- band definition and causality -----------------------------------------------------

def test_sigma_is_mean_move_at_same_time_over_previous_sessions():
    bars = _walk(seed=1)
    data = NBData(bars)
    sig = data.sigma(5)
    per_day = 26
    k = 20 * per_day + 7  # session 20, slot 7
    moves = [abs(data.close[d * per_day + 7] - data.open[d * per_day]) / data.open[d * per_day] for d in range(15, 20)]
    assert sig[k] == pytest.approx(np.mean(moves))
    assert np.isnan(sig[4 * per_day + 7]) and np.isfinite(sig[5 * per_day + 7])  # needs 5 prior sessions


def test_sigma_ignores_today_and_bands_follow_anchor():
    bars = _walk(seed=2)
    data = NBData(bars)
    # Poisoning today's closes must not change today's sigma.
    poisoned = bars.with_columns(pl.when(pl.col("session_date_ny") == bars["session_date_ny"][30 * 26])
                                 .then(pl.col("close") * 5).otherwise(pl.col("close")).alias("close"))
    assert np.allclose(NBData(poisoned).sigma(5)[30 * 26:31 * 26], data.sigma(5)[30 * 26:31 * 26])
    up, lo = data.bands(5, 1.0, "open")
    k = 30 * 26 + 5
    w = data.sigma(5)[k] * data.sess_open[k]
    assert up[k] == pytest.approx(data.sess_open[k] + w) and lo[k] == pytest.approx(data.sess_open[k] - w)
    up2, lo2 = data.bands(5, 1.0, "open_prev_close")
    pc = data.close[30 * 26 - 1]
    assert up2[k] == pytest.approx(max(data.sess_open[k], pc) + w)
    assert lo2[k] == pytest.approx(min(data.sess_open[k], pc) - w)


def test_check_bars_land_on_interval_from_open_and_vwap_resets_daily():
    data = NBData(_walk(seed=3))
    assert data.tf_minutes == 15 and data.open_minute == 9 * 60 + 30
    chk = data.check(30)
    assert list(np.flatnonzero(chk[:26])) == list(range(1, 26, 2))  # closes at 10:00, 10:30, ... 16:00
    assert data.check(15)[:26].all()
    k = 26  # first bar of session 1: VWAP is its typical price
    assert data.vwap[k] == pytest.approx((data.high[k] + data.low[k] + data.close[k]) / 3)


def test_no_lookahead_truncation_invariance():
    bars = _walk(seed=4)
    for p in (P, _p(direction="long", trail="band", stop_atr=1.0), _p(direction="short", trail="vwap",
              check_minutes=15, anchor="open"), _p(band_mult=0.5, band_lookback=3)):
        assert truncation_invariance(bars, p, exec_config=EC) == []


# --- execution rules -------------------------------------------------------------------

@pytest.mark.parametrize("seed", range(6))
def test_integrity_clean_and_nothing_held_overnight(seed):
    bars = _walk(seed=seed, n_days=60)
    for p in (P, _p(stop_atr=1.0), _p(direction="long", trail="vwap"), _p(direction="short", check_minutes=15),
              _p(band_mult=0.5, anchor="open", trail="band")):
        data, sim = _sim(bars, p)
        assert len(sim.entry_idx) > 0
        assert check_sim_integrity(sim, data, EC, p) == []
        assert np.all(data.sess[sim.exit_idx] == data.sess[sim.entry_idx])
        eod = sim.exit_reason == "eod_exit"
        assert np.all(sim.exit_idx[eod] == data.sess_end[sim.entry_idx[eod]])


def test_direction_filter_and_short_pnl_sign():
    bars = _walk(seed=5, n_days=60)
    for direction, want in (("long", {1}), ("short", {-1})):
        data, sim = _sim(bars, _p(direction=direction))
        assert set(sim.side.tolist()) <= want and len(sim.side)
    data, sim = _sim(bars, _p(direction="both"))
    assert {1, -1} <= set(sim.side.tolist())
    s = np.flatnonzero(sim.side < 0)[0]
    q = sim.quantity[s]
    assert sim.realized_pnl[s] == pytest.approx((sim.entry_px[s] - sim.exit_px[s]) * q - 2 * sim.entry_commission[s])


def _scripted(days: list[list[float]]) -> pl.DataFrame:
    return _bars(days, spread=0.05).with_columns(pl.lit(1000).alias("volume"))


def test_breakout_enters_next_open_and_trails_out_next_open():
    flat = [100.0 + 0.1 * ((i % 2) * 2 - 1) for i in range(26)]  # +-0.1 noise -> tiny sigma
    run = [100.0 + 0.1 * i for i in range(1, 8)] + [100.65, 100.2] + [100.0] * 17  # breaks out, then falls back
    bars = _scripted([flat] * 5 + [run])
    p = _p(band_lookback=5, trail="band", direction="long", anchor="open")
    data, sim = _sim(bars, p)
    t = 0
    assert len(sim.entry_idx) >= 1
    s, e, x = sim.signal_idx[t], sim.entry_idx[t], sim.exit_idx[t]
    assert data.check(30)[s] and e == s + 1 and data.sess[s] == 5
    assert sim.entry_px[t] == pytest.approx(data.open[e] * (1 + EC.slippage_bps_market / 1e4))
    assert sim.exit_reason[t] == "trail_exit" and x == sim.decision_idx[t] + 1
    assert data.close[sim.decision_idx[t]] < data.bands(5, 1.0, "open")[0][sim.decision_idx[t]]


def test_session_close_exit_at_last_close_and_final_session_forced():
    flat = [100.0 + 0.1 * ((i % 2) * 2 - 1) for i in range(26)]
    trend = [100.0 + 0.2 * i for i in range(1, 27)]  # never falls back: held to the close
    bars = _scripted([flat] * 5 + [trend] + [flat] + [trend])
    p = _p(band_lookback=5, trail="band", direction="long", anchor="open")
    data, sim = _sim(bars, p)
    assert sim.exit_reason[0] == "eod_exit" and sim.exit_idx[0] == data.sess_end[sim.entry_idx[0]]
    assert sim.exit_px[0] == pytest.approx(data.close[sim.exit_idx[0]] * (1 - EC.slippage_bps_market / 1e4))
    assert sim.exit_reason[-1] == "forced_close" and sim.forced_close[-1] and sim.exit_idx[-1] == data.n - 1


def test_same_direction_reentry_needs_rearm():
    """With a VWAP trail a long can exit while price is still above the band; it may not
    re-enter long until a check close is back inside the band."""
    bars = _walk(seed=7, n_days=80)
    p = _p(trail="vwap", direction="long")
    data, sim = _sim(bars, p)
    up, _ = data.bands(p.band_lookback, p.band_mult, p.anchor)
    chk = data.check(p.check_minutes)
    n_checked = 0
    for t in range(1, len(sim.entry_idx)):
        prev = t - 1
        if sim.exit_reason[prev] != "trail_exit" or data.sess[sim.signal_idx[t]] != data.sess[sim.decision_idx[prev]]:
            continue
        span = np.arange(sim.decision_idx[prev], sim.signal_idx[t] + 1)
        assert (chk[span] & ~(data.close[span] > up[span])).any()
        n_checked += 1
    assert n_checked > 0



@pytest.mark.parametrize("seed", [0, 3, 7])
def test_max_entries_per_session_caps_and_keeps_earliest_trades(seed):
    bars = _walk(n_days=60, seed=seed)
    data, free = _sim(bars, _p(check_minutes=15, trail="band"))
    per = np.unique(data.sess[free.entry_idx], return_counts=True)[1]
    assert per.max() > 1  # the fixture re-enters within a session
    _, same = _sim(bars, _p(check_minutes=15, trail="band", max_entries=int(per.max())))
    assert np.array_equal(same.entry_idx, free.entry_idx)  # a cap above the max changes nothing
    for cap in (1, 2):
        p = _p(check_minutes=15, trail="band", max_entries=cap)
        _, sim = _sim(bars, p)
        counts = dict(zip(*np.unique(data.sess[sim.entry_idx], return_counts=True)))
        assert max(counts.values()) <= cap
        assert check_sim_integrity(sim, data, EC, p) == []
        # Each session's first `cap` trades are the uncapped run's first `cap` trades.
        for sess in counts:
            first = free.entry_idx[data.sess[free.entry_idx] == sess][:cap]
            assert np.array_equal(sim.entry_idx[data.sess[sim.entry_idx] == sess], first)


def test_v4_grid_and_cap_mapping():
    g = nb_grid_v4(("ES",))
    assert variants_per_symbol(AXES_V4) == 13824 == len(g)
    assert {ce.config.max_entries_per_session for ce in g} == {1, 2, "none"}
    caps = {NBParams.from_config(ce.config).max_entries for ce in g}
    assert caps == {1, 2, None}
    assert NBParams.from_config(NoiseBandConfig(symbol="ES")).max_entries is None
    # Older configs hash exactly as before (no new field on the v1 model).
    assert "max_entries_per_session" not in NoiseBandConfig(symbol="ES").model_dump()
    one = NBParams.from_config(NoiseBandV4Config(symbol="ES", band_lookback=1))
    labels = [lab for lab, _ in local_perturbations_nb(one, SimpleNamespace(int_rel=0.2, band_mult_abs=0.25,
                                                                            stop_atr_abs=0.25))]
    assert labels == ["band_lookback=2", "band_mult=0.75", "band_mult=1.25"]

def test_stop_is_from_atr_before_entry_and_side_aware():
    bars = _walk(seed=8, n_days=60)
    p = _p(stop_atr=0.5)
    data, sim = _sim(bars, p)
    expect = data.open[sim.entry_idx] - sim.side * 0.5 * data.atr[sim.entry_idx - 1]
    assert np.allclose(sim.stop_level, expect)
    st = sim.exit_reason == "stop_exit"
    assert st.any() and (sim.side[st] < 0).any() and (sim.side[st] > 0).any()
    assert check_sim_integrity(sim, data, EC, p) == []


def test_first_entry_minutes_blocks_early_signals_only():
    bars = _walk(seed=12, n_days=60)
    data = NBData(bars)
    since_open = data.tod + data.tf_minutes - data.open_minute
    for fe in (15, 30, 60, 120):
        _, sim = _sim(bars, _p(check_minutes=15, first_entry_minutes=fe))
        assert len(sim.entry_idx) and since_open[sim.signal_idx].min() >= fe
    # Below the first check time the setting is a no-op (check 30: first entry 15 == 30).
    _, a = _sim(bars, _p(check_minutes=30, first_entry_minutes=15))
    _, b = _sim(bars, _p(check_minutes=30, first_entry_minutes=30))
    assert np.array_equal(a.entry_idx, b.entry_idx)


def test_stress_knobs_delay_and_missed_entries():
    bars = _walk(seed=9, n_days=60)
    data, base = _sim(bars)
    _, late = _sim(bars, entry_delay_bars=1)
    assert np.all(late.entry_idx == late.signal_idx + 2)
    assert np.all(data.sess[late.entry_idx] == data.sess[late.signal_idx])
    _, miss = _sim(bars, missed_entry_frac=0.5, stress_seed=3)
    assert 0 < len(miss.entry_idx) < len(base.entry_idx)
    assert check_sim_integrity(miss, data, EC, P) == []


def test_futures_costs_ticks_and_whole_contracts_for_shorts():
    bars = _walk(seed=10, n_days=60).with_columns(pl.lit("ES").alias("symbol"))
    p = _p(symbol="ES", direction="short")
    data, sim = _sim(bars, p, ec=FUT)
    assert len(sim.entry_idx) and np.allclose(sim.entry_px, data.open[sim.entry_idx] - 0.25)
    assert np.allclose(sim.quantity % 50, 0)


def test_daily_equity_marks_open_short_against_close():
    data = NBData(_walk(seed=11, n_days=3))
    e = data.day_end_idx
    sim = SimpleNamespace(entry_idx=np.array([5]), exit_idx=np.array([e[1]]), realized_pnl=np.array([0.0]),
                          quantity=np.array([10.0]), entry_px=np.array([data.close[5]]),
                          entry_commission=np.array([1.0]), side=np.array([-1]))
    eq = daily_equity(sim, data, 1000.0)
    assert eq[0] == pytest.approx(1000.0 - 10.0 * (data.close[e[0]] - data.close[5]) - 1.0)


# --- grid, lattice, perturbations, funnel plumbing --------------------------------------

def test_grid_size_and_config_mapping():
    assert variants_per_symbol(AXES_V1) == 8100 == len(nb_grid(("ES",)))
    p = NBParams.from_config(NoiseBandConfig(symbol="ES", band_mult=2.0, first_entry_minutes=60))
    assert (p.stop_atr, p.band_mult, p.first_entry_minutes) == (None, 2.0, 60)


def test_v2_grid_size_and_values():
    g = nb_grid_v2(("ES",))
    assert variants_per_symbol(AXES_V2) == 8100 == len(g)
    assert {ce.config.timeframe for ce in g} == {"5min"}
    assert sorted({ce.config.band_lookback for ce in g}) == [3, 5, 7, 10, 15, 25, 35, 45, 60, 80]
    assert sorted({ce.config.band_mult for ce in g}) == [0.25, 0.5, 0.75, 1.0, 1.25]



def test_v3_grid_is_v2_on_both_timeframes():
    g = nb_grid_v3(("ES",))
    assert variants_per_symbol(AXES_V3) == 16200 == len(g)
    assert {ce.config.timeframe for ce in g} == {"5min", "15min"}
    v2_ids = {ce.config_id for ce in nb_grid_v2(("ES",))}
    assert v2_ids <= {ce.config_id for ce in g}  # ids hash the settings, so the 5min half is v2

def test_lattice_neighbors_hold_categoricals():
    recs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in nb_grid(("ES",))]
    nb = neighbor_ids(recs, lattice=LATTICE_NB_V1)
    by = {r["config_id"]: r for r in recs}
    c = next(r for r in recs if r["band_lookback"] == 14 and r["band_mult"] == 1.0 and r["check_minutes"] == 30
             and r["first_entry_minutes"] == 30 and r["timeframe"] == "5min")
    ns = [by[i] for i in nb[c["config_id"]]]
    assert len(ns) == 2 * 5 - 1  # 5 ordered axes with >1 value; timeframe 5min is a boundary
    assert all((n["anchor"], n["trail"], n["direction"]) == (c["anchor"], c["trail"], c["direction"]) for n in ns)


def test_local_and_random_perturbations():
    lcfg = SimpleNamespace(int_rel=0.2, band_mult_abs=0.25, stop_atr_abs=0.25)
    moves = dict(local_perturbations_nb(_p(band_lookback=14, band_mult=1.0, stop_atr=1.0), lcfg))
    assert sorted(moves) == ["band_lookback=11", "band_lookback=17", "band_mult=0.75", "band_mult=1.25",
                             "stop_atr=0.75", "stop_atr=1.25"]
    assert len(local_perturbations_nb(_p(band_lookback=7), lcfg)) == 4  # no stop -> no stop moves
    assert dict(local_perturbations_nb(_p(band_lookback=7), lcfg))["band_lookback=6"].band_lookback == 6
    pc = SimpleNamespace(n_per_config=20, integer_rel_step=0.15, float_rel_step=0.1)
    ps = perturbations_nb(_p(band_lookback=14), config_id="x", base_seed=1, pcfg=pc)
    assert len(ps) == 20 and all(q.band_lookback != 14 and q.stop_atr is None for q in ps)
    assert all(q.check_minutes == 30 and q.trail == P.trail for q in ps)
    assert ps == perturbations_nb(_p(band_lookback=14), config_id="x", base_seed=1, pcfg=pc)


def test_market_configs_load_and_pick_the_noise_band_family():
    paths = sorted(Path(CONFIGS).glob("nb_funnel_*_v1.yaml"))
    assert {p.name.split("_")[2] for p in paths} >= {"es", "nq", "ym", "rty", "cl", "gc", "6e", "6j", "zn"}
    for path in paths:
        f = load_funnel_config(path)
        assert f.strategy == "noise_band" and family_for(f) is FAMILIES["noise_band"]
        assert f.parameter_stability.mode == "local_perturbation" and f.parameter_stability.local.band_mult_abs
        assert f.data.timeframes == ["5min", "15min"]
