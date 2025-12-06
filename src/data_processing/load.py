import pandas as pd
from pathlib import Path
from typing import List, Optional


def load_data(file_path: str, required_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Load the bike-sharing dataset from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the dataset CSV file.
    required_columns : list of str, optional
        List of column names that must be present in the dataset.
        If any are missing, a ValueError is raised.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be read with supported encodings
        or if required columns are missing.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Try reading with UTF-8, then fall back to latin1
    try:
        df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding="latin1", low_memory=False)
        except Exception as exc:
            raise ValueError(f"Unable to read dataset: {exc}")
    except Exception as exc:
        raise ValueError(f"Unable to read dataset: {exc}")

<<<<<<< HEAD
    # US9: validate required columns, if provided
=======
    # US9: Validate required columns
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

<<<<<<< HEAD

=======
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
    return df
