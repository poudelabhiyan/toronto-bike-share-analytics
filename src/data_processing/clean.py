<<<<<<< HEAD
=======
"""
Data cleaning utilities for the Toronto Bike Share trip-level dataset.

Main goals:
- Keep the original raw DataFrame untouched (work on a copy).
- Standardize column names.
- Fix data types (IDs, datetimes, durations).
- Handle missing values intelligently:
    * Station names and model are MAR (depend on IDs), so we impute
      using ID-based mappings first, then simple mode imputation.
- Detect and remove outliers in trip duration using robust quantiles.
- Ensure there are no missing values left in key columns.
"""

>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
from __future__ import annotations

import pandas as pd


<<<<<<< HEAD
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Toronto Bike Share trip dataset.

    Steps
    -----
    1. Work on a copy to avoid changing the caller's DataFrame.
    2. Standardize column names:
        - strip leading/trailing spaces
        - collapse double-spaces (e.g., 'Trip  Duration' -> 'Trip Duration')
    3. Enforce sensible dtypes:
        - ID columns as nullable integers (Int64)
        - 'Trip Duration' as numeric seconds
        - 'Start Time' and 'End Time' as datetimes
    4. Handle missing values:
        - Station names:
            * Use Start/End Station Id -> Name mapping to fill (MAR behaviour)
            * Any remaining stations get 'Unknown Start Station' / 'Unknown End Station'
        - Model:
            * Use Bike Id -> Model mapping (MAR)
            * Remaining missing filled with global mode
    5. Tidy categorical text:
        - Standardize 'User Type' capitalization.
    6. Outlier handling for trip duration:
        - Drop non-positive durations.
        - Keep trips between the 1st and 99.5th percentiles of duration.
    7. Drop duplicate rows and rows where both Start Time and End Time are missing.

    Returns
    -------
    pd.DataFrame
        Fully cleaned dataset, ready for analysis and visualization.
