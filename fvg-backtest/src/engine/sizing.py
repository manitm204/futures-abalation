"""Risk-based position sizing.

quantity = floor( (equity * risk_pct) / stop_distance ), whole shares only unless
fractional_shares is enabled. Stop distance must be strictly positive and
finite; zero/invalid stop distance is a rejection, never silently corrected.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from src.utils.config_models import ExecutionConfig


@dataclass(frozen=True)
class SizingResult:
    accepted: bool
    quantity: int
    rejection_reason: str | None = None
    risk_amount: float | None = None
    stop_distance: float | None = None


def compute_position_size(
    *, equity: float, entry_price: float, stop_price: float, config: ExecutionConfig
) -> SizingResult:
    stop_distance = abs(entry_price - stop_price)

    if stop_distance <= 0 or not math.isfinite(stop_distance):
        return SizingResult(accepted=False, quantity=0, rejection_reason="invalid_stop_distance")

    if entry_price <= 0 or not math.isfinite(entry_price):
        return SizingResult(accepted=False, quantity=0, rejection_reason="invalid_entry_price")

    risk_amount = equity * config.risk_per_trade_pct
    raw_quantity = risk_amount / stop_distance

    if config.fractional_shares:
        quantity = raw_quantity
    else:
        quantity = math.floor(raw_quantity)

    if quantity <= 0:
        return SizingResult(
            accepted=False, quantity=0, rejection_reason="quantity_rounds_to_zero",
            risk_amount=risk_amount, stop_distance=stop_distance,
        )

    notional = quantity * entry_price
    if not config.leverage or config.leverage <= 1.0:
        max_notional = equity
        if notional > max_notional:
            if config.fractional_shares:
                quantity = max_notional / entry_price
            else:
                quantity = math.floor(max_notional / entry_price)
            if quantity <= 0:
                return SizingResult(
                    accepted=False, quantity=0, rejection_reason="insufficient_buying_power",
                    risk_amount=risk_amount, stop_distance=stop_distance,
                )

    return SizingResult(
        accepted=True,
        quantity=int(quantity) if not config.fractional_shares else quantity,
        risk_amount=risk_amount,
        stop_distance=stop_distance,
    )
