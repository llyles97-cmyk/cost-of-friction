-- ============================================================
-- The Cost of Friction: Financial Services CX Analytics
-- Query 2: Resolution Analysis — Timely Response + Relief Rates
-- Dataset: CFPB Consumer Complaint Database
-- ============================================================


-- ============================================================
-- QUERY 1: Resolution type distribution overall
-- ============================================================
SELECT
    company_response,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM complaints
GROUP BY company_response
ORDER BY total DESC;


-- ============================================================
-- QUERY 2: Resolution rate by product category
-- "Closed with relief" = meaningful resolution
-- "Closed with explanation" = acknowledged but not resolved
-- ============================================================
SELECT
    product,
    COUNT(*) AS total_complaints,
    SUM(CASE WHEN company_response = 'Closed with relief' THEN 1 ELSE 0 END) AS resolved_with_relief,
    SUM(CASE WHEN company_response LIKE 'Closed with%' AND company_response != 'Closed with relief'
        THEN 1 ELSE 0 END) AS closed_no_relief,
    ROUND(
        100.0 * SUM(CASE WHEN company_response = 'Closed with relief' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS relief_rate_pct,
    ROUND(
        100.0 * SUM(CASE WHEN company_response != 'Closed with relief' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS unresolved_rate_pct
FROM complaints
GROUP BY product
ORDER BY unresolved_rate_pct DESC;


-- ============================================================
-- QUERY 3: Timely response rate by product
-- Late response compounds friction and churn risk
-- ============================================================
SELECT
    product,
    COUNT(*) AS total_complaints,
    SUM(CASE WHEN timely_response = 'Yes' THEN 1 ELSE 0 END) AS timely,
    SUM(CASE WHEN timely_response = 'No' THEN 1 ELSE 0 END) AS untimely,
    ROUND(
        100.0 * SUM(CASE WHEN timely_response = 'No' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS untimely_rate_pct
FROM complaints
GROUP BY product
ORDER BY untimely_rate_pct DESC;


-- ============================================================
-- QUERY 4: Consumer dispute rate by product
-- High dispute rate = consumer rejected company's resolution
-- ============================================================
SELECT
    product,
    COUNT(*) AS total_complaints,
    SUM(CASE WHEN consumer_disputed = 'Yes' THEN 1 ELSE 0 END) AS disputed,
    ROUND(
        100.0 * SUM(CASE WHEN consumer_disputed = 'Yes' THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN consumer_disputed IN ('Yes', 'No') THEN 1 ELSE 0 END), 0),
        2
    ) AS dispute_rate_pct
FROM complaints
GROUP BY product
ORDER BY dispute_rate_pct DESC;


-- ============================================================
-- QUERY 5: Untimely response + unresolved combination
-- The highest-risk complaints: late AND no meaningful relief
-- ============================================================
SELECT
    product,
    COUNT(*) AS total_complaints,
    SUM(CASE
        WHEN timely_response = 'No'
        AND company_response != 'Closed with relief'
        THEN 1 ELSE 0 END) AS high_risk_complaints,
    ROUND(
        100.0 * SUM(CASE
            WHEN timely_response = 'No'
            AND company_response != 'Closed with relief'
            THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS high_risk_rate_pct
FROM complaints
GROUP BY product
ORDER BY high_risk_rate_pct DESC;
