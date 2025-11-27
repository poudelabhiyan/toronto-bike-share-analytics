import pandas as pd
import pytest
from src.data_processing.load import load_data


def test_load_data_returns_dataframe():
    """Expect load_data to return a DataFrame when file exists."""
    df = load_data("data/bike_sharing.csv")   # make sure file name matches
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_data_raises_for_missing_file():
    """Expect load_data to raise FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        load_data("data/does_not_exist.csv")

def test_load_data_raises_when_required_columns_missing():
    from src.data_processing.load import load_data
    import pytest

    with pytest.raises(ValueError):
        load_data(
            "data/bike_sharing.csv",
            required_columns=["THIS_COLUMN_DOES_NOT_EXIST"]
        )
# tests for load functions
