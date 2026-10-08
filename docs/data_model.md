# Data model

## Source table: `trips`

One row per bike-share trip, loaded from `data/bike_sharing.csv`
(205,868 rows, 2024-08-01 to 2024-08-06).

| Column | Type | Description |
|---|---|---|
| Trip Id | integer | Trip identifier. Missing in 26.1% of rows (sparse extract rows). |
| Trip  Duration | integer (seconds) | Trip length. Note the two spaces in the source header. Median 725 s (~12 min). |
| Start Station Id | integer | Origin station id. Missing where the trip is unattributed. |
| Start Time | datetime (`M/D/YYYY H:MM`) | Trip start. Parsed to datetime on load. |
| Start Station Name | text | Origin station name. 28.2% missing/placeholder — see cleaning rules. |
| End Station Id | integer | Destination station id. |
| End Time | datetime (`M/D/YYYY H:MM`) | Trip end. |
| End Station Name | text | Destination station name. Same missingness pattern as start. |
| Bike Id | integer | Bike identifier. |
| User Type | text | `Casual Member` (91.2%) or `Annual Member` (8.8%). |
| Model | text | Bike model: ICONIC, EFIT G5, EFIT. |

There are no enforced keys in the flat file; `Trip Id` is the natural row
identifier where present.

## Cleaning rules (`src/data_processing/clean.py`)

1. Column names are stripped of leading/trailing whitespace (internal spacing
   such as `Trip  Duration` is preserved so downstream code keeps working).
2. Station names: blank strings and placeholders (`NULL`, `None`, `nan`,
   case-insensitive) are treated as missing, then filled from a
   station-id → station-name mapping built from rows where the name is known.
   Names that still cannot be resolved become `Unknown`.
3. Timestamps are parsed to datetime with invalid values coerced to missing.
4. Cleaning never mutates the input DataFrame (works on a copy).

Known data-quality facts (see `sql/05_data_quality.sql`):

- 53,759 rows (26.1%) are sparse: no trip id, duration, timestamps, or user type.
- 58,064 trips (28.2%) have no attributable start station, even after
  id-based resolution — station-level analysis excludes these.

## Power BI companion notes

The flat `trips` table maps directly to a Power BI star schema:

- **Fact table:** `trips` (one row per trip).
- **Dimensions:** `dim_station` (station id → name, from the cleaned mapping),
  `dim_time` (date, hour, weekday derived from Start Time),
  `dim_user` (user type), `dim_bike` (bike id → model).
- **Relationships:** fact → dimensions on station id, date, user type, bike id
  (single-direction, many-to-one).
- **Measures (DAX):**
  - `Total Trips = COUNTROWS(trips)`
  - `Avg Duration (min) = AVERAGE(trips[Trip  Duration]) / 60`
  - `Peak Hour Trips = CALCULATE([Total Trips], dim_time[hour] = 17)`
  - `% Unattributed = DIVIDE(CALCULATE([Total Trips], dim_station[name] = "Unknown"), [Total Trips])`
- **Power Query steps:** strip column whitespace, parse `M/D/YYYY H:MM`
  timestamps, apply the station-name resolution above, derive hour/weekday.

A `.pbix` implementing this model is a planned next step; the SQL queries in
`sql/` already answer the core business questions against the same model.
