"""Compact 1-minute backtester for last-half-hour momentum (equity index futures, RTH only).

Bars: only 1-minute bars whose NY open time is in [09:30, 16:00) on their own session date are
used (`lh_day_bars`). Each NY date is one session; nothing is held overnight.

Per session s (all values use bars that open BEFORE the entry time, or earlier sessions):
    prev_close[s] = close of session s-1's last bar
    open[s]       = open of session s's first bar (if it opens by 09:35)
    dec(m)        = close of the last bar opening before minute m (if it opens at m-1-lag or later)
    signal        : prev_close -> dec(entry) / prev_close - 1
                    open       -> dec(entry) / open - 1
                    first_half -> dec(10:00) / prev_close - 1
    fh            = dec(10:00) / prev_close - 1  (the agreement check)
    sigma         = std of the signal over the previous 20 sessions (>= 15 defined)
    rv / rv_med   = std of the previous 20 daily RTH close-to-close returns / its median over the
                    previous 120 sessions (>= 60 defined)
    trade if the signal is defined and non-zero and the filter / agreement allow it;
    side = sign(signal)

Execution (audited by src/experiments/lh_integrity.py):
  * entry at the OPEN of the first bar whose open time is >= the entry time (within
    MAX_ENTRY_LAG_MIN), with market slippage; `signal_idx` = the decision bar (entry bar - 1);
  * stop (optional): entry price before slippage x (1 -/+ stop%) against the position, live
    intrabar from the entry bar, filled at the worse of the bar's open and the stop, with stop
    slippage;
  * time exit at the CLOSE of the last bar whose open time is < the exit time; when that bar is
    the session's last bar (exit 16:00, or an early close) the exit is `eod_exit`;
  * one position at a time, compounding equity, unlevered whole contracts; every fill pays
    adverse slippage + commission;
  * a position closed on the data's final bar is flagged forced and is not a completed trade.
`side_override` / `session_sides` (luck benchmark only) replace the direction / the whole signal.
"""

from __future__ import annotations

from dataclasses import dataclass, replace  # noqa: F401  (replace re-exported for perturbations)
from datetime import date

import numpy as np
import pandas as pd
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.last_half_hour.config import (
    DAY_END_MIN,
    DAY_START_MIN,
    FIRST_HALF_END_MIN,
    LATE_MIN,
    MAX_ENTRY_LAG_MIN,
    MAX_OPEN_LAG_MIN,
    RV_LOOKBACK,
    RV_MEDIAN_LOOKBACK,
    RV_MEDIAN_MIN_PERIODS,
    SIGNALS,
    VOLUME_LOOKBACK_SESSIONS,
    VOLUME_MIN_SESSIONS,
    Z_LOOKBACK,
    Z_MIN_PERIODS,
    parse_filter,
    window_minutes,
)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "forced_close"


def lh_day_bars(df_1min: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """The strategy's bars: clean 1-minute bars with NY open time in [09:30, 16:00) on their own
    session date. Single symbol."""
    if timeframe != "1min":
        raise ValueError(f"last_half_hour runs on 1-minute bars only, got {timeframe!r}")
    if df_1min.is_empty():
        return df_1min
    ny = pl.col("bar_open_ts_ny")
    tod = ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)
    return (df_1min.filter((tod >= DAY_START_MIN) & (tod < DAY_END_MIN)
                           & (ny.dt.date() == pl.col("session_date_ny")))
            .sort("bar_open_ts"))


def rolling_prev_std(x: np.ndarray, n: int, min_periods: int) -> np.ndarray:
    """Std (ddof=1) of x over the previous n entries (excluding the current), NaN-aware."""
    return pd.Series(x).shift(1).rolling(n, min_periods=min_periods).std().to_numpy()


