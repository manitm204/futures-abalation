"""Compact bar-based backtester for the intraday noise-band breakout family (5min/15min bars).

The noise area, decided from data through bar k only:
    open_s     = the session's first bar open (known from the first bar on)
    move_k     = |close_k - open_s| / raw open_s   (raw = back-adjusted price - price_adjustment)
    sigma_k    = mean of move at the SAME time of day (bar-open minute, NY) over the
                 previous `band_lookback` sessions that have a bar at that time; today's
                 own move is never included. Undefined (NaN) until that many sessions exist.
    hi_s, lo_s = open_s, or max/min(open_s, previous session's last close) for
                 anchor = open_prev_close (the gap adjustment)
    upper_k    = hi_s + band_mult x sigma_k x raw open_s
    lower_k    = lo_s - band_mult x sigma_k x raw open_s
    vwap_k     = session VWAP of typical price (h+l+c)/3 x volume through bar k
Bars are RTH only (each root's day session, src/data/futures.py SESSIONS), and every
lookback runs over sessions, not bars.

Check bars: bars whose CLOSE lands on a multiple of `check_minutes` after the session
open (e.g. 10:00, 10:30, ... for a 09:30 open and 30 minutes). Signals and trailing
exits are only evaluated at check-bar closes; the protective stop and the session
close are live on every bar.

Execution assumptions (audited by src/experiments/nb_integrity.py):
  * long and/or short (`direction`), one position at a time, compounding equity, no
    leverage; every position is closed by the session's last bar (no overnight risk);
  * entry: at a check-bar close above upper (long) / below lower (short), at least
    `first_entry_minutes` after the session open, never on the session's last bar; filled at the NEXT bar's open (bar k+1+delay), which must be
    in the same session (otherwise the signal is skipped);
  * trailing exit at a check-bar close j: long when close_j < level_j, short when
    close_j > level_j, with level = upper/lower (trail=band), VWAP (vwap) or the
    tighter of the two (band_vwap: max(upper, VWAP) long, min(lower, VWAP) short);
    filled at bar j+1's open;
  * session-close exit: a position still open on the session's last bar is closed at
    that bar's CLOSE (a market-on-close fill with the same slippage) -- this takes
    precedence over a trailing exit decided at the same close;
  * optional protective stop at entry-bar open -/+ stop_atr x ATR(14), using the last
    ATR known BEFORE the entry fill, live from the entry bar; a touch exits that bar at
    the worse of its open and the stop (stop slippage) and takes precedence over every
    close-based exit of the same bar;
  * after a trailing or stop exit, a new entry in the SAME direction must re-arm: a
    check-bar close back on the inside of that side's band, at or after the exit
    decision bar, in the same session (each session starts armed). The opposite
    direction is not blocked. Signals can form from the exit fill bar's close on;
  * every fill pays adverse slippage + commission; sizing is the mean-reversion
    funnel's (as many whole contracts as equity covers at full contract value);
  * a position closed on the data's final bar by the session-close rule is flagged
    forced (the session may be cut short by the data end) and is not a completed trade.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import polars as pl

from src.data.aggregation import AGG_INTERVAL_MINUTES
from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.features.atr import wilder_atr
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.utils.config_models import ExecutionConfig

TRAIL_EXIT, EOD_EXIT, STOP_EXIT, FORCED = "trail_exit", "eod_exit", "stop_exit", "forced_close"
ATR_PERIOD = 14


class NBData:
    """Per-(symbol, timeframe) arrays. Session structure, VWAP and the per-lookback
    noise sigma are cached so the thousands of configs sharing them don't recompute.
    Exposes the attributes the daily mark-to-market code needs (ts, open..close,
    session_date, day_end_idx, days), like the mean-reversion data object."""

    def __init__(self, bars: pl.DataFrame) -> None:
        df = bars.sort("bar_open_ts")
        self.ts = df["bar_open_ts"].to_list()
        self.open = df["open"].to_numpy().astype(float)
        self.high = df["high"].to_numpy().astype(float)
        self.low = df["low"].to_numpy().astype(float)
        self.close = df["close"].to_numpy().astype(float)
        self.volume = (df["volume"].to_numpy().astype(float) if "volume" in df.columns else np.ones(df.height))
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
        # Session id per bar, and that session's first / last bar.
        self.sess = np.zeros(self.n, dtype=np.int64)
        if self.n:
            self.sess[self.day_start_idx[1:]] = 1
            self.sess = np.cumsum(self.sess)
        self.sess_start = self.day_start_idx[self.sess] if self.n else np.array([], dtype=int)
        self.sess_end = self.day_end_idx[self.sess] if self.n else np.array([], dtype=int)
        self.is_last = np.arange(self.n) == self.sess_end
        # Time of day (bar-open minute, NY) is the noise slot.
        self.tod = (ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)).to_numpy().astype(np.int64)
        self.tf_minutes = self._bar_minutes(df)
        first_tod = self.tod[self.day_start_idx] if self.n else np.array([], dtype=np.int64)
        vals, counts = np.unique(first_tod, return_counts=True)
        self.open_minute = int(vals[np.argmax(counts)]) if len(vals) else 0  # modal session open
        self.sess_open = self.open[self.sess_start] if self.n else np.array([])
        self.raw_sess_open = self.sess_open - self.price_adj
        prev_close = np.full(self.n, np.nan)
        if self.n and len(self.day_end_idx) > 1:
            last_close = self.close[self.day_end_idx]
            prev_close[self.sess > 0] = last_close[self.sess[self.sess > 0] - 1]
        self.prev_close = prev_close
        self._df = df
        self._cache: dict[tuple, np.ndarray] = {}

    @staticmethod
    def _bar_minutes(df: pl.DataFrame) -> int:
        if "timeframe" in df.columns and df.height and df["timeframe"][0] in AGG_INTERVAL_MINUTES:
            return AGG_INTERVAL_MINUTES[df["timeframe"][0]]
        d = np.diff(df["bar_open_ts"].to_numpy()).astype("timedelta64[m]").astype(np.int64)
        d = d[d > 0]
        return int(d.min()) if len(d) else 1

    def _get(self, key: tuple, fn) -> np.ndarray:
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    @property
    def move(self) -> np.ndarray:
        def calc():
            with np.errstate(divide="ignore", invalid="ignore"):
                m = np.abs(self.close - self.sess_open) / self.raw_sess_open
            m[~(self.raw_sess_open > 0)] = np.nan
            return m
        return self._get(("move",), calc)

    def sigma(self, lookback: int) -> np.ndarray:
        """Mean move at this bar's time of day over the previous `lookback` sessions."""
        def calc():
            f = pl.DataFrame({"i": np.arange(self.n), "slot": self.tod, "move": self.move})
            out = (f.sort(["slot", "i"])
                   .with_columns(pl.col("move").shift(1).rolling_mean(window_size=lookback, min_samples=lookback)
                                 .over("slot").alias("sigma"))
                   .sort("i"))
            return out["sigma"].fill_null(np.nan).to_numpy().astype(float)
        return self._get(("sigma", lookback), calc)

    @property
    def vwap(self) -> np.ndarray:
        def calc():
            typ = (self.high + self.low + self.close) / 3.0
            pv, v = np.cumsum(typ * self.volume), np.cumsum(self.volume)
            base = self.sess_start - 1
            pv0 = np.where(base >= 0, pv[np.maximum(base, 0)], 0.0)
            v0 = np.where(base >= 0, v[np.maximum(base, 0)], 0.0)
            cv = v - v0
            with np.errstate(divide="ignore", invalid="ignore"):
                out = (pv - pv0) / cv
            return np.where(cv > 0, out, self.close)  # no volume yet -> the close
        return self._get(("vwap",), calc)

    def check(self, minutes: int) -> np.ndarray:
        """Bars whose close lands on a multiple of `minutes` after the session open."""
        return self._get(("check", minutes),
                         lambda: (self.tod + self.tf_minutes - self.open_minute) % minutes == 0)

    def bands(self, lookback: int, mult: float, anchor: str) -> tuple[np.ndarray, np.ndarray]:
        def calc():
            if anchor == "open":
                hi = lo = self.sess_open
            elif anchor == "open_prev_close":
                hi = np.fmax(self.sess_open, self.prev_close)  # NaN prior close -> the open
                lo = np.fmin(self.sess_open, self.prev_close)
            else:
                raise ValueError(f"Unknown anchor {anchor!r}")
            w = mult * self.sigma(lookback) * self.raw_sess_open
            return np.stack([hi + w, lo - w])
        b = self._get(("bands", lookback, float(mult), anchor), calc)
        return b[0], b[1]

    @property
    def atr(self) -> np.ndarray:
        return self._get(("atr",), lambda: wilder_atr(self._df, period=ATR_PERIOD)["atr"]
                         .to_numpy().astype(float))


