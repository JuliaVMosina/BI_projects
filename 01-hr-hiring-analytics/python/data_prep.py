"""
HR Hiring Analytics Dashboard — Data Preparation
=================================================
Project 01 | Julia Mosina | BI Portfolio Finland

Sources:
  - StatFin API (stat.fi) — employment by industry and region
  - Synthetic hiring funnel — Applications → Screening → Interview → Offer → Hire

Output (saved to /data/):
  - dim_role.csv
  - dim_region.csv
  - dim_time.csv
  - fact_hiring.csv
  - statfin_employment.csv
"""

import requests
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, date

# ── Config ────────────────────────────────────────────────────────────────────

STATFIN_BASE = "https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ── Dimensions ────────────────────────────────────────────────────────────────

ROLES = [
    {"role_id": 1, "role_name": "BI Analyst",          "seniority": "Mid",    "domain": "Analytics"},
    {"role_id": 2, "role_name": "Data Engineer",        "seniority": "Mid",    "domain": "Engineering"},
    {"role_id": 3, "role_name": "Data Analyst",         "seniority": "Junior", "domain": "Analytics"},
    {"role_id": 4, "role_name": "Software Developer",   "seniority": "Mid",    "domain": "Development"},
    {"role_id": 5, "role_name": "BI Developer",         "seniority": "Senior", "domain": "Analytics"},
    {"role_id": 6, "role_name": "ML Engineer",          "seniority": "Senior", "domain": "Engineering"},
    {"role_id": 7, "role_name": "Product Analyst",      "seniority": "Mid",    "domain": "Analytics"},
    {"role_id": 8, "role_name": "Data Scientist",       "seniority": "Senior", "domain": "Analytics"},
]

REGIONS = [
    {"region_id": 1, "region_name": "Helsinki",    "is_capital": True,  "population": 658457},
    {"region_id": 2, "region_name": "Espoo",       "is_capital": False, "population": 302472},
    {"region_id": 3, "region_name": "Tampere",     "is_capital": False, "population": 244223},
    {"region_id": 4, "region_name": "Vantaa",      "is_capital": False, "population": 238047},
    {"region_id": 5, "region_name": "Oulu",        "is_capital": False, "population": 210481},
    {"region_id": 6, "region_name": "Turku",       "is_capital": False, "population": 197853},
    {"region_id": 7, "region_name": "Jyväskylä",  "is_capital": False, "population": 146193},
    {"region_id": 8, "region_name": "Kuopio",      "is_capital": False, "population": 121068},
]

# Funnel conversion rates by seniority level
CONVERSION_RATES = {
    "Junior": {"screening": 0.45, "interview": 0.50, "offer": 0.55, "hire": 0.75},
    "Mid":    {"screening": 0.35, "interview": 0.55, "offer": 0.60, "hire": 0.80},
    "Senior": {"screening": 0.25, "interview": 0.65, "offer": 0.70, "hire": 0.85},
}

# Average time-to-hire benchmarks in days by seniority
TTH_BENCHMARKS = {
    "Junior": {"mean": 28, "std": 7},
    "Mid":    {"mean": 38, "std": 10},
    "Senior": {"mean": 52, "std": 14},
}


# ── 1. Dimension tables ───────────────────────────────────────────────────────

def build_dim_role():
    df = pd.DataFrame(ROLES)
    df.to_csv(os.path.join(OUTPUT_DIR, "dim_role.csv"), index=False)
    print(f"✓ dim_role.csv — {len(df)} rows")
    return df


def build_dim_region():
    df = pd.DataFrame(REGIONS)
    df.to_csv(os.path.join(OUTPUT_DIR, "dim_region.csv"), index=False)
    print(f"✓ dim_region.csv — {len(df)} rows")
    return df


def build_dim_time(start="2024-01-01", end="2026-04-30"):
    dates = pd.date_range(start=start, end=end, freq="MS")  # month start
    df = pd.DataFrame({
        "time_id":      range(1, len(dates) + 1),
        "date":         dates,
        "year":         dates.year,
        "quarter":      dates.quarter,
        "month":        dates.month,
        "month_name":   dates.strftime("%B"),
        "year_month":   dates.strftime("%Y-%m"),
    })
    df.to_csv(os.path.join(OUTPUT_DIR, "dim_time.csv"), index=False)
    print(f"✓ dim_time.csv — {len(df)} rows")
    return df


# ── 2. Fact table — synthetic hiring funnel ───────────────────────────────────

