"""Random-entry benchmark: is a strategy's out-of-sample result better than luck?

For a target time in market (share of the window's bars with an open position),
`simulate_random_entries` places long trades at random bars inside the window,
each held a random 3-10 bars and exited on time, with no overlap, so the trades
cover that share of bars. Fills, slippage, commission and whole-contract sizing
are the strategy's own (`CostModel`), and the result is a `SimResult`, so the
same `daily_equity` / `window_metrics` code scores it (Sharpe, return, time in
market are computed exactly like a finalist's).

Exposure is counted as the engine counts it: a trade entered at bar e and exited
at the open of bar e+H occupies H+1 bars (entry bar through exit bar).
"""

from __future__ import annotations

from datetime import date

import numpy as np

from src.strategies.mean_reversion.backtest import TIME_EXIT, CostModel, MRData, SimResult
from src.utils.config_models import ExecutionConfig


def _random_lengths(target_bars: float, rng: np.random.Generator, hold_lo: int, hold_hi: int) -> list[int]:
    """Occupied-bar lengths (hold + 1) summing to ~target_bars; the last trade is kept
    with probability equal to the fraction of it that fits, so the total is unbiased."""
    lens: list[int] = []
    tot = 0
    while True:
        L = int(rng.integers(hold_lo, hold_hi + 1)) + 1
        if tot + L <= target_bars:
            lens.append(L)
            tot += L
            continue
        if rng.random() < (target_bars - tot) / L:
            lens.append(L)
        return lens


def random_intervals(n_bars: int, exposure: float, rng: np.random.Generator, *,
                     hold_lo: int = 3, hold_hi: int = 10) -> list[tuple[int, int]]:
    """Non-overlapping (start, hold) pairs, 0-based within a window of n_bars, whose
    occupied bars (hold + 1 each) cover ~`exposure` of the window, placed uniformly."""
    lens = _random_lengths(exposure * n_bars, rng, hold_lo, hold_hi)
    while lens and sum(lens) > n_bars:
        lens.pop()
    k = len(lens)
    if k == 0:
        return []
    rng.shuffle(lens)
    free = n_bars - sum(lens)
    # Uniform composition of `free` idle bars into k+1 gaps (stars and bars).
    cuts = np.sort(rng.choice(free + k, size=k, replace=False))
    gaps = np.diff(np.concatenate([[-1], cuts])) - 1
    out, pos = [], 0
    for g, L in zip(gaps, lens):
        start = pos + int(g)
        out.append((start, L - 1))
        pos = start + L
    return out


def simulate_random_entries(data: MRData, symbol: str, *, exec_config: ExecutionConfig, starting_equity: float,
                            window_start: date, window_end: date, exposure: float, rng: np.random.Generator,
                            hold_lo: int = 3, hold_hi: int = 10) -> SimResult:
    """Random long trades inside [window_start, window_end] at the target exposure,
    entered at a bar's open and exited at the open `hold` bars later, with the
    strategy's own costs and sizing. Equity compounds from `starting_equity`."""
    s64, e64 = np.datetime64(window_start, "D"), np.datetime64(window_end, "D")
    win = np.flatnonzero((data.session_date >= s64) & (data.session_date <= e64))
    costs = CostModel.for_symbol(exec_config, symbol)
    rows = []
    if len(win):
        first, n_bars = int(win[0]), len(win)
        equity = starting_equity
        for start, hold in random_intervals(n_bars, exposure, rng, hold_lo=hold_lo, hold_hi=hold_hi):
            e = first + start
            x = e + hold
            if e < 1 or x >= data.n:
                continue
            entry_px = costs.fill(data.open[e], "buy")
            qty = costs.size(equity, entry_px, entry_px - data.price_adj[e])
            if qty <= 0:
                continue
            exit_px = costs.fill(data.open[x], "sell")
            com = costs.commission(qty)
            realized = (exit_px - entry_px) * qty - 2 * com
            equity += realized
            rows.append((e - 1, e, x, x - 1, qty, entry_px, exit_px, com, realized))
    cols = list(zip(*rows)) if rows else [()] * 9
    k = len(rows)
    return SimResult(
        trades=[], equity_curve=[],
        signal_idx=np.asarray(cols[0], dtype=np.int64), entry_idx=np.asarray(cols[1], dtype=np.int64),
        exit_idx=np.asarray(cols[2], dtype=np.int64), decision_idx=np.asarray(cols[3], dtype=np.int64),
        quantity=np.asarray(cols[4], dtype=float), entry_px=np.asarray(cols[5], dtype=float),
        exit_px=np.asarray(cols[6], dtype=float), entry_commission=np.asarray(cols[7], dtype=float),
        realized_pnl=np.asarray(cols[8], dtype=float), forced_close=np.zeros(k, dtype=bool),
        exit_reason=np.full(k, TIME_EXIT, dtype=object), stop_level=np.full(k, np.nan),
    )
