"""RSI-divergence strategy: indicator causality, pivot/divergence rules, exits,
integrity checks, grid size and funnel wiring."""

from __future__ import annotations

import importlib.util
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_RSI, neighbor_ids
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import perturbations_rsi
from src.experiments.rsi_grid import AXES, rsi_grid, variants_per_symbol
from src.experiments.rsi_integrity import check_sim_integrity, truncation_invariance
from src.strategies.rsi_divergence.backtest import (
    RSIData,
    RSIParams,
    pivot_lows,
    simulate_rsi_divergence,
    wilder_rsi,
)
from src.strategies.rsi_divergence.config import RSIDivergenceConfig
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
FCFG = load_funnel_config(ROOT / "configs" / "funnel" / "rsi_funnel.yaml")
EC = ExecutionConfig()
P = RSIParams("SPY", "15min", rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=48,
              min_rsi_diff=0.0, stop_atr=1.0, target_r=2.0, max_hold=12)


def _bars(closes, *, per_day=26, start=date(2020, 1, 6), spread=0.2, highs=None, lows=None, opens=None):
    rows, d, prev = [], start, closes[0]
    for k, c in enumerate(closes):
        if k % per_day == 0:
            if k:
                d += timedelta(days=1)
            while d.weekday() >= 5:
                d += timedelta(days=1)
            t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        o = prev if opens is None or opens[k] is None else opens[k]
        h = max(o, c) + spread if highs is None or highs[k] is None else highs[k]
        lo = min(o, c) - spread if lows is None or lows[k] is None else lows[k]
        rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * (k % per_day)), "session_date_ny": d,
                     "open": o, "high": h, "low": lo, "close": c})
        prev = c
    return pl.DataFrame(rows)


def _walk(n=2600, seed=0):
    rng = np.random.default_rng(seed)
    return _bars(list(100 + np.cumsum(rng.normal(0.0, 0.3, n))))


# --- indicators ---------------------------------------------------------------------------

def test_wilder_rsi_matches_reference_and_is_causal():
    rng = np.random.default_rng(1)
    c = 100 + np.cumsum(rng.normal(0, 1, 200))
    r = wilder_rsi(c, 14)
    assert np.isnan(r[:14]).all() and np.isfinite(r[14:]).all()
    d = np.diff(c)
    ag, al = np.maximum(d[:14], 0).mean(), np.maximum(-d[:14], 0).mean()
    for t in range(14, 30):
        if t > 14:
            ag = (ag * 13 + max(d[t - 1], 0)) / 14
            al = (al * 13 + max(-d[t - 1], 0)) / 14
        assert r[t] == pytest.approx(100 - 100 / (1 + ag / al))
    assert np.allclose(wilder_rsi(c[:120], 14), r[:120], equal_nan=True)  # prefix-invariant
    assert wilder_rsi(np.arange(30.0), 7)[-1] == 100.0
    assert wilder_rsi(np.full(30, 5.0), 7)[-1] == 50.0


def test_pivot_lows_strict_left_inclusive_right():
    x = np.array([5, 4, 3, 2, 3, 4, 5, 2, 2, 6, 7, 8.0])
    assert pivot_lows(x, 3, 1).tolist() == [3, 7]  # 8 ties 7 on the left -> not a pivot
    assert pivot_lows(x, 3, 3).tolist() == [3, 7]  # a tie on the right is allowed (2 <= min(2, 6, 7))
    x1 = x.copy()
    x1[4] = 1.0
    assert pivot_lows(x1, 3, 1).tolist() == [4]  # bar 4 kills pivot 3 (right) and pivot 7 (left)
    x2 = x.copy()
    x2[1] = np.nan
    assert 3 not in pivot_lows(x2, 3, 1).tolist()  # NaN inside the left window


