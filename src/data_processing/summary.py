<<<<<<< HEAD
"""
Summary utilities for the Toronto Bike Share trip-level dataset.

This module assumes:
- Raw data is loaded with load.load_data()
- Data is cleaned with clean.clean_data()

It provides:
- Overall numeric summary for measure columns (excluding IDs)
- Trip duration summary (mean, min, max, quantiles) in minutes
- Trips by user type (counts and percentages)
- Time-based summaries (by hour, weekday, month)
- Station demand summaries (top start and end stations)
- Missing values overview (for documentation)
"""

import pandas as pd
from load import load_data
from clean import clean_data
=======
# functions for summary statistics
import pandas as pd
from .load import load_data
from .clean import clean_data
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e


# Columns that should be treated as identifiers, not measures
ID_COLUMNS = ["Trip Id", "Start Station Id", "End Station Id", "Bike Id"]


def _get_duration_column(df: pd.DataFrame) -> str | None:
    """
    Detect the trip duration column by pattern.
    After cleaning, your file should have a column that
    normalizes to 'tripduration' when spaces are removed.
    """
    for col in df.columns:
        if col.lower().replace(" ", "") == "tripduration":
            return col
    return None


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
<<<<<<< HEAD
    Generate summary statistics for numeric *measure* columns.
=======
    Generate summary statistics for numeric measure columns.
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    - Excludes ID-like columns (Trip Id, Station Ids, Bike Id).
    - Returns count, mean, std, min, quartiles, max, and missing_values.

    This is the main table you would show in a data understanding section.
    """
    # Select numeric columns
    numeric_df = df.select_dtypes(include=["int64", "Int64", "float64"])

    # Drop identifier columns from numeric summary
    drop_cols = []
    for col in numeric_df.columns:
        if col in ID_COLUMNS or "id" in col.lower():
            drop_cols.append(col)

    numeric_df = numeric_df.drop(columns=drop_cols, errors="ignore")

    if numeric_df.empty:
        return pd.DataFrame()

    summary = numeric_df.describe(percentiles=[0.25, 0.5, 0.75]).T
    summary["missing_values"] = numeric_df.isna().sum()
    return summary


def duration_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detailed trip duration summary.

    Returns a table with:
    - Total Trips
    - Mean Duration (minutes)
    - Median Duration (minutes)
    - Std Duration (minutes)
    - Min Duration (minutes)
    - 1st Quartile (minutes)
    - 3rd Quartile (minutes)
    - 99th Percentile (minutes)
    - Max Duration (minutes)
    """
    duration_col = _get_duration_column(df)
    if not duration_col:
        return pd.DataFrame({"Metric": [], "Value": []})

    # Work with duration in minutes
    duration_minutes = df[duration_col].astype(float) / 60.0
    duration_minutes = duration_minutes.dropna()

    if duration_minutes.empty:
        return pd.DataFrame({"Metric": [], "Value": []})

    metrics = [
        "Total Trips (non-missing duration)",
        "Mean Duration (minutes)",
        "Median Duration (minutes)",
        "Std Duration (minutes)",
        "Min Duration (minutes)",
        "1st Quartile (minutes)",
        "3rd Quartile (minutes)",
        "99th Percentile (minutes)",
        "Max Duration (minutes)",
    ]

    values = [
        int(duration_minutes.shape[0]),
        duration_minutes.mean(),
        duration_minutes.median(),
        duration_minutes.std(),
        duration_minutes.min(),
        duration_minutes.quantile(0.25),
        duration_minutes.quantile(0.75),
        duration_minutes.quantile(0.99),
        duration_minutes.max(),
    ]

    return pd.DataFrame({"Metric": metrics, "Value": values})


