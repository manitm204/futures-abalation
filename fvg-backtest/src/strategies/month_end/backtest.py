"""Compact 1-minute backtester for the Treasury month-end long, day session only (ZN / ZB).

Bars: only 1-minute bars whose NY open time is in [08:00, 17:00) are used (`me_day_bars`). Each
NY date is one session, so the session's last bar is the last bar before 17:00 ET and nothing
can be held overnight.

Per session date D:
    rank(D)  = number of NYSE trading days in D's calendar month on or after D (1 = the month's
               last trading day; 0 = D is not an NYSE trading day). Taken from the NYSE calendar,
               which is published in advance, so it never depends on later bars.
    first(D) = number of NYSE trading days in D's month on or before D (1 = the first; 0 = not a
               trading day)
    eligible if (1 <= rank(D) <= window or 1 <= first(D) <= first_days) and the event filter
             allows D (v1 has first_days = 0)
    trade    : LONG, enters at `entry`, exits at the exit rule's time (+ `exit_shift` minutes)

Execution (audited by src/experiments/me_integrity.py):
  * entry at the OPEN of the first bar whose open time is >= the entry time, with market
    slippage; if that bar opens more than MAX_ENTRY_LAG_MIN late (a gap in the bars) or is not
    before the exit, the day is skipped. `signal_idx` = the entry bar (a calendar rule, known in
    advance);
  * stop (optional): entry price before slippage x (1 - stop%), live intrabar from the entry bar,
    filled at the worse of the bar's open and the stop, with stop slippage;
  * time exit at the CLOSE of the last bar whose open time is < the exit time, with market
    slippage; when that bar is the session's last bar (early closes: the bars stop before the
    exit time) the exit is counted as `eod_exit`;
  * one position at a time, compounding equity, unlevered whole contracts (the other families'
    sizing); every fill pays adverse slippage + commission;
  * a position closed on the data's final bar by the session-close rule is flagged forced and is
    not a completed trade.
`day_mask` (placebo benchmark only) replaces the month-end rule with an explicit set of days.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas_market_calendars as mcal
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.month_end.config import (
    DAY_END_MIN,
    DAY_START_MIN,
    ENTRY_TIMES,
    EVENT_FILTERS,
    FOMC_DAYS,
    MAX_ENTRY_LAG_MIN,
    auction_days,
    exit_minutes,
)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "forced_close"


def me_day_bars(df_1min: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """The strategy's bars: clean 1-minute bars with NY open time in [08:00, 17:00), RTH flag
    ignored (the post-2021 strike at 16:00 ET is after the 15:00 ET pit close the other families
    use for ZN / ZB). Single symbol."""
    if timeframe != "1min":
        raise ValueError(f"month_end runs on 1-minute bars only, got {timeframe!r}")
    if df_1min.is_empty():
        return df_1min
    ny = pl.col("bar_open_ts_ny")
    tod = ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)
    return (df_1min.filter((tod >= DAY_START_MIN) & (tod < DAY_END_MIN)
                           & (ny.dt.date() == pl.col("session_date_ny")))
            .sort("bar_open_ts"))


def month_end_rank(days: list[date], *, from_start: bool = False) -> np.ndarray:
    """Per date: NYSE trading days in its calendar month on or after it (0 = not a trading day);
    with `from_start`, on or before it (1 = the month's first trading day). Uses the whole month's
    calendar, so the last data month is ranked as if complete."""
    if not days:
        return np.array([], dtype=np.int64)
    first = min(days).replace(day=1)
    last = max(days)
    end = date(last.year + (last.month == 12), last.month % 12 + 1, 1)
    sched = mcal.get_calendar("NYSE").schedule(start_date=first, end_date=end)
    tdays = [ts.date() for ts in sched.index]
    rank: dict[date, int] = {}
    by_month: dict[tuple[int, int], list[date]] = {}
    for d in tdays:
        by_month.setdefault((d.year, d.month), []).append(d)
    for ds in by_month.values():
        for i, d in enumerate(ds):
            rank[d] = i + 1 if from_start else len(ds) - i
    return np.array([rank.get(d, 0) for d in days], dtype=np.int64)


class MEData(CBData):
    """CBData (session structure, tod, caching) plus the month-end rank, the event flags and the
    strike regime per session."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        self.day_list: list[date] = [d.astype(object) for d in self.days]
        self.rank = month_end_rank(self.day_list)
        self.rank_start = month_end_rank(self.day_list, from_start=True)
        self.is_fomc = np.array([d in FOMC_DAYS for d in self.day_list], dtype=bool)
        auc = auction_days()
        self.is_auction = np.array([d in auc for d in self.day_list], dtype=bool)
        # Monotonic (session, minute) key for vectorized "first bar at/after a time" lookups.
        self._key = self.sess * 1440 + self.tod

    def bar_at_or_after(self, minutes: np.ndarray) -> np.ndarray:
        """Per session: index of the first bar with open time >= minutes[s] (day_end + 1 if none)."""
        s = np.arange(len(self.days), dtype=np.int64)
        return np.searchsorted(self._key, s * 1440 + minutes, side="left")

    def exit_target(self, rule: str, shift: int = 0) -> np.ndarray:
        return self._get(("exit_target", rule, shift), lambda: np.array(
            [exit_minutes(rule, d) + shift for d in self.day_list], dtype=np.int64))

    def filter_ok(self, event_filter: str) -> np.ndarray:
        if event_filter not in EVENT_FILTERS:
            raise ValueError(f"Unknown event_filter {event_filter!r}")
        ok = np.ones(len(self.days), dtype=bool)
        if event_filter in ("skip_fomc", "skip_fomc_auction"):
            ok &= ~self.is_fomc
        if event_filter == "skip_fomc_auction":
            ok &= ~self.is_auction
        return ok


@dataclass(frozen=True)
class MEParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    window: int
    entry_min: int          # NY minutes from midnight
    exit_rule: str          # "15:00" / "16:00" / "strike"
    event_filter: str
    exit_shift: int = 0     # minutes added to the exit target (local moves only)
    stop_pct: float | None = None   # None = no stop
    first_days: int = 0     # v2: also the next month's first N trading days

    @classmethod
    def from_config(cls, cfg) -> "MEParams":
        return cls(cfg.symbol, cfg.timeframe, int(cfg.window), ENTRY_TIMES[cfg.entry], cfg.exit, cfg.event_filter,
                   0, cfg.stop_pct_value, int(getattr(cfg, "first_days", 0)))


def as_params(cfg) -> MEParams:
    return cfg if isinstance(cfg, MEParams) else MEParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is always +1 (long); quantities are always positive."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray
    quantity: np.ndarray
    entry_px: np.ndarray
    exit_px: np.ndarray
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray
    entry_base: np.ndarray    # entry price before slippage
    side: np.ndarray
    stop_level: np.ndarray    # nan = no stop


def eligible_days(data: MEData, p: MEParams, day_mask: np.ndarray | None = None) -> np.ndarray:
    exit_minutes(p.exit_rule, date(2020, 1, 1))   # raises on an unknown exit rule
    if day_mask is not None:
        return np.asarray(day_mask, dtype=bool)
    if p.window < 0 or p.first_days < 0 or p.window + p.first_days < 1:
        raise ValueError(f"need window + first_days >= 1, got {p.window} + {p.first_days}")
    days = ((data.rank >= 1) & (data.rank <= p.window)) | ((data.rank_start >= 1) & (data.rank_start <= p.first_days))
    return days & data.filter_ok(p.event_filter)


def planned_trades(data: MEData, p: MEParams, day_mask: np.ndarray | None = None) -> dict[str, np.ndarray]:
    """Every trade the rules call for, before sizing, in time order: entry bar e, exit bar x, and
    whether x is a time exit (else the session's last bar)."""
    empty = {"e": np.array([], dtype=np.int64), "x": np.array([], dtype=np.int64),
             "timed": np.array([], dtype=bool)}
    if data.n == 0:
        return empty
    ok = eligible_days(data, p, day_mask)
    ds, de = data.day_start_idx, data.day_end_idx
    S = len(data.days)
    start = np.full(S, p.entry_min, dtype=np.int64)
    end = data.exit_target(p.exit_rule, p.exit_shift)
    e = data.bar_at_or_after(start)
    x = np.minimum(data.bar_at_or_after(end) - 1, de)   # last bar opening before the exit time
    valid = ok & (e <= de)
    e_c = np.minimum(e, data.n - 1)
    valid &= data.tod[e_c] - start <= MAX_ENTRY_LAG_MIN
    valid &= (e <= x) & (x >= ds)
    timed = x < de
    s = np.flatnonzero(valid)
    return {"e": e[s].astype(np.int64), "x": x[s].astype(np.int64), "timed": timed[s]}


def simulate_month_end(
    data: MEData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
    day_mask: np.ndarray | None = None,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many bars late (still
    not after the exit bar, else skipped); `missed_entry_frac` drops that fraction of the trades."""
    p = as_params(cfg)
    plan = planned_trades(data, p, day_mask)
    o, lo, c, ts, n = data.open, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    for e0, x, timed in zip(plan["e"].tolist(), plan["x"].tolist(), plan["timed"].tolist()):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = e0 + entry_delay_bars
        if e < free_from or e > x:
            continue
        base = o[e]
        fill_px = costs.fill(base, "buy")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side="long", quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        stop = base * (1 - p.stop_pct / 100) if p.stop_pct is not None else float("nan")
        j = x
        if p.stop_pct is not None:
            hit = np.flatnonzero(lo[e:x + 1] <= stop)
            j = e + int(hit[0]) if len(hit) else x
        if p.stop_pct is not None and lo[j] <= stop:
            why, exit_px = STOP_EXIT, costs.fill(min(o[j], stop), "sell", stop=True)
        else:
            why = TIME_EXIT if timed else (FORCED if x == n - 1 else EOD_EXIT)
            exit_px = costs.fill(c[x], "sell")
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side="long", quantity=qty, fill_price=exit_px,
                         fill_ts=ts[j], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[j])
        commissions = entry_fill.commission + exit_fill.commission
        realized = (exit_px - fill_px) * qty - commissions
        reason = {EOD_EXIT: ExitReason.SESSION_EXIT, FORCED: ExitReason.SESSION_EXIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, STOP_EXIT: ExitReason.STOP_LOSS}[why]
        has_stop = p.stop_pct is not None
        risk = base - stop if has_stop else float("nan")
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side="long", entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop, target_price=None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (risk * qty) if has_stop and risk > 0 else None,
            commission_total=commissions, holding_bars=j - e,
        ))
        rows.append((e0, e, j, e0, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, base, 1, stop))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[j], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = j + 1

    cols = list(zip(*rows)) if rows else [()] * 14
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), entry_base=f(cols[11]), side=i64(cols[12]),
        stop_level=f(cols[13]),
    )
