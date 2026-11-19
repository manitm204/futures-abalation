"""Stage 1 -- backtest integrity checks for the EMRT two-leg spread backtester.

Two layers, as for the other families:
  * `check_sim_integrity` runs on EVERY config's simulation. z is recomputed here by a different
    route (formation: straight from the month's fit; rolling: the explicit sd of the 100 S values
    under the bar's month params, not the backtester's rolling-covariance algebra), then: the hedge
    of each trade was fit only on bars before its decision, the trade uses its month's beta, each
    entry was a fresh cross beyond the band on an allowed side and outside the last-entry window,
    no qualifying signal was skipped while flat (unless entries are randomly missed), both legs
    filled at the next bar's open of the same session at adverse prices, the exit happened at the
    FIRST bar a rule fired and filled where that rule says, nothing is held overnight when flat,
    no overlap, gross notional fits equity, the P&L adds up from the two legs and the roll costs,
    and only the final trade may be forced.
  * `truncation_invariance`: re-run on data cut at several points; every trade completed before
    the cut must match the full-data run (empirical look-ahead test; it also covers the monthly
    refits, which must not change when later data is removed).
"""

from __future__ import annotations

import math

import numpy as np
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.strategies.emrt_spread.backtest import (
    EOD_EXIT,
    FORCED,
    STOP_EXIT,
    TARGET_EXIT,
    TIME_EXIT,
    PairData,
    SimResult,
    _legs,
    as_params,
    exit_levels,
    simulate_emrt_spread,
    size_pair,
    time_stop_bars,
)
from src.strategies.emrt_spread.config import rolling_window, tod_sessions
from src.utils.config_models import ExecutionConfig

_EPS = 1e-7
_CHUNK = 20_000

CHECKS = ["hedge_fit_not_before_decision", "beta_not_month_fit", "signal_not_fresh_cross", "side_not_allowed",
          "entry_inside_last_entry_cutoff", "signal_skipped_while_flat", "entry_not_next_bar_same_session",
          "entry_fill_better_than_market", "exit_before_entry", "position_held_overnight", "exit_not_at_first_rule",
          "exit_rule_not_met", "exit_fill_not_per_rule", "exit_fill_better_than_market", "time_stop_not_per_rule",
          "overlapping_positions", "position_exceeds_equity", "pnl_mismatch", "roll_cost_mismatch",
          "forced_close_not_final_trade", "undersized_leg", "entry_before_first_entry"]


