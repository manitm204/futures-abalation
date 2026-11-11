import pytest

from src.analysis.parameter_analysis import categorical_enrichment, numeric_distribution_comparison


def _result(stop_type: str, target_r: float) -> dict:
    return {"config": {"stop_type": stop_type, "target_r_multiple": target_r}}


def test_enrichment_ratio_above_one_when_overrepresented_in_top() -> None:
    # baseline: 50/50 split between "swing" and "fvg_distal"
    all_results = [_result("swing", 1.0)] * 50 + [_result("fvg_distal", 1.0)] * 50
    # top: entirely "swing" -- should show enrichment ratio of 2.0 (100% vs 50% baseline)
    top_results = [_result("swing", 1.0)] * 10
    rows = categorical_enrichment(all_results, top_results, param="stop_type")
    swing_row = next(r for r in rows if r.value == "swing")
    assert swing_row.baseline_frequency == pytest.approx(0.5)
    assert swing_row.top_n_frequency == pytest.approx(1.0)
    assert swing_row.enrichment_ratio == pytest.approx(2.0)


def test_enrichment_ratio_below_one_when_underrepresented() -> None:
    all_results = [_result("swing", 1.0)] * 50 + [_result("fvg_distal", 1.0)] * 50
    top_results = [_result("fvg_distal", 1.0)] * 10
    rows = categorical_enrichment(all_results, top_results, param="stop_type")
    swing_row = next(r for r in rows if r.value == "swing")
    assert swing_row.enrichment_ratio == pytest.approx(0.0)


def test_enrichment_ratio_near_one_when_representative() -> None:
    all_results = [_result("swing", 1.0)] * 50 + [_result("fvg_distal", 1.0)] * 50
    top_results = [_result("swing", 1.0)] * 5 + [_result("fvg_distal", 1.0)] * 5
    rows = categorical_enrichment(all_results, top_results, param="stop_type")
    for r in rows:
        assert r.enrichment_ratio == pytest.approx(1.0)


def test_enrichment_sorted_descending_by_ratio() -> None:
    all_results = [_result("a", 1.0)] * 50 + [_result("b", 1.0)] * 50
    top_results = [_result("b", 1.0)] * 10
    rows = categorical_enrichment(all_results, top_results, param="stop_type")
    assert rows[0].value == "b"


def test_numeric_distribution_comparison_medians() -> None:
    all_results = [_result("swing", float(i)) for i in range(100)]
    top_results = [_result("swing", float(i)) for i in range(90, 100)]  # skewed high
    comp = numeric_distribution_comparison(all_results, top_results, param="target_r_multiple")
    assert comp.baseline_median == pytest.approx(49.5)
    assert comp.top_n_median > comp.baseline_median


def test_numeric_distribution_comparison_empty_returns_none() -> None:
    comp = numeric_distribution_comparison([], [], param="target_r_multiple")
    assert comp is None
