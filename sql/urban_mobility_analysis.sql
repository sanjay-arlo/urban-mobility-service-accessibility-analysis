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

DROP TABLE IF EXISTS station_accessibility_proxy;
CREATE TABLE station_accessibility_proxy (
  line VARCHAR(20),
  station VARCHAR(150),
  network_role VARCHAR(30),
  interchange_flag TINYINT,
  accessibility_proxy_score DECIMAL(6,2),
  accessibility_band VARCHAR(20)
);

-- Business Query 1: Monthly ridership trend
SELECT month, total_ridership
FROM cmrl_passenger_flow
ORDER BY month;

-- Business Query 2: MoM growth using LAG()
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

-- Business Query 3: Ticketing mix
SELECT month,
       ROUND(closed_loop * 100.0 / total_ridership, 2) AS closed_loop_pct,
       ROUND(qr_tickets * 100.0 / total_ridership, 2) AS qr_pct,
       ROUND(ncmc * 100.0 / total_ridership, 2) AS ncmc_pct
FROM cmrl_passenger_flow
ORDER BY month;

-- Business Query 4: Highest-demand months
SELECT month, total_ridership
FROM cmrl_passenger_flow
ORDER BY total_ridership DESC
LIMIT 10;

-- Business Query 5: Interchange stations
SELECT station, line, accessibility_proxy_score
FROM station_accessibility_proxy
WHERE interchange_flag = 1
ORDER BY accessibility_proxy_score DESC, station;

-- Business Query 6: Network-role mix
SELECT network_role, COUNT(*) AS station_count
FROM station_accessibility_proxy
GROUP BY network_role
ORDER BY station_count DESC;

-- Business Query 7: Average connectivity proxy by line
SELECT line, ROUND(AVG(accessibility_proxy_score), 2) AS avg_proxy_score
FROM station_accessibility_proxy
GROUP BY line
ORDER BY avg_proxy_score DESC;

-- Business Query 8: Screening candidates for further study
SELECT station, line, accessibility_proxy_score, accessibility_band
FROM station_accessibility_proxy
WHERE accessibility_band = 'Basic'
ORDER BY accessibility_proxy_score, station;

-- IMPORTANT: Accessibility proxy is a network-structure screening signal,
-- not a measured travel-time, equity, socioeconomic or service-quality score.
