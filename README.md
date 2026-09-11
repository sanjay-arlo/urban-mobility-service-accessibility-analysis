# Urban Mobility Service & Accessibility Optimization

> Business Analyst case study using Chennai Metro public reporting to analyse passenger demand, ticketing behaviour, network connectivity and planning priorities.

## 🔴 Live Dashboard

### 🚀 [Open the Interactive Dashboard](https://sanjay-arlo.github.io/urban-mobility-service-accessibility-analysis/)

The dashboard loads the repository CSV files directly and calculates the displayed KPIs, trends and network summaries from the source data.

---

## 🎯 Business Problem

Transport-planning teams need a repeatable way to understand demand patterns, ticketing behaviour and network-structure signals before prioritising deeper operational or accessibility studies.

**Business Question → Data → Validation → KPI → Segmentation → Insight → Recommendation**

## Business Questions

1. How has Chennai Metro passenger demand changed month by month?
2. Which periods show the strongest observed ridership?
3. How has the mix of NCMC, QR and closed-loop ticketing changed?
4. How are stations distributed across network roles and lines?
5. Which stations have stronger network-connectivity signals?
6. Which patterns should trigger deeper planning investigation?

---

## 📊 Dashboard

### Executive Overview
- Total observed ridership for the selected period
- Peak observed month
- Weighted NCMC share
- Distinct interchange stations

### Demand & Ticketing
- Monthly ridership
- Month-over-month growth
- NCMC / QR / closed-loop share trends
- Financial-year comparison

### Network Accessibility Screening
- Accessibility screening bands
- Network-role mix
- Average proxy score by line
- Filters for financial year, network role, line and screening band

### Decision Support
- Evidence-led demand signal
- Ticketing signal
- Planning implication
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

### Accessibility proxy
The station score is a **screening-level network-structure measure**, not observed accessibility. The current source model assigns higher connectivity to interchange stations and lower connectivity to ordinary operational stations. It must not be interpreted as measured travel time, socioeconomic access, passenger equity, service quality or customer satisfaction.

---

## ⚠️ Data Integrity

Passenger-flow figures are based on the published Chennai Metro Rail Limited (CMRL) passenger-flow series stored in `data/cmrl_passenger_flow.csv`. The repository currently includes monthly observations from April 2023 through May 2026.

Station and network-role information is stored separately in `data/station_accessibility_proxy.csv` so ridership data and station data remain at their own grains.

The project deliberately avoids inventing vehicle-level delays, station-level passenger counts or causal effects that are not supported by the underlying sources.

---

## 📚 Data Sources

The analysis is structured from publicly reported Chennai Metro information. CMRL publishes passenger-flow, monthly ridership and peak-hour information through its public commuter information resources. Station/network references use public CMRL network information.

For future expansion, verified GTFS data from the public Transit Data Chennai ecosystem can be incorporated for stop-level and route-level accessibility analysis.

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

Dim_Station
    line
    station
    network_role
    interchange_flag
    accessibility_proxy_score
    accessibility_band
```

The two datasets are intentionally analysed at separate grains. A many-to-many join between monthly ridership and station records would create misleading numbers.

---

## 🧪 Analysis Workflow

1. **Load** — Read the CMRL passenger-flow and station datasets.
2. **Validate** — Check rows, missing values, duplicates and basic consistency.
3. **Feature engineer** — Calculate salary-like derived measures relevant to mobility analysis such as growth and weighted ticketing shares.
4. **Analyse** — Produce demand, ticketing, network-role and screening metrics.
5. **Compare** — Examine financial-year patterns and network-role distributions.
6. **Visualise** — Present calculated results through the browser dashboard.
7. **Interpret** — Convert observed patterns into investigation priorities while keeping claims within the limits of the data.

---

## 🗄️ SQL Analysis

`sql/urban_mobility_analysis.sql` contains reusable MySQL analysis for:

- monthly ridership
- MoM growth using `LAG()`
- ticketing mix
- highest-demand months
- interchange stations
- network-role mix
- line-level proxy comparison
- screening candidates for deeper study

---

## 📊 Excel & Power BI

The repository documentation includes a **Power BI model/DAX specification** and an **Excel analysis guide**. These are design/validation references rather than claims that a `.pbix` or `.xlsx` implementation is included.

A future release can add the actual Excel workbook and Power BI file where sharing those binaries is practical.

---

## 📂 Repository Structure

```text
urban-mobility-service-accessibility-analysis/
├── data/
│   ├── cmrl_passenger_flow.csv
│   └── station_accessibility_proxy.csv
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

## 🔮 Next Analytical Upgrade

The strongest next version would replace the simple screening proxy with verified stop-level GTFS and travel-time observations, then build an accessibility model that can distinguish connectivity, travel effort, interchange importance and first/last-mile access.

Until those fields exist, the proxy should remain a screening tool rather than a headline accessibility metric.

---

## 👤 Author

**Sanjay Arlo** — Business Analyst | Data Analyst
