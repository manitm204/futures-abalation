"""EMRT two-leg spread: grid, important extrema / EMRT, hedge fits, the pair simulator and its
integrity checks."""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_EMRT_V1
from src.experiments.emrt_grid import AXES_EMRT_V1, emrt_grid_v1
from src.experiments.emrt_integrity import check_sim_integrity, truncation_invariance
from src.experiments.funnel_config import LocalPerturbationCfg, PerturbationCfg
from src.experiments.funnel_robustness import local_perturbations_emrt, perturbations_emrt
from src.strategies.emrt_spread.backtest import (
    PairData,
    as_params,
    pair_daily_equity,
    pair_frame,
    simulate_emrt_spread,
    size_pair,
)
from src.strategies.emrt_spread.config import EMRTV1Config, hedge_c, hedge_name, rolling_window, split_pair
from src.strategies.emrt_spread.hedge import emrt, fit_formation, month_keys, zigzag_pivots
from src.utils.config_models import ExecutionConfig

EC = ExecutionConfig(starting_equity=10_000_000.0, instrument_type="futures", commission_per_contract=2.5,
                     slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                     commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)


# ---- synthetic pair ------------------------------------------------------------------------

def _leg_bars(ts, px, adj=None):
    n = len(px)
    adj = np.zeros(n) if adj is None else adj
    rng = np.random.default_rng(7)
    o = px + rng.normal(0, 0.05, n)
    return o, np.maximum(o, px) + 0.1, np.minimum(o, px) - 0.1, px, adj


def make_pair(days: int = 260, bars_per_day: int = 7, seed: int = 0, roll_day: int | None = None) -> pl.DataFrame:
    """1h-style bars on weekdays from 2018-01-02 (13:30 UTC open), leg A ~ ES, leg B ~ NQ, with a
    mean-reverting spread; optional roll (price_adjustment step) in leg A at `roll_day`."""
    rng = np.random.default_rng(seed)
    ts, sd = [], []
    d = datetime(2018, 1, 2, tzinfo=timezone.utc)
    while len(sd) < days * bars_per_day:
        if d.weekday() < 5:
            for i in range(bars_per_day):
                ts.append(d.replace(hour=14, minute=30) + timedelta(hours=i))
                sd.append(d.date())
        d += timedelta(days=1)
    n = len(ts)
    b = 7000 * np.exp(np.cumsum(rng.normal(0, 0.002, n)))
    ou = np.zeros(n)
    for t in range(1, n):
        ou[t] = 0.9 * ou[t - 1] + rng.normal(0, 0.0015)
    a = 3000 * (1 + 0.8 * (b / b[0] - 1) + ou)
    adjA = np.zeros(n)
    if roll_day is not None:
        adjA[: roll_day * bars_per_day] = 12.0  # bars before the roll are shifted (adjusted = raw + adj)
    oa, ha, la, ca, _ = _leg_bars(ts, a)
    ob, hb, lb, cb, adjB = _leg_bars(ts, b)
    tsa = pl.Series(ts).dt.cast_time_unit("us")
    common = {"bar_open_ts": tsa, "bar_close_ts": tsa + timedelta(hours=1),
              "bar_open_ts_ny": tsa.dt.convert_time_zone("America/New_York"),
              "session_date_ny": pl.Series(sd), "timeframe": ["1h"] * n}
    A = pl.DataFrame({**common, "open": oa, "high": ha, "low": la, "close": ca, "price_adjustment": adjA,
                      "volume": np.ones(n, dtype=np.int64)})
    B = pl.DataFrame({"bar_open_ts": tsa, "session_date_ny": pl.Series(sd), "open": ob, "high": hb, "low": lb,
                      "close": cb, "price_adjustment": adjB, "volume": np.ones(n, dtype=np.int64)})
    return pair_frame(A, B, "ES-NQ")


@pytest.fixture(scope="module")
def pair() -> PairData:
    return PairData(make_pair())


