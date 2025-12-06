import pandas as pd
from src.data_processing.visualize import plot_trip_duration


def test_plot_trip_duration_runs():
    df = pd.read_csv("data/bike_sharing.csv", encoding="latin1", low_memory=False)

    fig = plot_trip_duration(df, "Trip  Duration", max_duration_sec=6000)

    # The function should return a matplotlib Figure
    assert fig is not None
<<<<<<< HEAD
=======
# tests for visualizations
>>>>>>> b1ec868e132260de9f1142f38dc2aeca281cd73e
