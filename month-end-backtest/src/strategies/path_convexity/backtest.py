"""Compact bar-based backtester for the intraday price-path convexity fade (5min/15min bars).

Signal at bar k, from the closes of bars k-N+1 .. k only (N = lookback; indicators run over the
RTH bar series across sessions, like ATR in the other families). With P1 = close[k-N+1],
PN = close[k], mid = (P1 + PN) / 2, line_i = P1 + (PN - P1) * i / (N - 1) and A = ATR(14)[k]:
    paper    : (mid - mean(P)) / mid                (Gulen & Woeppel's convexity)
    atr      : (mid - mean(P)) / A                  (the same average line-minus-path gap, in ATR)
    maxgap   : g_j / A, j = argmax_i |line_i - P_i| (the largest single gap, signed; first on ties)
    reversal : (PN - P1) / A                        (CONTROL: the plain N-bar return)
z_k = (S_k - mean(S over bars k-Z+1..k)) / sd(same, population), Z = z_lookback.

Decisions (bar k close):
  * short when z_k >= entry_z and NOT z_{k-1} >= entry_z (a fresh cross into the extreme);
    long when z_k <= -entry_z and NOT z_{k-1} <= -entry_z. A HIGH signal always fades to SHORT;
  * quadrant: m = PN - P1. late = trade only against the window's net move (side = -sign(m));
    early = only with it (side = sign(m)); all = either (m = 0 counts only under all);
  * min_move_atr: |m| >= min_move_atr x A;
  * direction long / short / both; trend_filter emaN: long only if close_k > EMA(N)_k, short
    only if below (NaN EMA -> no trade);
  * no decision on the session's last bar or less than `last_entry_cutoff` minutes before the
    session's last close; a signal while a position is open is dropped (never queued).

Execution (audited by src/experiments/pc_integrity.py):
  * fill at the NEXT bar's open (bar k+1+delay) with market slippage; the fill bar must be in
    the decision's session, else the signal is skipped;
  * stop (optional): base -/+ stop_atr x ATR(14) of bar e-1 (known before the fill), base = the
    open before slippage. Live intrabar from the entry bar; fills at the worse of the bar's
    open and the stop, with stop slippage;
  * time exit: hold H bars (half = ceil(N/2), full = N) -> closed at the CLOSE of bar e+H-1 with
    market slippage, unless the stop hit first; hold = session (or a time exit at/after the
    session's last bar) -> closed at the session's last close. Nothing is held overnight;
  * one position at a time, compounding equity, unlevered whole contracts (the mean-reversion
    funnel's sizing); every fill pays adverse slippage + commission;
  * a position closed on the data's final bar by the session-close rule is flagged forced and
    is not a completed trade.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.path_convexity.config import (
    ATR_PERIOD,
    LAST_ENTRY_CUTOFF_MINUTES,
    QUADRANTS,
    SIGNAL_FORMS,
    hold_bars,
    trend_ema_span,
)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "forced_close"
_CHUNK = 20_000  # rows of the max-gap sliding window per block (bounds memory)


def max_gap(close: np.ndarray, n: int) -> np.ndarray:
    """Signed line-minus-path gap of largest magnitude over each N-bar window ending at k
    (NaN for k < N-1). First index on ties."""
    out = np.full(len(close), np.nan)
    if len(close) < n or n < 2:
        return out
    W = sliding_window_view(close, n)
    frac = np.arange(n) / (n - 1)
    for a in range(0, len(W), _CHUNK):
        w = W[a:a + _CHUNK]
        g = w[:, :1] + (w[:, -1:] - w[:, :1]) * frac - w
        j = np.abs(g).argmax(axis=1)
        out[n - 1 + a: n - 1 + a + len(w)] = g[np.arange(len(w)), j]
    return out


class PCData(CBData):
    """CBData (session structure, ATR, EMA, caching) plus the convexity signals."""

    def net_move(self, n: int) -> np.ndarray:
        def calc():
            m = np.full(self.n, np.nan)
            if self.n >= n:
                m[n - 1:] = self.close[n - 1:] - self.close[:self.n - n + 1]
            return m
        return self._get(("move", n), calc)

    def signal(self, form: str, n: int) -> np.ndarray:
        if form not in SIGNAL_FORMS:
            raise ValueError(f"Unknown signal_form {form!r}")
        if n < 2:
            raise ValueError(f"lookback must be >= 2, got {n}")

        def calc():
            c, a = self.close, self.atr(ATR_PERIOD)
            with np.errstate(invalid="ignore", divide="ignore"):
                if form == "reversal":
                    return self.net_move(n) / a
                if form == "maxgap":
                    return max_gap(c, n) / a
                first = np.full(self.n, np.nan)
                if self.n >= n:
                    first[n - 1:] = c[:self.n - n + 1]
                mid = (first + c) / 2
                mean = pd.Series(c).rolling(n, min_periods=n).mean().to_numpy()
                gap = mid - mean
                if form == "atr":
                    return gap / a
                return np.where(np.abs(mid) > 1e-9, gap / mid, np.nan)
        return self._get(("sig", form, n), calc)

    def zscore(self, form: str, n: int, z_lookback: int) -> np.ndarray:
        def calc():
            s = pd.Series(self.signal(form, n))
            r = s.rolling(z_lookback, min_periods=z_lookback)
            sd = r.std(ddof=0).to_numpy()
            with np.errstate(invalid="ignore", divide="ignore"):
                return np.where(sd > 0, (s.to_numpy() - r.mean().to_numpy()) / sd, np.nan)
        return self._get(("z", form, n, z_lookback), calc)


@dataclass(frozen=True)
class PCParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    lookback: int
    signal_form: str
    z_lookback: int
    entry_z: float
    quadrant: str
    min_move_atr: float
    direction: str
    hold: str
    stop_atr: float | None   # None = no stop
    trend_filter: str
    last_entry_cutoff: int = LAST_ENTRY_CUTOFF_MINUTES

    @classmethod
    def from_config(cls, cfg) -> "PCParams":
        return cls(cfg.symbol, cfg.timeframe, int(cfg.lookback), cfg.signal_form, int(cfg.z_lookback),
                   float(cfg.entry_z), cfg.quadrant, float(cfg.min_move_atr), cfg.direction, cfg.hold,
                   cfg.stop_atr_value, cfg.trend_filter)

    @property
    def hold_bars(self) -> int | None:
        return hold_bars(self.hold, self.lookback)


def as_params(cfg) -> PCParams:
    return cfg if isinstance(cfg, PCParams) else PCParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is +1 (long) / -1 (short); quantities are always positive."""

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