@pytest.fixture(scope="module")
def pair_frame_df() -> pl.DataFrame:
    return make_pair()


def cfg(**kw) -> EMRTV1Config:
    base = dict(symbol="ES-NQ", timeframe="1h", formation=3, hedge="emrt_c2.0", z_mode="formation", entry_z=1.5,
                exit="mean", stop="none", time_stop="none", side="both", overnight="hold")
    return EMRTV1Config(**{**base, **kw})


# ---- grid ----------------------------------------------------------------------------------

def test_grid_size_and_lattice():
    g = emrt_grid_v1(("ES-NQ",))
    assert len(g) == 51_840
    assert len({ce.config_id for ce in g}) == 51_840
    for ax, vals in LATTICE_EMRT_V1.ordered.items():
        assert sorted(map(str, vals)) == sorted(map(str, AXES_EMRT_V1[ax])), ax
    assert set(LATTICE_EMRT_V1.ordered) | set(LATTICE_EMRT_V1.fixed) == {"symbol", *AXES_EMRT_V1}


def test_names():
    assert hedge_c("emrt_c2.0") == 2.0 and hedge_c("ols") is None and hedge_c("notional") is None
    assert hedge_name(2.0) == "emrt_c2.0" and hedge_name(1.75) == "emrt_c1.75"
    assert rolling_window("formation") is None and rolling_window("rolling_250") == 250
    assert split_pair("ES-NQ") == ("ES", "NQ")
    with pytest.raises(ValueError):
        split_pair("ESNQ")
    with pytest.raises(ValueError):
        hedge_c("kalman")


# ---- important extrema / EMRT --------------------------------------------------------------

def test_zigzag_known_sequence():
    x = np.array([0, 1, 3, 1, -2, -1, 2, 4, 3, 0, -3, -1, 2.0])
    # min at 0 (first pivot, dropped), max 2, min 4, max 7, min 10; the final rise is unconfirmed
    assert np.flatnonzero(zigzag_pivots(x[None], np.array([2.5]))[0]).tolist() == [2, 4, 7, 10]


def _reference_important(x: np.ndarray, R: float) -> set[int]:
    """Definition: i is an important min if, scanning each way before a lower value appears, a value
    >= x_i + R is reached on BOTH sides (max likewise)."""
    out = set()
    for i in range(1, len(x) - 1):
        for sgn in (1, -1):  # 1: minimum, -1: maximum
            y = sgn * x
            ok = True
            for rng_ in (range(i - 1, -1, -1), range(i + 1, len(x))):
                hit = False
                for j in rng_:
                    if y[j] < y[i]:
                        break
                    if y[j] >= y[i] + R:
                        hit = True
                        break
                ok &= hit
            if ok:
                out.add(i)
    return out


@pytest.mark.parametrize("seed", range(8))
def test_zigzag_matches_definition(seed):
    rng = np.random.default_rng(seed)
    x = np.cumsum(rng.normal(0, 1, 120))
    R = 2.0 * x.std()
    zz = set(np.flatnonzero(zigzag_pivots(x[None], np.array([R]))[0]).tolist())
    ref = _reference_important(x, R)
    assert zz <= ref
    assert len(ref - zz) <= 1  # only the first pivot (no full move before it) may be dropped


def test_emrt_hand_example():
    # mean 0; pivots (after the dropped first) at 2 (max, back below mean at 4) and 5 (min, back at 7)
    x = np.array([0, 2, 3, 1, -1, -3, -1, 1, 3, 1, -1, -3, -2, 0.5, 2.0])
    x = x - x.mean()
    e, n, mu, sd = emrt(x[None], [0.5 / x.std()])  # R = 0.5
    P = np.flatnonzero(zigzag_pivots(x[None], np.array([0.5]))[0])
    D = x - x.mean()
    times = []
    for i in P:
        j = next((j for j in range(i + 1, len(x)) if np.sign(D[j]) != np.sign(D[i]) or D[j] == 0), len(x))
        times.append(j - i)
    assert n[0, 0] == len(P) >= 4
    assert e[0, 0] == pytest.approx(np.mean(times))


