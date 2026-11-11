"""Random-entry benchmark for the noise band: is a finalist's out-of-sample result
better than luck at the same time in market?

The noise-band counterpart of the mean-reversion random_entry module, with the
noise band's own constraints so the comparison is like for like:

  * intraday only: every random trade opens and closes inside one session (the
    strategy is always flat by the close), and trades never overlap;
  * trade lengths are drawn from a pool (the finalists' own validation trade lengths
    in bars), so trade count, and therefore costs, match the strategy's;
  * each trade is long with probability `p_long` (1.0 for long-only finalists; the
    finalists' actual long share for "both"), otherwise short;
  * fills, slippage, commission and whole-contract sizing are the strategy's own
    (`CostModel`), and the result is a noise-band `SimResult`, so the same
    `daily_equity` / `window_metrics` code scores it.

Exposure is counted as the engine counts it: a trade occupying bars e..e+L-1 has
exposure L bars. It enters at bar e's open and exits at bar e+L-1's open, like a
trailing exit; when that last bar is the session's last bar it exits at that bar's
close instead, like the strategy's session-close exit.
"""

from __future__ import annotations

from datetime import date

import numpy as np

from src.strategies.noise_band.backtest import EOD_EXIT, TRAIL_EXIT, CostModel, NBData, SimResult
from src.utils.config_models import ExecutionConfig


def _draw_lengths(target_bars: float, pool: np.ndarray, rng: np.random.Generator) -> list[int]:
    """Lengths from `pool` summing to ~target_bars; the last one is kept with probability
    equal to the fraction of it that fits, so the expected total is the target."""
    lens: list[int] = []
    tot = 0
    while True:
        L = int(pool[rng.integers(len(pool))])
        if tot + L <= target_bars:
            lens.append(L)
            tot += L
            continue
        if rng.random() < (target_bars - tot) / L:
            lens.append(L)
        return lens


def place_intraday(sess_bars: np.ndarray, lengths: list[int], rng: np.random.Generator,
                   max_tries: int = 50) -> list[tuple[int, int]]:
    """Assign each trade to a uniformly random session it fits in (no overlap with the
    session's other trades), then spread each session's trades uniformly over its bars.
    Returns (session index, start bar within the session, length) as (sess, start, L)."""
    load = np.zeros(len(sess_bars), dtype=np.int64)
    by_sess: dict[int, list[int]] = {}
    for L in lengths:
        for _ in range(max_tries):
            s = int(rng.integers(len(sess_bars)))
            if load[s] + L <= sess_bars[s]:
                load[s] += L
                by_sess.setdefault(s, []).append(L)
                break
        # a trade that finds no room after max_tries is dropped (rare at these exposures)
    out = []
    for s, lens in by_sess.items():
        rng.shuffle(lens)
        k, free = len(lens), int(sess_bars[s] - sum(lens))
        cuts = np.sort(rng.choice(free + k, size=k, replace=False))
        gaps = np.diff(np.concatenate([[-1], cuts])) - 1  # uniform split of idle bars into k+1 gaps
        pos = 0
        for g, L in zip(gaps, lens):
            start = pos + int(g)
            out.append((s, start, L))
            pos = start + L
    return out


def simulate_random_intraday(data: NBData, symbol: str, *, exec_config: ExecutionConfig, starting_equity: float,
                             window_start: date, window_end: date, exposure: float, length_pool: np.ndarray,
                             p_long: float, rng: np.random.Generator) -> SimResult:
    """Random intraday trades inside [window_start, window_end] at the target exposure."""
    s64, e64 = np.datetime64(window_start, "D"), np.datetime64(window_end, "D")
    sess_ids = np.flatnonzero((data.days >= s64) & (data.days <= e64))
    starts, ends = data.day_start_idx[sess_ids], data.day_end_idx[sess_ids]
    sess_bars = ends - starts + 1
    costs = CostModel.for_symbol(exec_config, symbol)
    rows = []
    if len(sess_ids):
        lengths = _draw_lengths(exposure * float(sess_bars.sum()), np.asarray(length_pool), rng)
        trades = sorted((int(starts[s]) + st, L) for s, st, L in place_intraday(sess_bars, lengths, rng))
        sides = np.where(rng.random(len(trades)) < p_long, 1, -1)
        equity = starting_equity
        for (e, L), d in zip(trades, sides):
            x = e + L - 1
            last = x == data.sess_end[e]
            entry_px = costs.fill(data.open[e], "buy" if d > 0 else "sell")
            qty = costs.size(equity, entry_px, entry_px - data.price_adj[e])
            if qty <= 0:
                continue
            exit_px = costs.fill(data.close[x] if last else data.open[x], "sell" if d > 0 else "buy")
            com = costs.commission(qty)
            realized = d * (exit_px - entry_px) * qty - 2 * com
            equity += realized
            rows.append((e - 1, e, x, x if last else x - 1, qty, entry_px, exit_px, com, realized,
                         EOD_EXIT if last else TRAIL_EXIT, int(d)))
    cols = list(zip(*rows)) if rows else [()] * 11
    k = len(rows)
    return SimResult(
        trades=[], equity_curve=[],
        signal_idx=np.asarray(cols[0], dtype=np.int64), entry_idx=np.asarray(cols[1], dtype=np.int64),
        exit_idx=np.asarray(cols[2], dtype=np.int64), decision_idx=np.asarray(cols[3], dtype=np.int64),
        quantity=np.asarray(cols[4], dtype=float), entry_px=np.asarray(cols[5], dtype=float),
        exit_px=np.asarray(cols[6], dtype=float), entry_commission=np.asarray(cols[7], dtype=float),
        realized_pnl=np.asarray(cols[8], dtype=float), forced_close=np.zeros(k, dtype=bool),
        exit_reason=np.asarray(cols[9], dtype=object), stop_level=np.full(k, np.nan),
        side=np.asarray(cols[10], dtype=np.int64),
    )
