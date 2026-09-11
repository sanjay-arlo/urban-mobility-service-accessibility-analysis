# Power BI Model & DAX Guide

This file defines the recommended Power BI implementation. It is a **model/DAX specification**, not a claim that a `.pbix` file is stored in this repository.

## Data model

### Fact_Ridership
- Month
- Date
- Financial Year
- Closed Loop
- QR Tickets
- NCMC
- Total Ridership

### Dim_GTFS_Station
- Stop ID
- Station Name
- Latitude
- Longitude
- Metro Route Count
- Metro Trip Count
- Interchange Flag
- Nearest Bus Stop Distance (m)
- Bus Stops Within 500m
- Network + First-Mile Screening Index
- First-Mile Band

### Fact_Metro_Segment_Travel_Time
- From Stop ID
- To Stop ID
- From Station
- To Station
- Median Scheduled Travel Time (min)
- Trip Observations

Keep these datasets at their own grains. Do not create a many-to-many relationship simply to make a visual work.

## Core measures

```DAX
Total Ridership = SUM(Fact_Ridership[Total Ridership])

QR Share % = DIVIDE(SUM(Fact_Ridership[QR Tickets]), [Total Ridership])

NCMC Share % = DIVIDE(SUM(Fact_Ridership[NCMC]), [Total Ridership])

Closed Loop Share % = DIVIDE(SUM(Fact_Ridership[Closed Loop]), [Total Ridership])

MoM Growth % =
VAR CurrentValue = [Total Ridership]
VAR PreviousValue =
    CALCULATE(
        [Total Ridership],
        DATEADD('Calendar'[Date], -1, MONTH)
    )
RETURN
DIVIDE(CurrentValue - PreviousValue, PreviousValue)

Interchange Stations =
CALCULATE(
    DISTINCTCOUNT(Dim_GTFS_Station[Stop ID]),
    Dim_GTFS_Station[Interchange Flag] = 1
)

Median First-Mile Distance (m) =
MEDIAN(Dim_GTFS_Station[Nearest Bus Stop Distance (m)])

Avg Screening Index =
AVERAGE(Dim_GTFS_Station[Network + First-Mile Screening Index])

Avg Scheduled Segment Time (min) =
AVERAGE(Fact_Metro_Segment_Travel_Time[Median Scheduled Travel Time (min)])
```

## Recommended pages

### 1 — Executive Overview
KPI cards, monthly ridership trend, peak month and weighted ticketing mix.

### 2 — Demand & Ticketing
MoM growth, NCMC/QR/closed-loop shares and financial-year comparison.

### 3 — GTFS Network & First/Last Mile
Station map/table, nearest-bus-stop distance, 500m bus-stop density, interchange status and first-mile bands.

### 4 — Scheduled Travel Time
Adjacent-station travel-time distribution, longest scheduled segments, evidence volume and line/segment filters.

### 5 — Decision Support
Finding → evidence → implication → recommended next investigation, with explicit limitations.

## Integrity rule
Static GTFS provides scheduled information, not observed congestion or real-time delay. Straight-line bus-stop distance is a first-mile proximity proxy, not a pedestrian-network route time. The screening index is an analytical prioritisation aid, not a transport-equity, accessibility-quality or passenger-experience score.
