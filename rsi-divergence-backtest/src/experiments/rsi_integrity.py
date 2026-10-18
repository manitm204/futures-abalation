"""Stage 1 -- backtest integrity checks for the RSI-divergence backtester.

Two layers:
  * `check_sim_integrity` runs on EVERY config's simulation: the signal really is
    a bullish divergence between two confirmed RSI pivot lows (pivot p known at
    c = p + pivot_right, previous pivot q within max_pivot_gap, RSI higher low by
    >= min_rsi_diff, price lower low), the signal precedes the entry, 1R comes
    from the ATR known before the fill, stop/target sit at the configured
    distances from the raw entry open, stop exits really touched the stop and
    filled no better than min(open, stop), target exits really touched the target
    and filled no better than it, a bar touching both is a stop exit, time exits
    are decided at the max_hold close and fill on the next open, no overlapping
    positions, adverse entry fill, no leverage, commission minimum respected,
    only the final trade may be force-closed.
  * `truncation_invariance` is an empirical look-ahead test: re-run a config on
    data cut at several points; every trade that completed before the cut must
    be identical to the full-data run. Any pivot or decision that peeks at future
    bars breaks this.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.rsi_divergence.backtest import (
    RSIData,
    SimResult,
    as_params,
    pivot_lows,
    simulate_rsi_divergence,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["entry_signal_condition_not_met", "pivot_not_confirmed_at_signal_bar", "entry_not_after_signal_bar",
          "exit_before_entry", "exit_decided_before_entry", "time_exit_not_at_max_hold",
          "exit_not_next_open_after_decision", "overlapping_positions", "entry_fill_better_than_open",
          "exit_fill_better_than_open", "holding_period_exceeds_max_hold", "position_exceeds_equity",
          "forced_close_not_final_trade", "commission_below_minimum", "stop_not_from_atr_known_before_entry",
          "target_not_at_configured_r", "stop_exit_without_touch", "stop_fill_better_than_min_open_stop",
          "target_exit_without_touch", "target_fill_better_than_target", "target_exit_on_stop_bar",
          "stop_or_target_touched_before_exit"]


def check_sim_integrity(sim: SimResult, data: RSIData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: list[str] = []
    if len(sim.entry_idx) == 0:
        return issues
    cfg = as_params(cfg)
    r = data.rsi(cfg.rsi_lookback)
    p, q, c = sim.pivot_idx, sim.prev_pivot_idx, sim.signal_idx
    piv = set(pivot_lows(r, cfg.pivot_left, cfg.pivot_right).tolist())
    dr = r[p] - r[q]
    bad = ~((p - q <= cfg.max_pivot_gap) & (p > q) & (dr > 0) & (dr >= cfg.min_rsi_diff - _EPS)
            & (data.low[p] < data.low[q]))
    bad |= np.array([int(a) not in piv or int(b) not in piv for a, b in zip(p, q)])
    if bad.any():
        issues.append("entry_signal_condition_not_met")
    if (c != p + cfg.pivot_right).any():
        issues.append("pivot_not_confirmed_at_signal_bar")
    if (sim.entry_idx <= c).any():
        issues.append("entry_not_after_signal_bar")
    if (sim.exit_idx < sim.entry_idx).any():
        issues.append("exit_before_entry")

    a_known = data.atr[sim.entry_idx - 1]
    raw = data.open[sim.entry_idx]
    if not np.allclose(sim.atr_used, a_known, rtol=0, atol=1e-12) or \
            not np.allclose(sim.stop_level, raw - cfg.stop_atr * a_known, rtol=0, atol=1e-9):
        issues.append("stop_not_from_atr_known_before_entry")
    if not np.allclose(sim.target_level, raw + cfg.target_r * cfg.stop_atr * a_known, rtol=0, atol=1e-9):
        issues.append("target_not_at_configured_r")

    done = ~sim.forced_close
    stopped = sim.exit_reason == "stop_exit"
    target = sim.exit_reason == "target_exit"
    timed = sim.exit_reason == "time_exit"
    if done.any() and (sim.decision_idx[done] < sim.entry_idx[done]).any():
        issues.append("exit_decided_before_entry")
    if timed.any():
        if (sim.decision_idx[timed] != sim.entry_idx[timed] + cfg.max_hold - 1).any():
            issues.append("time_exit_not_at_max_hold")
        if (sim.exit_idx[timed] != sim.decision_idx[timed] + 1).any():
            issues.append("exit_not_next_open_after_decision")
        if (sim.exit_px[timed] > data.open[sim.exit_idx[timed]] + _EPS).any():
            issues.append("exit_fill_better_than_open")
    if stopped.any():
        xi = sim.exit_idx[stopped]
        if (data.low[xi] > sim.stop_level[stopped] + _EPS).any():
            issues.append("stop_exit_without_touch")
        if (sim.exit_px[stopped] > np.minimum(data.open[xi], sim.stop_level[stopped]) + _EPS).any():
            issues.append("stop_fill_better_than_min_open_stop")
    if target.any():
        xi = sim.exit_idx[target]
        if (data.high[xi] < sim.target_level[target] - _EPS).any():
            issues.append("target_exit_without_touch")
        if (sim.exit_px[target] > sim.target_level[target] + _EPS).any():
            issues.append("target_fill_better_than_target")
        if (data.low[xi] <= sim.stop_level[target] + _EPS).any():
            issues.append("target_exit_on_stop_bar")
    # No bar from the entry bar up to (excluding) the exit bar may touch the stop or
    # target: the first touch must be the exit (for time exits, the exit bar is the
    # one after the max_hold close, so every held bar is covered).
    if done.any():
        e, x = sim.entry_idx[done], sim.exit_idx[done]
        held = e[:, None] + np.arange(max(int((x - e).max()), 1))[None, :]
        live = held < x[:, None]
        held = np.minimum(held, data.n - 1)
        touched = (data.low[held] <= sim.stop_level[done][:, None]) | \
                  (data.high[held] >= sim.target_level[done][:, None])
        if (touched & live).any():
            issues.append("stop_or_target_touched_before_exit")
    if done.any() and (sim.exit_idx[done] - sim.entry_idx[done] > cfg.max_hold).any():
        issues.append("holding_period_exceeds_max_hold")
    if len(sim.entry_idx) > 1 and (sim.entry_idx[1:] <= sim.exit_idx[:-1]).any():
        issues.append("overlapping_positions")
    if (sim.entry_px < data.open[sim.entry_idx] - _EPS).any():
        issues.append("entry_fill_better_than_open")
    eq_before = exec_config.starting_equity + np.concatenate([[0.0], np.cumsum(sim.realized_pnl)[:-1]])
    if (sim.quantity * sim.entry_px + sim.entry_commission > eq_before + 1e-6).any():
        issues.append("position_exceeds_equity")
    if sim.forced_close[:-1].any():
        issues.append("forced_close_not_final_trade")
    if (sim.entry_commission < exec_config.commission_minimum - _EPS).any():
        issues.append("commission_below_minimum")
    return issues


def truncation_invariance(
    bars: pl.DataFrame, cfg, *, exec_config: ExecutionConfig,
    cut_fracs: tuple[float, ...] = (0.35, 0.6, 0.85),
) -> list[str]:
    """Return a list of mismatch descriptions (empty = no look-ahead detected)."""
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_rsi_divergence(RSIData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_rsi_divergence(RSIData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "pivot_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
