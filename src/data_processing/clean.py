import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the bike-sharing dataset.

    Steps performed:
    1. Work on a copy to avoid mutating the caller’s DataFrame.
    2. Standardize column names.
    3. Fill missing station names using station IDs.
    4. Replace empty or missing station names with “Unknown”.
    5. Ensure timestamp columns are parsed correctly.

    Returns
    -------
    pd.DataFrame
        A cleaned version of the dataset.
    """
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = [col.strip() for col in df_clean.columns]

    # Fill missing Start Station Name
    if "Start Station Name" in df_clean.columns and "Start Station Id" in df_clean.columns:
        df_clean["Start Station Name"] = df_clean["Start Station Name"].fillna(
            df_clean["Start Station Id"].astype(str)
        )

    # Fill missing End Station Name
    if "End Station Name" in df_clean.columns and "End Station Id" in df_clean.columns:
        df_clean["End Station Name"] = df_clean["End Station Name"].fillna(
            df_clean["End Station Id"].astype(str)
        )

    # Replace empty strings with Unknown
    for col in ["Start Station Name", "End Station Name"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col].replace("", "Unknown", inplace=True)

    # Convert Start Time column to datetime if present
    if "Start Time" in df_clean.columns:
        df_clean["Start Time"] = pd.to_datetime(df_clean["Start Time"], errors="coerce")

    return df_clean
