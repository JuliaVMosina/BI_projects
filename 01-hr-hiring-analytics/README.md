# 01 · HR Hiring Analytics Dashboard

> **Where do candidates drop off in the IT hiring funnel in Finland?**

## Business Problem

Hiring managers in Finnish IT companies often lack visibility into where candidates drop off
and how their time-to-hire compares to the market. This dashboard answers both questions
using public labor market data and a modeled hiring funnel.

## Data Sources

- **stat.fi StatFin API** — employment by industry and region (open, free)
- **Synthetic hiring funnel** — modeled stages: Applications → Screening → Interview → Offer → Hire

## Stack

| Layer | Tool |
|---|---|
| Data collection & prep | Python (pandas, requests) |
| Data modeling | SQL — star schema |
| Visualization | Power BI Desktop + DAX |
| Publishing | Power BI Service |

## Data Model

```
dim_role       dim_region      dim_time
    \               |               /
     └──────── fact_hiring ────────┘
```

## Key Metrics

- **Time-to-hire** by role and region
- **Conversion rate** at each funnel stage
- **Benchmark** — pipeline metrics vs. market average (stat.fi)
- **Open positions heatmap** — where IT hiring is most active

## Dashboard Features

- Drill-through: region → role details
- Custom corporate theme
- Mobile layout (Power BI Mobile)
- Tooltip pages with market context

## Project Status

🔨 In progress

## Files

```
01-hr-hiring-analytics/
├── README.md
├── python/
│   └── data_prep.py        ← StatFin API + synthetic funnel generation
├── sql/
│   └── schema.sql          ← star schema DDL
└── screenshots/            ← dashboard previews
```
