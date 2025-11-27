"""
Basic data cleaning utilities for the Toronto Bike Share trip-level dataset.

This version is for US2:
•⁠  ⁠Work on a copy of the DataFrame
•⁠  ⁠Standardize column names
•⁠  ⁠Fix basic types (IDs, times, duration)
•⁠  ⁠Handle missing values with simple rules
•⁠  ⁠Do a simple outlier filter for trip duration
"""

from _future_ import annotations

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Toronto Bike Share trip dataset (basic version for US2).

    Steps:
    1. Work on a copy
    2. Standardize column names (strip spaces, collapse double spaces)
    3. Convert ID columns to Int64
    4. Convert Start Time and End Time to datetime
    5. Convert Trip Duration to numeric
    6. Fill missing values:
        - numeric columns: median
        - object columns: mode
    7. Remove non-positive or extreme trip durations (simple quantile rule)
    8. Drop duplicate rows
    """
    # 1. Work on a copy
    df = df.copy()

    # 2. Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("  ", " ", regex=False)
    )

    # Try to locate the Trip Duration column
    duration_col = None
    for col in df.columns:
        if col.lower().replace(" ", "") == "tripduration":
            duration_col = col
            break

    # 3. ID columns → Int64
    id_cols = ["Trip Id", "Start Station Id", "End Station Id", "Bike Id"]
    for col in id_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # 4. Datetime columns
    datetime_cols = ["Start Time", "End Time"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 5. Trip Duration → numeric
    if duration_col:
        df[duration_col] = pd.to_numeric(df[duration_col], errors="coerce")

    # 6. Fill missing values (simple strategy)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    object_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in object_cols:
        if df[col].isna().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val.iloc[0])

    # 7. Simple outlier handling for duration
    if duration_col:
        # remove non-positive durations
        df = df[df[duration_col] > 0]

        # keep values between 1st and 99th percentile
        lower_q = df[duration_col].quantile(0.01)
        upper_q = df[duration_col].quantile(0.99)
        df = df[(df[duration_col] >= lower_q) & (df[duration_col] <= upper_q)]

    # 8. Drop duplicate rows
    df = df.drop_duplicates()

    return df# functions for cleaning data
