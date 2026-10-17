"""Stage 1 -- backtest integrity checks for the channel-breakout backtester.

Two layers:
  * `check_sim_integrity` runs on EVERY config's simulation: signal precedes
    entry, no overlapping positions, fills are adverse (entry >= raw open, stop
    exits no better than min(open, stop) so gaps fill at the worse open),
    commissions respect the minimum, only the final trade may be force-closed,
    and no trade carries a profit target (so the stop-and-target-in-one-bar
    ambiguity cannot arise for this strategy).
  * `truncation_invariance` is an empirical look-ahead test: re-run a config on
    data cut at several points; every trade that completed before the cut must
    be identical to the full-data run. Any indicator or decision that peeks at
    future bars breaks this.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.channel_breakout.backtest import ChannelData, SimResult, simulate_channel
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9


def check_sim_integrity(sim: SimResult, data: ChannelData, exec_config: ExecutionConfig) -> list[str]:
    issues: list[str] = []
    if len(sim.entry_idx) == 0:
        return issues
    if (sim.entry_idx <= sim.signal_idx).any():
        issues.append("entry_not_after_signal_bar")
    if (sim.exit_idx < sim.entry_idx).any():
        issues.append("exit_before_entry")
    if len(sim.entry_idx) > 1 and (sim.entry_idx[1:] <= sim.exit_idx[:-1]).any():
        issues.append("overlapping_positions")
    if (sim.entry_px < data.open[sim.entry_idx] - _EPS).any():
        issues.append("entry_fill_better_than_open")
    stop = ~sim.forced_close
    if stop.any():
        raw = np.minimum(data.open[sim.exit_idx[stop]], sim.stop_level[stop])
        if (sim.exit_px[stop] > raw + _EPS).any():
            issues.append("stop_fill_better_than_min_open_stop")
    if sim.forced_close[:-1].any():
        issues.append("forced_close_not_final_trade")
    if (sim.entry_commission < exec_config.commission_minimum - _EPS).any():
        issues.append("commission_below_minimum")
    if any(t.target_price is not None for t in sim.trades):
        issues.append("unexpected_profit_target")
    return issues


def truncation_invariance(
    bars: pl.DataFrame, cfg, *, exec_config: ExecutionConfig, atr_period: int,
    cut_fracs: tuple[float, ...] = (0.35, 0.6, 0.85),
) -> list[str]:
    """Return a list of mismatch descriptions (empty = no look-ahead detected)."""
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_channel(ChannelData(bars, atr_period=atr_period), cfg,
                            exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_channel(ChannelData(bars.head(cut), atr_period=atr_period), cfg,
                                exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("entry_idx", "exit_idx", "quantity", "entry_px", "exit_px"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
