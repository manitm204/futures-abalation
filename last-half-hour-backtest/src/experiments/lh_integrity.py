"""Stage 1 -- backtest integrity checks for the last-half-hour momentum backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. The prior close, the 09:30 open, the
    decision closes, the signal, its 20-session standard deviation, the realized-volatility regime
    and the trade direction are recomputed here session by session with plain loops (not the
    backtester's vectorized code). Then: every trade is on a day the rules allow, in the signal's
    direction, entered at the open of the bar right after the decision bar (which opens before the
    entry time); no allowed day was skipped; fills are adverse; the stop sits where the rule puts
    it and every stop exit was really touched (and was the first touch); time exits at the close
    of the last bar before the exit time, session exits at the session's last bar; every bar of a
    trade is in 09:30-16:00 ET of ONE date; no overlapping positions, no leverage, only the final
    trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test).
"""

from __future__ import annotations

import numpy as np
import polars as pl

from src.strategies.last_half_hour.backtest import LHData, SimResult, as_params, simulate_last_half_hour
from src.strategies.last_half_hour.config import (
    DAY_END_MIN,
    DAY_START_MIN,
    FIRST_HALF_END_MIN,
    MAX_ENTRY_LAG_MIN,
    MAX_OPEN_LAG_MIN,
    RV_LOOKBACK,
    RV_MEDIAN_LOOKBACK,
    RV_MEDIAN_MIN_PERIODS,
    Z_LOOKBACK,
    Z_MIN_PERIODS,
)
from src.utils.config_models import ExecutionConfig

_EPS = 1e-9

CHECKS = ["signal_mismatch", "entry_not_per_rule", "day_not_allowed", "wrong_direction", "trade_skipped_while_flat",
          "entry_fill_better_than_market", "exit_before_entry", "bar_outside_day_window", "position_held_overnight",
          "stop_not_per_rule", "stop_exit_without_touch", "stop_fill_better_than_rule", "exit_not_at_first_touch",
          "time_exit_not_per_rule", "eod_exit_not_at_session_close", "exit_fill_better_than_market",
          "overlapping_positions", "position_exceeds_equity", "forced_close_not_final_trade",
          "commission_below_minimum"]


def _sessions(data: LHData) -> list[tuple[int, int]]:
    """(first bar, last bar) per session, by scanning the session dates."""
    out, a = [], 0
    for i in range(1, data.n + 1):
        if i == data.n or data.session_date[i] != data.session_date[a]:
            out.append((a, i - 1))
            a = i
    return out


def _dec(data: LHData, a: int, b: int, m: int) -> int | None:
    last = None
    for i in range(a, b + 1):
        if data.tod[i] < m:
            last = i
        else:
            break
    return last if last is not None and data.tod[last] >= m - 1 - MAX_ENTRY_LAG_MIN else None


def _prev_std(x: list[float], s: int, n: int, k: int) -> float:
    w = [v for v in x[max(0, s - n):s] if np.isfinite(v)]
    return float(np.std(w, ddof=1)) if len(w) >= k else np.nan


def independent_sides(data: LHData, p) -> list[tuple[int, int, int]]:
    """(decision bar, entry bar, side) for every session the rules trade, by explicit loops."""
    def build():
        sess = _sessions(data)
        S = len(sess)
        last_close = [float(data.close[b]) for _, b in sess]
        prev = [np.nan] + last_close[:-1]
        opn = [float(data.open[a]) if data.tod[a] - DAY_START_MIN <= MAX_OPEN_LAG_MIN else np.nan for a, _ in sess]
        fh, sig, dec_of = [], [], []
        for s, (a, b) in enumerate(sess):
            f = _dec(data, a, b, FIRST_HALF_END_MIN)
            fh.append(data.close[f] / prev[s] - 1 if f is not None else np.nan)
            d = _dec(data, a, b, p.entry_min)
            dec_of.append(d)
            if p.signal == "first_half":
                sig.append(fh[-1])
            else:
                base = prev[s] if p.signal == "prev_close" else opn[s]
                sig.append(data.close[d] / base - 1 if d is not None else np.nan)
        ret = [last_close[s] / prev[s] - 1 for s in range(S)]
        rv = [_prev_std(ret, s, RV_LOOKBACK, RV_LOOKBACK) for s in range(S)]
        out = []
        for s, (a, b) in enumerate(sess):
            r = sig[s]
            if not np.isfinite(r) or r == 0:
                continue
            if p.agree and not (np.isfinite(fh[s]) and np.sign(fh[s]) == np.sign(r)):
                continue
            if p.filter == "z":
                sd = _prev_std(sig, s, Z_LOOKBACK, Z_MIN_PERIODS)
                if not (np.isfinite(sd) and sd > 0 and abs(r) > p.z * sd):
                    continue
            elif p.filter == "rv_high":
                w = [v for v in rv[max(0, s - RV_MEDIAN_LOOKBACK):s] if np.isfinite(v)]
                if not (np.isfinite(rv[s]) and len(w) >= RV_MEDIAN_MIN_PERIODS and rv[s] > float(np.median(w))):
                    continue
            elif p.filter == "down_only" and not r < 0:
                continue
            d = dec_of[s]
            e = next((i for i in range(a, b + 1) if data.tod[i] >= p.entry_min), None)
            if d is None or e is None or e != d + 1 or data.tod[e] - p.entry_min > MAX_ENTRY_LAG_MIN:
                continue
            out.append((d, e, int(np.sign(r))))
        return out
    return data._get(("indep_sides", p.signal, p.agree, p.entry_min, p.filter, p.z), build)


