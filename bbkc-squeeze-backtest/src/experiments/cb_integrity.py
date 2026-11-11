"""Stage 1 -- backtest integrity checks for the compression-breakout backtester.

Two layers, as for the other families (src/experiments/integrity.py, nb_integrity.py):
  * `check_sim_integrity` runs on EVERY config's simulation. The compression flags, the
    trend EMA and the run / box behind each trade are recomputed here independently (numpy
    sliding windows and pandas, not the backtester's polars code), then: the box was built
    only from bars before the decision, the setup was live and this was the run's FIRST
    breakout, the breakout condition and filters held, the entry filled on the right bar of
    the SAME session at an adverse price, the stop / target sit where the rules put them,
    every stop / target exit was really touched (and was the first touch), session-close
    exits filled at the last close, nothing is held overnight, no overlapping positions, no
    leverage, and only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed
    before the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.strategies.compression_breakout.backtest import (
    CBData,
    SimResult,
    as_params,
    simulate_compression_breakout,
)
from src.strategies.compression_breakout.config import ATR_PERIOD, BB_STD, TREND_EMA
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["box_not_from_prior_compression_run", "setup_not_live", "not_first_breakout_of_run",
          "entry_signal_condition_not_met", "direction_not_allowed", "entry_against_trend",
          "entry_inside_last_entry_cutoff", "entry_not_after_signal_same_session", "exit_before_entry",
          "position_held_overnight", "entry_fill_better_than_market", "stop_not_per_rule",
          "target_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule",
          "target_exit_without_touch", "target_fill_better_than_rule", "target_taken_when_stop_touched",
          "exit_not_at_first_touch", "eod_exit_not_at_session_close", "exit_fill_better_than_market",
          "overlapping_positions", "position_exceeds_equity", "forced_close_not_final_trade",
          "commission_below_minimum"]


def _rolling(x: np.ndarray, w: int, fn) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) >= w:
        out[w - 1:] = fn(sliding_window_view(x, w), axis=1)
    return out


def independent_compression(data: CBData, p) -> np.ndarray:
    """Compression flag per bar, recomputed without the backtester's code (ATR excepted:
    src/features/atr.py is unit-tested on its own)."""
    if p.compression == "bbkc":
        sd = _rolling(data.close, p.squeeze_length, np.std)  # population sd (ddof=0)
        with np.errstate(invalid="ignore"):
            return BB_STD * sd < p.kc_mult * data.atr(p.squeeze_length)
    rng = data.high - data.low
    with np.errstate(invalid="ignore"):
        out = rng <= _rolling(rng, p.nr_lookback, np.min) + 1e-12
    if p.inside_bar:
        prev_h = np.concatenate([[np.inf], data.high[:-1]])
        prev_l = np.concatenate([[-np.inf], data.low[:-1]])
        out &= (data.high <= prev_h) & (data.low >= prev_l) & (np.arange(len(rng)) > 0)
    return out


def _box_at(comp: np.ndarray, data: CBData, k: int) -> tuple[int, int] | None:
    """(run start, last compression bar) of the run live at bar k: the last compression bar
    of k's session before k, and the run it closes."""
    s0 = int(data.sess_start[k])
    j = k - 1
    while j >= s0 and not comp[j]:
        j -= 1
    if j < s0:
        return None
    r = j
    while j - 1 >= s0 and comp[j - 1]:
        j -= 1
    return j, r