@dataclass(frozen=True)
class NBParams:
    """Free-valued strategy parameters (NoiseBandConfig restricts values to the grid
    lattice). Used for off-grid perturbations; the backtester accepts either."""

    symbol: str
    timeframe: str
    band_lookback: int
    band_mult: float
    check_minutes: int
    anchor: str
    trail: str
    direction: str
    stop_atr: float | None = None
    first_entry_minutes: int = 0   # bar close must be at least this long after the open

    @classmethod
    def from_config(cls, cfg) -> "NBParams":
        return cls(cfg.symbol, cfg.timeframe, cfg.band_lookback, cfg.band_mult, cfg.check_minutes,
                   cfg.anchor, cfg.trail, cfg.direction, cfg.stop_atr_value, cfg.first_entry_minutes)


def as_params(cfg) -> NBParams:
    return cfg if isinstance(cfg, NBParams) else NBParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is +1 (long) / -1 (short); quantities are always positive."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray   # bar whose close triggered the exit; stop exits: the stop bar
    quantity: np.ndarray
    entry_px: np.ndarray
    exit_px: np.ndarray
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray    # TRAIL_EXIT / EOD_EXIT / STOP_EXIT / FORCED
    stop_level: np.ndarray     # protective stop per trade (nan = no stop)
    side: np.ndarray


