"""Compact bar-based backtester for the moving-average crossover family (5min/15min/1h bars).

Signal, decided at bar c's close from data through bar c only:
    fast, slow = MA(fast_length), MA(slow_length) of closes, each an SMA or EMA per
               `ma_pair` ("EMA/SMA" = EMA fast, SMA slow). SMA_t is the mean of the
               last n closes through t; EMA (alpha = 2/(n+1)) is seeded with the SMA of
               the first n closes. Both are NaN during warm-up.
    diff     = fast - slow; the bar is "bullish" when diff > 0 (NaN -> not bullish).
    crossover at bar k: bullish at k, not bullish at k-1 with diff_{k-1} defined (a
               bullish run that starts during warm-up is never traded).
    A bar c of a bullish run (k <= c, every bar in k..c bullish) QUALIFIES when all of:
        c - k + 1 >= confirm_bars                  (1 = enter on the crossover bar)
        diff_c >= buffer_atr x ATR(14)_c            (buffer_atr = 0: off)
        slow_c > slow_{c - SLOPE_BARS}             (slope_filter on only)
        ADX(14)_c >= min_adx                        (v2; off by default)
        close_c - slow_c <= max_extension_atr x ATR(14)_c   (v2; off by default)
    The long entry signal is the first qualifying bar of a not-yet-traded run at or
    after the earliest allowed bar (the previous exit bar + cooldown_bars). At most
    one entry per bullish run: a run whose conditions never hold, or whose trade has
    exited (stop, target, time or cross), is not traded again until the next
    crossover. With no cooldown and no mid-run exits (v1) this is exactly the first
    qualifying bar of each run.
All lengths are in bars and run continuously across sessions (RTH bars only).

Execution assumptions (audited by src/experiments/ma_integrity.py):
  * long-only, one position at a time, compounding equity, no leverage;
  * the entry is a market order filled at the NEXT bar's open (bar c+1+delay),
    adverse slippage + commission on every fill. A signal on a session's last bar
    fills at the next session's open; positions are held overnight (as in the
    other families);
  * optional initial stop = entry-bar open - stop_atr x ATR(14), using the last ATR
    known BEFORE the entry fill; it is live from the entry bar on. A bar whose low
    touches it exits at the worse of its open and the stop (stop slippage);
  * crossover exit: at the close of the first bar j > c with fast <= slow (a raw
    cross: no confirmation or buffer), exit at bar j+1's open; j is never before the
    entry bar (under entry-delay stress a cross before the fill is acted on at the
    entry bar's close). If bar j also touches the stop, the stop (intrabar) fills first;
  * v2 (each off by default): a take-profit limit at entry-bar open + take_profit_atr x
    the same pre-fill ATR fills AT the target when a bar's high reaches it (a gap above
    is not credited; a bar touching stop and target is a stop); a time exit decided at
    the close of bar entry + max_hold - 1 fills at the next open (exactly max_hold bars
    after the entry; a cross back on that same close is labelled a cross exit);
    cooldown_bars blocks any entry fill until cooldown_bars bars after the exit bar;
  * sizing: each entry buys as many whole shares as current equity affords
    (identical to the RSI / mean-reversion funnels, so results are comparable);
  * signals while a position is open are ignored; a new signal may form at or after
    the exit bar (its entry then fills strictly after the exit);
  * a position still open when the data ends is force-closed at the last close and
    flagged (not counted as a completed trade).
"""

from __future__ import annotations

import math
from collections import OrderedDict
from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.lib.stride_tricks import sliding_window_view

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.engine.fills import _apply_slippage, _commission
from src.features.atr import wilder_atr
from src.strategies.ma_crossover.config import SLOPE_BARS
from src.strategies.rsi_divergence.backtest import wilder_adx
from src.utils.config_models import ExecutionConfig

STOP_EXIT, TARGET_EXIT, TIME_EXIT, CROSS_EXIT, FORCED = (
    "stop_exit", "target_exit", "time_exit", "cross_exit", "forced_close")
ATR_PERIOD = 14
ADX_PERIOD = 14


def sma(close: np.ndarray, period: int) -> np.ndarray:
    """Causal simple moving average; first defined at index period - 1."""
    out = np.full(len(close), np.nan)
    if len(close) >= period:
        out[period - 1:] = sliding_window_view(close, period).mean(axis=1)
    return out


def ema(close: np.ndarray, period: int) -> np.ndarray:
    """Causal EMA (alpha = 2 / (period + 1)) seeded with the SMA of the first
    `period` closes (first defined at index period - 1); NaN before that."""
    out = np.full(len(close), np.nan)
    if len(close) < period:
        return out
    a = 2.0 / (period + 1)
    prev = close[:period].mean()
    out[period - 1] = prev
    for t in range(period, len(close)):
        prev += a * (close[t] - prev)
        out[t] = prev
    return out