def build_fact_hiring(dim_role, dim_region, dim_time):
    records = []
    hiring_id = 1

    for _, time_row in dim_time.iterrows():
        for _, role_row in dim_role.iterrows():
            for _, region_row in dim_region.iterrows():

                seniority = role_row["seniority"]
                rates = CONVERSION_RATES[seniority]
                tth = TTH_BENCHMARKS[seniority]

                # Volume: Helsinki gets ~3x more applications, capital bonus
                base_apps = np.random.poisson(lam=12 if region_row["is_capital"] else 4)
                applications = max(1, base_apps)

                # Funnel calculation
                screening  = max(0, round(applications  * rates["screening"]  * np.random.uniform(0.85, 1.15)))
                interviews = max(0, round(screening      * rates["interview"]  * np.random.uniform(0.85, 1.15)))
                offers     = max(0, round(interviews     * rates["offer"]      * np.random.uniform(0.85, 1.15)))
                hires      = max(0, round(offers         * rates["hire"]       * np.random.uniform(0.85, 1.15)))

                # Clamp: each stage <= previous
                screening  = min(screening,  applications)
                interviews = min(interviews, screening)
                offers     = min(offers,     interviews)
                hires      = min(hires,      offers)

                # Time-to-hire in days
                avg_tth = round(np.random.normal(tth["mean"], tth["std"]))
                avg_tth = max(14, avg_tth)

                records.append({
                    "hiring_id":          hiring_id,
                    "time_id":            int(time_row["time_id"]),
                    "role_id":            int(role_row["role_id"]),
                    "region_id":          int(region_row["region_id"]),
                    "applications":       applications,
                    "screening_passed":   screening,
                    "interviews_done":    interviews,
                    "offers_made":        offers,
                    "hires":              hires,
                    "avg_time_to_hire_days": avg_tth,
                    "open_positions":     max(0, np.random.poisson(3)),
                })
                hiring_id += 1

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "fact_hiring.csv"), index=False)
    print(f"✓ fact_hiring.csv — {len(df)} rows")
    return df


# ── 3. StatFin API — IT employment by region ─────────────────────────────────

def fetch_statfin_employment():
    """
    Fetches employed persons in IT/information service activities
    from Statistics Finland StatFin API.
    Table: tyonv/statfin_tyonv_pxt_135y.px — Labour force survey
    """
    url = f"{STATFIN_BASE}/tyonv/statfin_tyonv_pxt_135y.px"

    # Query: IT sector (TOL 2008 code J = Information and communication)
    payload = {
        "query": [
            {
                "code": "Toimiala",
                "selection": {"filter": "item", "values": ["J"]}
            },
            {
                "code": "Tiedot",
                "selection": {"filter": "item", "values": ["vm01"]}  # employed persons (thousands)
            }
        ],
        "response": {"format": "json-stat2"}
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Parse JSON-stat2 response
        values = data["value"]
        time_labels = list(data["dimension"]["Vuosineljännes"]["category"]["label"].values())

        df = pd.DataFrame({
            "quarter":              time_labels,
            "it_employed_thousands": values,
        })
        df["it_employed_thousands"] = pd.to_numeric(df["it_employed_thousands"], errors="coerce")
        df = df.dropna()

        df.to_csv(os.path.join(OUTPUT_DIR, "statfin_employment.csv"), index=False)
        print(f"✓ statfin_employment.csv — {len(df)} rows (StatFin API)")
        return df

    except Exception as e:
        print(f"⚠ StatFin API unavailable ({e}), generating placeholder data")
        # Fallback: realistic IT employment trend for Finland 2020–2026
        quarters = pd.date_range("2020Q1", periods=25, freq="QS")
        employed = [169, 171, 174, 176, 179, 182, 185, 188, 191, 193,
                    195, 198, 201, 204, 207, 209, 212, 215, 218, 220,
                    222, 225, 227, 229, 231]
        df = pd.DataFrame({
            "quarter":               [f"{q.year}Q{(q.month - 1) // 3 + 1}" for q in quarters],
            "it_employed_thousands": employed[:len(quarters)],
        })
        df.to_csv(os.path.join(OUTPUT_DIR, "statfin_employment.csv"), index=False)
        print(f"✓ statfin_employment.csv — {len(df)} rows (fallback data)")
        return df


# ── 4. Summary stats ──────────────────────────────────────────────────────────

def print_summary(fact):
    print("\n── Dataset Summary ───────────────────────────────────")
    print(f"Total applications:    {fact['applications'].sum():,}")
    print(f"Total hires:           {fact['hires'].sum():,}")
    overall_rate = fact['hires'].sum() / fact['applications'].sum() * 100
    print(f"Overall hire rate:     {overall_rate:.1f}%")
    print(f"Avg time-to-hire:      {fact['avg_time_to_hire_days'].mean():.0f} days")
    print(f"Avg open positions:    {fact['open_positions'].mean():.1f}")
    print("──────────────────────────────────────────────────────")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building HR Hiring Analytics dataset...\n")

    dim_role   = build_dim_role()
    dim_region = build_dim_region()
    dim_time   = build_dim_time()
    fact       = build_fact_hiring(dim_role, dim_region, dim_time)
    _          = fetch_statfin_employment()

    print_summary(fact)
    print(f"\n✅ All files saved to: {os.path.abspath(OUTPUT_DIR)}")
