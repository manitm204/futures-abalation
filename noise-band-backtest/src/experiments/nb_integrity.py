"""Stage 1 -- backtest integrity checks for the noise-band backtester.

Two layers, as for the mean-reversion family (src/experiments/integrity.py):
  * `check_sim_integrity` runs on EVERY config's simulation: the signal bar was a
    check bar (not the session's last) whose close was beyond the band in the
    trade's direction (and that direction is allowed); the entry filled on the next
    bar of the SAME session; every exit is in the entry's session (nothing is held
    overnight); trailing exits were decided at a check close beyond the trailing
    level and filled at the next open; session-close exits filled at the session's
    last close; fills are adverse; stops come from the ATR known before the fill,
    really touched, and filled no better than the worse of open and stop; no
    overlapping positions, no leverage, only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade
    completed before the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.noise_band.backtest import NBData, SimResult, as_params, signal_arrays, simulate_noise_band
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["entry_signal_condition_not_met", "direction_not_allowed", "entry_not_next_bar_same_session",
          "exit_before_entry", "position_held_overnight", "trail_exit_condition_not_met",
          "exit_not_next_open_after_decision", "eod_exit_not_at_session_close", "overlapping_positions",
          "entry_fill_better_than_open", "exit_fill_better_than_market", "position_exceeds_equity",
          "forced_close_not_final_trade", "commission_below_minimum", "unexpected_stop_or_target",
          "stop_not_from_atr_known_before_entry", "stop_exit_without_touch", "stop_fill_better_than_open_stop",
          "entries_per_session_over_cap"]


def check_sim_integrity(sim: SimResult, data: NBData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: list[str] = []
    if len(sim.entry_idx) == 0:
        return issues
    p = as_params(cfg)
    sig = signal_arrays(data, p)
    s, e, x, dec, d = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.decision_idx, sim.side
    long_, short_ = d > 0, d < 0
    ok = np.where(long_, sig["entry_l"][s], sig["entry_s"][s])
    if not ok.all():
        issues.append("entry_signal_condition_not_met")
    if (p.direction == "long" and short_.any()) or (p.direction == "short" and long_.any()):
        issues.append("direction_not_allowed")
    if (e < s + 1).any() or (data.sess[e] != data.sess[s]).any():
        issues.append("entry_not_next_bar_same_session")
    if (x < e).any():
        issues.append("exit_before_entry")
    if (data.sess[x] != data.sess[e]).any():
        issues.append("position_held_overnight")
    why = sim.exit_reason
    trail, eod, stop = why == "trail_exit", (why == "eod_exit") | (why == "forced_close"), why == "stop_exit"
    if trail.any():
        lvl = np.where(long_[trail], sig["exit_l"][dec[trail]], sig["exit_s"][dec[trail]])
        if not lvl.all():
            issues.append("trail_exit_condition_not_met")
        if (x[trail] != dec[trail] + 1).any():
            issues.append("exit_not_next_open_after_decision")
    if eod.any() and ((x[eod] != data.sess_end[e[eod]]) | (dec[eod] != x[eod])).any():
        issues.append("eod_exit_not_at_session_close")
    # Adverse fills: long buys at/above the open and sells at/below the market price; short the reverse.
    if (d * (sim.entry_px - data.open[e]) < -_EPS).any():
        issues.append("entry_fill_better_than_open")
    mkt = np.where(trail, data.open[x], data.close[x])
    m = trail | eod
    if m.any() and (d[m] * (mkt[m] - sim.exit_px[m]) < -_EPS).any():
        issues.append("exit_fill_better_than_market")
    if stop.any():
        xi, lv, ds = x[stop], sim.stop_level[stop], d[stop]
        touched = np.where(ds > 0, data.low[xi] <= lv + _EPS, data.high[xi] >= lv - _EPS)
        if not touched.all():
            issues.append("stop_exit_without_touch")
        worst = np.where(ds > 0, np.minimum(data.open[xi], lv), np.maximum(data.open[xi], lv))
        if (ds * (worst - sim.exit_px[stop]) < -_EPS).any():
            issues.append("stop_fill_better_than_open_stop")
    if p.stop_atr is None:
        if np.isfinite(sim.stop_level).any():
            issues.append("unexpected_stop_or_target")
    else:
        expect = data.open[e] - d * p.stop_atr * data.atr[e - 1]
        if not np.allclose(sim.stop_level, expect, rtol=0, atol=1e-9):
            issues.append("stop_not_from_atr_known_before_entry")
    if p.max_entries is not None and np.unique(data.sess[e], return_counts=True)[1].max() > p.max_entries:
        issues.append("entries_per_session_over_cap")
    if len(e) > 1 and (e[1:] <= x[:-1]).any():
        issues.append("overlapping_positions")
    eq_before = exec_config.starting_equity + np.concatenate([[0.0], np.cumsum(sim.realized_pnl)[:-1]])
    raw_entry = sim.entry_px - data.price_adj[e]
    if (sim.quantity * raw_entry + sim.entry_commission > eq_before + 1e-6).any():
        issues.append("position_exceeds_equity")
    if sim.forced_close[:-1].any():
        issues.append("forced_close_not_final_trade")
    if (sim.entry_commission < exec_config.commission_minimum - _EPS).any():
        issues.append("commission_below_minimum")
    if any(t.target_price is not None for t in sim.trades):
        issues.append("unexpected_stop_or_target")
    return issues


def truncation_invariance(
    bars: pl.DataFrame, cfg, *, exec_config: ExecutionConfig,
    cut_fracs: tuple[float, ...] = (0.35, 0.6, 0.85),
) -> list[str]:
    """Return a list of mismatch descriptions (empty = no look-ahead detected)."""
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_noise_band(NBData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_noise_band(NBData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px", "side"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