def signal_arrays(data: NBData, p: NBParams) -> dict[str, np.ndarray]:
    """Per-bar booleans decided at that bar's close, keyed by direction (+1 / -1):
    entry signal, trailing-exit signal, and 'inside' (re-arms that side)."""
    up, lo = data.bands(p.band_lookback, p.band_mult, p.anchor)
    c, vw = data.close, data.vwap
    chk = data.check(p.check_minutes)
    since_open = data.tod + data.tf_minutes - data.open_minute  # bar close, minutes after the open
    can_enter = chk & ~data.is_last & (since_open >= p.first_entry_minutes)
    above, below = c > up, c < lo  # NaN band -> False
    if p.trail == "band":
        lvl_l, lvl_s = up, lo
    elif p.trail == "vwap":
        lvl_l = lvl_s = vw
    elif p.trail == "band_vwap":
        lvl_l, lvl_s = np.fmax(up, vw), np.fmin(lo, vw)
    else:
        raise ValueError(f"Unknown trail {p.trail!r}")
    if p.direction not in ("long", "short", "both"):
        raise ValueError(f"Unknown direction {p.direction!r}")
    out = {
        "entry_l": can_enter & above if p.direction in ("long", "both") else np.zeros(data.n, dtype=bool),
        "entry_s": can_enter & below if p.direction in ("short", "both") else np.zeros(data.n, dtype=bool),
        "exit_l": chk & (c < lvl_l), "exit_s": chk & (c > lvl_s),
        "inside_l": chk & ~above, "inside_s": chk & ~below,
        "upper": up, "lower": lo, "level_l": lvl_l, "level_s": lvl_s,
    }
    return out


