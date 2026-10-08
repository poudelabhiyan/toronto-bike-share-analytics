# Toronto Bike-Share Analytics

End-to-end analytics pipeline for Toronto bike-share data: cleaning, ridership analysis, visualizations, and a Streamlit dashboard. Built with Python, pandas, and pytest using test-driven development.

## Features

- Load Toronto bike-share trip data from CSV
- Clean and prepare data (handle missing values, standardize formats, remove outliers)
- Ridership analysis: peak hours, trip duration categories, station usage
- Visualizations: histograms, bar charts, demand charts
- Interactive Streamlit dashboard with filters and KPIs
- Full pytest test suite

## Installation

Clone the repository:
```
git clone https://github.com/poudelabhiyan/toronto-bike-share-analytics.git
cd toronto-bike-share-analytics
```

Install dependencies:
```
pip install -r requirements.txt
```

## Running Tests

```
pytest
```

## Dashboard

Launch the Streamlit dashboard:
```
streamlit run src/dashboard/app.py
```

Features: sidebar filters (date range, station, user type), KPIs (total trips, unique stations, busiest hour), peak-hour charts, top stations, duration distribution, and data preview.

## Project Structure

- `data/` — bike_sharing.csv dataset
- `src/data_processing/` — load, clean, summary, visualize modules
- `src/analysis/` — peak hours, duration categorization, station usage
- `src/visualization/` — chart utilities
- `src/dashboard/` — Streamlit app
- `tests/` — pytest suite
- `requirements.txt` — Python dependencies
- `LICENSE` — MIT License

## License

MIT — see LICENSE file.
