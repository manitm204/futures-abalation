"""v2 mean-reversion knobs: ATR stop, entry confirmation, cooldown, v2 grid,
lattice and perturbations. v1 behavior is covered by test_funnel_integrity.py."""

from __future__ import annotations

import numpy as np
import pytest

from src.analysis.neighborhood import LATTICE_V2, neighbor_ids
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_robustness import perturbations_v2
from src.experiments.integrity import check_sim_integrity, truncation_invariance
from src.experiments.mr_grid import AXES_V2, mr_grid_v2, variants_per_symbol
from src.strategies.mean_reversion.backtest import MRData, MRParams, simulate_mean_reversion
from src.strategies.mean_reversion.config import MeanReversionV2Config
from src.utils.config_models import ExecutionConfig
from tests.unit.test_funnel_integrity import _random_walk

EC = ExecutionConfig()
BASE = MRParams("SPY", "15min", "sma", 12, 12, -1.0, 0.0, 8, "none")


def _v2(**kw) -> MRParams:
    return MRParams(**{**BASE.__dict__, **kw})


def _sim(bars, p):
    data = MRData(bars)
    return data, simulate_mean_reversion(data, p, exec_config=EC, starting_equity=1e5)


def test_v2_grid_size_and_config_mapping():
    assert variants_per_symbol(AXES_V2) == 240_000
    cfg = MeanReversionV2Config(symbol="SPY", mean_lookback=32, max_holding_bars=16, stop_atr_multiple="1.5",
                                entry_confirmation="positive_bar_return", cooldown_bars=4)
    p = MRParams.from_config(cfg)
    assert (p.std_lookback, p.max_hold, p.stop_atr, p.cooldown_bars) == (32, 16, 1.5, 4)
    assert MRParams.from_config(MeanReversionV2Config(symbol="SPY")).stop_atr is None
    assert len({ce.config_id for ce in mr_grid_v2(("SPY",))[:500]}) == 500


def test_stop_uses_atr_known_before_entry_and_is_live_on_entry_bar():
    p = _v2(stop_atr=1.0)
    data, sim = _sim(_random_walk(seed=3), p)
    assert len(sim.entry_idx) > 0
    expect = data.open[sim.entry_idx] - 1.0 * data.atr[sim.entry_idx - 1]
    assert np.allclose(sim.stop_level, expect)
    st = sim.exit_reason == "stop_exit"
    assert st.any() and np.all(sim.exit_idx[st] == sim.decision_idx[st])
    assert np.all(sim.exit_px[st] <= np.minimum(data.open[sim.exit_idx[st]], sim.stop_level[st]) + 1e-9)
    assert check_sim_integrity(sim, data, EC, p) == []
    # Poisoning the ENTRY bars' ATR must not change any stop level.
    poisoned = MRData(_random_walk(seed=3))
    poisoned._cache[("atr",)] = data.atr.copy()
    poisoned._cache[("atr",)][sim.entry_idx] = 1e6
    sim2 = simulate_mean_reversion(poisoned, p, exec_config=EC, starting_equity=1e5)
    assert np.array_equal(sim.entry_idx[:3], sim2.entry_idx[:3]) and np.allclose(sim.stop_level[:3], sim2.stop_level[:3])


def test_stop_on_entry_bar_collapse():
    p = _v2(stop_atr=3.0)
    bars = _random_walk(seed=6)
    _, sim = _sim(bars, p)
    k = int(np.argmax(sim.exit_reason != "stop_exit"))  # a trade that was NOT stopped
    e = int(sim.entry_idx[k])
    crashed = bars.with_columns(bars["low"].scatter(e, 1.0))  # its entry bar's low collapses
    _, sim2 = _sim(crashed, p)
    assert sim2.entry_idx[k] == e and sim2.exit_idx[k] == e and sim2.exit_reason[k] == "stop_exit"
    assert np.array_equal(sim.entry_idx[:k], sim2.entry_idx[:k])


