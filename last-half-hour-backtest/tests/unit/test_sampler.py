from src.experiments.sampler import sample_configs
from src.experiments.spaces import DEFAULT_SILVER_BULLET_SPACE, Dimension, SearchSpace


def test_sampling_is_reproducible_given_same_seed() -> None:
    a = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=100, seed=7)
    b = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=100, seed=7)
    assert [x.config_id for x in a] == [x.config_id for x in b]


def test_different_seeds_produce_different_samples() -> None:
    a = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=100, seed=1)
    b = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=100, seed=2)
    assert [x.config_id for x in a] != [x.config_id for x in b]


def test_no_duplicate_config_ids() -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=500, seed=3)
    ids = [s.config_id for s in samples]
    assert len(ids) == len(set(ids))


def test_categorical_dimensions_get_stratified_coverage() -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=500, seed=5)
    symbols = {s.config.symbol for s in samples}
    assert symbols == {"SPY", "QQQ"}
    stop_types = {s.config.stop_type for s in samples}
    assert stop_types == {"swing", "fvg_distal", "swept_extreme"}


def test_numeric_dimensions_stay_within_declared_bounds() -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=300, seed=9)
    for s in samples:
        assert 0.0 <= s.config.fvg_min_points <= 0.5
        assert 5 <= s.config.fvg_max_age_bars <= 60
        assert 2 <= s.config.swing_left_bars <= 10


def test_fully_fixed_categorical_space_collapses_to_one_unique_config() -> None:
    # No numeric dims and single-choice categoricals -> only one truly unique
    # config exists; sampling more than that must not fabricate duplicates.
    space = SearchSpace(
        dimensions=(
            Dimension("symbol", "categorical", choices=("SPY",)),
            Dimension("stop_type", "categorical", choices=("swing",)),
        )
    )
    samples = sample_configs(space, n=5, seed=1)
    assert len(samples) == 1
    assert samples[0].config.symbol == "SPY"


def test_requesting_more_than_space_can_uniquely_produce_stops_gracefully() -> None:
    # tiny space: only 2 possible unique configs given the dimensions declared
    space = SearchSpace(
        dimensions=(
            Dimension("symbol", "categorical", choices=("SPY", "QQQ")),
        )
    )
    samples = sample_configs(space, n=1000, seed=1)
    # cannot exceed the number of distinct symbol values times distinct
    # combinations of all OTHER fields' defaults, which is exactly 2 here
    assert len(samples) == 2
