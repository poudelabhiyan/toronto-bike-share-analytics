import sys
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st
import altair as alt

# -------------------------------------------------------------------
# Ensure project root is in sys.path so "src" imports work
# -------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]  # .../Toronto-Bike-Analytics-Tool
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# -------------------------------------------------------------------
# Project imports
# -------------------------------------------------------------------
from src.data_processing.load import load_data
from src.data_processing.clean import clean_data
from src.analysis.peak_hours import compute_hourly_counts
from src.analysis.station_usage import compute_station_usage
from src.analysis.duration_categorization import categorize_trip_duration

DATA_PATH = ROOT_DIR / "data" / "bike_sharing.csv"


# -------------------------------------------------------------------
# Data loading with caching
# -------------------------------------------------------------------
@st.cache_data
def get_clean_data() -> pd.DataFrame:
    """
    Load and clean the bike-sharing dataset once, then cache it.
    """
    df_raw = load_data(str(DATA_PATH))
    df_clean = clean_data(df_raw)

    # Safety: ensure Start Time / End Time are datetime
    for col in ["Start Time", "End Time"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

    return df_clean


# -------------------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------------------
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render sidebar filters and return the filtered DataFrame.
    Filters:
    - Date range (Start Time)
    - Station name (text contains)
    - User Type
    """
    st.sidebar.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)

    df_filtered = df.copy()

    # Date range filter
    if "Start Time" in df_filtered.columns:
        min_date = df_filtered["Start Time"].min().date()
        max_date = df_filtered["Start Time"].max().date()

        start_date, end_date = st.sidebar.date_input(
            "Trip start date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        mask_date = (df_filtered["Start Time"].dt.date >= start_date.date()) & (
            df_filtered["Start Time"].dt.date <= end_date.date()
        )
        df_filtered = df_filtered.loc[mask_date]

    # Station filter (contains substring)
    station_filter = st.sidebar.text_input("Station name contains (optional)")
    if station_filter and "Start Station Name" in df_filtered.columns:
        df_filtered = df_filtered[
            df_filtered["Start Station Name"]
            .astype(str)
            .str.contains(station_filter, case=False, na=False)
        ]

    # User Type filter
    user_col = "User Type"
    if user_col in df_filtered.columns:
        user_types: List[str] = sorted(df_filtered[user_col].dropna().unique().tolist())
        selected_user = st.sidebar.selectbox(
            "User Type",
            options=["All"] + user_types,
            index=0,
        )
        if selected_user != "All":
            df_filtered = df_filtered[df_filtered[user_col] == selected_user]

    return df_filtered


# -------------------------------------------------------------------
# KPI calculations
# -------------------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Compute simple KPIs from the filtered DataFrame.
    """
    if df.empty:
        return {
            "total_trips": 0,
            "unique_stations": 0,
            "date_range": "No data",
            "busiest_hour": "No data",
        }

    total_trips = len(df)

    station_col = "Start Station Name"
    unique_stations = df[station_col].nunique() if station_col in df.columns else 0

    if "Start Time" in df.columns:
        min_date = df["Start Time"].min().date()
        max_date = df["Start Time"].max().date()
        date_range = f"{min_date} → {max_date}"

        hourly = compute_hourly_counts(df, timestamp_col="Start Time")
        if not hourly.empty:
            max_count = hourly["trip_count"].max()
            peak_hours = hourly.loc[hourly["trip_count"] == max_count, "hour"].tolist()
            busiest_hour = ", ".join(f"{h:02d}:00" for h in peak_hours)
        else:
            busiest_hour = "No data"
    else:
        date_range = "N/A"
        busiest_hour = "No Start Time"

    return {
        "total_trips": total_trips,
        "unique_stations": unique_stations,
        "date_range": date_range,
        "busiest_hour": busiest_hour,
    }


# -------------------------------------------------------------------
# Main layout
# -------------------------------------------------------------------
def main() -> None:
    st.set_page_config(
        page_title="Toronto Bike-Sharing Analytics Dashboard",
        layout="wide",
    )

    # --------- Global styling (dark professional theme) ----------
    st.markdown(
        """
        <style>
        :root {
            --bg-primary: #050711;
            --bg-card: #121420;
            --bg-card-soft: #181b2a;
            --border-card: #262a3a;
            --accent: #4ba3ff;
            --accent-soft: rgba(75, 163, 255, 0.18);
            --text-main: #e5e7eb;
            --text-muted: #9ca3af;
        }

        [data-testid="stAppViewContainer"] {
            background-color: var(--bg-primary);
        }

        [data-testid="stSidebar"] {
            background-color: #0b0f19;
        }

        .sidebar-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 1rem;
        }

        .big-title {
            font-size: 36px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 0.2rem;
        }

        .sub-caption {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 1.2rem;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 1.5rem;
            margin-bottom: 0.4rem;
        }

        .kpi-card {
            background: linear-gradient(145deg, #151827, #101322);
            padding: 0.9rem 1rem;
            border-radius: 14px;
            border: 1px solid var(--border-card);
            box-shadow: 0 0 18px rgba(0,0,0,0.45);
        }

        .kpi-label {
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.15rem;
        }

        .kpi-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-main);
        }

        .kpi-subvalue {
            font-size: 13px;
            color: var(--text-muted);
        }

        .chart-card {
            background-color: var(--bg-card);
            padding: 1rem 1.2rem;
            border-radius: 14px;
            border: 1px solid var(--border-card);
            box-shadow: 0 0 18px rgba(0,0,0,0.35);
        }

        .chart-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 0.6rem;
        }

        .data-expander > div {
            background-color: var(--bg-card-soft) !important;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title
    st.markdown('<div class="big-title">Toronto Bike-Sharing Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-caption">Interactive view of ridership patterns, station usage, and trip durations.</div>',
        unsafe_allow_html=True,
    )

    # Load data
    try:
        df = get_clean_data()
    except FileNotFoundError:
        st.error(f"Could not find data file at: {DATA_PATH}")
        return
    except Exception as exc:
        st.error(f"Error loading data: {exc}")
        return

    # Apply filters
    df_filtered = apply_filters(df)

    # ------------------------------------------------------------------
    # KPI SECTION
    # ------------------------------------------------------------------
    st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)

    kpis = compute_kpis(df_filtered)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Trips</div>
                <div class="kpi-value">{kpis['total_trips']:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Unique Start Stations</div>
                <div class="kpi-value">{kpis['unique_stations']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Date Range</div>
                <div class="kpi-value" style="font-size:18px;">{kpis['date_range']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Busiest Hour(s)</div>
                <div class="kpi-value" style="font-size:20px;">{kpis['busiest_hour']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    # ------------------------------------------------------------------
    # CHARTS SECTION
    # ------------------------------------------------------------------
    st.markdown('<div class="section-title">Usage Overview</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    # Peak hour chart
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Peak Hour Ridership</div>', unsafe_allow_html=True)
        try:
            hourly_counts = compute_hourly_counts(df_filtered, timestamp_col="Start Time")
            if not hourly_counts.empty:
                peak_chart = (
                    alt.Chart(hourly_counts)
                    .mark_bar(color="#4ba3ff")
                    .encode(
                        x=alt.X("hour:O", title="Hour of day"),
                        y=alt.Y("trip_count:Q", title="Number of trips"),
                        tooltip=["hour", "trip_count"],
                    )
                    .properties(height=280)
                )
                st.altair_chart(peak_chart, use_container_width=True)
            else:
                st.info("No data for peak hours in the selected range.")
        except Exception as e:
            st.error(f"Unable to load peak hour chart: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Station usage chart
    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top 10 Start Stations</div>', unsafe_allow_html=True)
        try:
            usage = compute_station_usage(df_filtered, station_col="Start Station Name")

            # Remove "Unknown" from ranking so it does not dominate the chart
            usage = usage[usage["station"] != "Unknown"]

            top_usage = usage.head(10)

            if not top_usage.empty:
                station_chart = (
                    alt.Chart(top_usage)
                    .mark_bar(color="#a855f7")
                    .encode(
                        x=alt.X("station:N", sort="-y", title="Station"),
                        y=alt.Y("trip_count:Q", title="Number of trips"),
                        tooltip=["station", "trip_count"],
                    )
                    .properties(height=280)
                ).configure_axisX(labelAngle=-45)
                st.altair_chart(station_chart, use_container_width=True)
            else:
                st.info("No station usage data (excluding 'Unknown') for the selected filters.")
        except Exception as e:
            st.error(f"Unable to load station usage chart: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Duration categories chart
    st.markdown('<div class="section-title">Trip Duration Categories</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    try:
        # Note: column name has two spaces in your dataset: "Trip  Duration"
        df_duration = categorize_trip_duration(
            df_filtered,
            duration_col="Trip  Duration",
        )

        if "duration_category" in df_duration.columns:
            counts = (
                df_duration["duration_category"]
                .value_counts()
                .reindex(["short", "medium", "long"])
                .fillna(0)
                .reset_index()
            )
            counts.columns = ["duration_category", "trip_count"]

            duration_chart = (
                alt.Chart(counts)
                .mark_bar(color="#22c55e")
                .encode(
                    x=alt.X("duration_category:N", title="Category"),
                    y=alt.Y("trip_count:Q", title="Number of trips"),
                    tooltip=["duration_category", "trip_count"],
                )
                .properties(height=260)
            )
            st.altair_chart(duration_chart, use_container_width=True)
        else:
            st.info("No duration category data available.")
    except KeyError:
        st.info("Trip Duration column not found; cannot compute duration categories.")
    except Exception as e:
        st.error(f"Unable to load duration categories chart: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Data preview
    # ------------------------------------------------------------------
    with st.expander("View filtered data sample", expanded=False):
        st.dataframe(df_filtered.head(20))


if __name__ == "__main__":
    main()
