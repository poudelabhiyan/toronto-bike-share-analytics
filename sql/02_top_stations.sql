-- Top 10 named start stations by trip count.
-- Answers: where demand concentrates; unattributed trips excluded.
SELECT "Start Station Name" AS station,
       COUNT(*) AS trips
FROM trips
WHERE TRIM(COALESCE("Start Station Name", '')) NOT IN ('', 'Unknown')
  AND LOWER(TRIM(COALESCE("Start Station Name", ''))) NOT IN ('null', 'none', 'nan')
GROUP BY station
ORDER BY trips DESC
LIMIT 10;
