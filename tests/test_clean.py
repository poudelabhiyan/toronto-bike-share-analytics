import pandas as pd
from src.data_processing.clean import clean_data


def test_clean_data_does_not_modify_original_df():
    raw = pd.DataFrame({
        "Trip Id": [1],
        "Trip Duration": [60],
    })

    copy_before = raw.copy(deep=True)
    cleaned = clean_data(raw)

    # Original must stay the same
    pd.testing.assert_frame_equal(raw, copy_before)
    # Cleaned can be different object
    assert cleaned is not raw


def test_clean_data_fills_station_names_from_ids_and_labels_unknown():
    df = pd.DataFrame({
        "Trip Id": [1, 2, 3],
        "Start Station Id": [10, 10, 11],
        "Start Station Name": ["Station A", None, None],
        "End Station Id": [20, 21, 21],
        "End Station Name": [None, "Station B", None],
        "Trip Duration": [60, 120, 180],
        "Start Time": ["2024-01-01 10:00", "2024-01-01 11:00", "2024-01-01 12:00"],
        "End Time": ["2024-01-01 10:10", "2024-01-01 11:10", "2024-01-01 12:10"],
    })

    cleaned = clean_data(df)

    # No missing station names
    assert cleaned["Start Station Name"].isna().sum() == 0
    assert cleaned["End Station Name"].isna().sum() == 0

    # ID 10 should map to "Station A"
    assert (
        cleaned.loc[cleaned["Start Station Id"] == 10, "Start Station Name"]
        .nunique()
        == 1
    )

    # Any leftover missing should be replaced by "Unknown ..." labels
    assert "Unknown Start Station" in cleaned["Start Station Name"].values \
           or "Unknown End Station" in cleaned["End Station Name"].values


def test_clean_data_standardizes_user_type_and_model_and_removes_outlier_durations():
    df = pd.DataFrame({
        "Trip Id": [1, 2, 3],
        "Trip Duration": [60, 120, 999999],  # last is an extreme outlier
        "User Type": ["member", "Casual Member", " MEMBER "],
        "Bike Id": [111, 111, 111],
        "Model": [None, "e-bike", None],
        "Start Station Id": [10, 10, 10],
        "Start Station Name": ["A", "A", "A"],
        "End Station Id": [20, 20, 20],
        "End Station Name": ["B", "B", "B"],
        "Start Time": ["2024-01-01 10:00"] * 3,
        "End Time": ["2024-01-01 10:10"] * 3,
    })

    cleaned = clean_data(df)

    # Outlier row should be removed (less than original 3 rows)
    assert len(cleaned) < len(df)

    # User Type normalized
    assert set(cleaned["User Type"].unique()) <= {
        "Member",
        "Casual Member",
    }

    # Model filled and uppercased
    assert cleaned["Model"].isna().sum() == 0
    for m in cleaned["Model"].unique():
        assert m == m.upper()
# tests for clean functions
