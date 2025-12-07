# Toronto Bike-Sharing Analytics Tool

A modular, test-driven analytical pipeline for processing, cleaning, analyzing, and visualizing Toronto Bike-Share trip-level data. The project is built using Python, PyTest, and Streamlit, following Agile SCRUM methodology with fully completed Sprint 1 and Sprint 2 deliverables.

## Table of Contents

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

## Project Overview

This project provides a complete, modular workflow that processes the Toronto Bike-Sharing dataset from raw CSV to a fully interactive analytics dashboard. The system is test-driven and includes data loading, cleaning, descriptive analysis, visualization, and dashboard implementation.

## Repository Structure

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

## Sprint 1 Summary
Objective

Develop the foundational data ingestion and cleaning pipeline using Test-Driven Development.

## Completed Deliverables
## Component	Description

### Load Module	CSV loading with fallback encodings and required-column validation

### Clean Module	Standardization, MAR/MCAR filling, type enforcement, outlier removal

### Project Structure	Organized into analysis, processing, dashboard, and tests

### Test Suite	Initial PyTest cases ensuring data integrity and module reliability

## Sprint 2 Summary
Objective

Implement analytical modules, visualization utilities, and an initial interactive dashboard.

## Completed Deliverables
## Component	Description

### Peak Hour Analysis	Extract and aggregate trip counts by hour
### Duration Categorization	Classify trips into short, medium, long
### Station Usage	Compute station-level demand metrics
### Visualization Library	Histogram, bar charts, duration distribution
### Streamlit Dashboard	Fully functional UI with KPIs, filters, and charts
### Expanded Test Coverage	All modules validated with passing tests

## Installation
Clone the Repository
git clone https://github.com/yourusernam/Toronto-Bike-Analytics-Tool.git
cd Toronto-Bike-Analytics-Tool

## Install Dependencies
pip install -r requirements.txt

## Running Tests
Execute the full PyTest suite
pytest


## Expected output:

22 passed in X.XXs

## Dashboard Usage
Launch Streamlit
streamlit run src/dashboard/app.py


## Dashboard Features:

Sidebar filters (date range, station, user type)

Key metrics (total trips, unique stations, busiest hour, date range)

Peak hour ridership visualization

Top stations usage chart

Duration category distribution

Filtered data preview

## Module Documentation
1. Data Loading
from src.data_processing.load import load_data
df = load_data("data/bike_sharing.csv")

2. Data Cleaning

Includes:

Column normalization

Datetime and numeric fixes

Missing value handling using MAR logic

Outlier trimming using quantiles

3. Analysis Modules

Functions:

compute_hourly_counts

get_peak_hours

compute_station_usage

categorize_trip_duration

4. Visualization

Includes:

Trip duration histograms

Peak hour bar charts

Station usage charts

5. Dashboard

The Streamlit app in app.py integrates all modules into an end-to-end interface.

##Future Enhancements

Add predictive modeling (e.g., demand forecasting)

Integrate geospatial mapping

Add real-time API ingestion

Build multi-page dashboard architecture

##Contributors

Abhiyan Poudel

Devarsh

Bibal

Yash

##License

This project is created for academic purposes under the University of Niagara Falls Canada guidelines.
