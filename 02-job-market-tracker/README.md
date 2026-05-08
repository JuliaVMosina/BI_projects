# 02 · Finland Tech Job Market — Skill Demand Tracker

> **What skills does the Finnish IT market actually require in 2026?**

## Live Dashboard

**→ [View on Tableau Public](https://public.tableau.com/app/profile/julia.v.mosina/viz/FinlandTechJobMarketSkillDemandTracker20242026/Dashboard1)**

---

## Business Problem

BI and Data Analyst candidates in Finland often rely on intuition when choosing what skills to develop.
This dashboard answers the question with data: which tools and technologies appear most frequently
in Finnish IT job postings, how demand has shifted over 2024–2026, and how requirements differ
by seniority level.

---

## Data Sources

- **Duunitori.fi** — Finland's largest job board (RSS feed, open access)
- **Synthetic dataset** — 600 job postings modeled on Finnish IT market research (2024–2026),
  used as fallback when RSS returns insufficient data. Skill probabilities based on
  market analysis of BI/Data Analyst roles in Finland.

---

## Stack

| Layer | Tool |
|---|---|
| Data collection | Python (feedparser, requests) |
| Skill extraction | Python (keyword matching NLP) |
| Data modeling | SQL — star schema |
| Visualization | Tableau Public |

---

## Data Model

```
dim_skill       dim_company     dim_time        dim_location
    \               |               |               /
     └──────────── fact_job_skills ────────────────┘
```

**fact_job_skills** — one row per job posting x skill (3,628 rows)

| Table | Rows | Key fields |
|---|---|---|
| fact_job_skills | 3,628 | job_id, skill_id, company_id, time_id, location_id, seniority |
| dim_skill | 25 | skill_name, category |
| dim_company | 30 | company_name |
| dim_time | 436 | date, year, month, quarter |
| dim_location | 9 | location_name, region, is_capital_region |

---

## Key Metrics

- **Top 10 in-demand skills** - ranked by number of job postings
- **Skill demand trend** - monthly view, Jan 2024 to May 2026
- **Skills by seniority** - Junior / Mid / Senior breakdown per skill
- **Most active employers** - top 10 companies by posting volume
- **Location split** - Helsinki capital region vs rest of Finland

---

## Dashboard Features

- KPI row: Total Postings - #1 Skill - Top Employer
- Seniority filter applies to all charts simultaneously
- Color-coded skill categories (BI Tool / Language / Cloud / Data Engineering)
- Capital region highlighted in Location Split (orange = Helsinki/Espoo/Vantaa)
- Timeline: Dec 2023 to Apr 2026

---

## Key Findings

- **SQL** is the most demanded skill (82% of postings) - foundational across all seniority levels
- **Python** follows at 70% - essential for Mid and Senior roles
- **Power BI** ranks #3 (61%) - dominant BI tool in Finnish market
- **DBT** appears in 19% of postings - growing trend in 2025-2026
- **Microsoft Fabric** already visible at 15% - emerging technology to watch
- **Helsinki capital region** accounts for ~56% of all postings

---

## Files

```
02-job-market-tracker/
├── README.md
├── python/
│   ├── data_collection.py    <- Duunitori RSS + synthetic data generation
│   └── data_prep.py          <- star schema CSV builder
├── sql/
│   └── schema.sql            <- DDL + key analytical queries
├── data/
│   ├── raw_jobs.csv          <- 600 job postings
│   ├── jobs_with_skills.csv  <- filtered (skill_count > 0)
│   ├── fact_job_skills.csv   <- 3,628 rows
│   ├── dim_skill.csv         <- 25 skills with categories
│   ├── dim_company.csv       <- 30 companies
│   ├── dim_time.csv          <- 436 dates
│   └── dim_location.csv      <- 9 Finnish locations
└── screenshots/
```

---

## Project Status

Complete - published on Tableau Public