class LHData(CBData):
    """CBData (session structure, tod, caching) plus the per-session closes, opens and signals."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        self.volume = (bars.sort("bar_open_ts")["volume"].to_numpy().astype(float) if "volume" in bars.columns
                       else np.zeros(self.n))
        self.day_list: list[date] = [d.astype(object) for d in self.days]
        S = len(self.days)
        self._key = self.sess * 1440 + self.tod
        self.last_close = self.close[self.day_end_idx] if S else np.array([])
        self.prev_close = np.concatenate([[np.nan], self.last_close[:-1]]) if S else np.array([])
        if S:
            st = self.day_start_idx
            self.day_open = np.where(self.tod[st] - DAY_START_MIN <= MAX_OPEN_LAG_MIN, self.open[st], np.nan)
        else:
            self.day_open = np.array([])

    def bar_at_or_after(self, minutes) -> np.ndarray:
        """Per session: index of the first bar with open time >= minutes (day_end + 1 if none)."""
        s = np.arange(len(self.days), dtype=np.int64)
        return np.searchsorted(self._key, s * 1440 + np.asarray(minutes, dtype=np.int64), side="left")

    def decision_bar(self, m: int) -> np.ndarray:
        """Per session: the last bar opening before minute m, or -1 if none recent enough."""
        def f():
            d = self.bar_at_or_after(m) - 1
            ok = (d >= self.day_start_idx) & (d <= self.day_end_idx)
            dc = np.clip(d, 0, max(self.n - 1, 0))
            ok &= self.tod[dc] >= m - 1 - MAX_ENTRY_LAG_MIN
            return np.where(ok, d, -1)
        return self._get(("dec", m), f)

    def dec_close(self, m: int) -> np.ndarray:
        d = self.decision_bar(m)
        return np.where(d >= 0, self.close[np.clip(d, 0, max(self.n - 1, 0))], np.nan)

    def first_half(self) -> np.ndarray:
        return self._get(("fh",), lambda: self.dec_close(FIRST_HALF_END_MIN) / self.prev_close - 1)

    def signal(self, name: str, entry_min: int) -> np.ndarray:
        if name not in SIGNALS:
            raise ValueError(f"Unknown signal {name!r}")

        def f():
            if name == "first_half":
                return self.first_half()
            base = self.prev_close if name == "prev_close" else self.day_open
            return self.dec_close(entry_min) / base - 1
        return self._get(("sig", name, entry_min), f)

    def sigma(self, name: str, entry_min: int) -> np.ndarray:
        return self._get(("sigma", name, entry_min),
                         lambda: rolling_prev_std(self.signal(name, entry_min), Z_LOOKBACK, Z_MIN_PERIODS))

    def late_ret(self, entry_min: int) -> np.ndarray:
        """Return over the LATE_MIN minutes before the entry: decision close / close LATE_MIN earlier - 1."""
        return self._get(("late", entry_min),
                         lambda: self.dec_close(entry_min) / self.dec_close(entry_min - LATE_MIN) - 1)

    def vnorm(self) -> np.ndarray:
        """Mean volume at each bar's minute of day over the prior VOLUME_LOOKBACK_SESSIONS sessions."""
        def calc():
            df = pl.DataFrame({"tod": self.tod, "v": self.volume})
            out = df.select(pl.col("v").shift(1).rolling_mean(VOLUME_LOOKBACK_SESSIONS,
                                                               min_samples=VOLUME_MIN_SESSIONS).over("tod"))
            return out["v"].fill_null(np.nan).to_numpy().astype(float)
        return self._get(("vnorm",), calc)

    def late_volume_ratio(self, entry_min: int) -> np.ndarray:
        """Per session: volume of the bars opening in [entry-LATE_MIN, entry) / the sum of their
        time-of-day norms (NaN if a norm is missing or there are no bars)."""
        def calc():
            a = self.bar_at_or_after(entry_min - LATE_MIN)
            b = self.bar_at_or_after(entry_min)
            vn = self.vnorm()
            cv = np.concatenate([[0.0], np.cumsum(self.volume)])
            cn = np.concatenate([[0.0], np.cumsum(np.nan_to_num(vn))])
            cbad = np.concatenate([[0], np.cumsum(~np.isfinite(vn))])
            V, N, bad = cv[b] - cv[a], cn[b] - cn[a], cbad[b] - cbad[a]
            with np.errstate(invalid="ignore", divide="ignore"):
                return np.where((bad == 0) & (N > 0) & (b > a), V / N, np.nan)
        return self._get(("lvr", entry_min), calc)

    def rv_high(self) -> np.ndarray:
        def f():
            ret = self.last_close / self.prev_close - 1
            rv = rolling_prev_std(ret, RV_LOOKBACK, RV_LOOKBACK)
            med = pd.Series(rv).shift(1).rolling(RV_MEDIAN_LOOKBACK, min_periods=RV_MEDIAN_MIN_PERIODS).median().to_numpy()
            return np.isfinite(rv) & np.isfinite(med) & (rv > med)
        return self._get(("rv_high",), f)


