import pandas as pd
from typing import List, Tuple


def compute_hourly_counts(df: pd.DataFrame, timestamp_col: str = "Start Time") -> pd.DataFrame:
    """
    Compute number of trips per hour.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a timestamp column.
    timestamp_col : str, default "Start Time"
        Name of the timestamp column.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ["hour", "trip_count"].

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"Start Time": ["2024-01-01 08:15:00", "2024-01-01 09:10:00"]})
    >>> compute_hourly_counts(df)
       hour  trip_count
    0     8           1
    1     9           1

    Notes
    -----
    - If the DataFrame is empty, returns an empty DataFrame with the correct columns.
    - If the timestamp column is missing, a KeyError is raised.
    """
    # Handle empty DataFrame early
    if df.empty:
        return pd.DataFrame(columns=["hour", "trip_count"])

    # Will raise KeyError if timestamp_col is missing, which our tests expect
    hours = pd.to_datetime(df[timestamp_col]).dt.hour

    hourly_counts = (
        hours.value_counts()
        .sort_index()
        .rename_axis("hour")
        .reset_index(name="trip_count")
    )

    return hourly_counts


def get_peak_hours(df: pd.DataFrame, timestamp_col: str = "Start Time") -> List[int]:
    """
    Return the list of peak hour(s) based on trip counts.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a timestamp column.
    timestamp_col : str, default "Start Time"
        Name of the timestamp column.

    Returns
    -------
    list of int
        List of hour values with the maximum trip count.
        Returns an empty list if there is no data.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"Start Time": ["2024-01-01 08:00:00", "2024-01-01 09:30:00"]})
    >>> get_peak_hours(df)
    [8, 9]
    """
    hourly_counts = compute_hourly_counts(df, timestamp_col=timestamp_col)

    if hourly_counts.empty:
        return []

    max_count = hourly_counts["trip_count"].max()
    peak_hours = hourly_counts.loc[
        hourly_counts["trip_count"] == max_count, "hour"
    ].tolist()

    return peak_hours


def calculate_peak_hours(df: pd.DataFrame, timestamp_col: str = "Start Time") -> Tuple[pd.DataFrame, List[int]]:
    """
    Convenience function that returns both hourly counts and peak hours.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a timestamp column.
    timestamp_col : str, default "Start Time"
        Name of the timestamp column.

    Returns
    -------
    (pd.DataFrame, list of int)
        - hourly_counts: DataFrame with columns ["hour", "trip_count"]
        - peak_hours: list of peak hour values
    """
    hourly_counts = compute_hourly_counts(df, timestamp_col=timestamp_col)
    peak_hours = get_peak_hours(df, timestamp_col=timestamp_col)
    return hourly_counts, peak_hours
