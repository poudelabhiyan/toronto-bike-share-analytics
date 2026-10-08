-- Trips by hour of day: when is demand highest?
-- Answers: peak commuting hours for rebalancing decisions.
-- Note: timestamps are stored as 'M/D/YYYY H:MM', so the hour is parsed
-- from the text rather than with strftime.
SELECT CAST(SUBSTR(time_part, 1, INSTR(time_part, ':') - 1) AS INTEGER) AS hour,
       COUNT(*) AS trips
FROM (SELECT SUBSTR("Start Time", INSTR("Start Time", ' ') + 1) AS time_part
      FROM trips
      WHERE "Start Time" IS NOT NULL AND TRIM("Start Time") <> '')
GROUP BY hour
ORDER BY trips DESC;
