"""Compact 1-minute backtester for the daytime FX-fix reversal legs (6E / 6J).

Bars: only 1-minute bars whose NY open time is in [08:00, 17:00) are used (`fx_day_bars`). Each
NY date is one session, so the session's last bar is the last bar before 17:00 ET and nothing
can be held overnight.

Per session date D (NY clock, minutes from midnight, every fix built in its own time zone):
    L  = the 16:00 Europe/London fix in NY time     (11:00 ET most weeks, 12:00 ET when only
                                                      the US has switched to summer time)
    E  = the 14:15 Europe/Berlin ECB fix in NY time (08:15 ET most weeks, 09:15 ET likewise)
    S  = L + switch_offset                          (the switch time)
  pre  leg: SHORT, enters at E, exits at S
  post leg: LONG,  enters at S, exits at S + post_hold (or at the session's last bar for "eod")
  both    : the pre trade, then the post trade
(6E and 6J are quoted in USD per foreign unit, so short the future = long the USD.)

Execution (audited by src/experiments/fx_integrity.py):
  * entry at the OPEN of the first bar whose open time is >= the target, with market slippage;
    if that bar opens more than MAX_ENTRY_LAG_MIN after the target (a gap in the bars) or is not
    before the exit time, the trade is skipped. `signal_idx` = the entry bar (a clock rule, known
    in advance);
  * time exit at the CLOSE of the last bar whose open time is < the exit time (that bar closes at
    the exit time when there is no gap), with market slippage; when that bar is the session's
    last bar the exit is counted as `eod_exit`;
  * stop (optional): entry price before slippage x (1 -/+ stop%), live intrabar from the entry
    bar, filled at the worse of the bar's open and the stop, with stop slippage;
  * vol gate (known before the session opens): v_d = sqrt(sum of squared log returns of the last
    close in each 5-minute bucket of session d); g_d = mean(v over the 20 sessions before d);
    m_d = median(g over the 250 sessions up to d). high: g_d > m_d; low: g_d <= m_d; NaN -> no
    trade;
  * one position at a time, compounding equity, unlevered whole contracts (the other families'
    sizing); every fill pays adverse slippage + commission;
  * a position closed on the data's final bar by the session-close rule is flagged forced and is
    not a completed trade.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.fx_fix.config import (
    DAY_END_MIN,
    DAY_START_MIN,
    ECB_FIX,
    LEGS,
    LONDON_FIX,
    MAX_ENTRY_LAG_MIN,
    RV_LONG_DAYS,
    RV_SAMPLE_MIN,
    RV_SHORT_DAYS,
    VOL_GATES,
    post_hold_minutes,
)
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "forced_close"
NY = ZoneInfo("America/New_York")


def fx_day_bars(df_1min: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """The strategy's bars: clean 1-minute bars with NY open time in [08:00, 17:00), RTH flag
    ignored (the London-fix legs run past the 15:00 ET pit close). Single symbol."""
    if timeframe != "1min":
        raise ValueError(f"fx_fix runs on 1-minute bars only, got {timeframe!r}")
    if df_1min.is_empty():
        return df_1min
    ny = pl.col("bar_open_ts_ny")
    tod = ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)
    return (df_1min.filter((tod >= DAY_START_MIN) & (tod < DAY_END_MIN)
                           & (ny.dt.date() == pl.col("session_date_ny")))
            .sort("bar_open_ts"))


def fix_minutes(day: date, fix: tuple[str, int, int]) -> int:
    """The fix's local clock time on `day`, as NY minutes from midnight."""
    tz, h, m = fix
    t = datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(tz)).astimezone(NY)
    return t.hour * 60 + t.minute


