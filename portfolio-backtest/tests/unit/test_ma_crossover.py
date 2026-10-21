"""MA-crossover strategy: indicator causality, crossover/confirmation/buffer/slope
rules, stop and crossover exits, integrity checks, grid size and funnel wiring."""

from __future__ import annotations

import importlib.util
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_MA, neighbor_ids
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import perturbations_ma
from src.experiments.ma_grid import AXES, ma_grid, variants_per_symbol
from src.experiments.ma_integrity import check_sim_integrity, truncation_invariance
from src.strategies.ma_crossover.backtest import MAData, MAParams, ema, simulate_ma_crossover, sma
from src.strategies.ma_crossover.config import SLOPE_BARS, MACrossoverConfig
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
FCFG = load_funnel_config(ROOT / "configs" / "funnel" / "ma_funnel.yaml")
EC = ExecutionConfig()
P = MAParams("SPY", "15min", "SMA/SMA", fast_length=5, slow_length=40, confirm_bars=1, buffer_atr=0.0,
             stop_atr=None, slope_filter=False)


def _bars(closes, *, per_day=26, start=date(2020, 1, 6), spread=0.2):
    rows, d, prev = [], start, closes[0]
    for k, c in enumerate(closes):
        if k % per_day == 0:
            if k:
                d += timedelta(days=1)
            while d.weekday() >= 5:
                d += timedelta(days=1)
            t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        o = prev
        rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * (k % per_day)), "session_date_ny": d,
                     "open": o, "high": max(o, c) + spread, "low": min(o, c) - spread, "close": c})
        prev = c
    return pl.DataFrame(rows)


def _walk(n=4000, seed=0):
    rng = np.random.default_rng(seed)
    return _bars(list(100 + np.cumsum(rng.normal(0.0, 0.3, n))))


def _sim(bars, p=P, **kw):
    data = MAData(bars)
    return data, simulate_ma_crossover(data, p, exec_config=EC, starting_equity=EC.starting_equity, **kw)


def _p(**kw):
    return MAParams(**{**P.__dict__, **kw})


# --- indicators ---------------------------------------------------------------------------

def test_sma_ema_reference_and_causal():
    rng = np.random.default_rng(1)
    c = 100 + np.cumsum(rng.normal(0, 1, 300))
    s = sma(c, 20)
    assert np.isnan(s[:19]).all() and s[19] == pytest.approx(c[:20].mean())
    assert s[150] == pytest.approx(c[131:151].mean())
    e = ema(c, 10)
    ref = c[:10].mean()
    assert np.isnan(e[:9]).all() and e[9] == pytest.approx(ref)
    for t in range(10, 40):
        ref += 2 / 11 * (c[t] - ref)
        assert e[t] == pytest.approx(ref)
    for f in (sma, ema):
        assert np.allclose(f(c[:120], 20), f(c, 20)[:120], equal_nan=True)  # prefix-invariant


def test_crossover_signal_rules_on_constructed_path():
    # Flat, then a steady rise: the fast SMA crosses above the slow SMA once.
    closes = [100.0] * 60 + [100.0 + 0.2 * i for i in range(1, 80)]
    data = MAData(_bars(closes, spread=0.05))
    d = data.diff("SMA/SMA", 5, 40)
    k = int(np.flatnonzero(d > 0)[0])
    c1, k1 = data.signals("SMA/SMA", 5, 40, 1, 0.0, False)
    assert c1.tolist() == [k] and k1.tolist() == [k]
    c3, _ = data.signals("SMA/SMA", 5, 40, 3, 0.0, False)
    assert c3.tolist() == [k + 2]
    cb, _ = data.signals("SMA/SMA", 5, 40, 1, 0.5, False)
    first_buf = int(np.flatnonzero((d >= 0.5 * data.atr) & (np.arange(data.n) >= k))[0])
    assert cb.tolist() == [first_buf] and first_buf > k
    cs, _ = data.signals("SMA/SMA", 5, 40, 1, 0.0, True)
    slow = data.ma("SMA", 40)
    assert cs.tolist() == [k] and slow[k] > slow[k - SLOPE_BARS]


def test_run_starting_in_warmup_is_not_traded():
    closes = [100.0 + 0.2 * i for i in range(120)]  # fast > slow from the first defined bar
    data = MAData(_bars(closes, spread=0.05))
    assert len(data.signals("SMA/SMA", 5, 40, 1, 0.0, False)[0]) == 0


# --- simulation + integrity ---------------------------------------------------------------

