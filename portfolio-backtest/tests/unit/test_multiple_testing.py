"""Bootstrap p-value + BH/BY FDR control."""

from __future__ import annotations

import numpy as np

from src.analysis.multiple_testing import benjamini_hochberg, benjamini_yekutieli, block_bootstrap_pvalue


def test_pvalue_small_for_strong_positive_mean():
    rng = np.random.default_rng(0)
    r = rng.normal(0.02, 0.01, size=60)  # clearly positive mean
    assert block_bootstrap_pvalue(r, n_boot=1000, seed=1) < 0.05


def test_pvalue_one_for_nonpositive_mean():
    assert block_bootstrap_pvalue([-0.01, 0.0, -0.02, 0.01], n_boot=200) == 1.0
    assert block_bootstrap_pvalue([0.0, 0.0], n_boot=200) == 1.0  # too short


def test_bh_rejects_small_pvalues_and_respects_m_total():
    p = [0.001, 0.2, 0.9]
    mask, cut = benjamini_hochberg(p, q=0.05, m_total=3)
    assert mask.tolist() == [True, False, False]
    # With a large full-search family, the same small p no longer passes.
    mask2, _ = benjamini_hochberg(p, q=0.05, m_total=10_000)
    assert mask2.tolist() == [False, False, False]


def test_by_is_stricter_than_bh():
    p = [0.004, 0.01, 0.2]
    bh, _ = benjamini_hochberg(p, q=0.05, m_total=100)
    by, _ = benjamini_yekutieli(p, q=0.05, m_total=100)
    assert int(by.sum()) <= int(bh.sum())
