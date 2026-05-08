-- ============================================================
-- HR Hiring Analytics — Star Schema
-- Project 01 | Julia Mosina | BI Portfolio Finland
-- ============================================================
-- Load order: dims first, then fact table
-- Compatible with: SQLite, PostgreSQL, SQL Server
-- ============================================================


-- ── Dimension: Role ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS dim_role (
    role_id     INTEGER PRIMARY KEY,
    role_name   TEXT    NOT NULL,  -- e.g. 'BI Analyst', 'Data Engineer'
    seniority   TEXT    NOT NULL,  -- 'Junior' | 'Mid' | 'Senior'
    domain      TEXT    NOT NULL   -- 'Analytics' | 'Engineering' | 'Development'
);


-- ── Dimension: Region ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS dim_region (
    region_id   INTEGER PRIMARY KEY,
    region_name TEXT    NOT NULL,  -- e.g. 'Helsinki', 'Tampere'
    is_capital  INTEGER NOT NULL,  -- 1 = Helsinki, 0 = other
    population  INTEGER NOT NULL
);


-- ── Dimension: Time ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS dim_time (
    time_id     INTEGER PRIMARY KEY,
    date        DATE    NOT NULL,
    year        INTEGER NOT NULL,
    quarter     INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    month_name  TEXT    NOT NULL,  -- e.g. 'January'
    year_month  TEXT    NOT NULL   -- e.g. '2025-03'
);


-- ── Fact: Hiring Funnel ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS fact_hiring (
    hiring_id               INTEGER PRIMARY KEY,
    time_id                 INTEGER NOT NULL REFERENCES dim_time(time_id),
    role_id                 INTEGER NOT NULL REFERENCES dim_role(role_id),
    region_id               INTEGER NOT NULL REFERENCES dim_region(region_id),

    -- Funnel stages
    applications            INTEGER NOT NULL DEFAULT 0,
    screening_passed        INTEGER NOT NULL DEFAULT 0,
    interviews_done         INTEGER NOT NULL DEFAULT 0,
    offers_made             INTEGER NOT NULL DEFAULT 0,
    hires                   INTEGER NOT NULL DEFAULT 0,

    -- KPIs
    avg_time_to_hire_days   INTEGER NOT NULL DEFAULT 0,
    open_positions          INTEGER NOT NULL DEFAULT 0
);


-- ── Indexes ───────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_fact_time   ON fact_hiring(time_id);
CREATE INDEX IF NOT EXISTS idx_fact_role   ON fact_hiring(role_id);
CREATE INDEX IF NOT EXISTS idx_fact_region ON fact_hiring(region_id);


-- ── Key DAX measures (reference for Power BI) ────────────────
/*
  -- Conversion rate: applications → hire
  Hire Rate =
    DIVIDE(SUM(fact_hiring[hires]), SUM(fact_hiring[applications]), 0)

  -- Average time-to-hire (weighted)
  Avg Time to Hire =
    DIVIDE(
        SUMX(fact_hiring, fact_hiring[hires] * fact_hiring[avg_time_to_hire_days]),
        SUM(fact_hiring[hires]),
        0
    )

  -- YoY change in applications
  Applications YoY % =
    VAR current = SUM(fact_hiring[applications])
    VAR prior   = CALCULATE(SUM(fact_hiring[applications]),
                      SAMEPERIODLASTYEAR(dim_time[date]))
    RETURN DIVIDE(current - prior, prior, 0)

  -- Funnel drop-off: screening stage
  Screening Drop-off % =
    1 - DIVIDE(SUM(fact_hiring[screening_passed]), SUM(fact_hiring[applications]), 0)
*/
