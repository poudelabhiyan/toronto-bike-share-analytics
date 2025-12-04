import pandas as pd
import pytest

from src.analysis.station_usage import (
    compute_station_usage,
    compute_top_stations,
)


def test_compute_station_usage_basic():
    data = {
        "Start Station Name": [
            "Station A",
            "Station A",
            "Station B",
            "Station C",
            "Station C",
            "Station C",
        ]
    }
    df = pd.DataFrame(data)

    result = compute_station_usage(df, station_col="Start Station Name")

    # Columns and row count
    assert list(result.columns) == ["station", "trip_count"]
    assert len(result) == 3  # A, B, C

    # Check counts
    assert result[result["station"] == "Station A"]["trip_count"].iloc[0] == 2
    assert result[result["station"] == "Station B"]["trip_count"].iloc[0] == 1
    assert result[result["station"] == "Station C"]["trip_count"].iloc[0] == 3


def test_compute_station_usage_missing_column():
    df = pd.DataFrame({"Other Col": ["X", "Y"]})

    with pytest.raises(KeyError):
        compute_station_usage(df, station_col="Start Station Name")


def test_compute_station_usage_handles_missing_names():
    data = {
        "Start Station Name": [
            "Station A",
            None,
            "Station B",
            "",
        ]
    }
    df = pd.DataFrame(data)

    result = compute_station_usage(df, station_col="Start Station Name")

    # Should treat None or empty as "Unknown"
    assert "Unknown" in result["station"].values


def test_compute_top_stations_limit():
    data = {
        "Start Station Name": [
            "A", "A", "A",
            "B", "B",
            "C",
        ]
    }
    df = pd.DataFrame(data)

    result = compute_top_stations(
        df,
        station_col="Start Station Name",
        top_n=2,
    )

    assert len(result) == 2
    # A has 3 trips, B has 2 trips
    assert list(result["station"]) == ["A", "B"]


def test_compute_top_stations_empty_dataframe():
    df = pd.DataFrame({"Start Station Name": []})

    result = compute_top_stations(
        df,
        station_col="Start Station Name",
        top_n=5,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert list(result.columns) == ["station", "trip_count"]

def compute_station_usage_filtered(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
    selected_stations: list[str] | None = None,
):
    """
    Return station usage filtered by station list.
    Used for dashboard integration.
    """
    usage = compute_station_usage(df, station_col)

    if selected_stations:
        usage = usage[usage["station"].isin(selected_stations)]

    return usage
def test_compute_station_usage_filtered():
    data = {
        "Start Station Name": ["A", "A", "B", "C"],
    }
    df = pd.DataFrame(data)

    usage = compute_station_usage_filtered(
        df, station_col="Start Station Name", selected_stations=["A"]
    )

    assert len(usage) == 1
    assert usage.iloc[0]["station"] == "A"
    assert usage.iloc[0]["trip_count"] == 2

