# Project Summary — Customer Churn Prediction
### Python | SQL | Power BI

*A plain-English explanation of the project and its findings.*

---

## 1. Business Problem

Telecom companies operate in a highly competitive market where customers can switch
providers easily. In our dataset, **26.5% of customers left the company** ("churned").
Every lost customer means lost monthly revenue plus the high cost of acquiring a
replacement — industry studies estimate acquiring a new customer costs **5–7 times more**
than keeping an existing one.

The problem: the company only finds out a customer is unhappy **after they leave**,
when it is too late to act.

## 2. Objective

Build a data-driven solution that:

1. **Predicts** which customers are likely to churn, before they leave
2. **Explains** the main reasons customers churn
3. **Quantifies** how much revenue is at risk
4. **Delivers** the results in a dashboard that business teams can actually use

## 3. Dataset

The Telco Customer Churn dataset: **7,043 customers and 21 columns**, covering:

- **Demographics** — gender, senior citizen status, partner, dependents
- **Account details** — tenure (months as a customer), contract type, billing, payment method
- **Services** — phone, internet type, security, backup, tech support, streaming
- **Billing** — monthly charges and total lifetime charges
- **Target** — `Churn`: did this customer leave? (Yes/No)

## 4. Data Cleaning

Real data is never perfect. Issues found and fixed:

- **`TotalCharges` stored as text** — 11 rows contained a blank space instead of a number.
  Investigation showed these were all brand-new customers (tenure = 0) who had not been
  billed yet, so the correct value was **0**, not a guess or a deleted row.
- **Verified no duplicates** — no repeated rows or customer IDs.
- **Kept `customerID`** in the data for reporting, but excluded it from model features
  (an ID contains no predictive information).
- Created new business-friendly columns: **TenureGroup**, **MonthlyChargeGroup**,
  **TotalChargeGroup**, **CustomerValueSegment**, and a numeric **ChurnFlag**.

## 5. Exploratory Data Analysis

Analysis in both Python (pandas + charts) and SQL revealed clear patterns:

| Question | Finding |
|---|---|
| Does contract type matter? | Month-to-month churn **42.7%** vs two-year **2.8%** |
| When do customers leave? | **47.4%** churn in the first 12 months; only 9.5% after 4 years |
| Does internet type matter? | Fiber optic **41.9%** vs DSL **19.0%** |
| Does payment method matter? | Electronic check **45.3%** — highest of all methods |
| Do charges matter? | Churners pay **~$74/month** on average vs ~$61 for loyal customers |
| Senior citizens? | Churn ~42% vs ~24% for non-seniors |

## 6. Predictive Modeling

Three classification models were trained and compared using a scikit-learn **Pipeline**
(preprocessing fitted only on training data — no data leakage):

- **Preprocessing:** One-hot encoding for categorical columns, standard scaling for
  numeric columns
- **Class imbalance:** handled with `class_weight="balanced"` since only 26.5% of
  customers churned
- **Split:** 80% training / 20% testing, stratified so both sets have the same churn rate

Models: **Logistic Regression**, **Decision Tree**, **Random Forest**.

## 7. Model Evaluation

Results on the held-out test set (1,409 customers):

| Model | Accuracy | Recall (Churn) | F1 (Churn) |
|---|---|---|---|
| Logistic Regression | 73.8% | 78.3% | 0.61 |
| **Decision Tree — selected** | 74.0% | **78.9%** | 0.62 |
| Random Forest | 77.0% | 70.9% | 0.62 |

**Why not pick the highest accuracy (Random Forest)?** Because the business cost of the
two possible mistakes is very different:

- **Missing a real churner** → lose the customer entirely (expensive)
- **False alarm on a loyal customer** → cost of one small retention offer (cheap)

So the model was chosen for the highest **recall on the churn class**: it correctly
identifies **~79% of customers who actually churn**. The model's feature importance
confirmed the EDA: **contract type, tenure, fiber optic internet, and monthly charges**
are the main churn drivers.

Every customer was then scored with a churn probability and grouped into
**High (≥60%) / Medium (30–59%) / Low (<30%)** risk levels.

## 8. Power BI Dashboard

A 4-page interactive dashboard built from the model's output file:

1. **Executive Overview** — KPI cards (total customers, churn rate, revenue at risk),
   churn split, and churn by contract and payment method, with slicers for filtering
2. **Customer Risk Center** — a ranked table of high-risk customers (the retention
   team's call list), churn probability distribution, and risk-level breakdown
3. **Churn Drivers & Segments** — churn by tenure and charge groups, the model's feature
   importance chart, and a contract-by-internet-service heatmap
4. **Retention Strategy** — a prioritized action plan mapping each at-risk segment to a
   recommended action and its expected business impact

The dashboard uses 28 DAX measures, including **Revenue at Risk** — the monthly revenue
of active customers the model predicts will churn: **~$110,000/month**.

## 9. Key Findings

1. **Contract type is the single strongest churn driver** — flexibility to leave means
   customers do leave.
2. **The first year is the danger zone** — nearly half of new customers churn within
   12 months.
3. **Premium services are churning** — fiber optic customers leave at twice the DSL rate,
   pointing to a price/value or service-quality problem.
4. **Payment friction correlates with churn** — electronic check users churn most;
   auto-pay users stay.
5. **~$110K of monthly revenue is savable** — these customers haven't left yet.

## 10. Business Recommendations

1. **Contract-upgrade campaign:** targeted discounts to convert month-to-month customers
   to 1- or 2-year contracts.
2. **90-day onboarding program:** welcome call, setup support, and a first-bill review
   to survive the high-risk early months.
3. **Proactive retention:** hand the model's High-risk customer list to the retention
   team for outreach with loyalty offers.
4. **Fiber optic review:** investigate whether pricing or reliability is driving premium
   customers away.
5. **Payment experience:** investigate electronic-check pain points and incentivize
   auto-pay enrollment.

## 11. Conclusion

This project demonstrates a complete analytics workflow: raw data → cleaning → exploration
→ machine learning → business-ready dashboard. The final model catches roughly **4 out of
5 customers who are about to churn**, and the analysis converts that prediction into
specific, prioritized retention actions worth an estimated **$110K in monthly revenue**.
The same pipeline could be retrained monthly and connected directly to a CRM, turning a
one-time analysis into an ongoing retention system.
