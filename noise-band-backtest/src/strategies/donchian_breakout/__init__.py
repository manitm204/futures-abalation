"""Donchian channel breakout strategy -- the base strategy for the ablation study.

A deliberately simple, legible trend-following breakout whose parameters form a
small set of discrete, orthogonal axes (see config.py). The ablation study
(src/experiments/grid.py) enumerates the full factorial of those axes and the
report ranks the variants out-of-sample.
"""

from src.strategies.donchian_breakout.strategy import DonchianBreakoutStrategy  # noqa: F401
