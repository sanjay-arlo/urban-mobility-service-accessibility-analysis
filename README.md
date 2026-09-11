# Urban Mobility Service & Accessibility Optimization

**Business Analyst case study analysing public-transport service trends, network connectivity, accessibility, and priority areas using Chennai Metropolitan Area data.**

---

## 📊 Project Overview

Public transport planning involves multiple modes, agencies, service indicators, and geographic access points. This project brings these datasets into an analytical framework to identify service trends, connectivity patterns, and areas that may deserve further investigation.

The project is designed around a practical business question:

> **Where are the public-transport service and accessibility gaps, and what data-backed interventions should transport planners prioritise?**

**Tech Stack:** Microsoft Excel | MySQL | SQL | Power BI | DAX

> **Data transparency:** Official transport sources are prioritised. Secondary or community datasets are clearly labelled. The analysis does not invent route-level delays, passenger counts, or causal effects that are not supported by the underlying data.

---

## 🎯 Business Objectives

- Understand public-transport demand and service trends over time
- Compare available transport modes and network coverage
- Identify highly connected transport locations
- Assess potential accessibility gaps using measurable network indicators
- Prioritise areas for further operational or planning investigation
- Convert analytical findings into practical business recommendations

---

## 👥 Business Stakeholders

- Transport planning teams
- Mobility and infrastructure planners
- Operations managers
- Public-service decision makers
- Business intelligence and strategy teams

---

## 🔍 Key Business Questions

### Service Performance
- How has public-transport demand changed over time?
- What are the major trends in bus and metro usage?
- Which service indicators are improving or declining?

### Network Accessibility
- Which locations have the strongest route connectivity?
- Which locations provide access to multiple transport modes?
- Where are potential accessibility gaps?

### Decision Support
- Which areas should receive further investigation?
- Where could multimodal connectivity create the greatest opportunity?
- Which findings should influence future transport planning?

---

## 🧩 Analytical Framework

**Business Problem → Data Audit → Data Cleaning → KPI Definition → SQL Analysis → Power BI → Insight → Recommendation**

The project deliberately separates **observed evidence** from **analytical inference** and avoids unsupported causal claims.

---

## 📁 Data Model

### Fact Tables

**Fact_MTC_Performance**
- Financial year
- Performance metric
- Metric value

**Fact_Metro_Ridership**
- Month
- Ridership
- Peak-demand indicators where available

### Dimension / Network Tables

**Dim_Stop**
- Stop ID
- Stop name
- Latitude
- Longitude
- Agency / mode

**Dim_Route**
- Route ID
- Route name
- Agency
- Mode

**Bridge_Stop_Route**
- Stop ID
- Route ID

This structure avoids forcing unrelated datasets into a single table simply because they can technically be joined.

---

## 📗 Excel Analysis

Excel is used for the initial data-audit and business-analysis layer:

- Missing-value checks
- Duplicate detection
- Data-type validation
- Date standardisation
- Pivot-table analysis
- Year-over-year trend calculations
- KPI preparation
- Source-data reconciliation

Excel acts as the validation layer before the data is moved into SQL and Power BI.

---

## 🗄️ SQL Analysis

The SQL layer answers business questions using:

- JOINs
- CTEs
- Window functions
- GROUP BY / HAVING
- CASE statements
- Ranking
- Year-over-year analysis
- Month-over-month analysis
- Multimodal connectivity analysis
- Route and stop-level aggregation

Example business query:

```sql
SELECT
    stop_name,
    COUNT(DISTINCT route_id) AS route_count
FROM bridge_stop_route
GROUP BY stop_name
ORDER BY route_count DESC;
```

**Business question:** Which transport locations have the highest route connectivity?

---

## 📊 Power BI Dashboard

### 1. Executive Transport Overview

- Ridership KPIs
- Service trend
- Mode comparison
- Year-over-year change
- Network summary

### 2. Network Accessibility

- Interactive transport map
- Route connectivity
- Stop density
- Multimodal locations
- Agency and mode filters

### 3. Demand vs Accessibility

A prioritisation matrix separates areas into four groups:

| Segment | Interpretation |
|---|---|
| High demand + low accessibility | 🔴 Priority for investigation |
| High demand + high accessibility | 🟢 Strong network coverage |
| Low demand + low accessibility | 🟡 Requires further investigation |
| Low demand + high accessibility | 🔵 Potentially sufficient coverage |

### 4. Recommendations

Each recommendation follows:

**Finding → Evidence → Business implication → Recommended action**

---

## 📈 KPI Framework

The dashboard will focus on measurable indicators such as:

- Total / monthly ridership
- Ridership growth rate
- Route connectivity
- Stop connectivity
- Multimodal access
- Stop density
- Accessibility opportunity score
- Priority-area count

Where a metric is derived rather than officially published, its calculation methodology is documented in the project.

---

## ⚠️ Analytical Limitations

This project intentionally documents its limitations:

1. Public datasets do not consistently provide vehicle-level GPS and actual arrival timestamps, so route-level delay claims are not made without supporting data.
2. Network accessibility is an analytical proxy and does not directly measure passenger satisfaction or actual travel behaviour.
3. Ridership and accessibility are analysed as separate dimensions; high network coverage does not automatically mean high demand.
4. Planned future infrastructure is not treated as operational service.
5. Observed correlations are not presented as causal relationships without supporting evidence.
6. Different datasets may have different time periods, definitions, and geographic granularity; these are documented before analysis.

---

## 💡 Example Business Recommendations

Recommendations will be generated from the actual findings rather than predetermined numbers. Examples of evidence-based actions include:

- Prioritise high-demand areas with relatively weaker multimodal connectivity for further planning studies.
- Investigate locations with low network coverage before considering additional service.
- Use demand trends to support peak-period capacity planning.
- Identify strong multimodal hubs that could support first/last-mile integration.
- Establish a repeatable KPI framework for future transport-performance monitoring.

---

## 🛠️ Tools & Skills Demonstrated

**Business Analysis**
- Business problem definition
- Requirements thinking
- KPI definition
- Stakeholder-oriented analysis
- Gap analysis
- Root-cause thinking
- Decision prioritisation
- Business recommendations

**Excel**
- Data cleaning
- Pivot tables
- KPI calculations
- Data validation

**SQL / MySQL**
- Complex joins
- CTEs
- Window functions
- Aggregation
- Ranking
- Business-question-driven queries

**Power BI**
- Data modelling
- DAX measures
- Interactive dashboards
- Geographic analysis
- Drill-down and filtering
- Data storytelling

---

## 📂 Project Structure

```text
urban-mobility-service-accessibility-analysis/
├── data/
│   ├── raw/
│   └── cleaned/
├── excel/
│   └── transport_data_analysis.xlsx
├── sql/
│   ├── schema.sql
│   ├── data_load.sql
│   └── business_analysis_queries.sql
├── powerbi/
│   └── Urban_Mobility_Dashboard.pbix
├── screenshots/
│   └── dashboard_overview.png
└── README.md
```

---

## 🚀 Project Outcome

The final solution is intended to provide a repeatable decision-support framework that connects public-transport data with business questions, measurable KPIs, accessibility analysis, and prioritised recommendations.

---

## 📫 Project Author

**Sanjay Arlo**  
Business Analyst | Data Analyst  
Chennai, India