def test_positive_bar_confirmation_and_cooldown():
    bars = _random_walk(seed=5)
    p = _v2(entry_confirmation="positive_bar_return", cooldown_bars=4)
    data, sim = _sim(bars, p)
    c = data.close
    assert len(sim.signal_idx) > 0 and np.all(c[sim.signal_idx] > c[sim.signal_idx - 1])
    assert np.all(sim.signal_idx[1:] >= sim.exit_idx[:-1] + 4)
    assert check_sim_integrity(sim, data, EC, p) == []
    _, base = _sim(bars, BASE)
    assert len(sim.entry_idx) <= len(base.entry_idx)


def test_v2_no_lookahead():
    bars = _random_walk(seed=8)
    for p in (_v2(stop_atr=1.5, cooldown_bars=2), _v2(entry_confirmation="positive_bar_return", stop_atr=3.0,
                                                      trend_filter="above_sma_100", mean_type="ema")):
        assert truncation_invariance(bars, p, exec_config=EC) == []


def test_v2_lattice_stop_order_and_categoricals():
    def rec(cid, **kw):
        base = {"config_id": cid, "symbol": "SPY", "timeframe": "15min", "mean_type": "sma", "mean_lookback": 20,
                "entry_z": -1.5, "exit_z": 0.0, "max_holding_bars": 4, "trend_filter": "none",
                "entry_confirmation": "none", "cooldown_bars": 0, "stop_atr_multiple": "none"}
        return {**base, **kw}
    ids = neighbor_ids([rec("none"), rec("s3", stop_atr_multiple="3.0"), rec("s1", stop_atr_multiple="1.0"),
                        rec("conf", entry_confirmation="positive_bar_return"), rec("cd1", cooldown_bars=1)],
                       lattice=LATTICE_V2)
    assert sorted(ids["none"]) == ["cd1", "s3"]  # no stop sits next to the widest stop; confirmation is fixed
    assert ids["conf"] == []


def test_perturbations_v2():
    p = _v2(mean_lookback=20, std_lookback=20, max_hold=8, cooldown_bars=4, stop_atr=2.0, trend_filter="above_sma_100")
    pc = load_funnel_config().parameter_stability.perturbation
    a = perturbations_v2(p, config_id="x", base_seed=1, pcfg=pc)
    assert a == perturbations_v2(p, config_id="x", base_seed=1, pcfg=pc) and len(a) == pc.n_per_config
    for q in a:
        assert q.std_lookback == q.mean_lookback != 20 and q.cooldown_bars >= 0
        assert q.stop_atr == pytest.approx(q.stop_atr) and 2.0 * 0.85 - 1e-9 <= q.stop_atr <= 2.0 * 1.15 + 1e-9
        assert (q.trend_filter, q.entry_confirmation, q.mean_type) == ("above_sma_100", "none", "sma")
    assert all(q.stop_atr is None for q in perturbations_v2(BASE, config_id="y", base_seed=1, pcfg=pc))


def test_raw_v2_config_applies_every_knob_in_the_funnel_path():
    """Regression: the funnel passes grid configs (not MRParams) to the simulator;
    the v2 stop was silently ignored that way in the first mr_v2 run."""
    from src.experiments.funnel_prep import build_dev_record
    from src.experiments.mr_grid import ConfigEntry
    fcfg = load_funnel_config()
    bars = _random_walk(seed=3)
    data = MRData(bars)
    cfg = MeanReversionV2Config(symbol="SPY", timeframe="15min", mean_lookback=12, entry_z=-1.0,
                                stop_atr_multiple="1.0", cooldown_bars=2, entry_confirmation="positive_bar_return")
    raw = simulate_mean_reversion(data, cfg, exec_config=EC, starting_equity=1e5)
    via = simulate_mean_reversion(data, MRParams.from_config(cfg), exec_config=EC, starting_equity=1e5)
    assert (raw.exit_reason == "stop_exit").any()
    assert np.array_equal(raw.exit_idx, via.exit_idx) and np.allclose(raw.realized_pnl, via.realized_pnl)
    rec, _ = build_dev_record(ConfigEntry(cfg, "x"), data, fcfg=fcfg, exec_config=EC)
    assert rec["full_n_stop_exits"] > 0 and rec["integrity_issues"] == ""
