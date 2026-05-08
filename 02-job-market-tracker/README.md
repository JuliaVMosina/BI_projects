# 02 · Finland Tech Job Market Tracker

> **What skills does the Finnish BI/Data market actually require in 2026?**

## Business Problem

Most job seekers look at job postings one by one. This dashboard aggregates hundreds of postings,
extracts skill requirements with Python NLP, and shows demand trends — updated monthly.

## Data Sources

- **Duunitori** — Finnish job board (public listings)
- **LinkedIn Finland** — job posting data
- **Kaggle datasets** — supplementary job market data

## Stack

| Layer | Tool |
|---|---|
| Data collection | Python (requests, BeautifulSoup) |
| NLP skill extraction | Python (spaCy / keyword matching) |
| Aggregation | SQL |
| Visualization | Tableau Public |

## Key Metrics

- **Top-20 skills** by mention frequency
- **Demand trend** by month — which skills are growing
- **Salary ranges** by role and city
- **Company hiring activity** — who is hiring most actively

## Dashboard Features

- Skill word cloud
- Helsinki vs. rest of Finland comparison
- Junior / Mid / Senior filter
- Monthly update

## Project Status

⏳ Planned — starts after Project 01

## Files

```
02-job-market-tracker/
├── README.md
├── python/
│   ├── collect_jobs.py     ← data collection
│   └── extract_skills.py   ← NLP skill extraction
├── sql/
│   └── aggregations.sql
└── screenshots/
```
