"""Stop and target price resolution for a Silver Bullet signal.

A stop must be logically beyond the entry in the correct direction; invalid
geometry is rejected (returns None) rather than silently corrected -- the
caller (signals.py) turns a None into a recorded rejection reason.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.strategies.ict_silver_bullet.config import SilverBulletConfig


@dataclass(frozen=True)
class ExitContext:
    direction: str  # "bullish" | "bearish" -- FVG direction, maps to long/short
    entry_price: float
    fvg_distal: float
    fvg_proximal: float
    swept_extreme: float | None
    mss_reference_price: float | None
    atr: float | None
    opposing_level_price: float | None  # nearest available opposing liquidity level, for target_type="liquidity"


def resolve_stop(config: SilverBulletConfig, ctx: ExitContext) -> float | None:
    is_long = ctx.direction == "bullish"
    buffer = config.stop_buffer_points

    if config.stop_type == "swing":
        base = ctx.mss_reference_price
        if base is None:
            return None
    elif config.stop_type == "fvg_distal":
        base = ctx.fvg_distal
    elif config.stop_type == "swept_extreme":
        if ctx.swept_extreme is None:
            return None
        base = ctx.swept_extreme
    elif config.stop_type == "fixed_points":
        assert config.stop_fixed_points is not None
        return ctx.entry_price - config.stop_fixed_points if is_long else ctx.entry_price + config.stop_fixed_points
    elif config.stop_type == "atr_multiple":
        if ctx.atr is None:
            return None
        assert config.stop_atr_multiple is not None
        dist = ctx.atr * config.stop_atr_multiple
        return ctx.entry_price - dist if is_long else ctx.entry_price + dist
    else:
        raise ValueError(f"Unsupported stop_type: {config.stop_type}")

    stop = (base - buffer) if is_long else (base + buffer)
    return stop


def resolve_target(config: SilverBulletConfig, ctx: ExitContext, *, stop_price: float | None) -> float | None:
    """Returns None for target_type values that are time-based (end_of_window,
    end_of_session, max_holding_time) -- those exits are handled via
    TradeIntent.time_exit_ts, not a price target."""
    is_long = ctx.direction == "bullish"

    if config.target_type in ("end_of_window", "end_of_session", "max_holding_time"):
        return None
    if config.target_type == "r_multiple":
        if stop_price is None:
            return None
        assert config.target_r_multiple is not None
        risk = abs(ctx.entry_price - stop_price)
        return ctx.entry_price + risk * config.target_r_multiple if is_long else ctx.entry_price - risk * config.target_r_multiple
    if config.target_type == "fixed_points":
        assert config.target_fixed_points is not None
        return ctx.entry_price + config.target_fixed_points if is_long else ctx.entry_price - config.target_fixed_points
    if config.target_type == "liquidity":
        return ctx.opposing_level_price  # None if no known opposing level -- caller rejects

    raise ValueError(f"Unsupported target_type: {config.target_type}")


def validate_stop_geometry(direction: str, entry_price: float, stop_price: float) -> bool:
    is_long = direction == "bullish"
    return (stop_price < entry_price) if is_long else (stop_price > entry_price)
