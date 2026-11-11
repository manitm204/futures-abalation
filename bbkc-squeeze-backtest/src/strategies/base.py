"""Strategy protocol. The engine (src/engine/*) depends only on this interface
plus the TradeIntent it produces -- adding a new strategy never requires
touching the data, portfolio, execution, experiment, or analytics layers.
"""

from __future__ import annotations

from typing import Any, Protocol

import polars as pl

from src.engine.simulator import TradeIntent


class Strategy(Protocol):
    """A strategy turns bar data into TradeIntents. Everything upstream of
    `generate_signals` (feature computation) and downstream of
    `create_entry_order`/`create_exit_order` (fill simulation, portfolio
    accounting) is shared engine code the strategy never touches directly.
    """

    def required_data(self) -> dict[str, Any]:
        """Symbols, timeframes, and any auxiliary data (e.g. daily bars for
        bias) this strategy needs loaded before it can run."""
        ...

    def validate_config(self) -> None:
        """Raise if the strategy's own configuration is internally inconsistent.
        Called once before any data processing."""
        ...

    def compute_features(self, bars: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
        """Attach strategy-specific feature columns (ATR, displacement, window
        labels, ...) to the relevant timeframe(s)' bar frames."""
        ...

    def generate_signals(self, features: dict[str, pl.DataFrame]) -> tuple[pl.DataFrame, pl.DataFrame]:
        """Returns (signals, rejected_setups) tables. A detected setup is not
        automatically a filled trade -- signals still go through order creation
        and fill simulation in the engine."""
        ...

    def create_entry_order(self, signal_row: dict) -> TradeIntent | None:
        """Turn one signal row into a TradeIntent (or None if it should be
        skipped without even attempting an order)."""
        ...

    def update_trade_state(self, trade: Any, bar: dict) -> Any:
        """Optional hook for strategies with dynamic exit management (e.g.
        trailing stops) -- Silver Bullet's exits are static, so this is a
        passthrough for now."""
        ...

    def create_exit_order(self, trade: Any) -> Any:
        """Optional hook mirroring create_entry_order for strategies that need
        custom exit-order construction beyond stop/target/time-exit."""
        ...

    def serialize_diagnostics(self) -> dict[str, Any]:
        """Strategy-specific diagnostic payload for the run manifest."""
        ...