def test_emrt_needs_min_pivots():
    e, n, _, _ = emrt(np.linspace(0, 1, 50)[None], [2.0])
    assert np.isinf(e[0, 0]) and n[0, 0] == 0


def test_fit_recovers_hedge_and_controls():
    rng = np.random.default_rng(3)
    b = np.cumsum(rng.normal(0, 0.002, 3000))
    ou = np.zeros(3000)
    for t in range(1, 3000):
        ou[t] = 0.95 * ou[t - 1] + rng.normal(0, 0.0008)
    a = 0.7 * b + ou
    f = fit_formation(a, b)
    assert set(f) == {"emrt_c1.5", "emrt_c2.0", "emrt_c2.5", "ols", "notional"}
    assert f["ols"]["beta"] == pytest.approx(0.7, abs=0.05)
    assert f["notional"]["beta"] == 1.0
    for h in ("emrt_c1.5", "emrt_c2.0", "emrt_c2.5"):
        assert 0.6 <= f[h]["beta"] <= 0.8
        # the EMRT pick reverts at least as fast as the OLS spread at the same C would
        assert f[h]["emrt"] <= fit_formation(a, b, cs=(hedge_c(h),))[h]["emrt"] + 1e-9
    assert f["emrt_c2.0"]["emrt"] < f["notional"]["emrt"]
    off = fit_formation(a, b, cs=(1.75,))
    assert set(off) == {"emrt_c1.75", "ols", "notional"}


def test_month_keys():
    d = np.array(["2018-01-31", "2018-02-01", "2019-12-31"], dtype="datetime64[D]")
    assert month_keys(d).tolist() == [2018 * 12, 2018 * 12 + 1, 2019 * 12 + 11]


# ---- data / fits ---------------------------------------------------------------------------

def test_fits_use_only_previous_months(pair):
    f = pair.fits(3)
    first_key = month_keys(pair.session_date[:1])[0]
    for i, k in enumerate(f["key"].tolist()):
        tradable = np.isfinite(f["fits"]["ols"]["beta"][i])
        assert tradable == (k - 3 >= first_key)
        if tradable:
            assert f["fit_end"][i] == f["start"][i] - 1
            assert month_keys(pair.session_date[[f["fit_start"][i]]])[0] == k - 3


def test_size_pair():
    qa, qb = size_pair(10e6, 150_000.0, 140_000.0, 0.8, 2.5)
    fits = lambda a, b: a * 150_000 + b * 140_000 + 2.5 * (a + b) <= 10e6  # noqa: E731
    # floor(10e6 / 270k) = 37, but qb = round(31.7) = 32 overshoots equity, so one fewer
    assert (qa, qb) == (36, round(36 * 150_000 * 0.8 / 140_000)) and fits(qa, qb)
    assert not fits(37, round(37 * 150_000 * 0.8 / 140_000))
    assert size_pair(100_000.0, 150_000.0, 140_000.0, 0.8, 2.5) == (0, 0)
    assert size_pair(10e6, 150_000.0, 140_000.0, float("nan"), 2.5) == (0, 0)


# ---- simulator ------------------------------------------------------------------------------

@pytest.mark.parametrize("kw", [
    {}, {"overnight": "flat"}, {"hedge": "ols", "z_mode": "rolling_50"}, {"hedge": "notional", "exit": "half"},
    {"stop": "1.5", "time_stop": "3emrt"}, {"side": "long", "z_mode": "rolling_100"},
    {"side": "short", "overnight": "flat", "entry_z": 1.0}, {"hedge": "emrt_c1.5", "formation": 6},
])
def test_sim_integrity_clean(pair, kw):
    c = cfg(**kw)
    s = simulate_emrt_spread(pair, c, exec_config=EC, starting_equity=EC.starting_equity)
    assert len(s.entry_idx) > 5, kw
    assert check_sim_integrity(s, pair, EC, c) == []
    if c.overnight == "flat":
        assert set(s.exit_reason) <= {"target_exit", "stop_exit", "time_exit", "eod_exit", "forced_close"}
        assert np.all(pair.session_date[s.exit_idx] == pair.session_date[s.entry_idx])


