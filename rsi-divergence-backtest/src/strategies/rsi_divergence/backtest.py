"""Compact bar-based backtester for the RSI-divergence family (5min/15min/1h bars).

Signal (regular bullish divergence, the TradingView built-in "RSI Divergence"
convention), decided at bar c's close from data through bar c only:
    RSI      = Wilder RSI(rsi_lookback) of closes (seeded with the simple average
               of the first `rsi_lookback` gains/losses, then smoothed recursively)
    pivot low at bar p: RSI_p < every RSI of the `pivot_left` bars before p and
               RSI_p <= every RSI of the `pivot_right` bars after p; it is only
               KNOWN at the close of bar c = p + pivot_right (the confirmation bar)
    divergence: for consecutive RSI pivot lows q < p,
               p - q <= max_pivot_gap,
               RSI_p - RSI_q > 0 and >= min_rsi_diff   (RSI higher low)
               low_p < low_q                            (price lower low, at the pivot bars)
    long entry signal at the confirmation bar c.
All lookbacks are in bars and run continuously across sessions (RTH bars only).

Execution assumptions (audited by src/experiments/rsi_integrity.py):
  * long-only, one position at a time, compounding equity, no leverage;
  * the entry is a market order filled at the NEXT bar's open (bar c+1+delay),
    adverse slippage + commission on every fill. A signal on a session's last
    bar fills at the next session's open; positions may be held overnight (as in
    the mean-reversion and channel families);
  * 1R = stop_atr x ATR(14), using the last ATR known BEFORE the entry fill
    (ATR at bar c); stop = entry open - 1R, target = entry open + target_r x R,
    both measured from the raw entry-bar open and live from the entry bar;
  * a bar whose low touches the stop exits at the worse of its open and the stop
    (stop slippage); a bar whose high touches the target exits AT the target
    (limit slippage; a gap above the target is NOT credited). If one bar touches
    both, the stop is assumed to have filled first (conservative);
  * otherwise, once the position has been held `max_hold` bars (decided at bar
    j's close with j - entry + 1 >= max_hold), it exits at the next bar's open,
    so a time exit fills exactly `max_hold` bars after the entry fill;
  * sizing: each entry buys as many whole shares as current equity affords
    (identical to the mean-reversion funnel, so results are comparable);
  * signals confirmed while a position is open are ignored; a new signal may
    form at or after the exit bar (its entry then fills strictly after the exit);
  * a position still open when the data ends is force-closed at the last close
    and flagged (not counted as a completed trade).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.engine.fills import _apply_slippage, _commission
from src.features.atr import wilder_atr
from src.utils.config_models import ExecutionConfig

STOP_EXIT, TARGET_EXIT, TIME_EXIT, FORCED = "stop_exit", "target_exit", "time_exit", "forced_close"
ATR_PERIOD = 14


def wilder_rsi(close: np.ndarray, period: int) -> np.ndarray:
    """Causal Wilder RSI; NaN until `period` price changes have accumulated
    (first defined at index `period`). RSI_t uses closes up to and including t."""
    n = len(close)
    out = np.full(n, np.nan)
    if n <= period:
        return out
    d = np.diff(close)
    gain, loss = np.maximum(d, 0.0), np.maximum(-d, 0.0)
    ag, al = gain[:period].mean(), loss[:period].mean()

    def rsi(g: float, l: float) -> float:
        if l == 0.0:
            return 50.0 if g == 0.0 else 100.0
        return 100.0 - 100.0 / (1.0 + g / l)

    out[period] = rsi(ag, al)
    for t in range(period, n - 1):  # d[t] is close[t+1] - close[t]
        ag += (gain[t] - ag) / period
        al += (loss[t] - al) / period
        out[t + 1] = rsi(ag, al)
    return out


def pivot_lows(x: np.ndarray, left: int, right: int) -> np.ndarray:
    """Indices p with x_p < min(x[p-left:p]) and x_p <= min(x[p+1:p+right+1]),
    all values finite. Pivot p is only known at the close of bar p + right."""
    n = len(x)
    if n < left + right + 1:
        return np.array([], dtype=np.int64)
    p = np.arange(left, n - right)
    lmin = sliding_window_view(x, left).min(axis=1)[p - left]       # x[p-left .. p-1]
    rmin = sliding_window_view(x, right).min(axis=1)[p + 1]         # x[p+1 .. p+right]
    with np.errstate(invalid="ignore"):
        ok = (x[p] < lmin) & (x[p] <= rmin)  # any NaN in the window -> False
    return p[ok]


class RSIData:
    """Per-(symbol, timeframe) arrays. RSI series, pivots and divergence signals
    are cached by their parameters so the thousands of configs sharing them don't
    recompute. Exposes the same attributes as the other families' data objects
    (ts, open..close, session_date, day_end_idx, days), which is all the daily
    mark-to-market code needs."""

    def __init__(self, bars: pl.DataFrame) -> None:
        df = bars.sort("bar_open_ts")
        self.ts = df["bar_open_ts"].to_list()
        self.open = df["open"].to_numpy().astype(float)
        self.high = df["high"].to_numpy().astype(float)
        self.low = df["low"].to_numpy().astype(float)
        self.close = df["close"].to_numpy().astype(float)
        self.n = df.height
        if "session_date_ny" in df.columns:
            sd = df["session_date_ny"]
        else:
            sd = df["bar_open_ts"].dt.convert_time_zone("America/New_York").dt.date()
        self.session_date = sd.to_numpy().astype("datetime64[D]")
        if self.n:
            change = np.flatnonzero(self.session_date[1:] != self.session_date[:-1])
            self.day_end_idx = np.append(change, self.n - 1)
        else:
            self.day_end_idx = np.array([], dtype=int)
        self.days = self.session_date[self.day_end_idx]
        self._df = df
        self._cache: dict[tuple, object] = {}

    def _get(self, key: tuple, fn):
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    def rsi(self, period: int) -> np.ndarray:
        return self._get(("rsi", period), lambda: wilder_rsi(self.close, period))

    def pivots(self, period: int, left: int, right: int) -> np.ndarray:
        return self._get(("piv", period, left, right), lambda: pivot_lows(self.rsi(period), left, right))

    def divergences(self, period: int, left: int, right: int, max_gap: int,
                    min_diff: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(signal bar c, pivot p, previous pivot q) for every bullish divergence, sorted by c."""
        def calc():
            pv = self.pivots(period, left, right)
            if len(pv) < 2:
                e = np.array([], dtype=np.int64)
                return e, e, e
            q, p = pv[:-1], pv[1:]
            r = self.rsi(period)
            dr = r[p] - r[q]
            ok = (p - q <= max_gap) & (dr > 0) & (dr >= min_diff) & (self.low[p] < self.low[q])
            return p[ok] + right, p[ok], q[ok]
        return self._get(("div", period, left, right, max_gap, float(min_diff)), calc)

    @property
    def atr(self) -> np.ndarray:
        return self._get(("atr",), lambda: wilder_atr(self._df, period=ATR_PERIOD)["atr"]
                         .to_numpy().astype(float))