def trips_by_user_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number and percentage of trips by User Type.

    Returns:
        DataFrame with columns:
        - User Type
        - trip_count
        - trip_percent (percentage of total trips)
    """
    if "User Type" not in df.columns:
        return pd.DataFrame(columns=["User Type", "trip_count", "trip_percent"])

    counts = (
        df.groupby("User Type")
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
    )

    total_trips = counts["trip_count"].sum()
    counts["trip_percent"] = (counts["trip_count"] / total_trips) * 100.0
    return counts


def trips_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trip counts by hour of day based on Start Time.

    Returns:
        DataFrame with columns:
        - hour (0–23)
        - trip_count
    """
    if "Start Time" not in df.columns:
        return pd.DataFrame(columns=["hour", "trip_count"])

    s = df["Start Time"].dropna()
    hourly = (
        s.dt.hour.value_counts()
        .sort_index()
        .reset_index()
    )
    hourly.columns = ["hour", "trip_count"]
    return hourly


def trips_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trip counts by day of week (Monday–Sunday) based on Start Time.

    Returns:
        DataFrame with columns:
        - weekday (day name)
        - trip_count
    """
    if "Start Time" not in df.columns:
        return pd.DataFrame(columns=["weekday", "trip_count"])

    s = df["Start Time"].dropna()
    weekday = (
        s.dt.day_name()
        .value_counts()
        .reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        .dropna()
        .reset_index()
    )
    weekday.columns = ["weekday", "trip_count"]
    return weekday


def trips_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trip counts by calendar month (1–12) based on Start Time.

    Returns:
        DataFrame with columns:
        - month (1–12)
        - trip_count
    """
    if "Start Time" not in df.columns:
        return pd.DataFrame(columns=["month", "trip_count"])

    s = df["Start Time"].dropna()
    month = (
        s.dt.month.value_counts()
        .sort_index()
        .reset_index()
    )
    month.columns = ["month", "trip_count"]
    return month


def top_start_stations(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Top N start stations by trip count.

    Returns:
        DataFrame with columns:
        - Start Station Name
        - trip_count
    """
    if "Start Station Name" not in df.columns:
        return pd.DataFrame(columns=["Start Station Name", "trip_count"])

    result = (
        df.groupby("Start Station Name")
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
        .head(n)
    )
    return result


def top_end_stations(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Top N end stations by trip count.

    Returns:
        DataFrame with columns:
        - End Station Name
        - trip_count
    """
    if "End Station Name" not in df.columns:
        return pd.DataFrame(columns=["End Station Name", "trip_count"])

    result = (
        df.groupby("End Station Name")
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
        .head(n)
    )
    return result


def missing_values_overview(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple missing values overview for documentation.

    Returns:
        DataFrame with:
        - column
        - missing_count
        - missing_percent
    """
    total_rows = df.shape[0]
    counts = df.isna().sum()
    overview = counts.reset_index()
    overview.columns = ["column", "missing_count"]
    overview["missing_percent"] = (overview["missing_count"] / total_rows) * 100.0
    return overview


<<<<<<< HEAD
if __name__ == "__main__":
=======
if _name_ == "_main_":
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    # End-to-end summary when run as a script
    # 1 Load raw
    df_raw = load_data()

    # 2 Clean
    df_clean = clean_data(df_raw)

    # 3 Generate and print summaries
    print("=== Numeric summary (non-ID measures) ===")
    print(summary_statistics(df_clean))

    print("\n=== Trip duration summary (minutes) ===")
    print(duration_summary(df_clean))

    print("\n=== Trips by user type ===")
    print(trips_by_user_type(df_clean))

    print("\n=== Trips by hour ===")
    print(trips_by_hour(df_clean))

    print("\n=== Trips by weekday ===")
    print(trips_by_weekday(df_clean))

    print("\n=== Trips by month ===")
    print(trips_by_month(df_clean))

    print("\n=== Top 10 start stations ===")
    print(top_start_stations(df_clean, n=10))

    print("\n=== Top 10 end stations ===")
    print(top_end_stations(df_clean, n=10))

    print("\n=== Missing values overview ===")
    print(missing_values_overview(df_clean))
<<<<<<< HEAD
=======

>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
