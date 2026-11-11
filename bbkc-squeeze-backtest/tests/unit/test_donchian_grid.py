"""The ablation grid is the full factorial, deterministic, and de-duplicated."""

from __future__ import annotations

from src.experiments.grid import AXES, donchian_grid, variants_per_symbol


def test_grid_size_is_full_factorial():
    expected = 1
    for vals in AXES.values():
        expected *= len(vals)
    assert variants_per_symbol() == expected
    g = donchian_grid(("SPY", "QQQ"))
    assert len(g) == expected * 2


def test_config_ids_unique_and_deterministic():
    g1 = donchian_grid(("SPY", "QQQ"))
    g2 = donchian_grid(("SPY", "QQQ"))
    ids1 = [x.config_id for x in g1]
    assert len(set(ids1)) == len(ids1)
    assert ids1 == [x.config_id for x in g2]  # same order, same ids every run


def test_every_axis_value_appears():
    g = donchian_grid(("SPY",))
    for axis, vals in AXES.items():
        seen = {getattr(x.config, axis) for x in g}
        assert set(vals) <= seen
