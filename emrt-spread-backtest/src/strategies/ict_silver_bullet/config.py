"""Typed, validated configuration for the ICT Silver Bullet strategy.

Conditional validation: fields that only apply to a specific choice (e.g.
target_r_multiple only when target_type == "r_multiple") are enforced via a
model validator, not left to be silently ignored or to crash deep in signal
generation.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from src.utils.config_models import FrozenModel

StopType = Literal["swing", "fvg_distal", "swept_extreme", "fixed_points", "atr_multiple"]
TargetType = Literal["r_multiple", "liquidity", "fixed_points", "end_of_window", "end_of_session", "max_holding_time"]
FvgEntryRule = Literal["proximal", "midpoint", "distal", "first_touch"]
TieHandling = Literal["first", "last", "reject"]
BreakMode = Literal["wick", "close"]
BiasMode = Literal["none", "prior_daily_direction", "prior_day_close_vs_open", "hourly_swing_structure", "daily_ma20_slope", "price_vs_daily_ma20"]

# London excluded by default: FMP's intraday endpoint has no pre-market coverage
# (see ASSUMPTIONS.md). The window definition itself stays available for a future
# data source; it is simply not selectable in this study's default config.
TRADABLE_WINDOWS: tuple[str, ...] = ("ny_am", "ny_pm")


class SilverBulletConfig(FrozenModel):
    symbol: str
    entry_timeframe: Literal["1min", "5min", "15min"] = "1min"
    windows: tuple[str, ...] = TRADABLE_WINDOWS

    # FVG
    fvg_min_points: float = 0.0
    fvg_min_bps: float = 0.0
    fvg_min_atr_multiple: float = 0.0
    fvg_max_age_bars: int | None = 30
    fvg_entry_rule: FvgEntryRule = "midpoint"
    fvg_full_mitigation_invalidates: bool = True
    fvg_require_entry_within_window: bool = True

    # Swings / liquidity / sweeps
    swing_left_bars: int = 5
    swing_right_bars: int = 5
    swing_tie_handling: TieHandling = "reject"
    eligible_level_types: tuple[str, ...] = ("prior_session_low", "prior_session_high", "swing_low", "swing_high")
    sweep_k_bars: int = 3
    sweep_min_penetration_points: float = 0.0
    sweep_min_penetration_atr_multiple: float = 0.0
    sweep_allow_repeated: bool = False

    # Displacement (independently toggleable, never combined into a score)
    displacement_enable_true_range_atr: bool = True
    displacement_true_range_atr_threshold: float = 1.5
    displacement_enable_body_atr: bool = False
    displacement_body_atr_threshold: float = 1.0

    # Market structure
    require_market_structure_shift: bool = True
    mss_break_mode: BreakMode = "close"
    mss_max_bars_after_sweep: int = 15

    # Higher-timeframe bias
    bias_mode: BiasMode = "none"

    # Stops
    stop_type: StopType = "swing"
    stop_buffer_points: float = 0.0
    stop_atr_multiple: float | None = None
    stop_fixed_points: float | None = None

    # Targets
    target_type: TargetType = "r_multiple"
    target_r_multiple: float | None = 2.0
    target_fixed_points: float | None = None

    max_holding_minutes: int | None = None
    atr_period: int = 14

    @model_validator(mode="after")
    def _validate_conditional_fields(self) -> "SilverBulletConfig":
        if not set(self.windows) <= set(TRADABLE_WINDOWS):
            unsupported = set(self.windows) - set(TRADABLE_WINDOWS)
            raise ValueError(
                f"windows contains unsupported/untestable value(s) {unsupported}. "
                f"Only {TRADABLE_WINDOWS} have data coverage (see ASSUMPTIONS.md re: London)."
            )
        if self.target_type == "r_multiple" and self.target_r_multiple is None:
            raise ValueError("target_r_multiple is required when target_type == 'r_multiple'")
        if self.target_type == "fixed_points" and self.target_fixed_points is None:
            raise ValueError("target_fixed_points is required when target_type == 'fixed_points'")
        if self.stop_type == "atr_multiple" and self.stop_atr_multiple is None:
            raise ValueError("stop_atr_multiple is required when stop_type == 'atr_multiple'")
        if self.stop_type == "fixed_points" and self.stop_fixed_points is None:
            raise ValueError("stop_fixed_points is required when stop_type == 'fixed_points'")
        if self.target_type == "max_holding_time" and self.max_holding_minutes is None:
            raise ValueError("max_holding_minutes is required when target_type == 'max_holding_time'")
        return self
