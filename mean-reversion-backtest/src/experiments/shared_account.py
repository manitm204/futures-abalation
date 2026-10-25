"""Several strategies trading one futures account balance.

Each strategy's entry and exit bars, fill prices and stops come from price alone,
never from position size, so a strategy's trade list is the same at any size.
`share_account` takes those trade lists and re-sizes every trade, in time order,
against one shared balance:

  * a trade is given `per_trade` x the account balance (e.g. 0.75);
  * the account's open positions together may not exceed `cap` x the balance
    (e.g. 1.0), so a trade that opens while another is still open gets only what
    is left (e.g. the remaining 0.25), in whole contracts;
  * a trade that can't afford one contract is skipped.

"Balance" is the account's cash (starting equity plus closed-trade P&L), the
same convention the single-strategy engine sizes from. A position's share of the
cap is its contract value at entry (contracts x raw entry price x multiplier).

Strategies may run on different bar sizes (one `MRData` each), so events are
ordered by clock time: an entry at the open of its bar, an exit at the open of
its exit bar, except a stop, which can fill any time inside its bar and so only
frees capital from the END of that bar. A position closing at or before an entry's
time frees its capital for that entry. Trades entering at the same time go in the
order the strategies are listed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from src.strategies.mean_reversion.backtest import STOP_EXIT, CostModel, MRData, SimResult


@dataclass
class SharedAccountResult:
    sims: list[SimResult]          # one per strategy, re-sized; skipped trades removed
    contracts: list[np.ndarray]    # contracts given to each ORIGINAL trade (0 = skipped)
    trimmed: list[np.ndarray]      # True where the trade got less than `per_trade` because of the cap


def _take(sim: SimResult, keep: np.ndarray, qty: np.ndarray, com: np.ndarray, pnl: np.ndarray) -> SimResult:
    return replace(sim, trades=[], equity_curve=[], signal_idx=sim.signal_idx[keep], entry_idx=sim.entry_idx[keep],
                   exit_idx=sim.exit_idx[keep], decision_idx=sim.decision_idx[keep], quantity=qty[keep],
                   entry_px=sim.entry_px[keep], exit_px=sim.exit_px[keep], entry_commission=com[keep],
                   realized_pnl=pnl[keep], forced_close=sim.forced_close[keep], exit_reason=sim.exit_reason[keep],
                   stop_level=sim.stop_level[keep])


def share_account(sims: list[SimResult], data: MRData | list[MRData], costs: CostModel, starting_equity: float, *,
                  bar_minutes: int | list[int] = 0, per_trade: float = 0.75, cap: float = 1.0) -> SharedAccountResult:
    """`data` / `bar_minutes`: one per strategy, or a single value shared by all."""
    datas = data if isinstance(data, list) else [data] * len(sims)
    mins = bar_minutes if isinstance(bar_minutes, list) else [bar_minutes] * len(sims)
    mult = costs.multiplier
    per_c = costs.ec.commission_per_contract
    events = sorted((datas[s].bar_open[int(e)], s, t) for s, sim in enumerate(sims) for t, e in enumerate(sim.entry_idx))
    n_c = [np.zeros(len(sim.entry_idx), dtype=np.int64) for sim in sims]
    trim = [np.zeros(len(sim.entry_idx), dtype=bool) for sim in sims]
    cash = float(starting_equity)
    open_: list[tuple] = []  # (time capital is freed, allocated value, realized P&L)
    for when, s, t in events:
        still = []
        for free_at, alloc, pnl in open_:
            if free_at <= when:
                cash += pnl
            else:
                still.append((free_at, alloc, pnl))
        open_ = still
        sim, d = sims[s], datas[s]
        e = int(sim.entry_idx[t])
        raw = float(sim.entry_px[t] - d.price_adj[e])
        per = raw * mult
        used = sum(a for _, a, _ in open_)
        want = per_trade * cash
        budget = min(want, cap * cash - used)
        k = int(np.floor(budget / per)) if per > 0 and budget > 0 else 0
        while k > 0 and k * (per + per_c) > budget:
            k -= 1
        n_c[s][t] = k
        trim[s][t] = budget < want and k < int(np.floor(want / per))
        if k == 0:
            continue
        q = k * mult
        pnl = (sim.exit_px[t] - sim.entry_px[t]) * q - 2 * k * per_c
        x = int(sim.exit_idx[t])
        free_at = d.bar_open[x] + (np.timedelta64(mins[s], "m") if sim.exit_reason[t] == STOP_EXIT else np.timedelta64(0, "m"))
        open_.append((free_at, k * per, pnl))
    out = []
    for s, sim in enumerate(sims):
        k = n_c[s]
        q = k * mult
        com = k * per_c
        pnl = (sim.exit_px - sim.entry_px) * q - 2 * com
        out.append(_take(sim, k > 0, q.astype(float), com.astype(float), pnl))
    return SharedAccountResult(out, n_c, trim)
