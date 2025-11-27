# functions for loading data
import pandas as pd


def load_data(file_path: str = "data/bike sharing.csv") -> pd.DataFrame:
    """
    Load the Toronto Bike Share trip-level dataset.

    Parameters:
        file_path (str): Path to the CSV file. Defaults to 'data/bike sharing.csv'.

    Returns:
        pd.DataFrame: DataFrame containing the loaded dataset.
    """
    try:
        # Try UTF-8 first
        try:
            df = pd.read_csv(
                file_path,
                encoding="utf-8",
                low_memory=False
            )
        except UnicodeDecodeError:
            # Fallback for Excel/Windows-style encodings
            df = pd.read_csv(
                file_path,
                encoding="latin1",
                low_memory=False
            )

        # Optional: parse date-time columns if needed
        for col in ["Start Time", "End Time"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        print("Data loaded successfully.")
        return df

    except FileNotFoundError:
        print("Error: File not found. Check your file path.")
    except Exception as e:
        print(f"Unexpected error while loading data: {e}")


if name == "main":
    # When you run: python src/data_processing/load.py
    df = load_data()

    if df is not None:
        print("\nFirst 5 rows:")
        print(df.head())

        print("\nColumns in the dataset:")
        print(df.columns)

        print("\nDataset shape (rows, columns):")
        print(df.shape)
