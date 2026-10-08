import pandas as pd


def categorize_trip_duration(
    df: pd.DataFrame,
    duration_col: str = "Trip Duration",
) -> pd.DataFrame:
    """
    Categorize trips into duration ranges (short / medium / long).

    Durations are assumed to be in seconds.

    Categories (based on minutes):
    - < 20 minutes        -> "short"
    - 20 to 40 minutes    -> "medium"
    - > 40 minutes        -> "long"

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing a trip-duration column.
    duration_col : str, default "Trip Duration"
        Name of the column storing trip duration values in seconds.

    Returns
    -------
    pd.DataFrame
        A copy of the original DataFrame with an extra column
        ``"duration_category"`` containing the labels
        "short", "medium", or "long".

    Raises
    ------
    KeyError
        If the specified duration column is missing.
    ValueError
        If any duration value is negative.
    """
    if duration_col not in df.columns:
        # Fall back to detecting the duration column by normalized name,
        # so both "Trip Duration" and the raw file's "Trip  Duration"
        # (double space) resolve without caller changes.
        detected = next(
            (
                col
                for col in df.columns
                if col.lower().replace(" ", "") == "tripduration"
            ),
            None,
        )
        if detected is None:
            raise KeyError(duration_col)
        duration_col = detected

    # Empty input -> return empty with correct column
    if df.empty:
        result = df.copy()
        result["duration_category"] = pd.Series(dtype="object")
        return result

    # Validate for negative durations
    if (df[duration_col] < 0).any():
        raise ValueError("Trip duration cannot be negative.")

    result = df.copy()

    # Convert seconds to minutes
    minutes = result[duration_col] / 60.0

    # Use pandas.cut for clear binning logic
    bins = [0, 20, 40, float("inf")]
    labels = ["short", "medium", "long"]

    result["duration_category"] = pd.cut(
        minutes,
        bins=bins,
        labels=labels,
        right=True,
        include_lowest=True,
    )

    return result