@dataclass(frozen=True)
class RSIParams:
    """Free-valued strategy parameters (RSIDivergenceConfig restricts values to the
    grid lattice). Used for off-grid perturbations; the backtester accepts either."""

    symbol: str
    timeframe: str
    rsi_lookback: int
    pivot_left: int
    pivot_right: int
    max_pivot_gap: int
    min_rsi_diff: float
    stop_atr: float
    target_r: float
    max_hold: int

    @classmethod
    def from_config(cls, cfg) -> "RSIParams":
        return cls(cfg.symbol, cfg.timeframe, cfg.rsi_lookback, cfg.pivot_left, cfg.pivot_right,
                   cfg.max_pivot_gap, float(cfg.min_rsi_diff), float(cfg.stop_atr), float(cfg.target_r),
                   cfg.max_hold)


def as_params(cfg) -> RSIParams:
    return cfg if isinstance(cfg, RSIParams) else RSIParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray     # confirmation bar c
    pivot_idx: np.ndarray      # second RSI pivot low p (c = p + pivot_right)
    prev_pivot_idx: np.ndarray # first RSI pivot low q
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray   # bar that triggered the exit (stop/target: that bar; time: the close before the fill; -1 forced)
    quantity: np.ndarray
    entry_px: np.ndarray       # entry fill price (after slippage)
    exit_px: np.ndarray        # exit fill price (after slippage)
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray    # STOP_EXIT / TARGET_EXIT / TIME_EXIT / FORCED
    stop_level: np.ndarray
    target_level: np.ndarray
    atr_used: np.ndarray       # ATR that set 1R


def scale_variable_costs(exec_config: ExecutionConfig, multiplier: float) -> ExecutionConfig:
    """Scale the VARIABLE execution costs (per-share commission, slippage bps) by
    `multiplier`, always from the given baseline so stress scenarios never
    compound. The per-order commission minimum is fixed and left unchanged."""
    return exec_config.model_copy(update={
        "commission_per_share": exec_config.commission_per_share * multiplier,
        "slippage_bps_market": exec_config.slippage_bps_market * multiplier,
        "slippage_bps_stop": exec_config.slippage_bps_stop * multiplier,
        "slippage_bps_limit_adverse": exec_config.slippage_bps_limit_adverse * multiplier,
    })


def signal_arrays(data: RSIData, cfg) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cfg = as_params(cfg)
    return data.divergences(cfg.rsi_lookback, cfg.pivot_left, cfg.pivot_right, cfg.max_pivot_gap,
                            cfg.min_rsi_diff)


def _whole_shares(equity: float, px: float, ec: ExecutionConfig) -> int:
    """Most whole shares whose cost plus commission fits in `equity` (no leverage)."""
    if not (px > 0 and math.isfinite(px)):
        return 0
    q = math.floor(equity / px)
    while q > 0 and q * px + _commission(q, ec) > equity:
        q -= 1
    return q


