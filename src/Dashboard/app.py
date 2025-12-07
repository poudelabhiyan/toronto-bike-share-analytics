import streamlit as st
import pandas as pd

#a samll change

#  NEW IMPORTS for US12
from src.data_processing.load import load_data
from src.analysis.kpis import compute_core_kpis
from src.analysis.peak_hours import compute_hourly_counts_for_range

# NEW IMPORTS for station usage + duration charts
from src.analysis.station_usage import compute_station_usage
from src.analysis.duration_bins import (
    compute_trip_durations,
    compute_duration_categories,
)


def main():
    st.title("Toronto Bike-Sharing Dashboard")

    st.write("Dashboard is loading...")
    st.write("This is just a placeholder. Full layout will come in Sprint 2.")

    # --- LOAD DATA ---
    df = load_data("data/bike_sharing.csv")

    # Sidebar Filters
    st.sidebar.header("Filters")

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    station_filter = st.sidebar.text_input("Station Name (optional)")
    user_type_filter = st.sidebar.selectbox("User Type", ["All", "Member", "Casual"])

    # --- APPLY DATE FILTER ---
    df_filtered = df.copy()

    if "Start Time" in df_filtered.columns:
        df_filtered["Start Time"] = pd.to_datetime(df_filtered["Start Time"])
        df_filtered = df_filtered[
            (df_filtered["Start Time"].dt.date >= start_date)
            & (df_filtered["Start Time"].dt.date <= end_date)
        ]

    # --- OPTIONAL STATION FILTER ---
    if station_filter and "Start Station Name" in df_filtered.columns:
        df_filtered = df_filtered[
            df_filtered["Start Station Name"].str.contains(
                station_filter, case=False, na=False
            )
        ]

    # --------------------
    #   KPI SECTION
    # --------------------
    st.header("Key Metrics")

    try:
        kpis = compute_core_kpis(df_filtered, timestamp_col="Start Time")

        col1, col2 = st.columns(2)
        col1.metric("Total Trips", kpis["total_trips"])
        col2.metric("Busiest Hour", kpis["peak_hour_string"])

    except Exception as e:
        st.write("Unable to compute KPIs:", e)

    # --------------------
    #   CHARTS SECTION
    # --------------------
    st.header("Usage Charts")

    # ---- Peak Hour Chart ----
    st.subheader("Peak Hour Chart")

    hourly_counts = compute_hourly_counts_for_range(
        df_filtered,
        timestamp_col="Start Time"
    )

    if not hourly_counts.empty:
        hourly_counts = hourly_counts.set_index("hour")
        st.bar_chart(hourly_counts["trip_count"])
    else:
        st.write("No data available for selected filters.")

    # ---- Station Usage Chart ----
    st.subheader("Station Usage Chart")

    try:
        usage = compute_station_usage(
            df_filtered,
            station_col="Start Station Name"
        )

        top_usage = usage.head(10)

        if not top_usage.empty:
            top_usage = top_usage.set_index("station")
            st.bar_chart(top_usage["trip_count"])
        else:
            st.write("No station data for selected filters.")

    except Exception as e:
        st.write("Unable to load station usage chart:", e)

    # ---- Trip Duration Categories ----
    st.subheader("Trip Duration Categories")

    try:
        df_durations = compute_trip_durations(
            df_filtered,
            start_col="Start Time",
            end_col="End Time",
        )

        df_bins = compute_duration_categories(df_durations)

        if not df_bins.empty:
            counts = (
                df_bins["duration_category"]
                .value_counts()
                .reindex(["Short", "Medium", "Long"])
                .fillna(0)
            )
            st.bar_chart(counts)
        else:
            st.write("No duration data for selected filters.")

    except Exception as e:
        st.write("Unable to load duration chart:", e)


if __name__ == "__main__":
    main()
