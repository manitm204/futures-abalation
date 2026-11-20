"""Stage 1 -- backtest integrity checks for the FX-fix backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. The fix times are recomputed here
    with pandas time-zone conversion (not the backtester's zoneinfo code), the vol gate with
    plain numpy loops, and the entry / exit bars by scanning each session's bars. Then: each
    trade entered at the first bar at/after its leg's start time (within the entry-lag limit),
    on the leg's side, on a day the vol gate allowed; no eligible trade was skipped while flat;
    the entry filled at the bar's open at an adverse price; the stop sits where the rule puts
    it and every stop exit was really touched (and was the first touch); time exits happened at
    the close of the last bar before the exit time, session exits at the session's last bar;
    every bar of every trade is inside 08:00-17:00 ET of ONE date (nothing held overnight); no
    overlapping positions, no leverage, only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl

from src.strategies.fx_fix.backtest import FXData, SimResult, as_params, simulate_fx_fix
from src.strategies.fx_fix.config import (
    DAY_END_MIN,
    DAY_START_MIN,
    ECB_FIX,
    LONDON_FIX,
    MAX_ENTRY_LAG_MIN,
    RV_LONG_DAYS,
    RV_SAMPLE_MIN,
    RV_SHORT_DAYS,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["fix_time_mismatch", "entry_not_at_leg_start", "side_not_per_leg", "leg_not_allowed",
          "vol_gate_not_met", "trade_skipped_while_flat", "entry_fill_better_than_market",
          "exit_before_entry", "bar_outside_day_window", "position_held_overnight", "stop_not_per_rule",
          "stop_exit_without_touch", "stop_fill_better_than_rule", "exit_not_at_first_touch",
          "time_exit_not_per_rule", "eod_exit_not_at_session_close", "exit_fill_better_than_market",
          "overlapping_positions", "position_exceeds_equity", "forced_close_not_final_trade",
          "commission_below_minimum"]


def independent_fix_minutes(days: np.ndarray, fix: tuple[str, int, int]) -> np.ndarray:
    """NY minutes-from-midnight of a local-clock fix on each date, via pandas tz conversion."""
    tz, h, m = fix
    local = (pd.to_datetime(days.astype("datetime64[D]")) + pd.Timedelta(hours=h, minutes=m)).tz_localize(tz)
    ny = local.tz_convert("America/New_York")
    return np.asarray(ny.hour * 60 + ny.minute, dtype=np.int64)


def independent_gate(data: FXData, vol_gate: str) -> np.ndarray:
    """Per session: does the vol gate allow trading? Plain loops."""
    S = len(data.days)
    if vol_gate == "none":
        return np.ones(S, dtype=bool)
    v = np.full(S, np.nan)
    for s in range(S):
        a, b = data.day_start_idx[s], data.day_end_idx[s]
        closes, cur_bucket, last = [], None, None
        for i in range(a, b + 1):
            bk = data.tod[i] // RV_SAMPLE_MIN
            if cur_bucket is not None and bk != cur_bucket:
                closes.append(last)
            cur_bucket, last = bk, data.close[i]
        if last is not None:
            closes.append(last)
        r = np.diff(np.log(np.asarray(closes, dtype=float)))
        v[s] = np.sqrt(np.sum(r * r)) if len(closes) else np.nan
    g = np.full(S, np.nan)
    for s in range(RV_SHORT_DAYS, S):
        w = v[s - RV_SHORT_DAYS:s]
        if np.isfinite(w).all():
            g[s] = w.mean()
    out = np.zeros(S, dtype=bool)
    for s in range(S):
        if s - RV_LONG_DAYS + 1 < 0:
            continue
        w = g[s - RV_LONG_DAYS + 1:s + 1]
        if not np.isfinite(w).all():
            continue
        med = float(np.median(w))
        out[s] = g[s] > med if vol_gate == "high" else g[s] <= med
    return out


def independent_plan(data: FXData, p) -> list[tuple[int, int, int, str, bool]]:
    """(entry bar, exit bar, side, leg, timed) for every trade the rules call for, by scanning bars."""
    days = data.days
    lon = data._get(("indep_london",), lambda: independent_fix_minutes(days, LONDON_FIX))
    ecb = data._get(("indep_ecb",), lambda: independent_fix_minutes(days, ECB_FIX))
    gate = data._get(("indep_gate", p.vol_gate), lambda: independent_gate(data, p.vol_gate))
    H = p.hold_minutes
    out = []
    for s in range(len(days)):
        if not gate[s]:
            continue
        a, b = int(data.day_start_idx[s]), int(data.day_end_idx[s])
        tod = data.tod[a:b + 1]
        sw = int(lon[s]) + p.switch_offset
        legs = []
        if p.leg in ("pre", "both"):
            legs.append(("pre", -1, int(ecb[s]), sw))
        if p.leg in ("post", "both"):
            legs.append(("post", 1, sw, None if H is None else sw + H))
        for name, side, start, end in legs:
            e = next((a + i for i, t in enumerate(tod) if t >= start), None)
            if e is None or data.tod[e] - start > MAX_ENTRY_LAG_MIN:
                continue
            stop_at = DAY_END_MIN if end is None else end
            before = [a + i for i, t in enumerate(tod) if t < stop_at]
            if not before:
                continue
            x = before[-1]
            if x < e:
                continue
            out.append((e, x, side, name, end is not None and x < b))
    out.sort()
    return out


def check_sim_integrity(sim: SimResult, data: FXData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    if not (np.array_equal(data.london_min, independent_fix_minutes(data.days, LONDON_FIX))
            and np.array_equal(data.ecb_min, independent_fix_minutes(data.days, ECB_FIX))):
        issues.add("fix_time_mismatch")
    plan = data._get(("indep_plan", p.leg, p.switch_offset, p.post_hold, p.vol_gate),
                     lambda: independent_plan(data, p))
    by_entry = {e: (x, side, leg, timed) for e, x, side, leg, timed in plan}
    gate = data._get(("indep_gate", p.vol_gate), lambda: independent_gate(data, p.vol_gate))
    o, h, lo, c = data.open, data.high, data.low, data.close
    k_, e_, x_, d_ = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.side

    # Planned trades never overlap (the pre leg ends on the bar before the post leg starts), so
    # every planned trade must have been taken (stress runs aside).
    taken = set(int(k) for k in k_)
    if any(e not in taken for e, *_ in plan):
        issues.add("trade_skipped_while_flat")

    for i in range(len(e_)):
        k, e, x, d = int(k_[i]), int(e_[i]), int(x_[i]), int(d_[i])
        s = int(data.sess[e])
        if k not in by_entry:
            issues.add("entry_not_at_leg_start")
            plan_x, plan_side, plan_leg, timed = x, d, sim.leg[i], False
        else:
            plan_x, plan_side, plan_leg, timed = by_entry[k]
        if e < k or data.sess[e] != data.sess[k]:
            issues.add("entry_not_at_leg_start")
        if plan_side != d or (sim.leg[i] == "pre") != (d < 0):
            issues.add("side_not_per_leg")
        if (p.leg == "pre" and sim.leg[i] != "pre") or (p.leg == "post" and sim.leg[i] != "post"):
            issues.add("leg_not_allowed")
        if not gate[s]:
            issues.add("vol_gate_not_met")
        if abs(sim.entry_base[i] - o[e]) > _EPS or d * (sim.entry_px[i] - o[e]) < -_EPS:
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
            stop = o[e] * (1 - d * p.stop_pct / 100)
            if not abs(sim.stop_level[i] - stop) <= 1e-9 * max(1.0, abs(stop)):
                issues.add("stop_not_per_rule")
        stop_hit = ((lambda j: False) if p.stop_pct is None else
                    (lambda j: lo[j] <= stop) if d > 0 else (lambda j: h[j] >= stop))
        for j in range(e, x):
            if stop_hit(j):
                issues.add("exit_not_at_first_touch")
                break
        why = sim.exit_reason[i]
        L = int(data.day_end_idx[s])
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            worst = min(o[x], stop) if d > 0 else max(o[x], stop)
            if d * (worst - sim.exit_px[i]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
            if x > plan_x:
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if not timed or x != plan_x or x >= L or stop_hit(x):
                issues.add("time_exit_not_per_rule")
            if d * (c[x] - sim.exit_px[i]) < -_EPS:
                issues.add("exit_fill_better_than_market")
        else:  # eod_exit / forced_close
            if x != L or stop_hit(x) or (timed and x == plan_x):
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
    full = simulate_fx_fix(FXData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_fx_fix(FXData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
