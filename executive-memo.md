# Executive Memo

**TO:** VP of Customer Experience / Chief Operating Officer
**FROM:** CX Analytics
**RE:** Estimated Revenue at Risk from Customer Friction — Financial Services Complaint Analysis
**DATE:** Q2 2024
**CLASSIFICATION:** Internal Strategy

---

## Bottom Line

An analysis of 100,000+ consumer financial complaints filed with the CFPB identifies **an estimated $37.6 million in revenue at risk** from unresolved customer friction across nine product categories. Three categories account for 66% of that exposure. Two of them — Credit Reporting and Debt Collection — are currently operating with unresolved complaint rates above 88%, meaning fewer than 1 in 8 complaints in these categories results in meaningful relief for the customer.

The complaint is not the cost. The complaint is the signal. What it signals is churn probability — and churn in financial services, at an average customer LTV of $1,850 over five years, has a calculable price.

---

## The Revenue at Risk Model

```
revenue_at_risk = unresolved_complaints × estimated_churn_rate × avg_customer_LTV
```

**Model assumptions:**
- Average customer LTV: $1,850 (midpoint of FDIC/industry $1,500–$2,200 range)
- Churn rates by category: sourced from J.D. Power Retail Banking Satisfaction Study and KPMG CX research
- High-risk multiplier: 2.0x applied to complaints that are both untimely AND unresolved (industry benchmark: 1.8–2.2x)

All estimates are directional. They should be validated against institution-specific LTV and churn data before operational use.

---

## Priority Findings

### 1. Credit Reporting — $13.4M at Risk | Friction Score: 50.9 (Critical)

Credit reporting complaints represent the single largest share of complaint volume — approximately 43% of all CFPB complaints in this analysis. The unresolved rate is **91.9%**, the highest of any category. The complaint-to-relief rate is effectively 1 in 12.

The volume alone makes this category the largest revenue exposure in the portfolio, even though credit reporting carries a lower per-complaint churn rate (18%) than higher-intent product categories like checking accounts. At scale, volume wins.

**Key driver:** "Incorrect information on credit report" is the dominant issue. These complaints are frequently closed with explanation — technically resolved, meaningfully not.

---

### 2. Debt Collection — $7.1M at Risk | Friction Score: 38.9 (Critical)

Debt collection complaints carry the highest consumer dispute rate of any category — meaning consumers are not just filing complaints, they are actively rejecting the company's resolution. An 88% unresolved rate combined with a 30% estimated churn probability produces the second-highest revenue exposure in the analysis.

**Key driver:** "Debt not owed" and "communication tactics" dominate. These complaints are structural — they reflect systemic issues in third-party debt management, not isolated service failures.

**Secondary risk:** Debt collection complaints carry regulatory exposure beyond direct churn. CFPB supervisory attention to this category is documented and ongoing.

---

### 3. Checking / Savings — $4.7M at Risk | Friction Score: 32.0 (High)

Checking and savings account complaints carry the **highest estimated churn rate** of any category (35%) and the highest untimely response rate (4.5%). Customers who file complaints about unauthorized transactions, account freezes, or fee disputes — and receive a late, unhelpful response — are the highest-probability churners in the portfolio.

This category punches above its weight. At 9% of complaint volume, it accounts for 12.4% of total estimated revenue at risk. The per-complaint cost here is the highest of any category.

**Key driver:** Unauthorized transactions and account management disputes. These are high-urgency, high-emotion complaints where response speed matters most — and where untimely response compounds friction most severely.

---

## The Untimely Response Problem

Across all categories, complaints that receive an untimely response and are closed without relief carry a **2x churn multiplier** relative to baseline. These are not just dissatisfied customers — they are customers who were ignored and then not helped.

The untimely + unresolved combination is concentrated in:
- Money Transfer (6.4% untimely rate)
- Checking / Savings (4.5%)
- Payday / Personal Loan (4.0%)

These categories are smaller in volume but represent the highest per-complaint revenue risk.

---

## Three Recommendations, Ranked by ROI

### Recommendation 1 — Triage High-Risk Complaints at Intake
**Estimated impact:** $4–8M reduction in at-risk revenue
**Investment required:** Complaint routing logic (low technical complexity)

Flag complaints that match high-risk criteria at intake: product category (Checking/Savings, Debt Collection) + submission channel + issue type. Route these to dedicated resolution teams with a 24-hour response SLA rather than standard queue. The 2x churn multiplier for untimely + unresolved complaints means that faster response on the highest-risk complaints produces disproportionate retention value.

---

### Recommendation 2 — Redefine "Resolved" for Credit Reporting
**Estimated impact:** $3–6M reduction in at-risk revenue
**Investment required:** Policy and process change (medium complexity)

The credit reporting category has a 91.9% "unresolved" rate under the current model because "closed with explanation" is counted as unresolved — and by the consumer's behavior, it should be. Customers who receive an explanation but no action on their credit report are not retained customers. Shifting even 10% of credit reporting complaints from explanation-only to actionable relief — through dispute facilitation, bureau liaison support, or enhanced self-service — would reduce estimated revenue at risk in this category by $1.3M.

---

### Recommendation 3 — Build a Friction Dashboard for Monthly Leadership Review
**Estimated impact:** Structural — enables ongoing prioritization
**Investment required:** Analytics infrastructure (medium complexity)

The current state: complaint volume is tracked. Resolution rates are tracked. Revenue at risk is not tracked. This memo is a one-time calculation. The friction score model built in this analysis is designed to be run monthly, updated with new complaint data, and presented to CX leadership as a leading indicator of churn — not a lagging indicator of satisfaction.

A monthly dashboard showing friction score by category, untimely response rate, and estimated revenue at risk gives the CX function a business-language metric that connects directly to revenue. That connection is what justifies investment in complaint resolution infrastructure.

---

## Caveats and Limitations

- Revenue at risk estimates use industry-average LTV and churn benchmarks, not institution-specific data. Actual figures will vary.
- CFPB complaint data is self-reported and not a statistical sample of all customer experiences.
- Churn probability estimates assume a direct relationship between complaint type and churn intent, which is supported by J.D. Power and KPMG research but not causally proven.
- This analysis covers complaint volume and resolution patterns — it does not capture complaints that were never filed (the dark matter of customer friction).

---

## Methodology

Full analysis, SQL queries, and Python pipeline available at:
**github.com/llyles97-cmyk/cost-of-friction**

Data: CFPB Consumer Complaint Database (100,000+ records)
Tools: SQL (SQLite), Python (pandas, matplotlib)
Churn benchmarks: J.D. Power U.S. Retail Banking Satisfaction Study (2023), KPMG CX in Financial Services
LTV benchmark: FDIC 2023 National Survey + industry analyst consensus

---

*This memo is a portfolio research document built to demonstrate applied CX analytics methodology. It does not represent findings from any specific financial institution.*
