"""Typed conditional parameter search space for the ICT Silver Bullet strategy.

Each dimension is declared with its type and allowed values/range. Conditional
constraints (e.g. target_r_multiple only meaningful when target_type ==
"r_multiple") are NOT re-implemented here -- they're already enforced by
SilverBulletConfig's pydantic validators. The sampler builds a raw parameter
dict, constructs a SilverBulletConfig from it, and lets construction fail
(caught, not silently discarded) for combinations that don't make sense, e.g.
supplying target_r_multiple when target_type == "fixed_points" is harmless
(the field is just unused), but omitting a required conditional field raises --
the sampler always supplies every field with a value so this only matters for
the *raw values assigned*, not missing fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Kind = Literal["categorical", "int_range", "float_range"]


@dataclass(frozen=True)
class Dimension:
    name: str
    kind: Kind
    choices: tuple[Any, ...] | None = None  # categorical
    low: float | None = None  # int_range / float_range
    high: float | None = None


@dataclass(frozen=True)
class SearchSpace:
    dimensions: tuple[Dimension, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        names = [d.name for d in self.dimensions]
        if len(names) != len(set(names)):
            raise ValueError(f"Duplicate dimension names in search space: {names}")

    def get(self, name: str) -> Dimension:
        for d in self.dimensions:
            if d.name == name:
                return d
        raise KeyError(f"No such dimension: {name!r}")


# The default space for the initial SPY/QQQ Silver Bullet study. Symbol and
# window set are NOT independently optimized per-window (per spec: windows are
# a categorical comparison recorded on every trade, not tuned); every sampled
# config trades ALL configured windows so window performance can be compared
# post-hoc, not selected for during sampling.
DEFAULT_SILVER_BULLET_SPACE = SearchSpace(
    dimensions=(
        Dimension("symbol", "categorical", choices=("SPY", "QQQ")),
        Dimension("entry_timeframe", "categorical", choices=("1min", "5min")),

        Dimension("fvg_min_points", "float_range", low=0.0, high=0.5),
        Dimension("fvg_min_atr_multiple", "float_range", low=0.0, high=1.0),
        Dimension("fvg_max_age_bars", "int_range", low=5, high=60),
        Dimension("fvg_entry_rule", "categorical", choices=("proximal", "midpoint", "distal")),

        Dimension("swing_left_bars", "int_range", low=2, high=10),
        Dimension("swing_right_bars", "int_range", low=2, high=10),

        Dimension("sweep_k_bars", "int_range", low=1, high=8),
        Dimension("sweep_min_penetration_atr_multiple", "float_range", low=0.0, high=0.5),

        Dimension("displacement_true_range_atr_threshold", "float_range", low=1.0, high=3.0),

        Dimension("require_market_structure_shift", "categorical", choices=(True, False)),
        Dimension("mss_max_bars_after_sweep", "int_range", low=5, high=30),

        # bias_mode restricted to "none" for now: daily-bar-dependent modes
        # (prior_daily_direction, price_vs_daily_ma20, etc.) are implemented and
        # unit-tested in src/features/bias.py, but daily-bar ingestion/normalization
        # is not yet wired into the data or strategy layers (see ASSUMPTIONS.md).
        # Sampling those modes here would waste search budget on configs that can
        # only ever resolve to a "bias_unresolvable" rejection. Re-enable once
        # daily data is available end-to-end.
        Dimension("bias_mode", "categorical", choices=("none",)),

        Dimension("stop_type", "categorical", choices=("swing", "fvg_distal", "swept_extreme")),
        Dimension("stop_buffer_points", "float_range", low=0.0, high=0.3),

        Dimension("target_type", "categorical", choices=("r_multiple", "end_of_window")),
        Dimension("target_r_multiple", "float_range", low=1.0, high=4.0),
    )
)
