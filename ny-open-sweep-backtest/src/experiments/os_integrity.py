"""Stage 1 -- backtest integrity checks for the NY-open liquidity-sweep backtester.

Three layers:
  * `check_levels` (run level): recomputes every session's pre-open ranges from the FULL Globex
    bars with plain loops and compares them with the columns `os_day_bars` attached. A level may
    only use bars that open before 09:30 of its own session.
  * `check_sim_integrity` runs on EVERY config's simulation. The 09:30 open, the prior RTH
    high/low, dATR, the window, the penetration, the fade / continuation trigger and its side are
    recomputed session by session with plain loops (not the backtester's code). Then: every trade
    is on a session and bar the rules allow, in the rule's direction, entered at the open of the
    bar after the trigger; no allowed session was skipped; fills are adverse; the stop and target
    sit where the rule puts them; every stop / target exit was really touched (target: traded
    through by a tick) and was the first touch; time exits at the close of the last bar before
    the exit time, session exits at the session's last bar; every bar of a trade is in
    09:30-16:00 ET of ONE date; no overlapping positions, no leverage, only the final trade may
    be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.mean_reversion.backtest import CostModel
from src.strategies.open_sweep.backtest import OSData, SimResult, as_params, simulate_open_sweep
from src.strategies.open_sweep.config import (
    DATR_LOOKBACK,
    DAY_END_MIN,
    DAY_START_MIN,
    EVENING_START_MIN,
    LEVEL_MIN_COVERAGE,
    LEVEL_WINDOWS,
    MAX_ENTRY_GAP_MIN,
    MAX_OPEN_LAG_MIN,
    MIN_STOP_DATR,
    PRE_OPEN_LEVELS,
    STRUCT_PAD_TICKS,
    TARGET_THROUGH_TICKS,
    level_minutes,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["signal_mismatch", "entry_not_per_rule", "day_not_allowed", "wrong_direction", "trade_skipped_while_flat",
          "entry_fill_better_than_market", "exit_before_entry", "bar_outside_day_window", "position_held_overnight",
          "stop_not_per_rule", "target_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule",
          "target_exit_without_trade_through", "target_fill_not_at_target", "exit_not_at_first_touch",
          "time_exit_not_per_rule", "eod_exit_not_at_session_close", "exit_fill_better_than_market",
          "overlapping_positions", "position_exceeds_equity", "forced_close_not_final_trade",
          "commission_below_minimum"]


def check_levels(df_full: pl.DataFrame, day_bars: pl.DataFrame) -> list[str]:
    """Recompute the pre-open levels with plain loops; return mismatch descriptions."""
    full = df_full.sort("bar_open_ts")
    ny = full["bar_open_ts_ny"].to_list()
    sd = full["session_date_ny"].to_list()
    hi, lo = full["high"].to_list(), full["low"].to_list()
    acc: dict = {}
    for i in range(full.height):
        m = ny[i].hour * 60 + ny[i].minute
        for lv in PRE_OPEN_LEVELS:
            if lv == "onh":
                inside = m >= EVENING_START_MIN or m < DAY_START_MIN
            else:
                a, b = LEVEL_WINDOWS[lv]
                inside = a <= m < b
            if not inside:
                continue
            # a pre-open bar must open before 09:30 of its own session date
            if m < DAY_START_MIN and ny[i].date() != sd[i]:
                return [f"bar {ny[i]} counted for session {sd[i]} is not before that session's open"]
            k = (sd[i], lv)
            h0, l0, n0 = acc.get(k, (-np.inf, np.inf, 0))
            acc[k] = (max(h0, hi[i]), min(l0, lo[i]), n0 + 1)
    firsts = day_bars.group_by("session_date_ny").agg(pl.all().first()).sort("session_date_ny")
    probs = []
    for row in firsts.iter_rows(named=True):
        for lv in PRE_OPEN_LEVELS:
            h0, l0, n0 = acc.get((row["session_date_ny"], lv), (np.nan, np.nan, 0))
            if n0 < np.ceil(LEVEL_MIN_COVERAGE * level_minutes(lv)):
                h0 = l0 = np.nan
            got_h = row[f"{lv}_h"] if row[f"{lv}_h"] is not None else np.nan
            got_l = row[f"{lv}_l"] if row[f"{lv}_l"] is not None else np.nan
            for want, got, nm in ((h0, got_h, "h"), (l0, got_l, "l")):
                if not ((np.isnan(want) and np.isnan(got)) or abs(want - got) <= 1e-9):
                    probs.append(f"{row['session_date_ny']} {lv}_{nm}: expected {want}, got {got}")
    return probs[:20]


def _sessions(data: OSData) -> list[tuple[int, int]]:
    out, a = [], 0
    for i in range(1, data.n + 1):
        if i == data.n or data.session_date[i] != data.session_date[a]:
            out.append((a, i - 1))
            a = i
    return out


def independent_plan(data: OSData, p) -> dict[int, tuple]:
    """trigger bar -> (entry bar, side, extreme, H, L, dATR, session last bar), by explicit loops."""
    def build():
        sess = _sessions(data)
        S = len(sess)
        rng = [max(data.high[a:b + 1]) - min(data.low[a:b + 1]) for a, b in sess]
        datr = [float(np.mean(rng[s - DATR_LOOKBACK:s])) if s >= DATR_LOOKBACK else np.nan for s in range(S)]
        if p.level == "pdr":
            H = [np.nan] + [max(data.high[a:b + 1]) for a, b in sess[:-1]]
            L = [np.nan] + [min(data.low[a:b + 1]) for a, b in sess[:-1]]
        else:
            HH, LL = data.levels(p.level)  # pre-open columns (verified by check_levels) or a placebo
            H, L = list(HH), list(LL)
        out = {}
        for s, (a, b) in enumerate(sess):
            o9 = data.open[a] if data.tod[a] - DAY_START_MIN <= MAX_OPEN_LAG_MIN else np.nan
            if not (np.isfinite(o9) and np.isfinite(datr[s])):
                continue
            win = [i for i in range(a, b + 1) if data.tod[i] < DAY_START_MIN + p.window]
            if not win:
                continue
            pen = p.pen * datr[s]
            found = []
            for upper in (True, False):
                if p.side == ("low" if upper else "high"):
                    continue
                lvl = H[s] if upper else L[s]
                if not np.isfinite(lvl) or (upper and not o9 <= lvl) or (not upper and not o9 >= lvl):
                    continue
                pb = next((i for i in win if (data.high[i] > lvl + pen if upper else data.low[i] < lvl - pen)), None)
                if pb is None:
                    continue
                k = win.index(pb)
                if p.mode == "fade":
                    t = next((win[j] for j in range(k, min(k + p.confirm, len(win)))
                              if (data.close[win[j]] < lvl if upper else data.close[win[j]] > lvl)), None)
                    if t is None:
                        continue
                    sd = -1 if upper else 1
                else:
                    if k + p.confirm - 1 >= len(win):
                        continue
                    seg = win[k:k + p.confirm]
                    if not all((data.close[i] > lvl if upper else data.close[i] < lvl) for i in seg):
                        continue
                    t = seg[-1]
                    sd = 1 if upper else -1
                ext = (max(data.high[pb:t + 1]) if sd < 0 else min(data.low[pb:t + 1]))
                found.append((t, sd, ext))
            if not found or (len(found) == 2 and found[0][0] == found[1][0]):
                continue
            t, sd, ext = min(found)
            e = t + 1
            if e > b or data.tod[e] - data.tod[t] > MAX_ENTRY_GAP_MIN:
                continue
            out[t] = (e, sd, ext, H[s], L[s], datr[s], b)
        return out
    if p.level in data.level_override:
        return build()
    return data._get(("indep_plan", p.level, p.side, p.window, round(p.pen, 9), p.confirm, p.mode), build)


def independent_exit_bar(data: OSData, e: int, b: int, exit_min: int) -> tuple[int, bool]:
    before = [i for i in range(e, b + 1) if data.tod[i] < min(exit_min, DAY_END_MIN)]
    x = before[-1] if before else e - 1
    return x, x < b


def check_sim_integrity(sim: SimResult, data: OSData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    tick = CostModel.for_symbol(exec_config, p.symbol).tick
    plan = independent_plan(data, p)
    o, hi, lo, c = data.open, data.high, data.low, data.close
    k_, e_, x_ = sim.signal_idx, sim.entry_idx, sim.exit_idx

    def rule_levels(t, e):
        pe, sd, ext, H, L, da, b = plan[t]
        base = o[e]
        floor = MIN_STOP_DATR * da
        if p.stop_kind == "datr":
            dist = max(p.stop_mult * da, floor)
        else:
            pad = STRUCT_PAD_TICKS * tick
            dist = max(base - (ext - pad) if sd > 0 else (ext + pad) - base, floor)
        stop = base - sd * dist
        if p.target_kind == "none":
            tgt = np.nan
        elif p.target_kind == "r":
            tgt = base + sd * p.target_r * dist
        else:
            if p.mode == "fade":
                tgt = L if sd < 0 else H
            else:
                tgt = H + (H - L) if sd > 0 else L - (H - L)
            if not sd * (tgt - base) > 0:
                tgt = -np.inf
        return stop, tgt

    taken = set(int(k) for k in k_)
    for t, (e, sd, ext, H, L, da, b) in plan.items():
        x, _ = independent_exit_bar(data, e, b, p.exit_min)
        if x < e or t in taken:
            continue
        _, tgt = rule_levels(t, e)
        if tgt == -np.inf:
            continue
        issues.add("trade_skipped_while_flat")
        break

    for i in range(len(e_)):
        k, e, x = int(k_[i]), int(e_[i]), int(x_[i])
        sd = int(sim.side[i])
        if k not in plan:
            issues.add("day_not_allowed")
            continue
        pe, psd, ext, H, L, da, b = plan[k]
        if e != pe:
            issues.add("entry_not_per_rule")
        if sd != psd:
            issues.add("wrong_direction")
        plan_x, timed = independent_exit_bar(data, pe, b, p.exit_min)
        if data.session_date[k] != data.session_date[e] or data.tod[k] >= DAY_START_MIN + p.window:
            issues.add("signal_mismatch")
        if abs(sim.entry_base[i] - o[e]) > _EPS or sd * (sim.entry_px[i] - o[e]) < -_EPS:
            issues.add("entry_fill_better_than_market")
        if x < e:
            issues.add("exit_before_entry")
        if (data.tod[e:x + 1] < DAY_START_MIN).any() or (data.tod[e:x + 1] >= DAY_END_MIN).any():
            issues.add("bar_outside_day_window")
        if data.session_date[x] != data.session_date[e]:
            issues.add("position_held_overnight")
        stop, tgt = rule_levels(k, e)
        if not abs(sim.stop_level[i] - stop) <= 1e-9 * max(1.0, abs(stop)):
            issues.add("stop_not_per_rule")
        if np.isfinite(tgt) != np.isfinite(sim.target_level[i]) or (
                np.isfinite(tgt) and not abs(sim.target_level[i] - tgt) <= 1e-9 * max(1.0, abs(tgt))):
            issues.add("target_not_per_rule")
        thru = TARGET_THROUGH_TICKS * tick
        stop_hit = (lambda j: lo[j] <= stop) if sd > 0 else (lambda j: hi[j] >= stop)
        if np.isfinite(tgt):
            tgt_hit = (lambda j: hi[j] >= tgt + thru) if sd > 0 else (lambda j: lo[j] <= tgt - thru)
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
            if x > plan_x:
                issues.add("time_exit_not_per_rule")
        elif why == "target_exit":
            if not tgt_hit(x) or stop_hit(x):
                issues.add("target_exit_without_trade_through")
            if not abs(sim.exit_px[i] - tgt) <= 1e-9 * max(1.0, abs(tgt)):
                issues.add("target_fill_not_at_target")
            if x > plan_x:
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if not timed or x != plan_x or x >= b or stop_hit(x) or tgt_hit(x):
                issues.add("time_exit_not_per_rule")
        else:  # eod_exit / forced_close
            if x != b or stop_hit(x) or tgt_hit(x) or (timed and x == plan_x):
                issues.add("eod_exit_not_at_session_close")
        if why not in ("stop_exit", "target_exit") and sd * (c[x] - sim.exit_px[i]) < -_EPS:
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
    full = simulate_open_sweep(OSData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_open_sweep(OSData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
