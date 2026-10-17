"""Donchian breakout strategy, implementing the Strategy protocol
(src/strategies/base.py). Registered as "donchian_breakout".

Deliberately thin: feature computation + signal detection live in signals.py;
this class adapts a signal row into the engine's TradeIntent and otherwise
leans entirely on the shared engine for sizing, fills, exits, and accounting.
"""

from __future__ import annotations

from typing import Any

import polars as pl

from src.engine.events import ExitReason, OrderType
from src.engine.simulator import TradeIntent
from src.strategies.donchian_breakout.config import DonchianBreakoutConfig
from src.strategies.donchian_breakout.signals import generate_signals
from src.strategies.registry import register_strategy
from src.utils.hashing import config_id as compute_config_id


@register_strategy("donchian_breakout")
class DonchianBreakoutStrategy:
    def __init__(self, config: DonchianBreakoutConfig) -> None:
        self.config = config
        self.config_id = compute_config_id(config.model_dump(mode="json"))

    def required_data(self) -> dict[str, Any]:
        return {"symbols": [self.config.symbol], "timeframes": [self.config.timeframe]}

    def validate_config(self) -> None:
        pass  # DonchianBreakoutConfig's pydantic model already enforces consistency

    def compute_features(self, bars: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
        # Feature computation is folded into signal generation (channel/ATR/SMA
        # are all cheap rolling ops); nothing to precompute separately.
        return bars

    def generate_signals(self, features: dict[str, pl.DataFrame]) -> tuple[pl.DataFrame, pl.DataFrame]:
        entry_bars = features[self.config.timeframe]
        return generate_signals(entry_bars, config=self.config, config_id=self.config_id)

    def create_entry_order(self, signal_row: dict) -> TradeIntent | None:
        if signal_row["direction"] not in ("long", "short"):
            return None

        max_holding_bars = signal_row.get("max_holding_bars")
        reason = ExitReason.TIME_EXIT if max_holding_bars is not None else ExitReason.SESSION_EXIT

        return TradeIntent(
            signal_id=signal_row["signal_id"],
            config_id=signal_row["config_id"],
            symbol=signal_row["symbol"],
            side=signal_row["direction"],
            submission_ts=signal_row["submission_ts"],
            stop_price=signal_row["stop_price"],
            entry_order_type=OrderType.MARKET,
            target_price=signal_row["target_price"],
            time_exit_ts=signal_row["time_exit_ts"],
            time_exit_reason=reason,
            window=None,
            max_holding_bars=max_holding_bars,
        )

    def update_trade_state(self, trade: Any, bar: dict) -> Any:
        return trade  # static stops/targets; no dynamic management

    def create_exit_order(self, trade: Any) -> Any:
        return None  # engine resolves stop/target/time-exit

    def serialize_diagnostics(self) -> dict[str, Any]:
        return {"config_id": self.config_id, "config": self.config.model_dump(mode="json")}