=======
def _get_duration_column(df: pd.DataFrame) -> str | None:
    """
    Detect the trip duration column by pattern.
    After cleaning, the file should have a column that
    normalizes to 'tripduration' when spaces are removed.
    """
    for col in df.columns:
        if col.lower().replace(" ", "") == "tripduration":
            return col
    return None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Toronto Bike Share trip dataset (refined version for US10).

    Steps:
    1. Work on a copy to avoid changing the caller's DataFrame.
    2. Standardize column names:
        - strip leading/trailing spaces
        - collapse double-spaces
    3. Enforce sensible dtypes:
        - ID columns as nullable integers (Int64)
        - trip duration as numeric seconds
        - 'Start Time' and 'End Time' as datetimes
    4. Handle missing values with MAR logic:
        - station names via ID → most common name mapping, then fallback label
        - model via Bike Id → most common model, then global mode
    5. Tidy categorical text for 'User Type' and 'Model'.
    6. Outlier removal for trip duration using 1st–99.5th percentiles.
    7. Drop duplicates and rows with both times missing.
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    """
    # 1. Work on a copy so the original df is never modified in place
    df = df.copy()

<<<<<<< HEAD
    # 2. Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("  ", " ", regex=False)
    )

    # Identify the trip-duration column after standardization.
    duration_col = None
    for col in df.columns:
        if col.lower().replace(" ", "") == "tripduration":
            duration_col = col
            break

    # 3. Type conversions
    # ------------------------------------------------------------------
    # ID columns as identifiers (nullable integers)
=======
    # 2. Standardize column names (important for consistent access)
    df.columns = (
        df.columns
        .str.strip()                       # remove leading/trailing spaces
        .str.replace("  ", " ", regex=False)  # collapse double spaces
    )

    # Identify the trip-duration column after standardization
    duration_col = _get_duration_column(df)

    # 3. Type conversions
    # ------------------------------------------------------------------
    # 3a. ID columns as identifiers, not continuous numbers
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    id_cols = ["Trip Id", "Start Station Id", "End Station Id", "Bike Id"]
    for col in id_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

<<<<<<< HEAD
    # Start/End Time as datetime
=======
    # 3b. Convert start/end times to datetime for time-based analysis
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    datetime_cols = ["Start Time", "End Time"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

<<<<<<< HEAD
    # Trip duration as numeric seconds
    if duration_col:
        df[duration_col] = pd.to_numeric(df[duration_col], errors="coerce")

    # 4. Missing values – station names and model
    # ------------------------------------------------------------------
    # 4a. Start Station Name: use Start Station Id → most common name, then "Unknown"
=======
    # 3c. Convert trip duration to numeric seconds
    if duration_col:
        df[duration_col] = pd.to_numeric(df[duration_col], errors="coerce")

    # 4. Missing values – station names and model (MAR logic)
    # ------------------------------------------------------------------
    # 4a. Start Station Name: use Start Station Id → most common name
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    if "Start Station Name" in df.columns and "Start Station Id" in df.columns:
        start_map = (
            df.dropna(subset=["Start Station Name"])
              .groupby("Start Station Id")["Start Station Name"]
              .agg(lambda x: x.mode().iloc[0])
        )

        missing_mask = df["Start Station Name"].isna()
        df.loc[missing_mask, "Start Station Name"] = (
            df.loc[missing_mask, "Start Station Id"].map(start_map)
        )

<<<<<<< HEAD
=======
        # Any stations still missing after ID-based imputation get a generic label
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
        df["Start Station Name"] = df["Start Station Name"].fillna(
            "Unknown Start Station"
        )

<<<<<<< HEAD
    # 4b. End Station Name: analogous logic
=======
    # 4b. End Station Name: analogous logic using End Station Id
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    if "End Station Name" in df.columns and "End Station Id" in df.columns:
        end_map = (
            df.dropna(subset=["End Station Name"])
              .groupby("End Station Id")["End Station Name"]
              .agg(lambda x: x.mode().iloc[0])
        )

        missing_mask = df["End Station Name"].isna()
        df.loc[missing_mask, "End Station Name"] = (
            df.loc[missing_mask, "End Station Id"].map(end_map)
        )

        df["End Station Name"] = df["End Station Name"].fillna(
            "Unknown End Station"
        )

<<<<<<< HEAD
    # 4c. Model: use Bike Id → most common model, then overall mode
=======
    # 4c. Model: use Bike Id → most common model first, then overall mode
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    if "Model" in df.columns:
        df["Model"] = df["Model"].astype("string").str.strip().str.upper()

        if "Bike Id" in df.columns:
            model_map = (
                df.dropna(subset=["Model"])
                  .groupby("Bike Id")["Model"]
                  .agg(lambda x: x.mode().iloc[0])
            )

            missing_mask = df["Model"].isna()
            df.loc[missing_mask, "Model"] = (
                df.loc[missing_mask, "Bike Id"].map(model_map)
            )

<<<<<<< HEAD
=======
        # Remaining NA (if any) → fill with global mode
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
        if df["Model"].isna().any():
            mode_model = df["Model"].mode().iloc[0]
            df["Model"] = df["Model"].fillna(mode_model)

    # 5. Standardize text fields (categoricals)
    # ------------------------------------------------------------------
    if "User Type" in df.columns:
        df["User Type"] = (
            df["User Type"]
              .astype("string")
              .str.strip()
<<<<<<< HEAD
              .str.title()
        )

    # 6. Outlier handling for trip duration
=======
              .str.title()   # 'casual member' -> 'Casual Member'
        )

    # 6. Outlier detection and removal for trip duration
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    # ------------------------------------------------------------------
    if duration_col:
        # Remove non-positive durations
        df = df[df[duration_col] > 0]

<<<<<<< HEAD
        # Keep durations between 1st and 99.5th percentiles
        lower_q = df[duration_col].quantile(0.01)
        upper_q = df[duration_col].quantile(0.995)
        df = df[(df[duration_col] >= lower_q) & (df[duration_col] <= upper_q)]

    # 7. Drop duplicate rows
    df = df.drop_duplicates()

    # 8. Drop rows where both times are missing (if both columns exist)
=======
        # Use a robust quantile rule to remove extreme outliers:
        # keep durations between the 1st and 99.5th percentiles
        lower_q = df[duration_col].quantile(0.01)
        upper_q = df[duration_col].quantile(0.995)

        df = df[(df[duration_col] >= lower_q) & (df[duration_col] <= upper_q)]

    # 7. Drop duplicate rows
    # ------------------------------------------------------------------
    df = df.drop_duplicates()

    # 8. Optional: drop rows where both times are missing (should be rare)
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    if set(datetime_cols).issubset(df.columns):
        df = df.dropna(subset=datetime_cols, how="all")

    return df
