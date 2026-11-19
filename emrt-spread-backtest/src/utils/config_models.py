"""Base pydantic config models shared across data/execution/strategy/experiment configs.

Concrete configs (e.g. Silver Bullet strategy config in
src/strategies/ict_silver_bullet/config.py) subclass these. Keeping the base
models here (rather than duplicated per layer) is what lets a new strategy's
config plug into hashing/serialization/experiment-space code without changes
to those layers.
"""

from __future__ import annotations

from datetime import time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    """Base for all config models: immutable, extra fields forbidden (fail loudly on typos)."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class SilverBulletWindow(FrozenModel):
    name: Literal["london", "ny_am", "ny_pm"]
    start: time
    end: time  # half-open: [start, end)

    @model_validator(mode="after")
    def _check_order(self) -> "SilverBulletWindow":
        if self.start >= self.end:
            raise ValueError(f"window {self.name}: start {self.start} must be < end {self.end}")
        return self


DEFAULT_SILVER_BULLET_WINDOWS: tuple[SilverBulletWindow, ...] = (
    SilverBulletWindow(name="london", start=time(3, 0), end=time(4, 0)),
    SilverBulletWindow(name="ny_am", start=time(10, 0), end=time(11, 0)),
    SilverBulletWindow(name="ny_pm", start=time(14, 0), end=time(15, 0)),
)


class ExecutionConfig(FrozenModel):
    starting_equity: float = Field(default=100_000.0, gt=0)
    risk_per_trade_pct: float = Field(default=0.0025, gt=0, le=0.05)
    max_open_positions_per_symbol: int = Field(default=1, ge=1, le=1)
    allow_pyramiding: bool = False
    allow_overlapping_trades: bool = False
    allow_short: bool = True
    fractional_shares: bool = False
    leverage: float = Field(default=1.0, ge=1.0, le=1.0)

    commission_per_share: float = Field(default=0.005, ge=0)
    commission_minimum: float = Field(default=1.00, ge=0)
    slippage_bps_market: float = Field(default=1.0, ge=0)
    slippage_bps_stop: float = Field(default=1.0, ge=0)
    slippage_bps_limit_adverse: float = Field(default=0.0, ge=0)
    extended_hours_slippage_multiplier: float = Field(default=2.0, ge=1.0)
    include_sec_finra_fees: bool = False

    intrabar_collision_mode: Literal["stop_first", "target_first", "discard_ambiguous"] = "stop_first"

    # Futures (instrument_type = "futures"): quantity is whole contracts sized so
    # contract value (raw price x multiplier, from src/data/futures.py) fits in
    # equity; slippage is in ticks and commission per contract per fill. The
    # per-share / bps fields above are then unused.
    instrument_type: Literal["equity", "futures"] = "equity"
    commission_per_contract: float = Field(default=0.0, ge=0)
    slippage_ticks_market: float = Field(default=0.0, ge=0)
    slippage_ticks_stop: float = Field(default=0.0, ge=0)


DEFAULT_EXECUTION_CONFIG = ExecutionConfig()
