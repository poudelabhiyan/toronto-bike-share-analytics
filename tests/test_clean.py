import pandas as pd
<<<<<<< HEAD

=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
from src.data_processing.clean import clean_data


def test_clean_data_does_not_modify_original_df():
<<<<<<< HEAD
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
=======
    raw = pd.DataFrame({
        "Trip Id": [1],
        "Trip Duration": [60],
    })
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e

    copy_before = raw.copy(deep=True)
    cleaned = clean_data(raw)

    # Original must stay the same
    pd.testing.assert_frame_equal(raw, copy_before)
<<<<<<< HEAD
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
=======
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
import pandas as pd
from src.data_processing.clean import clean_data


def test_clean_data_basic():
    df = pd.DataFrame({
        "Trip Id": [1, 2, 2],
        "Trip Duration": [100, None, 5000],
        "Start Station Name": ["A", None, "A"]
    })

    cleaned = clean_data(df)

    # No missing values
    assert cleaned.isna().sum().sum() == 0
    # Duplicates removed
    assert len(cleaned) <= 2
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
