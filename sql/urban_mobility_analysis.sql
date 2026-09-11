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
  line VARCHAR(20) NOT NULL,
  station VARCHAR(150) NOT NULL,
  network_role VARCHAR(30) NOT NULL,
  interchange_flag TINYINT NOT NULL,
  accessibility_proxy_score DECIMAL(6,2) NOT NULL,
  accessibility_band VARCHAR(40) NOT NULL
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

-- 3. Ticketing mix by month
SELECT month,
       ROUND(closed_loop * 100.0 / NULLIF(total_ridership,0), 2) AS closed_loop_pct,
       ROUND(qr_tickets * 100.0 / NULLIF(total_ridership,0), 2) AS qr_pct,
       ROUND(ncmc * 100.0 / NULLIF(total_ridership,0), 2) AS ncmc_pct
FROM cmrl_passenger_flow
ORDER BY month;

-- 4. Highest-demand months
SELECT month, total_ridership
FROM cmrl_passenger_flow
ORDER BY total_ridership DESC
LIMIT 10;

-- 5. Financial-year demand summary (financial year must be derived from month)
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

-- 6. Interchange stations
SELECT station,
       GROUP_CONCAT(DISTINCT line ORDER BY line SEPARATOR ', ') AS lines,
       MAX(accessibility_proxy_score) AS proxy_score
FROM station_accessibility_proxy
WHERE interchange_flag = 1
GROUP BY station
ORDER BY proxy_score DESC, station;

-- 7. Network-role mix
SELECT network_role,
       COUNT(*) AS station_count,
       ROUND(AVG(accessibility_proxy_score), 2) AS avg_proxy_score
FROM station_accessibility_proxy
GROUP BY network_role
ORDER BY station_count DESC;

-- 8. Average proxy by line
SELECT line,
       COUNT(*) AS station_count,
       ROUND(AVG(accessibility_proxy_score), 2) AS avg_proxy_score,
       SUM(interchange_flag) AS interchange_stations
FROM station_accessibility_proxy
GROUP BY line
ORDER BY avg_proxy_score DESC;

-- 9. Screening candidates for deeper accessibility study.
-- These are ordinary operational stations under the current proxy definition.
SELECT station, line, accessibility_proxy_score, accessibility_band
FROM station_accessibility_proxy
WHERE accessibility_band LIKE 'Basic%'
ORDER BY accessibility_proxy_score, station;

-- 10. Methodology note:
-- The accessibility proxy is a network-structure screening signal only.
-- It must not be interpreted as measured travel time, socioeconomic access,
-- passenger equity, service quality or customer satisfaction.
