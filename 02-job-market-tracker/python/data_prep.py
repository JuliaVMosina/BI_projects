"""
Project 02 — Finland Tech Job Market Tracker
Step 2: Data Preparation — build star schema CSVs

Input:  data/jobs_with_skills.csv
Output: data/fact_job_skills.csv
        data/dim_skill.csv
        data/dim_company.csv
        data/dim_time.csv
        data/dim_location.csv
"""

import pandas as pd
import os

# ── Skill categories ──────────────────────────────────────────────────────────

SKILL_CATEGORIES = {
    "Power BI":         "BI Tool",
    "Tableau":          "BI Tool",
    "Looker":           "BI Tool",
    "Qlik":             "BI Tool",
    "Looker Studio":    "BI Tool",
    "SSRS":             "BI Tool",
    "Superset":         "BI Tool",
    "SQL":              "Language",
    "Python":           "Language",
    "R":                "Language",
    "DAX":              "Language",
    "Power Query":      "Language",
    "DBT":              "Data Engineering",
    "dbt":              "Data Engineering",
    "Airflow":          "Data Engineering",
    "Spark":            "Data Engineering",
    "Databricks":       "Data Engineering",
    "Snowflake":        "Data Engineering",
    "Azure":            "Cloud",
    "AWS":              "Cloud",
    "GCP":              "Cloud",
    "Microsoft Fabric": "Cloud",
    "Excel":            "General",
    "A/B Testing":      "Analytics Method",
    "Machine Learning": "Analytics Method",
    "Statistics":       "Analytics Method",
}


def build_dim_skill(skills_series: pd.Series) -> pd.DataFrame:
    all_skills = set()
    for s in skills_series.dropna():
        all_skills.update(s.split("|"))
    all_skills.discard("")

    dim = pd.DataFrame({
        "skill_id":   range(1, len(all_skills) + 1),
        "skill_name": sorted(all_skills),
    })
    dim["category"] = dim["skill_name"].map(SKILL_CATEGORIES).fillna("Other")
    return dim


def build_dim_company(df: pd.DataFrame) -> pd.DataFrame:
    companies = df["company"].dropna().unique()
    dim = pd.DataFrame({
        "company_id":   range(1, len(companies) + 1),
        "company_name": sorted(companies),
    })
    return dim


def build_dim_time(df: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(df["date"].dropna().unique())
    dim = pd.DataFrame({"date": sorted(dates)})
    dim["time_id"] = range(1, len(dim) + 1)
    dim["year"]    = dim["date"].dt.year
    dim["month"]   = dim["date"].dt.month
    dim["month_name"] = dim["date"].dt.strftime("%B")
    dim["week"]    = dim["date"].dt.isocalendar().week.astype(int)
    dim["quarter"] = dim["date"].dt.quarter
    dim["date"]    = dim["date"].dt.strftime("%Y-%m-%d")
    return dim[["time_id", "date", "year", "quarter", "month", "month_name", "week"]]


def build_dim_location(df: pd.DataFrame) -> pd.DataFrame:
    locations = df["location"].dropna().unique()
    region_map = {
        "Helsinki":    "Uusimaa",
        "Espoo":       "Uusimaa",
        "Vantaa":      "Uusimaa",
        "Tampere":     "Pirkanmaa",
        "Turku":       "Southwest Finland",
        "Oulu":        "North Ostrobothnia",
        "Jyväskylä":   "Central Finland",
        "Remote":      "Remote",
        "Other Finland": "Other",
    }
    dim = pd.DataFrame({
        "location_id":   range(1, len(locations) + 1),
        "location_name": sorted(locations),
    })
    dim["region"] = dim["location_name"].map(region_map).fillna("Other")
    dim["is_capital_region"] = dim["location_name"].isin(
        ["Helsinki", "Espoo", "Vantaa"]
    )
    return dim


def build_fact_job_skills(df, dim_skill, dim_company, dim_time, dim_location):
    """Explode skills — one row per job × skill."""
    rows = []
    skill_lookup    = dim_skill.set_index("skill_name")["skill_id"].to_dict()
    company_lookup  = dim_company.set_index("company_name")["company_id"].to_dict()
    time_lookup     = dim_time.set_index("date")["time_id"].to_dict()
    location_lookup = dim_location.set_index("location_name")["location_id"].to_dict()

    for _, row in df.iterrows():
        if not row["skills"]:
            continue
        skills = [s for s in row["skills"].split("|") if s]
        for skill in skills:
            rows.append({
                "job_id":      row["job_id"],
                "skill_id":    skill_lookup.get(skill),
                "company_id":  company_lookup.get(row["company"]),
                "time_id":     time_lookup.get(row["date"]),
                "location_id": location_lookup.get(row["location"]),
                "seniority":   row["seniority"],
                "title":       row["title"],
            })

    return pd.DataFrame(rows).dropna(subset=["skill_id", "company_id", "time_id"])


def main():
    print("=== Finland Job Market Tracker — Data Preparation ===\n")

    input_path = "../data/jobs_with_skills.csv"
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        print("   Run data_collection.py first.")
        return

    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    print(f"Loaded {len(df)} job postings\n")

    # Build dimensions
    dim_skill    = build_dim_skill(df["skills"])
    dim_company  = build_dim_company(df)
    dim_time     = build_dim_time(df)
    dim_location = build_dim_location(df)

    # Build fact
    fact = build_fact_job_skills(df, dim_skill, dim_company, dim_time, dim_location)

    # Save
    os.makedirs("../data", exist_ok=True)
    dim_skill.to_csv("../data/dim_skill.csv", index=False)
    dim_company.to_csv("../data/dim_company.csv", index=False)
    dim_time.to_csv("../data/dim_time.csv", index=False)
    dim_location.to_csv("../data/dim_location.csv", index=False)
    fact.to_csv("../data/fact_job_skills.csv", index=False)

    print("✅ Saved:")
    print(f"   dim_skill.csv     ({len(dim_skill)} skills)")
    print(f"   dim_company.csv   ({len(dim_company)} companies)")
    print(f"   dim_time.csv      ({len(dim_time)} dates)")
    print(f"   dim_location.csv  ({len(dim_location)} locations)")
    print(f"   fact_job_skills.csv ({len(fact)} rows)")

    print("\nTop 15 skills in demand:")
    skill_counts = fact.merge(dim_skill, on="skill_id")
    top = skill_counts["skill_name"].value_counts().head(15)
    for skill, count in top.items():
        bar = "█" * (count * 30 // top.max())
        print(f"  {skill:<20} {bar} {count}")


if __name__ == "__main__":
    main()