def simulate_rsi_divergence(
    data: RSIData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off, i.e. the baseline run):
    `entry_delay_bars` fills the entry that many extra bars late (1R still uses
    the ATR known before the fill); `missed_entry_frac` randomly drops that
    fraction of signals (each divergence is a single-bar event, so a dropped
    signal is never re-taken a bar later). Seeded by `stress_seed`. Cost stress is
    passed via `exec_config` (see `scale_variable_costs`)."""
    cfg = as_params(cfg)
    sig_c, sig_p, sig_q = signal_arrays(data, cfg)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    ec = exec_config
    atr = data.atr
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    H = cfg.max_hold

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    next_ok = 0  # earliest bar a signal may be confirmed on (no position open)

    for s in range(len(sig_c)):
        ci = int(sig_c[s])
        if ci < next_ok:
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        entry_idx = ci + 1 + entry_delay_bars
        if entry_idx >= n:
            break
        a_known = atr[entry_idx - 1]
        if not math.isfinite(a_known) or a_known <= 0:
            continue  # ATR warm-up: no usable 1R -> skip this signal
        entry_px_raw = o[entry_idx]
        risk = cfg.stop_atr * a_known
        stop = entry_px_raw - risk
        target = entry_px_raw + cfg.target_r * risk
        entry_fill_px = _apply_slippage(entry_px_raw, side="long", action="buy", bps=ec.slippage_bps_market,
                                        extended_hours=False, config=ec)
        qty = _whole_shares(equity, entry_fill_px, ec)
        if qty <= 0:
            continue
        seq += 1
        entry_fill = Fill(
            order_id=f"e{seq}", symbol=cfg.symbol, side="long", quantity=qty, fill_price=entry_fill_px,
            fill_ts=ts[entry_idx], commission=_commission(qty, ec),
            slippage_points=abs(entry_fill_px - entry_px_raw), bar_open_ts=ts[entry_idx],
        )

        end = min(entry_idx + H, n - 1)  # bars j in [entry_idx, end) can stop/target out
        hit = np.flatnonzero((lo[entry_idx:end] <= stop) | (hi[entry_idx:end] >= target))
        if len(hit):
            j = entry_idx + int(hit[0])
            if lo[j] <= stop:  # stop first if both touched in one bar
                why = STOP_EXIT
                exit_px = _apply_slippage(min(o[j], stop), side="long", action="sell", bps=ec.slippage_bps_stop,
                                          extended_hours=False, config=ec)
            else:
                why = TARGET_EXIT
                exit_px = _apply_slippage(target, side="long", action="sell", bps=ec.slippage_bps_limit_adverse,
                                          extended_hours=False, config=ec)
            decision, exit_idx = j, j
        elif entry_idx + H <= n - 1:
            why, decision = TIME_EXIT, entry_idx + H - 1
            exit_idx = decision + 1
            exit_px = _apply_slippage(o[exit_idx], side="long", action="sell", bps=ec.slippage_bps_market,
                                      extended_hours=False, config=ec)
        else:  # data ended with the position open -> forced close at the last close
            why, decision, exit_idx = FORCED, -1, n - 1
            exit_px = _apply_slippage(c[exit_idx], side="long", action="sell", bps=ec.slippage_bps_market,
                                      extended_hours=False, config=ec)
        forced = why == FORCED

        exit_fill = Fill(
            order_id=f"x{seq}", symbol=cfg.symbol, side="long", quantity=qty, fill_price=exit_px,
            fill_ts=ts[exit_idx], commission=_commission(qty, ec), slippage_points=0.0, bar_open_ts=ts[exit_idx],
        )
        commissions = entry_fill.commission + exit_fill.commission
        realized = (exit_px - entry_fill_px) * qty - commissions
        reason = {STOP_EXIT: ExitReason.STOP_LOSS, TARGET_EXIT: ExitReason.TAKE_PROFIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, FORCED: ExitReason.SESSION_EXIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=cfg.symbol, side="long",
            entry_order_id=entry_fill.order_id, entry_fill=entry_fill, quantity=qty,
            stop_price=stop, target_price=target, exit_fill=exit_fill, exit_reason=reason,
            realized_pnl=realized, realized_r=(exit_px - entry_fill_px) / risk, commission_total=commissions,
            holding_bars=exit_idx - entry_idx,
        ))
        rows.append((ci, int(sig_p[s]), int(sig_q[s]), entry_idx, exit_idx, decision, qty, entry_fill_px, exit_px,
                     entry_fill.commission, realized, forced, why, stop, target, a_known))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        next_ok = exit_idx

    cols = list(zip(*rows)) if rows else [()] * 16
    i64 = lambda k: np.asarray(cols[k], dtype=np.int64)  # noqa: E731
    f64 = lambda k: np.asarray(cols[k], dtype=float)  # noqa: E731
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(0), pivot_idx=i64(1), prev_pivot_idx=i64(2), entry_idx=i64(3), exit_idx=i64(4),
        decision_idx=i64(5), quantity=f64(6), entry_px=f64(7), exit_px=f64(8), entry_commission=f64(9),
        realized_pnl=f64(10), forced_close=np.asarray(cols[11], dtype=bool),
        exit_reason=np.asarray(cols[12], dtype=object), stop_level=f64(13), target_level=f64(14),
        atr_used=f64(15),
    )
