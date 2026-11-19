import polars as pl

from src.features.displacement import DisplacementConfig, compute_displacement_flags


def _bars(ohlcv: list[tuple[float, float, float, float, float]]) -> pl.DataFrame:
    o, h, l, c, atr = zip(*ohlcv)
    return pl.DataFrame(
        {
            "open": list(o), "high": list(h), "low": list(l), "close": list(c),
            "volume": [100.0] * len(o), "atr": list(atr),
        }
    )


def test_true_range_atr_rule_flags_large_bar() -> None:
    # bar range = 3, atr = 1 -> ratio 3.0 >= threshold 1.5
    df = _bars([(100, 103, 100, 102, 1.0)])
    cfg = DisplacementConfig(enable_true_range_atr=True, true_range_atr_threshold=1.5, enable_body_atr=False)
    out = compute_displacement_flags(df, config=cfg)
    assert out["displacement_true_range_atr"][0] is True
    assert out["tr_atr_ratio"][0] == 3.0


def test_true_range_atr_rule_false_for_small_bar() -> None:
    df = _bars([(100, 100.5, 99.8, 100.2, 1.0)])
    cfg = DisplacementConfig(enable_true_range_atr=True, true_range_atr_threshold=1.5)
    out = compute_displacement_flags(df, config=cfg)
    assert out["displacement_true_range_atr"][0] is False


def test_disabled_rule_produces_null_not_false() -> None:
    df = _bars([(100, 103, 100, 102, 1.0)])
    cfg = DisplacementConfig(enable_true_range_atr=False)
    out = compute_displacement_flags(df, config=cfg)
    assert out["displacement_true_range_atr"][0] is None


def test_body_atr_rule() -> None:
    # body = |102-100| = 2, atr=1 -> ratio 2.0
    df = _bars([(100, 103, 99, 102, 1.0)])
    cfg = DisplacementConfig(enable_body_atr=True, body_atr_threshold=1.5)
    out = compute_displacement_flags(df, config=cfg)
    assert out["body_atr_ratio"][0] == 2.0
    assert out["displacement_body_atr"][0] is True


def test_run_body_sum_atr_rule() -> None:
    # 3 consecutive up bars, bodies +1,+1,+1 -> sum=3, atr=1 -> ratio 3.0
    df = _bars([(100, 101.5, 99.5, 101, 1.0), (101, 102.5, 100.5, 102, 1.0), (102, 103.5, 101.5, 103, 1.0)])
    cfg = DisplacementConfig(enable_run_body_sum_atr=True, run_body_sum_atr_threshold=2.5, run_lookback_bars=3)
    out = compute_displacement_flags(df, config=cfg)
    assert out["run_body_sum_atr_ratio"][2] == 3.0
    assert out["displacement_run_body_sum_atr"][2] is True


def test_close_location_rule() -> None:
    # close at the very top of the bar's range -> close_location = 1.0
    df = _bars([(100, 103, 100, 103, 1.0)])
    cfg = DisplacementConfig(enable_close_location=True, close_location_threshold=0.7)
    out = compute_displacement_flags(df, config=cfg)
    assert out["close_location"][0] == 1.0
    assert out["displacement_close_location"][0] is True


def test_min_consecutive_directional_rule() -> None:
    # up, up, up, down -> run lengths 1,2,3,1
    df = _bars(
        [
            (100, 101, 99, 101, 1.0),
            (101, 102, 100, 102, 1.0),
            (102, 103, 101, 103, 1.0),
            (103, 104, 100, 100, 1.0),
        ]
    )
    cfg = DisplacementConfig(enable_min_consecutive_directional=True, min_consecutive_directional_bars=3)
    out = compute_displacement_flags(df, config=cfg)
    assert out["consecutive_directional_bars"].to_list() == [1, 2, 3, 1]
    assert out["displacement_min_consecutive_directional"].to_list() == [False, False, True, False]


def test_volume_confirmation_rule_uses_only_prior_bars() -> None:
    # avg volume computed via rolling_mean().shift(1) -- must not include current bar
    rows = [(100.0, 101.0, 99.0, 100.5, 1.0) for _ in range(5)]
    df = _bars(rows)
    df = df.with_columns(pl.Series("volume", [100.0, 100.0, 100.0, 100.0, 1000.0]))
    cfg = DisplacementConfig(enable_volume_confirmation=True, volume_multiple_of_avg=2.0, volume_avg_lookback_bars=4)
    out = compute_displacement_flags(df, config=cfg)
    # last bar's ratio uses avg of the PRIOR 4 bars (all 100) = 100, so 1000/100=10 -> True
    assert out["displacement_volume_confirmation"][-1] is True
    # confirm shift(1) means the current (huge-volume) bar itself isn't in its own average
    assert out["volume_ratio_to_avg"][-1] == 10.0
