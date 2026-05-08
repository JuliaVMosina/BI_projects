# 03 · Finland Economic Pulse

> **GDP, employment, inflation — one dashboard, always up to date.**

## Business Problem

Economic indicators are published by Statistics Finland monthly but scattered across
multiple reports. This dashboard consolidates them into a single view with automatic
refresh — no manual updates needed.

## Data Sources

- **stat.fi StatFin API** — GDP, CPI, employment rate, unemployment (open, free, official)
- **Eurostat API** *(optional)* — EU comparison

## Stack

| Layer | Tool |
|---|---|
| Data collection | Python (requests, StatFin API) |
| Transformation | Python (pandas) |
| Visualization | Power BI Desktop + DAX |
| Publishing | Power BI Service (scheduled refresh) |

## Key Metrics

- **GDP growth** — YoY and QoQ
- **Inflation (CPI)** — monthly trend
- **Employment rate** by region
- **Unemployment** — trend and 12-month moving average

## Dashboard Features

- **Scheduled refresh** — data updates automatically from StatFin API
- EU average comparison (Eurostat)
- Custom Finnish theme
- Drill-through: Finland → region → city
- Mobile layout

## Project Status

⏳ Planned — starts after Project 02

## Files

```
03-economic-pulse/
├── README.md
├── python/
│   └── statfin_loader.py   ← StatFin API connector
├── sql/
│   └── schema.sql
└── screenshots/
```