MA_FUNCS = {"SMA": sma, "EMA": ema}
CACHE_MAX_BYTES = 120 * 2**20  # per MAData (i.e. per worker per timeframe)


def _nbytes(v) -> int:
    if isinstance(v, np.ndarray):
        return v.nbytes
    if isinstance(v, tuple):
        return sum(_nbytes(x) for x in v)
    return 0


class MAData:
    """Per-(symbol, timeframe) arrays. Moving averages, crossover regimes and
    entry signals are cached by their parameters so the thousands of configs
    sharing them don't recompute. Exposes the same attributes as the other
    families' data objects (ts, open..close, session_date, day_end_idx, days),
    which is all the daily mark-to-market code needs."""

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
        self._cache: OrderedDict[tuple, object] = OrderedDict()
        self._cache_bytes = 0

    def _get(self, key: tuple, fn):
        """LRU cache bounded by CACHE_MAX_BYTES: off-grid perturbations each bring new
        MA lengths, so an unbounded cache grows without limit in a long-lived worker."""
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        val = fn()
        self._cache[key] = val
        self._cache_bytes += _nbytes(val)
        while self._cache_bytes > CACHE_MAX_BYTES and len(self._cache) > 1:
            _, old = self._cache.popitem(last=False)
            self._cache_bytes -= _nbytes(old)
        return val

    def ma(self, kind: str, length: int) -> np.ndarray:
        return self._get(("ma", kind, length), lambda: MA_FUNCS[kind](self.close, length))

    def diff(self, pair: str, fast: int, slow: int) -> np.ndarray:
        """fast MA - slow MA (NaN during either warm-up)."""
        kf, ks = pair.split("/")
        return self._get(("diff", pair, fast, slow), lambda: self.ma(kf, fast) - self.ma(ks, slow))

    def regimes(self, pair: str, fast: int, slow: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(bullish, run_start, valid): per bar, whether fast > slow, the index of the
        crossover bar that started the current bullish run (-1 if not bullish), and
        whether that run is tradable (it began with a real cross from a defined diff)."""
        def calc():
            d = self.diff(pair, fast, slow)
            with np.errstate(invalid="ignore"):
                bull = d > 0
            prev = np.r_[False, bull[:-1]]
            ar = np.arange(self.n)
            start = np.maximum.accumulate(np.where(bull & ~prev, ar, -1)) if self.n else ar
            start = np.where(bull, start, -1)
            valid = bull & (start > 0)
            valid[valid] &= np.isfinite(d[start[valid] - 1])
            return bull, start, valid
        return self._get(("regime", pair, fast, slow), calc)

    def next_not_bull(self, pair: str, fast: int, slow: int) -> np.ndarray:
        """Per bar i: the first bar j >= i that is not bullish (n if none)."""
        def calc():
            bull = self.regimes(pair, fast, slow)[0]
            idx = np.where(bull, self.n, np.arange(self.n))
            return np.minimum.accumulate(idx[::-1])[::-1]
        return self._get(("nnb", pair, fast, slow), calc)

    def qualifies(self, pair: str, fast: int, slow: int, confirm: int, buffer: float, slope: bool,
                  min_adx: float | None = None, max_ext: float | None = None) -> np.ndarray:
        """Bool per bar: do the entry conditions hold at this bar's close?"""
        def calc():
            _, start, valid = self.regimes(pair, fast, slow)
            ar = np.arange(self.n)
            cond = valid & (ar - start + 1 >= confirm)
            with np.errstate(invalid="ignore"):  # NaN (warm-up) -> condition fails
                if buffer:
                    cond &= self.diff(pair, fast, slow) >= buffer * self.atr
                if slope:
                    cond &= self.slope_up(pair.split("/")[1], slow)
                if min_adx is not None:
                    cond &= self.adx >= min_adx
                if max_ext is not None:
                    cond &= self.close - self.ma(pair.split("/")[1], slow) <= max_ext * self.atr
            return cond
        return self._get(("qual", pair, fast, slow, confirm, float(buffer), slope, min_adx, max_ext), calc)

    def qualifying_bars(self, *args) -> np.ndarray:
        """Sorted indices of the bars where `qualifies(*args)` holds."""
        return self._get(("qidx", *args), lambda: np.flatnonzero(self.qualifies(*args)))

    def signals(self, pair: str, fast: int, slow: int, confirm: int, buffer: float,
                slope: bool) -> tuple[np.ndarray, np.ndarray]:
        """(first qualifying bar c, crossover bar k) of every run, sorted by c (v1 rule)."""
        idx = self.qualifying_bars(pair, fast, slow, confirm, float(buffer), slope, None, None)
        start = self.regimes(pair, fast, slow)[1]
        _, first = np.unique(start[idx], return_index=True)
        return idx[first], start[idx[first]]

    def slope_up(self, kind: str, length: int) -> np.ndarray:
        """slow_t > slow_{t - SLOPE_BARS} (False during warm-up)."""
        def calc():
            m = self.ma(kind, length)
            out = np.zeros(self.n, bool)
            with np.errstate(invalid="ignore"):
                out[SLOPE_BARS:] = m[SLOPE_BARS:] > m[:-SLOPE_BARS]
            return out
        return self._get(("slope", kind, length), calc)

    @property
    def adx(self) -> np.ndarray:
        return self._get(("adx",), lambda: wilder_adx(self.high, self.low, self.close, ADX_PERIOD))

    @property
    def atr(self) -> np.ndarray:
        return self._get(("atr",), lambda: wilder_atr(self._df, period=ATR_PERIOD)["atr"]
                         .to_numpy().astype(float))


@dataclass(frozen=True)
class MAParams:
    """Free-valued strategy parameters (MACrossoverConfig restricts values to the
    grid lattice). Used for off-grid perturbations; the backtester accepts either."""

    symbol: str
    timeframe: str
    ma_pair: str
    fast_length: int
    slow_length: int
    confirm_bars: int
    buffer_atr: float
    stop_atr: float | None
    slope_filter: bool
    max_hold: int | None = None            # v2: time exit after this many bars (None = off)
    take_profit_atr: float | None = None   # v2: target = entry open + this x ATR (None = off)
    cooldown_bars: int = 0                 # v2: bars after an exit before an entry may fill
    min_adx: float | None = None           # v2: ADX(14)_c >= this (None = off)
    max_extension_atr: float | None = None # v2: close_c - slow_c <= this x ATR(14)_c (None = off)

    @classmethod
    def from_config(cls, cfg) -> "MAParams":
        f = lambda v: None if v is None else float(v)  # noqa: E731
        v2 = {}
        if hasattr(cfg, "max_hold"):
            v2 = {"max_hold": cfg.max_hold, "take_profit_atr": f(cfg.take_profit_atr),
                  "cooldown_bars": int(cfg.cooldown_bars), "min_adx": f(cfg.min_adx),
                  "max_extension_atr": f(cfg.max_extension_atr)}
        return cls(cfg.symbol, cfg.timeframe, cfg.ma_pair, cfg.fast_length, cfg.slow_length, cfg.confirm_bars,
                   float(cfg.buffer_atr), f(cfg.stop_atr), bool(cfg.slope_filter), **v2)


def as_params(cfg) -> MAParams:
    return cfg if isinstance(cfg, MAParams) else MAParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray     # signal bar c
    cross_idx: np.ndarray      # crossover bar k that started the bullish run
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray   # bar that triggered the exit (stop: that bar; cross: the close before the fill; -1 forced)
    quantity: np.ndarray
    entry_px: np.ndarray       # entry fill price (after slippage)
    exit_px: np.ndarray        # exit fill price (after slippage)
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray    # STOP_EXIT / TARGET_EXIT / TIME_EXIT / CROSS_EXIT / FORCED
    stop_level: np.ndarray     # NaN when the stop is off
    target_level: np.ndarray   # NaN when the take profit is off
    atr_used: np.ndarray       # ATR known before the entry fill


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


def qualify_args(cfg) -> tuple:
    cfg = as_params(cfg)
    return (cfg.ma_pair, cfg.fast_length, cfg.slow_length, cfg.confirm_bars, float(cfg.buffer_atr),
            cfg.slope_filter, cfg.min_adx, cfg.max_extension_atr)


def _whole_shares(equity: float, px: float, ec: ExecutionConfig) -> int:
    """Most whole shares whose cost plus commission fits in `equity` (no leverage)."""
    if not (px > 0 and math.isfinite(px)):
        return 0
    q = math.floor(equity / px)
    while q > 0 and q * px + _commission(q, ec) > equity:
        q -= 1
    return q


def simulate_ma_crossover(
    data: MAData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off, i.e. the baseline run):
    `entry_delay_bars` fills the entry that many extra bars late (the stop still
    uses the ATR known before the fill); `missed_entry_frac` randomly drops that
    fraction of signals (a dropped signal's bullish run is not traded at all).
    Seeded by `stress_seed`. Cost stress is passed via `exec_config` (see
    `scale_variable_costs`)."""
    cfg = as_params(cfg)
    qidx = data.qualifying_bars(*qualify_args(cfg))
    start = data.regimes(cfg.ma_pair, cfg.fast_length, cfg.slow_length)[1]
    nnb = data.next_not_bull(cfg.ma_pair, cfg.fast_length, cfg.slow_length)
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
    next_ok = 0      # earliest bar a signal may form on (no position open, cooldown over)
    used_run = -1    # crossover bar of the last run that was traded (or dropped)

    while True:
        j = int(np.searchsorted(qidx, next_ok))
        if j >= len(qidx):
            break
        ci = int(qidx[j])
        k = int(start[ci])
        if k == used_run:  # this run was already traded: skip to the bar after it ends
            next_ok = int(nnb[ci])
            continue
        used_run = k
        if rng is not None and rng.random() < missed_entry_frac:
            continue  # the whole run is dropped, never re-entered a bar later
        entry_idx = ci + 1 + entry_delay_bars
        if entry_idx >= n:
            break
        a_known = atr[entry_idx - 1]
        if not math.isfinite(a_known) or a_known <= 0:
            continue  # ATR warm-up -> skip this run
        entry_px_raw = o[entry_idx]
        stop = entry_px_raw - cfg.stop_atr * a_known if cfg.stop_atr is not None else math.nan
        target = entry_px_raw + cfg.take_profit_atr * a_known if cfg.take_profit_atr is not None else math.nan
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

        # First close after the signal with fast <= slow (n: none). With an entry delay the
        # signal's run can end before the fill; the exit is then decided at the entry bar's close.
        cross = max(int(nnb[ci + 1]), entry_idx)
        timed = entry_idx + H - 1 if H is not None else n  # close of the max_hold-th bar held
        dec = min(cross, timed)    # first close-based exit decision
        last = min(dec, n - 1)     # bars entry..last can stop / target out (intrabar, before that close)
        seg_lo, seg_hi = lo[entry_idx:last + 1], hi[entry_idx:last + 1]
        hit = np.flatnonzero((seg_lo <= stop) | (seg_hi >= target)) if (cfg.stop_atr is not None
                                                                        or cfg.take_profit_atr is not None) else ()
        if len(hit):
            jx = entry_idx + int(hit[0])
            if lo[jx] <= stop:  # stop first if both touched in one bar
                why = STOP_EXIT
                exit_px = _apply_slippage(min(o[jx], stop), side="long", action="sell", bps=ec.slippage_bps_stop,
                                          extended_hours=False, config=ec)
            else:
                why = TARGET_EXIT
                exit_px = _apply_slippage(target, side="long", action="sell", bps=ec.slippage_bps_limit_adverse,
                                          extended_hours=False, config=ec)
            decision, exit_idx = jx, jx
        elif dec <= n - 2:
            why, decision, exit_idx = (CROSS_EXIT if dec == cross else TIME_EXIT), dec, dec + 1
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
        # The crossover exit is the strategy's own signal exit (MR maps its z exit the same way).
        reason = {STOP_EXIT: ExitReason.STOP_LOSS, TARGET_EXIT: ExitReason.TAKE_PROFIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, CROSS_EXIT: ExitReason.TAKE_PROFIT,
                  FORCED: ExitReason.SESSION_EXIT}[why]
        risk = cfg.stop_atr * a_known if cfg.stop_atr is not None else a_known  # no stop: R in ATR units
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=cfg.symbol, side="long",
            entry_order_id=entry_fill.order_id, entry_fill=entry_fill, quantity=qty,
            stop_price=stop, target_price=None if cfg.take_profit_atr is None else target,
            exit_fill=exit_fill, exit_reason=reason,
            realized_pnl=realized, realized_r=(exit_px - entry_fill_px) / risk, commission_total=commissions,
            holding_bars=exit_idx - entry_idx,
        ))
        rows.append((ci, k, entry_idx, exit_idx, decision, qty, entry_fill_px, exit_px,
                     entry_fill.commission, realized, forced, why, stop, a_known, target))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        next_ok = exit_idx + cfg.cooldown_bars  # signal at c fills at c + 1 > exit + cooldown

    cols = list(zip(*rows)) if rows else [()] * 15
    i64 = lambda k: np.asarray(cols[k], dtype=np.int64)  # noqa: E731
    f64 = lambda k: np.asarray(cols[k], dtype=float)  # noqa: E731
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(0), cross_idx=i64(1), entry_idx=i64(2), exit_idx=i64(3), decision_idx=i64(4),
        quantity=f64(5), entry_px=f64(6), exit_px=f64(7), entry_commission=f64(8), realized_pnl=f64(9),
        forced_close=np.asarray(cols[10], dtype=bool), exit_reason=np.asarray(cols[11], dtype=object),
        stop_level=f64(12), atr_used=f64(13), target_level=f64(14),
    )
