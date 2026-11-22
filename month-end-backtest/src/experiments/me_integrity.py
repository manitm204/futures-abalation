"""Stage 1 -- backtest integrity checks for the Treasury month-end backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. The month-end rank is recomputed
    here month by month from the shared TradingCalendar (not the backtester's vectorized
    schedule code), the FOMC / auction flags from the CSV with pandas, and the entry / exit bars
    by scanning each session's bars. Then: each trade is long, on an eligible day (last `window`
    NYSE trading days, event filter met), entered at the first bar at/after the entry time
    (within the entry-lag limit); no eligible day was skipped while flat; the entry filled at the
    bar's open at an adverse price; the stop sits where the rule puts it and every stop exit was
    really touched (and was the first touch); time exits happened at the close of the last bar
    before the exit target, session exits at the session's last bar; every bar of every trade is inside
    08:00-17:00 ET of ONE date (nothing held overnight); no overlapping positions, no leverage,
    only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import polars as pl

from src.data.calendars import TradingCalendar
from src.strategies.month_end.backtest import MEData, SimResult, as_params, simulate_month_end
from src.strategies.month_end.config import (
    AUCTION_CSV,
    DAY_END_MIN,
    DAY_START_MIN,
    FOMC_DAYS,
    MAX_ENTRY_LAG_MIN,
    STRIKE_SWITCH_DATE,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["month_end_rank_mismatch", "event_flag_mismatch", "entry_not_per_rule", "day_not_eligible",
          "event_filter_violated", "not_long", "trade_skipped_while_flat", "entry_fill_better_than_market",
          "exit_before_entry", "bar_outside_day_window", "position_held_overnight", "stop_not_per_rule",
          "stop_exit_without_touch", "stop_fill_better_than_rule", "exit_not_at_first_touch", "time_exit_not_per_rule",
          "eod_exit_not_at_session_close", "exit_fill_better_than_market", "overlapping_positions",
          "position_exceeds_equity", "forced_close_not_final_trade", "commission_below_minimum"]


def independent_rank(days: list[date], *, from_start: bool = False) -> np.ndarray:
    """Month-end rank per date (or, with `from_start`, the day's number in its month), one
    calendar month at a time via TradingCalendar."""
    cal = TradingCalendar()
    cache: dict[tuple[int, int], list[date]] = {}
    out = np.zeros(len(days), dtype=np.int64)
    for i, d in enumerate(days):
        key = (d.year, d.month)
        if key not in cache:
            nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            cache[key] = [t for t in cal.trading_days(date(d.year, d.month, 1), nxt) if t.month == d.month]
        month = cache[key]
        out[i] = (sum(1 for t in month if (t <= d if from_start else t >= d)) if d in month else 0)
    return out


def independent_flags(days: list[date]) -> tuple[np.ndarray, np.ndarray]:
    auc = set(pd.read_csv(AUCTION_CSV, parse_dates=["auction_date"])["auction_date"].dt.date)
    return (np.array([d in FOMC_DAYS for d in days], dtype=bool), np.array([d in auc for d in days], dtype=bool))


def independent_exit_minutes(rule: str, d: date, shift: int) -> int:
    if rule == "strike":
        base = 16 * 60 if d >= STRIKE_SWITCH_DATE else 15 * 60
    else:
        hh, mm = rule.split(":")
        base = int(hh) * 60 + int(mm)
    return base + shift


def independent_eligible(data: MEData, p) -> np.ndarray:
    rank = data._get(("indep_rank",), lambda: independent_rank(data.day_list))
    first = data._get(("indep_rank_start",), lambda: independent_rank(data.day_list, from_start=True))
    fomc, auc = data._get(("indep_flags",), lambda: independent_flags(data.day_list))
    ok = ((rank >= 1) & (rank <= p.window)) | ((first >= 1) & (first <= p.first_days))
    if p.event_filter in ("skip_fomc", "skip_fomc_auction"):
        ok &= ~fomc
    if p.event_filter == "skip_fomc_auction":
        ok &= ~auc
    return ok


def independent_plan(data: MEData, p) -> list[tuple[int, int, bool]]:
    """(entry bar, exit bar, timed) for every trade the rules call for, by scanning bars."""
    ok = independent_eligible(data, p)
    out = []
    for s in range(len(data.days)):
        if not ok[s]:
            continue
        a, b = int(data.day_start_idx[s]), int(data.day_end_idx[s])
        tod = data.tod[a:b + 1]
        e = next((a + i for i, t in enumerate(tod) if t >= p.entry_min), None)
        if e is None or data.tod[e] - p.entry_min > MAX_ENTRY_LAG_MIN:
            continue
        end = independent_exit_minutes(p.exit_rule, data.day_list[s], p.exit_shift)
        before = [a + i for i, t in enumerate(tod) if t < end]
        if not before:
            continue
        x = before[-1]
        if x < e:
            continue
        out.append((e, x, x < b))
    return out


def check_sim_integrity(sim: SimResult, data: MEData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    rank = data._get(("indep_rank",), lambda: independent_rank(data.day_list))
    first = data._get(("indep_rank_start",), lambda: independent_rank(data.day_list, from_start=True))
    if not (np.array_equal(rank, data.rank) and np.array_equal(first, data.rank_start)):
        issues.add("month_end_rank_mismatch")
    fomc, auc = data._get(("indep_flags",), lambda: independent_flags(data.day_list))
    if not (np.array_equal(fomc, data.is_fomc) and np.array_equal(auc, data.is_auction)):
        issues.add("event_flag_mismatch")
    plan = data._get(("indep_plan", p.window, p.first_days, p.entry_min, p.exit_rule, p.exit_shift,  # stop-free plan
                      p.event_filter),
                     lambda: independent_plan(data, p))
    by_entry = {e: (x, timed) for e, x, timed in plan}
    elig = independent_eligible(data, p)
    o, lo, c = data.open, data.low, data.close
    k_, e_, x_ = sim.signal_idx, sim.entry_idx, sim.exit_idx

    # Planned trades are one per day and never overlap, so every one must have been taken.
    taken = set(int(k) for k in k_)
    if any(e not in taken for e, *_ in plan):
        issues.add("trade_skipped_while_flat")

    for i in range(len(e_)):
        k, e, x = int(k_[i]), int(e_[i]), int(x_[i])
        s = int(data.sess[e])
        if k not in by_entry:
            issues.add("entry_not_per_rule")
            plan_x, timed = x, False
        else:
            plan_x, timed = by_entry[k]
        if e < k or data.sess[e] != data.sess[k]:
            issues.add("entry_not_per_rule")
        if int(sim.side[i]) != 1:
            issues.add("not_long")
        if not ((1 <= rank[s] <= p.window) or (1 <= first[s] <= p.first_days)):
            issues.add("day_not_eligible")
        elif not elig[s]:
            issues.add("event_filter_violated")
        if abs(sim.entry_base[i] - o[e]) > _EPS or sim.entry_px[i] - o[e] < -_EPS:
            issues.add("entry_fill_better_than_market")
        if x < e:
            issues.add("exit_before_entry")
        if (data.tod[e:x + 1] < DAY_START_MIN).any() or (data.tod[e:x + 1] >= DAY_END_MIN).any():
            issues.add("bar_outside_day_window")
        if data.sess[x] != data.sess[e] or data.session_date[x] != data.session_date[e]:
            issues.add("position_held_overnight")
        if p.stop_pct is None:
            stop = np.nan
            if np.isfinite(sim.stop_level[i]):
                issues.add("stop_not_per_rule")
        else:
            stop = o[e] * (1 - p.stop_pct / 100)
            if not abs(sim.stop_level[i] - stop) <= 1e-9 * max(1.0, abs(stop)):
                issues.add("stop_not_per_rule")
        stop_hit = (lambda j: False) if p.stop_pct is None else (lambda j: lo[j] <= stop)
        if any(stop_hit(j) for j in range(e, x)):
            issues.add("exit_not_at_first_touch")
        why = sim.exit_reason[i]
        L = int(data.day_end_idx[s])
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            if min(o[x], stop) - sim.exit_px[i] < -_EPS:
                issues.add("stop_fill_better_than_rule")
            if x > plan_x:
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if not timed or x != plan_x or x >= L or stop_hit(x):
                issues.add("time_exit_not_per_rule")
        else:  # eod_exit / forced_close
            if x != L or stop_hit(x) or (timed and x == plan_x):
                issues.add("eod_exit_not_at_session_close")
        if why != "stop_exit" and c[x] - sim.exit_px[i] < -_EPS:
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
    full = simulate_month_end(MEData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_month_end(MEData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
