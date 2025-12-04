import streamlit as st
import pandas as pd

#  NEW IMPORTS for US12
from src.data_processing.load import load_data
from src.analysis.kpis import compute_core_kpis
from src.analysis.peak_hours import compute_hourly_counts_for_range


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

    # ---- Other placeholders (Sprint 2 work) ----
    st.subheader("Station Usage Chart")
    st.write("Placeholder for station usage chart")

    st.subheader("Trip Duration Categories")
    st.write("Placeholder for duration bins chart")


if __name__ == "__main__":
    main()
