"""Compact bar-based backtester for the intraday volatility-compression breakout (5min/15min bars).

Compression, decided from data through bar k only (indicators run over the RTH bar series
across sessions, like ATR in the other families):
    bbkc : 2 x sd(close, L) < kc_mult x ATR(L)     (Bollinger Bands, 2 sd, inside the Keltner
                                                   Channel; both centred on SMA(close, L);
                                                   sd is the population sd; ATR is Wilder's)
    nr   : high_k - low_k <= min(high - low over bars k-N+1 .. k)   (NR-N; ties count), and with
           inside_bar also high_k <= high_{k-1} and low_k >= low_{k-1}
A RUN is a maximal stretch of consecutive compression bars inside one session; a run never
continues across the session open. The run's BOX through bar r is [min low, max high] of its
bars up to r.

Setups: at bar k the active run is the one holding the last compression bar r <= k-1 of
the same session. It is live when k - r <= setup_expiry_bars and the run (through r) is at
least min_squeeze_bars long (NR: 1) and its box is at least min_box_atr x ATR(14)[r] wide.
So the box a decision uses is built only from bars BEFORE the decision bar:
    entry_type = close : breakout at bar k when close_k > box high (long) / < box low (short)
    entry_type = wick  : breakout at bar k when high_k > box high / low_k < box low (a stop
                         order resting at the edge); both edges in one bar is ambiguous
                         (unknown order) and is not traded.
The FIRST breakout of a run decides; the run is then consumed, whether or not that
breakout becomes a trade (wrong direction, trend filter, too late in the session, a
position already open, a missed entry). This keeps one setup = one decision.

Execution assumptions (audited by src/experiments/cb_integrity.py):
  * long and/or short (`direction`), one position at a time, compounding equity, no leverage;
    every position is closed by the session's last bar (nothing is held overnight);
  * filters, all known at the decision: trend_filter = ema50 needs close > EMA(50) for a long
    and < for a short (close entries: at bar k; wick entries: at bar k-1, the last close
    before the order can fill); no decision on the session's last bar or less than
    `last_entry_cutoff` minutes before the session's last close;
  * close entries fill at the NEXT bar's open (bar k+1+delay) with market slippage; wick
    entries fill on bar k at the worse of its open and the box edge, with stop slippage
    (with an entry delay they fill at the open `delay` bars later instead); the fill bar
    must be in the same session, else the setup is skipped;
  * stop: the far side of the box (`stop_atr` None) or base -/+ stop_atr x ATR(14) using the
    last ATR known BEFORE the fill bar (bar e-1), where base is the entry price before
    slippage. R = the base-to-stop distance; a setup with R <= 0 is skipped;
  * target (optional): base +/- target_r x R; filled at the better of the bar's open and the
    target (a gap through it fills at the open), with market slippage;
  * stop and target are live intrabar from the entry bar on. A bar that touches both counts as
    the stop (conservative). On a wick entry's own bar only the stop is checked: a stop touch
    there counts even though the bar's order of events is unknown (conservative), and it
    fills at the stop;
  * session-close exit: a position still open on the session's last bar is closed at that
    bar's CLOSE (market-on-close with market slippage); stop and target take precedence;
  * every fill pays adverse slippage + commission; sizing is the mean-reversion funnel's
    (as many whole contracts as equity covers at full contract value);
  * a position closed on the data's final bar by the session-close rule is flagged forced
    (the session may be cut short by the data end) and is not a completed trade.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import polars as pl

from src.data.aggregation import AGG_INTERVAL_MINUTES
from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.features.atr import wilder_atr
from src.strategies.compression_breakout.config import (
    ATR_PERIOD,
    BB_STD,
    LAST_ENTRY_CUTOFF_MINUTES,
    TREND_EMA,
)
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.utils.config_models import ExecutionConfig

TARGET_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "target_exit", "eod_exit", "stop_exit", "forced_close"


def _cacheable(kc_mult: float) -> bool:
    return round(kc_mult, 2) == kc_mult


class CBData:
    """Per-(symbol, timeframe) arrays. Session structure, the indicators and the compression
    runs are cached so the thousands of configs sharing them don't recompute. Exposes the
    attributes the daily mark-to-market code needs (ts, open..close, session_date,
    day_end_idx, days), like the mean-reversion data object."""

    def __init__(self, bars: pl.DataFrame) -> None:
        df = bars.sort("bar_open_ts")
        self.ts = df["bar_open_ts"].to_list()
        self.open = df["open"].to_numpy().astype(float)
        self.high = df["high"].to_numpy().astype(float)
        self.low = df["low"].to_numpy().astype(float)
        self.close = df["close"].to_numpy().astype(float)
        self.n = df.height
        self.price_adj = (df["price_adjustment"].to_numpy().astype(float) if "price_adjustment" in df.columns
                          else np.zeros(self.n))
        ny = (df["bar_open_ts_ny"] if "bar_open_ts_ny" in df.columns
              else df["bar_open_ts"].dt.convert_time_zone("America/New_York"))
        sd = df["session_date_ny"] if "session_date_ny" in df.columns else ny.dt.date()
        self.session_date = sd.to_numpy().astype("datetime64[D]")
        if self.n:
            change = np.flatnonzero(self.session_date[1:] != self.session_date[:-1])
            self.day_end_idx = np.append(change, self.n - 1)
            self.day_start_idx = np.concatenate([[0], change + 1])
        else:
            self.day_end_idx = self.day_start_idx = np.array([], dtype=int)
        self.days = self.session_date[self.day_end_idx]
        self.bar_open = df["bar_open_ts"].to_numpy()
        self.sess = np.zeros(self.n, dtype=np.int64)
        if self.n:
            self.sess[self.day_start_idx[1:]] = 1
            self.sess = np.cumsum(self.sess)
        self.sess_start = self.day_start_idx[self.sess] if self.n else np.array([], dtype=int)
        self.sess_end = self.day_end_idx[self.sess] if self.n else np.array([], dtype=int)
        self.is_last = np.arange(self.n) == self.sess_end
        self.tod = (ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)).to_numpy().astype(np.int64)
        self.tf_minutes = self._bar_minutes(df)
        self._df = df
        self._cache: dict[tuple, object] = {}

    @staticmethod
    def _bar_minutes(df: pl.DataFrame) -> int:
        if "timeframe" in df.columns and df.height and df["timeframe"][0] in AGG_INTERVAL_MINUTES:
            return AGG_INTERVAL_MINUTES[df["timeframe"][0]]
        d = np.diff(df["bar_open_ts"].to_numpy()).astype("timedelta64[m]").astype(np.int64)
        d = d[d > 0]
        return int(d.min()) if len(d) else 1

    def _get(self, key: tuple, fn, *, cache: bool = True):
        if not cache:
            return fn()
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    # --- indicators (causal; NaN during warm-up) ---------------------------------------------

    def atr(self, period: int) -> np.ndarray:
        return self._get(("atr", period), lambda: wilder_atr(self._df, period=period)["atr"]
                         .fill_null(np.nan).to_numpy().astype(float))

    def sma_sd(self, length: int) -> tuple[np.ndarray, np.ndarray]:
        """SMA and population sd of closes over the last `length` bars (bar k included)."""
        def calc():
            s = pl.Series(self.close)
            m = s.rolling_mean(window_size=length, min_samples=length).fill_null(np.nan).to_numpy()
            v = s.rolling_std(window_size=length, min_samples=length, ddof=0).fill_null(np.nan).to_numpy()
            return m.astype(float), v.astype(float)
        return self._get(("sma_sd", length), calc)

    @property
    def ema_trend(self) -> np.ndarray:
        return self._get(("ema", TREND_EMA), lambda: pl.Series(self.close)
                         .ewm_mean(span=TREND_EMA, adjust=False, min_samples=TREND_EMA)
                         .fill_null(np.nan).to_numpy().astype(float))

    @property
    def bar_range(self) -> np.ndarray:
        return self._get(("range",), lambda: self.high - self.low)

    # --- compression and runs ------------------------------------------------------------------

    def compression(self, p: "CBParams") -> np.ndarray:
        if p.compression == "bbkc":
            key = ("comp", "bbkc", p.squeeze_length, round(p.kc_mult, 9))

            def calc():
                _, sd = self.sma_sd(p.squeeze_length)
                with np.errstate(invalid="ignore"):
                    return BB_STD * sd < p.kc_mult * self.atr(p.squeeze_length)  # NaN -> False
            # Perturbation draws give each job its own float kc_mult: cache only grid-like values
            # (two decimals: every grid value and every +/- 0.25 local move), so the per-worker
            # cache cannot grow without bound (the noise-band funnel ran out of memory that way).
            return self._get(key, calc, cache=_cacheable(p.kc_mult))
        if p.compression == "nr":
            def calc():
                rng = self.bar_range
                mn = pl.Series(rng).rolling_min(window_size=p.nr_lookback, min_samples=p.nr_lookback)
                mn = mn.fill_null(np.nan).to_numpy()
                with np.errstate(invalid="ignore"):
                    out = rng <= mn  # NaN -> False
                if p.inside_bar:
                    inside = np.zeros(self.n, dtype=bool)
                    inside[1:] = (self.high[1:] <= self.high[:-1]) & (self.low[1:] >= self.low[:-1])
                    out &= inside
                return out
            return self._get(("comp", *self._comp_key(p)), calc)
        raise ValueError(f"Unknown compression {p.compression!r}")

    def runs(self, p: "CBParams") -> dict[str, np.ndarray]:
        """Per bar: the start of its compression run (-1 off-run), the run's box high / low
        through that bar, and the last compression bar of the same session BEFORE the bar."""
        comp = self.compression(p)
        key = ("runs", *self._comp_key(p))

        def calc():
            n = self.n
            prev = np.concatenate([[False], comp[:-1]])
            new_sess = np.concatenate([[True], self.sess[1:] != self.sess[:-1]])
            start = comp & (~prev | new_sess)
            rid = np.cumsum(start) - 1
            starts = np.flatnonzero(start)
            run_start = np.full(n, -1, dtype=np.int64)
            if len(starts):
                run_start[comp] = starts[rid[comp]]
            g = np.where(comp, rid, -1)
            f = pl.DataFrame({"g": g, "h": self.high, "l": self.low}).with_columns(
                pl.col("h").cum_max().over("g"), pl.col("l").cum_min().over("g"))
            box_hi = np.where(comp, f["h"].to_numpy(), np.nan)
            box_lo = np.where(comp, f["l"].to_numpy(), np.nan)
            last = np.maximum.accumulate(np.where(comp, np.arange(n), -1)) if n else np.array([], dtype=np.int64)
            before = np.concatenate([[-1], last[:-1]]) if n else last
            before = np.where(before >= self.sess_start, before, -1)
            return {"run_start": run_start, "box_hi": box_hi, "box_lo": box_lo, "last_before": before}
        return self._get(key, calc, cache=p.compression == "nr" or _cacheable(p.kc_mult))

    @staticmethod
    def _comp_key(p: "CBParams") -> tuple:
        if p.compression == "bbkc":
            return ("bbkc", p.squeeze_length, round(p.kc_mult, 9))
        return ("nr", p.nr_lookback, bool(p.inside_bar))


@dataclass(frozen=True)
class CBParams:
    """Free-valued strategy parameters (the line's config class restricts values to the grid
    lattice). Used for off-grid perturbations; the backtester accepts either. Settings of the
    other compression line are None (squeeze settings on an NR line, nr_lookback on a squeeze
    line)."""

    symbol: str
    timeframe: str
    compression: str
    squeeze_length: int | None
    kc_mult: float | None
    min_squeeze_bars: int | None
    nr_lookback: int | None
    entry_type: str
    setup_expiry_bars: int
    stop_atr: float | None      # None = stop at the far side of the box
    target_r: float | None      # None = no profit target
    direction: str
    trend_filter: str
    min_box_atr: float = 0.0    # the box must be at least this x ATR(14) wide (0 = any)
    inside_bar: bool = False    # NR only: the NR bar must also be an inside bar
    last_entry_cutoff: int = LAST_ENTRY_CUTOFF_MINUTES

    @classmethod
    def from_config(cls, cfg) -> "CBParams":
        kc = getattr(cfg, "kc_mult", None)
        return cls(cfg.symbol, cfg.timeframe, cfg.compression, getattr(cfg, "squeeze_length", None),
                   None if kc is None else float(kc), getattr(cfg, "min_squeeze_bars", None),
                   getattr(cfg, "nr_lookback", None), cfg.entry_type, cfg.setup_expiry_bars,
                   cfg.stop_atr_value, cfg.target_r_value, cfg.direction, cfg.trend_filter,
                   float(cfg.min_box_atr), bool(getattr(cfg, "inside_bar", False)))

    @property
    def min_run(self) -> int:
        return self.min_squeeze_bars if self.compression == "bbkc" else 1


def as_params(cfg) -> CBParams:
    return cfg if isinstance(cfg, CBParams) else CBParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is +1 (long) / -1 (short); quantities are always positive."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray     # breakout (decision) bar; wick entries fill on this bar
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray   # bar on which the exit happened
    quantity: np.ndarray
    entry_px: np.ndarray
    exit_px: np.ndarray
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray    # TARGET_EXIT / EOD_EXIT / STOP_EXIT / FORCED
    stop_level: np.ndarray
    target_level: np.ndarray   # nan = no target
    entry_base: np.ndarray     # entry price before slippage (the R anchor)
    box_hi: np.ndarray
    box_lo: np.ndarray
    run_start: np.ndarray
    side: np.ndarray


def setups(data: CBData, p: CBParams) -> dict[str, np.ndarray]:
    """Every run's first breakout, one row per consumed setup (sorted by bar):
    k (decision bar), side (+1 / -1 / 0 = both edges in one wick bar), the box it broke,
    the run start and its last compression bar before k, and `ok` -- whether the
    filters (direction, trend, entry window) allow a trade."""
    if p.entry_type not in ("close", "wick"):
        raise ValueError(f"Unknown entry_type {p.entry_type!r}")
    if p.direction not in ("long", "short", "both"):
        raise ValueError(f"Unknown direction {p.direction!r}")
    if p.trend_filter not in ("none", "ema50"):
        raise ValueError(f"Unknown trend_filter {p.trend_filter!r}")
    ru = data.runs(p)
    lb = ru["last_before"]
    k = np.arange(data.n)
    valid = lb >= 0
    r = np.where(valid, lb, 0)
    s = ru["run_start"][r]
    active = valid & (k - r <= p.setup_expiry_bars) & (r - s + 1 >= p.min_run)
    bh, bl = ru["box_hi"][r], ru["box_lo"][r]
    if p.min_box_atr > 0:
        with np.errstate(invalid="ignore"):
            active &= (bh - bl) >= p.min_box_atr * data.atr(ATR_PERIOD)[r]  # NaN ATR -> not live
    if p.entry_type == "close":
        up, dn = data.close > bh, data.close < bl
    else:
        up, dn = data.high > bh, data.low < bl
    ks = np.flatnonzero(active & (up | dn))
    if len(ks):
        _, first = np.unique(s[ks], return_index=True)
        ks = np.sort(ks[first])
    side = np.where(up[ks] & ~dn[ks], 1, np.where(dn[ks] & ~up[ks], -1, 0)).astype(np.int64)
    ok = side != 0
    if p.direction == "long":
        ok &= side > 0
    elif p.direction == "short":
        ok &= side < 0
    if p.trend_filter == "ema50":
        j = ks if p.entry_type == "close" else ks - 1
        ema, c = data.ema_trend[j], data.close[j]
        ok &= np.where(side > 0, c > ema, c < ema)  # NaN EMA -> False
    to_close = data.tod[data.sess_end[ks]] - data.tod[ks]  # bar close to the session's last close, minutes
    ok &= ~data.is_last[ks] & (to_close >= p.last_entry_cutoff)
    return {"k": ks, "side": side, "box_hi": bh[ks], "box_lo": bl[ks], "run_start": s[ks],
            "last_comp": r[ks], "ok": ok}


def simulate_compression_breakout(
    data: CBData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills the entry that many
    extra bars late at that bar's open (still within the session, else skipped);
    `missed_entry_frac` drops that fraction of the setups that would have been traded
    (the setup is consumed, so a missed entry is never re-taken later)."""
    p = as_params(cfg)
    st = setups(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    atr = data.atr(ATR_PERIOD) if p.stop_atr is not None else None
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    intrabar = p.entry_type == "wick" and entry_delay_bars == 0

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0  # first bar a new decision may use (close: k >= exit bar; wick: k > exit bar)
    for i in np.flatnonzero(st["ok"]):
        k, d = int(st["k"][i]), int(st["side"][i])
        if k < free_from:
            continue  # a position was open: the setup is consumed
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        bh, bl = float(st["box_hi"][i]), float(st["box_lo"][i])
        if p.entry_type == "close":
            e = k + 1 + entry_delay_bars
        else:
            e = k + entry_delay_bars
        if e >= n or e > data.sess_end[k]:
            continue
        if intrabar:
            base = max(o[e], bh) if d > 0 else min(o[e], bl)
            fill_px = costs.fill(base, "buy" if d > 0 else "sell", stop=True)
        else:
            base = o[e]
            fill_px = costs.fill(base, "buy" if d > 0 else "sell")
        if p.stop_atr is None:
            stop = bl if d > 0 else bh
        else:
            a = atr[e - 1] if e >= 1 else float("nan")
            if not math.isfinite(a) or a <= 0:
                continue
            stop = base - d * p.stop_atr * a
        risk = d * (base - stop)
        if not risk > 0:
            continue
        target = base + d * p.target_r * risk if p.target_r is not None else float("nan")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        L = int(data.sess_end[e])
        side = "long" if d > 0 else "short"
        x_action = "sell" if d > 0 else "buy"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        for j in range(e, L + 1):
            if (d > 0 and lo[j] <= stop) or (d < 0 and hi[j] >= stop):
                px = stop if (intrabar and j == e) else (min(o[j], stop) if d > 0 else max(o[j], stop))
                exit_px, why = costs.fill(px, x_action, stop=True), STOP_EXIT
                break
            if math.isfinite(target) and not (intrabar and j == e) and \
                    ((d > 0 and hi[j] >= target) or (d < 0 and lo[j] <= target)):
                px = max(o[j], target) if d > 0 else min(o[j], target)
                exit_px, why = costs.fill(px, x_action), TARGET_EXIT
                break
            if j == L:
                exit_px, why = costs.fill(c[j], x_action), (FORCED if j == n - 1 else EOD_EXIT)
                break
        x = j
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[x], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[x])
        commissions = entry_fill.commission + exit_fill.commission
        realized = d * (exit_px - fill_px) * qty - commissions
        reason = {TARGET_EXIT: ExitReason.TAKE_PROFIT, EOD_EXIT: ExitReason.SESSION_EXIT,
                  STOP_EXIT: ExitReason.STOP_LOSS, FORCED: ExitReason.SESSION_EXIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop,
            target_price=None if math.isnan(target) else target,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (risk * qty), commission_total=commissions, holding_bars=x - e,
        ))
        rows.append((k, e, x, x, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, stop,
                     target, base, bh, bl, int(st["run_start"][i]), d))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[x], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = x if p.entry_type == "close" else x + 1

    cols = list(zip(*rows)) if rows else [()] * 18
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=f(cols[11]), target_level=f(cols[12]),
        entry_base=f(cols[13]), box_hi=f(cols[14]), box_lo=f(cols[15]), run_start=i64(cols[16]),
        side=i64(cols[17]),
    )
