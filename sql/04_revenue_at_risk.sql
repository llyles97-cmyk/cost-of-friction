-- ============================================================
-- The Cost of Friction: Financial Services CX Analytics
-- Query 4: Revenue at Risk Model
-- ============================================================
-- revenue_at_risk = unresolved_complaints
--                × estimated_churn_rate
--                × avg_customer_ltv
--
-- Churn rates by category (industry benchmark):
--   Checking/Savings disputes:     35% estimated churn
--   Credit card billing:           28% estimated churn
--   Mortgage/Loan servicing:       22% estimated churn
--   Credit reporting:              18% estimated churn
--   Debt collection:               30% estimated churn
--   Other/General:                 20% estimated churn
--
-- LTV assumption: $1,850 (midpoint of $1,500–$2,200 range)
-- Sources: J.D. Power, KPMG, FDIC — see data/dataset_citations.md
-- ============================================================


WITH category_mapping AS (
    SELECT
        product,
        COUNT(*) AS total_complaints,
        SUM(CASE WHEN company_response != 'Closed with relief' THEN 1 ELSE 0 END) AS unresolved_complaints,
        SUM(CASE WHEN timely_response = 'No'
                 AND company_response != 'Closed with relief'
                 THEN 1 ELSE 0 END) AS high_risk_complaints,
        CASE
            WHEN product LIKE '%Checking%' OR product LIKE '%Savings%'
                THEN 0.35
            WHEN product LIKE '%Credit card%'
                THEN 0.28
            WHEN product LIKE '%Mortgage%' OR product LIKE '%loan%'
                THEN 0.22
            WHEN product LIKE '%Credit reporting%' OR product LIKE '%credit repair%'
                THEN 0.18
            WHEN product LIKE '%Debt collection%'
                THEN 0.30
            ELSE 0.20
        END AS estimated_churn_rate,
        1850 AS avg_ltv
    FROM complaints
    GROUP BY product
),
revenue_model AS (
    SELECT
        product,
        total_complaints,
        unresolved_complaints,
        high_risk_complaints,
        estimated_churn_rate,
        avg_ltv,
        ROUND(unresolved_complaints * estimated_churn_rate * avg_ltv, 0)
            AS base_revenue_at_risk,
        ROUND(high_risk_complaints * (estimated_churn_rate * 2.0) * avg_ltv, 0)
            AS high_risk_revenue_at_risk
    FROM category_mapping
)
SELECT
    product,
    total_complaints,
    unresolved_complaints,
    high_risk_complaints,
    ROUND(estimated_churn_rate * 100, 0) AS churn_rate_pct,
    avg_ltv,
    base_revenue_at_risk,
    high_risk_revenue_at_risk,
    base_revenue_at_risk + high_risk_revenue_at_risk AS total_revenue_at_risk
FROM revenue_model
ORDER BY total_revenue_at_risk DESC;


-- ============================================================
-- SUMMARY: Total estimated revenue at risk across all categories
-- ============================================================
WITH category_mapping AS (
    SELECT
        product,
        SUM(CASE WHEN company_response != 'Closed with relief' THEN 1 ELSE 0 END) AS unresolved,
        SUM(CASE WHEN timely_response = 'No'
                 AND company_response != 'Closed with relief'
                 THEN 1 ELSE 0 END) AS high_risk,
        CASE
            WHEN product LIKE '%Checking%' OR product LIKE '%Savings%' THEN 0.35
            WHEN product LIKE '%Credit card%' THEN 0.28
            WHEN product LIKE '%Mortgage%' OR product LIKE '%loan%' THEN 0.22
            WHEN product LIKE '%Credit reporting%' THEN 0.18
            WHEN product LIKE '%Debt collection%' THEN 0.30
            ELSE 0.20
        END AS churn_rate
    FROM complaints
    GROUP BY product
)
SELECT
    SUM(unresolved) AS total_unresolved_complaints,
    SUM(high_risk) AS total_high_risk_complaints,
    ROUND(SUM(unresolved * churn_rate * 1850), 0) AS total_base_revenue_at_risk,
    ROUND(SUM(high_risk * churn_rate * 2.0 * 1850), 0) AS total_high_risk_revenue_at_risk,
    ROUND(SUM(unresolved * churn_rate * 1850) +
          SUM(high_risk * churn_rate * 2.0 * 1850), 0) AS grand_total_revenue_at_risk
FROM category_mapping;
