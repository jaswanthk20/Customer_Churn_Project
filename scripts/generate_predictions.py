"""
============================================================
 STEP 3: GENERATE CUSTOMER-LEVEL PREDICTIONS
 Customer Churn Prediction Project
============================================================
 What this script does:
   1. Loads the cleaned dataset and the trained model (.pkl)
   2. Predicts churn + churn probability for EVERY customer
   3. Assigns a Risk_Level (High / Medium / Low)
   4. Exports:
        - outputs/churn_predictions.csv           (analysis copy)
        - data/powerbi/churn_predictions_powerbi.csv  (Power BI copy)
        - outputs/business_insights.txt           (plain-English findings)

 How to run (from the project root folder):
   python scripts/generate_predictions.py

 (Run data_cleaning.py and churn_model.py first.)
============================================================
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
MODEL_PATH = PROJECT_ROOT / "outputs" / "churn_prediction_model.pkl"
PREDICTIONS_PATH = PROJECT_ROOT / "outputs" / "churn_predictions.csv"
POWERBI_PATH = PROJECT_ROOT / "data" / "powerbi" / "churn_predictions_powerbi.csv"
INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "business_insights.txt"

# Same feature lists used in churn_model.py — the saved pipeline
# expects exactly these input columns.
NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
CATEGORICAL_FEATURES = [
    "gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod",
]


def assign_risk_level(probability):
    """
    Convert a churn probability into a simple label the business can act on.
      High   -> probability 60% or more  (call these customers first)
      Medium -> 30% to 59%               (send retention offers)
      Low    -> under 30%                (business as usual)
    """
    if probability >= 0.60:
        return "High"
    elif probability >= 0.30:
        return "Medium"
    else:
        return "Low"


def write_business_insights(preds):
    """Compute headline numbers and save them as a plain-text report."""
    total = len(preds)
    churned = (preds["Actual_Churn"] == "Yes").sum()
    churn_rate = churned / total * 100

    high_risk = preds[preds["Risk_Level"] == "High"]
    # Revenue at risk = monthly revenue from customers the model
    # flags as likely to churn (still active, predicted churn = Yes).
    at_risk = preds[(preds["Predicted_Churn"] == "Yes") & (preds["Actual_Churn"] == "No")]
    revenue_at_risk = at_risk["MonthlyCharges"].sum()

    def seg_rate(col, val):
        seg = preds[preds[col] == val]
        return (seg["Actual_Churn"] == "Yes").mean() * 100 if len(seg) else 0

    lines = [
        "============================================================",
        " CUSTOMER CHURN — BUSINESS INSIGHTS & RECOMMENDATIONS",
        "============================================================",
        "",
        "HEADLINE NUMBERS",
        f"- Total customers analyzed: {total:,}",
        f"- Customers who churned: {churned:,} ({churn_rate:.1f}%)",
        f"- Customers flagged HIGH risk by the model: {len(high_risk):,}",
        f"- Active customers predicted to churn: {len(at_risk):,}",
        f"- Estimated monthly revenue at risk: ${revenue_at_risk:,.0f}",
        "",
        "KEY INSIGHTS",
        f"1. CONTRACT TYPE is the #1 churn driver. Month-to-month customers "
        f"churn at {seg_rate('Contract', 'Month-to-month'):.1f}%, versus "
        f"{seg_rate('Contract', 'One year'):.1f}% (one-year) and "
        f"{seg_rate('Contract', 'Two year'):.1f}% (two-year).",
        f"2. NEW CUSTOMERS leave the most. Churn in the first 12 months is "
        f"{seg_rate('TenureGroup', '0-12 months'):.1f}%, falling to "
        f"{seg_rate('TenureGroup', '49-72 months'):.1f}% after 4 years.",
        f"3. FIBER OPTIC customers churn at "
        f"{seg_rate('InternetService', 'Fiber optic'):.1f}%, far above DSL at "
        f"{seg_rate('InternetService', 'DSL'):.1f}% — likely a price or "
        f"service-quality issue worth investigating.",
        f"4. ELECTRONIC CHECK payers churn at "
        f"{seg_rate('PaymentMethod', 'Electronic check'):.1f}%, the highest of "
        f"any payment method.",
        "5. HIGH MONTHLY CHARGES combined with a month-to-month contract is "
        "the highest-risk combination in the customer base.",
        "",
        "RECOMMENDATIONS",
        "1. Offer month-to-month customers a discount to move to 1- or 2-year "
        "contracts — contract length is the strongest retention lever.",
        "2. Build a 90-day onboarding program (welcome calls, setup help, "
        "first-bill review) — most churn happens early in the customer life.",
        "3. Give the High-risk list from this model to the retention team "
        "for proactive outreach with loyalty offers.",
        "4. Review fiber optic pricing and service quality — its churn rate "
        "is roughly double DSL's.",
        "5. Investigate the electronic-check experience (failed payments, "
        "manual effort) and nudge customers toward auto-pay methods.",
        "",
        "HOW TO USE THE MODEL OUTPUT",
        "- churn_predictions.csv lists every customer with a churn "
        "probability and a High/Medium/Low risk level.",
        "- Sort by Churn_Probability (descending) and filter "
        "Actual_Churn = 'No' to get the retention call list.",
        "============================================================",
    ]

    INSIGHTS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Business insights saved to: {INSIGHTS_PATH}")


def main():
    # ---------- 1. Load data and model ----------
    print("Loading cleaned data and trained model...")
    df = pd.read_csv(CLEAN_DATA_PATH)
    pipeline = joblib.load(MODEL_PATH)

    # ---------- 2. Predict for every customer ----------
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    churn_probability = pipeline.predict_proba(X)[:, 1]  # P(churn) per customer
    predicted = pipeline.predict(X)                      # 1 = churn, 0 = stay

    # ---------- 3. Build the output table for Power BI ----------
    preds = pd.DataFrame({
        "customerID": df["customerID"],
        "Actual_Churn": df["Churn"],
        "Predicted_Churn": np.where(predicted == 1, "Yes", "No"),
        "Churn_Probability": churn_probability.round(4),
        "Risk_Level": [assign_risk_level(p) for p in churn_probability],
        "Contract": df["Contract"],
        "PaymentMethod": df["PaymentMethod"],
        "InternetService": df["InternetService"],
        "tenure": df["tenure"],
        "MonthlyCharges": df["MonthlyCharges"],
        "TotalCharges": df["TotalCharges"],
        "TenureGroup": df["TenureGroup"],
        "MonthlyChargeGroup": df["MonthlyChargeGroup"],
        "CustomerValueSegment": df["CustomerValueSegment"],
    })

    # ---------- 4. Export both copies ----------
    PREDICTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    POWERBI_PATH.parent.mkdir(parents=True, exist_ok=True)
    preds.to_csv(PREDICTIONS_PATH, index=False)
    preds.to_csv(POWERBI_PATH, index=False)
    print(f"Predictions saved to: {PREDICTIONS_PATH}")
    print(f"Power BI copy saved to: {POWERBI_PATH}")

    # ---------- 5. Quick summary ----------
    print("\nRisk level breakdown:")
    print(preds["Risk_Level"].value_counts())
    print(f"\nAverage churn probability: {preds['Churn_Probability'].mean():.2%}")

    # ---------- 6. Business insights report ----------
    write_business_insights(preds)


if __name__ == "__main__":
    main()
