# Dashboard User Guide — Customer Churn Analytics

*A guide for business users. No data science background needed.*

---

## What this dashboard is for

This dashboard shows **which customers are likely to cancel their telecom
service, why, and what it costs the business** — before they actually leave.
It is powered by a machine learning model that scores all 7,043 customers
with a churn probability from 0% to 100%.

## Who should use it

| User | Go-to page |
|---|---|
| Executives / leadership | **Overview** — the health check |
| Retention / customer-care team | **Risk Center** — the daily call list |
| Analysts / strategy | **Churn Drivers** — the "why" |
| Program owners / planning | **Retention Strategy** — the action plan |

---

## How to use each page

### Page 1 — Executive Overview
The 60-second health check. Six numbers across the top tell the whole story:
how many customers we have, how many we're losing (26.5%), how many the model
expects to lose, and what that's worth (**$110K/month, $1.32M/year at risk**).
The charts below show *where* churn concentrates: contract type and payment
method. Use the slicers (top-right) to re-ask every question for a segment —
e.g. select "Fiber optic" to see churn for fiber customers only.

### Page 2 — Customer Risk Center
**This page is a prioritized retention call list.** The big table ranks
still-active customers by churn probability — the customer at the top is the
one most likely to cancel next. Work from the top down. The scatter chart on
the right shows the danger zone: customers who are **new (left side) and
expensive (top)** — that top-left cluster is where retention effort pays
most. The table already excludes customers who have left.

### Page 3 — Churn Drivers & Segments
Explains **why** customers leave. The top-left chart is the machine learning
model's ranking of churn drivers — month-to-month contracts dominate,
followed by short tenure and fiber optic service. The heatmap shows the
riskiest combination: **month-to-month + fiber optic = 54.6% churn**, the
single worst segment in the business.

### Page 4 — Retention Strategy
Turns the analysis into an action plan: five prioritized plays, each with the
problem, the recommended action, and the expected impact. The two charts show
where the at-risk money sits (mostly month-to-month contracts: $92K of the
$110K) and which value segments the high-risk customers belong to.

---

## KPI dictionary (also used as visual tooltips)

| Metric | Suggested tooltip text |
|---|---|
| **Churn Rate** | "The percentage of customers who cancelled their service. 26.5% overall — every point of churn ≈ 70 customers and ≈ $4.5K of monthly revenue." |
| **Revenue at Risk** | "The combined monthly bills of active customers our model predicts will churn. This is revenue we still have and can protect with retention action — currently ≈ $110K/month." |
| **High Risk Customers** | "Customers with a 60%+ modeled probability of churning. The 'Active' version excludes customers who already left — those are the ones worth calling." |
| **Churn Probability** | "The model's estimate (0–100%) that this specific customer will cancel, based on their contract, tenure, services, and billing profile. 90% means: of 100 similar customers, ~90 churned." |
| **Feature Importance** | "How strongly each customer attribute influenced the model's predictions. Longer bar = bigger churn driver. This is why the recommendations target contracts, onboarding, and payment methods." |
| **Model Accuracy** | "How often the model's churn prediction matched what really happened (~75%). We deliberately tuned the model to over-warn rather than miss churners — catching ~4 out of 5 real churners." |

## How to filter

- **Slicers (top-right dropdowns):** pick a Contract, Internet Service, Risk
  Level, or Tenure Group — every number and chart on the page recalculates.
- **Click any bar or chart segment:** the rest of the page cross-highlights
  to that selection. Click it again to deselect.
- **Right-click a contract bar → Drill through → Segment detail** (if built):
  opens a focused page for just that segment. Use the back arrow to return.
- **Reset:** clear each slicer, or use the "All Customers" bookmark.

## How to read churn probability and act on it

| Risk level | Probability | What to do |
|---|---|---|
| **High** (red) | ≥ 60% | Personal outreach this week — call, tailored offer |
| **Medium** (amber) | 30–59% | Automated retention: email offer, contract-upgrade promo |
| **Low** (green) | < 30% | No action — don't spend retention budget here |

A probability is **not a certainty** — it's a ranking tool. Its job is to make
sure the retention team spends its limited time on the right 1,050 customers
instead of all 5,174.

## Common business questions this dashboard answers

| Question | Where to look |
|---|---|
| Which customers should we contact first? | Page 2 table, top rows |
| Which contract type churns most? | Page 1 — Month-to-month, 42.7% |
| Which payment method is linked to churn? | Page 1 — Electronic check, 45.3% |
| How much monthly revenue is at risk? | Page 1 KPI — $110,234 |
| Which segment should get contract-upgrade discounts? | Page 4 — month-to-month holds $92K of the at-risk revenue |
| Are new customers more likely to churn? | Page 3 tenure chart — 47.4% churn in months 0–12 vs 9.5% after 4 years |
| What's our riskiest customer profile? | Page 3 heatmap — month-to-month + fiber optic (54.6%) |
| Is the model trustworthy? | ~75% accuracy, catches ~4 of 5 churners (Page 4 note) |

## Business impact (why this matters)

Without a model, retention teams find out about churn **after** the
cancellation call. With this dashboard, they get a ranked list of 1,050
at-risk active customers **before** they leave. If outreach saves just
**1 in 4** of them, the company protects roughly **$28K of monthly revenue —
about $330K per year** — from one modeling project and a dashboard refresh.
