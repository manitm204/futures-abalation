from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import polars as pl

from src.features.sessions import label_windows
from src.utils.config_models import DEFAULT_SILVER_BULLET_WINDOWS

NY = ZoneInfo("America/New_York")


def _bars_at_ny_times(times: list[tuple[int, int]]) -> pl.DataFrame:
    ts = [datetime(2024, 6, 3, h, m, tzinfo=NY) for h, m in times]  # June: EDT
    return pl.DataFrame({"bar_open_ts_ny": ts})


def test_ny_am_window_labeled() -> None:
    df = _bars_at_ny_times([(10, 0), (10, 59), (9, 59), (11, 0)])
    out = label_windows(df, DEFAULT_SILVER_BULLET_WINDOWS)
    labels = out["sb_window"].to_list()
    assert labels[0] == "ny_am"
    assert labels[1] == "ny_am"
    assert labels[2] is None  # just before window
    assert labels[3] is None  # window end is exclusive


def test_ny_pm_window_labeled() -> None:
    df = _bars_at_ny_times([(14, 0), (14, 30), (14, 59), (15, 0)])
    out = label_windows(df, DEFAULT_SILVER_BULLET_WINDOWS)
    labels = out["sb_window"].to_list()
    assert labels == ["ny_pm", "ny_pm", "ny_pm", None]


def test_london_window_labeled() -> None:
    df = _bars_at_ny_times([(3, 0), (3, 30), (4, 0)])
    out = label_windows(df, DEFAULT_SILVER_BULLET_WINDOWS)
    assert out["sb_window"].to_list() == ["london", "london", None]


def test_bars_outside_all_windows_are_null() -> None:
    df = _bars_at_ny_times([(12, 0), (16, 0), (1, 0)])
    out = label_windows(df, DEFAULT_SILVER_BULLET_WINDOWS)
    assert out["sb_window"].to_list() == [None, None, None]
