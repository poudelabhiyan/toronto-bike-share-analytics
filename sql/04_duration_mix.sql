-- Trip duration mix: short (<20 min), medium (20-40 min), long (>40 min).
-- Answers: are bikes used for quick hops or longer rides?
SELECT CASE
         WHEN CAST("Trip  Duration" AS INTEGER) < 1200 THEN 'short (<20 min)'
         WHEN CAST("Trip  Duration" AS INTEGER) <= 2400 THEN 'medium (20-40 min)'
         ELSE 'long (>40 min)'
       END AS duration_bucket,
       COUNT(*) AS trips,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_trips
FROM trips
WHERE TRIM(COALESCE("Trip  Duration", '')) <> ''
  AND CAST("Trip  Duration" AS INTEGER) >= 0
GROUP BY duration_bucket
ORDER BY trips DESC;
