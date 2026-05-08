# 01 · HR Hiring Analytics Dashboard

> **Where do candidates drop off in the IT hiring funnel in Finland?**

## Live Dashboard

**→ [View on Tableau Public](https://public.tableau.com/app/profile/julia.v.mosina/viz/HRHiringAnalyticsFinlandITMarket2024-2026/Dashboard3)**

*Power BI version (.pbix) available for download below — built in parallel to demonstrate multi-tool proficiency.*

---

## Business Problem

Hiring managers in Finnish IT companies often lack visibility into where candidates drop off
and how their time-to-hire compares to the market. This dashboard answers both questions
using public labor market data and a modeled hiring funnel.

---

## Data Sources

- **stat.fi StatFin API** — employment by industry and region (open, free, official)
- **Synthetic hiring funnel** — modeled stages: Applications → Screening → Interview → Offer → Hire

---

## Stack

| Layer | Tool |
|---|---|
| Data collection & prep | Python (pandas, requests) |
| Data modeling | SQL — star schema |
| Visualization (primary) | Tableau Public |
| Visualization (secondary) | Power BI Desktop + DAX |

---

## Data Model

```
dim_role       dim_region      dim_time
    \               |               /
     └──────── fact_hiring ────────┘
```

---

## Key Metrics

- **Time-to-hire** by role and seniority — with market benchmarks
- **Hiring funnel conversion** — Applications → Screening → Interview → Offer → Hire
- **Applications trend** vs. hire rate % — dual-axis monthly view
- **Regional breakdown** — where IT hiring is most active in Finland

---

## Dashboard Features

- KPI row: Total Applications, Total Hires, Hire Rate %, Avg Time to Hire
- Contextual tooltips with market benchmarks on every visual
- Dual-axis trend: Applications volume + Hire Rate % monthly
- Color by seniority: Junior / Mid / Senior breakdown
- Teal + Orange theme — clean, modern, accessible

---

## DAX Measures (Power BI version)

```dax
Hire Rate % = DIVIDE(SUM(fact_hiring[hires]), SUM(fact_hiring[applications]), 0)

Avg Time to Hire =
    DIVIDE(
        SUMX(fact_hiring, fact_hiring[hires] * fact_hiring[avg_time_to_hire_days]),
        SUM(fact_hiring[hires]), 0
    )

Applications YoY % =
    VAR _current = SUM(fact_hiring[applications])
    VAR _prior = CALCULATE(SUM(fact_hiring[applications]), dim_time[year] = MAX(dim_time[year]) - 1)
    RETURN DIVIDE(_current - _prior, _prior, 0)
```

---

## Project Status

✅ Complete — published on Tableau Public

---

## Files

```
01-hr-hiring-analytics/
├── README.md
├── python/
│   └── data_prep.py              ← StatFin API + synthetic funnel generation
├── sql/
│   └── schema.sql                ← star schema DDL + DAX reference
├── data/
│   ├── fact_hiring.csv           ← 1,792 rows
│   ├── dim_role.csv              ← 8 IT roles
│   ├── dim_region.csv            ← 8 Finnish regions
│   ├── dim_time.csv              ← 28 months (2024–2026)
│   └── statfin_employment.csv    ← Statistics Finland data
└── screenshots/
```
