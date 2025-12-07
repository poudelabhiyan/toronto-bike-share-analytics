Toronto Bike-Sharing Analytics Tool

A modular, test-driven analytical pipeline for processing, cleaning, analyzing, and visualizing Toronto Bike-Share trip-level data.
Built using Python, PyTest, and Streamlit. Designed following Agile SCRUM methodology with fully implemented Sprint 1 and Sprint 2 deliverables.

Table of Contents

Project Overview

Repository Structure

Sprint 1 Summary

Sprint 2 Summary

Installation

Running Tests

Dashboard Usage

Module Documentation

Future Enhancements

Contributors

License

1. Project Overview

This project provides a complete workflow to ingest the Toronto Bike Share dataset, clean it, generate descriptive analytics, and display insights through a modular dashboard.
The system uses a test-driven development approach with full PyTest coverage for reliability.

2. Repository Structure
Toronto-Bike-Analytics-Tool/
│
├── data/
│   └── bike_sharing.csv
│
├── src/
│   ├── analysis/
│   │   ├── peak_hours.py
│   │   ├── duration_categorization.py
│   │   ├── station_usage.py
│   │   └── __init__.py
│   │
│   ├── data_processing/
│   │   ├── load.py
│   │   ├── clean.py
│   │   ├── summary.py
│   │   └── visualize.py
│   │
│   ├── visualization/
│   │   ├── charts.py
│   │   └── __init__.py
│   │
│   └── dashboard/
│       ├── app.py
│       └── __init__.py
│
├── tests/
│   ├── test_load.py
│   ├── test_clean.py
│   ├── test_peak_hours.py
│   ├── test_duration_categorization.py
│   ├── test_station_usage.py
│   └── test_visualize.py
│
└── README.md

3. Sprint 1 Summary
Objective

Build the foundation of the data processing pipeline with proper TDD.

Deliverables
Component	Status	Description
Load module	Completed	Safe CSV loading with encoding fallback and required-column validation
Clean module	Completed	Standardization, type fixing, MAR/MCAR handling, outlier removal
PyTest setup	Completed	Base test suite created and passing
Repository scaffolding	Completed	Clean module structure and documentation
4. Sprint 2 Summary
Objective

Add analysis logic, visualization utilities, and the first version of the dashboard.

Deliverables
Component	Status	Description
Peak hour analysis	Completed	Hour extraction and hourly counts
Duration categorization	Completed	Short, medium, long classification
Station usage module	Completed	Trip count by station
Visualizations	Completed	Trip duration, peak hour histogram, station charts
Dashboard base	Completed	Layout, filters, KPIs
All tests	Completed	22 passing tests across modules
5. Installation
Clone the repository
git clone https://github.com/yourusername/Toronto-Bike-Analytics-Tool.git
cd Toronto-Bike-Analytics-Tool

Install dependencies
pip install -r requirements.txt

6. Running Tests

To run the full test suite:

pytest


Expected output:

======================== 22 passed in 6.13s ========================

7. Dashboard Usage

Run the Streamlit dashboard:

streamlit run src/dashboard/app.py


The dashboard includes:

Filters

KPIs

Duration charts

Station usage charts

Hourly trend charts

8. Module Documentation
Data Loading
from src.data_processing.load import load_data
df = load_data("data/bike_sharing.csv")

Data Cleaning

Includes:

Column normalization

Datetime parsing

Duration type conversion

Missing value imputation using MAR logic

Outlier removal

Analysis Modules

compute_hourly_counts

get_peak_hours

compute_station_usage

categorize_trip_duration

Visualization Modules

Trip duration distribution

Peak hour histogram

Station ranking charts

Duration vs hour scatter plot

Dashboard

Defined in src/dashboard/app.py with:

Sidebar filters

KPI section

Chart rendering

9. Future Enhancements

Station location map visualizations

Predictive analytics (forecasting demand)

Integration with external APIs

Improved interactive dashboard features

10. Contributors

Abhiyan Poudel (Product Owner)

Team Members: Devarsh, Yash, Bibal

11. License

This project is for academic purposes under the University of Niagara Falls Canada guidelines.
