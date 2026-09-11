# Chennai Metro Passenger Demand & Access Analysis

> A Business Analyst case study that turns passenger demand and public-transport data into simple, decision-ready insights.

## 🚀 Live Dashboard

**[Open the interactive dashboard](https://sanjay-arlo.github.io/urban-mobility-service-accessibility-analysis/)**

---

## 1. What is this project about?

Imagine a transport-planning manager asks:

> **“Passenger demand is changing, but which metro stations may need better bus connectivity or deeper investigation?”**

This project answers that question with a simple business workflow:

**Business Question → Data → Analysis → Finding → Recommendation**

The project looks at four things:

1. **Passenger demand** — how metro usage changes over time.
2. **How passengers pay** — NCMC, QR and closed-loop ticketing mix.
3. **Station access** — how close metro stations are to nearby bus stops.
4. **Travel time** — timetable-based travel time between metro stations.

The goal is not to build a transport-engineering model. The goal is to show how a **Business Analyst converts data into a practical decision-support story**.

---

## 2. Business questions answered

### Demand
- When is passenger demand highest?
- Which months or financial years are strongest?
- Is passenger demand increasing or decreasing?

### Customer / ticketing behaviour
- How is the ticket-payment mix changing?
- Is NCMC becoming more important over time?

### Passenger access
- Which metro stations have nearby bus connectivity?
- Which stations are farther from a mapped bus stop?
- Which stations deserve a closer look for first/last-mile improvement?

### Travel time
- Which station-to-station journeys have the longest scheduled time?
- Where could operations teams investigate timetable or service patterns further?

---

## 3. What a non-technical person will see on the dashboard

The dashboard deliberately avoids heavy transport jargon.

| Dashboard term | Plain-English meaning |
|---|---|
| **Station Type** | Standard station or station where passengers can transfer between metro services |
| **Metro Corridor** | The metro route/group being compared |
| **Bus Access** | How close a station is to a nearby bus stop |
| **Easy Bus Access** | Nearest mapped bus stop is under 250 metres away |
| **Moderate Bus Access** | 250–500 metres away |
| **Limited Bus Access** | More than 500 metres away |
| **Priority Score** | A screening score used to decide which stations should be investigated first |
| **Scheduled Travel Time** | Timetable-based time between adjacent metro stations |
| **GTFS** | The technical data format used for public-transport stops and timetables |

The technical terms are still retained in the methodology and data files so that recruiters can see the underlying technical capability.

---

## 4. Dashboard sections

### 1 — Passenger Demand
Shows:
- Monthly passenger demand
- Monthly demand change
- Financial-year comparison
- Ticket-payment mix

### 2 — Passenger Access to Metro Stations
Shows:
- Bus access levels
- Stations farthest from a bus stop
- Access priority by metro corridor
- Standard vs transfer stations

### 3 — Scheduled Travel Time
Shows:
- Longest scheduled station-to-station times
- Typical and higher-end scheduled travel time

### 4 — Stations to Investigate
A simple table ranks stations using the screening score so a manager can quickly identify candidates for deeper analysis.

### 5 — Business Recommendations
The dashboard translates the analysis into business actions instead of stopping at charts.

### 6 — Plain-English Glossary
Explains every specialist term used in the project.

---

## 5. Key business insight framework

The project follows this structure:

**Finding**

A measurable pattern is found in the data.

**Business meaning**

The pattern is translated into something a manager can understand.

**Action**

The result becomes a recommendation or a question for the next analysis stage.

### Example

**Finding:** A station is more than 500m from the nearest mapped bus stop.

**Business meaning:** Bus connectivity may be weaker at that location compared with stations with closer bus access.

**Action:** Prioritise the station for a deeper first/last-mile study using pedestrian routes, feeder services and actual passenger behaviour.

This is why the project is a **Business Analyst case study**, not just a dashboard project.

---

## 6. Data sources

### Passenger demand
`data/cmrl_passenger_flow.csv`

Contains the monthly passenger-flow series used for the demand and ticketing analysis.

### Public transport network
The automated pipeline uses community-maintained Chennai GTFS feeds for:
- metro stops and routes;
- bus stops;
- timetable information.

The repository does **not** present the community feed as an official CMRL/CUMTA publication.

---

## 7. Data methodology

### Passenger demand
Passenger demand is analysed at **monthly level**.

### Ticketing share
The dashboard uses a weighted calculation:

`NCMC Share = Total NCMC Passengers ÷ Total Passengers`

This is preferable to averaging monthly percentages because larger passenger months should carry more weight.

### Bus access
For each metro station:

- Distance to the nearest bus stop is calculated using the Haversine formula.
- The number of bus stops within a 500m straight-line radius is counted.
- These are used as **proximity indicators**, not as measured walking time.

### Priority score
The station priority score combines:

- metro connectivity signal;
- closeness to the nearest bus stop;
- number of nearby bus stops.

It is a **screening tool**. A high or low score does not prove that a station has good or poor service quality.

### Scheduled travel time
Travel time between adjacent metro stations is derived from timetable `stop_times` data.

It is:

- **scheduled**;
- **not real-time**;
- **not observed road traffic time**;
- **not passenger door-to-door journey time**.

---

## 8. Data-grain rule

One important Business Analyst principle in this project is **not mixing different levels of data incorrectly**.

- Monthly passenger data = one row per month.
- Station access data = one row per station.
- Segment travel-time data = one row per station pair.

These datasets should not be joined directly just to make a chart. Doing that could duplicate passenger totals and produce misleading results.

---

## 9. Technical stack

- **Excel** — business calculations and analysis planning
- **SQL / MySQL** — querying and business analysis
- **Python / Pandas** — GTFS processing and data preparation
- **HTML / CSS / JavaScript** — interactive dashboard
- **Plotly.js** — charts
- **Papa Parse** — browser-side CSV loading
- **GitHub Actions** — automated GTFS refresh
- **GitHub Pages** — live dashboard hosting
- **Power BI** — recommended implementation specification and DAX design

The project intentionally combines technical work with business communication.

---

## 10. Repository structure

```text
urban-mobility-service-accessibility-analysis/
│
├── data/
│   ├── cmrl_passenger_flow.csv
│   ├── station_accessibility_proxy.csv
│   ├── gtfs_station_metrics.csv
│   ├── gtfs_metro_segment_travel_times.csv
│   ├── gtfs_refresh_metadata.json
│   └── GTFS_Sources_and_Methodology.md
│
├── scripts/
│   └── build_gtfs_accessibility.py
│
├── sql/
│   └── urban_mobility_analysis.sql
│
├── excel/
│   └── Excel_Analysis_Guide.md
│
├── powerbi/
│   └── PowerBI_Model_and_DAX_Guide.md
│
├── .github/
│   └── workflows/
│       └── refresh_gtfs.yml
│
├── index.html
└── README.md
```

---

## 11. Automated GTFS refresh

GitHub Actions periodically refreshes the GTFS-derived files.

The process:

**Download feed → Validate tables → Prepare metro and bus data → Calculate station access indicators → Calculate scheduled segment times → Save CSV outputs**

Generated files:

```text
data/gtfs_station_metrics.csv
data/gtfs_metro_segment_travel_times.csv
data/gtfs_refresh_metadata.json
```

This makes the project more realistic than using a one-time manually prepared dataset.

---

## 12. SQL analysis

`sql/urban_mobility_analysis.sql` contains reusable queries for:

- monthly demand;
- month-over-month growth;
- ticketing mix;
- highest-demand months;
- financial-year comparison;
- stations with weak bus-stop proximity;
- station priority screening;
- metro connectivity;
- scheduled travel-time hotspots.

---

## 13. Power BI and Excel

The repository includes implementation guides rather than pretending that binary `.pbix` or `.xlsx` files are stored here.

This keeps the project honest while still showing how the model can be implemented in common Business Analyst tools.

---

## 14. Limitations

This project is designed for **screening and portfolio demonstration**, not for final transport policy decisions.

Important limitations:

- passenger-flow data and station-access data have different grains;
- static GTFS represents scheduled service, not live delays;
- bus-stop distance is straight-line proximity, not pedestrian-network distance;
- the community GTFS source is not presented as official CMRL/CUMTA data;
- the priority score is an analytical aid, not a measure of equity, accessibility quality or passenger satisfaction;
- the current timetable-derived segment layer has limited schedule coverage and should be validated before operational use.

---

## 15. Future upgrades

The next strong analytical upgrades would be:

1. **Pedestrian-network travel time** instead of straight-line distance.
2. **Actual bus/metro travel-time reliability** instead of scheduled time only.
3. **Passenger or station-level demand linkage** where reliable data is available.
4. **Feeder-service analysis** for stations identified as investigation candidates.
5. **Geospatial maps** to make station-level patterns easier to interpret.

---

## 16. Why this demonstrates Business Analyst skills

This project is designed to demonstrate that I can:

- translate a vague business problem into clear questions;
- define KPIs;
- work with messy or multi-source data;
- maintain correct data grain;
- analyse trends and customer behaviour;
- segment operational problems;
- identify priority areas;
- explain technical analysis in plain English;
- convert findings into recommendations;
- document assumptions and limitations;
- build an interactive decision-support dashboard.

The strongest part of the project is **not the chart design**. It is the chain from **business question to evidence to recommended action**.

---

## 👤 Author

**Sanjay Arlo**  
Business Analyst | Data Analyst

[Live Dashboard](https://sanjay-arlo.github.io/urban-mobility-service-accessibility-analysis/) · [GitHub Repository](https://github.com/sanjay-arlo/urban-mobility-service-accessibility-analysis)
