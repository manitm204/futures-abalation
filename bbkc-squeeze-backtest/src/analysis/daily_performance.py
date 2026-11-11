"""Window performance from a regularly sampled, mark-to-market daily equity series.

The engine's equity curve only has a point at each trade EXIT, so Sharpe built
from it skips flat days and open-position swings. Here equity is marked at
every session close of the window:

    equity(d) = start + realized P&L of trades exited by d's last bar
                + qty * (close(d) - entry fill) - entry commission  [open trade]

Returns are close-to-close on EVERY trading day in the window (flat days are 0),
so Sharpe = mean/std(ddof=1) * sqrt(periods_per_year) over a regular grid. Idle
cash is not credited interest and the Sharpe excess is taken over
`risk_free_rate_annual` (0 by default), so the two are consistent. Undefined metrics (zero variance, too few days, non-positive total
P&L for contribution ratios) are returned as None with a flag -- never silently
replaced.
"""

from __future__ import annotations

import math
from datetime import date

import numpy as np
from scipy import stats

from src.strategies.mean_reversion.backtest import MRData, SimResult


def daily_equity(sim: SimResult, data: MRData, starting_equity: float) -> np.ndarray:
    """Mark-to-market equity at every session close in `data` (aligned with data.days)."""
    e = data.day_end_idx
    eq = np.full(len(e), float(starting_equity))
    if len(sim.entry_idx) == 0:
        return eq
    cum = np.concatenate([[0.0], np.cumsum(sim.realized_pnl)])
    k = np.searchsorted(sim.exit_idx, e, side="right")  # trades exited at or before day end
    eq += cum[k]
    j = np.searchsorted(sim.entry_idx, e, side="right") - 1  # latest trade entered by day end
    has = j >= 0
    jj = np.where(has, j, 0)
    open_mask = has & (sim.exit_idx[jj] > e)
    if open_mask.any():
        jo = jj[open_mask]
        side = getattr(sim, "side", None)  # +1 / -1 per trade (noise band); long-only families have none
        sgn = side[jo] if side is not None else 1.0
        eq[open_mask] += (sgn * sim.quantity[jo] * (data.close[e[open_mask]] - sim.entry_px[jo])
                          - sim.entry_commission[jo])
    return eq


def _sharpe(rets: np.ndarray, ppy: int, rf_annual: float) -> tuple[float | None, float | None]:
    """(annualized Sharpe, per-period Sharpe) or (None, None) if undefined."""
    if len(rets) < 2:
        return None, None
    ex = rets - rf_annual / ppy
    sd = float(ex.std(ddof=1))
    if not math.isfinite(sd) or sd <= 0:
        return None, None
    sr = float(ex.mean() / sd)
    return sr * math.sqrt(ppy), sr


def _drawdown(series: np.ndarray) -> tuple[float, int, bool]:
    """(max drawdown <= 0, longest underwater stretch in trading days, recovered?)."""
    peak = np.maximum.accumulate(series)
    dd = series / peak - 1.0
    under = series < peak - 1e-9
    longest = cur = 0
    for u in under:
        cur = cur + 1 if u else 0
        longest = max(longest, cur)
    return float(dd.min()), int(longest), not bool(under[-1]) if len(under) else True


def _ratio(num: float, den: float) -> float | None:
    return float(num / den) if den > 0 else None


