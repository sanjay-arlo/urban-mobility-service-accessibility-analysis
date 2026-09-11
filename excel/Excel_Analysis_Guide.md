# Excel Analysis Guide

This folder contains the Excel analysis specification for the mobility case study. The repository does **not** claim that an `.xlsx` workbook is included.

## Workbook structure

### Sheet 1 — Source_Ridership
Load `../data/cmrl_passenger_flow.csv` as an Excel Table named `Fact_Ridership`.

Recommended checks:
- Row count
- Missing values
- Duplicate months
- `Closed Loop + QR Tickets + NCMC = Total Ridership`
- Date sorting

### Sheet 2 — Demand_Calculations
Create:

`MoM Growth % = (Current Ridership / Previous Ridership) - 1`

`NCMC Share % = NCMC / Total Ridership`

`QR Share % = QR Tickets / Total Ridership`

`Closed Loop Share % = Closed Loop / Total Ridership`

Use a weighted period ticketing share rather than averaging monthly percentages.

### Sheet 3 — GTFS_Station
Load `../data/gtfs_station_metrics.csv` after the GTFS refresh workflow runs.

Recommended pivots:
- Median nearest bus-stop distance by line
- Stations with >500m nearest bus stop
- Bus stops within 500m by station
- Interchange status and metro route coverage
- Network + first-mile screening index distribution

### Sheet 4 — GTFS_Travel_Time
Load `../data/gtfs_metro_segment_travel_times.csv`.

Recommended analysis:
- Median scheduled travel time by adjacent station pair
- Longest scheduled segments
- Segment observation counts
- Travel-time distribution by line where route labels are available

### Sheet 5 — Executive_Checks
Reconcile the Excel calculations against the dashboard:

- Total selected-period ridership
- Peak month
- Weighted NCMC share
- Metro station count
- Median nearest bus-stop distance
- Longest scheduled metro segment

## Business-analysis outputs

Use the workbook to answer:

1. Where are the strongest observed demand periods?
2. How is ticketing behaviour changing over time?
3. Which stations have weaker first/last-mile proximity?
4. Which adjacent metro segments have longer scheduled travel times?
5. Which network patterns should trigger deeper operational or pedestrian-access study?
6. What additional observed data is needed before making an accessibility or investment decision?

## Integrity rule
GTFS travel time is **scheduled timetable duration**, not observed traffic time. Bus-stop distance is a straight-line proximity measure, not a walking-network route. The screening index is an analytical prioritisation aid only.
