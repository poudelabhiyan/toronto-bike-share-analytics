<<<<<<< HEAD
from __future__ import annotations
=======
"""
Station Usage Analysis

This module computes trip counts per starting station
and provides helper functions for the dashboard to show
busiest stations and apply station filters.
"""

from _future_ import annotations
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

from typing import Iterable, Optional

import pandas as pd

<<<<<<< HEAD
=======
_all_ = [
    "compute_station_usage",
    "compute_top_stations",
    "compute_station_usage_filtered",
]


# ---------- Internal helpers ----------


def _empty_usage_df() -> pd.DataFrame:
    """Return an empty usage DataFrame with the correct columns."""
    return pd.DataFrame({"station": [], "trip_count": []})


def _validate_station_column(df: pd.DataFrame, station_col: str) -> None:
    """
    Ensure the station column exists in the DataFrame.

    Raises
    ------
    KeyError
        If the station column is missing.
    """
    if station_col not in df.columns:
        raise KeyError(
            f"Missing required station column '{station_col}'. "
            f"Available columns: {list(df.columns)}"
        )


def _clean_station_names(df: pd.DataFrame, station_col: str) -> pd.DataFrame:
    """
    Replace missing or empty station names with 'Unknown'.

    This keeps the logic in one place so that both analytics
    code and dashboard use the same cleaning rules.
    """
    df_local = df.copy()

    # None / NaN -> "Unknown"
    df_local[station_col] = df_local[station_col].fillna("Unknown")

    # Empty strings or whitespace -> "Unknown"
    mask_empty = df_local[station_col].astype(str).str.strip() == ""
    df_local.loc[mask_empty, station_col] = "Unknown"

    return df_local


# ---------- Public API ----------

>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

def compute_station_usage(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
) -> pd.DataFrame:
    """
<<<<<<< HEAD
    Compute trip counts per station.
=======
    Count trips per starting station and return a sorted DataFrame.
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    Parameters
    ----------
    df : pd.DataFrame
<<<<<<< HEAD
        Input DataFrame containing a station column.
    station_col : str, default "Start Station Name"
        Name of the column that contains station names.
=======
        Input bike-sharing data.
    station_col : str, optional
        Column name for starting station, defaults to 'Start Station Name'
        (matches the Toronto dataset).
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    Returns
    -------
    pd.DataFrame
<<<<<<< HEAD
        DataFrame with columns:
        - 'station': station name
        - 'trip_count': number of trips starting at that station
        Sorted in descending order of trip_count.
    """
    # If column is missing, let tests see a KeyError
    if station_col not in df.columns:
        raise KeyError(f"Column '{station_col}' not found in DataFrame")

    # Empty DataFrame → return empty with correct columns
    if df.empty:
        return pd.DataFrame(
            {
                "station": pd.Series(dtype="object"),
                "trip_count": pd.Series(dtype="int"),
            }
        )

    # Clean station names: treat None / NaN / empty string as "Unknown"
    station_series = df[station_col].fillna("Unknown")
    station_series = station_series.replace("", "Unknown")

    usage = (
        station_series.to_frame(name=station_col)
        .groupby(station_col, dropna=False)
=======
        Columns:
        - station
        - trip_count

        Sorted in descending order of trip_count.
    """
    _validate_station_column(df, station_col)

    if df.empty:
        return _empty_usage_df()

    df_clean = _clean_station_names(df, station_col)

    usage = (
        df_clean.groupby(station_col)
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
        .size()
        .reset_index(name="trip_count")
        .rename(columns={station_col: "station"})
        .sort_values("trip_count", ascending=False)
        .reset_index(drop=True)
    )

    return usage


def compute_top_stations(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
<<<<<<< HEAD
    top_n: Optional[int] = None,
) -> pd.DataFrame:
    """
    Compute station usage and return only the top N stations.
=======
    top_n: Optional[int] = 10,
) -> pd.DataFrame:
    """
    Return the top N busiest starting stations.
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    Parameters
    ----------
    df : pd.DataFrame
<<<<<<< HEAD
        Input trips DataFrame.
    station_col : str, default "Start Station Name"
        Column containing station names.
    top_n : int, optional
        If provided, limit the result to the top N stations
        by trip_count.
=======
        Input bike-sharing data.
    station_col : str, optional
        Column for station name, default 'Start Station Name'.
    top_n : int, optional
        Number of stations to return. If None or negative, all
        stations are returned.
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    Returns
    -------
    pd.DataFrame
<<<<<<< HEAD
        Same format as compute_station_usage, possibly truncated
        to top_n rows.
    """
    usage = compute_station_usage(df, station_col=station_col)

    if top_n is not None and top_n >= 0:
        usage = usage.head(top_n)

    return usage
=======
        Same columns as compute_station_usage, limited to top_n rows.
    """
    usage = compute_station_usage(df, station_col=station_col)

    if usage.empty:
        return usage

    if top_n is None or top_n < 0:
        return usage

    return usage.head(top_n)
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e


def compute_station_usage_filtered(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
    selected_stations: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """
<<<<<<< HEAD
    Return station usage filtered by a list of selected stations.
=======
    Return station usage filtered by selected stations.

>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    Useful for dashboard integration.

    Parameters
    ----------
    df : pd.DataFrame
        Input trips DataFrame.
    station_col : str, default "Start Station Name"
        Column containing station names.
    selected_stations : iterable of str, optional
        When provided, only these stations are kept.

    Returns
    -------
    pd.DataFrame
        Station usage DataFrame filtered by selected stations.
    """
    usage = compute_station_usage(df, station_col=station_col)

    if selected_stations:
        usage = usage[usage["station"].isin(selected_stations)]

    return usage
