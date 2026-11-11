"""Walk-forward evaluation: rank/select on a rolling or expanding historical
window, evaluate ONLY on the next untouched period, advance, and aggregate
out-of-sample trades across all folds. Selection never sees its own
evaluation period -- enforced by construction (each fold's train window ends
strictly before its test window begins).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Literal

WindowMode = Literal["rolling", "expanding"]


@dataclass(frozen=True)
class WalkForwardFold:
    fold_index: int
    train_start: date
    train_end: date
    test_start: date
    test_end: date


def build_folds(
    *,
    overall_start: date,
    overall_end: date,
    train_months: int,
    test_months: int,
    mode: WindowMode = "expanding",
) -> list[WalkForwardFold]:
    """Builds non-overlapping test windows walking forward from `overall_start`.
    In "expanding" mode, each fold's train_start stays fixed at overall_start
    (train window grows). In "rolling" mode, train_start advances with the fold
    so the train window has constant length `train_months`.
    """
    folds: list[WalkForwardFold] = []
    fold_idx = 0

    train_end = _add_months(overall_start, train_months)
    while True:
        test_start = train_end
        test_end = _add_months(test_start, test_months)
        if test_start >= overall_end:
            break
        test_end = min(test_end, overall_end)

        train_start = overall_start if mode == "expanding" else _add_months(train_end, -train_months)
        folds.append(
            WalkForwardFold(
                fold_index=fold_idx, train_start=train_start, train_end=train_end,
                test_start=test_start, test_end=test_end,
            )
        )
        fold_idx += 1
        train_end = _add_months(train_end, test_months)
        if test_end >= overall_end:
            break

    return folds


def _add_months(d: date, months: int) -> date:
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    import calendar as _cal

    day = min(d.day, _cal.monthrange(year, month)[1])
    return date(year, month, day)


@dataclass
class WalkForwardResult:
    fold: WalkForwardFold
    selected_config_id: str | None
    out_of_sample_trades: list  # engine Trade objects from the test window only


def run_walk_forward(
    folds: list[WalkForwardFold],
    *,
    select_fn: Callable[[WalkForwardFold], str | None],
    evaluate_fn: Callable[[WalkForwardFold, str], list],
) -> list[WalkForwardResult]:
    """`select_fn(fold)` must rank/select using ONLY data in
    [fold.train_start, fold.train_end) -- this module does not enforce that
    internally (it doesn't have access to the data), so the caller's select_fn
    implementation is the actual causality boundary. `evaluate_fn(fold, config_id)`
    must evaluate using ONLY [fold.test_start, fold.test_end).
    """
    results: list[WalkForwardResult] = []
    for fold in folds:
        selected = select_fn(fold)
        trades = evaluate_fn(fold, selected) if selected is not None else []
        results.append(WalkForwardResult(fold=fold, selected_config_id=selected, out_of_sample_trades=trades))
    return results


def aggregate_out_of_sample_trades(results: list[WalkForwardResult]) -> list:
    """Concatenates out-of-sample trades across all folds -- this pooled trade
    list is the walk-forward result reported, never any single fold's dev-period
    performance."""
    trades: list = []
    for r in results:
        trades.extend(r.out_of_sample_trades)
    return trades
