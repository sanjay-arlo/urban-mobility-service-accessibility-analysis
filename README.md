# Urban Mobility Service & Accessibility Optimization

**Business Analyst case study using public transport information to analyse passenger demand, ticketing behaviour, network connectivity and planning priorities.**

## Business Problem
Transport-planning teams need a repeatable way to understand changing passenger demand and network-connectivity signals so they can prioritise deeper operational and accessibility studies.

**Business Question → KPI → Analysis → Insight → Recommendation**

## Business Questions
- How has metro passenger demand changed month by month?
- Which periods show the strongest observed demand?
- How is usage shifting across NCMC, QR and closed-loop ticketing?
- Which stations act as interchange points?
- Which stations have stronger network-connectivity signals?
- Where should planners prioritise further investigation?

## Tools
**Excel** — data validation, formulas, pivots and KPI checks  
**SQL / MySQL** — CTEs, window functions, aggregation and ranking  
**Power BI** — data modelling, DAX and decision-oriented dashboards

## Data Sources
The passenger-flow dataset is structured from Chennai Metro Rail Limited (CMRL) public reporting. CMRL's Commuters Corner publishes Monthly Ridership, Passenger Flow and Peak Hour Per Direction Traffic information. The published Passenger Flow series used here covers Apr-2023 to May-2026.

Station/network references are based on CMRL public station and network information. CUMTA's Transit Data Chennai portal is documented as the public GTFS repository for Chennai Metro, MTC and Suburban Rail.

## Data Integrity
This project does **not** invent vehicle-level delays, route-level passenger loads or causal effects that are not supported by the source data.

The **Accessibility Proxy Score** is only a network-structure screening measure. It is not a measured travel-time, socioeconomic-accessibility, passenger-equity or service-quality score.

Ridership demand and network accessibility are analysed as separate dimensions rather than forcing unrelated grains into one table.

## Dashboard
### 1. Executive Overview
- Total observed ridership
- Peak observed month
- Ridership trend
- Ticketing mix

### 2. Demand & Ticketing
- Monthly ridership
- MoM growth
- NCMC share
- QR share
- Closed-loop share

### 3. Network Accessibility
- Station connectivity
- Interchange locations
- Network-role analysis
- Accessibility proxy ranking

### 4. Decision Support
**Finding → Evidence → Business implication → Recommended action**

## SQL Analysis
Business queries cover monthly trends, MoM growth with `LAG()`, ticketing mix, highest-demand periods, interchange analysis, network-role mix and connectivity ranking.

## Excel Analysis
Excel is the validation layer for source-data checks, KPI calculations, pivots, trend validation and reconciliation.

## Power BI
Recommended pages are Executive Overview, Demand & Ticketing, Network Accessibility and Decision Support. Keep ridership and station/network data at their own grains instead of using artificial many-to-many joins.

## Decision Framework
| Evidence pattern | Interpretation |
|---|---|
| High demand + weaker connectivity | Priority for deeper study |
| High demand + strong connectivity | Strong network node |
| Low demand + weaker connectivity | Investigate before expansion |
| Low demand + strong connectivity | Review sufficiency of current coverage |

These are screening categories, not automatic investment decisions.

## Repository Structure
```text
urban-mobility-service-accessibility-analysis/
├── data/
│   ├── cmrl_passenger_flow.csv
│   └── station_accessibility_proxy.csv
├── excel/
│   └── Urban_Mobility_Analysis.xlsx
├── sql/
│   └── urban_mobility_analysis.sql
├── powerbi/
│   └── PowerBI_Model_and_DAX_Guide.md
├── index.html
└── README.md
```

## Live Dashboard
[Open the Interactive Dashboard](https://sanjay-arlo.github.io/urban-mobility-service-accessibility-analysis/)

## Example Observed Metrics
CMRL reported **10,184,419 passengers in March 2026** and **10,468,732 in July 2025** in the published passenger-flow series. March 2026 included **5,290,363 NCMC**, **4,860,707 QR** and **33,349 closed-loop** passengers.

## Future Enhancement
Add verified stop-level GTFS, travel-time observations, first/last-mile information and demographic context to build a stronger accessibility-equity model.

## Author
**Sanjay Arlo** — Business Analyst | Data Analyst