class FXData(CBData):
    """CBData (session structure, tod, caching) plus fix times per session and the vol gate."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        days = [d.astype(object) for d in self.days]
        self.london_min = np.array([fix_minutes(d, LONDON_FIX) for d in days], dtype=np.int64)
        self.ecb_min = np.array([fix_minutes(d, ECB_FIX) for d in days], dtype=np.int64)
        # Monotonic (session, minute) key for vectorized "first bar at/after a time" lookups.
        self._key = self.sess * 1440 + self.tod

    def bar_at_or_after(self, minutes: np.ndarray) -> np.ndarray:
        """Per session: index of the first bar with open time >= minutes[s] (day_end + 1 if none)."""
        s = np.arange(len(self.days), dtype=np.int64)
        return np.searchsorted(self._key, s * 1440 + minutes, side="left")

    def session_vol(self) -> np.ndarray:
        """v_d per session: sqrt of the sum of squared log returns of 5-minute-bucket closes."""
        def calc():
            df = pl.DataFrame({"s": self.sess, "b": self.tod // RV_SAMPLE_MIN, "c": self.close})
            last = df.group_by(["s", "b"], maintain_order=True).agg(pl.col("c").last())
            r = last.with_columns(pl.col("c").log().diff().over("s").alias("r"))
            rv = r.group_by("s", maintain_order=True).agg((pl.col("r") ** 2).sum().alias("rv")).sort("s")
            out = np.full(len(self.days), np.nan)
            out[rv["s"].to_numpy()] = np.sqrt(rv["rv"].to_numpy())
            return out
        return self._get(("sess_vol",), calc)

    def vol_regime(self) -> tuple[np.ndarray, np.ndarray]:
        """(g, m) per session: trailing 20-session mean of v BEFORE the session, and the median
        of g over the last 250 sessions (this one included). Both known at the session's open."""
        def calc():
            v = pd.Series(self.session_vol())
            g = v.rolling(RV_SHORT_DAYS, min_periods=RV_SHORT_DAYS).mean().shift(1)
            m = g.rolling(RV_LONG_DAYS, min_periods=RV_LONG_DAYS).median()
            return g.to_numpy(), m.to_numpy()
        return self._get(("vol_regime",), calc)

    def gate_ok(self, vol_gate: str) -> np.ndarray:
        if vol_gate not in VOL_GATES:
            raise ValueError(f"Unknown vol_gate {vol_gate!r}")
        if vol_gate == "none":
            return np.ones(len(self.days), dtype=bool)
        g, m = self.vol_regime()
        with np.errstate(invalid="ignore"):
            return (g > m) if vol_gate == "high" else (g <= m)  # NaN -> False


@dataclass(frozen=True)
class FXParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    leg: str
    switch_offset: int
    post_hold: str
    vol_gate: str
    stop_pct: float | None   # None = no stop

    @classmethod
    def from_config(cls, cfg) -> "FXParams":
        return cls(cfg.symbol, cfg.timeframe, cfg.leg, int(cfg.switch_offset), cfg.post_hold, cfg.vol_gate,
                   cfg.stop_pct_value)

    @property
    def hold_minutes(self) -> int | None:
        return post_hold_minutes(self.post_hold)