def _sessions(data: PairData) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Own session structure from the session dates: (session number per bar, first bar of each
    session, bars per session)."""
    sd = data.session_date
    starts = np.concatenate([[0], np.flatnonzero(sd[1:] != sd[:-1]) + 1]) if data.n else np.zeros(0, np.int64)
    num = np.zeros(data.n, dtype=np.int64)
    if data.n:
        num[starts[1:]] = 1
        num = np.cumsum(num)
    lens = np.diff(np.append(starts, data.n))
    return num, starts, lens


def _intraday_legs(data: PairData) -> tuple[np.ndarray, np.ndarray]:
    def calc():
        num, starts, _ = _sessions(data)
        f = starts[num]
        with np.errstate(invalid="ignore", divide="ignore"):
            a = (data.close - data.open[f]) / (data.open[f] - data.price_adj[f])
            b = (data.b_close - data.b_open[f]) / (data.b_open[f] - data.b_price_adj[f])
        return a, b
    return data._get(("integrity_intraday",), calc)


def _tod_z(data: PairData, idx: np.ndarray, beta: np.ndarray, S: np.ndarray, n_sess: int) -> np.ndarray:
    """Explicit time-of-day z: S at the same bar of each of the previous n_sess sessions, under the
    row's beta; their mean and population sd (>= max(5, n_sess // 2) of them must exist)."""
    a, b = _intraday_legs(data)
    num, starts, lens = _sessions(data)
    out = np.full(len(idx), np.nan)
    need = max(5, n_sess // 2)
    h = np.arange(1, n_sess + 1)
    for c in range(0, len(idx), _CHUNK):
        ii = idx[c:c + _CHUNK]
        sn = num[ii]
        pos = ii - starts[sn]
        past = sn[:, None] - h[None, :]
        okp = past >= 0
        pc = np.where(okp, past, 0)
        has = okp & (pos[:, None] < lens[pc])
        bars = np.where(has, starts[pc] + pos[:, None], 0)
        Sh = np.where(has, a[bars] - beta[c:c + _CHUNK, None] * b[bars], np.nan)
        cnt = has.sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            mu = np.nansum(Sh, axis=1) / np.maximum(cnt, 1)
            var = np.nansum((Sh - mu[:, None]) ** 2, axis=1) / np.maximum(cnt, 1)
            sd = np.sqrt(var)
            z = np.where((cnt >= need) & (sd > 1e-12), (S[c:c + _CHUNK] - mu) / sd, np.nan)
        out[c:c + _CHUNK] = z
    return out


def independent_z(data: PairData, idx: np.ndarray, prm: dict, z_mode: str, anchor: str = "formation_end") -> np.ndarray:
    """z of bars idx under per-row params prm (arrays aligned with idx)."""
    idx = np.asarray(idx, dtype=np.int64)
    A0, RA, B0, RB, beta = (np.asarray(prm[k], dtype=float) * np.ones(len(idx)) for k in ("A0", "RA", "B0", "RB", "beta"))
    if anchor == "session":
        ia, ib = _intraday_legs(data)
        S = ia[idx] - beta * ib[idx]
    else:
        a = (data.close[idx] - A0) / RA
        b = (data.b_close[idx] - B0) / RB
        S = a - beta * b
    out = np.full(len(idx), np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        w = rolling_window(z_mode)
        nt = tod_sessions(z_mode)
        if nt is not None:
            return _tod_z(data, idx, beta, S, nt)
        if w is None:
            sd = np.asarray(prm["sd"], dtype=float) * np.ones(len(idx))
            mu = np.asarray(prm["mu"], dtype=float) * np.ones(len(idx))
            return np.where(sd > 0, (S - mu) / sd, np.nan)
        if data.n < w:
            return out
        WA = sliding_window_view(data.close, w)
        WB = sliding_window_view(data.b_close, w)
        ok = idx >= w - 1
        for s in range(0, len(idx), _CHUNK):
            sl = slice(s, s + _CHUNK)
            ii, m = idx[sl], ok[sl]
            if not m.any():
                continue
            r = ii[m] - (w - 1)
            Sw = ((WA[r] - A0[sl][m, None]) / RA[sl][m, None]
                  - beta[sl][m, None] * (WB[r] - B0[sl][m, None]) / RB[sl][m, None])
            sd = Sw.std(axis=1)
            z = np.where(sd > 1e-12, (S[sl][m] - Sw.mean(axis=1)) / sd, np.nan)
            tmp = out[sl]
            tmp[m] = z
            out[sl] = tmp
    return out


def _month_params(data: PairData, p, rows: np.ndarray) -> dict:
    f = data.fits(p.formation, p.hedge, p.anchor)
    h = f["fits"][p.hedge]
    mi = f["month_of_bar"][rows]
    return {"month": mi, "beta": h["beta"][mi], "mu": h["mu"][mi], "sd": h["sd"][mi], "emrt": h["emrt"][mi],
            "A0": f["A0"][mi], "RA": f["RA"][mi], "B0": f["B0"][mi], "RB": f["RB"][mi],
            "fit_end": f["fit_end"][mi], "start": f["start"][mi]}


def _independent_zz(data: PairData, p) -> tuple[np.ndarray, np.ndarray]:
    """(z_k, z_prev_k) for every bar by the independent route; cached on the data object under
    its own key (the backtester's z arrays are never read here)."""
    def calc():
        n = data.n
        k = np.arange(n)
        prm = _month_params(data, p, k)
        z = independent_z(data, k, prm, p.z_mode, p.anchor)
        zp = np.full(n, np.nan)
        if n > 1:
            zp[1:] = independent_z(data, k[:-1], {kk: v[1:] for kk, v in prm.items()}, p.z_mode, p.anchor)
            if p.anchor == "session":
                zp[_sessions(data)[1]] = np.nan  # the intraday spread restarts each session
        return z, zp
    return data._get(("integrity_z", p.formation, p.hedge, p.z_mode, p.anchor), calc)


def qualifying(data: PairData, p, tol: float) -> np.ndarray:
    """Per bar: side (+1 / -1) of a qualifying entry decision, 0 = none (independent z).
    tol > 0 lenient (confirm the backtester's trades), tol < 0 strict (skipped-signal check)."""
    z, zp = _independent_zz(data, p)
    E = p.entry_z
    with np.errstate(invalid="ignore"):
        lg = (z <= -E + tol) & (zp > -E - tol)
        sh = (z >= E - tol) & (zp < E + tol)
    side = np.where(lg, 1, np.where(sh, -1, 0))
    if p.side == "long":
        side = np.where(side > 0, side, 0)
    elif p.side == "short":
        side = np.where(side < 0, side, 0)
    to_close = data.tod[data.sess_end] - data.tod
    side = np.where(~data.is_last & (to_close >= p.last_entry_cutoff), side, 0)
    if p.first_entry > 0:
        _, starts, _ = _sessions(data)
        num = _sessions(data)[0]
        since_open = data.tod + data.tf_minutes - data.tod[starts[num]]
        side = np.where(since_open >= p.first_entry, side, 0)
    return side


def check_sim_integrity(sim: SimResult, data: PairData, exec_config: ExecutionConfig, cfg) -> list[str]:
    p = as_params(cfg)
    issues: set[str] = set()
    nt = len(sim.entry_idx)
    if nt == 0:
        return []
    la, lb = _legs(data.pair)
    ec = exec_config
    com, tk_m, tk_s = ec.commission_per_contract, ec.slippage_ticks_market, ec.slippage_ticks_stop
    n = data.n
    k, e, x, j, d = sim.signal_idx, sim.entry_idx, sim.exit_idx, sim.decision_idx, sim.side
    prm = _month_params(data, p, k)
    if np.any(prm["fit_end"] >= k) or np.any(prm["start"] > k):
        issues.add("hedge_fit_not_before_decision")
    if not np.allclose(sim.beta, prm["beta"], rtol=0, atol=1e-12) or np.any(sim.month != prm["month"]):
        issues.add("beta_not_month_fit")
    lenient = qualifying(data, p, 1e-9)
    if np.any(lenient[k] != d):
        bad = lenient[k] != d
        if np.any((d[bad] != 1) & (d[bad] != -1)) or (p.side == "long" and np.any(d < 0)) or (p.side == "short" and np.any(d > 0)):
            issues.add("side_not_allowed")
        to_close = data.tod[data.sess_end[k]] - data.tod[k]
        if np.any(data.is_last[k] | (to_close < p.last_entry_cutoff)):
            issues.add("entry_inside_last_entry_cutoff")
        issues.add("signal_not_fresh_cross")
    if p.first_entry > 0 and np.any(data.tod[k] + data.tf_minutes - data.tod[data.sess_start[k]] < p.first_entry):
        issues.add("entry_before_first_entry")
    if np.any(e <= k) or np.any(data.session_date[e] != data.session_date[k]):
        issues.add("entry_not_next_bar_same_session")
    a_mkt = data.open[e] + d * tk_m * la.tick
    b_mkt = data.b_open[e] - d * tk_m * lb.tick
    if np.any(d * (sim.a_entry - a_mkt) < -_EPS) or np.any(-d * (sim.b_entry - b_mkt) < -_EPS):
        issues.add("entry_fill_better_than_market")
    if np.any(x < e) or np.any(j < e) or np.any(x < j):
        issues.add("exit_before_entry")
    if p.overnight == "flat" and np.any(data.session_date[x] != data.session_date[e]):
        issues.add("position_held_overnight")
    if nt > 1 and np.any(k[1:] < x[:-1]):
        issues.add("overlapping_positions")
    if np.any(sim.qa < 1) or np.any(sim.qb < 1):
        issues.add("undersized_leg")
    gross = (sim.qa * la.mult * (data.open[e] - data.price_adj[e]) + sim.qb * lb.mult * (data.b_open[e] - data.b_price_adj[e])
             + com * (sim.qa + sim.qb))
    if np.any(gross > sim.equity_before * (1 + 1e-9)):
        issues.add("position_exceeds_equity")
    if np.any(sim.forced_close[:-1]):
        issues.add("forced_close_not_final_trade")

    # exits: first bar a rule fired, the right fill
    for t in range(nt):
        kt, et, jt, xt, dt = int(k[t]), int(e[t]), int(j[t]), int(x[t]), int(d[t])
        pt = {kk: v[t] for kk, v in prm.items()}
        H = time_stop_bars(p, float(pt["emrt"]))
        if (H is None) != (sim.hold_limit[t] < 0) or (H is not None and H != sim.hold_limit[t]):
            issues.add("time_stop_not_per_rule")
        T = et + H - 1 if H is not None else n
        span = np.arange(et, jt + 1)
        zz = independent_z(data, span, {kk: np.full(len(span), v) for kk, v in pt.items()}, p.z_mode, p.anchor)
        tgt, stp = exit_levels(p, dt)
        with np.errstate(invalid="ignore"):
            ht = (zz >= tgt - 1e-9) if dt > 0 else (zz <= tgt + 1e-9)
            hs = np.zeros(len(span), bool) if stp is None else ((zz <= stp + 1e-9) if dt > 0 else (zz >= stp - 1e-9))
            ht_s = (zz >= tgt + 1e-9) if dt > 0 else (zz <= tgt - 1e-9)
            hs_s = np.zeros(len(span), bool) if stp is None else ((zz <= stp - 1e-9) if dt > 0 else (zz >= stp + 1e-9))
        cl = (span == T) | (span == n - 1)
        if p.overnight == "flat":
            cl |= span == data.sess_end[span]
        if np.any((ht_s | hs_s | cl)[:-1]):
            issues.add("exit_not_at_first_rule")
        why = sim.exit_reason[t]
        last_ok = {TARGET_EXIT: ht[-1], STOP_EXIT: hs[-1], TIME_EXIT: jt == T, FORCED: jt == n - 1,
                   EOD_EXIT: p.overnight == "flat" and jt == data.sess_end[jt]}.get(why, False)
        if not last_ok:
            issues.add("exit_rule_not_met")
        at_close = cl[-1]
        if (at_close and xt != jt) or (not at_close and xt != jt + 1):
            issues.add("exit_fill_not_per_rule")
        ticks = tk_s if why == STOP_EXIT else tk_m
        a_ref = data.close[xt] if at_close else data.open[xt]
        b_ref = data.b_close[xt] if at_close else data.b_open[xt]
        if dt * (sim.a_exit[t] - (a_ref - dt * ticks * la.tick)) > _EPS or -dt * (sim.b_exit[t] - (b_ref + dt * ticks * lb.tick)) > _EPS:
            issues.add("exit_fill_better_than_market")
        ra = int(np.sum(data.price_adj[et + 1:xt + 1] != data.price_adj[et:xt]))
        rb = int(np.sum(data.b_price_adj[et + 1:xt + 1] != data.b_price_adj[et:xt]))
        roll = ra * sim.qa[t] * 2 * (com + tk_m * la.tick * la.mult) + rb * sim.qb[t] * 2 * (com + tk_m * lb.tick * lb.mult)
        if not math.isclose(roll, sim.roll_cost[t], rel_tol=1e-9, abs_tol=1e-6) or ra + rb != sim.n_rolls[t]:
            issues.add("roll_cost_mismatch")
        if p.overnight == "flat" and ra + rb:
            issues.add("position_held_overnight")
        pnl = (dt * sim.qa[t] * la.mult * (sim.a_exit[t] - sim.a_entry[t])
               - dt * sim.qb[t] * lb.mult * (sim.b_exit[t] - sim.b_entry[t]) - 2 * com * (sim.qa[t] + sim.qb[t]) - roll)
        if not math.isclose(pnl, sim.realized_pnl[t], rel_tol=1e-9, abs_tol=1e-4):
            issues.add("pnl_mismatch")
    eq = sim.equity_before
    if nt > 1 and not np.allclose(eq[1:], eq[:-1] + sim.realized_pnl[:-1], rtol=1e-12, atol=1e-4):
        issues.add("pnl_mismatch")

    # no qualifying signal skipped while flat (strict); not checkable when entries are randomly missed
    strict = qualifying(data, p, -1e-9)
    bounds = np.concatenate([[0], x])
    ends = np.concatenate([k, [n]])
    for t in range(nt + 1):
        lo, hi = int(bounds[t]), int(ends[t])
        cand = np.flatnonzero(strict[lo:hi]) + lo
        for kk in cand.tolist():
            ee = kk + 1
            if ee >= n or ee > data.sess_end[kk]:
                continue
            bt = _month_params(data, p, np.array([kk]))["beta"][0]
            eqv = eq[t] if t < nt else (eq[-1] + sim.realized_pnl[-1])
            qa, _ = size_pair(eqv, (data.open[ee] - data.price_adj[ee]) * la.mult,
                              (data.b_open[ee] - data.b_price_adj[ee]) * lb.mult, bt, com)
            if qa >= 1:
                issues.add("signal_skipped_while_flat")
                break
        if "signal_skipped_while_flat" in issues:
            break
    return sorted(issues)


_TRUNC: dict[tuple, PairData] = {}


def _cached(bars: pl.DataFrame, cut: int) -> PairData:
    """Truncated data objects are reused across the sampled configs of one run (each is built only
    from its own first `cut` bars, so sharing it cannot leak anything; the monthly refits are the
    slow part and are then computed once per cut)."""
    key = (bars.height, cut, str(bars["bar_open_ts"][0]), str(bars["bar_open_ts"][-1]),
           str(bars["timeframe"][0]), float(bars["close"].sum()))
    if key not in _TRUNC:
        if len(_TRUNC) > 64:
            _TRUNC.clear()
        _TRUNC[key] = PairData(bars.head(cut))
    return _TRUNC[key]


def truncation_invariance(
    bars: pl.DataFrame, cfg, *, exec_config: ExecutionConfig,
    cut_fracs: tuple[float, ...] = (0.35, 0.6, 0.85),
) -> list[str]:
    """Return a list of mismatch descriptions (empty = no look-ahead detected)."""
    bars = bars.sort("bar_open_ts")
    eq0 = exec_config.starting_equity
    full = simulate_emrt_spread(_cached(bars, bars.height), cfg, exec_config=exec_config, starting_equity=eq0)
    problems: list[str] = []
    for frac in cut_fracs:
        cut = int(bars.height * frac)
        part = simulate_emrt_spread(_cached(bars, cut), cfg, exec_config=exec_config, starting_equity=eq0)
        done = ~part.forced_close
        kk = int(done.sum())
        if kk > len(full.entry_idx):
            problems.append(f"cut@{frac}: truncated run has more completed trades")
            continue
        for name in ("signal_idx", "entry_idx", "exit_idx", "qa", "qb", "beta", "a_entry", "a_exit",
                     "b_entry", "b_exit", "side", "realized_pnl"):
            a, b = getattr(part, name)[done], getattr(full, name)[:kk]
            if not np.allclose(a, b, rtol=0, atol=1e-9):
                problems.append(f"cut@{frac}: {name} differs from full-data run")
                break
    return problems