def signals(data: PCData, p: PCParams) -> dict[str, np.ndarray]:
    """Every decision bar: k, side (+1 / -1). Filters are already applied (a fresh cross only
    counts on the bar it happens; positions are handled by the simulator)."""
    if p.quadrant not in QUADRANTS:
        raise ValueError(f"Unknown quadrant {p.quadrant!r}")
    if p.direction not in ("long", "short", "both"):
        raise ValueError(f"Unknown direction {p.direction!r}")
    span = trend_ema_span(p.trend_filter)
    z = data.zscore(p.signal_form, p.lookback, p.z_lookback)
    zp = np.concatenate([[np.nan], z[:-1]])
    with np.errstate(invalid="ignore"):
        short = (z >= p.entry_z) & ~(zp >= p.entry_z)
        long_ = (z <= -p.entry_z) & ~(zp <= -p.entry_z)
    side = np.where(short, -1, np.where(long_, 1, 0)).astype(np.int64)
    ok = side != 0
    if p.direction == "long":
        ok &= side > 0
    elif p.direction == "short":
        ok &= side < 0
    m = data.net_move(p.lookback)
    sm = np.sign(np.nan_to_num(m))
    if p.quadrant == "late":
        ok &= side == -sm
    elif p.quadrant == "early":
        ok &= side == sm
    if p.min_move_atr > 0:
        with np.errstate(invalid="ignore"):
            ok &= np.abs(m) >= p.min_move_atr * data.atr(ATR_PERIOD)  # NaN -> False
    if span is not None:
        ema = data.ema(span)
        with np.errstate(invalid="ignore"):
            ok &= np.where(side > 0, data.close > ema, data.close < ema)
    to_close = data.tod[data.sess_end] - data.tod
    ok &= ~data.is_last & (to_close >= p.last_entry_cutoff)
    ks = np.flatnonzero(ok)
    return {"k": ks, "side": side[ks]}


def simulate_path_convexity(
    data: PCData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many extra bars late
    (still within the session, else skipped); `missed_entry_frac` drops that fraction of the
    signals that would have been traded."""
    p = as_params(cfg)
    st = signals(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    atr = data.atr(ATR_PERIOD)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    H = p.hold_bars

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    for k, d in zip(st["k"].tolist(), st["side"].tolist()):
        if k < free_from:
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = k + 1 + entry_delay_bars
        if e >= n or e > data.sess_end[k]:
            continue
        base = o[e]
        fill_px = costs.fill(base, "buy" if d > 0 else "sell")
        if p.stop_atr is not None:
            a = atr[e - 1]
            if not math.isfinite(a) or a <= 0:
                continue
            stop = base - d * p.stop_atr * a
        else:
            stop = float("nan")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        L = int(data.sess_end[e])
        T = e + H - 1 if H is not None else n
        side = "long" if d > 0 else "short"
        x_action = "sell" if d > 0 else "buy"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        has_stop = math.isfinite(stop)
        for j in range(e, L + 1):
            if has_stop and ((d > 0 and lo[j] <= stop) or (d < 0 and hi[j] >= stop)):
                px = min(o[j], stop) if d > 0 else max(o[j], stop)
                exit_px, why = costs.fill(px, x_action, stop=True), STOP_EXIT
                break
            if j == L:
                exit_px, why = costs.fill(c[j], x_action), (FORCED if j == n - 1 else EOD_EXIT)
                break
            if j == T:
                exit_px, why = costs.fill(c[j], x_action), TIME_EXIT
                break
        x = j
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[x], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[x])
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
            commission_total=commissions, holding_bars=x - e,
        ))
        rows.append((k, e, x, x, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, stop, base, d))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[x], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = x  # a decision at the exit bar's close may enter on the next bar

    cols = list(zip(*rows)) if rows else [()] * 14
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=f(cols[11]), entry_base=f(cols[12]),
        side=i64(cols[13]),
    )
