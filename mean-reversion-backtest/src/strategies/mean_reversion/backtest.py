"""Compact bar-based backtester for the mean-reversion family (5min/15min/1h bars).

Signal, decided at bar i's close from data through bar i only:
    z_i  = (close_i - mean_i) / std_i
    mean = SMA or EMA (adjust=False) of the last `mean_lookback` closes, incl. bar i
    std  = rolling sample std (ddof=1) of the last `std_lookback` closes, incl. bar i
    long entry when z_i <= entry_z and the trend filter holds (close_i > SMA_n_i)
All lookbacks are in bars and run continuously across sessions (RTH bars only;
the overnight gap is just the step between one session's last bar and the next
session's first).

Execution assumptions (audited by src/experiments/integrity.py):
  * long-only, one position at a time, compounding equity, no leverage;
  * every order is a market order filled at the NEXT bar's open (entry: bar
    i+1+delay; exit: the bar after the exit decision), adverse slippage +
    commission on every fill. A signal on a session's last bar fills at the next
    session's open; positions may be held overnight (as in the channel family);
  * exit decided at bar j's close (j >= entry bar) when z_j >= exit_z, or when the
    position has been held `max_hold` bars (j - entry + 1 >= max_hold), so a time
    exit fills exactly `max_hold` bars after the entry fill;
  * no profit target. v1 has no stop; v2 adds an optional ATR stop at
    entry fill - k * ATR(14), using the last ATR known BEFORE the entry fill, live
    from the entry bar (a touch exits that bar, at the worse of the open and the
    stop; it takes precedence over a z/time exit decided at the same close);
  * sizing: each entry buys as many whole shares as current equity affords
    (kept identical in v1 and v2 so results are comparable);
  * v2 options: `entry_confirmation = positive_bar_return` also requires the
    signal bar's close > the previous bar's close; `cooldown_bars = N` requires
    the next signal bar to be at least N bars after the previous exit bar;
  * after a TIME exit the setup must re-arm (z closes above entry_z) before the
    next entry, so the holding cap can't be undone by an immediate re-entry;
  * a position still open when the data ends is force-closed at the last close
    and flagged (not counted as a completed trade).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.engine.fills import _apply_slippage, _commission
from src.features.atr import wilder_atr
from src.utils.config_models import ExecutionConfig

Z_EXIT, TIME_EXIT, STOP_EXIT, FORCED = "z_exit", "time_exit", "stop_exit", "forced_close"
ATR_PERIOD = 14


class MRData:
    """Per-(symbol, timeframe) arrays. Means, stds and z-scores are cached by
    lookback so the thousands of configs sharing them don't recompute. Exposes
    the same attributes as the channel family's data object (ts, open..close,
    session_date, day_end_idx, days), which is all the daily mark-to-market code
    needs."""

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
        # NY session date per bar (datetime64[D]); day_end_idx = last bar of each session.
        self.session_date = sd.to_numpy().astype("datetime64[D]")
        if self.n:
            change = np.flatnonzero(self.session_date[1:] != self.session_date[:-1])
            self.day_end_idx = np.append(change, self.n - 1)
        else:
            self.day_end_idx = np.array([], dtype=int)
        self.days = self.session_date[self.day_end_idx]
        self._df = df
        self._close_s = df["close"]
        self._cache: dict[tuple, np.ndarray] = {}

    def _get(self, key: tuple, fn) -> np.ndarray:
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    def mean(self, kind: str, k: int) -> np.ndarray:
        if kind == "sma":
            return self._get(("sma", k), lambda: self._close_s.rolling_mean(window_size=k).to_numpy().astype(float))
        if kind == "ema":
            return self._get(("ema", k), lambda: self._close_s.ewm_mean(span=k, adjust=False, min_samples=k)
                             .to_numpy().astype(float))
        raise ValueError(f"Unknown mean_type {kind!r}")

    def std(self, k: int) -> np.ndarray:
        return self._get(("std", k), lambda: self._close_s.rolling_std(window_size=k, ddof=1)
                         .to_numpy().astype(float))

    def zscore(self, kind: str, mean_k: int, std_k: int) -> np.ndarray:
        def calc():
            s = self.std(std_k)
            with np.errstate(divide="ignore", invalid="ignore"):
                z = (self.close - self.mean(kind, mean_k)) / s
            z[~(s > 0)] = np.nan  # zero / undefined std -> no signal
            return z
        return self._get(("z", kind, mean_k, std_k), calc)

    @property
    def atr(self) -> np.ndarray:
        return self._get(("atr",), lambda: wilder_atr(self._df, period=ATR_PERIOD)["atr"]
                         .to_numpy().astype(float))

    def positive_bar(self) -> np.ndarray:
        def calc():
            up = np.zeros(self.n, dtype=bool)
            up[1:] = self.close[1:] > self.close[:-1]
            return up
        return self._get(("up",), calc)

    def trend_ok(self, trend_filter: str) -> np.ndarray:
        if trend_filter == "above_sma_100":
            trend_filter = "sma100"
        if trend_filter == "none":
            return np.ones(self.n, dtype=bool)
        if trend_filter.startswith("sma"):
            return self.close > self.mean("sma", int(trend_filter[3:]))  # NaN warm-up -> False
        raise ValueError(f"Unknown trend_filter {trend_filter!r}")


@dataclass(frozen=True)
class MRParams:
    """Free-valued strategy parameters (MeanReversionConfig restricts values to the
    grid lattice). Used for off-grid perturbations; the backtester accepts either."""

    symbol: str
    timeframe: str
    mean_type: str
    mean_lookback: int
    std_lookback: int
    entry_z: float
    exit_z: float
    max_hold: int
    trend_filter: str
    # v2 knobs; the defaults reproduce v1 exactly.
    entry_confirmation: str = "none"
    cooldown_bars: int = 0
    stop_atr: float | None = None

    @classmethod
    def from_config(cls, cfg) -> "MRParams":
        """Accepts a v1 MeanReversionConfig or a v2 MeanReversionV2Config."""
        return cls(cfg.symbol, cfg.timeframe, cfg.mean_type, cfg.mean_lookback, cfg.std_lookback,
                   cfg.entry_z, cfg.exit_z, cfg.max_hold, cfg.trend_filter,
                   getattr(cfg, "entry_confirmation", "none"), getattr(cfg, "cooldown_bars", 0),
                   getattr(cfg, "stop_atr_value", None))


def as_params(cfg) -> MRParams:
    """Normalize a v1/v2 grid config (or MRParams) to MRParams, so every caller
    sees the same attribute names (e.g. a v2 config's `stop_atr_multiple`
    becomes `stop_atr`) and no knob can be silently ignored."""
    return cfg if isinstance(cfg, MRParams) else MRParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray   # bar whose close triggered the exit; stop exits: the stop bar (-1 if forced)
    quantity: np.ndarray
    entry_px: np.ndarray       # entry fill price (after slippage)
    exit_px: np.ndarray        # exit fill price (after slippage)
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray   # True = position still open at end of data, closed at last bar
    exit_reason: np.ndarray    # Z_EXIT / TIME_EXIT / STOP_EXIT / FORCED
    stop_level: np.ndarray     # protective stop price per trade (nan = no stop)


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


def signal_arrays(data: MRData, cfg) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(dip, entry signal, exit signal) booleans per bar, decided at that bar's close."""
    z = data.zscore(cfg.mean_type, cfg.mean_lookback, cfg.std_lookback)
    dip = z <= cfg.entry_z  # NaN -> False
    signal = dip & data.trend_ok(cfg.trend_filter)
    confirm = getattr(cfg, "entry_confirmation", "none")
    if confirm == "positive_bar_return":
        signal = signal & data.positive_bar()
    elif confirm != "none":
        raise ValueError(f"Unknown entry_confirmation {confirm!r}")
    return dip, signal, z >= cfg.exit_z