def window_metrics(
    sim: SimResult,
    data: MRData,
    eq_daily: np.ndarray,
    *,
    start: date,
    end: date,
    starting_equity: float,
    periods_per_year: int = 252,
    risk_free_rate_annual: float = 0.0,
    top_trades_k: int = 5,
    top_trades_frac: float = 0.05,
) -> tuple[dict, np.ndarray]:
    """Metrics for [start, end] (NY session dates). Returns (metrics, daily returns)."""
    days = data.days
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    dmask = (days >= s64) & (days <= e64)
    flags: list[str] = []
    prior = np.flatnonzero(days < s64)
    eq0 = float(eq_daily[prior[-1]]) if len(prior) else float(starting_equity)
    eq_win = eq_daily[dmask]
    series = np.concatenate([[eq0], eq_win])
    rets = series[1:] / series[:-1] - 1.0 if len(eq_win) else np.array([])
    n_days = len(rets)
    ppy = periods_per_year

    sharpe, sr_pp = _sharpe(rets, ppy, risk_free_rate_annual)
    if sharpe is None:
        flags.append("sharpe_undefined")
    net_return = float(series[-1] / series[0] - 1.0)
    total_pnl = float(series[-1] - series[0])
    cagr = (float((series[-1] / series[0]) ** (ppy / n_days) - 1.0)
            if n_days > 0 and series[-1] > 0 else None)
    max_dd, dd_dur, recovered = _drawdown(series)

    # Trades attributed to the window by ENTRY session date.
    ent_day = data.session_date[sim.entry_idx] if len(sim.entry_idx) else np.array([], dtype="datetime64[D]")
    tmask = (ent_day >= s64) & (ent_day <= e64)
    pnl = sim.realized_pnl[tmask]
    forced = sim.forced_close[tmask]
    completed = int((~forced).sum())
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    profit_factor = _ratio(float(wins.sum()), float(-losses.sum()))
    if profit_factor is None and len(pnl):
        flags.append("profit_factor_undefined_no_losses")

    # Exposure: fraction of the window's bars with an open position.
    bar_mask = (data.session_date >= s64) & (data.session_date <= e64)
    win_bars = int(bar_mask.sum())
    in_mkt = 0
    if win_bars and tmask.any():
        first_bar = int(np.argmax(bar_mask))
        last_bar = first_bar + win_bars - 1
        a = np.clip(sim.entry_idx[tmask], first_bar, last_bar)
        b = np.clip(sim.exit_idx[tmask], first_bar, last_bar)
        in_mkt = int((b - a + 1).sum())
    exposure = in_mkt / win_bars if win_bars else None
    notional = float((sim.quantity[tmask] * (sim.entry_px[tmask] + sim.exit_px[tmask])).sum())
    years = n_days / ppy if n_days else 0.0
    turnover = notional / float(np.mean(series)) / years if years > 0 else None

    # Overlap / independence: the engine holds one position at a time, so
    # concurrent overlap is 0 by construction; trades sharing a session are the
    # remaining source of clustering.
    if tmask.any():
        _, counts = np.unique(ent_day[tmask], return_counts=True)
        same_session_frac = float(counts[counts > 1].sum() / counts.sum())
    else:
        same_session_frac = None
    overlap = 0
    if tmask.sum() > 1:
        ei, xi = sim.entry_idx[tmask], sim.exit_idx[tmask]
        overlap = int((ei[1:] <= xi[:-1]).sum())

    # Per-year slices (in-sample diagnostics when the window is development).
    year_ret, year_sharpe, year_trades, year_pnl = {}, {}, {}, {}
    wdays = days[dmask]
    years_in = sorted({int(str(d)[:4]) for d in wdays})
    ent_year = np.array([int(str(d)[:4]) for d in ent_day[tmask]]) if tmask.any() else np.array([], dtype=int)
    day_year = np.array([int(str(d)[:4]) for d in wdays])
    for y in years_in:
        ym = day_year == y
        idx = np.flatnonzero(ym)
        y0 = series[idx[0]]  # series is offset by one: series[i] is equity before day i
        y1 = series[idx[-1] + 1]
        year_ret[y] = float(y1 / y0 - 1.0)
        year_pnl[y] = float(y1 - y0)
        year_sharpe[y] = _sharpe(rets[ym], ppy, risk_free_rate_annual)[0]
        year_trades[y] = int(((ent_year == y) & ~forced).sum()) if len(ent_year) else 0
    n_profitable_years = sum(1 for v in year_ret.values() if v > 0)

    best_year = max(year_pnl, key=year_pnl.get) if year_pnl else None
    if best_year is not None:
        keep = day_year != best_year
        excl_ret = float(np.prod(1 + rets[keep]) - 1.0) if keep.any() else None
        excl_sharpe = _sharpe(rets[keep], ppy, risk_free_rate_annual)[0]
    else:
        excl_ret = excl_sharpe = None
    best_year_contrib = _ratio(year_pnl[best_year], total_pnl) if best_year is not None else None
    win_sorted = np.sort(wins)[::-1]
    k_frac = max(1, math.ceil(top_trades_frac * len(pnl))) if len(pnl) else 0
    top_k_contrib = _ratio(float(win_sorted[:top_trades_k].sum()), total_pnl) if len(win_sorted) else None
    top_frac_contrib = _ratio(float(win_sorted[:k_frac].sum()), total_pnl) if len(win_sorted) else None
    if total_pnl <= 0:
        flags.append("contribution_ratios_undefined_nonpositive_total")

    if n_days >= 3 and float(rets.std()) > 0:
        skew = float(stats.skew(rets))
        exkurt = float(stats.kurtosis(rets))  # excess (normal = 0)
        rho1 = float(np.corrcoef(rets[:-1], rets[1:])[0, 1]) if n_days > 3 else None
    else:
        skew = exkurt = rho1 = None

    m = {
        "n_days": n_days, "start_equity": float(series[0]), "end_equity": float(series[-1]),
        "net_return": net_return, "net_pnl": total_pnl, "cagr": cagr,
        "sharpe": sharpe, "sharpe_per_period": sr_pp,
        "max_drawdown": max_dd, "max_dd_duration_days": dd_dur, "dd_recovered": recovered,
        "n_trades": int(tmask.sum()), "n_completed_trades": completed, "n_forced_close": int(forced.sum()),
        "profit_factor": profit_factor, "win_rate": float((pnl > 0).mean()) if len(pnl) else None,
        "exposure": exposure, "turnover_annual": turnover,
        "concurrent_overlap_trades": overlap, "same_session_trade_frac": same_session_frac,
        "year_return": year_ret, "year_sharpe": year_sharpe, "year_trades": year_trades,
        "year_pnl": year_pnl, "n_profitable_years": n_profitable_years,
        "best_year": best_year, "best_year_contribution": best_year_contrib,
        "excl_best_year_return": excl_ret, "excl_best_year_sharpe": excl_sharpe,
        "top_k_trades_contribution": top_k_contrib, "top_frac_trades_contribution": top_frac_contrib,
        "skew": skew, "excess_kurtosis": exkurt, "autocorr_lag1": rho1,
        "flags": flags,
    }
    return m, rets
