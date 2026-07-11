"""
============================================================
 STEP 2: MACHINE LEARNING MODEL TRAINING
 Customer Churn Prediction Project
============================================================
 What this script does:
   1. Loads the cleaned dataset from data/processed/
   2. Splits data into features (X) and target (y)
   3. Builds a preprocessing pipeline (encoding + scaling)
   4. Trains 3 models: Logistic Regression, Decision Tree, Random Forest
   5. Compares them with Accuracy, Precision, Recall, and F1-score
   6. Picks the best model for the BUSINESS goal (catching churners)
   7. Saves:
        - outputs/model_performance.csv
        - outputs/feature_importance.csv
        - outputs/churn_prediction_model.pkl

 How to run (from the project root folder):
   python scripts/churn_model.py

 IMPORTANT BUSINESS IDEA:
   For churn prediction, RECALL on the "churn" class matters most.
   Recall answers: "Of all customers who really churned,
   how many did the model catch?"
   Missing a churner (false negative) means losing a customer we
   could have saved. Contacting a loyal customer by mistake
   (false positive) only costs a small retention offer.
============================================================
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MODEL_PATH = OUTPUTS_DIR / "churn_prediction_model.pkl"
PERFORMANCE_PATH = OUTPUTS_DIR / "model_performance.csv"
IMPORTANCE_PATH = OUTPUTS_DIR / "feature_importance.csv"

RANDOM_STATE = 42  # fixed seed so results are reproducible

# ------------------------------------------------------------
# Columns used by the model
# ------------------------------------------------------------
# customerID is just a label -> NOT a feature.
# Churn / ChurnFlag are the answer -> NOT features (that would be leakage).
# The engineered "Group"/"Segment" columns are made FROM tenure and charges,
# so we leave them out of the model too (they would be duplicates) —
# they are for SQL analysis and Power BI.
NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
CATEGORICAL_FEATURES = [
    "gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod",
]
TARGET = "ChurnFlag"


def build_preprocessor():
    """
    Build the preprocessing step that runs INSIDE the pipeline.

    - StandardScaler: puts numeric columns on the same scale
      (helps Logistic Regression converge and compare coefficients).
    - OneHotEncoder: turns text categories into 0/1 columns
      (models cannot read text like "Month-to-month").

    Because preprocessing lives inside the Pipeline, it is fitted
    ONLY on training data — this prevents data leakage.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )


def get_models():
    """
    The three models we will compare.
    class_weight="balanced" tells the model to pay extra attention
    to the smaller class (churners are only ~27% of customers).
    """
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=6, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300, max_depth=10, class_weight="balanced",
            random_state=RANDOM_STATE, n_jobs=-1
        ),
    }


def evaluate_model(name, pipeline, X_test, y_test):
    """Print and return the key metrics for one trained model."""
    y_pred = pipeline.predict(X_test)

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        # pos_label=1 -> we measure precision/recall/F1 for the CHURN class
        "Precision (Churn)": precision_score(y_test, y_pred, pos_label=1),
        "Recall (Churn)": recall_score(y_test, y_pred, pos_label=1),
        "F1-Score (Churn)": f1_score(y_test, y_pred, pos_label=1),
    }

    print(f"\n----- {name} -----")
    for k, v in metrics.items():
        if k != "Model":
            print(f"{k}: {v:.4f}")

    print("\nConfusion Matrix (rows = actual, columns = predicted):")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Stayed", "Churned"]))

    return metrics


def extract_feature_importance(pipeline, model_name):
    """
    Get 'how much did each feature matter' from the final model.
      - Logistic Regression -> absolute value of coefficients
      - Tree models         -> built-in feature_importances_
    """
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    # OneHotEncoder created new column names like "Contract_Two year";
    # get_feature_names_out gives us the full expanded list.
    feature_names = preprocessor.get_feature_names_out()

    if hasattr(model, "feature_importances_"):        # tree-based models
        importance = model.feature_importances_
    else:                                             # logistic regression
        importance = np.abs(model.coef_[0])

    fi = pd.DataFrame({"Feature": feature_names, "Importance": importance})
    # Clean the "num__" / "cat__" prefixes so charts look nicer
    fi["Feature"] = fi["Feature"].str.replace("num__", "").str.replace("cat__", "")
    fi = fi.sort_values("Importance", ascending=False).reset_index(drop=True)
    fi["Model"] = model_name
    return fi


def main():
    # ---------- 1. Load cleaned data ----------
    print("Loading cleaned dataset...")
    df = pd.read_csv(CLEAN_DATA_PATH)
    print(f"Shape: {df.shape}")

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    # ---------- 2. Train / test split ----------
    # stratify=y keeps the same churn % in both sets — important
    # because churners are the minority class.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training rows: {len(X_train)} | Testing rows: {len(X_test)}")

    # ---------- 3. Train and evaluate all models ----------
    results = []
    trained = {}
    for name, model in get_models().items():
        pipeline = Pipeline(
            steps=[("preprocessor", build_preprocessor()), ("model", model)]
        )
        pipeline.fit(X_train, y_train)
        trained[name] = pipeline
        results.append(evaluate_model(name, pipeline, X_test, y_test))

    results_df = pd.DataFrame(results)
    print("\n========== MODEL COMPARISON ==========")
    print(results_df.round(4).to_string(index=False))

    # ---------- 4. Pick the best model FOR THE BUSINESS ----------
    # We choose the model with the highest RECALL on the churn class,
    # because missing a real churner is the most expensive mistake.
    # (F1 is the tie-breaker so we don't pick a model that flags everyone.)
    results_df = results_df.sort_values(
        ["Recall (Churn)", "F1-Score (Churn)"], ascending=False
    )
    best_name = results_df.iloc[0]["Model"]
    best_pipeline = trained[best_name]
    print(f"\nBest model for churn detection: {best_name}")
    print("(Chosen for highest churn recall — catching real churners matters most.)")

    # ---------- 5. Save outputs ----------
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    perf_out = pd.DataFrame(results)
    perf_out["Selected"] = np.where(perf_out["Model"] == best_name, "Yes", "No")
    perf_out.round(4).to_csv(PERFORMANCE_PATH, index=False)
    print(f"Model performance saved to: {PERFORMANCE_PATH}")

    fi = extract_feature_importance(best_pipeline, best_name)
    fi.to_csv(IMPORTANCE_PATH, index=False)
    print(f"Feature importance saved to: {IMPORTANCE_PATH}")
    print("\nTop 10 most important features:")
    print(fi.head(10).to_string(index=False))

    joblib.dump(best_pipeline, MODEL_PATH)
    print(f"\nTrained model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
