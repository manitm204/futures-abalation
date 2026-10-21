"""Stage 1 -- backtest integrity checks for the moving-average crossover backtester.

Two layers:
  * `check_sim_integrity` runs on EVERY config's simulation: the signal bar c sits
    in a tradable bullish run (fast > slow on every bar from the crossover bar k
    through c, after a defined non-bullish bar k-1), the run has lasted at least
    confirm_bars bars, the MA separation clears buffer_atr x ATR(14)_c, the slow MA
    is rising over SLOPE_BARS bars when the slope filter is on (v2: ADX(14)_c >= min_adx,
    close_c - slow_c <= max_extension_atr x ATR(14)_c), c is the first bar of its run
    meeting all of these at or after the previous exit + cooldown_bars, each run is
    traded at most once, the entry fills after c, stop and target come from the ATR
    known before the fill, stop exits really touched the stop and filled no better
    than min(open, stop), target exits really touched the target, filled no better
    than it and were not on a stop bar, crossover exits are decided at the first close
    after c with fast <= slow (never before the entry bar, never after the max_hold
    close) and time exits at the max_hold close before any cross, both filling at the
    next open, no bar before the exit touched the stop or target, no overlapping
    positions, adverse entry fill, no leverage, commission minimum respected, only
    the final trade may be force-closed.
  * `truncation_invariance` is an empirical look-ahead test: re-run a config on
    data cut at several points; every trade that completed before the cut must
    be identical to the full-data run. Any MA or decision that peeks at future
    bars breaks this.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.ma_crossover.backtest import MAData, SimResult, as_params, simulate_ma_crossover
from src.strategies.ma_crossover.config import SLOPE_BARS
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["entry_signal_condition_not_met", "signal_not_first_in_run", "run_traded_twice",
          "entry_not_after_signal_bar", "exit_before_entry", "exit_decided_before_entry",
          "cross_exit_not_at_first_cross", "exit_not_next_open_after_decision", "overlapping_positions",
          "entry_fill_better_than_open", "exit_fill_better_than_open", "position_exceeds_equity",
          "forced_close_not_final_trade", "commission_below_minimum", "stop_not_from_atr_known_before_entry",
          "stop_exit_without_stop", "stop_exit_without_touch", "stop_fill_better_than_min_open_stop",
          "stop_touched_before_exit", "buffer_filter_violated", "slope_filter_violated",
          "adx_filter_violated", "extension_filter_violated", "entry_during_cooldown",
          "target_not_from_atr_known_before_entry", "target_exit_without_target", "target_exit_without_touch",
          "target_fill_better_than_target", "target_exit_on_stop_bar", "time_exit_not_at_max_hold",
          "cross_exit_after_max_hold", "holding_period_exceeds_max_hold"]


def _signal_ok(data: MAData, cfg, t: np.ndarray) -> np.ndarray:
    """Bool per bar index in `t`: do the entry conditions hold at that bar's close?
    Recomputed here from the raw indicators (not the simulator's cached mask)."""
    bull, start, valid = data.regimes(cfg.ma_pair, cfg.fast_length, cfg.slow_length)
    slow = data.ma(cfg.ma_pair.split("/")[1], cfg.slow_length)
    ok = valid[t] & (t - start[t] + 1 >= cfg.confirm_bars)
    with np.errstate(invalid="ignore"):
        if cfg.buffer_atr:
            ok &= data.diff(cfg.ma_pair, cfg.fast_length, cfg.slow_length)[t] >= cfg.buffer_atr * data.atr[t] - _EPS
        if cfg.slope_filter:
            ok &= (t >= SLOPE_BARS) & (slow[t] > slow[np.maximum(t - SLOPE_BARS, 0)])
        if cfg.min_adx is not None:
            ok &= data.adx[t] >= cfg.min_adx - _EPS
        if cfg.max_extension_atr is not None:
            ok &= data.close[t] - slow[t] <= cfg.max_extension_atr * data.atr[t] + _EPS
    return ok


def check_sim_integrity(sim: SimResult, data: MAData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: list[str] = []
    if len(sim.entry_idx) == 0:
        return issues
    cfg = as_params(cfg)
    c, k = sim.signal_idx, sim.cross_idx
    d = data.diff(cfg.ma_pair, cfg.fast_length, cfg.slow_length)
    bull, start, valid = data.regimes(cfg.ma_pair, cfg.fast_length, cfg.slow_length)

    # The run: bullish on every bar k..c, k-1 defined and not bullish.
    run_ok = (k > 0) & (k <= c) & np.isfinite(d[np.maximum(k - 1, 0)]) & ~bull[np.maximum(k - 1, 0)]
    run_ok &= np.array([bool((d[a:b + 1] > 0).all()) for a, b in zip(k, c)])
    if not (run_ok & _signal_ok(data, cfg, c)).all():
        issues.append("entry_signal_condition_not_met")
    if cfg.buffer_atr and not (d[c] >= cfg.buffer_atr * data.atr[c] - _EPS).all():
        issues.append("buffer_filter_violated")
    if cfg.slope_filter:
        slow = data.ma(cfg.ma_pair.split("/")[1], cfg.slow_length)
        if not ((c >= SLOPE_BARS) & (slow[c] > slow[np.maximum(c - SLOPE_BARS, 0)])).all():
            issues.append("slope_filter_violated")
    if cfg.min_adx is not None and not (data.adx[c] >= cfg.min_adx - _EPS).all():
        issues.append("adx_filter_violated")
    if cfg.max_extension_atr is not None:
        slow = data.ma(cfg.ma_pair.split("/")[1], cfg.slow_length)
        if not (data.close[c] - slow[c] <= cfg.max_extension_atr * data.atr[c] + _EPS).all():
            issues.append("extension_filter_violated")
    # Earliest allowed signal bar: the previous exit bar + cooldown (0 for the first trade).
    allowed = np.concatenate([[0], sim.exit_idx[:-1] + cfg.cooldown_bars])
    if (c < allowed).any():
        issues.append("entry_during_cooldown")
    if any(bool(_signal_ok(data, cfg, np.arange(max(a, lo_), b)).any()) for a, b, lo_ in zip(k, c, allowed)):
        issues.append("signal_not_first_in_run")
    if len(np.unique(k)) != len(k):
        issues.append("run_traded_twice")
    if (sim.entry_idx <= c).any():
        issues.append("entry_not_after_signal_bar")
    if (sim.exit_idx < sim.entry_idx).any():
        issues.append("exit_before_entry")

    a_known = data.atr[sim.entry_idx - 1]
    raw = data.open[sim.entry_idx]
    stop_ok = np.allclose(sim.atr_used, a_known, rtol=0, atol=1e-12)
    if cfg.stop_atr is not None:
        stop_ok &= np.allclose(sim.stop_level, raw - cfg.stop_atr * a_known, rtol=0, atol=1e-9)
    else:
        stop_ok &= bool(np.isnan(sim.stop_level).all())
    if not stop_ok:
        issues.append("stop_not_from_atr_known_before_entry")
    if cfg.take_profit_atr is not None:
        tgt_ok = np.allclose(sim.target_level, raw + cfg.take_profit_atr * a_known, rtol=0, atol=1e-9)
    else:
        tgt_ok = bool(np.isnan(sim.target_level).all())
    if not tgt_ok:
        issues.append("target_not_from_atr_known_before_entry")

    done = ~sim.forced_close
    stopped = sim.exit_reason == "stop_exit"
    crossed = sim.exit_reason == "cross_exit"
    target = sim.exit_reason == "target_exit"
    timed = sim.exit_reason == "time_exit"
    H = cfg.max_hold
    if done.any() and (sim.decision_idx[done] < sim.entry_idx[done]).any():
        issues.append("exit_decided_before_entry")
    if crossed.any():
        cc, e = c[crossed], sim.entry_idx[crossed]
        with np.errstate(invalid="ignore"):
            nb = np.flatnonzero(~(d > 0))  # bars with fast <= slow (or undefined)
        pos = np.searchsorted(nb, cc + 1)
        first = np.where(pos < len(nb), nb[np.minimum(pos, len(nb) - 1)], -1)
        if (sim.decision_idx[crossed] != np.maximum(first, e)).any() or (first < 0).any():
            issues.append("cross_exit_not_at_first_cross")
        if H is not None and (sim.decision_idx[crossed] > e + H - 1).any():
            issues.append("cross_exit_after_max_hold")
    if timed.any():
        e = sim.entry_idx[timed]
        with np.errstate(invalid="ignore"):
            nb = np.flatnonzero(~(d > 0))
        pos = np.searchsorted(nb, c[timed] + 1)
        first = np.where(pos < len(nb), nb[np.minimum(pos, len(nb) - 1)], data.n)
        if H is None or (sim.decision_idx[timed] != e + H - 1).any() or \
                (np.maximum(first, e) <= sim.decision_idx[timed]).any():
            issues.append("time_exit_not_at_max_hold")
    sig_exit = crossed | timed
    if sig_exit.any():
        if (sim.exit_idx[sig_exit] != sim.decision_idx[sig_exit] + 1).any():
            issues.append("exit_not_next_open_after_decision")
        if (sim.exit_px[sig_exit] > data.open[sim.exit_idx[sig_exit]] + _EPS).any():
            issues.append("exit_fill_better_than_open")
    if target.any():
        if cfg.take_profit_atr is None:
            issues.append("target_exit_without_target")
        else:
            xi = sim.exit_idx[target]
            if (data.high[xi] < sim.target_level[target] - _EPS).any():
                issues.append("target_exit_without_touch")
            if (sim.exit_px[target] > sim.target_level[target] + _EPS).any():
                issues.append("target_fill_better_than_target")
            if cfg.stop_atr is not None and (data.low[xi] <= sim.stop_level[target] + _EPS).any():
                issues.append("target_exit_on_stop_bar")
    if H is not None and done.any() and (sim.exit_idx[done] - sim.entry_idx[done] > H).any():
        issues.append("holding_period_exceeds_max_hold")
    if stopped.any():
        if cfg.stop_atr is None:
            issues.append("stop_exit_without_stop")
        else:
            xi = sim.exit_idx[stopped]
            if (data.low[xi] > sim.stop_level[stopped] + _EPS).any():
                issues.append("stop_exit_without_touch")
            if (sim.exit_px[stopped] > np.minimum(data.open[xi], sim.stop_level[stopped]) + _EPS).any():
                issues.append("stop_fill_better_than_min_open_stop")
    # No bar from the entry bar up to (excluding) the exit bar may touch the stop or the
    # target: the first touch must be the exit (for cross / time exits this covers the
    # decision bar too).
    if (cfg.stop_atr is not None or cfg.take_profit_atr is not None) and done.any():
        e, x = sim.entry_idx[done], sim.exit_idx[done]
        held = e[:, None] + np.arange(max(int((x - e).max()), 1))[None, :]
        live = held < x[:, None]
        held = np.minimum(held, data.n - 1)
        with np.errstate(invalid="ignore"):
            touched = (data.low[held] <= sim.stop_level[done][:, None]) | \
                      (data.high[held] >= sim.target_level[done][:, None])
        if (touched & live).any():
            issues.append("stop_touched_before_exit")
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
    full = simulate_ma_crossover(MAData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_ma_crossover(MAData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "cross_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
