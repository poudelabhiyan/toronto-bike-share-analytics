# tests for load functions
import pandas as pd
import pytest
from src.data_processing.load import load_data


def test_load_data_returns_dataframe():
    df = load_data("data/bike_sharing.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_data_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("data/does_not_exist.csv")