@dataclass(frozen=True)
class LHParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    signal: str
    agree: bool
    entry_min: int          # NY minutes from midnight
    exit_min: int           # NY minutes; 16:00 = the session's last bar
    filter: str             # "none" / "z" / "rv_high" / "down_only"
    z: float | None = None  # z filter threshold
    stop_pct: float | None = None
    fh_rel: str = "any"     # v2: first-half-hour move vs the day's move: any / same / opp
    late_rel: str = "any"   # v2: move over the LATE_MIN minutes before entry vs the day's move
    vol_gate: float | None = None   # v2: late volume / norm >= gate
    direction: str = "follow"       # v2: follow / fade the day's move

    @classmethod
    def from_config(cls, cfg) -> "LHParams":
        e, x = window_minutes(cfg.window)
        kind, z = parse_filter(cfg.filter)
        return cls(cfg.symbol, cfg.timeframe, cfg.signal, getattr(cfg, "agree", "off") == "on", e, x, kind, z,
                   cfg.stop_pct_value, getattr(cfg, "fh_rel", "any"), getattr(cfg, "late_rel", "any"),
                   getattr(cfg, "vol_gate_value", None), getattr(cfg, "direction", "follow"))


def as_params(cfg) -> LHParams:
    return cfg if isinstance(cfg, LHParams) else LHParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

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
    side: np.ndarray          # +1 long / -1 short
    stop_level: np.ndarray    # nan = no stop


def session_side(data: LHData, p: LHParams) -> np.ndarray:
    """Per session: +1 / -1 if the rules call for a trade, else 0 (clock checks are separate)."""
    if p.filter not in ("none", "z", "rv_high", "down_only"):
        raise ValueError(f"Unknown filter {p.filter!r}")
    if p.signal == "first_half" and p.agree:
        raise ValueError("agree is redundant with the first_half signal")
    r = data.signal(p.signal, p.entry_min)
    ok = np.isfinite(r) & (r != 0)
    if p.agree:
        fh = data.first_half()
        ok &= np.isfinite(fh) & (np.sign(fh) == np.sign(r))
    if p.fh_rel != "any":
        fh = data.first_half()
        want = np.sign(r) if p.fh_rel == "same" else -np.sign(r)
        ok &= np.isfinite(fh) & (np.sign(fh) == want)
    if p.late_rel != "any":
        lr = data.late_ret(p.entry_min)
        want = np.sign(r) if p.late_rel == "same" else -np.sign(r)
        ok &= np.isfinite(lr) & (np.sign(lr) == want)
    if p.vol_gate is not None:
        vr = data.late_volume_ratio(p.entry_min)
        with np.errstate(invalid="ignore"):
            ok &= np.isfinite(vr) & (vr >= p.vol_gate)
    if p.filter == "z":
        sg = data.sigma(p.signal, p.entry_min)
        with np.errstate(invalid="ignore"):
            ok &= np.isfinite(sg) & (sg > 0) & (np.abs(r) > p.z * sg)
    elif p.filter == "rv_high":
        ok &= data.rv_high()
    elif p.filter == "down_only":
        ok &= r < 0
    flip = -1 if p.direction == "fade" else 1
    return np.where(ok, flip * np.sign(np.nan_to_num(r)), 0).astype(np.int64)


