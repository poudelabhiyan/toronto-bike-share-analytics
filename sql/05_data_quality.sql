-- Data-quality audit: missingness per column.
-- Answers: how much of the extract is usable for station-level analysis.
-- (Blanks and placeholder strings like 'NULL' both count as missing.)
WITH cleaned AS (
  SELECT
    NULLIF(TRIM(COALESCE("Trip Id", '')), '') AS trip_id,
    NULLIF(TRIM(COALESCE("Trip  Duration", '')), '') AS duration,
    NULLIF(TRIM(COALESCE("Start Station Id", '')), '') AS start_id,
    CASE WHEN LOWER(TRIM(COALESCE("Start Station Name", ''))) IN ('', 'unknown', 'null', 'none', 'nan')
         THEN NULL ELSE TRIM("Start Station Name") END AS start_name,
    NULLIF(TRIM(COALESCE("Start Time", '')), '') AS start_time,
    NULLIF(TRIM(COALESCE("User Type", '')), '') AS user_type
  FROM trips
),
total AS (SELECT COUNT(*) AS n FROM cleaned)
SELECT 'Trip Id' AS column_name,
       (SELECT n FROM total) - COUNT(trip_id) AS missing_values,
       ROUND(100.0 * ((SELECT n FROM total) - COUNT(trip_id)) / (SELECT n FROM total), 1) AS missing_pct
FROM cleaned
UNION ALL SELECT 'Trip Duration', (SELECT n FROM total) - COUNT(duration), ROUND(100.0 * ((SELECT n FROM total) - COUNT(duration)) / (SELECT n FROM total), 1) FROM cleaned
UNION ALL SELECT 'Start Station Id', (SELECT n FROM total) - COUNT(start_id), ROUND(100.0 * ((SELECT n FROM total) - COUNT(start_id)) / (SELECT n FROM total), 1) FROM cleaned
UNION ALL SELECT 'Start Station Name', (SELECT n FROM total) - COUNT(start_name), ROUND(100.0 * ((SELECT n FROM total) - COUNT(start_name)) / (SELECT n FROM total), 1) FROM cleaned
UNION ALL SELECT 'Start Time', (SELECT n FROM total) - COUNT(start_time), ROUND(100.0 * ((SELECT n FROM total) - COUNT(start_time)) / (SELECT n FROM total), 1) FROM cleaned
UNION ALL SELECT 'User Type', (SELECT n FROM total) - COUNT(user_type), ROUND(100.0 * ((SELECT n FROM total) - COUNT(user_type)) / (SELECT n FROM total), 1) FROM cleaned;
