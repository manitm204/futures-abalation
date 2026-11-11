"""Wires the shared feature layer (src/features/*) together using a
SilverBulletConfig's resolved parameters. Returns a dict of named tables:
bars (with atr/window/displacement columns attached), fvgs, swings, levels,
sweeps, mss -- the inputs signals.py needs.
"""

from __future__ import annotations

import polars as pl

from src.data.calendars import TradingCalendar
from src.features.atr import wilder_atr
from src.features.displacement import DisplacementConfig, compute_displacement_flags
from src.features.fvg import FvgConfig, annotate_touches, detect_fvgs
from src.features.liquidity import prior_session_extremes, swing_levels
from src.features.market_structure import MarketStructureConfig, detect_market_structure_shifts
from src.features.sessions import label_windows
from src.features.sweeps import SweepConfig, detect_sweeps
from src.features.swings import SwingConfig, detect_swings
from src.strategies.ict_silver_bullet.config import SilverBulletConfig


def compute_all_features(
    bars: pl.DataFrame, *, config: SilverBulletConfig, calendar: TradingCalendar
) -> dict[str, pl.DataFrame]:
    bars = bars.sort("bar_open_ts")
    bars = wilder_atr(bars, period=config.atr_period)
    bars = label_windows(bars)
    disp_cfg = DisplacementConfig(
        enable_true_range_atr=config.displacement_enable_true_range_atr,
        true_range_atr_threshold=config.displacement_true_range_atr_threshold,
        enable_body_atr=config.displacement_enable_body_atr,
        body_atr_threshold=config.displacement_body_atr_threshold,
    )
    bars = compute_displacement_flags(bars, config=disp_cfg)

    fvg_cfg = FvgConfig(
        timeframe=config.entry_timeframe,
        min_points=config.fvg_min_points,
        min_bps=config.fvg_min_bps,
        min_atr_multiple=config.fvg_min_atr_multiple,
        max_age_bars=config.fvg_max_age_bars,
        entry_rule=config.fvg_entry_rule,
        full_mitigation_invalidates=config.fvg_full_mitigation_invalidates,
        require_entry_within_window=config.fvg_require_entry_within_window,
    )
    fvgs = detect_fvgs(bars, config=fvg_cfg)
    fvgs = annotate_touches(fvgs, bars)

    swing_cfg = SwingConfig(
        left_bars=config.swing_left_bars, right_bars=config.swing_right_bars,
        timeframe=config.entry_timeframe, tie_handling=config.swing_tie_handling,
    )
    swings = detect_swings(bars, config=swing_cfg)

    levels = pl.concat(
        [
            prior_session_extremes(bars, calendar=calendar, timeframe=config.entry_timeframe),
            swing_levels(swings),
        ],
        how="diagonal",
    )

    sweep_cfg = SweepConfig(
        eligible_level_types=config.eligible_level_types,
        k_bars=config.sweep_k_bars,
        min_penetration_points=config.sweep_min_penetration_points,
        min_penetration_atr_multiple=config.sweep_min_penetration_atr_multiple,
        timeframe=config.entry_timeframe,
        allow_repeated_sweeps=config.sweep_allow_repeated,
    )
    sweeps = detect_sweeps(bars, levels, config=sweep_cfg)

    mss_cfg = MarketStructureConfig(
        required=config.require_market_structure_shift,
        break_mode=config.mss_break_mode,
        max_bars_after_sweep=config.mss_max_bars_after_sweep,
    )
    mss = detect_market_structure_shifts(bars, sweeps, swings, config=mss_cfg)

    return {"bars": bars, "fvgs": fvgs, "swings": swings, "levels": levels, "sweeps": sweeps, "mss": mss}
