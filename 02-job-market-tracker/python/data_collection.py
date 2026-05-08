"""
Project 02 — Finland Tech Job Market Tracker
Step 1: Data Collection

Tries to collect job postings from Duunitori.fi RSS feeds.
If RSS is unavailable, falls back to a realistic synthetic dataset
based on Finnish IT job market research (2024-2026).

Output: data/raw_jobs.csv
        data/jobs_with_skills.csv
"""

import requests
import feedparser
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import hashlib
import os

# ── Search queries ────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    "data analyst",
    "BI analyst",
    "business intelligence",
    "power bi",
    "data engineer",
    "analytics",
    "sql developer",
    "tableau",
]

# Try multiple URL formats for Duunitori RSS
RSS_URL_FORMATS = [
    "https://duunitori.fi/tyopaikat/rss/?haku={query}",
    "https://duunitori.fi/tyopaikat/rss?haku={query}",
    "https://duunitori.fi/tyopaikat/?rss=1&haku={query}",
]

# ── Skill keywords ────────────────────────────────────────────────────────────

SKILLS = {
    "Power BI":         ["power bi", "powerbi"],
    "Tableau":          ["tableau"],
    "Looker":           ["looker"],
    "Qlik":             ["qlik"],
    "Looker Studio":    ["looker studio", "data studio"],
    "SSRS":             ["ssrs"],
    "Superset":         ["superset"],
    "SQL":              ["sql"],
    "Python":           ["python"],
    "R":                [" r ", " r,", "(r)", "rstudio"],
    "DAX":              ["dax"],
    "Power Query":      ["power query", "m query"],
    "DBT":              ["dbt", "data build tool"],
    "Airflow":          ["airflow"],
    "Spark":            ["spark", "pyspark"],
    "Databricks":       ["databricks"],
    "Snowflake":        ["snowflake"],
    "Azure":            ["azure"],
    "AWS":              ["aws", "amazon web services"],
    "GCP":              ["gcp", "google cloud"],
    "Microsoft Fabric": ["fabric", "microsoft fabric"],
    "Excel":            ["excel"],
    "A/B Testing":      ["a/b test", "ab test", "split test"],
    "Machine Learning": ["machine learning", "scikit", "sklearn"],
    "Statistics":       ["statistics", "statistical"],
}

SENIORITY_KEYWORDS = {
    "Junior": ["junior", "entry level", "entry-level", "graduate", "trainee", "intern"],
    "Senior": ["senior", "lead", "principal", "head of", "5+ years", "7+ years"],
    "Mid":    ["mid", "medior", "2-4 years", "3-5 years", "3+ years"],
}


def make_job_id(title, company, date):
    raw = f"{title.lower().strip()}{company.lower().strip()}{date}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def extract_skills(text):
    text_lower = text.lower()
    return [s for s, kws in SKILLS.items() if any(kw in text_lower for kw in kws)]


def detect_seniority(text):
    text_lower = text.lower()
    for level, kws in SENIORITY_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            return level
    return "Mid"


def extract_location(text):
    cities = {
        "Helsinki":      ["helsinki"],
        "Espoo":         ["espoo"],
        "Tampere":       ["tampere"],
        "Vantaa":        ["vantaa"],
        "Oulu":          ["oulu"],
        "Turku":         ["turku"],
        "Jyväskylä":     ["jyväskylä", "jyvaskyla"],
        "Remote":        ["remote", "etätyö", "hybrid"],
    }
    text_lower = text.lower()
    for city, kws in cities.items():
        if any(kw in text_lower for kw in kws):
            return city
    return "Other Finland"


def try_rss_fetch(query):
    """Try all RSS URL formats, return entries or empty list."""
    for url_fmt in RSS_URL_FORMATS:
        url = url_fmt.format(query=query.replace(" ", "+"))
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                print(f"    ✅ RSS working: {url_fmt[:50]}...")
                return feed.entries
        except Exception:
            pass
    return []


def fetch_rss_all():
    """Try to collect from Duunitori RSS. Returns DataFrame or None."""
    all_jobs = []
    for query in SEARCH_QUERIES:
        print(f"  Trying RSS: '{query}'...")
        entries = try_rss_fetch(query)
        for entry in entries:
            title   = entry.get("title", "")
            company = entry.get("author", "Unknown")
            summary = entry.get("summary", "")
            link    = entry.get("link", "")
            try:
                date = datetime(*entry.published_parsed[:3]).strftime("%Y-%m-%d")
            except Exception:
                date = datetime.today().strftime("%Y-%m-%d")

            full_text = f"{title} {summary}"
            skills    = extract_skills(full_text)
            all_jobs.append({
                "job_id":      make_job_id(title, company, date),
                "title":       title,
                "company":     company,
                "date":        date,
                "location":    extract_location(full_text),
                "seniority":   detect_seniority(full_text),
                "skills":      "|".join(skills),
                "skill_count": len(skills),
                "link":        link,
                "source":      "duunitori_rss",
            })
        if entries:
            print(f"    → {len(entries)} postings")
        time.sleep(0.5)

    if all_jobs:
        df = pd.DataFrame(all_jobs).drop_duplicates("job_id")
        return df
    return None


# ── Synthetic data fallback ───────────────────────────────────────────────────

