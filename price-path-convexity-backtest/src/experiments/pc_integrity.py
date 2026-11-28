"""Stage 1 -- backtest integrity checks for the price-path convexity backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. The signal, its z-score, the net
    move and the trend EMA are recomputed here independently (plain numpy loops / sliding
    windows, not the backtester's pandas code), then: each trade's decision bar was a fresh
    cross of the threshold on the right side, the quadrant / minimum-move / direction / trend /
    entry-window filters held, no earlier qualifying signal was skipped while flat, the entry
    filled at the next bar's open of the SAME session at an adverse price, the stop sits where
    the rule puts it, every stop exit was really touched (and was the first touch), time and
    session exits happened on the right bar at the close, nothing is held overnight, no
    overlapping positions, no leverage, and only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.experiments.cb_integrity import _rolling
from src.strategies.path_convexity.backtest import (
    PCData,
    SimResult,
    as_params,
    simulate_path_convexity,
)
from src.strategies.path_convexity.config import ATR_PERIOD, trend_ema_span
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["signal_not_fresh_cross", "side_not_per_signal", "quadrant_not_allowed", "net_move_below_minimum",
          "direction_not_allowed", "entry_against_trend", "entry_inside_last_entry_cutoff",
          "signal_skipped_while_flat", "entry_not_next_bar_same_session", "entry_fill_better_than_market",
          "exit_before_entry", "position_held_overnight", "stop_not_per_rule", "stop_exit_without_touch",
          "stop_fill_better_than_rule", "exit_not_at_first_touch", "time_exit_not_per_rule",
          "held_past_time_stop", "eod_exit_not_at_session_close", "exit_fill_better_than_market",
          "overlapping_positions", "position_exceeds_equity", "forced_close_not_final_trade",
          "commission_below_minimum"]


def independent_signal(close: np.ndarray, atr: np.ndarray, form: str, n: int) -> np.ndarray:
    out = np.full(len(close), np.nan)
    if len(close) < n:
        return out
    W = sliding_window_view(close, n)
    p1, pn = W[:, 0], W[:, -1]
    a = atr[n - 1:]
    with np.errstate(invalid="ignore", divide="ignore"):
        if form == "reversal":
            s = (pn - p1) / a
        else:
            line = p1[:, None] + (pn - p1)[:, None] * (np.arange(n) / (n - 1))[None, :]
            g = line - W  # mean(line) == midpoint, so mean(g) == midpoint - mean(path)
            if form == "maxgap":
                s = g[np.arange(len(g)), np.abs(g).argmax(axis=1)] / a
            elif form == "atr":
                s = g.mean(axis=1) / a
            else:
                mid = (p1 + pn) / 2
                s = np.where(np.abs(mid) > 1e-9, g.mean(axis=1) / mid, np.nan)
    out[n - 1:] = s
    return out


def independent_z(sig: np.ndarray, zl: int) -> np.ndarray:
    m = _rolling(sig, zl, np.mean)
    sd = _rolling(sig, zl, np.std)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(sd > 0, (sig - m) / sd, np.nan)


def qualifying(data: PCData, p, tol: float = 1e-9) -> dict[str, np.ndarray]:
    """Per bar: the side (+1 / -1) a qualifying decision would take there, 0 = none. Built from
    the independent signal. tol > 0 is lenient (a cross within tol of the threshold counts: used
    to confirm the backtester's trades); tol < 0 is strict (used for the skipped-signal check),
    so floating-point differences between the two implementations never raise a false flag."""
    atr = data.atr(ATR_PERIOD)
    # Cached on the data object under their own keys (the backtester never reads them), so the
    # thousands of configs sharing a signal don't recompute it.
    sig = data._get(("indep_sig", p.signal_form, p.lookback),
                    lambda: independent_signal(data.close, atr, p.signal_form, p.lookback))
    z = data._get(("indep_z", p.signal_form, p.lookback, p.z_lookback),
                  lambda: independent_z(sig, p.z_lookback))
    zp = np.concatenate([[np.nan], z[:-1]])
    with np.errstate(invalid="ignore"):
        short = (z >= p.entry_z - tol) & ~(zp >= p.entry_z + tol)
        long_ = (z <= -p.entry_z + tol) & ~(zp <= -p.entry_z - tol)
    side = np.where(short & ~long_, -1, np.where(long_ & ~short, 1, 0))
    m = np.full(data.n, np.nan)
    if data.n >= p.lookback:
        m[p.lookback - 1:] = data.close[p.lookback - 1:] - data.close[:data.n - p.lookback + 1]
    sm = np.sign(np.nan_to_num(m))
    ok = side != 0
    ok &= {"long": side > 0, "short": side < 0, "both": np.ones(data.n, bool)}[p.direction]
    if p.quadrant == "late":
        ok &= side == -sm
    elif p.quadrant == "early":
        ok &= side == sm
    if p.min_move_atr > 0:
        with np.errstate(invalid="ignore"):
            ok &= np.abs(m) >= p.min_move_atr * atr
    span = trend_ema_span(p.trend_filter)
    if span is not None:
        ema = pd.Series(data.close).ewm(span=span, adjust=False, min_periods=span).mean().to_numpy()
        with np.errstate(invalid="ignore"):
            ok &= np.where(side > 0, data.close > ema, data.close < ema)
    regime = getattr(p, "regime", "none")
    if regime == "dtrend50":
        sess = pd.Series(data.close).groupby(data.sess).last()          # daily closes, session by session
        dsma = sess.rolling(50, min_periods=50).mean().shift(1)         # through the previous session
        ref = dsma.reindex(data.sess).to_numpy()
        with np.errstate(invalid="ignore"):
            ok &= np.where(side > 0, data.close > ref, data.close < ref)
    elif regime == "volhi":
        r = pd.Series(atr / data.close)
        med = r.rolling(1300, min_periods=1300).median().to_numpy()
        with np.errstate(invalid="ignore"):
            ok &= (r.to_numpy() >= med)
    if getattr(p, "window", "all") == "mid":
        # bar_open is UTC; the New York minute-of-day comes from pandas, not from the backtester's `tod`
        ny = pd.DatetimeIndex(data.bar_open).tz_localize("UTC").tz_convert("America/New_York")
        mins = (ny.hour * 60 + ny.minute).to_numpy() + 15
        ok &= (mins >= 600) & (mins <= 900)
    gap = (data.bar_open[data.sess_end] - data.bar_open).astype("timedelta64[m]").astype(np.int64)
    ok &= ~data.is_last & (gap >= p.last_entry_cutoff)
    return {"side": np.where(ok, side, 0), "raw_side": side, "z": z, "zp": zp, "move": m}


def check_sim_integrity(sim: SimResult, data: PCData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    q = qualifying(data, p)
    strict = qualifying(data, p, tol=-1e-9)["side"]
    k_, e_, x_, d_ = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.side
    o, h, lo, c = data.open, data.high, data.low, data.close
    atr14 = data.atr(ATR_PERIOD)
    H = p.hold_bars
    span = trend_ema_span(p.trend_filter)
    ema = (None if span is None else
           pd.Series(c).ewm(span=span, adjust=False, min_periods=span).mean().to_numpy())

    # Every qualifying bar while flat must have been taken (a missed entry only under stress).
    flat_from = 0
    for t in range(len(e_)):
        k = int(k_[t])
        skipped = np.flatnonzero(strict[flat_from:k] != 0) + flat_from
        for s in skipped:  # a skipped signal is fine only if its fill bar would leave the session
            if s + 1 <= data.sess_end[s] and s + 1 < data.n and (p.stop_atr is None or np.isfinite(atr14[s])):
                issues.add("signal_skipped_while_flat")
                break
        flat_from = int(x_[t])

    for t in range(len(e_)):
        k, e, x, d = int(k_[t]), int(e_[t]), int(x_[t]), int(d_[t])
        raw = q["raw_side"][k]
        if raw == 0:
            issues.add("signal_not_fresh_cross")
        elif raw != d:
            issues.add("side_not_per_signal")
        m = q["move"][k]
        sm = np.sign(m) if np.isfinite(m) else 0
        if (p.quadrant == "late" and d != -sm) or (p.quadrant == "early" and d != sm):
            issues.add("quadrant_not_allowed")
        if p.min_move_atr > 0 and not abs(m) >= p.min_move_atr * atr14[k]:
            issues.add("net_move_below_minimum")
        if (p.direction == "long" and d < 0) or (p.direction == "short" and d > 0):
            issues.add("direction_not_allowed")
        if ema is not None and not (np.isfinite(ema[k]) and (c[k] > ema[k] if d > 0 else c[k] < ema[k])):
            issues.add("entry_against_trend")
        gap = (data.bar_open[data.sess_end[k]] - data.bar_open[k]).astype("timedelta64[m]").astype(np.int64)
        if data.is_last[k] or gap < p.last_entry_cutoff:
            issues.add("entry_inside_last_entry_cutoff")
        if e < k + 1 or data.sess[e] != data.sess[k]:
            issues.add("entry_not_next_bar_same_session")
        if abs(sim.entry_base[t] - o[e]) > _EPS or d * (sim.entry_px[t] - o[e]) < -_EPS:
            issues.add("entry_fill_better_than_market")
        if p.stop_atr is None:
            stop = np.nan
            if np.isfinite(sim.stop_level[t]):
                issues.add("stop_not_per_rule")
        else:
            stop = o[e] - d * p.stop_atr * atr14[e - 1]
            if not abs(sim.stop_level[t] - stop) <= 1e-9 * max(1.0, abs(stop)):
                issues.add("stop_not_per_rule")
        stop_hit = ((lambda j: False) if p.stop_atr is None else
                    (lambda j: lo[j] <= stop) if d > 0 else (lambda j: h[j] >= stop))
        for j in range(e, x):
            if stop_hit(j):
                issues.add("exit_not_at_first_touch")
                break
        L = int(data.sess_end[e])
        T = e + H - 1 if H is not None else None
        why = sim.exit_reason[t]
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            worst = min(o[x], stop) if d > 0 else max(o[x], stop)
            if d * (worst - sim.exit_px[t]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
        elif why == "time_exit":
            if T is None or x != T or x >= L or stop_hit(x):
                issues.add("time_exit_not_per_rule")
            if d * (c[x] - sim.exit_px[t]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        else:  # eod_exit / forced_close
            if x != L or stop_hit(x) or (T is not None and T < L):
                issues.add("eod_exit_not_at_session_close")
            if d * (c[x] - sim.exit_px[t]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        if T is not None and x > T:
            issues.add("held_past_time_stop")
        if x < e:
            issues.add("exit_before_entry")
        if data.sess[x] != data.sess[e]:
            issues.add("position_held_overnight")

    if len(e_) > 1 and (e_[1:] <= x_[:-1]).any():
        issues.add("overlapping_positions")
    if len(e_):
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
    full = simulate_path_convexity(PCData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_path_convexity(PCData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
