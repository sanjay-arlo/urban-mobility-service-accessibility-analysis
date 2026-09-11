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

### Dim_Station
- Line
- Station
- Network Role
- Interchange Flag
- Accessibility Proxy Score
- Accessibility Band

Keep ridership and station/network data at their own grains. Do not create a many-to-many relationship simply to make a visual work.

## Core measures

```DAX
Total Ridership = SUM(Fact_Ridership[Total Ridership])

QR Share % =
DIVIDE(SUM(Fact_Ridership[QR Tickets]), [Total Ridership])

NCMC Share % =
DIVIDE(SUM(Fact_Ridership[NCMC]), [Total Ridership])

Closed Loop Share % =
DIVIDE(SUM(Fact_Ridership[Closed Loop]), [Total Ridership])

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
    DISTINCTCOUNT(Dim_Station[Station]),
    Dim_Station[Interchange Flag] = 1
)

Avg Accessibility Proxy =
AVERAGE(Dim_Station[Accessibility Proxy Score])
```

## Recommended pages

### 1 — Executive Overview
KPI cards, monthly ridership trend, peak month and ticketing mix.

### 2 — Demand & Ticketing
MoM growth, NCMC/QR/closed-loop shares and financial-year comparison.

### 3 — Network Accessibility Screening
Station connectivity, interchange locations, proxy-score distribution and network filters.

### 4 — Decision Support
Finding → evidence → implication → recommended next investigation, with limitations.

## Integrity rule
Never present the accessibility proxy as observed accessibility, passenger satisfaction, travel time, transport equity, or service quality. It is a screening indicator derived from network structure.
