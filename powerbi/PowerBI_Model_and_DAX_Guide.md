# Power BI Model & DAX Guide — Business-Friendly Version

This document shows how the project can be rebuilt in Power BI. It is a **model and DAX specification**, not a claim that a `.pbix` file is stored in the repository.

## Business pages

### 1. Passenger Demand
Use KPI cards, monthly demand, monthly change and financial-year comparison.

### 2. How Passengers Pay
Show NCMC, QR and closed-loop ticket shares over time.

### 3. Passenger Access
Show which metro stations are easier or harder to reach from nearby bus stops.

### 4. Scheduled Travel Time
Show timetable-based travel time between adjacent stations.

### 5. Stations to Investigate
Rank stations that deserve a deeper access review.

## Friendly business field names

| Technical field | Dashboard / business label |
|---|---|
| `network_role` | Station Type |
| `Interchange` | Transfer Station |
| `Operational` | Standard Station |
| `line` | Metro Corridor |
| `nearest_bus_stop_m` | Distance to Nearest Bus Stop |
| `bus_stops_within_500m` | Bus Stops Nearby |
| `first_mile_band` | Bus Access |
| `network_first_mile_screening_index` | Station Access Priority Score |
| `median_scheduled_travel_time_min` | Scheduled Travel Time |

## Core measures

```DAX
Total Passengers = SUM(Fact_Ridership[Total Ridership])

NCMC Share % = DIVIDE(SUM(Fact_Ridership[NCMC]), [Total Passengers])

QR Share % = DIVIDE(SUM(Fact_Ridership[QR Tickets]), [Total Passengers])

Closed Loop Share % = DIVIDE(SUM(Fact_Ridership[Closed Loop]), [Total Passengers])

Monthly Demand Change % =
VAR CurrentValue = [Total Passengers]
VAR PreviousValue =
    CALCULATE(
        [Total Passengers],
        DATEADD('Calendar'[Date], -1, MONTH)
    )
RETURN DIVIDE(CurrentValue - PreviousValue, PreviousValue)

Station Count = DISTINCTCOUNT(Dim_GTFS_Station[Stop ID])

Median Bus-Stop Distance (m) = MEDIAN(Dim_GTFS_Station[Nearest Bus Stop Distance (m)])

Average Access Priority Score = AVERAGE(Dim_GTFS_Station[Station Access Priority Score])

Average Scheduled Travel Time (min) = AVERAGE(Fact_Metro_Segment_Travel_Time[Scheduled Travel Time (min)])
```

## Model rule

Keep monthly demand, station access and station-pair travel time at their own grains. Do not directly join them in a way that duplicates passenger totals.

## Business communication rule

Power BI visuals should answer a business question first. Technical terms such as **GTFS**, `stop_id`, Haversine distance and `stop_times` belong in tooltips, methodology pages or documentation rather than headline KPI labels.

## Interpretation rule

- Passenger totals = observed demand.
- Bus-stop distance = proximity indicator.
- Scheduled travel time = timetable information.
- Priority Score = screening tool for deciding where to investigate next.

None of these should be presented as proof of passenger satisfaction, equity, actual walking time or live traffic performance.
