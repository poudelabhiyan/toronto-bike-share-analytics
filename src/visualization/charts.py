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
    if duration_col not in df.columns:
        raise KeyError(f"'{duration_col}' column not found in DataFrame.")

    # 1) Select and clean the series
    durations = df[duration_col].dropna()

    # 2) Remove extreme outliers so the plot is readable
    if max_duration_sec is not None:
        durations = durations[durations <= max_duration_sec]

    if durations.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5,
            0.5,
            "No duration data available for plotting.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

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


def plot_peak_hour_histogram(df: pd.DataFrame) -> plt.Figure:
    """
    Plot a histogram of trip counts by hour of the day.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset containing a 'Start Time' column.

    Returns
    -------
    matplotlib.figure.Figure
        Histogram figure showing distribution of ridership by hour.
    """
    if "Start Time" not in df.columns:
        raise KeyError("Start Time column is required for peak hour visualization.")

    df_local = df.copy()
    df_local["Start Time"] = pd.to_datetime(df_local["Start Time"], errors="coerce")
    df_local = df_local.dropna(subset=["Start Time"])

    if df_local.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5,
            0.5,
            "No Start Time data available for plotting.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    df_local["hour"] = df_local["Start Time"].dt.hour
    hours = df_local["hour"].dropna()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(hours, bins=24, edgecolor="black", color="#4ba3ff")

    ax.set_title("Distribution of Ridership by Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Trips")
    ax.set_xticks(range(0, 24, 1))
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    fig.tight_layout()
    return fig


def plot_top_stations(df_usage: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    """
    Plot a bar chart of the top N busiest start stations.

    Parameters
    ----------
    df_usage : pd.DataFrame
        Output of compute_station_usage() with columns ["station", "trip_count"].
    top_n : int
        Number of top stations to plot.

    Returns
    -------
    matplotlib.figure.Figure
        Bar chart of top N stations.
    """
    required_cols = {"station", "trip_count"}
    if not required_cols.issubset(df_usage.columns):
        raise KeyError(
            f"df_usage must contain columns {required_cols}, "
            f"found {list(df_usage.columns)}"
        )

    df_top = df_usage.head(top_n)

    if df_top.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5,
            0.5,
            "No station usage data available.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_top["station"], df_top["trip_count"], color="#a855f7")

    ax.set_title(f"Top {top_n} Busiest Start Stations")
    ax.set_xlabel("Station")
    ax.set_ylabel("Trip Count")
    ax.set_xticklabels(df_top["station"], rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    fig.tight_layout()
    return fig


def plot_duration_category_distribution(df: pd.DataFrame) -> plt.Figure:
    """
    Plot the number of trips in each duration category.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a 'duration_category' column from categorize_trip_duration().

    Returns
    -------
    matplotlib.figure.Figure
        Bar chart of short/medium/long distribution.
    """
    if "duration_category" not in df.columns:
        raise KeyError("duration_category column not found.")

    counts = (
        df["duration_category"]
        .value_counts()
        .reindex(["short", "medium", "long"])
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(counts.index, counts.values, color="#22c55e", edgecolor="black")

    ax.set_title("Trip Duration Category Distribution")
    ax.set_xlabel("Duration Category")
    ax.set_ylabel("Number of Trips")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    fig.tight_layout()
    return fig


def plot_daily_trends(df: pd.DataFrame) -> plt.Figure:
    """
    Plot total number of trips per day.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing a 'Start Time' column.

    Returns
    -------
    matplotlib.figure.Figure
        Line chart of daily ridership trends.
    """
    if "Start Time" not in df.columns:
        raise KeyError("Start Time column is required.")

    df_local = df.copy()
    df_local["Start Time"] = pd.to_datetime(df_local["Start Time"], errors="coerce")
    df_local = df_local.dropna(subset=["Start Time"])

    if df_local.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5,
            0.5,
            "No Start Time data available for plotting.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    df_local["date"] = df_local["Start Time"].dt.date
    daily_counts = df_local.groupby("date").size()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_counts.index, daily_counts.values, linewidth=2, color="#4ba3ff")

    ax.set_title("Daily Trip Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Trips")
    ax.grid(True, linestyle="--", alpha=0.6)

    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_duration_vs_hour(df: pd.DataFrame, duration_col: str) -> plt.Figure:
    """
    Scatter plot of trip duration (min) vs starting hour.

    Parameters
    ----------
    df : pd.DataFrame
        Clean dataset with Start Time and trip duration column.
    duration_col : str
        Trip duration column in seconds.

    Returns
    -------
    matplotlib.figure.Figure
        Scatter plot figure.
    """
    if "Start Time" not in df.columns:
        raise KeyError("Start Time column is required.")
    if duration_col not in df.columns:
        raise KeyError(f"{duration_col} column not found in DataFrame.")

    df_local = df.copy()
    df_local["Start Time"] = pd.to_datetime(df_local["Start Time"], errors="coerce")
    df_local = df_local.dropna(subset=["Start Time"])

    if df_local.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5,
            0.5,
            "No data available for plotting duration vs hour.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    df_local["hour"] = df_local["Start Time"].dt.hour
    df_local["duration_min"] = df_local[duration_col] / 60.0

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df_local["hour"], df_local["duration_min"], alpha=0.4, color="#f59e0b")

    ax.set_title("Trip Duration (minutes) vs Start Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Trip Duration (minutes)")
    ax.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    return fig


__all__ = [
    "plot_trip_duration",
    "plot_peak_hour_histogram",
    "plot_top_stations",
    "plot_duration_category_distribution",
    "plot_daily_trends",
    "plot_duration_vs_hour",
]