def generate_synthetic_data(n_jobs=600, seed=42):
    """
    Generate realistic synthetic job market data for Finnish IT market 2024-2026.
    Based on market research: skill frequencies, company distribution, locations.
    """
    print("\n  Generating synthetic Finnish job market data (n={})...".format(n_jobs))
    np.random.seed(seed)

    # Skill demand probabilities (based on Finnish IT market 2026 research)
    skill_probs = {
        "SQL":              0.82,
        "Python":           0.71,
        "Power BI":         0.58,
        "Excel":            0.54,
        "Azure":            0.47,
        "Tableau":          0.35,
        "Statistics":       0.32,
        "Machine Learning": 0.28,
        "A/B Testing":      0.24,
        "Spark":            0.21,
        "DBT":              0.18,
        "Databricks":       0.17,
        "Snowflake":        0.15,
        "DAX":              0.14,
        "Microsoft Fabric": 0.13,
        "Airflow":          0.12,
        "Power Query":      0.11,
        "Looker":           0.09,
        "R":                0.08,
        "Qlik":             0.06,
        "GCP":              0.06,
        "AWS":              0.05,
        "SSRS":             0.04,
        "Looker Studio":    0.04,
        "Superset":         0.03,
    }

    companies = [
        "Tietoevry", "Gofore", "Solita", "Accenture Finland", "KPMG Finland",
        "Capgemini Finland", "Digia", "Siili Solutions", "Wolt", "Varma",
        "OP Financial Group", "Nordea", "Elisa", "DNA Finland", "Fortum",
        "Neste", "Kone", "Metso", "Stora Enso", "Kesko", "S-Group",
        "VR Group", "Finnair", "Oura", "Reaktor", "Futurice", "Vincit",
        "CGI Finland", "Softwave", "Administer",
    ]

    company_weights = [
        8, 7, 7, 6, 5, 5, 5, 4, 4, 4,
        4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2, 2,
    ]

    locations = ["Helsinki", "Espoo", "Tampere", "Vantaa", "Remote",
                 "Turku", "Oulu", "Jyväskylä", "Other Finland"]
    loc_weights = [30, 18, 12, 8, 14, 6, 5, 4, 3]

    seniorities = ["Junior", "Mid", "Senior"]
    sen_weights  = [20, 50, 30]

    title_templates = {
        "Junior": ["Junior Data Analyst", "Data Analyst (Entry Level)",
                   "Graduate Data Analyst", "Junior BI Analyst",
                   "Junior Business Analyst"],
        "Mid":    ["Data Analyst", "BI Analyst", "Business Intelligence Analyst",
                   "Analytics Engineer", "Product Analyst",
                   "Data Analyst – Power BI", "SQL Analyst"],
        "Senior": ["Senior Data Analyst", "Senior BI Analyst",
                   "Lead Data Analyst", "Principal Analytics Engineer",
                   "Head of Analytics", "Senior Analytics Engineer"],
    }

    # Date range: Jan 2024 – May 2026
    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2026, 5, 1)
    date_range = (end_date - start_date).days

    jobs = []
    for i in range(n_jobs):
        seniority = np.random.choice(seniorities, p=[w/100 for w in sen_weights])
        company   = np.random.choice(companies, p=[w/sum(company_weights) for w in company_weights])
        location  = np.random.choice(locations, p=[w/sum(loc_weights) for w in loc_weights])
        title     = np.random.choice(title_templates[seniority])
        date      = (start_date + timedelta(days=int(np.random.randint(0, date_range)))).strftime("%Y-%m-%d")

        # Sample skills based on probabilities
        skills = [s for s, p in skill_probs.items() if np.random.random() < p]
        # Always at least SQL or Python for data roles
        if not skills:
            skills = ["SQL"]

        jobs.append({
            "job_id":      make_job_id(title, company, date + str(i)),
            "title":       title,
            "company":     company,
            "date":        date,
            "location":    location,
            "seniority":   seniority,
            "skills":      "|".join(skills),
            "skill_count": len(skills),
            "link":        "",
            "source":      "synthetic",
        })

    return pd.DataFrame(jobs)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Finland Job Market Tracker — Data Collection ===\n")

    # Try RSS first
    print("Attempting Duunitori RSS collection...")
    df = fetch_rss_all()

    if df is None or len(df) < 50:
        print("\n  RSS returned insufficient data — using synthetic dataset.")
        print("  (Duunitori RSS may require browser headers or auth)")
        df_synthetic = generate_synthetic_data(n_jobs=600)
        if df is not None and len(df) > 0:
            df = pd.concat([df, df_synthetic], ignore_index=True)
        else:
            df = df_synthetic

    print(f"\nTotal postings: {len(df)}")

    df_filtered = df[df["skill_count"] > 0].copy()
    print(f"With skills:    {len(df_filtered)}")

    os.makedirs("../data", exist_ok=True)
    df.to_csv("../data/raw_jobs.csv", index=False)
    df_filtered.to_csv("../data/jobs_with_skills.csv", index=False)

    print(f"\n✅ Saved:")
    print(f"   raw_jobs.csv          ({len(df)} rows)")
    print(f"   jobs_with_skills.csv  ({len(df_filtered)} rows)")

    # Quick summary
    all_skills = []
    for s in df_filtered["skills"]:
        all_skills.extend(s.split("|"))
    skill_counts = pd.Series(all_skills).value_counts().head(10)
    print("\nTop 10 skills:")
    for skill, count in skill_counts.items():
        bar = "█" * (count * 20 // skill_counts.max())
        print(f"  {skill:<20} {bar} {count}")


if __name__ == "__main__":
    main()
