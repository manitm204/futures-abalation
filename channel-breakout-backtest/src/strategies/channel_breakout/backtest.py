"""Compact, fast backtester for the channel-breakout family.

Why not the shared simulator: the exit here is a *trailing* Donchian channel
(the lowest low of the last `exit_lookback` bars, which moves every bar),
optionally tightened by a fixed ATR stop. The shared engine resolves a single
fixed stop/target per trade and cannot express a moving stop. This module runs a
one-pass, non-overlapping state machine instead, but reuses the engine's
execution primitives (sizing, slippage, commission) and emits engine `Trade` /
`EquityPoint` objects, so `compute_metrics` and the split analysis are unchanged.

Execution assumptions match the shared engine's: long-only; a breakout confirmed
at bar *i*'s close fills at bar *i+1*'s open (next-bar, no look-ahead); risk-based
sizing on the protective level at entry; commission + adverse slippage on every
fill; one position at a time (compounding equity).
"""

from __future__ import annotations

import math

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


def _signal_array(data: ChannelData, cfg: ChannelBreakoutConfig) -> np.ndarray:
    """Boolean per-bar long-entry signal (confirmed at that bar's close)."""
    upper = data.entry_upper(cfg.entry_lookback)
    threshold = upper + cfg.buffer_atr * data.atr
    raw = data.close > threshold  # NaN threshold -> False (warmup)
    raw = np.nan_to_num(raw, nan=False).astype(bool)
    if cfg.confirm == 2:
        prev = np.concatenate([[False], raw[:-1]])
        raw = raw & prev
    return raw & data.trend_ok(cfg.trend_filter)


def run_channel_backtest(
    data: ChannelData,
    cfg: ChannelBreakoutConfig,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> tuple[list[Trade], list[EquityPoint]]:
    """Execution-stress knobs (default off, i.e. the baseline run):
    `entry_delay_bars` fills the entry that many extra bars late (simulating a
    delayed/slower fill); `missed_entry_frac` randomly drops that fraction of
    otherwise-valid signals (simulating missed entries), reproducibly seeded by
    `stress_seed`. Higher costs / adverse fills are passed via `exec_config`
    (commission + slippage bps), so no extra knob is needed for those.
    """
    signal = _signal_array(data, cfg)
    exit_lb = cfg.exit_lookback
    lower = data.exit_lower(exit_lb)
    atr_mult = cfg.init_stop_atr  # None = channel exit only
    o, h, l, c, atr, ts, n = data.open, data.high, data.low, data.close, data.atr, data.ts, data.n
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
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
            i += 1  # simulated missed entry
            continue

        entry_idx = i + 1 + entry_delay_bars
        if entry_idx >= n:
            break
        entry_px_raw = o[entry_idx]
        if not math.isfinite(entry_px_raw):
            i += 1
            continue

        atr_entry = atr[entry_idx] if math.isfinite(atr[entry_idx]) else atr[i]
        atr_stop_level = (
            entry_px_raw - atr_mult * atr_entry
            if (atr_mult is not None and math.isfinite(atr_entry))
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

        # Walk forward for the trailing-channel / ATR stop (checked from entry_idx+1).
        exit_idx = None
        for j in range(entry_idx + 1, n):
            lv = eff_stop(j, atr_stop_level)
            if math.isfinite(lv) and l[j] <= lv:
                gapped = o[j] < lv
                base = o[j] if gapped else lv
                exit_px = _apply_slippage(
                    base, side="long", action="sell", bps=exec_config.slippage_bps_stop,
                    extended_hours=False, config=exec_config,
                )
                exit_idx = j
                reason = ExitReason.STOP_LOSS
                break

        if exit_idx is None:  # data ended with the position open -> forced close at last bar
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
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[exit_idx], cash=equity, position_value=0.0, equity=equity))

        i = exit_idx  # resume signal search after the exit bar

    return trades, equity_curve
