"""Stage 1 -- backtest integrity checks for the drift-burst backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. The burst statistic, the time-of-day
    volume norm and the news zones are recomputed here independently (per-session sliding
    windows and plain dictionaries, not the backtester's cumulative sums and polars code), then:
    each trade's decision bar meets its entry mode (fresh cross / peak that stopped rising /
    two falling bars) with |T| > threshold, on the fade side, with the side / volume / news
    filters met; at most `max_trades` per session; no qualifying signal was skipped while flat
    with trades left that day; stops and targets sit where the rule puts them, every stop or
    target exit was really touched (and was the first touch, stop first), with fills no better
    than the rule; the entry filled at the next
    bar's open of the SAME session at an adverse price; time and session exits happened on the
    right bar at the close; nothing is held overnight; no overlapping positions, no leverage,
    and only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.strategies.drift_burst.backtest import DBData, SimResult, as_params, simulate_drift_burst
from src.strategies.drift_burst.config import (
    ENTRY_LAG,
    NEWS_ZONES,
    VOL_LOOKBACK_MULT,
    VOLUME_LOOKBACK_SESSIONS,
    VOLUME_MIN_SESSIONS,
    WED_ZONES,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9
_TOL = 1e-7   # relative tolerance between the two implementations of T and the volume ratio

CHECKS = ["peak_below_threshold", "peak_still_rising", "not_a_fresh_cross", "not_confirmed",
          "side_not_fade", "side_not_allowed",
          "volume_gate_not_met", "inside_news_zone", "too_many_trades_in_session",
          "stop_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule",
          "target_not_per_rule", "target_exit_without_touch", "target_fill_better_than_rule",
          "exit_not_at_first_touch",
          "signal_skipped_while_flat", "entry_not_next_bar_same_session", "entry_fill_better_than_market",
          "exit_before_entry", "position_held_overnight", "time_exit_not_per_rule",
          "eod_exit_not_at_session_close", "exit_fill_better_than_market", "overlapping_positions",
          "position_exceeds_equity", "forced_close_not_final_trade", "commission_below_minimum"]


def independent_tstat(data: DBData, k: int) -> np.ndarray:
    """T per bar, session by session with sliding windows."""
    m = VOL_LOOKBACK_MULT * k
    T = np.full(data.n, np.nan)
    for a, b in zip(data.day_start_idx, data.day_end_idx):
        lc = np.log(data.close[a:b + 1])
        L = len(lc)
        if L <= m + k:
            continue
        r1 = np.diff(lc)                                   # r1[j] = return of bar a+j+1
        sq = sliding_window_view(r1 ** 2, m).mean(axis=1)  # sq[j] = mean over bars a+j+1 .. a+j+m
        for i in range(m + k, L):                          # bar a+i, window ends at bar a+i-k
            s = np.sqrt(sq[i - k - m])
            if s > 0:
                T[a + i] = (lc[i] - lc[i - k]) / (s * np.sqrt(k))
    return T


def independent_vnorm(data: DBData) -> np.ndarray:
    hist: dict[int, list[float]] = {}
    out = np.full(data.n, np.nan)
    for i in range(data.n):
        h = hist.setdefault(int(data.tod[i]), [])
        last = h[-VOLUME_LOOKBACK_SESSIONS:]
        if len(last) >= VOLUME_MIN_SESSIONS:
            out[i] = float(np.mean(last))
        h.append(float(data.volume[i]))
    return out


def independent_ratio(data: DBData, k: int, i: int, vn: np.ndarray) -> float:
    a = i - k + 1
    if a < data.sess_start[i]:
        return np.nan
    w = vn[a:i + 1]
    if not np.isfinite(w).all() or w.sum() <= 0:
        return np.nan
    return float(data.volume[a:i + 1].sum() / w.sum())


def in_news(data: DBData, k: int, t: int, lag: int = 1) -> bool:
    s = max(t - lag - k + 1, int(data.sess_start[t]))
    lo, hi = int(data.tod[s]), int(data.tod[t])
    zones = list(NEWS_ZONES) + (list(WED_ZONES) if data.weekday[t] == 2 else [])
    return any(lo <= z1 and hi >= z0 for z0, z1 in zones)


def _qualifies(data, p, T, vn, t, tol) -> tuple[int, str | None]:
    """(side, first failed check or None) for a decision at bar t."""
    lag = ENTRY_LAG[p.entry_mode]
    r = t - lag
    if r - 1 < 0 or data.sess[r - 1] != data.sess[t] or data.is_last[t]:
        return 0, "entry_not_next_bar_same_session"
    tr = T[r]
    if not (np.isfinite(tr) and abs(tr) > p.threshold * (1 - tol)):
        return 0, "peak_below_threshold"
    if p.entry_mode == "cross":
        tm = T[t - 1]
        if np.isfinite(tm) and np.sign(tm) == np.sign(tr) and abs(tm) > p.threshold * (1 + tol):
            return 0, "not_a_fresh_cross"
    else:
        t1 = T[r + 1]
        if np.isfinite(t1) and np.sign(t1) == np.sign(tr) and abs(t1) >= abs(tr) * (1 + tol):
            return 0, "peak_still_rising"
        if p.entry_mode == "confirm":
            t2 = T[r + 2]
            a1, a2 = (abs(t1) if np.isfinite(t1) else 0.0), (abs(t2) if np.isfinite(t2) else 0.0)
            flip = np.isfinite(t1) and np.isfinite(t2) and np.sign(t1) != np.sign(t2)
            if not (a2 < a1 * (1 + tol) or flip):
                return 0, "not_confirmed"
    side = -int(np.sign(tr))
    if p.side == "long_only" and side < 0:
        return side, "side_not_allowed"
    if p.vol_gate is not None:
        rr = independent_ratio(data, p.burst_window, r, vn)
        if not (np.isfinite(rr) and rr >= p.vol_gate * (1 - tol)):
            return side, "volume_gate_not_met"
    if p.news_filter == "on" and in_news(data, p.burst_window, t, lag):
        return side, "inside_news_zone"
    return side, None


def check_sim_integrity(sim: SimResult, data: DBData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    k = p.burst_window
    T = data._get(("indep_T", k), lambda: independent_tstat(data, k))
    vn = data._get(("indep_vnorm",), lambda: independent_vnorm(data))
    k_, e_, x_, d_ = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.side
    o, c = data.open, data.close

    # Strict candidates (tol < 0) for the skipped-signal check, so float differences between the
    # two implementations never raise a false flag.
    def strict_ok(t):
        side, why = _qualifies(data, p, T, vn, t, -_TOL)
        return why is None and side != 0
    lag = ENTRY_LAG[p.entry_mode]
    with np.errstate(invalid="ignore"):
        big = np.abs(T) > p.threshold
    cand = np.flatnonzero(big) + lag
    cand = cand[cand < data.n]
    free_from, ti = 0, 0
    done_in: dict[int, int] = {}
    for t in cand:
        while ti < len(k_) and k_[ti] < t:
            free_from = int(x_[ti]) + 1
            s_ = int(data.sess[k_[ti]])
            done_in[s_] = done_in.get(s_, 0) + 1
            ti += 1
        if ti < len(k_) and k_[ti] == t:
            continue
        if t < free_from or done_in.get(int(data.sess[t]), 0) >= p.max_trades:
            continue
        if t + 1 > data.sess_end[t] or t + 1 >= data.n:
            continue
        if sim.forced_close.any() and t > int(x_[-1]):
            continue
        if strict_ok(int(t)):
            issues.add("signal_skipped_while_flat")
            break

    seen_sess: dict[int, int] = {}
    h, lo = data.high, data.low
    for i in range(len(e_)):
        t, e, x, d = int(k_[i]), int(e_[i]), int(x_[i]), int(d_[i])
        side, why = _qualifies(data, p, T, vn, t, _TOL)
        if why is not None:
            issues.add(why)
        elif side != d:
            issues.add("side_not_fade")
        s = int(data.sess[t])
        seen_sess[s] = seen_sess.get(s, 0) + 1
        if seen_sess[s] > p.max_trades:
            issues.add("too_many_trades_in_session")
        if e < t + 1 or data.sess[e] != data.sess[t]:
            issues.add("entry_not_next_bar_same_session")
        if abs(sim.entry_base[i] - o[e]) > _EPS or d * (sim.entry_px[i] - o[e]) < -_EPS:
            issues.add("entry_fill_better_than_market")
        if x < e:
            issues.add("exit_before_entry")
        if data.sess[x] != data.sess[e]:
            issues.add("position_held_overnight")
        L = int(data.sess_end[e])
        T_exit = e + p.hold - 1
        r = t - lag
        B = abs(data.close[r] - data.close[r - p.burst_window])
        stop = o[e] - d * p.stop * B if p.stop is not None else np.nan
        tgt = o[e] + d * p.target * B if p.target is not None else np.nan
        if (p.stop is None) != (not np.isfinite(sim.stop_level[i])) or \
                (p.stop is not None and abs(sim.stop_level[i] - stop) > 1e-9 * max(1.0, abs(stop))):
            issues.add("stop_not_per_rule")
        if (p.target is None) != (not np.isfinite(sim.target_level[i])) or \
                (p.target is not None and abs(sim.target_level[i] - tgt) > 1e-9 * max(1.0, abs(tgt))):
            issues.add("target_not_per_rule")
        stop_hit = (lambda j: False) if p.stop is None else ((lambda j: lo[j] <= stop) if d > 0 else (lambda j: h[j] >= stop))
        tgt_hit = (lambda j: False) if p.target is None else ((lambda j: h[j] >= tgt) if d > 0 else (lambda j: lo[j] <= tgt))
        for j in range(e, x):
            if stop_hit(j) or tgt_hit(j):
                issues.add("exit_not_at_first_touch")
                break
        why = sim.exit_reason[i]
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            worst = min(o[x], stop) if d > 0 else max(o[x], stop)
            if d * (worst - sim.exit_px[i]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
            if x > min(T_exit, L):
                issues.add("time_exit_not_per_rule")
        elif why == "target_exit":
            if not tgt_hit(x) or stop_hit(x):
                issues.add("target_exit_without_touch")
            best = max(o[x], tgt) if d > 0 else min(o[x], tgt)
            if d * (best - sim.exit_px[i]) < -_EPS:
                issues.add("target_fill_better_than_rule")
            if x > min(T_exit, L):
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if x != T_exit or x >= L or stop_hit(x) or tgt_hit(x):
                issues.add("time_exit_not_per_rule")
            if d * (c[x] - sim.exit_px[i]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        else:
            if x != L or T_exit < L or stop_hit(x) or tgt_hit(x):
                issues.add("eod_exit_not_at_session_close")
            if d * (c[x] - sim.exit_px[i]) < -_EPS:
                issues.add("exit_fill_better_than_market")

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
    full = simulate_drift_burst(DBData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_drift_burst(DBData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