@pytest.mark.parametrize("p", [
    P,
    _p(ma_pair="EMA/SMA", fast_length=8, slow_length=60, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5),
    _p(ma_pair="SMA/EMA", fast_length=12, slow_length=80, confirm_bars=3, stop_atr=2.5, slope_filter=True),
    _p(ma_pair="EMA/EMA", fast_length=20, slow_length=150, confirm_bars=4, buffer_atr=0.5, slope_filter=True),
])
def test_random_walk_integrity_and_no_lookahead(p):
    bars = _walk()
    data, sim = _sim(bars, p)
    assert len(sim.trades) >= 5
    assert check_sim_integrity(sim, data, EC, p) == []
    assert truncation_invariance(bars, p, exec_config=EC) == []
    assert set(sim.exit_reason) <= {"stop_exit", "cross_exit", "forced_close"}
    assert len(set(sim.cross_idx.tolist())) == len(sim.cross_idx)  # one entry per bullish run


def test_cross_exit_and_stop_levels():
    data, sim = _sim(_walk(seed=3))
    assert (sim.exit_reason[:-1] == "cross_exit").all() and np.isnan(sim.stop_level).all()
    d = data.diff("SMA/SMA", 5, 40)
    for c, x in zip(sim.signal_idx, sim.decision_idx):
        if x >= 0:
            assert d[x] <= 0 and (d[c:x] > 0).all()
    p = _p(stop_atr=1.5)
    data, sim = _sim(_walk(seed=3), p)
    a = data.atr[sim.entry_idx - 1]
    assert np.allclose(sim.stop_level, data.open[sim.entry_idx] - 1.5 * a)
    st = sim.exit_reason == "stop_exit"
    assert st.any() and (np.array([t.realized_r for t in sim.trades])[st] <= -1 + 1e-6).all()


def test_stop_fills_before_cross_on_same_bar():
    bars = _walk(seed=5)
    p = _p(stop_atr=3.0)
    data, sim = _sim(bars, p)
    k = int(np.flatnonzero(sim.exit_reason == "cross_exit")[0])
    j = int(sim.decision_idx[k])
    lows = bars["low"].to_list()
    lows[j] = float(sim.stop_level[k]) - 0.01  # the cross bar now also touches the stop
    data2, sim2 = _sim(bars.with_columns(pl.Series("low", lows)), p)
    m = int(np.flatnonzero(sim2.entry_idx == sim.entry_idx[k])[0])
    assert sim2.exit_reason[m] == "stop_exit" and sim2.exit_idx[m] <= j
    assert check_sim_integrity(sim2, data2, EC, p) == []


def test_integrity_catches_tampering():
    p = _p(stop_atr=2.0)
    data, sim = _sim(_walk(seed=7), p)
    sim.stop_level[0] -= 1.0
    assert "stop_not_from_atr_known_before_entry" in check_sim_integrity(sim, data, EC, p)
    data, sim = _sim(_walk(seed=7), p)
    sim.signal_idx[0] += 1
    assert "signal_not_first_in_run" in check_sim_integrity(sim, data, EC, p)
    data, sim = _sim(_walk(seed=7), p)
    k = int(np.flatnonzero(sim.exit_reason == "cross_exit")[0])
    sim.decision_idx[k] += 1
    assert "cross_exit_not_at_first_cross" in check_sim_integrity(sim, data, EC, p)


def test_stress_knobs():
    bars = _walk(seed=2)
    _, base = _sim(bars)
    data, delayed = _sim(bars, entry_delay_bars=1)
    assert (delayed.entry_idx - delayed.signal_idx == 2).all()
    assert check_sim_integrity(delayed, data, EC, P) == []
    _, missed = _sim(bars, missed_entry_frac=0.5, stress_seed=1)
    assert len(missed.trades) < len(base.trades)
    assert set(missed.signal_idx.tolist()) <= set(data.signals("SMA/SMA", 5, 40, 1, 0.0, False)[0].tolist())


# --- grid / funnel wiring -----------------------------------------------------------------

def test_grid_size_and_axes():
    assert variants_per_symbol() == 60_000
    assert variants_per_symbol({k: v for k, v in AXES.items() if k != "timeframe"}) == 20_000
    g = ma_grid(("SPY",))
    assert len(g) == 60_000 and len({ce.config_id for ce in g}) == 60_000
    with pytest.raises(Exception):
        MACrossoverConfig(symbol="SPY", fast_length=9)
    with pytest.raises(Exception):
        MACrossoverConfig(symbol="SPY", stop_atr=1.0)


