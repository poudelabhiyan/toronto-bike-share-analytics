import streamlit as st

def main():
    st.title("Toronto Bike-Sharing Dashboard")

    st.write("Dashboard is loading...")
    st.write("This is just a placeholder. Full layout will come in Sprint 2.")

    # Sidebar Filters
    st.sidebar.header("Filters")

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    station_filter = st.sidebar.text_input("Station Name (optional)")
    user_type_filter = st.sidebar.selectbox("User Type", ["All", "Member", "Casual"])

    # Main KPIs section
    st.header("Key Metrics")
    st.write("KPI cards will be displayed here.")

    # Charts Section
    st.header("Usage Charts")
    st.write("Charts will be added here after integration.")

    st.subheader("Peak Hour Chart")
    st.write("Placeholder for peak-hour chart")

    st.subheader("Station Usage Chart")
    st.write("Placeholder for station usage chart")

    st.subheader("Trip Duration Categories")
    st.write("Placeholder for duration bins chart")

if __name__ == "__main__":
    main()
