# Data Sources

## Primary Dataset

**CFPB Consumer Complaint Database**
- Source: Kaggle — kaggle.com/datasets/kaggle/us-consumer-finance-complaints
- Original publisher: Consumer Financial Protection Bureau (CFPB) — consumerfinance.gov
- License: U.S. Government Work (public domain)
- Records analyzed: 100,000+
- Key columns:
  - `Date received` — submission date
  - `Product` — financial product category (e.g., Mortgage, Credit card, Checking account)
  - `Sub-product` — subcategory
  - `Issue` — primary complaint issue
  - `Sub-issue` — secondary issue detail
  - `Company` — financial institution named in complaint
  - `State` — consumer state
  - `Submitted via` — channel (Web, Phone, Referral, etc.)
  - `Company response to consumer` — resolution type (Closed with relief, Closed with explanation, etc.)
  - `Timely response` — Yes/No flag for response within regulatory window
  - `Consumer disputed` — whether consumer disputed the company's resolution

---

## Supporting Research — Revenue at Risk Model

**Customer Lifetime Value (LTV) Benchmarks**
- FDIC national survey data — average retail banking customer tenure and product holdings
- Industry standard LTV estimate: $1,500–$2,200 per retail banking customer over 5-year horizon
- Source: FDIC 2023 National Survey of Unbanked and Underbanked Households + industry analyst benchmarks

**Churn Probability by Complaint Category**
- J.D. Power U.S. Retail Banking Satisfaction Study (2023) — complaint-to-churn correlation by product type
- KPMG "Customer Experience in Financial Services" — unresolved complaint churn multiplier estimates
- Bain & Company "Customer Loyalty in Retail Banking" — NPS-to-churn relationship in financial services
- Industry consensus estimate: unresolved complaint churn rate 25–40% depending on product category

**Untimely Response Multiplier**
- Industry CX research consensus: untimely complaint response correlates with 1.8–2.2x baseline churn probability
- Sources: Forrester Research CX Index (Financial Services), CFPB supervisory research

---

## Methodology Notes

The revenue at risk model uses publicly available industry benchmarks rather than proprietary data. All dollar estimates are directional — intended to demonstrate the analytical approach and order of magnitude, not precise financial projections. Estimates should be validated against institution-specific LTV and churn data before use in operational decisions.

Complaint data from the CFPB is self-reported by consumers and not a statistical sample of all customer experiences. Findings reflect patterns in the complaint population, not the full customer base.
