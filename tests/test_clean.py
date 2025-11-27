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
