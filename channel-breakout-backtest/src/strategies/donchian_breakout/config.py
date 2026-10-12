"""Typed, validated configuration for the Donchian breakout base strategy.

Every field here is a discrete ablation axis. The full factorial over these
axes is the search space the study enumerates (see src/experiments/grid.py).
The values deliberately map onto the user's framing of "for one parameter there
are a few possibilities" -- e.g. `breakout_price` is literally the
close / wick / typical ("any") price choice for confirming a breakout.

Conditional fields (e.g. `trend_filter_ma_period` only matters when
`trend_filter != "none"`) are enforced by a pydantic model validator rather
than silently ignored or allowed to crash deep in signal generation, mirroring
the convention in src/strategies/ict_silver_bullet/config.py.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

Timeframe = Literal["15min", "1h"]
BreakoutPrice = Literal["close", "wick", "typical"]
TrendFilter = Literal["none", "sma50", "sma200"]
Direction = Literal["both", "long_only"]
StopMode = Literal["atr_1.5", "atr_2.5", "channel_mid"]
TargetMode = Literal["r_1.5", "r_3.0", "none"]
TimeExit = Literal["eod", "max_120min"]

INTERVAL_MINUTES: dict[str, int] = {"15min": 15, "1h": 60}


class DonchianBreakoutConfig(FrozenModel):
    """One variant of the Donchian breakout strategy.

    symbol/timeframe identify the data; the remaining fields are the tunable
    knobs. All are categorical so the search space is a clean finite grid.
    """

    symbol: str
    timeframe: Timeframe = "15min"

    # Channel: breakout above the highest high / below the lowest low of the
    # prior `channel_lookback` bars (the current bar is excluded from the channel).
    channel_lookback: Literal[20, 40, 60] = 20

    # Which price of the just-closed bar must clear the channel to confirm a
    # breakout. "close" = bar close, "wick" = bar high (long)/low (short),
    # "typical" = (high+low+close)/3 (the "any/other price" option).
    breakout_price: BreakoutPrice = "close"

    # Regime filter: only take longs when close > SMA(n), shorts when close < SMA(n).
    trend_filter: TrendFilter = "none"

    # Whether shorts are allowed at all.
    direction: Direction = "both"

    # Stop placement. atr_* = k * ATR(atr_period) from entry; channel_mid =
    # midpoint of the opposing channel at signal time.
    stop: StopMode = "atr_1.5"

    # Profit target. r_x = x * (entry - stop) risk distance; "none" = no target
    # (exit only on stop, time-exit, opposite breakout, or end of data).
    target: TargetMode = "r_1.5"

    # Intraday-only: every position is closed by the session close in BOTH modes
    # (never held across the overnight gap, which RTH-only data cannot see).
    # eod = hold until the session close; max_120min = additionally cap the hold
    # at 120 minutes (whichever comes first).
    time_exit: TimeExit = "eod"

    atr_period: int = 14

    # --- Derived, non-ablated accessors (not part of the grid) ---

    @property
    def stop_atr_multiple(self) -> float | None:
        return {"atr_1.5": 1.5, "atr_2.5": 2.5, "channel_mid": None}[self.stop]

    @property
    def target_r_multiple(self) -> float | None:
        return {"r_1.5": 1.5, "r_3.0": 3.0, "none": None}[self.target]

    @property
    def trend_filter_ma_period(self) -> int | None:
        return {"none": None, "sma50": 50, "sma200": 200}[self.trend_filter]

    @property
    def max_holding_bars(self) -> int | None:
        if self.time_exit != "max_120min":
            return None
        return max(1, 120 // INTERVAL_MINUTES[self.timeframe])

    @property
    def allow_short(self) -> bool:
        return self.direction == "both"
