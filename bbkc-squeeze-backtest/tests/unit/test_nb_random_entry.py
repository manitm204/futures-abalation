"""Noise-band random-entry benchmark: intraday, non-overlapping, on-target exposure,
side mix, and scored by the same metrics code as the strategy."""

from __future__ import annotations

from datetime import date

import numpy as np

from src.analysis.daily_performance import daily_equity, window_metrics
from src.experiments.nb_random_entry import place_intraday, simulate_random_intraday
from src.strategies.noise_band.backtest import NBData
from tests.unit.test_noise_band import EC, _walk


def _data():
    return NBData(_walk(n_days=80, seed=5))


def test_place_intraday_fits_sessions_without_overlap():
    rng = np.random.default_rng(0)
    sess_bars = np.array([26] * 50)
    lens = [int(x) for x in rng.integers(2, 12, 120)]
    out = place_intraday(sess_bars, lens, rng)
    assert sorted(L for _, _, L in out) == sorted(lens)
    for s in {s for s, _, _ in out}:
        iv = sorted((st, st + L) for t, st, L in out if t == s)
        assert iv[0][0] >= 0 and iv[-1][1] <= 26
        assert all(a[1] <= b[0] for a, b in zip(iv, iv[1:]))


def test_random_trades_are_intraday_on_target_and_side_mix():
    data = _data()
    start, end = data.days[10].astype(object), data.days[-1].astype(object)
    pool = np.array([3, 5, 8, 12])
    for p_long in (1.0, 0.5):
        exps, longs = [], []
        for k in range(30):
            sim = simulate_random_intraday(data, "SPY", exec_config=EC, starting_equity=1e5, window_start=start,
                                           window_end=end, exposure=0.2, length_pool=pool, p_long=p_long,
                                           rng=np.random.default_rng(k))
            assert (data.sess[sim.entry_idx] == data.sess[sim.exit_idx]).all()  # never overnight
            assert (sim.entry_idx[1:] > sim.exit_idx[:-1]).all()                # never overlapping
            assert (data.session_date[sim.entry_idx] >= np.datetime64(start)).all()
            m, _ = window_metrics(sim, data, daily_equity(sim, data, 1e5), start=start, end=end, starting_equity=1e5)
            exps.append(m["exposure"]); longs.extend(sim.side.tolist())
        assert abs(np.mean(exps) - 0.2) < 0.01
        assert abs(np.mean(np.array(longs) > 0) - p_long) < 0.05