def as_params(cfg) -> FXParams:
    return cfg if isinstance(cfg, FXParams) else FXParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is +1 (long) / -1 (short); `leg` is "pre" / "post"; quantities are always positive."""

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
    stop_level: np.ndarray    # nan = no stop
    entry_base: np.ndarray    # entry price before slippage
    side: np.ndarray
    leg: np.ndarray


def leg_windows(data: FXData, p: FXParams) -> list[dict[str, np.ndarray]]:
    """Per leg in this config: per session, the entry target, exit target (NY minutes; None-like
    -1 = the session's last bar) and side. Pre legs come before post legs within a day."""
    if p.leg not in LEGS:
        raise ValueError(f"Unknown leg {p.leg!r}")
    switch = data.london_min + p.switch_offset
    out = []
    if p.leg in ("pre", "both"):
        out.append({"leg": "pre", "side": -1, "start": data.ecb_min.copy(), "end": switch})
    if p.leg in ("post", "both"):
        H = p.hold_minutes
        end = np.full(len(switch), -1, dtype=np.int64) if H is None else switch + H
        out.append({"leg": "post", "side": 1, "start": switch, "end": end})
    return out


def planned_trades(data: FXData, p: FXParams) -> dict[str, np.ndarray]:
    """Every trade the rules call for, before stops and sizing, in time order:
    entry bar e, exit bar x (time / session-close exit), side, leg, and whether x is a time exit."""
    empty = {"e": np.array([], dtype=np.int64), "x": np.array([], dtype=np.int64),
             "side": np.array([], dtype=np.int64), "leg": np.array([], dtype=object),
             "timed": np.array([], dtype=bool)}
    if data.n == 0:
        return empty
    ok = data.gate_ok(p.vol_gate)
    ds, de = data.day_start_idx, data.day_end_idx
    rows = []
    for w in leg_windows(data, p):
        e = data.bar_at_or_after(w["start"])
        eod = w["end"] < 0
        xa = data.bar_at_or_after(np.where(eod, DAY_END_MIN, w["end"]))
        x = np.minimum(xa - 1, de)  # last bar opening before the exit time
        valid = ok & (e <= de)
        e_c = np.minimum(e, data.n - 1)
        valid &= data.tod[e_c] - w["start"] <= MAX_ENTRY_LAG_MIN
        valid &= (e <= x) & (x >= ds)
        timed = ~eod & (x < de)
        for s in np.flatnonzero(valid):
            rows.append((int(e[s]), int(x[s]), w["side"], w["leg"], bool(timed[s])))
    rows.sort()
    if not rows:
        return empty
    e, x, side, leg, timed = zip(*rows)
    return {"e": np.array(e, dtype=np.int64), "x": np.array(x, dtype=np.int64),
            "side": np.array(side, dtype=np.int64), "leg": np.array(leg, dtype=object),
            "timed": np.array(timed, dtype=bool)}


def simulate_fx_fix(
    data: FXData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many bars late (still
    before the exit bar, else skipped); `missed_entry_frac` drops that fraction of the trades."""
    p = as_params(cfg)
    plan = planned_trades(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    for e0, x, d, leg, timed in zip(plan["e"].tolist(), plan["x"].tolist(), plan["side"].tolist(),
                                    plan["leg"].tolist(), plan["timed"].tolist()):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = e0 + entry_delay_bars
        if e < free_from or e > x:
            continue
        base = o[e]
        fill_px = costs.fill(base, "buy" if d > 0 else "sell")
        stop = base * (1 - d * p.stop_pct / 100) if p.stop_pct is not None else float("nan")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side = "long" if d > 0 else "short"
        x_action = "sell" if d > 0 else "buy"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        has_stop = math.isfinite(stop)
        for j in range(e, x + 1):
            if has_stop and ((d > 0 and lo[j] <= stop) or (d < 0 and hi[j] >= stop)):
                px = min(o[j], stop) if d > 0 else max(o[j], stop)
                exit_px, why = costs.fill(px, x_action, stop=True), STOP_EXIT
                break
            if j == x:
                if timed:
                    why = TIME_EXIT
                else:
                    why = FORCED if j == n - 1 else EOD_EXIT
                exit_px = costs.fill(c[j], x_action)
                break
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[j], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[j])
        commissions = entry_fill.commission + exit_fill.commission
        realized = d * (exit_px - fill_px) * qty - commissions
        reason = {EOD_EXIT: ExitReason.SESSION_EXIT, STOP_EXIT: ExitReason.STOP_LOSS,
                  FORCED: ExitReason.SESSION_EXIT, TIME_EXIT: ExitReason.TIME_EXIT}[why]
        risk = abs(base - stop) if has_stop else float("nan")
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop, target_price=None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (risk * qty) if has_stop and risk > 0 else None,
            commission_total=commissions, holding_bars=j - e,
        ))
        rows.append((e0, e, j, e0, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, stop,
                     base, d, leg))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[j], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = j + 1

    cols = list(zip(*rows)) if rows else [()] * 15
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=f(cols[11]), entry_base=f(cols[12]),
        side=i64(cols[13]), leg=np.asarray(cols[14], dtype=object),
    )
