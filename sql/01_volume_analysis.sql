-- ============================================================
-- The Cost of Friction: Financial Services CX Analytics
-- Query 1: Volume Analysis — Complaint Distribution
-- Dataset: CFPB Consumer Complaint Database
-- ============================================================


-- ============================================================
-- SCHEMA REFERENCE
-- ============================================================
-- date_received              TEXT    Complaint submission date
-- product                    TEXT    Financial product category
-- sub_product                TEXT    Product subcategory
-- issue                      TEXT    Primary complaint issue
-- sub_issue                  TEXT    Secondary issue detail
-- company                    TEXT    Financial institution
-- state                      TEXT    Consumer state
-- submitted_via              TEXT    Submission channel
-- company_response           TEXT    Resolution type
-- timely_response            TEXT    Yes / No
-- consumer_disputed          TEXT    Yes / No / N/A
-- ============================================================


-- ============================================================
-- QUERY 1: Total complaint volume by product category
-- ============================================================
SELECT
    product,
    COUNT(*) AS total_complaints,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM complaints
GROUP BY product
ORDER BY total_complaints DESC;


-- ============================================================
-- QUERY 2: Top issues within each product category
-- ============================================================
WITH ranked_issues AS (
    SELECT
        product,
        issue,
        COUNT(*) AS complaint_count,
        ROW_NUMBER() OVER (
            PARTITION BY product
            ORDER BY COUNT(*) DESC
        ) AS rank
    FROM complaints
    GROUP BY product, issue
)
SELECT
    product,
    issue,
    complaint_count
FROM ranked_issues
WHERE rank <= 3
ORDER BY product, rank;


-- ============================================================
-- QUERY 3: Complaint volume trend by year
-- ============================================================
SELECT
    SUBSTR(date_received, 1, 4) AS complaint_year,
    COUNT(*) AS total_complaints,
    ROUND(
        100.0 * (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY SUBSTR(date_received, 1, 4))) /
        NULLIF(LAG(COUNT(*)) OVER (ORDER BY SUBSTR(date_received, 1, 4)), 0),
        1
    ) AS yoy_growth_pct
FROM complaints
GROUP BY complaint_year
ORDER BY complaint_year;


-- ============================================================
-- QUERY 4: Submission channel distribution
-- Which channels generate the most complaints?
-- ============================================================
SELECT
    submitted_via,
    COUNT(*) AS total_complaints,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM complaints
GROUP BY submitted_via
ORDER BY total_complaints DESC;


-- ============================================================
-- QUERY 5: Top 10 companies by complaint volume
-- ============================================================
SELECT
    company,
    COUNT(*) AS total_complaints,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS market_share_of_complaints
FROM complaints
GROUP BY company
ORDER BY total_complaints DESC
LIMIT 10;
