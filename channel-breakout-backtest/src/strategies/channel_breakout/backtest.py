"""Compact, fast backtester for the channel-breakout family.

Why not the shared simulator: the exit here is a *trailing* Donchian channel
(the lowest low of the last `exit_lookback` bars, which moves every bar),
optionally tightened by a fixed ATR stop. The shared engine resolves a single
fixed stop/target per trade and cannot express a moving stop. This module runs a
one-pass, non-overlapping state machine instead, but reuses the engine's
execution primitives (sizing, slippage, commission) and emits engine `Trade` /
`EquityPoint` objects, so `compute_metrics` and the split analysis are unchanged.

Execution assumptions (audited for the screening funnel's stage 1):
  * long-only, one position at a time (no overlapping trades), compounding equity;
  * a breakout confirmed at bar *i*'s close fills at bar *i+1+delay*'s open;
  * the ATR used for the initial stop / sizing is the last ATR known before the
    entry fill (bar entry-1's close) -- never the entry bar's own ATR, which
    includes that bar's not-yet-seen high/low/close;
  * the stop is live from the ENTRY bar onward: if the entry bar's low touches
    the protective level the trade exits on that bar (conservative: the intrabar
    path is unknown, so we assume the adverse touch happened);
  * a bar that gaps through the stop fills at the (worse) open, otherwise at the
    stop level; adverse slippage + commission on every fill;
  * there is no profit target, so a bar can never touch both stop and target.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.engine.fills import _apply_slippage, _commission
from src.engine.sizing import compute_position_size
from src.features.atr import wilder_atr
from src.strategies.channel_breakout.config import ChannelBreakoutConfig
from src.utils.config_models import ExecutionConfig


class ChannelData:
    """Per-(symbol, timeframe) precomputed arrays. Rolling channels are cached by
    lookback so the same channel isn't recomputed across the thousands of configs
    that share it."""

    def __init__(self, bars: pl.DataFrame, *, atr_period: int = 14) -> None:
        df = wilder_atr(bars.sort("bar_open_ts"), period=atr_period)
        self.ts = df["bar_open_ts"].to_list()
        self.open = df["open"].to_numpy().astype(float)
        self.high = df["high"].to_numpy().astype(float)
        self.low = df["low"].to_numpy().astype(float)
        self.close = df["close"].to_numpy().astype(float)
        self.atr = df["atr"].to_numpy().astype(float)
        self.n = df.height
        # NY session date per bar (datetime64[D]); day_end_idx = last bar of each session.
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
        self._upper: dict[int, np.ndarray] = {}
        self._lower: dict[int, np.ndarray] = {}
        self._ma: dict[str, np.ndarray] = {}

    def entry_upper(self, lookback: int) -> np.ndarray:
        if lookback not in self._upper:
            s = self._df["high"].rolling_max(window_size=lookback).shift(1)
            self._upper[lookback] = s.to_numpy().astype(float)
        return self._upper[lookback]

    def exit_lower(self, lookback: int) -> np.ndarray:
        if lookback not in self._lower:
            s = self._df["low"].rolling_min(window_size=lookback).shift(1)
            self._lower[lookback] = s.to_numpy().astype(float)
        return self._lower[lookback]

    def _sma(self, k: int) -> np.ndarray:
        key = f"sma{k}"
        if key not in self._ma:
            self._ma[key] = self._df["close"].rolling_mean(window_size=k).to_numpy().astype(float)
        return self._ma[key]

    def _ema(self, k: int) -> np.ndarray:
        key = f"ema{k}"
        if key not in self._ma:
            s = self._df["close"].ewm_mean(span=k, adjust=False, min_periods=k)
            self._ma[key] = s.to_numpy().astype(float)
        return self._ma[key]

    def trend_ok(self, trend_filter: str) -> np.ndarray:
        c = self.close
        if trend_filter == "off":
            return np.ones(self.n, dtype=bool)
        if trend_filter.startswith("sma"):
            return c > self._sma(int(trend_filter[3:]))
        if trend_filter == "ema50_gt_ema200":
            return self._ema(50) > self._ema(200)
        if trend_filter.startswith("ema"):
            return c > self._ema(int(trend_filter[3:]))
        raise ValueError(f"Unknown trend_filter {trend_filter!r}")


@dataclass(frozen=True)
class ChannelParams:
    """Free-valued strategy parameters (the grid's ChannelBreakoutConfig restricts
    values to the grid lattice). Used for off-grid parameter perturbations; the
    backtester accepts either type (same attribute names)."""

    symbol: str
    timeframe: str
    entry_lookback: int
    exit_lookback: int
    buffer_atr: float
    init_stop_atr: float | None
    confirm: int
    trend_filter: str

    @classmethod
    def from_config(cls, cfg: ChannelBreakoutConfig) -> "ChannelParams":
        return cls(cfg.symbol, cfg.timeframe, cfg.entry_lookback, cfg.exit_lookback,
                   cfg.buffer_atr, cfg.init_stop_atr, cfg.confirm, cfg.trend_filter)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    quantity: np.ndarray
    entry_px: np.ndarray       # entry fill price (after slippage)
    exit_px: np.ndarray        # exit fill price (after slippage)
    stop_level: np.ndarray     # raw protective level that triggered the exit (nan if forced)
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray   # True = position still open at end of data, closed at last bar


def scale_variable_costs(exec_config: ExecutionConfig, multiplier: float) -> ExecutionConfig:
    """Scale the VARIABLE execution costs (per-share commission, slippage bps)
    by `multiplier`, always starting from the given baseline so stress scenarios
    never compound (1.5x is 1.5x baseline, not 1.5x of an already-stressed run).
    The per-order commission minimum is a fixed cost and is left unchanged."""
    return exec_config.model_copy(update={
        "commission_per_share": exec_config.commission_per_share * multiplier,
        "slippage_bps_market": exec_config.slippage_bps_market * multiplier,
        "slippage_bps_stop": exec_config.slippage_bps_stop * multiplier,
        "slippage_bps_limit_adverse": exec_config.slippage_bps_limit_adverse * multiplier,
    })


def _signal_array(data: ChannelData, cfg) -> np.ndarray:
    """Boolean per-bar long-entry signal (confirmed at that bar's close)."""
    upper = data.entry_upper(cfg.entry_lookback)
    threshold = upper + cfg.buffer_atr * data.atr
    raw = data.close > threshold  # NaN threshold -> False (warmup)
    raw = np.nan_to_num(raw, nan=False).astype(bool)
    if cfg.confirm == 2:
        prev = np.concatenate([[False], raw[:-1]])
        raw = raw & prev
    return raw & data.trend_ok(cfg.trend_filter)


def simulate_channel(
    data: ChannelData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off, i.e. the baseline run):
    `entry_delay_bars` fills the entry that many extra bars late; the order /
    position logic is re-run so later trades shift accordingly.
    `missed_entry_frac` randomly drops that fraction of breakout EPISODES (a
    contiguous run of signal bars): the whole episode is skipped, so a missed
    entry is genuinely missed rather than re-taken one bar later. Reproducibly
    seeded by `stress_seed`. Cost stress is passed via `exec_config`
    (see `scale_variable_costs`).
    """
    signal = _signal_array(data, cfg)
    lower = data.exit_lower(cfg.exit_lookback)
    atr_mult = cfg.init_stop_atr  # None = channel exit only
    o, h, l, c, atr, ts, n = data.open, data.high, data.low, data.close, data.atr, data.ts, data.n
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    i = 0

    def eff_stop(j: int, atr_stop: float | None) -> float:
        lv = lower[j]
        cands = []
        if atr_stop is not None and math.isfinite(atr_stop):
            cands.append(atr_stop)
        if math.isfinite(lv):
            cands.append(lv)
        return max(cands) if cands else float("-inf")

    while i < n - 1:  # need bar i+1 to enter
        if not signal[i]:
            i += 1
            continue

        if rng is not None and rng.random() < missed_entry_frac:
            while i < n and signal[i]:  # skip the whole breakout episode
                i += 1
            continue

        entry_idx = i + 1 + entry_delay_bars
        if entry_idx >= n:
            break
        entry_px_raw = o[entry_idx]
        if not math.isfinite(entry_px_raw):
            i += 1
            continue

        atr_known = atr[entry_idx - 1]  # last ATR known before the entry fill
        atr_stop_level = (
            entry_px_raw - atr_mult * atr_known
            if (atr_mult is not None and math.isfinite(atr_known))
            else None
        )
        protective0 = eff_stop(entry_idx, atr_stop_level)
        if not math.isfinite(protective0) or protective0 >= entry_px_raw:
            i += 1  # no usable protective level -> skip this signal
            continue

        sizing = compute_position_size(
            equity=equity, entry_price=entry_px_raw, stop_price=protective0, config=exec_config
        )
        if not sizing.accepted:
            i += 1
            continue
        qty = sizing.quantity

        seq += 1
        entry_fill_px = _apply_slippage(
            entry_px_raw, side="long", action="buy", bps=exec_config.slippage_bps_market,
            extended_hours=False, config=exec_config,
        )
        entry_fill = Fill(
            order_id=f"e{seq}", symbol=cfg.symbol, side="long", quantity=qty,
            fill_price=entry_fill_px, fill_ts=ts[entry_idx], commission=_commission(qty, exec_config),
            slippage_points=abs(entry_fill_px - entry_px_raw), bar_open_ts=ts[entry_idx],
        )
        risk_per_share = entry_fill_px - protective0

        # Stop is live from the entry bar itself (conservative; see module doc).
        exit_idx = None
        stop_hit = float("nan")
        for j in range(entry_idx, n):
            lv = eff_stop(j, atr_stop_level)
            if math.isfinite(lv) and l[j] <= lv:
                gapped = o[j] < lv
                base = o[j] if gapped else lv
                exit_px = _apply_slippage(
                    base, side="long", action="sell", bps=exec_config.slippage_bps_stop,
                    extended_hours=False, config=exec_config,
                )
                exit_idx = j
                stop_hit = lv
                reason = ExitReason.STOP_LOSS
                break

        forced = exit_idx is None
        if forced:  # data ended with the position open -> forced close at last bar
            j = n - 1
            exit_px = _apply_slippage(
                c[j], side="long", action="sell", bps=exec_config.slippage_bps_market,
                extended_hours=False, config=exec_config,
            )
            exit_idx = j
            reason = ExitReason.SESSION_EXIT

        exit_fill = Fill(
            order_id=f"x{seq}", symbol=cfg.symbol, side="long", quantity=qty,
            fill_price=exit_px, fill_ts=ts[exit_idx], commission=_commission(qty, exec_config),
            slippage_points=0.0, bar_open_ts=ts[exit_idx],
        )
        gross = (exit_px - entry_fill_px) * qty
        commissions = entry_fill.commission + exit_fill.commission
        realized = gross - commissions

        trade = Trade(
            trade_id=f"t{seq}", config_id="", symbol=cfg.symbol, side="long",
            entry_order_id=entry_fill.order_id, entry_fill=entry_fill, quantity=qty,
            stop_price=protective0, target_price=None, exit_fill=exit_fill, exit_reason=reason,
            realized_pnl=realized,
            realized_r=(exit_px - entry_fill_px) / risk_per_share if risk_per_share > 0 else None,
            commission_total=commissions, holding_bars=exit_idx - entry_idx,
        )
        trades.append(trade)
        rows.append((i, entry_idx, exit_idx, qty, entry_fill_px, exit_px, stop_hit,
                     entry_fill.commission, realized, forced))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))

        i = max(exit_idx, i + 1)  # resume signal search at the exit bar

    cols = list(zip(*rows)) if rows else [()] * 10
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=np.asarray(cols[0], dtype=np.int64), entry_idx=np.asarray(cols[1], dtype=np.int64),
        exit_idx=np.asarray(cols[2], dtype=np.int64), quantity=np.asarray(cols[3], dtype=float),
        entry_px=np.asarray(cols[4], dtype=float), exit_px=np.asarray(cols[5], dtype=float),
        stop_level=np.asarray(cols[6], dtype=float), entry_commission=np.asarray(cols[7], dtype=float),
        realized_pnl=np.asarray(cols[8], dtype=float), forced_close=np.asarray(cols[9], dtype=bool),
    )


def run_channel_backtest(
    data: ChannelData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> tuple[list[Trade], list[EquityPoint]]:
    """Back-compatible wrapper returning (trades, exit-point equity curve)."""
    sim = simulate_channel(data, cfg, exec_config=exec_config, starting_equity=starting_equity,
                           entry_delay_bars=entry_delay_bars, missed_entry_frac=missed_entry_frac,
                           stress_seed=stress_seed)
    return sim.trades, sim.equity_curve
