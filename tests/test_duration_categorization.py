import pandas as pd
import pytest

from src.analysis.duration_categorization import categorize_trip_duration



def test_categorize_trip_duration_basic():
    df = pd.DataFrame({
        "Trip Duration": [300, 1800, 3600, 4200]  # 5, 30, 60, 70 minutes
    })

    result = categorize_trip_duration(df)

    assert "duration_category" in result.columns
    assert result.loc[0, "duration_category"] == "short"   # 5 min
    assert result.loc[1, "duration_category"] == "medium"  # 30 min
    assert result.loc[2, "duration_category"] == "long"    # 60 min
    assert result.loc[3, "duration_category"] == "long"    # 70 min


def test_categorize_trip_duration_handles_empty_df():
    df = pd.DataFrame({"Trip Duration": []})

    result = categorize_trip_duration(df)

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert "duration_category" in result.columns


def test_categorize_trip_duration_raises_for_negative_values():
    df = pd.DataFrame({
        "Trip Duration": [300, -60]  # includes a negative duration
    })

    with pytest.raises(ValueError):
        categorize_trip_duration(df)


def test_categorize_trip_duration_missing_column_raises():
    df = pd.DataFrame({
        "Other Column": [100, 200]
    })

    with pytest.raises(KeyError):
        categorize_trip_duration(df)
