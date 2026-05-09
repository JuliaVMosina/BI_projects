# BI Portfolio — Julia Mosina

**BI & Data Analyst** | Power BI · Tableau · SQL · Python · DBT | Espoo, Finland

Hands-on projects built on Finnish open data and real-world business scenarios.
Each project follows the same structure: business problem → data → solution → measurable result.

---

## Portfolio Structure

This GitHub account contains three types of projects — each with a distinct purpose:

### 📊 This repository — Market & Research Projects
Open data, Finnish market research, public dashboards.
*"What is happening in the market?"*
Built with StatFin API, public job data, open economic indicators.
Audience: broad — recruiters, stakeholders, general public.

### 🏢 Corporate Simulation Repositories
Separate repos targeting specific companies: KONE, Oura, Tietoevry.
*"How would an internal dashboard look at this company?"*
Synthetic data modeled after real business operations. Power BI — the tool these companies actually use.
Each repo is written as a real work project, not a study exercise.
→ [kone-service-dashboard](https://github.com/JuliaVMosina/kone-service-dashboard)

### ⚙️ Engineering Project
→ [product-analytics-framework](https://github.com/JuliaVMosina/product-analytics-framework) — DBT · SQL · Python
*"How do you build an analytics platform from scratch?"*
Bachelor's thesis implementation: event taxonomy, dbt staging/intermediate/marts layers,
cohort retention, WIAU North Star Metric. Shows data engineering depth beyond BI visualization.

---

## Projects

### 01 · HR Hiring Analytics Dashboard
> *Where do candidates drop off in the IT hiring funnel?*

Finnish labor market data (stat.fi) combined with a synthetic hiring funnel.
Built to answer the question every recruiter has but rarely sees visualized.

**Stack:** Python · SQL · Power BI · Tableau Public  
**Skills demonstrated:** DAX · star schema · contextual tooltips · dual-tool delivery  
→ [View live dashboard](https://public.tableau.com/app/profile/julia.v.mosina/viz/HRHiringAnalyticsFinlandITMarket2024-2026/Dashboard3) · [View project](./01-hr-hiring-analytics/)

---

### 02 · Finland Tech Job Market Tracker
> *What skills does the Finnish market actually require in 2026?*

600 job postings from the Finnish IT market analyzed with Python NLP to extract
skill demand trends across seniority levels, companies, and regions.

**Stack:** Python · SQL · Tableau Public  
**Skills demonstrated:** data collection · keyword NLP · star schema · seniority segmentation · trend analysis  
→ [View live dashboard](https://public.tableau.com/app/profile/julia.v.mosina/viz/FinlandTechJobMarketSkillDemandTracker20242026/Dashboard1) · [View project](./02-job-market-tracker/)

---

### 03 · Finland Economic Pulse
> *GDP, employment, inflation — one dashboard, always up to date.*

Connected directly to the StatFin API (Statistics Finland).
Scheduled refresh in Power BI Service — data updates automatically.

**Stack:** Python · Tableau Public  
**Skills demonstrated:** REST API integration · star schema · time series visualization · KPI design  
→ [View live dashboard](https://public.tableau.com/app/profile/julia.v.mosina/viz/FinlandEconomicPulseGDPCPIEmployment20152026/Dashboard1) · [View project](./03-economic-pulse/)

---

## Tech Stack

| Tool | Usage |
|---|---|
| Power BI Desktop + Service | Main BI tool — reports, DAX, publish |
| Tableau Public | Alternative visualization, public sharing |
| SQL | Data modeling, star schema, aggregations |
| Python (pandas) | Data collection, cleaning, transformation |
| DBT | Data transformation, staging/intermediate/marts layers |
| Git / GitHub | Version control, portfolio |
| stat.fi StatFin API | Finnish open data source |

---

## Contact

[LinkedIn](https://www.linkedin.com/in/julia-mosina) · Espoo, Finland · Open to opportunities in Finland and EU
