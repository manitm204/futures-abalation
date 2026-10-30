from datetime import date

from src.experiments.walk_forward import aggregate_out_of_sample_trades, build_folds, run_walk_forward


def test_expanding_folds_train_start_stays_fixed() -> None:
    folds = build_folds(
        overall_start=date(2018, 1, 1), overall_end=date(2020, 1, 1),
        train_months=12, test_months=3, mode="expanding",
    )
    assert len(folds) > 1
    assert all(f.train_start == date(2018, 1, 1) for f in folds)


def test_expanding_folds_train_end_grows() -> None:
    folds = build_folds(
        overall_start=date(2018, 1, 1), overall_end=date(2020, 1, 1),
        train_months=12, test_months=3, mode="expanding",
    )
    train_ends = [f.train_end for f in folds]
    assert train_ends == sorted(train_ends)
    assert len(set(train_ends)) == len(train_ends)  # strictly increasing


def test_rolling_folds_train_length_constant() -> None:
    folds = build_folds(
        overall_start=date(2018, 1, 1), overall_end=date(2020, 1, 1),
        train_months=12, test_months=3, mode="rolling",
    )
    for f in folds:
        approx_months = (f.train_end.year - f.train_start.year) * 12 + (f.train_end.month - f.train_start.month)
        assert approx_months == 12


def test_folds_never_overlap_train_and_test() -> None:
    folds = build_folds(
        overall_start=date(2018, 1, 1), overall_end=date(2022, 1, 1),
        train_months=6, test_months=2, mode="expanding",
    )
    for f in folds:
        assert f.train_end <= f.test_start


def test_folds_test_windows_are_sequential_non_overlapping() -> None:
    folds = build_folds(
        overall_start=date(2018, 1, 1), overall_end=date(2020, 1, 1),
        train_months=12, test_months=3, mode="expanding",
    )
    for i in range(1, len(folds)):
        assert folds[i].test_start >= folds[i - 1].test_end


def test_run_walk_forward_never_lets_selection_see_test_data() -> None:
    """Selection function only receives the fold object (train/test date
    boundaries), never the test-period data itself -- the causality boundary is
    enforced by what the caller's select_fn implementation is given access to."""
    folds = build_folds(overall_start=date(2018, 1, 1), overall_end=date(2019, 1, 1), train_months=6, test_months=3)

    seen_test_starts_during_selection = []

    def select_fn(fold):
        # A correctly-implemented select_fn would only look at [train_start, train_end)
        # data, which this test doesn't have access to -- it just verifies the fold
        # boundaries handed to select_fn are self-consistent (train precedes test).
        assert fold.train_end <= fold.test_start
        return f"selected_for_fold_{fold.fold_index}"

    def evaluate_fn(fold, config_id):
        return [f"trade_from_fold_{fold.fold_index}_{config_id}"]

    results = run_walk_forward(folds, select_fn=select_fn, evaluate_fn=evaluate_fn)
    assert len(results) == len(folds)
    all_trades = aggregate_out_of_sample_trades(results)
    assert len(all_trades) == len(folds)


def test_aggregate_out_of_sample_trades_pools_across_folds() -> None:
    from src.experiments.walk_forward import WalkForwardFold, WalkForwardResult

    f1 = WalkForwardFold(0, date(2018, 1, 1), date(2018, 6, 1), date(2018, 6, 1), date(2018, 9, 1))
    f2 = WalkForwardFold(1, date(2018, 1, 1), date(2018, 9, 1), date(2018, 9, 1), date(2018, 12, 1))
    results = [
        WalkForwardResult(fold=f1, selected_config_id="c1", out_of_sample_trades=["t1", "t2"]),
        WalkForwardResult(fold=f2, selected_config_id="c2", out_of_sample_trades=["t3"]),
    ]
    pooled = aggregate_out_of_sample_trades(results)
    assert pooled == ["t1", "t2", "t3"]
