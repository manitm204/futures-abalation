"""Stage 1 -- backtest integrity checks for the mean-reversion backtester.

Two layers:
  * `check_sim_integrity` runs on EVERY config's simulation: the signal bar's
    z-score really met the entry rule, the signal precedes the entry, the exit
    was decided on a close at or after the entry bar and filled on the next
    bar's open, no overlapping positions, fills are adverse (entry >= raw open,
    exit <= raw open), the holding cap is respected, no leverage, commissions
    respect the minimum, only the final trade may be force-closed, no trade
    carries a profit target (so stop/target-in-one-bar ambiguity cannot arise),
    a stop exists only when configured and comes from the ATR known before the
    fill, stop exits really touched the stop and filled no better than
    min(open, stop), and the cooldown is respected.
  * `truncation_invariance` is an empirical look-ahead test: re-run a config on
    data cut at several points; every trade that completed before the cut must
    be identical to the full-data run. Any indicator or decision that peeks at
    future bars breaks this.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.mean_reversion.backtest import MRData, SimResult, as_params, simulate_mean_reversion
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["entry_signal_condition_not_met", "entry_not_after_signal_bar", "exit_before_entry",
          "exit_decided_before_entry", "exit_not_next_open_after_decision", "overlapping_positions",
          "entry_fill_better_than_open", "exit_fill_better_than_open", "holding_period_exceeds_max_hold",
          "position_exceeds_equity", "forced_close_not_final_trade", "commission_below_minimum",
          "unexpected_stop_or_target", "stop_not_from_atr_known_before_entry", "stop_exit_without_touch",
          "stop_fill_better_than_min_open_stop", "cooldown_violated"]


def check_sim_integrity(sim: SimResult, data: MRData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: list[str] = []
    if len(sim.entry_idx) == 0:
        return issues
    cfg = as_params(cfg)
    z = data.zscore(cfg.mean_type, cfg.mean_lookback, cfg.std_lookback)
    zs = z[sim.signal_idx]
    bad_signal = ~(zs <= cfg.entry_z + _EPS) | ~data.trend_ok(cfg.trend_filter)[sim.signal_idx]
    if getattr(cfg, "entry_confirmation", "none") == "positive_bar_return":
        bad_signal |= ~data.positive_bar()[sim.signal_idx]
    if bad_signal.any():
        issues.append("entry_signal_condition_not_met")
    if (sim.entry_idx <= sim.signal_idx).any():
        issues.append("entry_not_after_signal_bar")
    if (sim.exit_idx < sim.entry_idx).any():
        issues.append("exit_before_entry")
    done = ~sim.forced_close
    stopped = sim.exit_reason == "stop_exit"
    mkt = done & ~stopped
    if done.any() and (sim.decision_idx[done] < sim.entry_idx[done]).any():
        issues.append("exit_decided_before_entry")
    if mkt.any():
        if (sim.exit_idx[mkt] != sim.decision_idx[mkt] + 1).any():
            issues.append("exit_not_next_open_after_decision")
        if (sim.exit_px[mkt] > data.open[sim.exit_idx[mkt]] + _EPS).any():
            issues.append("exit_fill_better_than_open")
    if stopped.any():
        xi = sim.exit_idx[stopped]
        if (data.low[xi] > sim.stop_level[stopped] + _EPS).any():
            issues.append("stop_exit_without_touch")
        if (sim.exit_px[stopped] > np.minimum(data.open[xi], sim.stop_level[stopped]) + _EPS).any():
            issues.append("stop_fill_better_than_min_open_stop")
    k = getattr(cfg, "stop_atr", None)
    if k is None:
        if np.isfinite(sim.stop_level).any():
            issues.append("unexpected_stop_or_target")
    else:
        expect = data.open[sim.entry_idx] - k * data.atr[sim.entry_idx - 1]
        if not np.allclose(sim.stop_level, expect, rtol=0, atol=1e-9):
            issues.append("stop_not_from_atr_known_before_entry")
    cd = getattr(cfg, "cooldown_bars", 0)
    if cd and len(sim.entry_idx) > 1 and (sim.signal_idx[1:] < sim.exit_idx[:-1] + cd).any():
        issues.append("cooldown_violated")
    if done.any():
        if (sim.exit_idx[done] - sim.entry_idx[done] > cfg.max_hold).any():
            issues.append("holding_period_exceeds_max_hold")
    if len(sim.entry_idx) > 1 and (sim.entry_idx[1:] <= sim.exit_idx[:-1]).any():
        issues.append("overlapping_positions")
    if (sim.entry_px < data.open[sim.entry_idx] - _EPS).any():
        issues.append("entry_fill_better_than_open")
    eq_before = exec_config.starting_equity + np.concatenate([[0.0], np.cumsum(sim.realized_pnl)[:-1]])
    raw_entry = sim.entry_px - data.price_adj[sim.entry_idx]  # back-adjusted futures: real contract price
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
    full = simulate_mean_reversion(MRData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_mean_reversion(MRData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
