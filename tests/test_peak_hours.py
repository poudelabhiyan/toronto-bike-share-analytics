import pandas as pd
import pytest

from src.analysis.peak_hours import (
    compute_hourly_counts,
    get_peak_hours,
)


def test_compute_hourly_counts_basic():
    data = {
        "Start Time": [
            "2024-01-01 08:15:00",
            "2024-01-01 08:45:00",
            "2024-01-01 09:10:00",
        ]
    }
    df = pd.DataFrame(data)

    result = compute_hourly_counts(df, timestamp_col="Start Time")

    assert set(result.columns) == {"hour", "trip_count"}
    assert len(result) == 2
    assert result.loc[result["hour"] == 8, "trip_count"].iloc[0] == 2
    assert result.loc[result["hour"] == 9, "trip_count"].iloc[0] == 1


def test_compute_hourly_counts_empty_df():
    df = pd.DataFrame({"Start Time": []})
    result = compute_hourly_counts(df, timestamp_col="Start Time")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert list(result.columns) == ["hour", "trip_count"]


def test_compute_hourly_counts_missing_timestamp():
    df = pd.DataFrame({"Other Col": ["2024-01-01 08:00:00"]})

    with pytest.raises(KeyError):
        compute_hourly_counts(df, timestamp_col="Start Time")


def test_get_peak_hours_single_peak():
    data = {
        "Start Time": [
            "2024-01-01 08:00:00",
            "2024-01-01 08:30:00",
            "2024-01-01 09:00:00",
        ]
    }
    df = pd.DataFrame(data)

    peak = get_peak_hours(df, timestamp_col="Start Time")

    assert peak == [8]


def test_get_peak_hours_multiple_peaks():
    data = {
        "Start Time": [
            "2024-01-01 08:00:00",
            "2024-01-01 09:00:00",
            "2024-01-01 09:30:00",
            "2024-01-01 08:45:00",
        ]
    }
    df = pd.DataFrame(data)

    peak = get_peak_hours(df, timestamp_col="Start Time")

    assert sorted(peak) == [8, 9]


def test_get_peak_hours_empty_df():
    df = pd.DataFrame({"Start Time": []})

    peak = get_peak_hours(df, timestamp_col="Start Time")

    assert peak == []
