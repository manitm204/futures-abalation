"""Stage 1 -- backtest integrity checks for the Silver Bullet backtester.

Two layers:
  * `check_sim_integrity` runs on EVERY config's simulation. ATR, swings, their first
    penetrations, sweeps, FVGs, the window filter, the sweep requirement, the limit / stop /
    target prices, the one-order-at-a-time rule and the limit fills are all recomputed with plain
    Python loops (not the backtester's numpy code). Then: every trade is one the rules call for
    (same setup bar, fill bar, side, limit, stop, target); none the rules call for is missing;
    entry fills are never BETTER than the limit / the bar's open;
    every stop / target exit was really touched (target: 1-tick trade-through, not on the fill
    bar) and was the first touch; time exits at the close of the window's last bar; every bar of a
    trade is inside the window interval of one session; no overlap, no leverage, one trade per
    session, only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import bisect

import numpy as np
import polars as pl

from src.strategies.mean_reversion.backtest import CostModel
from src.strategies.silver_bullet.backtest import SBData, SimResult, as_params, simulate_silver_bullet
from src.strategies.silver_bullet.config import (
    ATR_LEN,
    MIN_STOP_ATR,
    PAD_TICKS,
    STRUCT_FALLBACK_BARS,
    SWEEP_LOOKBACK_MIN,
    SWEEP_RECLAIM_BARS,
    THROUGH_TICKS,
    WINDOWS,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["setup_not_per_rule", "entry_not_per_rule", "wrong_direction", "trade_skipped_while_flat",
          "limit_not_per_rule", "entry_fill_better_than_rule", "exit_before_entry", "bar_outside_window",
          "position_held_overnight", "more_than_one_trade_per_session", "stop_not_per_rule",
          "target_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule",
          "target_exit_without_trade_through", "target_fill_not_at_target", "exit_not_at_first_touch",
          "time_exit_not_per_rule", "exit_fill_better_than_market", "overlapping_positions",
          "position_exceeds_equity", "forced_close_not_final_trade", "commission_below_minimum"]


def _sessions(data: SBData) -> list[tuple[int, int]]:
    out, a = [], 0
    for i in range(1, data.n + 1):
        if i == data.n or data.session_date[i] != data.session_date[a]:
            out.append((a, i - 1))
            a = i
    return out


def _features(data: SBData, L: int) -> dict:
    """ATR, swings + first penetrations, sweeps, all by explicit loops (cached per swing length)."""
    def build():
        h, lo, c = data.high.tolist(), data.low.tolist(), data.close.tolist()
        mins = data.minute.tolist()
        sess = _sessions(data)
        sid = [0] * data.n
        atr = [float("nan")] * data.n
        for s, (a, b) in enumerate(sess):
            trs = []
            for i in range(a, b + 1):
                sid[i] = s
                if i == a:
                    tr = h[i] - lo[i]
                else:
                    tr = max(h[i] - lo[i], abs(h[i] - c[i - 1]), abs(lo[i] - c[i - 1]))
                trs.append(tr)
                if len(trs) >= ATR_LEN:
                    atr[i] = sum(trs[-ATR_LEN:]) / ATR_LEN
        highs, lows = [], []  # (i, price, first penetration k or None)
        sweeps = {1: [], -1: []}  # (confirm j, extreme)
        for a, b in sess:
            for i in range(a + L, b - L + 1):
                if all(h[i] > h[j] for j in range(i - L, i)) and all(h[i] >= h[j] for j in range(i + 1, i + L + 1)):
                    k = next((j for j in range(i + 1, b + 1) if h[j] > h[i]), None)
                    highs.append((i, h[i], k))
                    if k is not None:
                        for j in range(k, min(k + SWEEP_RECLAIM_BARS - 1, b) + 1):
                            if c[j] < h[i]:
                                sweeps[-1].append((j, max(h[k:j + 1])))
                                break
                if all(lo[i] < lo[j] for j in range(i - L, i)) and all(lo[i] <= lo[j] for j in range(i + 1, i + L + 1)):
                    k = next((j for j in range(i + 1, b + 1) if lo[j] < lo[i]), None)
                    lows.append((i, lo[i], k))
                    if k is not None:
                        for j in range(k, min(k + SWEEP_RECLAIM_BARS - 1, b) + 1):
                            if c[j] > lo[i]:
                                sweeps[1].append((j, min(lo[k:j + 1])))
                                break
        for d in sweeps:
            sweeps[d].sort(key=lambda t: t[0])
        by_sess: dict = {}
        for name, pool in (("highs", highs), ("lows", lows)):
            for t in pool:
                by_sess.setdefault((name, sid[t[0]]), []).append(t)
        return {"sess": sess, "sid": sid, "atr": atr, "pools": by_sess, "mins": mins,
                "sweeps": sweeps, "sweep_j": {d: [t[0] for t in v] for d, v in sweeps.items()}}
    return data._get(("indep_features", L), build)


def independent_plan(data: SBData, p, tick: float) -> list[tuple]:
    """(m, e, x, side, limit, stop, target) for every trade the rules call for, by explicit loops."""
    def build():
        F = _features(data, p.swing)
        h, lo, c, o = data.high, data.low, data.close, data.open
        tod, mins, sid, atr = data.tod, F["mins"], F["sid"], F["atr"]
        thru = THROUGH_TICKS * tick
        pad = PAD_TICKS * tick
        trades = []
        for a, b in F["sess"]:
            busy_until = -1
            done = False
            for m in range(a + 2, b + 1):
                if done:
                    break
                if m <= busy_until or mins[m] - mins[m - 2] != 2:
                    continue
                iv = next((q for q in WINDOWS[p.window] if q[0] <= tod[m - 2] and tod[m] < q[1] and tod[m] >= tod[m - 2]),
                          None)
                if iv is None:
                    continue
                if h[m - 2] < lo[m]:
                    s, g_lo, g_hi = 1, h[m - 2], lo[m]
                elif lo[m - 2] > h[m]:
                    s, g_lo, g_hi = -1, h[m], lo[m - 2]
                else:
                    continue
                A = atr[m - 2]
                if not np.isfinite(A):
                    continue
                pc = c[m - 2]
                disp = max(h[m - 1] - lo[m - 1], abs(h[m - 1] - pc), abs(lo[m - 1] - pc))
                if disp < p.disp * A or not (g_hi - g_lo > 0) or g_hi - g_lo < p.fvg_min * A:
                    continue
                q = bisect.bisect_right(F["sweep_j"][s], m - 3) - 1
                ext = None
                if q >= 0:
                    j, e0 = F["sweeps"][s][q]
                    if sid[j] == sid[m - 2] and mins[m - 2] - mins[j] <= SWEEP_LOOKBACK_MIN:
                        ext = e0
                if p.sweep and ext is None:
                    continue
                lim = (g_hi if s > 0 else g_lo) if p.entry == "prox" else (g_lo + g_hi) / 2
                if p.stop == "fvg":
                    ref = g_lo - pad if s > 0 else g_hi + pad
                else:
                    if ext is None:
                        a0 = max(a, m - 2 - STRUCT_FALLBACK_BARS + 1)
                        ext = min(lo[a0:m - 1]) if s > 0 else max(h[a0:m - 1])
                    ref = ext - pad if s > 0 else ext + pad
                raw = (lim - ref) * s
                if raw <= 0:
                    continue
                dist = max(raw, MIN_STOP_ATR * A)
                stop = lim - s * dist
                if p.target_kind == "r":
                    tgt = lim + s * p.target_r * dist
                elif p.target_kind == "liq":
                    pool = F["pools"].get(("highs" if s > 0 else "lows", sid[m]), [])
                    cand = [px for i, px, k in pool if a <= i and i + p.swing <= m and (k is None or k > m)
                            and (px - lim) * s > 0]
                    if not cand:
                        continue
                    tgt = min(cand) if s > 0 else max(cand)
                else:
                    tgt = float("nan")
                x = max(i for i in range(m, min(b, m + iv[1] - iv[0] + 5) + 1) if iv[0] <= tod[i] < iv[1])
                last_live = min(m + p.max_age, x)
                if last_live <= m:
                    continue
                e = next((i for i in range(m + 1, last_live + 1)
                          if (lo[i] <= lim - thru if s > 0 else h[i] >= lim + thru)), None)
                if e is None:
                    busy_until = last_live
                    continue
                trades.append((m, e, x, s, lim, stop, tgt))
                done = True
        return trades
    key = ("indep_plan", p.window, round(p.fvg_min, 9), round(p.disp, 9), p.entry, p.stop, p.target_kind,
           None if p.target_r is None else round(p.target_r, 9), p.sweep, p.swing, p.max_age, tick)
    return data._get(key, build)


def _close(a: float, b: float) -> bool:
    if not (np.isfinite(a) or np.isfinite(b)):
        return True
    return bool(np.isfinite(a) and np.isfinite(b) and abs(a - b) <= 1e-9 * max(1.0, abs(b)))


def check_sim_integrity(sim: SimResult, data: SBData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    tick = CostModel.for_symbol(exec_config, p.symbol).tick
    plan = {t[0]: t for t in independent_plan(data, p, tick)}
    o, hi, lo, c = data.open, data.high, data.low, data.close
    m_, e_, x_ = sim.signal_idx, sim.entry_idx, sim.exit_idx
    thru = THROUGH_TICKS * tick

    got = set(int(m) for m in m_)
    cut = int(m_[-1]) if len(m_) and sim.forced_close[-1] else None  # nothing trades after a forced close
    if any(m not in got and (cut is None or m < cut) for m in plan):
        issues.add("trade_skipped_while_flat")
    sess_seen = set()
    for i in range(len(e_)):
        m, e, x = int(m_[i]), int(e_[i]), int(x_[i])
        sd = int(sim.side[i])
        s_id = data.session_date[e]
        if s_id in sess_seen:
            issues.add("more_than_one_trade_per_session")
        sess_seen.add(s_id)
        if m not in plan:
            issues.add("setup_not_per_rule")
            continue
        pm, pe, px, psd, lim, stop, tgt = plan[m]
        if e != pe:
            issues.add("entry_not_per_rule")
        if sd != psd:
            issues.add("wrong_direction")
        if not _close(sim.entry_base[i], lim):
            issues.add("limit_not_per_rule")
        rule_fill = min(o[e], lim) if sd > 0 else max(o[e], lim)
        if sd * (rule_fill - sim.entry_px[i]) > _EPS or not (lo[e] <= lim - thru if sd > 0 else hi[e] >= lim + thru):
            issues.add("entry_fill_better_than_rule")
        if x < e:
            issues.add("exit_before_entry")
        iv = next(q for q in WINDOWS[p.window] if q[0] <= data.tod[m] < q[1])
        if ((data.tod[e:x + 1] < iv[0]) | (data.tod[e:x + 1] >= iv[1])).any():
            issues.add("bar_outside_window")
        if data.session_date[x] != data.session_date[e]:
            issues.add("position_held_overnight")
        if not _close(sim.stop_level[i], stop):
            issues.add("stop_not_per_rule")
        if not _close(sim.target_level[i], tgt):
            issues.add("target_not_per_rule")
        stop_hit = (lambda j: lo[j] <= stop) if sd > 0 else (lambda j: hi[j] >= stop)
        if np.isfinite(tgt):
            tgt_hit = (lambda j: j > e and hi[j] >= tgt + thru) if sd > 0 else (lambda j: j > e and lo[j] <= tgt - thru)
        else:
            tgt_hit = lambda j: False  # noqa: E731
        if any(stop_hit(j) or tgt_hit(j) for j in range(e, x)):
            issues.add("exit_not_at_first_touch")
        why = sim.exit_reason[i]
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            rule_px = min(o[x], stop) if sd > 0 else max(o[x], stop)
            if sd * (rule_px - sim.exit_px[i]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
            if x > px:
                issues.add("time_exit_not_per_rule")
        elif why == "target_exit":
            if not tgt_hit(x) or stop_hit(x):
                issues.add("target_exit_without_trade_through")
            if not _close(sim.exit_px[i], tgt):
                issues.add("target_fill_not_at_target")
            if x > px:
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if x != px or stop_hit(x) or tgt_hit(x):
                issues.add("time_exit_not_per_rule")
            if sd * (c[x] - sim.exit_px[i]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        else:  # forced_close: only on the data's last bar
            if x != data.n - 1:
                issues.add("time_exit_not_per_rule")

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
    full = simulate_silver_bullet(SBData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_silver_bullet(SBData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        k = int(done.sum())
        if k > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "entry_idx", "exit_idx", "quantity", "entry_px", "exit_px", "side",
                     "stop_level", "target_level"):
            a, b = getattr(part, name)[done], getattr(full, name)[:k]
            if not np.allclose(a, b, rtol=0, atol=1e-9, equal_nan=True):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
