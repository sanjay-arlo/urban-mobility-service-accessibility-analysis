# Power BI Model & DAX Guide

## Model

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

Keep ridership and station/network data at their own grains. Do not create artificial many-to-many joins just to make visuals work.

## DAX Measures

```DAX
Total Ridership = SUM(Fact_Ridership[Total Ridership])

QR Share % =
DIVIDE(
    SUM(Fact_Ridership[QR Tickets]),
    [Total Ridership]
)

NCMC Share % =
DIVIDE(
    SUM(Fact_Ridership[NCMC]),
    [Total Ridership]
)

Closed Loop Share % =
DIVIDE(
    SUM(Fact_Ridership[Closed Loop]),
    [Total Ridership]
)

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

## Dashboard Pages

### Page 1 — Executive Overview
KPI cards, monthly ridership trend, peak month and ticketing mix.

### Page 2 — Demand & Ticketing
MoM growth, NCMC/QR/closed-loop shares and financial-year comparison.

### Page 3 — Network Accessibility
Station connectivity, interchange locations, proxy-score distribution and filters.

### Page 4 — Decision Support
Finding → evidence → implication → recommended action, plus limitations.

## Integrity Rule
Never present the accessibility proxy as observed accessibility, passenger satisfaction, travel time, transport equity or service quality.
