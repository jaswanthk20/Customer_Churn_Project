"""
============================================================
 STEP 1: DATA CLEANING & FEATURE ENGINEERING
 Customer Churn Prediction Project
============================================================
 What this script does:
   1. Loads the raw Telco Customer Churn dataset
   2. Explores the data (shape, types, missing values, churn rate)
   3. Cleans the data (fixes TotalCharges, handles blanks, duplicates)
   4. Creates new business-friendly features (TenureGroup, segments)
   5. Saves the cleaned dataset to data/processed/

 How to run (from the project root folder):
   python scripts/data_cleaning.py
============================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# File paths (relative to the project root)
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "telco_customer_churn.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_customer_churn.csv"


def load_data():
    """Load the raw dataset from data/raw/."""
    print("Loading raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH)
    return df


def explore_data(df):
    """Print a quick overview of the dataset so we understand what we have."""
    print("\n========== DATA UNDERSTANDING ==========")
    print(f"Dataset shape (rows, columns): {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(list(df.columns))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print("\nChurn counts:")
    print(df["Churn"].value_counts())

    churn_pct = (df["Churn"] == "Yes").mean() * 100
    print(f"\nChurn percentage: {churn_pct:.2f}%")


def clean_data(df):
    """Fix data quality issues found in the raw dataset."""
    print("\n========== DATA CLEANING ==========")
    df = df.copy()

    # --- 1. Fix TotalCharges ---
    # In the raw file TotalCharges is stored as TEXT because some rows
    # contain a blank space " " (these are brand-new customers with tenure = 0).
    # errors="coerce" turns anything that is not a number into NaN (missing).
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    blanks = df["TotalCharges"].isnull().sum()
    print(f"Blank/invalid TotalCharges values found: {blanks}")

    # --- 2. Handle the missing TotalCharges ---
    # A customer with tenure = 0 has not paid anything yet,
    # so the correct value for TotalCharges is 0.
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    # --- 3. Check for duplicate rows and duplicate customer IDs ---
    dup_rows = df.duplicated().sum()
    dup_ids = df["customerID"].duplicated().sum()
    print(f"Duplicate rows: {dup_rows} | Duplicate customer IDs: {dup_ids}")
    if dup_rows > 0:
        df = df.drop_duplicates()
        print("Duplicates removed.")

    # --- 4. Keep customerID ---
    # We do NOT use customerID as a model feature (it is just a label),
    # but we KEEP it in the file so we can identify customers in Power BI.

    # --- 5. Tidy up categorical text values ---
    # Strip any accidental spaces around text values.
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    print("Cleaning complete.")
    return df


def engineer_features(df):
    """Create new columns that make the data easier to analyze and model."""
    print("\n========== FEATURE ENGINEERING ==========")
    df = df.copy()

    # --- ChurnFlag: 1 if the customer churned, 0 if they stayed ---
    # Models and SQL both work more easily with numbers than "Yes"/"No".
    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

    # --- TenureGroup: how long the customer has been with us ---
    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=["0-12 months", "13-24 months", "25-48 months", "49-72 months"],
    )

    # --- MonthlyChargeGroup: low / medium / high monthly bill ---
    df["MonthlyChargeGroup"] = pd.cut(
        df["MonthlyCharges"],
        bins=[0, 35, 70, 200],
        labels=["Low (<$35)", "Medium ($35-$70)", "High (>$70)"],
    )

    # --- TotalChargeGroup: lifetime spend buckets (quartiles) ---
    df["TotalChargeGroup"] = pd.qcut(
        df["TotalCharges"],
        q=4,
        labels=["Q1 Lowest Spend", "Q2", "Q3", "Q4 Highest Spend"],
    )

    # --- CustomerValueSegment: business view of customer value ---
    # High bill + long tenure = the customers we most want to keep.
    def value_segment(row):
        if row["MonthlyCharges"] >= 70 and row["tenure"] >= 24:
            return "High Value"
        elif row["MonthlyCharges"] >= 70 or row["tenure"] >= 24:
            return "Medium Value"
        else:
            return "Low Value"

    df["CustomerValueSegment"] = df.apply(value_segment, axis=1)

    print("New columns created: ChurnFlag, TenureGroup, MonthlyChargeGroup,")
    print("                     TotalChargeGroup, CustomerValueSegment")
    return df


def main():
    df = load_data()
    explore_data(df)
    df = clean_data(df)
    df = engineer_features(df)

    # Save the cleaned dataset for the modeling step and for SQL/Power BI.
    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"\nCleaned dataset saved to: {CLEAN_DATA_PATH}")
    print(f"Final shape: {df.shape}")


if __name__ == "__main__":
    main()
