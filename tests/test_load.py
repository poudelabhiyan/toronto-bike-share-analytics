import pandas as pd
import pytest
<<<<<<< HEAD

=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
from src.data_processing.load import load_data


def test_load_data_returns_dataframe():
    """Expect load_data to return a DataFrame when file exists."""
<<<<<<< HEAD
    df = load_data("data/bike_sharing.csv")  # make sure file name matches
=======
    df = load_data("data/bike_sharing.csv")   # make sure file name matches
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_data_raises_for_missing_file():
    """Expect load_data to raise FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        load_data("data/does_not_exist.csv")

<<<<<<< HEAD

def test_load_data_raises_when_required_columns_missing():
    """Expect load_data to raise ValueError when required columns are missing."""
    with pytest.raises(ValueError):
        load_data(
            "data/bike_sharing.csv",
            required_columns=["THIS_COLUMN_DOES_NOT_EXIST"],
        )
=======
def test_load_data_raises_when_required_columns_missing():
    from src.data_processing.load import load_data
    import pytest

    with pytest.raises(ValueError):
        load_data(
            "data/bike_sharing.csv",
            required_columns=["THIS_COLUMN_DOES_NOT_EXIST"]
        )
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
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
