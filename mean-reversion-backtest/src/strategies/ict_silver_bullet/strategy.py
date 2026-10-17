"""ICT Silver Bullet strategy, implementing the Strategy protocol
(src/strategies/base.py). Registered as "ict_silver_bullet".
"""

from __future__ import annotations

from typing import Any

import polars as pl

from src.data.calendars import TradingCalendar
from src.engine.events import ExitReason, OrderType
from src.engine.simulator import TradeIntent
from src.strategies.ict_silver_bullet.config import SilverBulletConfig
from src.strategies.ict_silver_bullet.features import compute_all_features
from src.strategies.ict_silver_bullet.signals import generate_signals
from src.strategies.registry import register_strategy
from src.utils.hashing import config_id as compute_config_id


@register_strategy("ict_silver_bullet")
class SilverBulletStrategy:
    def __init__(self, config: SilverBulletConfig) -> None:
        self.config = config
        self.config_id = compute_config_id(config.model_dump(mode="json"))
        self._calendar = TradingCalendar()
        self._features: dict[str, pl.DataFrame] | None = None

    def required_data(self) -> dict[str, Any]:
        return {"symbols": [self.config.symbol], "timeframes": [self.config.entry_timeframe]}

    def validate_config(self) -> None:
        pass  # SilverBulletConfig's pydantic validators already enforce consistency

    def compute_features(self, bars: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
        entry_bars = bars[self.config.entry_timeframe]
        self._features = compute_all_features(entry_bars, config=self.config, calendar=self._calendar)
        return self._features

    def generate_signals(self, features: dict[str, pl.DataFrame]) -> tuple[pl.DataFrame, pl.DataFrame]:
        return generate_signals(features, config=self.config, config_id=self.config_id)

    def create_entry_order(self, signal_row: dict) -> TradeIntent | None:
        if signal_row["direction"] not in ("long", "short"):
            return None

        time_exit_reason = ExitReason.WINDOW_EXIT
        max_holding_bars = None
        if self.config.target_type == "max_holding_time":
            interval_min = {"1min": 1, "5min": 5, "15min": 15}[self.config.entry_timeframe]
            max_holding_bars = max(1, self.config.max_holding_minutes // interval_min)
        elif self.config.target_type == "end_of_session":
            time_exit_reason = ExitReason.SESSION_EXIT

        return TradeIntent(
            signal_id=signal_row["signal_id"],
            config_id=signal_row["config_id"],
            symbol=signal_row["symbol"],
            side=signal_row["direction"],
            submission_ts=signal_row["earliest_entry_ts"],
            stop_price=signal_row["stop_price"],
            entry_order_type=OrderType.MARKET if signal_row["entry_order_type"] == "market" else OrderType.LIMIT,
            entry_limit_price=signal_row["entry_price"],
            entry_expiration_ts=signal_row["entry_expiration_ts"],
            target_price=signal_row["target_price"],
            time_exit_ts=signal_row["entry_expiration_ts"] if self.config.target_type in ("end_of_window", "end_of_session") else None,
            time_exit_reason=time_exit_reason,
            window=signal_row["window"],
            max_holding_bars=max_holding_bars,
        )

    def update_trade_state(self, trade: Any, bar: dict) -> Any:
        return trade  # Silver Bullet uses static stops/targets; no dynamic management

    def create_exit_order(self, trade: Any) -> Any:
        return None  # handled entirely by the engine's stop/target/time-exit resolution

    def serialize_diagnostics(self) -> dict[str, Any]:
        return {"config_id": self.config_id, "config": self.config.model_dump(mode="json")}