def check_sim_integrity(sim: SimResult, data: CBData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    if len(sim.entry_idx) == 0:
        return []
    p = as_params(cfg)
    comp = independent_compression(data, p)
    ema = pd.Series(data.close).ewm(span=TREND_EMA, adjust=False, min_periods=TREND_EMA).mean().to_numpy()
    wick = p.entry_type == "wick"
    atr14 = data.atr(ATR_PERIOD)

    def wide(r: int, b_h: float, b_l: float) -> bool:
        return p.min_box_atr <= 0 or bool(b_h - b_l >= p.min_box_atr * atr14[r])  # NaN ATR -> False
    k_, e_, x_, d_ = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.side
    o, h, lo, c = data.open, data.high, data.low, data.close

    def broke(k: int, bh: float, bl: float) -> tuple[bool, bool]:
        return ((h[k] > bh, lo[k] < bl) if wick else (c[k] > bh, c[k] < bl))

    for t in range(len(e_)):
        k, e, x, d = int(k_[t]), int(e_[t]), int(x_[t]), int(d_[t])
        run = _box_at(comp, data, k)
        if run is None:
            issues.add("box_not_from_prior_compression_run")
            continue
        s, r = run
        bh, bl = float(h[s:r + 1].max()), float(lo[s:r + 1].min())
        if s != sim.run_start[t] or abs(bh - sim.box_hi[t]) > _EPS or abs(bl - sim.box_lo[t]) > _EPS:
            issues.add("box_not_from_prior_compression_run")
        if not (k - r <= p.setup_expiry_bars and r - s + 1 >= p.min_run and wide(r, bh, bl)):
            issues.add("setup_not_live")
        up, dn = broke(k, bh, bl)
        if not ((d > 0 and up and not dn) or (d < 0 and dn and not up)):
            issues.add("entry_signal_condition_not_met")
        # An earlier live breakout of the same run would have consumed it. Bars s..r are the
        # run and r+1..k-1 are not compression, so bar k2's last compression bar is min(k2-1, r).
        b_h, b_l = -np.inf, np.inf
        for k2 in range(s + 1, k):
            r2 = min(k2 - 1, r)
            b_h, b_l = max(b_h, h[r2]), min(b_l, lo[r2])
            if (k2 - r2 <= p.setup_expiry_bars and r2 - s + 1 >= p.min_run and wide(r2, b_h, b_l)
                    and any(broke(k2, b_h, b_l))):
                issues.add("not_first_breakout_of_run")
                break
        if p.trend_filter == "ema50":
            j = k - 1 if wick else k
            if not (np.isfinite(ema[j]) and (c[j] > ema[j] if d > 0 else c[j] < ema[j])):
                issues.add("entry_against_trend")
        gap = (data.bar_open[data.sess_end[k]] - data.bar_open[k]).astype("timedelta64[m]").astype(np.int64)
        if data.is_last[k] or gap < p.last_entry_cutoff:
            issues.add("entry_inside_last_entry_cutoff")
        if e < (k if wick else k + 1) or data.sess[e] != data.sess[k]:
            issues.add("entry_not_after_signal_same_session")
        intrabar = wick and e == k
        base = (max(o[e], bh) if d > 0 else min(o[e], bl)) if intrabar else o[e]
        if abs(sim.entry_base[t] - base) > _EPS or d * (sim.entry_px[t] - base) < -_EPS:
            issues.add("entry_fill_better_than_market")
        if p.stop_atr is None:
            stop = bl if d > 0 else bh
        else:
            stop = base - d * p.stop_atr * atr14[e - 1]
        if not abs(sim.stop_level[t] - stop) <= 1e-9 * max(1.0, abs(stop)):
            issues.add("stop_not_per_rule")
        risk = d * (base - stop)
        if p.target_r is None:
            if np.isfinite(sim.target_level[t]):
                issues.add("target_not_per_rule")
        elif not abs(sim.target_level[t] - (base + d * p.target_r * risk)) <= 1e-9 * max(1.0, abs(base)):
            issues.add("target_not_per_rule")
        stop_hit = (lambda j: lo[j] <= stop) if d > 0 else (lambda j: h[j] >= stop)
        tgt = sim.target_level[t]
        tgt_hit = (lambda j: np.isfinite(tgt) and (h[j] >= tgt if d > 0 else lo[j] <= tgt))
        for j in range(e, x):  # bars before the exit bar: no touch that should have exited
            if stop_hit(j) or (tgt_hit(j) and not (intrabar and j == e)):
                issues.add("exit_not_at_first_touch")
                break
        why = sim.exit_reason[t]
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            worst = stop if (intrabar and x == e) else (min(o[x], stop) if d > 0 else max(o[x], stop))
            if d * (worst - sim.exit_px[t]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
        elif why == "target_exit":
            if not tgt_hit(x) or (intrabar and x == e):
                issues.add("target_exit_without_touch")
            if stop_hit(x):
                issues.add("target_taken_when_stop_touched")
            best = max(o[x], tgt) if d > 0 else min(o[x], tgt)
            if d * (best - sim.exit_px[t]) < -_EPS:
                issues.add("target_fill_better_than_rule")
        else:  # eod_exit / forced_close
            if x != data.sess_end[e] or stop_hit(x) or (tgt_hit(x) and not (intrabar and x == e)):
                issues.add("eod_exit_not_at_session_close")
            if d * (c[x] - sim.exit_px[t]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        if x < e:
            issues.add("exit_before_entry")
        if data.sess[x] != data.sess[e]:
            issues.add("position_held_overnight")
        if (p.direction == "long" and d < 0) or (p.direction == "short" and d > 0):
            issues.add("direction_not_allowed")

    if len(e_) > 1 and (e_[1:] <= x_[:-1]).any():
        issues.add("overlapping_positions")
    eq_before = exec_config.starting_equity + np.concatenate([[0.0], np.cumsum(sim.realized_pnl)[:-1]])
    raw_entry = sim.entry_px - data.price_adj[e_]
    if (sim.quantity * raw_entry + sim.entry_commission > eq_before + 1e-6).any():
        issues.add("position_exceeds_equity")
    if sim.forced_close[:-1].any():
        issues.add("forced_close_not_final_trade")
    if (sim.entry_commission < exec_config.commission_minimum - _EPS).any():
        issues.add("commission_below_minimum")
    return [x for x in CHECKS if x in issues]


def truncation_invariance(
    bars: pl.DataFrame, cfg, *, exec_config: ExecutionConfig,
    cut_fracs: tuple[float, ...] = (0.35, 0.6, 0.85),
) -> list[str]:
    """Return a list of mismatch descriptions (empty = no look-ahead detected)."""
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_compression_breakout(CBData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_compression_breakout(CBData(bars.head(cut)), cfg, exec_config=exec_config,
                                             starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px", "side",
                     "stop_level", "box_hi", "box_lo"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
