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

### Sheet 2 — Calculations
Create:

`MoM Growth % = (Current Ridership / Previous Ridership) - 1`

`NCMC Share % = NCMC / Total Ridership`

`QR Share % = QR Tickets / Total Ridership`

`Closed Loop Share % = Closed Loop / Total Ridership`

Use a weighted annual ticketing share for period summaries rather than averaging monthly percentages.

### Sheet 3 — Station_Network
Load `../data/station_accessibility_proxy.csv` as `Dim_Station`.

Recommended pivots:
- Station count by network role
- Interchange stations by line
- Average proxy score by line
- Accessibility band distribution

### Sheet 4 — Executive_Checks
Reconcile the Excel calculations against the dashboard:

- Total selected-period ridership
- Peak month
- Weighted NCMC share
- Distinct interchange count

## Business-analysis outputs

The goal is not simply to reproduce charts. Use the workbook to answer:

1. Where are the strongest observed demand periods?
2. How is ticketing behaviour changing over time?
3. Which network roles are most common?
4. Which stations/lines should be prioritised for deeper study?
5. What additional data is needed before making an accessibility or investment decision?

## Integrity rule
The station score is a screening proxy based on network structure. Do not label it as measured accessibility, travel time, socioeconomic access, passenger equity, or service quality.
