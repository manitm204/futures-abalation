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

`share_account_multi` adds per-market and per-group caps and per-strategy contract
specs (several markets, micro contracts); `share_account` is its one-market case.

Strategies may run on different bar sizes (one `MRData` each), so events are
ordered by clock time: an entry at the open of its bar, an exit at the open of
its exit bar, except a stop, which can fill any time inside its bar and so only
frees capital from the END of that bar. A position closing at or before an entry's
time frees its capital for that entry. Trades entering at the same time go in the
order the strategies are listed.

Noise-band copy: trades may be short (`SimResult.side`, P&L signed accordingly), and
a session-close exit frees its capital at the end of the last bar, like a stop.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from src.strategies.mean_reversion.backtest import STOP_EXIT, CostModel, MRData, SimResult
from src.strategies.noise_band.backtest import EOD_EXIT, FORCED

# Exits that can fill at any time inside (or at the end of) their bar free capital only from that bar's END:
# a stop, and the noise band's session-close exit, which fills at the last bar's close.
_END_OF_BAR_EXITS = (STOP_EXIT, EOD_EXIT, FORCED)


def _side(sim: SimResult) -> np.ndarray:
    """+1 / -1 per trade; long-only families (no `side`) are all +1."""
    s = getattr(sim, "side", None)
    return np.ones(len(sim.entry_idx)) if s is None else np.asarray(s, dtype=float)


@dataclass
class SharedAccountResult:
    sims: list[SimResult]          # one per strategy, re-sized; skipped trades removed
    contracts: list[np.ndarray]    # contracts given to each ORIGINAL trade (0 = skipped)
    trimmed: list[np.ndarray]      # True where the trade got less than `per_trade` because of a cap
    bound: list[np.ndarray] | None = None  # which cap limited each trade: "market", "group", "total" or ""
    peak: dict | None = None       # largest open value seen at an entry, as a share of the balance


def _take(sim: SimResult, keep: np.ndarray, qty: np.ndarray, com: np.ndarray, pnl: np.ndarray) -> SimResult:
    return replace(sim, trades=[], equity_curve=[], signal_idx=sim.signal_idx[keep], entry_idx=sim.entry_idx[keep],
                   exit_idx=sim.exit_idx[keep], decision_idx=sim.decision_idx[keep], quantity=qty[keep],
                   entry_px=sim.entry_px[keep], exit_px=sim.exit_px[keep], entry_commission=com[keep],
                   realized_pnl=pnl[keep], forced_close=sim.forced_close[keep], exit_reason=sim.exit_reason[keep],
                   stop_level=sim.stop_level[keep],
                   **({"side": sim.side[keep]} if getattr(sim, "side", None) is not None else {}))


def share_account(sims: list[SimResult], data: MRData | list[MRData], costs: CostModel, starting_equity: float, *,
                  bar_minutes: int | list[int] = 0, per_trade: float = 0.75, cap: float = 1.0) -> SharedAccountResult:
    """One market: `data` / `bar_minutes` one per strategy, or a single value shared by all."""
    return share_account_multi(sims, data, costs, starting_equity, bar_minutes=bar_minutes, per_trade=per_trade,
                               total_cap=cap)


def share_account_multi(sims: list[SimResult], data: MRData | list[MRData], costs: CostModel | list[CostModel],
                        starting_equity: float, *, bar_minutes: int | list[int] = 0, per_trade: float = 0.75,
                        total_cap: float = 1.0, market: list[str] | None = None, market_cap: float | None = None,
                        group: list[str | None] | None = None, group_cap: float | None = None) -> SharedAccountResult:
    """Several strategies, possibly on several markets, in one account.

    `costs` (multiplier, commission) may differ per strategy, e.g. micro contracts. A trade's budget is
    the smallest of `per_trade` x balance and the room left under each cap: `total_cap` over everything
    open, `market_cap` over open positions in the same `market`, and `group_cap` over open positions in
    the same `group` (e.g. the correlated stock-index futures; None = in no group)."""
    n = len(sims)
    datas = data if isinstance(data, list) else [data] * n
    mins = bar_minutes if isinstance(bar_minutes, list) else [bar_minutes] * n
    cms = costs if isinstance(costs, list) else [costs] * n
    mkts = market or [""] * n
    grps = group or [None] * n
    events = sorted((datas[s].bar_open[int(e)], s, t) for s, sim in enumerate(sims) for t, e in enumerate(sim.entry_idx))
    n_c = [np.zeros(len(sim.entry_idx), dtype=np.int64) for sim in sims]
    trim = [np.zeros(len(sim.entry_idx), dtype=bool) for sim in sims]
    bound = [np.full(len(sim.entry_idx), "", dtype=object) for sim in sims]
    peak = {"total": 0.0, "market": 0.0, "group": 0.0}
    cash = float(starting_equity)
    open_: list[tuple] = []  # (time capital is freed, allocated value, realized P&L, market, group)
    for when, s, t in events:
        still = []
        for o in open_:
            if o[0] <= when:
                cash += o[2]
            else:
                still.append(o)
        open_ = still
        sim, d, cm = sims[s], datas[s], cms[s]
        e = int(sim.entry_idx[t])
        per = float(sim.entry_px[t] - d.price_adj[e]) * cm.multiplier
        per_c = cm.ec.commission_per_contract
        want = per_trade * cash
        room = {"total": total_cap * cash - sum(o[1] for o in open_)}
        if market_cap is not None:
            room["market"] = market_cap * cash - sum(o[1] for o in open_ if o[3] == mkts[s])
        if group_cap is not None and grps[s] is not None:
            room["group"] = group_cap * cash - sum(o[1] for o in open_ if o[4] == grps[s])
        tight = min(room, key=room.get)
        budget = min(want, room[tight])
        k = int(np.floor(budget / per)) if per > 0 and budget > 0 else 0
        while k > 0 and k * (per + per_c) > budget:
            k -= 1
        n_c[s][t] = k
        trim[s][t] = budget < want and k < int(np.floor(want / per))
        if trim[s][t]:
            bound[s][t] = tight
        if k == 0:
            continue
        q = k * cm.multiplier
        pnl = _side(sim)[t] * (sim.exit_px[t] - sim.entry_px[t]) * q - 2 * k * per_c
        x = int(sim.exit_idx[t])
        free_at = d.bar_open[x] + (np.timedelta64(mins[s], "m") if sim.exit_reason[t] in _END_OF_BAR_EXITS else np.timedelta64(0, "m"))
        open_.append((free_at, k * per, pnl, mkts[s], grps[s]))
        peak["total"] = max(peak["total"], sum(o[1] for o in open_) / cash)
        peak["market"] = max(peak["market"], sum(o[1] for o in open_ if o[3] == mkts[s]) / cash)
        if grps[s] is not None:
            peak["group"] = max(peak["group"], sum(o[1] for o in open_ if o[4] == grps[s]) / cash)
    out = []
    for s, sim in enumerate(sims):
        k = n_c[s]
        q = k * cms[s].multiplier
        com = k * cms[s].ec.commission_per_contract
        pnl = _side(sim) * (sim.exit_px - sim.entry_px) * q - 2 * com
        out.append(_take(sim, k > 0, q.astype(float), com.astype(float), pnl))
    return SharedAccountResult(out, n_c, trim, bound, peak)
