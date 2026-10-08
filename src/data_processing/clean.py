import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the bike-sharing dataset.

    Steps performed:
    1. Work on a copy to avoid mutating the caller’s DataFrame.
    2. Standardize column names.
    3. Fill missing station names from the station ID -> name mapping
       built from rows where the name is known; remaining gaps become
       "Unknown".
    4. Ensure timestamp columns are parsed correctly.

    Returns
    -------
    pd.DataFrame
        A cleaned version of the dataset.
    """
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = [col.strip() for col in df_clean.columns]

    def _fill_station_names(id_col: str, name_col: str) -> None:
        if id_col not in df_clean.columns or name_col not in df_clean.columns:
            return
        # Normalize blanks and placeholder strings ("NULL", "None", "nan")
        # to missing so they participate in the fill
        name_series = df_clean[name_col].astype(object)
        stripped = name_series.astype(str).str.strip()
        missing_mask = stripped.eq("") | stripped.str.lower().isin(
            {"null", "none", "nan", "na", "n/a"}
        )
        name_series = name_series.mask(missing_mask)
        # Build ID -> name mapping from rows where the name is known
        known = df_clean.loc[name_series.notna(), [id_col, name_col]]
        mapping = (
            known.drop_duplicates(subset=id_col, keep="first")
            .set_index(id_col)[name_col]
        )
        filled = name_series.fillna(df_clean[id_col].map(mapping))
        df_clean[name_col] = filled.fillna("Unknown")

    _fill_station_names("Start Station Id", "Start Station Name")
    _fill_station_names("End Station Id", "End Station Name")

    # Convert Start Time column to datetime if present
    if "Start Time" in df_clean.columns:
        df_clean["Start Time"] = pd.to_datetime(df_clean["Start Time"], errors="coerce")

    return df_clean
