-- ============================================================
-- Project 02 — Finland Tech Job Market Tracker
-- Star Schema DDL
-- ============================================================

-- Dimension: Skills
CREATE TABLE dim_skill (
    skill_id    INTEGER PRIMARY KEY,
    skill_name  VARCHAR(50)  NOT NULL,
    category    VARCHAR(50)  NOT NULL  -- BI Tool / Language / Cloud / Data Engineering / Analytics Method
);

-- Dimension: Companies
CREATE TABLE dim_company (
    company_id   INTEGER PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL
);

-- Dimension: Time
CREATE TABLE dim_time (
    time_id    INTEGER PRIMARY KEY,
    date       DATE         NOT NULL,
    year       INTEGER      NOT NULL,
    quarter    INTEGER      NOT NULL,
    month      INTEGER      NOT NULL,
    month_name VARCHAR(20)  NOT NULL,
    week       INTEGER      NOT NULL
);

-- Dimension: Location
CREATE TABLE dim_location (
    location_id        INTEGER PRIMARY KEY,
    location_name      VARCHAR(50)  NOT NULL,
    region             VARCHAR(50)  NOT NULL,
    is_capital_region  BOOLEAN      NOT NULL DEFAULT FALSE
);

-- Fact: Job Skills (one row per job × skill)
CREATE TABLE fact_job_skills (
    id          SERIAL PRIMARY KEY,
    job_id      VARCHAR(20)  NOT NULL,
    skill_id    INTEGER      REFERENCES dim_skill(skill_id),
    company_id  INTEGER      REFERENCES dim_company(company_id),
    time_id     INTEGER      REFERENCES dim_time(time_id),
    location_id INTEGER      REFERENCES dim_location(location_id),
    seniority   VARCHAR(10)  NOT NULL,   -- Junior / Mid / Senior
    title       VARCHAR(200)
);

-- Indexes
CREATE INDEX idx_fact_skill    ON fact_job_skills(skill_id);
CREATE INDEX idx_fact_company  ON fact_job_skills(company_id);
CREATE INDEX idx_fact_time     ON fact_job_skills(time_id);
CREATE INDEX idx_fact_location ON fact_job_skills(location_id);
CREATE INDEX idx_fact_seniority ON fact_job_skills(seniority);

-- ============================================================
-- Key analytical queries
-- ============================================================

-- Top 15 skills overall
SELECT
    s.skill_name,
    s.category,
    COUNT(DISTINCT f.job_id) AS job_count,
    ROUND(COUNT(DISTINCT f.job_id) * 100.0 /
          (SELECT COUNT(DISTINCT job_id) FROM fact_job_skills), 1) AS pct_of_jobs
FROM fact_job_skills f
JOIN dim_skill s ON f.skill_id = s.skill_id
GROUP BY s.skill_name, s.category
ORDER BY job_count DESC
LIMIT 15;

-- Skill demand trend by month (last 12 months)
SELECT
    t.year,
    t.month,
    t.month_name,
    s.skill_name,
    COUNT(DISTINCT f.job_id) AS job_count
FROM fact_job_skills f
JOIN dim_time  t ON f.time_id  = t.time_id
JOIN dim_skill s ON f.skill_id = s.skill_id
WHERE s.skill_name IN ('SQL', 'Python', 'Power BI', 'Azure', 'DBT', 'Microsoft Fabric')
GROUP BY t.year, t.month, t.month_name, s.skill_name
ORDER BY t.year, t.month;

-- Skills by seniority
SELECT
    f.seniority,
    s.skill_name,
    COUNT(DISTINCT f.job_id) AS job_count
FROM fact_job_skills f
JOIN dim_skill s ON f.skill_id = s.skill_id
GROUP BY f.seniority, s.skill_name
ORDER BY f.seniority, job_count DESC;

-- Top hiring companies
SELECT
    c.company_name,
    COUNT(DISTINCT f.job_id) AS job_count
FROM fact_job_skills f
JOIN dim_company c ON f.company_id = c.company_id
GROUP BY c.company_name
ORDER BY job_count DESC
LIMIT 15;

-- Helsinki vs Rest of Finland
SELECT
    CASE WHEN l.is_capital_region THEN 'Capital Region'
         WHEN l.location_name = 'Remote' THEN 'Remote'
         ELSE 'Rest of Finland'
    END AS area,
    COUNT(DISTINCT f.job_id) AS job_count
FROM fact_job_skills f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY 1
ORDER BY job_count DESC;
