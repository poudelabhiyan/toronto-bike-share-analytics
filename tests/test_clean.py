import pandas as pd

from src.data_processing.clean import clean_data


def test_clean_data_does_not_modify_original_df():
    """clean_data must not modify the original DataFrame in place."""
    raw = pd.DataFrame(
        {
            "Trip Id": [1],
            "Trip  Duration": [60],  # double space like raw CSV
            "Start Station Id": [10],
            "Start Station Name": ["Station A"],
            "End Station Id": [20],
            "End Station Name": ["Station B"],
            "Start Time": ["2024-01-01 10:00"],
            "End Time": ["2024-01-01 10:10"],
        }
    )

    copy_before = raw.copy(deep=True)
    cleaned = clean_data(raw)

    # Original must stay the same
    pd.testing.assert_frame_equal(raw, copy_before)
    # Cleaned must be a different object
    assert cleaned is not raw


def test_clean_data_fills_station_names_from_ids_and_sets_unknown():
    """Missing station names should be filled from IDs or labeled Unknown."""
    df = pd.DataFrame(
        {
            "Trip Id": [1, 2, 3],
            "Start Station Id": [10, 10, 11],
            "Start Station Name": ["Station A", None, None],
            "End Station Id": [20, 21, 21],
            "End Station Name": [None, "Station B", None],
            # All durations the same so quantile filter does not drop any row
            "Trip  Duration": [120, 120, 120],
            "Start Time": ["2024-01-01 10:00"] * 3,
            "End Time": ["2024-01-01 10:10"] * 3,
        }
    )

    cleaned = clean_data(df)

    # No null station names after cleaning
    assert cleaned["Start Station Name"].isna().sum() == 0
    assert cleaned["End Station Name"].isna().sum() == 0

    # For ID 10, both rows should use the known name "Station A"
    start_names_for_10 = cleaned.loc[
        cleaned["Start Station Id"] == 10, "Start Station Name"
    ].unique()
    assert set(start_names_for_10) == {"Station A"}

    # For ID 11 (no mapping), label should start with "Unknown"
    unknown_rows = cleaned.loc[cleaned["Start Station Id"] == 11, "Start Station Name"]
    assert len(unknown_rows) == 1
    assert unknown_rows.iloc[0].startswith("Unknown")