def planned_trades(data: LHData, p: LHParams, session_sides: np.ndarray | None = None) -> dict[str, np.ndarray]:
    """Every trade the rules call for, before sizing, in time order: decision bar d, entry bar e,
    exit bar x, side, and whether x is a time exit (else the session's last bar).
    `session_sides` (luck benchmark only) replaces the signal: +1 / -1 / 0 per session."""
    empty = {k: np.array([], dtype=np.int64) for k in ("d", "e", "x", "side")}
    empty["timed"] = np.array([], dtype=bool)
    if data.n == 0:
        return empty
    if not p.exit_min > p.entry_min:
        raise ValueError(f"exit {p.exit_min} must be after entry {p.entry_min}")
    side = session_side(data, p) if session_sides is None else np.asarray(session_sides, dtype=np.int64)
    ds, de = data.day_start_idx, data.day_end_idx
    d = data.decision_bar(p.entry_min)
    e = data.bar_at_or_after(p.entry_min)
    x = np.minimum(data.bar_at_or_after(min(p.exit_min, DAY_END_MIN)) - 1, de)
    e_c = np.minimum(e, data.n - 1)
    valid = (side != 0) & (d >= 0) & (e <= de) & (e == d + 1)
    valid &= data.tod[e_c] - p.entry_min <= MAX_ENTRY_LAG_MIN
    valid &= (e <= x) & (x >= ds)
    s = np.flatnonzero(valid)
    return {"d": d[s].astype(np.int64), "e": e[s].astype(np.int64), "x": x[s].astype(np.int64),
            "side": side[s], "timed": (x < de)[s]}


def simulate_last_half_hour(
    data: LHData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
    side_override: np.ndarray | None = None,
    session_sides: np.ndarray | None = None,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many bars late (still
    not after the exit bar, else skipped); `missed_entry_frac` drops that fraction of the trades.
    `side_override` (one +1/-1 per planned trade) replaces the direction; `session_sides` (one
    +1/-1/0 per session) replaces the signal and filters altogether (luck benchmark)."""
    p = as_params(cfg)
    plan = planned_trades(data, p, session_sides)
    if side_override is not None:
        if len(side_override) != len(plan["e"]):
            raise ValueError("side_override needs one entry per planned trade")
        plan["side"] = np.asarray(side_override, dtype=np.int64)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    for d, e0, x, sd, timed in zip(plan["d"].tolist(), plan["e"].tolist(), plan["x"].tolist(),
                                   plan["side"].tolist(), plan["timed"].tolist()):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = e0 + entry_delay_bars
        if e < free_from or e > x:
            continue
        long = sd > 0
        base = o[e]
        fill_px = costs.fill(base, "buy" if long else "sell")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side_s = "long" if long else "short"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        has_stop = p.stop_pct is not None
        stop = (base * (1 - sd * p.stop_pct / 100)) if has_stop else float("nan")
        j = x
        if has_stop:
            hit = np.flatnonzero(lo[e:x + 1] <= stop) if long else np.flatnonzero(hi[e:x + 1] >= stop)
            j = e + int(hit[0]) if len(hit) else x
        stopped = has_stop and (lo[j] <= stop if long else hi[j] >= stop)
        if stopped:
            why = STOP_EXIT
            exit_px = costs.fill(min(o[j], stop) if long else max(o[j], stop), "sell" if long else "buy", stop=True)
        else:
            why = TIME_EXIT if timed else (FORCED if x == n - 1 else EOD_EXIT)
            exit_px = costs.fill(c[x], "sell" if long else "buy")
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[j], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[j])
        commissions = entry_fill.commission + exit_fill.commission
        realized = sd * (exit_px - fill_px) * qty - commissions
        reason = {EOD_EXIT: ExitReason.SESSION_EXIT, FORCED: ExitReason.SESSION_EXIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, STOP_EXIT: ExitReason.STOP_LOSS}[why]
        risk = abs(base - stop) if has_stop else float("nan")
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side_s, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop, target_price=None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (risk * qty) if has_stop and risk > 0 else None,
            commission_total=commissions, holding_bars=j - e,
        ))
        rows.append((d, e, j, d, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, base, sd, stop))
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
