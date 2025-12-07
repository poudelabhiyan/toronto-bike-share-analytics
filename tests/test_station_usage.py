import pandas as pd
import pytest

from src.analysis.station_usage import (
    compute_station_usage,
    compute_top_stations,
<<<<<<< HEAD
    compute_station_usage_filtered,
=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
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

<<<<<<< HEAD
    # Sorted descending by trip_count
    assert result["trip_count"].tolist() == sorted(
        result["trip_count"].tolist(), reverse=True
    )

=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

def test_compute_station_usage_missing_column():
    df = pd.DataFrame({"Other Col": ["X", "Y"]})

<<<<<<< HEAD
    # Column missing -> KeyError (as we implemented)
=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
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

<<<<<<< HEAD
    # Check that counts still make sense (2 valid named + Unknown)
    assert len(result) == 3


def test_compute_station_usage_empty_dataframe():
    df = pd.DataFrame({"Start Station Name": []})

    result = compute_station_usage(df, station_col="Start Station Name")

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["station", "trip_count"]
    assert len(result) == 0

=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

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

<<<<<<< HEAD
    # Only 2 rows should be returned
    assert len(result) == 2

=======
    assert len(result) == 2
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
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

<<<<<<< HEAD

=======
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
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
def test_compute_station_usage_filtered():
    data = {
        "Start Station Name": ["A", "A", "B", "C"],
    }
    df = pd.DataFrame(data)

    usage = compute_station_usage_filtered(
<<<<<<< HEAD
        df,
        station_col="Start Station Name",
        selected_stations=["A"],
=======
        df, station_col="Start Station Name", selected_stations=["A"]
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    )

    assert len(usage) == 1
    assert usage.iloc[0]["station"] == "A"
    assert usage.iloc[0]["trip_count"] == 2
<<<<<<< HEAD
=======

>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
