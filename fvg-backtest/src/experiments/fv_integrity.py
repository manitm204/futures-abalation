"""Stage 1 -- backtest integrity checks for the FVG-after-displacement backtester.

  * `check_sim_integrity` runs on EVERY config's simulation. ATR, the session VWAP, the gaps,
    the window / size / displacement / VWAP filters, the order level, the one-order-at-a-time
    rule, the fills, the stop, the target and the hold exit are recomputed with plain Python loops
    (not the backtester's numpy code). Every trade must be one the rules call for and none may be
    missing; fills are never better than the rule's; every stop / target exit was really touched
    (target: 1-tick trade-through, not on the fill bar) and was the first touch; the time exit is at
    the hold's last bar; every bar of a trade is in one session before 16:00; no overlap, no
    leverage, one trade per session, only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; completed trades must match.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.fvg.backtest import FVData, SimResult, as_params, simulate_fvg
from src.strategies.fvg.config import (
    ATR_LEN,
    MIN_STOP_ATR,
    PAD_TICKS,
    RTH_START_MIN,
    SESSION_END_MIN,
    THROUGH_TICKS,
    WINDOWS,
)
from src.strategies.mean_reversion.backtest import CostModel
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["setup_not_per_rule", "entry_not_per_rule", "wrong_direction", "trade_skipped_while_flat",
          "reference_not_per_rule", "entry_fill_better_than_rule", "exit_before_entry", "bar_after_session_end",
          "position_held_overnight", "more_than_one_trade_per_session", "stop_not_per_rule",
          "target_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule",
          "target_exit_without_trade_through", "target_fill_not_at_target", "exit_not_at_first_touch",
          "time_exit_not_per_rule", "exit_fill_better_than_market", "overlapping_positions",
          "position_exceeds_equity", "forced_close_not_final_trade", "commission_below_minimum"]


def _base(data: FVData) -> dict:
    """ATR, VWAP and every gap, by explicit loops (cached per data object)."""
    def build():
        h, lo, c, tod, mins = (data.high.tolist(), data.low.tolist(), data.close.tolist(), data.tod.tolist(),
                               data.minute.tolist())
        vol = data._df["volume"].to_list() if "volume" in data._df.columns else [1.0] * data.n
        sess, a = [], 0
        for i in range(1, data.n + 1):
            if i == data.n or data.session_date[i] != data.session_date[a]:
                sess.append((a, i - 1))
                a = i
        atr = [float("nan")] * data.n
        vwap = [float("nan")] * data.n
        sid = [0] * data.n
        for s, (a, b) in enumerate(sess):
            trs, pv, vv = [], 0.0, 0.0
            for i in range(a, b + 1):
                sid[i] = s
                trs.append(h[i] - lo[i] if i == a else max(h[i] - lo[i], abs(h[i] - c[i - 1]), abs(lo[i] - c[i - 1])))
                if len(trs) >= ATR_LEN:
                    atr[i] = sum(trs[-ATR_LEN:]) / ATR_LEN
                if RTH_START_MIN <= tod[i] < SESSION_END_MIN:
                    pv += (h[i] + lo[i] + c[i]) / 3.0 * vol[i]
                    vv += vol[i]
                    if vv > 0:
                        vwap[i] = pv / vv
        gaps = []  # (m, gap side, gap lo, gap hi, middle-bar true range)
        for s, (a, b) in enumerate(sess):
            for m in range(a + 2, b + 1):
                if mins[m] - mins[m - 2] != 2:
                    continue
                if h[m - 2] < lo[m]:
                    g, glo, ghi = 1, h[m - 2], lo[m]
                elif lo[m - 2] > h[m]:
                    g, glo, ghi = -1, h[m], lo[m - 2]
                else:
                    continue
                pc = c[m - 2]
                gaps.append((m, g, glo, ghi, max(h[m - 1] - lo[m - 1], abs(h[m - 1] - pc), abs(lo[m - 1] - pc))))
        return {"sess": sess, "sid": sid, "atr": atr, "vwap": vwap, "gaps": gaps, "tod": tod, "mins": mins}
    return data._get(("fv_indep_base",), build)


def independent_plan(data: FVData, p, tick: float) -> list[tuple]:
    """(m, e, x, side, reference, kind, stop, target) for every trade the rules call for."""
    def build():
        B = _base(data)
        tod, mins, sid, atr, vwap = B["tod"], B["mins"], B["sid"], B["atr"], B["vwap"]
        o, h, lo, c = data.open.tolist(), data.high.tolist(), data.low.tolist(), data.close.tolist()
        wa, wb = WINDOWS[p.window]
        thru, pad = THROUGH_TICKS * tick, PAD_TICKS * tick
        out = []
        busy_until, done = -1, set()
        for m, g, glo, ghi, disp in B["gaps"]:
            s = sid[m]
            if s in done or m <= busy_until:
                continue
            A = atr[m - 2]
            if not (A == A) or not (wa <= tod[m - 2] <= tod[m] < wb):
                continue
            if disp < p.disp * A or not ghi - glo > 0 or ghi - glo < p.fvg_min * A:
                continue
            sd = g if p.mode == "with" else -g
            if p.vwap and not (vwap[m] == vwap[m] and (c[m] - vwap[m]) * sd > 0):
                continue
            sess_end = data.sess_end[m]
            wl = max(i for i in range(m, min(sess_end, m + (wb - wa) + 5) + 1) if tod[i] < wb)
            if p.entry == "mkt":
                e = m + 1
                if e > wl or mins[e] - mins[m] > 2:
                    continue
                base, kind = o[e], 2
            else:
                lvl = (ghi if g > 0 else glo) if p.entry == "prox" else (glo + ghi) / 2
                last_live = min(m + p.wait, wl)
                if last_live <= m:
                    continue
                e = None
                for i in range(m + 1, last_live + 1):
                    if p.mode == "with":
                        hit = lo[i] <= lvl - thru if g > 0 else h[i] >= lvl + thru
                    else:
                        hit = lo[i] <= lvl if g > 0 else h[i] >= lvl
                    if hit:
                        e = i
                        break
                if e is None:
                    busy_until = last_live
                    continue
                base, kind = lvl, (0 if p.mode == "with" else 1)
            if p.stop_kind == "struct":
                ref = (min(lo[m - 2:m + 1]) - pad) if sd > 0 else (max(h[m - 2:m + 1]) + pad)
                raw = (base - ref) * sd
                if raw <= 0:
                    continue
            else:
                raw = p.stop_mult * A
            dist = max(raw, MIN_STOP_ATR * A)
            stop = base - sd * dist
            tgt = base + sd * p.target_r * dist if p.target_r is not None else float("nan")
            x = e
            for i in range(e, sess_end + 1):
                if mins[i] - mins[e] < p.hold and tod[i] < SESSION_END_MIN:
                    x = i
                else:
                    break
            out.append((m, e, x, sd, base, kind, stop, tgt))
            done.add(s)
        return out
    key = ("fv_indep_plan", p.window, p.mode, round(p.disp, 9), round(p.fvg_min, 9), p.vwap, p.entry, p.wait,
           p.stop_kind, p.stop_mult, p.target_r, p.hold, tick)
    return data._get(key, build)


def _close(a: float, b: float) -> bool:
    if not (np.isfinite(a) or np.isfinite(b)):
        return True
    return bool(np.isfinite(a) and np.isfinite(b) and abs(a - b) <= 1e-9 * max(1.0, abs(b)))


def check_sim_integrity(sim: SimResult, data: FVData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    costs = CostModel.for_symbol(exec_config, p.symbol)
    tick = costs.tick
    plan = {t[0]: t for t in independent_plan(data, p, tick)}
    o, hi, lo, c = data.open, data.high, data.low, data.close
    m_, e_, x_ = sim.signal_idx, sim.entry_idx, sim.exit_idx
    thru = THROUGH_TICKS * tick
    got = set(int(m) for m in m_)
    cut = int(m_[-1]) if len(m_) and sim.forced_close[-1] else None
    if any(m not in got and (cut is None or m < cut) for m in plan):
        issues.add("trade_skipped_while_flat")
    seen = set()
    for i in range(len(e_)):
        m, e, x, sd = int(m_[i]), int(e_[i]), int(x_[i]), int(sim.side[i])
        if data.session_date[e] in seen:
            issues.add("more_than_one_trade_per_session")
        seen.add(data.session_date[e])
        if m not in plan:
            issues.add("setup_not_per_rule")
            continue
        _, pe, px, psd, base, kind, stop, tgt = plan[m]
        if e != pe:
            issues.add("entry_not_per_rule")
        if sd != psd:
            issues.add("wrong_direction")
        if not _close(sim.entry_base[i], base):
            issues.add("reference_not_per_rule")
        act = "buy" if sd > 0 else "sell"
        if kind == 0:
            rule = min(o[e], base) if sd > 0 else max(o[e], base)
        elif kind == 1:
            rule = costs.fill(max(o[e], base) if sd > 0 else min(o[e], base), act, stop=True)
        else:
            rule = costs.fill(o[e], act)
        if sd * (rule - sim.entry_px[i]) > _EPS:
            issues.add("entry_fill_better_than_rule")
        if x < e:
            issues.add("exit_before_entry")
        if (data.tod[e:x + 1] >= SESSION_END_MIN).any() or (data.tod[e:x + 1] < RTH_START_MIN).any():
            issues.add("bar_after_session_end")
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
            rp = min(o[x], stop) if sd > 0 else max(o[x], stop)
            if sd * (rp - sim.exit_px[i]) < -_EPS:
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
        elif x != data.n - 1:
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
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_fvg(FVData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        part = simulate_fvg(FVData(bars.head(int(bars.height * frac))), cfg, exec_config=exec_config,
                            starting_equity=eq0)
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
