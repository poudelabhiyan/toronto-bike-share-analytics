from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


def compute_station_usage(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
) -> pd.DataFrame:
    """
    Compute trip counts per station.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing a station column.
    station_col : str, default "Start Station Name"
        Name of the column that contains station names.

    Returns
    -------
    pd.DataFrame
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
    top_n: Optional[int] = None,
) -> pd.DataFrame:
    """
    Compute station usage and return only the top N stations.

    Parameters
    ----------
    df : pd.DataFrame
        Input trips DataFrame.
    station_col : str, default "Start Station Name"
        Column containing station names.
    top_n : int, optional
        If provided, limit the result to the top N stations
        by trip_count.

    Returns
    -------
    pd.DataFrame
        Same format as compute_station_usage, possibly truncated
        to top_n rows.
    """
    usage = compute_station_usage(df, station_col=station_col)

    if top_n is not None and top_n >= 0:
        usage = usage.head(top_n)

    return usage


def compute_station_usage_filtered(
    df: pd.DataFrame,
    station_col: str = "Start Station Name",
    selected_stations: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """
    Return station usage filtered by a list of selected stations.
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
