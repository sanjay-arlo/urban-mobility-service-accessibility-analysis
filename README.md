# Urban Mobility Service & Accessibility Optimization

> Business Analyst case study combining Chennai Metro passenger demand with GTFS-based network, scheduled travel-time and first/last-mile evidence.

## 🔴 Live Dashboard

### 🚀 [Open the Interactive Dashboard](https://sanjay-arlo.github.io/urban-mobility-service-accessibility-analysis/)

The dashboard loads repository CSV outputs directly. Ridership and ticketing are based on CMRL passenger-flow reporting; network and first/last-mile metrics are generated from the GTFS refresh pipeline.

---

## 🎯 Business Problem

Transport-planning teams need a repeatable way to understand demand patterns and network access signals before prioritising deeper operational studies.

**Business Question → Data → Validation → KPI → Segmentation → Insight → Recommendation**

## Business Questions

1. How has Chennai Metro passenger demand changed month by month?
2. Which periods show the strongest observed ridership?
3. How has the mix of NCMC, QR and closed-loop ticketing changed?
4. Which stations have strong network connectivity and interchanges?
5. Which stations are farther from the nearest bus stop?
6. What is the scheduled travel time between adjacent metro stations?
7. Which stations or network patterns deserve deeper first/last-mile investigation?

---

## 📊 Dashboard

### Executive Overview
- Total observed ridership for the selected period
- Peak observed month
- Weighted NCMC share
- GTFS-derived metro-station count
- Median straight-line distance to the nearest GTFS bus stop

### Demand & Ticketing
- Monthly ridership
- Month-over-month growth
- NCMC / QR / closed-loop share trends
- Financial-year comparison

### GTFS Network & First/Last Mile
- First-mile proximity bands
- Nearest bus-stop distance by station
- Bus-stop density within 500m
- Scheduled metro segment travel time
- Network + first-mile screening index by line
- Filters for financial year, network role, line and first-mile band

### Decision Support
- Evidence-led demand signal
- First/last-mile investigation signal
- Scheduled travel-time signal
- Explicit methodology and limitations

---

## 🧮 KPI Definitions

### Ridership
`Total Ridership = SUM(monthly total_ridership)`

### Weighted ticketing share
`NCMC Share = SUM(NCMC) / SUM(Total Ridership)`

This avoids averaging monthly percentages without weighting by passenger volume.

### MoM growth
`MoM Growth % = (Current Month Ridership − Previous Month Ridership) / Previous Month Ridership × 100`

### Scheduled travel time
For each adjacent metro-station pair, scheduled travel time is calculated from GTFS `stop_times.txt`. The dashboard reports the median observed timetable duration across matching trips.

### First/last-mile proximity
For each metro station:

- `Nearest bus stop distance` = straight-line Haversine distance to the closest GTFS bus stop.
- `Bus stops within 500m` = count of GTFS bus stops inside a 500m straight-line radius.

### Network + first-mile screening index
A transparent 0–100 analytical index combines three min-max-normalised components with equal weight:

1. Metro route coverage
2. Inverse nearest-bus-stop distance
3. Bus-stop density within 500m

It is a **screening index only**. It is not a measure of transport equity, socioeconomic accessibility, observed travel time, pedestrian accessibility or service quality.

---

## ⚠️ Data Integrity

Passenger-flow figures are based on CMRL public passenger-flow reporting stored in `data/cmrl_passenger_flow.csv`.

The GTFS pipeline uses a machine-readable Chennai unified feed from the community-maintained ChennaiGTFS project. The project does **not** represent that feed as an official CUMTA/CMRL publication.

Static GTFS provides scheduled transit information. It does not prove real-time delays or actual road congestion. First-mile distances are straight-line proximity measures, not pedestrian-network walking distances.

The analysis keeps monthly ridership and station/network data at separate grains to avoid misleading joins.

---

## 📚 Data Sources

- **CMRL public commuter information** for passenger-flow/ridership reporting.
- **CUMTA Transit Data Chennai** as the official Chennai open-data context for static GTFS.
- **ChennaiGTFS community feed** as the automated machine-readable source used by this portfolio pipeline.

Detailed source and methodology notes are in `data/GTFS_Sources_and_Methodology.md`.

---

## 🔄 GTFS Refresh Pipeline

`python scripts/build_gtfs_accessibility.py` downloads the configured unified GTFS feed and generates:

```text
data/
├── gtfs_station_metrics.csv
├── gtfs_metro_segment_travel_times.csv
└── gtfs_refresh_metadata.json
```

GitHub Actions runs the refresh weekly and supports manual execution through workflow dispatch.

The pipeline validates the presence of core GTFS tables, derives scheduled metro travel time from `stop_times.txt`, calculates bus-stop proximity with the Haversine formula, and records the source/refresh metadata.

---

## 🗂️ Data Model

```text
Fact_Ridership
    month
    date
    financial_year
    closed_loop
    qr_tickets
    ncmc
    total_ridership

Dim_GTFS_Station
    stop_id
    station_name
    latitude
    longitude
    metro_route_count
    metro_trip_count
    interchange_flag
    nearest_bus_stop_m
    bus_stops_within_500m
    route_coverage_score
    first_mile_proximity_score
    bus_stop_density_score
    network_first_mile_screening_index
    first_mile_band

Fact_Metro_Segment_Travel_Time
    from_stop_id
    to_stop_id
    from_station
    to_station
    median_scheduled_travel_time_min
    trip_observations
```

The datasets remain at their own grains. Monthly ridership should not be joined directly to station-level or segment-level records for passenger totals.

---

## 🗄️ SQL Analysis

`sql/urban_mobility_analysis.sql` contains reusable MySQL analysis for monthly ridership, MoM growth, ticketing mix, demand ranking, interchange analysis, network-role mix and line-level screening.

---

## 📊 Excel & Power BI

The repository includes an **Excel analysis guide** and a **Power BI model/DAX specification**. These are methodological references, not claims that `.xlsx` or `.pbix` binaries are present.

---

## 📂 Repository Structure

```text
urban-mobility-service-accessibility-analysis/
├── data/
│   ├── cmrl_passenger_flow.csv
│   ├── station_accessibility_proxy.csv
│   └── GTFS_Sources_and_Methodology.md
├── scripts/
│   └── build_gtfs_accessibility.py
├── .github/workflows/
│   └── refresh_gtfs.yml
├── excel/
│   └── Excel_Analysis_Guide.md
├── powerbi/
│   └── PowerBI_Model_and_DAX_Guide.md
├── sql/
│   └── urban_mobility_analysis.sql
├── index.html
└── README.md
```

---

## 🔮 Further Upgrade

The next level is to replace straight-line bus-stop proximity with **pedestrian-network routing** using OpenStreetMap and to add **GTFS-Realtime or observed vehicle telemetry** for actual travel-time reliability. That would move the project from network screening toward a defensible accessibility and service-quality analysis.

---

## 👤 Author

**Sanjay Arlo** — Business Analyst | Data Analyst
