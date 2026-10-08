# SQL analysis

Analytical SQL queries over the Toronto bike-share trip data. Each query answers
a defined business question and has been run against the full dataset
(`data/bike_sharing.csv`, 205,868 trips) — the results are quoted in the
repository README.

## How to run

Load the CSV into SQLite, then run any query file:

```bash
sqlite3 bikeshare.db <<'EOF'
.mode csv
.import --skip 1 data/bike_sharing.csv trips
EOF
sqlite3 bikeshare.db < sql/01_hourly_demand.sql
```

Or in Python (no extra install needed):

```python
import sqlite3, csv
con = sqlite3.connect(":memory:")
cur = con.cursor()
with open("data/bike_sharing.csv", encoding="latin1") as f:
    reader = csv.reader(f)
    cols = next(reader)
    cur.execute(f"CREATE TABLE trips ({', '.join('\"' + c + '\" TEXT' for c in cols)})")
    cur.executemany(f"INSERT INTO trips VALUES ({','.join('?' * len(cols))})", reader)
for row in cur.execute(open("sql/01_hourly_demand.sql").read()):
    print(row)
```

## Queries

| File | Question it answers | Result on the full data |
|---|---|---|
| `01_hourly_demand.sql` | When is demand highest? | Peak 17:00 (14,572 trips); quietest 04:00 (647) |
| `02_top_stations.sql` | Where does demand concentrate? | York St / Queens Quay W leads (1,288 trips) |
| `03_user_type_summary.sql` | Who rides and how do they differ? | Casual 91.2% @ 18.1 min avg; Annual 8.8% @ 11.4 min avg |
| `04_duration_mix.sql` | Quick hops or long rides? | 75.1% short (<20 min), 18.2% medium, 6.7% long |
| `05_data_quality.sql` | How complete is the extract? | 26.1% of rows are sparse; 28.2% lack station names |

Notes:

- Timestamps are stored as `M/D/YYYY H:MM` text, so `01_hourly_demand.sql`
  parses the hour from the string instead of using `strftime`.
- `Trip  Duration` (two spaces, as in the source file) is cast to a number
  before comparison — comparing it as text misclassifies durations.
- The queries treat blanks and placeholder strings (`NULL`, `None`) as missing.
