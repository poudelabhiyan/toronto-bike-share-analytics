# functions for loading data
import pandas as pd
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the bike-sharing dataset from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the dataset CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be read with supported encodings.
    """
    path = Path(file_path)

    # Check that the file exists
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Try reading with UTF-8, then fall back to latin1
    try:
        return pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        try:
            return pd.read_csv(path, encoding="latin1", low_memory=False)
        except Exception as exc:
            raise ValueError(f"Unable to read dataset: {exc}")
    except Exception as exc:
        raise ValueError(f"Unable to read dataset: {exc}")
      