def test_lattice_neighbors_and_perturbations():
    cfgs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in ma_grid(("SPY",))[:4000]]
    nb = neighbor_ids(cfgs, lattice=LATTICE_MA)
    assert max(len(v) for v in nb.values()) <= 2 * len(LATTICE_MA.ordered)
    assert all(len(v) >= 1 for v in nb.values())
    pcfg = FCFG.parameter_stability.perturbation
    q = _p(buffer_atr=0.2, stop_atr=2.0, fast_length=20, slow_length=40)
    ps = perturbations_ma(q, config_id="abc", base_seed=1, pcfg=pcfg)
    assert ps == perturbations_ma(q, config_id="abc", base_seed=1, pcfg=pcfg)
    assert len(ps) == 20 and all(x.fast_length < x.slow_length and x.confirm_bars >= 1 and x.ma_pair == q.ma_pair
                                 and x.slope_filter == q.slope_filter for x in ps)
    off = perturbations_ma(P, config_id="abc", base_seed=1, pcfg=pcfg)
    assert all(x.stop_atr is None and x.buffer_atr == 0.0 for x in off)


def test_funnel_record_and_script_import():
    assert FCFG.strategy == "ma_crossover" and family_for(FCFG).data_cls is MAData
    bars = _walk()
    ce = ma_grid(("SPY",))[0]
    data = MAData(bars)
    fcfg = FCFG.model_copy(update={"data": FCFG.data.model_copy(update={
        "development": FCFG.data.development.model_copy(update={"start": date(2020, 1, 1),
                                                                "end": date(2020, 12, 31)})})})
    rec, rets = build_dev_record(ce, data, fcfg=fcfg, exec_config=EC)
    assert rec["integrity_issues"] == "" and "full_n_cross_exits" in rec and len(rets) == len(data.days)
    spec = importlib.util.spec_from_file_location("run_ma_funnel", ROOT / "scripts" / "run_ma_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._select_space(FCFG)
    assert mod.GRID_KEYS[1:] == tuple(AXES)
    for ce in ma_grid(("SPY",))[:50]:
        assert mod._params({**ce.config.model_dump(mode="json")}) == MAParams.from_config(ce.config)


# --- v2 space: max hold / take profit / cooldown / min ADX / max extension --------------

from src.analysis.neighborhood import LATTICE_MA_V2  # noqa: E402
from src.experiments.ma_grid import AXES_V2, ma_grid_v2  # noqa: E402
from src.strategies.ma_crossover.config import MACrossoverV2Config  # noqa: E402

FCFG_V2 = load_funnel_config(ROOT / "configs" / "funnel" / "ma_funnel_v2.yaml")
P2 = _p(ma_pair="EMA/EMA", fast_length=8, slow_length=80, stop_atr=2.0, max_hold=16, take_profit_atr=2.0,
        cooldown_bars=4, min_adx=15.0, max_extension_atr=3.0)


@pytest.mark.parametrize("p", [
    P2,
    _p(max_hold=8),
    _p(take_profit_atr=4.0, stop_atr=2.0),
    _p(cooldown_bars=12, confirm_bars=2, buffer_atr=0.2),
    _p(min_adx=25.0, slope_filter=True),
    _p(max_extension_atr=1.5, slow_length=150),
    _p(ma_pair="SMA/EMA", fast_length=12, slow_length=100, max_hold=32, take_profit_atr=4.0, cooldown_bars=12,
       min_adx=15.0, max_extension_atr=1.5, stop_atr=2.0, slope_filter=True),
])
def test_v2_random_walk_integrity_and_no_lookahead(p):
    bars = _walk(n=6000, seed=11)
    data, sim = _sim(bars, p)
    assert len(sim.trades) >= 3
    assert check_sim_integrity(sim, data, EC, p) == []
    assert truncation_invariance(bars, p, exec_config=EC) == []
    assert len(set(sim.cross_idx.tolist())) == len(sim.cross_idx)


def test_v2_exits_levels_and_cooldown():
    data, sim = _sim(_walk(n=6000, seed=12), P2)
    a = data.atr[sim.entry_idx - 1]
    raw = data.open[sim.entry_idx]
    assert np.allclose(sim.target_level, raw + 2.0 * a) and np.allclose(sim.stop_level, raw - 2.0 * a)
    tgt, tm = sim.exit_reason == "target_exit", sim.exit_reason == "time_exit"
    assert tgt.any() and np.allclose(sim.exit_px[tgt], sim.target_level[tgt])
    assert tm.any() and (sim.exit_idx[tm] - sim.entry_idx[tm] == 16).all()
    assert (sim.exit_idx[sim.exit_reason != "forced_close"] - sim.entry_idx[sim.exit_reason != "forced_close"] <= 16).all()
    assert (sim.signal_idx[1:] >= sim.exit_idx[:-1] + 4).all()
    assert (data.adx[sim.signal_idx] >= 15).all()
    slow = data.ma("EMA", 80)
    assert (data.close[sim.signal_idx] - slow[sim.signal_idx] <= 3.0 * data.atr[sim.signal_idx] + 1e-9).all()


def test_v2_filters_only_remove_or_delay_entries():
    bars = _walk(n=6000, seed=13)
    _, base = _sim(bars, P)
    for kw in ({"min_adx": 25.0}, {"max_extension_atr": 1.5}):
        data, f = _sim(bars, _p(**kw))
        assert set(f.cross_idx.tolist()) <= set(base.cross_idx.tolist())  # same runs, never new ones
        k = {int(x): int(c) for x, c in zip(base.cross_idx, base.signal_idx)}
        assert all(c >= k[int(x)] for x, c in zip(f.cross_idx, f.signal_idx))  # same bar or later in the run


def test_v2_cooldown_delays_reentry_after_whipsaw():
    bars = _walk(n=6000, seed=14)
    _, base = _sim(bars, P)
    gaps = base.signal_idx[1:] - base.exit_idx[:-1]
    assert (gaps < 12).any()  # some re-entries come quickly after an exit
    data, cd = _sim(bars, _p(cooldown_bars=12))
    assert (cd.signal_idx[1:] >= cd.exit_idx[:-1] + 12).all()
    assert check_sim_integrity(cd, data, EC, _p(cooldown_bars=12)) == []


def test_v2_integrity_catches_tampering():
    data, sim = _sim(_walk(n=6000, seed=12), P2)
    k = int(np.flatnonzero(sim.exit_reason == "time_exit")[0])
    sim.decision_idx[k] -= 1
    sim.exit_idx[k] -= 1
    assert "time_exit_not_at_max_hold" in check_sim_integrity(sim, data, EC, P2)
    data, sim = _sim(_walk(n=6000, seed=12), P2)
    sim.target_level[0] += 1.0
    assert "target_not_from_atr_known_before_entry" in check_sim_integrity(sim, data, EC, P2)
    data, sim = _sim(_walk(n=6000, seed=12), P2)
    q = _p(**{**P2.__dict__, "cooldown_bars": 400})
    assert "entry_during_cooldown" in check_sim_integrity(sim, data, EC, q)


def test_v2_grid_lattice_and_wiring():
    assert variants_per_symbol(AXES_V2) == 248_832
    assert variants_per_symbol({k: v for k, v in AXES_V2.items() if k != "timeframe"}) == 124_416
    g = ma_grid_v2(("SPY",))
    assert len(g) == 248_832 and len({ce.config_id for ce in g}) == 248_832
    with pytest.raises(Exception):
        MACrossoverV2Config(symbol="SPY", max_hold=10)
    cfgs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in g[:5000]]
    nb = neighbor_ids(cfgs, lattice=LATTICE_MA_V2)
    assert max(len(v) for v in nb.values()) <= 2 * len(LATTICE_MA_V2.ordered)
    assert all(len(v) >= 1 for v in nb.values())
    pc = FCFG_V2.parameter_stability.perturbation
    ps = perturbations_ma(P2, config_id="x", base_seed=1, pcfg=pc)
    assert all(x.max_hold >= 1 and x.cooldown_bars >= 0 and x.min_adx > 0 and x.take_profit_atr > 0
               and x.max_extension_atr > 0 for x in ps)
    assert FCFG_V2.strategy == "ma_crossover_v2" and family_for(FCFG_V2).data_cls is MAData
    ce = g[123_457]
    fcfg = FCFG_V2.model_copy(update={"data": FCFG_V2.data.model_copy(update={
        "development": FCFG_V2.data.development.model_copy(update={"start": date(2020, 1, 1),
                                                                   "end": date(2020, 12, 31)})})})
    rec, _ = build_dev_record(ce, MAData(_walk()), fcfg=fcfg, exec_config=EC)
    assert rec["integrity_issues"] == "" and "full_n_time_exits" in rec
    spec = importlib.util.spec_from_file_location("run_ma_funnel", ROOT / "scripts" / "run_ma_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._select_space(FCFG_V2)
    assert mod.GRID_KEYS[1:] == tuple(AXES_V2)
    for ce in g[::5000]:
        assert mod._params(ce.config.model_dump(mode="json")) == MAParams.from_config(ce.config)