def test_divergence_rule_on_injected_rsi():
    """Two RSI pivot lows; divergence needs price lower low, RSI higher low (>= min diff), gap limit."""
    n = 60
    close = np.full(n, 100.0)
    lows = [None] * n
    lows[20], lows[35] = 98.0, 97.0          # price lower low at the pivot bars
    data = RSIData(_bars(list(close), lows=lows))
    rsi = np.full(n, 50.0)
    rsi[20], rsi[35] = 25.0, 30.0             # RSI higher low by 5 points
    data._cache[("rsi", 7)] = rsi
    c, p, q = data.divergences(7, 3, 1, 48, 0.0)
    assert (c.tolist(), p.tolist(), q.tolist()) == ([36], [35], [20])
    assert data.divergences(7, 3, 3, 48, 5.0)[0].tolist() == [38]   # confirmed pivot_right bars later
    assert len(data.divergences(7, 3, 1, 48, 8.0)[0]) == 0          # RSI difference too small
    assert len(data.divergences(7, 3, 1, 12, 0.0)[0]) == 0          # pivots 15 bars apart > gap
    lows[35] = 98.5
    data2 = RSIData(_bars(list(close), lows=lows))
    data2._cache[("rsi", 7)] = rsi
    assert len(data2.divergences(7, 3, 1, 48, 0.0)[0]) == 0         # no price lower low


# --- simulator ----------------------------------------------------------------------------

def _sim(bars, p=P, **kw):
    data = RSIData(bars)
    return data, simulate_rsi_divergence(data, p, exec_config=EC, starting_equity=1e5, **kw)


def test_random_walk_integrity_and_no_lookahead():
    bars = _walk()
    for p in (P, RSIParams("SPY", "15min", 14, 5, 3, 24, 3.0, 0.75, 1.0, 6)):
        data, sim = _sim(bars, p)
        assert len(sim.trades) > 10
        assert check_sim_integrity(sim, data, EC, p) == []
        assert truncation_invariance(bars, p, exec_config=EC) == []
        assert set(sim.exit_reason) <= {"stop_exit", "target_exit", "time_exit", "forced_close"}


def test_exit_levels_and_fills():
    data, sim = _sim(_walk(seed=3))
    a = data.atr[sim.entry_idx - 1]
    raw = data.open[sim.entry_idx]
    assert np.allclose(sim.stop_level, raw - P.stop_atr * a)
    assert np.allclose(sim.target_level, raw + P.target_r * P.stop_atr * a)
    tgt = sim.exit_reason == "target_exit"
    assert tgt.any() and np.allclose(sim.exit_px[tgt], sim.target_level[tgt])  # 0 bps limit slippage
    tm = sim.exit_reason == "time_exit"
    assert (sim.exit_idx[tm] - sim.entry_idx[tm] == P.max_hold).all()
    r = np.array([t.realized_r for t in sim.trades])
    assert (r[sim.exit_reason == "stop_exit"] <= -1 + 1e-6).all()


def test_same_bar_stop_and_target_is_a_stop():
    bars = _walk(seed=5)
    data, sim = _sim(bars)
    k = int(np.flatnonzero(sim.exit_reason == "target_exit")[0])
    j = int(sim.exit_idx[k])
    lows = bars["low"].to_list()
    lows[j] = float(sim.stop_level[k]) - 0.01  # the target bar now also touches the stop
    data2, sim2 = _sim(bars.with_columns(pl.Series("low", lows)))
    m = int(np.flatnonzero(sim2.entry_idx == sim.entry_idx[k])[0])
    assert sim2.exit_reason[m] == "stop_exit" and sim2.exit_idx[m] == j
    assert check_sim_integrity(sim2, data2, EC, P) == []


def test_integrity_catches_tampering():
    data, sim = _sim(_walk(seed=7))
    sim.stop_level[0] -= 1.0
    assert "stop_not_from_atr_known_before_entry" in check_sim_integrity(sim, data, EC, P)
    data, sim = _sim(_walk(seed=7))
    sim.signal_idx[0] += 1
    assert "pivot_not_confirmed_at_signal_bar" in check_sim_integrity(sim, data, EC, P)


