# 📊 Customer Churn Prediction — Python, SQL & Power BI

An end-to-end predictive analytics project that identifies telecom customers likely to
**churn** (cancel their service), quantifies the **revenue at risk**, and delivers the
results through an interactive **Power BI dashboard**.

---

## 🎯 Project Overview

| | |
|---|---|
| **Goal** | Predict which customers will churn so the business can retain them proactively |
| **Dataset** | Telco Customer Churn — 7,043 customers, 21 columns |
| **Tools** | Python (pandas, scikit-learn), SQL, Power BI, Jupyter |
| **Output** | Customer-level churn probabilities + risk levels + 3-page dashboard |
| **Headline result** | Model catches **~79% of real churners**; ~**$110K/month** revenue identified at risk |

## 💼 Business Problem

Telecom companies lose ~26% of customers per year. Acquiring a new customer costs
**5–7x more** than retaining an existing one. If we can predict *who* is about to leave
and *why*, a targeted retention offer (discount, contract upgrade, service call) can save
significant revenue. This project answers three questions:

1. **Who** is likely to churn? (machine learning predictions)
2. **Why** do customers churn? (feature importance + EDA)
3. **How much** revenue is at risk? (business analysis + dashboard)

## 📁 Dataset Description

`data/raw/telco_customer_churn.csv` — one row per customer:

| Category | Columns |
|---|---|
| Identity | customerID, gender, SeniorCitizen, Partner, Dependents |
| Account | tenure, Contract, PaperlessBilling, PaymentMethod |
| Services | PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies |
| Billing | MonthlyCharges, TotalCharges |
| Target | **Churn** (Yes / No) — 26.5% churned |

## 🔄 Project Workflow

```
Raw CSV ──► Python cleaning ──► Cleaned CSV ──► ML models (3) ──► Best model
                                    │                                  │
                                    ▼                                  ▼
                              SQL analysis                  Predictions + risk levels
                                                                       │
                                                                       ▼
                                                            Power BI dashboard (3 pages)
```

## 🗂️ Folder Structure

```
Customer_Churn_Project/
├── data/
│   ├── raw/                    # original dataset
│   ├── processed/              # cleaned dataset (script output)
│   └── powerbi/                # Power BI-ready predictions (script output)
├── notebooks/
│   └── customer_churn_model.ipynb   # full workflow with charts & explanations
├── scripts/
│   ├── data_cleaning.py        # step 1: clean + feature engineering
│   ├── churn_model.py          # step 2: train & compare 3 models
│   └── generate_predictions.py # step 3: score all customers + insights
├── sql/
│   ├── create_tables.sql
│   ├── exploratory_analysis.sql
│   └── churn_business_queries.sql
├── powerbi/
│   ├── dashboard_build_guide.md    # step-by-step build instructions
│   ├── dax_measures.txt            # all DAX formulas
│   └── dashboard_wireframe.md      # page layouts
├── outputs/                    # model, predictions, metrics (script output)
├── README.md
├── requirements.txt
└── project_summary.md
```

## 🚀 How to Run the Project

### 1. Python setup (Windows)

```bash
# From the project root folder:
pip install -r requirements.txt

# Run the pipeline in order:
python scripts/data_cleaning.py
python scripts/churn_model.py
python scripts/generate_predictions.py
```

Or open the notebook for the guided version with charts:

```bash
jupyter notebook notebooks/customer_churn_model.ipynb
```

### 2. SQL analysis

Works with SQLite (zero install), PostgreSQL, MySQL, or BigQuery.
Quick start with SQLite:

```bash
sqlite3 churn.db
.mode csv
.import --skip 1 data/processed/cleaned_customer_churn.csv customer_churn
.import --skip 1 outputs/churn_predictions.csv churn_predictions
.read sql/exploratory_analysis.sql
.read sql/churn_business_queries.sql
```

(Alternatively, use a GUI like **DB Browser for SQLite** — create the tables with
`sql/create_tables.sql`, import both CSVs, and run the queries.)

### 3. Power BI dashboard

1. Open Power BI Desktop → Get data → Text/CSV → `data/powerbi/churn_predictions_powerbi.csv`
2. Create the measures from `powerbi/dax_measures.txt`
3. Follow `powerbi/dashboard_build_guide.md` to build the 3 pages:
   **Executive Overview · Customer Risk Analysis · Business Insights**

## 🤖 Machine Learning Models

Three models compared, all with `class_weight="balanced"` to handle the 26.5% / 73.5%
class imbalance, evaluated on a stratified 20% hold-out test set:

| Model | Accuracy | Precision (Churn) | Recall (Churn) | F1 (Churn) |
|---|---|---|---|---|
| Logistic Regression | 73.8% | 0.50 | 0.78 | 0.61 |
| **Decision Tree (selected)** | 74.0% | 0.51 | **0.79** | 0.62 |
| Random Forest | 77.0% | 0.55 | 0.71 | 0.62 |

**Why recall over accuracy?** Missing a real churner (false negative) means losing
~$65–100/month plus reacquisition costs. Flagging a loyal customer by mistake (false
positive) only costs a small retention offer. So the model was selected for the
**highest recall on the churn class** — it catches ~79% of customers who actually churn.

## 🔍 Key Insights

1. **Contract type is the #1 churn driver** — month-to-month customers churn at **42.7%**
   vs 11.3% (one-year) and 2.8% (two-year).
2. **New customers churn most** — 47.4% churn in the first 12 months, dropping to 9.5%
   after 4 years.
3. **Fiber optic customers churn at 41.9%** — more than double DSL (19.0%).
4. **Electronic check payers churn at 45.3%** — the highest of any payment method.
5. **~$110K/month of revenue is at risk** from active customers the model predicts will churn.

## 💡 Business Recommendations

1. **Contract-upgrade campaign:** discount offers to move month-to-month customers to
   1–2 year contracts.
2. **90-day onboarding program:** welcome calls, setup help, and first-bill review for
   new customers.
3. **Proactive retention outreach:** give the model's High-risk list to the retention team.
4. **Fiber optic review:** investigate pricing and service quality behind its churn rate.
5. **Payment friction:** nudge electronic-check payers toward auto-pay.

## 🔮 Future Improvements

- Hyperparameter tuning (GridSearchCV) and gradient boosting (XGBoost/LightGBM)
- SHAP values for per-customer explanation ("this customer is risky *because*…")
- Retrain monthly on fresh data; track model drift
- Cost-based threshold tuning (optimize the retention budget, not just recall)
- Deploy as an API so the CRM can score customers in real time
---

*Dataset: IBM Telco Customer Churn (public sample dataset). Built for portfolio and
educational purposes.*
