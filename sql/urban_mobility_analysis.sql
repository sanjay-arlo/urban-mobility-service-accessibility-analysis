CREATE DATABASE IF NOT EXISTS urban_mobility_analysis;
USE urban_mobility_analysis;

DROP TABLE IF EXISTS cmrl_passenger_flow;
CREATE TABLE cmrl_passenger_flow (
  month CHAR(7) PRIMARY KEY,
  closed_loop INT NOT NULL,
  qr_tickets INT NOT NULL,
  ncmc INT NOT NULL,
  total_ridership INT NOT NULL
);

DROP TABLE IF EXISTS gtfs_station_metrics;
CREATE TABLE gtfs_station_metrics (
  stop_id VARCHAR(150) PRIMARY KEY,
  station_name VARCHAR(200) NOT NULL,
  latitude DECIMAL(10,7),
  longitude DECIMAL(10,7),
  nearest_bus_stop_m DECIMAL(10,1),
  bus_stops_within_500m INT,
  nearest_bus_stop VARCHAR(200),
  nearest_bus_stop_id VARCHAR(150),
  metro_route_count INT,
  metro_trip_count INT,
  interchange_flag TINYINT,
  route_coverage_score DECIMAL(8,3),
  first_mile_proximity_score DECIMAL(8,3),
  bus_stop_density_score DECIMAL(8,3),
  network_first_mile_screening_index DECIMAL(8,2),
  first_mile_band VARCHAR(40)
);

DROP TABLE IF EXISTS gtfs_metro_segment_travel_times;
CREATE TABLE gtfs_metro_segment_travel_times (
  from_stop_id VARCHAR(150),
  to_stop_id VARCHAR(150),
  from_station VARCHAR(200),
  to_station VARCHAR(200),
  median_scheduled_travel_time_min DECIMAL(8,2),
  trip_observations INT,
  PRIMARY KEY (from_stop_id, to_stop_id)
);

-- 1. Monthly ridership trend
SELECT month, total_ridership
FROM cmrl_passenger_flow
ORDER BY month;

-- 2. MoM growth using LAG()
WITH x AS (
  SELECT month, total_ridership,
         LAG(total_ridership) OVER (ORDER BY month) AS previous_ridership
  FROM cmrl_passenger_flow
)
SELECT month, total_ridership,
       ROUND((total_ridership - previous_ridership) * 100.0 /
             NULLIF(previous_ridership, 0), 2) AS mom_growth_pct
FROM x
ORDER BY month;

-- 3. Ticketing mix
SELECT month,
       ROUND(closed_loop * 100.0 / NULLIF(total_ridership, 0), 2) AS closed_loop_pct,
       ROUND(qr_tickets * 100.0 / NULLIF(total_ridership, 0), 2) AS qr_pct,
       ROUND(ncmc * 100.0 / NULLIF(total_ridership, 0), 2) AS ncmc_pct
FROM cmrl_passenger_flow
ORDER BY month;

-- 4. Highest-demand months
SELECT month, total_ridership
FROM cmrl_passenger_flow
ORDER BY total_ridership DESC
LIMIT 10;

-- 5. Financial-year demand summary
WITH fy AS (
  SELECT *,
         CASE
           WHEN CAST(SUBSTRING(month,6,2) AS UNSIGNED) >= 4
             THEN CONCAT(SUBSTRING(month,1,4), '-', RIGHT(CAST(CAST(SUBSTRING(month,1,4) AS UNSIGNED) + 1 AS CHAR),2))
           ELSE CONCAT(CAST(CAST(SUBSTRING(month,1,4) AS UNSIGNED) - 1 AS CHAR), '-', RIGHT(SUBSTRING(month,1,4),2))
         END AS financial_year
  FROM cmrl_passenger_flow
)
SELECT financial_year,
       SUM(total_ridership) AS total_ridership,
       ROUND(AVG(total_ridership),0) AS avg_monthly_ridership,
       MAX(total_ridership) AS peak_month_ridership
FROM fy
GROUP BY financial_year
ORDER BY financial_year;

-- 6. Stations with weak first-mile proximity
SELECT station_name, nearest_bus_stop_m, bus_stops_within_500m,
       metro_route_count, interchange_flag,
       network_first_mile_screening_index
FROM gtfs_station_metrics
WHERE nearest_bus_stop_m > 500
ORDER BY nearest_bus_stop_m DESC;

-- 7. Strong first-mile / network screening candidates
SELECT station_name, nearest_bus_stop_m, bus_stops_within_500m,
       metro_route_count, interchange_flag,
       network_first_mile_screening_index
FROM gtfs_station_metrics
ORDER BY network_first_mile_screening_index DESC
LIMIT 15;

-- 8. Interchange and network coverage
SELECT station_name, metro_route_count, metro_trip_count,
       interchange_flag, network_first_mile_screening_index
FROM gtfs_station_metrics
ORDER BY metro_route_count DESC, metro_trip_count DESC;

-- 9. Scheduled metro travel-time hotspots
SELECT from_station, to_station,
       median_scheduled_travel_time_min, trip_observations
FROM gtfs_metro_segment_travel_times
ORDER BY median_scheduled_travel_time_min DESC
LIMIT 15;

-- 10. Planning screen: longer first-mile distance + limited nearby bus coverage
SELECT station_name, nearest_bus_stop_m, bus_stops_within_500m,
       metro_route_count, interchange_flag
FROM gtfs_station_metrics
WHERE nearest_bus_stop_m > 500
  AND bus_stops_within_500m <= 2
ORDER BY nearest_bus_stop_m DESC;

-- IMPORTANT:
-- GTFS scheduled travel time is timetable-derived, not observed traffic time.
-- First-mile distance is straight-line proximity to a GTFS bus stop, not walking-network travel time.
-- The screening index is an analytical prioritisation aid, not a transport-equity or service-quality score.