def test_stress_knobs():
    bars = _walk(seed=2)
    _, base = _sim(bars)
    _, delayed = _sim(bars, entry_delay_bars=1)
    assert (delayed.entry_idx[:3] - delayed.signal_idx[:3] == 2).all()
    _, missed = _sim(bars, missed_entry_frac=0.5, stress_seed=1)
    assert len(missed.trades) < len(base.trades)
    assert set(missed.signal_idx) <= set(data_sig := RSIData(bars).divergences(7, 3, 1, 48, 0.0)[0].tolist())
    assert data_sig


# --- grid / funnel wiring -----------------------------------------------------------------

def test_grid_size_and_axes():
    assert variants_per_symbol() == 98_304
    assert variants_per_symbol({k: v for k, v in AXES.items() if k != "timeframe"}) == 32_768
    g = rsi_grid(("SPY",))
    assert len(g) == 98_304 and len({ce.config_id for ce in g}) == 98_304
    with pytest.raises(Exception):
        RSIDivergenceConfig(symbol="SPY", rsi_lookback=9)


def test_lattice_neighbors_and_perturbations():
    cfgs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in rsi_grid(("SPY",))[:4096]]
    nb = neighbor_ids(cfgs, lattice=LATTICE_RSI)
    assert max(len(v) for v in nb.values()) <= 2 * len(LATTICE_RSI.ordered)
    assert all(len(v) >= 1 for v in nb.values())
    ps = perturbations_rsi(P, config_id="abc", base_seed=1, pcfg=FCFG.parameter_stability.perturbation)
    assert ps == perturbations_rsi(P, config_id="abc", base_seed=1, pcfg=FCFG.parameter_stability.perturbation)
    assert len(ps) == 20 and all(x.timeframe == P.timeframe and x.pivot_right >= 1 and x.min_rsi_diff >= 0
                                 for x in ps)


