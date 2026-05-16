# Aspia Group — Executive BI Dashboard (Power BI)

**Domain:** Finance & HR Outsourcing | **Tool:** Power BI | **Year:** 2026

A 4-page executive dashboard built on synthetic data modelled after Aspia Group —
a Nordics-based finance and payroll outsourcing company with 3,000+ employees across 100+ offices.

---

## Pages

### 1. Overview
High-level KPIs, revenue by region (map + bar), client funnel, NPS trend, service line donut.
> *Key metrics: Total Revenue EUR, Active Clients, Retention Rate %, NPS Score*

### 2. Financial Performance
Revenue dynamics by service line (Accounting, Payroll, HR Services, Tax & Legal).
MoM % growth line chart, YoY comparison, regional revenue breakdown, service mix matrix.
> *Key metrics: Revenue MoM %, Revenue YoY %, Revenue per Client EUR*

### 3. Client Portfolio
Client base growth 2022–2024: peak ~450 clients in mid-2023, churn signal emerging in 2024.
New vs churned clients by month, industry distribution (donut), client size segmentation.
> *Key metrics: Active Clients, Retention Rate %, NPS Score, New/Churned Clients*

### 4. Operational Efficiency
Employee utilization by role (~87% avg), contracts by service line (active vs cancelled),
avg services per client growth trend (2022–2024), experience vs clients managed scatter.
> *Key metrics: Avg Utilization %, Avg Clients per Employee, Active Contracts*

---

## Data Model

| Table | Description |
|---|---|
| `monthly_revenue` | Revenue by month, region, service line (2022–2024) |
| `monthly_kpis` | Operational KPIs: retention, NPS, new/churned clients, avg services |
| `clients` | Client master: industry, size, status, region, acquired/churn date |
| `contracts` | Contract-level data: service line, monthly value, status |
| `employees` | Employee data: role, utilization %, clients managed, years experience |
| `MonthTable` | Calculated date dimension for time intelligence |

---

## Key DAX Measures

```dax
-- Month-over-month revenue growth using date arithmetic
Revenue MoM % =
VAR CurrentDate = SELECTEDVALUE(monthly_revenue[month])
VAR CurYear     = YEAR(CurrentDate)
VAR CurMonth    = MONTH(CurrentDate)
VAR PrevDate    = DATE(IF(CurMonth=1, CurYear-1, CurYear), IF(CurMonth=1, 12, CurMonth-1), 1)
VAR PriorRev    = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[month] = PrevDate)
RETURN DIVIDE(SUM(monthly_revenue[revenue_eur]) - PriorRev, PriorRev) * 100

-- Year-over-year comparison
Revenue YoY % =
VAR RevCurrent = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[year] = 2024)
VAR RevPrior   = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[year] = 2023)
RETURN DIVIDE(RevCurrent - RevPrior, RevPrior) * 100
```

---

## Skills Demonstrated

`Power BI` · `DAX` · `Power Query` · `Data Modeling` · `Star Schema` · `Time Intelligence` · `KPI Design` · `Business Storytelling`

---

## Screenshots

| Page | Preview |
|---|---|
| Overview | *(add screenshot)* |
| Financial Performance | *(add screenshot)* |
| Client Portfolio | *(add screenshot)* |
| Operational Efficiency | *(add screenshot)* |
