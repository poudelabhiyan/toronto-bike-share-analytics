-- Demand and trip length by user type.
-- Answers: who rides (casual vs annual) and how their usage differs.
SELECT "User Type" AS user_type,
       COUNT(*) AS trips,
       ROUND(AVG(CAST("Trip  Duration" AS REAL)) / 60.0, 1) AS avg_minutes,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_trips
FROM trips
WHERE TRIM(COALESCE("User Type", '')) <> ''
  AND TRIM(COALESCE("Trip  Duration", '')) <> ''
GROUP BY user_type
ORDER BY trips DESC;