def test_funnel_record_and_script_import():
    assert FCFG.strategy == "rsi_divergence" and family_for(FCFG).data_cls is RSIData
    bars = _walk()
    ce = rsi_grid(("SPY",))[0]
    data = RSIData(bars)
    fcfg = FCFG.model_copy(update={"data": FCFG.data.model_copy(update={
        "development": FCFG.data.development.model_copy(update={"start": date(2020, 1, 1),
                                                                "end": date(2020, 12, 31)})})})
    rec, rets = build_dev_record(ce, data, fcfg=fcfg, exec_config=EC)
    assert rec["integrity_issues"] == "" and "full_n_target_exits" in rec and len(rets) == len(data.days)
    spec = importlib.util.spec_from_file_location("run_rsi_funnel", ROOT / "scripts" / "run_rsi_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._select_space(FCFG)
    assert mod.GRID_KEYS[1:] == tuple(AXES)
    assert mod._params({**ce.config.model_dump(mode="json")}) == RSIParams.from_config(ce.config)


# --- v2 space: RSI-extreme / ADX / minimum price divergence filters ------------------------

def _adx_reference(h, l, c, n=14):
    """Plain-loop Wilder ADX (TradingView ta.dmi) to check the vectorized version."""
    N = len(c)
    tr, pdm, mdm = [None] * N, [None] * N, [None] * N
    for t in range(1, N):
        up, dn = h[t] - h[t - 1], l[t - 1] - l[t]
        pdm[t] = up if up > dn and up > 0 else 0.0
        mdm[t] = dn if dn > up and dn > 0 else 0.0
        tr[t] = max(h[t] - l[t], abs(h[t] - c[t - 1]), abs(l[t] - c[t - 1]))

    def rma(x, start):
        out, prev = [None] * N, None
        for t in range(start, N):
            if t == start + n - 1:
                prev = sum(x[start:start + n]) / n
            elif t >= start + n:
                prev += (x[t] - prev) / n
            out[t] = prev
        return out

    st, sp, sm = rma(tr, 1), rma(pdm, 1), rma(mdm, 1)
    dx = [None] * N
    for t in range(n, N):
        pdi, mdi = 100 * sp[t] / st[t], 100 * sm[t] / st[t]
        dx[t] = 100 * abs(pdi - mdi) / (pdi + mdi) if pdi + mdi > 0 else 0.0
    return rma(dx, n)


def test_wilder_adx_matches_reference_and_is_causal():
    from src.strategies.rsi_divergence.backtest import wilder_adx
    bars = _walk(400, seed=4)
    h, l, c = (bars[k].to_numpy() for k in ("high", "low", "close"))
    a = wilder_adx(h, l, c, 14)
    ref = _adx_reference(h, l, c, 14)
    assert np.isnan(a[:27]).all() and np.isfinite(a[27:]).all()
    assert np.allclose(a[27:], np.array(ref[27:], dtype=float))
    assert np.allclose(wilder_adx(h[:200], l[:200], c[:200]), a[:200], equal_nan=True)


def test_v2_filters_on_injected_rsi():
    n = 60
    close = np.full(n, 100.0)
    lows = [None] * n
    lows[20], lows[35] = 98.0, 97.0
    data = RSIData(_bars(list(close), lows=lows))
    rsi = np.full(n, 50.0)
    rsi[20], rsi[35] = 35.0, 40.0
    data._cache[("rsi", 7)] = rsi
    base = data.divergences(7, 3, 1, 48, 0.0)[0].tolist()
    assert base == [36]
    assert data.divergences(7, 3, 1, 48, 0.0, rsi_lower=40.0)[0].tolist() == [36]   # RSI_q 35 <= 40
    assert len(data.divergences(7, 3, 1, 48, 0.0, rsi_lower=30.0)[0]) == 0          # 35 > 30
    atr_p = data.atr[35]
    k_ok, k_bad = 0.99 / atr_p, 1.01 / atr_p                                         # price gap is 1.0
    assert data.divergences(7, 3, 1, 48, 0.0, min_px_atr=k_ok)[0].tolist() == [36]
    assert len(data.divergences(7, 3, 1, 48, 0.0, min_px_atr=k_bad)[0]) == 0
    data._cache[("adx",)] = np.full(n, 25.0)
    assert data.divergences(7, 3, 1, 48, 0.0, adx_max=30.0)[0].tolist() == [36]
    assert len(data.divergences(7, 3, 1, 48, 0.0, adx_max=20.0)[0]) == 0
    assert data.divergences(7, 3, 1, 48, 0.0)[0].tolist() == base                    # cache not polluted


def test_v2_grid_sim_integrity_and_wiring():
    from src.analysis.neighborhood import LATTICE_RSI_V2
    from src.experiments.rsi_grid import AXES_V2, rsi_grid_v2
    from src.strategies.rsi_divergence.config import RSIDivergenceV2Config
    assert variants_per_symbol(AXES_V2) == 69_984
    g = rsi_grid_v2(("SPY",))
    assert len(g) == 69_984 and len({ce.config_id for ce in g}) == 69_984
    assert not {ce.config_id for ce in g} & {ce.config_id for ce in rsi_grid(("SPY",))[:5000]}
    with pytest.raises(Exception):
        RSIDivergenceV2Config(symbol="SPY", adx_filter="lt25")
    bars = _walk(seed=6)
    cfg = RSIDivergenceV2Config(symbol="SPY", rsi_lookback=7, pivot_left=3, max_pivot_gap=24, rsi_extreme="40/60",
                                adx_filter="lt30", min_price_div_atr=0.1, stop_atr=1.5, target_r=1.5)
    p = RSIParams.from_config(cfg)
    assert (p.rsi_extreme_lower, p.adx_max, p.min_price_div_atr) == (40.0, 30.0, 0.1)
    data, sim = _sim(bars, p)
    _, loose = _sim(bars, RSIParams(**{**p.__dict__, "rsi_extreme_lower": None, "adx_max": None,
                                       "min_price_div_atr": 0.0}))
    assert 0 < len(sim.trades) < len(loose.trades)
    assert check_sim_integrity(sim, data, EC, p) == []
    assert truncation_invariance(bars, p, exec_config=EC) == []
    off = RSIParams(**{**p.__dict__, "rsi_extreme_lower": 1.0})
    assert "rsi_extreme_filter_violated" in check_sim_integrity(sim, data, EC, off)
    cfgs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in g[:3000]]
    nb = neighbor_ids(cfgs, lattice=LATTICE_RSI_V2)
    assert all(len(v) >= 1 for v in nb.values())
    ps = perturbations_rsi(p, config_id="x", base_seed=1, pcfg=FCFG.parameter_stability.perturbation)
    assert all(x.adx_max is not None and x.rsi_extreme_lower is not None and x.min_price_div_atr > 0 for x in ps)
    p_off = RSIParams.from_config(RSIDivergenceV2Config(symbol="SPY"))
    assert all(x.adx_max is None and x.rsi_extreme_lower is None and x.min_price_div_atr == 0
               for x in perturbations_rsi(p_off, config_id="x", base_seed=1, pcfg=FCFG.parameter_stability.perturbation))
    fv2 = load_funnel_config(ROOT / "configs" / "funnel" / "rsi_funnel_v2.yaml")
    assert fv2.strategy == "rsi_divergence_v2" and family_for(fv2).data_cls is RSIData
    spec = importlib.util.spec_from_file_location("run_rsi_funnel_v2", ROOT / "scripts" / "run_rsi_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._select_space(fv2)
    assert mod.GRID_KEYS[1:] == tuple(AXES_V2)
    assert mod._params(cfg.model_dump(mode="json")) == p


# --- v3 space: EMA trend filter / breakout entry / entry session window -------------------

def test_ema_matches_reference_and_is_causal():
    from src.strategies.rsi_divergence.backtest import ema
    rng = np.random.default_rng(8)
    c = 100 + np.cumsum(rng.normal(0, 1, 120))
    e = ema(c, 20)
    assert np.isnan(e[:19]).all() and e[19] == pytest.approx(c[:20].mean())
    ref = c[:20].mean()
    for t in range(20, 120):
        ref = ref + 2 / 21 * (c[t] - ref)
        assert e[t] == pytest.approx(ref)
    assert np.allclose(ema(c[:60], 20), e[:60], equal_nan=True)


def test_trend_filter_on_injected_rsi():
    n = 60
    lows = [None] * n
    lows[20], lows[35] = 98.0, 97.0
    data = RSIData(_bars([100.0] * n, lows=lows))
    rsi = np.full(n, 50.0)
    rsi[20], rsi[35] = 25.0, 30.0
    data._cache[("rsi", 7)] = rsi
    data._cache[("ema", 20)] = np.full(n, 99.0)   # close 100 > 99 -> long allowed
    data._cache[("ema", 50)] = np.full(n, 101.0)  # close 100 < 101 -> filtered
    assert data.divergences(7, 3, 1, 48, 0.0, trend_ema=20)[0].tolist() == [36]
    assert len(data.divergences(7, 3, 1, 48, 0.0, trend_ema=50)[0]) == 0
    assert data.divergences(7, 3, 1, 48, 0.0)[0].tolist() == [36]


def _v3(**kw) -> RSIParams:
    return RSIParams(**{**P.__dict__, "max_pivot_gap": 24, "stop_atr": 1.5, "max_hold": 24, **kw})


def test_breakout_entry_rule_and_integrity():
    from src.strategies.rsi_divergence.backtest import BREAKOUT_BARS
    bars = _walk(seed=9)
    base = _v3()
    brk = _v3(entry_breakout=True)
    data, imm = _sim(bars, base)
    data, sim = _sim(bars, brk)
    assert 0 < len(sim.trades) <= len(imm.trades)
    assert (imm.trigger_idx == imm.signal_idx).all() and (imm.entry_idx == imm.signal_idx + 1).all()
    c, t = sim.signal_idx, sim.trigger_idx
    assert ((t > c) & (t <= c + BREAKOUT_BARS)).all() and (sim.entry_idx == t + 1).all()
    assert (data.close[t] > data.high[c]).all()
    for ci, ti in zip(c, t):
        assert not (data.close[ci + 1:ti] > data.high[ci]).any()  # first breakout close
    assert check_sim_integrity(sim, data, EC, brk) == []
    assert truncation_invariance(bars, brk, exec_config=EC) == []
    sim.trigger_idx[0] += 1
    assert "breakout_trigger_invalid" in check_sim_integrity(sim, data, EC, brk)


def test_session_window_and_trend_integrity():
    bars = _walk(seed=10)
    data, full = _sim(bars, _v3())
    m = data.minute_ny
    assert m[0] == 570 and m[25] == 945  # 15-min test bars: 09:30 .. 15:45 New York
    first = (m[full.entry_idx] < 600)
    last = (m[full.entry_idx] >= 930)
    assert first.any() and last.any()
    for w in ("excl_first30", "excl_last30", "excl_first_last30"):
        p = _v3(session_window=w, trend_ema=20)
        data, sim = _sim(bars, p)
        em = m[sim.entry_idx]
        assert len(sim.trades) > 0
        assert not (("first" in w) and (em < 600).any()) and not (("last" in w) and (em >= 930).any())
        assert (data.close[sim.signal_idx] > data.ema(20)[sim.signal_idx]).all()
        assert check_sim_integrity(sim, data, EC, p) == []
        assert truncation_invariance(bars, p, exec_config=EC) == []
    data, full = _sim(bars, _v3())  # full-session trades include 09:30-10:00 entries
    assert "entry_in_excluded_session_window" in check_sim_integrity(full, data, EC, _v3(session_window="excl_first30"))


def test_v3_grid_and_wiring():
    from src.analysis.neighborhood import LATTICE_RSI_V3
    from src.experiments.rsi_grid import AXES_V3, rsi_grid_v3
    from src.strategies.rsi_divergence.config import RSIDivergenceV3Config
    assert variants_per_symbol(AXES_V3) == 248_832
    assert variants_per_symbol({k: v for k, v in AXES_V3.items() if k != "timeframe"}) == 124_416
    g = rsi_grid_v3(("SPY",))
    assert len(g) == 248_832 and len({ce.config_id for ce in g}) == 248_832
    with pytest.raises(Exception):
        RSIDivergenceV3Config(symbol="SPY", adx_filter="lt30")
    cfg = RSIDivergenceV3Config(symbol="SPY", trend_filter="ema50", entry_confirmation="breakout",
                                session_window="excl_first_last30", rsi_extreme="30/70", min_price_div_atr=0.25)
    p = RSIParams.from_config(cfg)
    assert (p.trend_ema, p.entry_breakout, p.session_window, p.adx_max, p.rsi_extreme_lower) == \
        (50, True, "excl_first_last30", None, 30.0)
    cfgs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in g[:4000]]
    nb = neighbor_ids(cfgs, lattice=LATTICE_RSI_V3)
    assert all(len(v) >= 1 for v in nb.values())
    ps = perturbations_rsi(p, config_id="x", base_seed=1, pcfg=FCFG.parameter_stability.perturbation)
    assert all(x.trend_ema is not None and x.trend_ema != 50 and x.entry_breakout
               and x.session_window == "excl_first_last30" for x in ps)
    fv3 = load_funnel_config(ROOT / "configs" / "funnel" / "rsi_funnel_v3.yaml")
    assert fv3.strategy == "rsi_divergence_v3" and family_for(fv3).data_cls is RSIData
    assert fv3.data.timeframes == ["5min", "15min"]
    spec = importlib.util.spec_from_file_location("run_rsi_funnel_v3", ROOT / "scripts" / "run_rsi_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._select_space(fv3)
    assert mod.GRID_KEYS[1:] == tuple(AXES_V3)
    assert mod._params(cfg.model_dump(mode="json")) == p