def test_pnl_by_hand(pair):
    s = simulate_emrt_spread(pair, cfg(), exec_config=EC, starting_equity=EC.starting_equity)
    t = 0
    d, qa, qb = s.side[t], s.qa[t], s.qb[t]
    e = s.entry_idx[t]
    assert s.a_entry[t] == pytest.approx(pair.open[e] + d * 0.25)   # ES tick 0.25, against us
    assert s.b_entry[t] == pytest.approx(pair.b_open[e] - d * 0.25)  # NQ tick 0.25
    pnl = d * qa * 50 * (s.a_exit[t] - s.a_entry[t]) - d * qb * 20 * (s.b_exit[t] - s.b_entry[t]) - 2 * 2.5 * (qa + qb)
    assert s.realized_pnl[t] == pytest.approx(pnl - s.roll_cost[t])
    eq = pair_daily_equity(s, pair, EC.starting_equity)
    assert eq[-1] == pytest.approx(EC.starting_equity + s.realized_pnl.sum())


def test_roll_cost_charged_when_held_over_roll():
    c = cfg(entry_z=1.0)
    base = simulate_emrt_spread(PairData(make_pair()), c, exec_config=EC, starting_equity=EC.starting_equity)
    multi = np.flatnonzero(base.exit_idx // 7 > base.entry_idx // 7)
    assert len(multi), "no trade held across sessions"
    t = int(multi[0])
    roll_day = int(base.exit_idx[t] // 7)        # leg A rolls before that session's first bar
    data = PairData(make_pair(roll_day=roll_day))
    s = simulate_emrt_spread(data, c, exec_config=EC, starting_equity=EC.starting_equity)
    assert np.array_equal(s.entry_idx, base.entry_idx) and np.array_equal(s.exit_idx, base.exit_idx)
    roll_bar = roll_day * 7
    over = (s.entry_idx < roll_bar) & (s.exit_idx >= roll_bar)
    assert over[t] and s.n_rolls[t] == 1
    assert s.roll_cost[t] == pytest.approx(s.qa[t] * 2 * (2.5 + 0.25 * 50))
    assert np.all(s.roll_cost[~over] == 0) and np.all(s.n_rolls[over] == 1)
    assert check_sim_integrity(s, data, EC, c) == []
    flat = simulate_emrt_spread(data, cfg(entry_z=1.0, overnight="flat"), exec_config=EC,
                                starting_equity=EC.starting_equity)
    assert flat.n_rolls.sum() == 0


def test_integrity_catches_tampering(pair):
    c = cfg()
    s = simulate_emrt_spread(pair, c, exec_config=EC, starting_equity=EC.starting_equity)
    assert "pnl_mismatch" in check_sim_integrity(replace(s, realized_pnl=s.realized_pnl + 1000.0), pair, EC, c)
    better = s.a_entry.copy()
    better[0] -= s.side[0] * 1.0
    assert "entry_fill_better_than_market" in check_sim_integrity(replace(s, a_entry=better), pair, EC, c)
    late = s.decision_idx.copy()
    late[0] += 1
    xs = s.exit_idx.copy()
    xs[0] += 1
    iss = check_sim_integrity(replace(s, decision_idx=late, exit_idx=xs), pair, EC, c)
    assert "exit_not_at_first_rule" in iss
    beta = s.beta.copy()
    beta[0] += 0.01
    assert "beta_not_month_fit" in check_sim_integrity(replace(s, beta=beta), pair, EC, c)
    keep = np.arange(len(s.entry_idx)) != 0  # drop the first trade: its signal is now skipped
    sub = replace(s, **{f: getattr(s, f)[keep] for f in (
        "signal_idx", "entry_idx", "exit_idx", "decision_idx", "side", "qa", "qb", "beta", "month", "a_entry", "a_exit",
        "b_entry", "b_exit", "a_entry_base", "b_entry_base", "entry_commission", "roll_cost", "n_rolls", "hold_limit",
        "realized_pnl", "forced_close", "exit_reason", "quantity", "entry_px", "exit_px", "equity_before")})
    assert "signal_skipped_while_flat" in check_sim_integrity(sub, pair, EC, c)


@pytest.mark.parametrize("kw", [{}, {"overnight": "flat", "z_mode": "rolling_50", "hedge": "ols"},
                                {"time_stop": "3emrt", "stop": "2.5", "formation": 6}])
def test_truncation_invariance(pair_frame_df, kw):
    assert truncation_invariance(pair_frame_df, cfg(**kw), exec_config=EC) == []


def test_execution_stress_knobs(pair):
    c = cfg(entry_z=1.0)
    base = simulate_emrt_spread(pair, c, exec_config=EC, starting_equity=EC.starting_equity)
    delay = simulate_emrt_spread(pair, c, exec_config=EC, starting_equity=EC.starting_equity, entry_delay_bars=1)
    assert np.all(delay.entry_idx >= delay.signal_idx + 2)
    miss = simulate_emrt_spread(pair, c, exec_config=EC, starting_equity=EC.starting_equity,
                                missed_entry_frac=0.5, stress_seed=1)
    assert len(miss.entry_idx) < len(base.entry_idx)


# ---- robustness moves -----------------------------------------------------------------------

def test_local_and_random_perturbations_run(pair):
    p = as_params(cfg(stop="1.5", time_stop="3emrt", z_mode="rolling_100", formation=6))
    lc = LocalPerturbationCfg(int_rel=0.2, stop_atr_abs=0.25, entry_z_abs=0.25, stop_z_abs=0.25, emrt_c_abs=0.25,
                              time_stop_mult_abs=0.5)
    moves = dict(local_perturbations_emrt(p, lc))
    assert set(moves) == {"formation=5", "formation=7", "entry_z=1.25", "entry_z=1.75", "stop_z=1.25", "stop_z=1.75",
                          "emrt_c=1.75", "emrt_c=2.25", "z_window=80", "z_window=120", "time_stop_mult=2.5",
                          "time_stop_mult=3.5"}
    assert moves["emrt_c=1.75"].hedge == "emrt_c1.75"
    s = simulate_emrt_spread(pair, moves["emrt_c=1.75"], exec_config=EC, starting_equity=EC.starting_equity)
    assert check_sim_integrity(s, pair, EC, moves["emrt_c=1.75"]) == []
    ctrl = dict(local_perturbations_emrt(as_params(cfg(hedge="ols")), lc))
    assert not any(k.startswith("emrt_c") for k in ctrl) and {"formation=2", "formation=4"} <= set(ctrl)
    pp = perturbations_emrt(p, config_id="x", base_seed=1, pcfg=PerturbationCfg(n_per_config=5, integer_rel_step=0.15,
                                                                               float_rel_step=0.1))
    assert len(pp) == 5 and all(q.formation != 6 or q.entry_z != 1.5 for q in pp)
    for q in pp:
        simulate_emrt_spread(pair, q, exec_config=EC, starting_equity=EC.starting_equity)


# ---- v2: session-anchored, intraday ---------------------------------------------------------

from src.experiments.emrt_grid import AXES_EMRT_V2, emrt_grid_v2  # noqa: E402
from src.analysis.neighborhood import LATTICE_EMRT_V2  # noqa: E402
from src.strategies.emrt_spread.config import EMRTV2Config, tod_sessions  # noqa: E402


def cfg2(**kw) -> EMRTV2Config:
    base = dict(symbol="ES-NQ", timeframe="15min", formation=1, hedge="emrt_c2.0", z_mode="tod_20", entry_z=1.5,
                exit="mean", stop="none", time_stop="none", side="both", first_entry=0)
    return EMRTV2Config(**{**base, **kw})


def make_intraday_pair(days: int = 120, bars_per_day: int = 26, seed: int = 5) -> pl.DataFrame:
    """15-minute-style bars from 14:30 UTC with an intraday-mean-reverting spread."""
    rng = np.random.default_rng(seed)
    ts, sd = [], []
    d = datetime(2018, 1, 2, tzinfo=timezone.utc)
    while len(sd) < days * bars_per_day:
        if d.weekday() < 5:
            for i in range(bars_per_day):
                ts.append(d.replace(hour=14, minute=30) + timedelta(minutes=15 * i))
                sd.append(d.date())
        d += timedelta(days=1)
    n = len(ts)
    b = 7000 * np.exp(np.cumsum(rng.normal(0, 0.0012, n)))
    ou = np.zeros(n)
    for t in range(1, n):
        ou[t] = 0.0 if t % bars_per_day == 0 else 0.8 * ou[t - 1] + rng.normal(0, 0.0008)
    a = 3000 * (1 + 0.8 * (b / b[0] - 1)) * (1 + ou)
    tsa = pl.Series(ts).dt.cast_time_unit("us")
    common = {"bar_open_ts": tsa, "bar_close_ts": tsa + timedelta(minutes=15),
              "bar_open_ts_ny": tsa.dt.convert_time_zone("America/New_York"),
              "session_date_ny": pl.Series(sd), "timeframe": ["15min"] * n}
    noise = np.random.default_rng(9).normal(0, 0.05, n)
    A = pl.DataFrame({**common, "open": a + noise, "high": a + 1, "low": a - 1, "close": a,
                      "price_adjustment": np.zeros(n), "volume": np.ones(n, dtype=np.int64)})
    B = pl.DataFrame({"bar_open_ts": tsa, "session_date_ny": pl.Series(sd), "open": b + noise, "high": b + 1,
                      "low": b - 1, "close": b, "price_adjustment": np.zeros(n), "volume": np.ones(n, dtype=np.int64)})
    return pair_frame(A, B, "ES-NQ")


@pytest.fixture(scope="module")
def ipair_df() -> pl.DataFrame:
    return make_intraday_pair()


@pytest.fixture(scope="module")
def ipair(ipair_df) -> PairData:
    return PairData(ipair_df)


def test_v2_grid():
    g = emrt_grid_v2(("ES-NQ",))
    assert len(g) == 13_824 and len({ce.config_id for ce in g}) == 13_824
    assert all(ce.config.overnight == "flat" and ce.config.anchor == "session" for ce in g)
    for ax, vals in LATTICE_EMRT_V2.ordered.items():
        assert sorted(map(str, vals)) == sorted(map(str, AXES_EMRT_V2[ax])), ax
    assert set(LATTICE_EMRT_V2.ordered) | set(LATTICE_EMRT_V2.fixed) == {"symbol", "anchor", *AXES_EMRT_V2}
    # v1 ids are unchanged by the v2 fields
    assert "anchor" not in EMRTV1Config(symbol="ES-NQ").model_dump()
    assert tod_sessions("tod_60") == 60 and tod_sessions("formation") is None


def test_session_resets_in_zigzag_and_emrt():
    x = np.array([0, 3, 0, -3, 0, 3.0, 0, 0, 3, 0, -3, 0, 3, 0.0])
    resets = np.zeros(len(x), bool)
    resets[7] = True
    P = zigzag_pivots(x[None], np.array([2.5]), resets)[0]
    assert not P[6] and not P[7]      # nothing confirmed across the reset
    assert P[3] and P[10]             # both segments find their own swings
    seg_end = np.where(np.arange(len(x)) < 7, 6, len(x) - 1)
    e_seg, _, _, _ = emrt(np.r_[np.full(7, 1.0), np.full(7, -1.0)][None] + 0, [0.5], resets, seg_end)
    assert np.isinf(e_seg[0, 0])      # flat segments: no pivots


def test_intraday_legs_and_tod_z(ipair):
    d = ipair.intraday()
    s0 = ipair.sess_start
    assert np.allclose(d["a"], (ipair.close - ipair.open[s0]) / ipair.open[s0])
    z, zp = ipair.zscores(1, "ols", "tod_20", "session")
    assert np.all(np.isnan(zp[d["sess_start"]]))
    first_ok = np.flatnonzero(np.isfinite(z))[0]
    assert ipair.sess[first_ok] >= 10   # needs >= 10 previous sessions of the same bar
    with pytest.raises(ValueError):
        ipair.zscores(1, "ols", "rolling_50", "session")


@pytest.mark.parametrize("kw", [{}, {"z_mode": "formation"}, {"hedge": "ols", "z_mode": "tod_60"},
                                {"hedge": "notional", "exit": "half", "stop": "1.5"}, {"first_entry": 30},
                                {"time_stop": "3emrt", "side": "short"}, {"hedge": "emrt_c1.5", "formation": 3}])
def test_v2_sim_integrity_and_flat(ipair, kw):
    c = cfg2(**kw)
    s = simulate_emrt_spread(ipair, c, exec_config=EC, starting_equity=EC.starting_equity)
    assert len(s.entry_idx) > 5, kw
    assert check_sim_integrity(s, ipair, EC, c) == []
    assert np.all(ipair.session_date[s.exit_idx] == ipair.session_date[s.entry_idx])
    assert s.n_rolls.sum() == 0
    if c.first_entry:
        assert np.all(ipair.tod[s.signal_idx] + 15 - ipair.tod[ipair.sess_start[s.signal_idx]] >= 30)


@pytest.mark.parametrize("kw", [{}, {"z_mode": "formation", "time_stop": "3emrt"}])
def test_v2_truncation_invariance(ipair_df, kw):
    assert truncation_invariance(ipair_df, cfg2(**kw), exec_config=EC) == []


def test_v2_integrity_catches_cross_session_entry(ipair):
    c = cfg2()
    s = simulate_emrt_spread(ipair, c, exec_config=EC, starting_equity=EC.starting_equity)
    early = s.signal_idx.copy()
    early[0] -= 1
    assert check_sim_integrity(replace(s, signal_idx=early), ipair, EC, c)


def test_v2_local_moves(ipair):
    p = as_params(cfg2(z_mode="tod_20", stop="1.5", time_stop="3emrt", formation=3))
    lc = LocalPerturbationCfg(int_rel=0.2, stop_atr_abs=0.25, entry_z_abs=0.25, stop_z_abs=0.25, emrt_c_abs=0.25,
                              time_stop_mult_abs=0.5)
    moves = dict(local_perturbations_emrt(p, lc))
    assert {"z_window=16", "z_window=24", "formation=2", "formation=4", "emrt_c=1.75", "emrt_c=2.25"} <= set(moves)
    assert moves["z_window=16"].z_mode == "tod_16" and moves["z_window=16"].anchor == "session"
    for m in ("z_window=16", "emrt_c=1.75", "formation=2"):
        s = simulate_emrt_spread(ipair, moves[m], exec_config=EC, starting_equity=EC.starting_equity)
        assert check_sim_integrity(s, ipair, EC, moves[m]) == []
    one = dict(local_perturbations_emrt(as_params(cfg2(formation=1)), lc))
    assert [k for k in one if k.startswith("formation=")] == ["formation=2"]
