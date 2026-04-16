-- ============================================================
-- The Cost of Friction: Financial Services CX Analytics
-- Query 3: Friction Score by Product Category
-- ============================================================
-- friction_score = (complaint_volume_share × 0.4)
--               + (unresolved_rate × 0.35)
--               + (untimely_rate × 0.15)
--               + (dispute_rate × 0.10)
--
-- Weights reflect relative contribution to churn probability:
-- Volume share: directional signal of systemic issue
-- Unresolved rate: strongest predictor of churn intent
-- Untimely rate: amplifier of frustration and churn probability
-- Dispute rate: consumer rejection of resolution
-- ============================================================


WITH base_metrics AS (
    SELECT
        product,
        COUNT(*) AS total_complaints,
        ROUND(
            100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
            4
        ) AS volume_share,
        ROUND(
            100.0 * SUM(CASE WHEN company_response != 'Closed with relief' THEN 1 ELSE 0 END) /
            COUNT(*),
            4
        ) AS unresolved_rate,
        ROUND(
            100.0 * SUM(CASE WHEN timely_response = 'No' THEN 1 ELSE 0 END) /
            COUNT(*),
            4
        ) AS untimely_rate,
        ROUND(
            100.0 * SUM(CASE WHEN consumer_disputed = 'Yes' THEN 1 ELSE 0 END) /
            NULLIF(SUM(CASE WHEN consumer_disputed IN ('Yes','No') THEN 1 ELSE 0 END), 0),
            4
        ) AS dispute_rate
    FROM complaints
    GROUP BY product
),
friction_scored AS (
    SELECT
        product,
        total_complaints,
        volume_share,
        unresolved_rate,
        untimely_rate,
        dispute_rate,
        ROUND(
            (volume_share * 0.40) +
            (unresolved_rate * 0.35) +
            (untimely_rate * 0.15) +
            (COALESCE(dispute_rate, 0) * 0.10),
            2
        ) AS friction_score
    FROM base_metrics
)
SELECT
    product,
    total_complaints,
    volume_share,
    unresolved_rate,
    untimely_rate,
    dispute_rate,
    friction_score,
    CASE
        WHEN friction_score >= 35 THEN 'Critical'
        WHEN friction_score >= 25 THEN 'High'
        WHEN friction_score >= 15 THEN 'Medium'
        ELSE 'Low'
    END AS friction_tier
FROM friction_scored
ORDER BY friction_score DESC;