def _whole_shares(equity: float, px: float, ec: ExecutionConfig) -> int:
    """Most whole shares whose cost plus commission fits in `equity` (no leverage)."""
    if not (px > 0 and math.isfinite(px)):
        return 0
    q = math.floor(equity / px)
    while q > 0 and q * px + _commission(q, ec) > equity:
        q -= 1
    return q


def simulate_mean_reversion(
    data: MRData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off, i.e. the baseline run):
    `entry_delay_bars` fills the entry that many extra bars late; exits are
    still checked from the (delayed) entry bar on.
    `missed_entry_frac` randomly drops that fraction of signal EPISODES (a
    contiguous run of signal bars): the whole episode is skipped, so a missed
    entry is genuinely missed rather than re-taken a bar later. Seeded by
    `stress_seed`. Cost stress is passed via `exec_config` (see
    `scale_variable_costs`).
    """
    cfg = as_params(cfg)
    dip, signal, exit_sig = signal_arrays(data, cfg)
    o, lo, c, ts, n = data.open, data.low, data.close, data.ts, data.n
    ec = exec_config
    stop_mult = getattr(cfg, "stop_atr", None)
    cooldown = getattr(cfg, "cooldown_bars", 0)
    atr = data.atr if stop_mult is not None else None
    next_ok = 0  # earliest bar allowed to signal (cooldown)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    i = 0
    armed = True

    while i < n - 1:  # need bar i+1 to enter
        if not armed:  # re-arm after a time exit once z closes above entry_z
            armed = not dip[i]
            if not armed:
                i += 1
                continue
        if not signal[i] or i < next_ok:
            i += 1
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            while i < n and signal[i]:  # skip the whole signal episode
                i += 1
            continue

        entry_idx = i + 1 + entry_delay_bars
        if entry_idx >= n:
            break
        entry_px_raw = o[entry_idx]
        entry_fill_px = _apply_slippage(entry_px_raw, side="long", action="buy", bps=ec.slippage_bps_market,
                                        extended_hours=False, config=ec)
        stop = float("nan")
        if stop_mult is not None:
            a_known = atr[entry_idx - 1]  # last ATR known before the entry fill
            if not math.isfinite(a_known) or a_known <= 0:
                i += 1  # ATR warm-up: no usable stop -> skip this signal
                continue
            stop = entry_px_raw - stop_mult * a_known
        qty = _whole_shares(equity, entry_fill_px, ec)
        if qty <= 0:
            i += 1
            continue
        seq += 1
        entry_fill = Fill(
            order_id=f"e{seq}", symbol=cfg.symbol, side="long", quantity=qty, fill_price=entry_fill_px,
            fill_ts=ts[entry_idx], commission=_commission(qty, ec),
            slippage_points=abs(entry_fill_px - entry_px_raw), bar_open_ts=ts[entry_idx],
        )

        decision, why = -1, FORCED
        exit_idx = exit_px = None
        for j in range(entry_idx, n - 1):  # z/time exits fill at bar j+1's open
            if lo[j] <= stop:  # stop live from the entry bar; nan stop never triggers
                base = min(o[j], stop)  # a gap through the stop fills at the worse open
                exit_px = _apply_slippage(base, side="long", action="sell", bps=ec.slippage_bps_stop,
                                          extended_hours=False, config=ec)
                decision, why, exit_idx = j, STOP_EXIT, j
                break
            if exit_sig[j]:
                decision, why = j, Z_EXIT
                break
            if j - entry_idx + 1 >= cfg.max_hold:
                decision, why = j, TIME_EXIT
                break
        if why == STOP_EXIT:
            pass
        elif decision >= 0:
            exit_idx = decision + 1
            exit_px = _apply_slippage(o[exit_idx], side="long", action="sell", bps=ec.slippage_bps_market,
                                      extended_hours=False, config=ec)
        else:  # data ended with the position open -> forced close at the last close
            exit_idx = n - 1
            exit_px = _apply_slippage(c[exit_idx], side="long", action="sell", bps=ec.slippage_bps_market,
                                      extended_hours=False, config=ec)
        forced = decision < 0

        exit_fill = Fill(
            order_id=f"x{seq}", symbol=cfg.symbol, side="long", quantity=qty, fill_price=exit_px,
            fill_ts=ts[exit_idx], commission=_commission(qty, ec), slippage_points=0.0, bar_open_ts=ts[exit_idx],
        )
        commissions = entry_fill.commission + exit_fill.commission
        realized = (exit_px - entry_fill_px) * qty - commissions
        reason = {Z_EXIT: ExitReason.TAKE_PROFIT, TIME_EXIT: ExitReason.TIME_EXIT,
                  STOP_EXIT: ExitReason.STOP_LOSS, FORCED: ExitReason.SESSION_EXIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=cfg.symbol, side="long",
            entry_order_id=entry_fill.order_id, entry_fill=entry_fill, quantity=qty,
            stop_price=None if math.isnan(stop) else stop, target_price=None, exit_fill=exit_fill, exit_reason=reason,
            realized_pnl=realized, realized_r=None, commission_total=commissions,
            holding_bars=exit_idx - entry_idx,
        ))
        rows.append((i, entry_idx, exit_idx, decision, qty, entry_fill_px, exit_px, entry_fill.commission,
                     realized, forced, why, stop))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        armed = why != TIME_EXIT
        next_ok = exit_idx + cooldown
        i = exit_idx  # a new signal can form at the exit bar's close (after any cooldown)

    cols = list(zip(*rows)) if rows else [()] * 12
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=np.asarray(cols[0], dtype=np.int64), entry_idx=np.asarray(cols[1], dtype=np.int64),
        exit_idx=np.asarray(cols[2], dtype=np.int64), decision_idx=np.asarray(cols[3], dtype=np.int64),
        quantity=np.asarray(cols[4], dtype=float), entry_px=np.asarray(cols[5], dtype=float),
        exit_px=np.asarray(cols[6], dtype=float), entry_commission=np.asarray(cols[7], dtype=float),
        realized_pnl=np.asarray(cols[8], dtype=float), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=np.asarray(cols[11], dtype=float),
    )