def independent_exit(data: LHData, e: int, exit_min: int) -> tuple[int, bool]:
    """(exit bar, timed) for an entry at bar e."""
    s_date = data.session_date[e]
    b = e
    while b + 1 < data.n and data.session_date[b + 1] == s_date:
        b += 1
    before = [i for i in range(e, b + 1) if data.tod[i] < min(exit_min, DAY_END_MIN)]
    x = before[-1] if before else e - 1
    return x, x < b


def check_sim_integrity(sim: SimResult, data: LHData, exec_config: ExecutionConfig, cfg) -> list[str]:
    issues: set[str] = set()
    p = as_params(cfg)
    if data.n == 0:
        return []
    plan = independent_sides(data, p)
    by_dec = {d: (e, sd) for d, e, sd in plan}
    o, hi, lo, c = data.open, data.high, data.low, data.close
    k_, e_, x_ = sim.signal_idx, sim.entry_idx, sim.exit_idx

    taken = set(int(k) for k in k_)
    for d, e, _ in plan:   # one trade per session, never overlapping: every planned one with e <= exit must be taken
        x, _t = independent_exit(data, e, p.exit_min)
        if x >= e and d not in taken:
            issues.add("trade_skipped_while_flat")
            break

    for i in range(len(e_)):
        k, e, x = int(k_[i]), int(e_[i]), int(x_[i])
        sd = int(sim.side[i])
        if k not in by_dec:
            issues.add("day_not_allowed")
            plan_x, timed = x, False
        else:
            pe, psd = by_dec[k]
            if e != pe:
                issues.add("entry_not_per_rule")
            if sd != psd:
                issues.add("wrong_direction")
            plan_x, timed = independent_exit(data, pe, p.exit_min)
        if data.tod[k] >= p.entry_min or data.session_date[k] != data.session_date[e]:
            issues.add("signal_mismatch")
        adverse = sd * (sim.entry_px[i] - o[e])
        if abs(sim.entry_base[i] - o[e]) > _EPS or adverse < -_EPS:
            issues.add("entry_fill_better_than_market")
        if x < e:
            issues.add("exit_before_entry")
        if (data.tod[e:x + 1] < DAY_START_MIN).any() or (data.tod[e:x + 1] >= DAY_END_MIN).any():
            issues.add("bar_outside_day_window")
        if data.session_date[x] != data.session_date[e]:
            issues.add("position_held_overnight")
        if p.stop_pct is None:
            stop = np.nan
            if np.isfinite(sim.stop_level[i]):
                issues.add("stop_not_per_rule")
        else:
            stop = o[e] * (1 - sd * p.stop_pct / 100)
            if not abs(sim.stop_level[i] - stop) <= 1e-9 * max(1.0, abs(stop)):
                issues.add("stop_not_per_rule")
        if p.stop_pct is None:
            stop_hit = lambda j: False  # noqa: E731
        elif sd > 0:
            stop_hit = lambda j: lo[j] <= stop  # noqa: E731
        else:
            stop_hit = lambda j: hi[j] >= stop  # noqa: E731
        if any(stop_hit(j) for j in range(e, x)):
            issues.add("exit_not_at_first_touch")
        why = sim.exit_reason[i]
        L = int(data.day_end_idx[data.sess[e]])
        if why == "stop_exit":
            if not stop_hit(x):
                issues.add("stop_exit_without_touch")
            rule_px = min(o[x], stop) if sd > 0 else max(o[x], stop)
            if sd * (rule_px - sim.exit_px[i]) < -_EPS:
                issues.add("stop_fill_better_than_rule")
            if x > plan_x:
                issues.add("time_exit_not_per_rule")
        elif why == "time_exit":
            if not timed or x != plan_x or x >= L or stop_hit(x):
                issues.add("time_exit_not_per_rule")
        else:  # eod_exit / forced_close
            if x != L or stop_hit(x) or (timed and x == plan_x):
                issues.add("eod_exit_not_at_session_close")
        if why != "stop_exit" and sd * (c[x] - sim.exit_px[i]) < -_EPS:
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
    full = simulate_last_half_hour(LHData(bars), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_last_half_hour(LHData(bars.head(cut)), cfg, exec_config=exec_config, starting_equity=eq0)
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
