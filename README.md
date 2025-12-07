Toronto Bike-Sharing Analytics Tool

A modular, test-driven analytical pipeline for processing, cleaning, analyzing, and visualizing Toronto Bike-Share trip-level data. Built using Python, PyTest, and Streamlit. Designed following Agile SCRUM methodology with fully implemented Sprint 1 and Sprint 2 deliverables.

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

Project Overview

This project provides a complete workflow to ingest the Toronto Bike Share dataset, clean it, generate descriptive analytics, and present insights in an interactive Streamlit dashboard. The system is fully test-driven, with modules validated by PyTest.

Repository Structure
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

Sprint 1 Summary
Objective

Build the core data ingestion and cleaning modules using TDD.

Deliverables
Component	Status	Description
Load module	Completed	CSV loading with encoding fallback and required-column validation
Clean module	Completed	Name standardization, missing value handling (MAR/MCAR), type fixing
PyTest suite	Completed	Foundational test files and passing tests
Project structure	Completed	Modular package layout with folders for processing, analysis, and tests
Sprint 2 Summary
Objective

Implement analysis modules, visualization utilities, and the initial dashboard structure.

Deliverables
Component	Status	Description
Peak hour analysis	Completed	Hour extraction and hourly aggregation
Duration categorization	Completed	Classification into short, medium, and long
Station usage	Completed	Trip count per station
Visualization utilities	Completed	Histograms, bar charts, duration distribution
Streamlit dashboard	Completed	KPIs, filters, layout, and charts
Test coverage	Completed	All analysis modules tested; 22 tests passing
Installation
Clone the repository
git clone https://github.com/yourusername/Toronto-Bike-Analytics-Tool.git
cd Toronto-Bike-Analytics-Tool

Install dependencies
pip install -r requirements.txt

Running Tests

Run full test suite:

pytest


Expected result:

22 passed in X.XXs

Dashboard Usage

Run the Streamlit app:

streamlit run src/dashboard/app.py


Features include:

Sidebar filters

Trip KPIs

Peak hour chart

Station rankings

Duration category chart

Data preview

Module Documentation
Data Loading
from src.data_processing.load import load_data
df = load_data("data/bike_sharing.csv")

Cleaning Module

Includes:

Column normalization

Datetime and numeric parsing

Missing value imputation using MAR logic

Outlier trimming using quantiles

Analysis Modules

compute_hourly_counts

get_peak_hours

compute_station_usage

categorize_trip_duration

Visualization

Trip duration histograms

Peak hour histograms

Station usage bar charts

Dashboard

app.py contains full layout and rendering logic

Future Enhancements

Geographic visualizations

Predictive modelling

API integration

Time-series forecasting

Contributors

Abhiyan Poudel

Devarsh

Yash

Bibal

License

This project is created for academic use under the University of Niagara Falls Canada guidelines.
