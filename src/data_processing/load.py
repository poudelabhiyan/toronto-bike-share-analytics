# functions for loading data
import pandas as pd
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Try UTF-8 first
    try:
        return pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        # Fallback for Windows encodings
        return pd.read_csv(path, encoding="latin1", low_memory=False)
