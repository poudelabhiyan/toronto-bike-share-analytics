import pandas as pd
import matplotlib.pyplot as plt


def plot_trip_duration(
    df: pd.DataFrame,
    duration_col: str,
    max_duration_sec: int = 6000,
) -> plt.Figure:
    """
    Plot the distribution of trip duration (in minutes) with key percentiles.

    Parameters
    ----------
    df : pd.DataFrame
        Bike-sharing dataset.
    duration_col : str
        Name of the column that contains trip duration values (in seconds).
    max_duration_sec : int, optional
        Maximum duration (in seconds) to include in the plot to remove
        extreme outliers. Defaults to 6000 seconds (~100 minutes).

    Returns
    -------
    matplotlib.figure.Figure
        Figure object with the duration distribution plot.
    """
    # 1) Select and clean the series
    durations = df[duration_col].dropna()

    # 2) Remove extreme outliers so the plot is readable
    if max_duration_sec is not None:
        durations = durations[durations <= max_duration_sec]

    # 3) Convert to minutes for easier interpretation
    durations_min = durations / 60

    # 4) Basic stats for annotations
    median = durations_min.median()
    p90 = durations_min.quantile(0.90)

    # 5) Build the plot
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(durations_min, bins=50, edgecolor="black")
    ax.axvline(median, color="red", linestyle="--",
               label=f"Median: {median:.1f} min")
    ax.axvline(p90, color="orange", linestyle="--",
               label=f"90th percentile: {p90:.1f} min")

    ax.set_title("Trip Duration Distribution (capped, in minutes)")
    ax.set_xlabel("Trip duration (minutes)")
    ax.set_ylabel("Number of trips")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.legend()

    fig.tight_layout()
    return fig
