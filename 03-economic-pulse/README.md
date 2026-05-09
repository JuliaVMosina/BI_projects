# 03 · Finland Economic Pulse

> **GDP, employment, inflation — one dashboard, always up to date.**

## Live Dashboard

**→ [View on Tableau Public](https://public.tableau.com/app/profile/julia.v.mosina/viz/FinlandEconomicPulseGDPCPIEmployment20152026/Dashboard1)**

---

## Business Problem

Macroeconomic data for Finland is publicly available but scattered across multiple StatFin tables.
This dashboard consolidates four key indicators into a single view — enabling quick reading of
where the Finnish economy stands and how it has moved since 2015.

---

## Data Sources

- **StatFin API** (Statistics Finland / stat.fi) — official open data
- **Synthetic dataset** — realistic data modeled on official Finnish national accounts,
  Labour Force Survey, and CPI publications (2015–2026), used as API fallback.

---

## Stack

| Layer | Tool |
|---|---|
| Data collection | Python (requests, pandas, numpy) |
| Data modeling | Python — star schema CSV builder |
| Visualization | Tableau Public |

---

## Data Model

```
dim_indicator       dim_time
      \               /
       fact_indicators
```

**fact_indicators** — one row per indicator × date (363 rows)

| Table | Rows | Key fields |
|---|---|---|
| fact_indicators | 363 | time_id, indicator_id, date, value, frequency, unit |
| dim_indicator | 4 | indicator_id, indicator, category, frequency, unit, description |
| dim_time | 136 | time_id, date, year, quarter, month, month_name |

---

## Indicators Covered

| Indicator | Frequency | Source |
|---|---|---|
| GDP Growth YoY % | Quarterly | National Accounts (StatFin ntp) |
| CPI Inflation YoY % | Monthly | Consumer Price Index (StatFin khi) |
| Employment Rate % | Quarterly | Labour Force Survey (StatFin tyti) |
| Unemployment Rate % | Monthly | Labour Force Survey (StatFin tyti) |

---

## Dashboard Features

- KPI row: latest value for each indicator (filtered to MAX date)
- GDP Trend — area chart with recession reference band (below 0%)
- CPI Trend — inflation spike of 2022 clearly visible
- Employment Rate trend — long-term upward trajectory 2015–2026
- Unemployment Rate trend — COVID impact and recovery visible

---

## Key Findings

- **GDP**: COVID shock -5.8% in 2020 Q2, recession in 2023 (-1.2%), recovery to +1.2% in 2026
- **CPI**: Inflation peaked at ~8% in 2022, normalized to ~2% by 2026
- **Employment**: Steady rise from 68% (2015) to ~74% (2026), interrupted by COVID
- **Unemployment**: Improved from 9.4% (2015) to 7.8% (2026), with COVID spike in 2020

---

## Files

```
03-economic-pulse/
├── README.md
├── python/
│   ├── data_collection.py    ← synthetic data generation (StatFin-modeled)
│   └── data_prep.py          ← star schema CSV builder
└── data/
    ├── raw_gdp.csv
    ├── raw_cpi.csv
    ├── raw_employment.csv
    ├── raw_unemployment.csv
    ├── fact_indicators.csv   ← 363 rows
    ├── dim_indicator.csv     ← 4 indicators
    └── dim_time.csv          ← 136 dates
```

---

## Project Status

Complete — published on Tableau Public
