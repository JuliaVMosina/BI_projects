"""
Project 03 — Finland Economic Pulse
Step 2: Build unified star schema for dashboard

Input:  data/raw_gdp.csv
        data/raw_cpi.csv
        data/raw_employment.csv
        data/raw_unemployment.csv

Output: data/fact_indicators.csv  ← one row per indicator × date
        data/dim_indicator.csv
        data/dim_time.csv
"""

import pandas as pd
import os


def build_fact_and_dims():
    print("=== Finland Economic Pulse — Data Preparation ===\n")

    # Load raw files
    gdp  = pd.read_csv("../data/raw_gdp.csv")
    cpi  = pd.read_csv("../data/raw_cpi.csv")
    emp  = pd.read_csv("../data/raw_employment.csv")
    unemp = pd.read_csv("../data/raw_unemployment.csv")

    # Normalise to long format: date, indicator_name, value, frequency
    gdp_long = gdp[["date", "year", "quarter", "gdp_yoy_pct"]].copy()
    gdp_long.columns = ["date", "year", "period_num", "value"]
    gdp_long["indicator"] = "GDP Growth YoY %"
    gdp_long["frequency"] = "Quarterly"
    gdp_long["unit"]      = "%"

    cpi_long = cpi[["date", "year", "month", "cpi_yoy_pct"]].copy()
    cpi_long.columns = ["date", "year", "period_num", "value"]
    cpi_long["indicator"] = "CPI Inflation YoY %"
    cpi_long["frequency"] = "Monthly"
    cpi_long["unit"]      = "%"

    emp_long = emp[["date", "year", "quarter", "employment_rate_pct"]].copy()
    emp_long.columns = ["date", "year", "period_num", "value"]
    emp_long["indicator"] = "Employment Rate %"
    emp_long["frequency"] = "Quarterly"
    emp_long["unit"]      = "%"

    unemp_long = unemp[["date", "year", "month", "unemployment_rate_pct"]].copy()
    unemp_long.columns = ["date", "year", "period_num", "value"]
    unemp_long["indicator"] = "Unemployment Rate %"
    unemp_long["frequency"] = "Monthly"
    unemp_long["unit"]      = "%"

    # Combine
    fact = pd.concat([gdp_long, cpi_long, emp_long, unemp_long], ignore_index=True)
    fact["date"] = pd.to_datetime(fact["date"])

    # dim_indicator
    dim_indicator = pd.DataFrame({
        "indicator_id": [1, 2, 3, 4],
        "indicator":    ["GDP Growth YoY %", "CPI Inflation YoY %",
                         "Employment Rate %", "Unemployment Rate %"],
        "category":     ["Economy", "Prices", "Labour Market", "Labour Market"],
        "frequency":    ["Quarterly", "Monthly", "Quarterly", "Monthly"],
        "unit":         ["%", "%", "%", "%"],
        "description":  [
            "Real GDP growth compared to same quarter previous year",
            "Consumer Price Index change compared to same month previous year",
            "Share of employed persons aged 15-64 in total population",
            "Share of unemployed persons in labour force",
        ]
    })

    # dim_time — all unique dates
    all_dates = fact["date"].sort_values().unique()
    dim_time = pd.DataFrame({"date": all_dates})
    dim_time["time_id"]    = range(1, len(dim_time) + 1)
    dim_time["year"]       = dim_time["date"].dt.year
    dim_time["quarter"]    = dim_time["date"].dt.quarter
    dim_time["month"]      = dim_time["date"].dt.month
    dim_time["month_name"] = dim_time["date"].dt.strftime("%B")
    dim_time["date"]       = dim_time["date"].dt.strftime("%Y-%m-%d")
    dim_time = dim_time[["time_id", "date", "year", "quarter", "month", "month_name"]]

    # Add keys to fact
    indicator_map = dim_indicator.set_index("indicator")["indicator_id"].to_dict()
    time_map      = dim_time.set_index("date")["time_id"].to_dict()

    fact["date_str"]      = fact["date"].dt.strftime("%Y-%m-%d")
    fact["indicator_id"]  = fact["indicator"].map(indicator_map)
    fact["time_id"]       = fact["date_str"].map(time_map)
    fact["value"]         = fact["value"].round(2)

    fact_out = fact[["time_id", "indicator_id", "indicator",
                     "date_str", "year", "value", "frequency", "unit"]].copy()
    fact_out.rename(columns={"date_str": "date"}, inplace=True)

    # Save
    os.makedirs("../data", exist_ok=True)
    fact_out.to_csv("../data/fact_indicators.csv", index=False)
    dim_indicator.to_csv("../data/dim_indicator.csv", index=False)
    dim_time.to_csv("../data/dim_time.csv", index=False)

    print("✅ Saved:")
    print(f"   fact_indicators.csv  ({len(fact_out)} rows)")
    print(f"   dim_indicator.csv    ({len(dim_indicator)} indicators)")
    print(f"   dim_time.csv         ({len(dim_time)} dates)")

    print("\nLatest values per indicator:")
    latest = fact_out.sort_values("date").groupby("indicator").last()[["date", "value"]]
    print(latest.to_string())


if __name__ == "__main__":
    build_fact_and_dims()