def simulate_noise_band(
    data: NBData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills the entry that many
    extra bars late (still within the session, else skipped); `missed_entry_frac` drops
    that fraction of signal EPISODES -- a missed signal blocks its direction until the
    side re-arms, so it is genuinely missed rather than re-taken a bar later."""
    p = as_params(cfg)
    sig = signal_arrays(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    atr = data.atr if p.stop_atr is not None else None
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    cand = np.flatnonzero(sig["entry_l"] | sig["entry_s"])
    inside = {1: np.flatnonzero(sig["inside_l"]), -1: np.flatnonzero(sig["inside_s"])}
    exit_sig = {1: sig["exit_l"], -1: sig["exit_s"]}
    block: dict[int, tuple[int, int] | None] = {1: None, -1: None}  # side -> (session, from bar)

    def armed(d: int, k: int) -> bool:
        b = block[d]
        if b is None:
            return True
        if b[0] != data.sess[k]:
            block[d] = None
            return True
        ins = inside[d]
        m = np.searchsorted(ins, b[1])
        if m < len(ins) and ins[m] <= k:
            block[d] = None
            return True
        return False

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    ci = 0
    start = 0
    while True:
        ci += int(np.searchsorted(cand[ci:], start))
        if ci >= len(cand):
            break
        k = int(cand[ci])
        ci += 1
        d = 1 if sig["entry_l"][k] else -1
        if not armed(d, k):
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            block[d] = (int(data.sess[k]), k + 1)  # skip this episode until the side re-arms
            continue
        e = k + 1 + entry_delay_bars
        if e >= n or e > data.sess_end[k]:
            continue
        L = int(data.sess_end[e])
        raw_px = o[e]
        fill_px = costs.fill(raw_px, "buy" if d > 0 else "sell")
        stop = float("nan")
        if p.stop_atr is not None:
            a = atr[e - 1]
            if not math.isfinite(a) or a <= 0:
                continue
            stop = raw_px - d * p.stop_atr * a
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side = "long" if d > 0 else "short"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - raw_px), bar_open_ts=ts[e])
        x_action = "sell" if d > 0 else "buy"
        why = None
        for j in range(e, L + 1):
            if math.isfinite(stop) and ((d > 0 and lo[j] <= stop) or (d < 0 and hi[j] >= stop)):
                base = min(o[j], stop) if d > 0 else max(o[j], stop)
                exit_px, decision, exit_idx, why = costs.fill(base, x_action, stop=True), j, j, STOP_EXIT
                break
            if j == L:
                exit_px, decision, exit_idx = costs.fill(c[j], x_action), j, j
                why = FORCED if j == n - 1 else EOD_EXIT
                break
            if exit_sig[d][j]:
                exit_px, decision, exit_idx, why = costs.fill(o[j + 1], x_action), j, j + 1, TRAIL_EXIT
                break
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[exit_idx], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[exit_idx])
        commissions = entry_fill.commission + exit_fill.commission
        realized = d * (exit_px - fill_px) * qty - commissions
        reason = {TRAIL_EXIT: ExitReason.TAKE_PROFIT, EOD_EXIT: ExitReason.SESSION_EXIT,
                  STOP_EXIT: ExitReason.STOP_LOSS, FORCED: ExitReason.SESSION_EXIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=None if math.isnan(stop) else stop, target_price=None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized, realized_r=None,
            commission_total=commissions, holding_bars=exit_idx - e,
        ))
        rows.append((k, e, exit_idx, decision, qty, fill_px, exit_px, entry_fill.commission, realized, forced,
                     why, stop, d))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        if why in (TRAIL_EXIT, STOP_EXIT):
            block[d] = (int(data.sess[decision]), decision)
        start = exit_idx  # a new signal can form at the exit bar's close

    cols = list(zip(*rows)) if rows else [()] * 13
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=np.asarray(cols[0], dtype=np.int64), entry_idx=np.asarray(cols[1], dtype=np.int64),
        exit_idx=np.asarray(cols[2], dtype=np.int64), decision_idx=np.asarray(cols[3], dtype=np.int64),
        quantity=np.asarray(cols[4], dtype=float), entry_px=np.asarray(cols[5], dtype=float),
        exit_px=np.asarray(cols[6], dtype=float), entry_commission=np.asarray(cols[7], dtype=float),
        realized_pnl=np.asarray(cols[8], dtype=float), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=np.asarray(cols[11], dtype=float),
        side=np.asarray(cols[12], dtype=np.int64),
    )
