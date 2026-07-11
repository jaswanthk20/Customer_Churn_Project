-- ============================================================
-- CREATE TABLES — Customer Churn Prediction Project
-- ============================================================
-- Works in SQLite as-is. Notes for other databases:
--   * PostgreSQL / MySQL : change TEXT -> VARCHAR(100) if you prefer
--   * BigQuery           : change REAL -> FLOAT64, INTEGER -> INT64
--
-- Load order:
--   1. Run this script to create the tables
--   2. Import data/processed/cleaned_customer_churn.csv  -> customer_churn
--   3. Import outputs/churn_predictions.csv              -> churn_predictions
--
-- Easy way to load in SQLite (from the project root):
--   sqlite3 churn.db
--   .mode csv
--   .import --skip 1 data/processed/cleaned_customer_churn.csv customer_churn
--   .import --skip 1 outputs/churn_predictions.csv churn_predictions
-- ============================================================


-- ------------------------------------------------------------
-- Table 1: customer_churn
-- One row per customer, from the cleaned dataset.
-- ------------------------------------------------------------
DROP TABLE IF EXISTS customer_churn;

CREATE TABLE customer_churn (
    customerID           TEXT PRIMARY KEY,   -- unique customer identifier
    gender               TEXT,               -- Male / Female
    SeniorCitizen        INTEGER,            -- 1 = senior citizen, 0 = not
    Partner              TEXT,               -- Yes / No
    Dependents           TEXT,               -- Yes / No
    tenure               INTEGER,            -- months with the company (0-72)
    PhoneService         TEXT,               -- Yes / No
    MultipleLines        TEXT,               -- Yes / No / No phone service
    InternetService      TEXT,               -- DSL / Fiber optic / No
    OnlineSecurity       TEXT,               -- Yes / No / No internet service
    OnlineBackup         TEXT,
    DeviceProtection     TEXT,
    TechSupport          TEXT,
    StreamingTV          TEXT,
    StreamingMovies      TEXT,
    Contract             TEXT,               -- Month-to-month / One year / Two year
    PaperlessBilling     TEXT,               -- Yes / No
    PaymentMethod        TEXT,               -- 4 payment methods
    MonthlyCharges       REAL,               -- current monthly bill ($)
    TotalCharges         REAL,               -- lifetime spend ($)
    Churn                TEXT,               -- Yes = customer left
    ChurnFlag            INTEGER,            -- 1 = churned, 0 = stayed
    TenureGroup          TEXT,               -- 0-12 / 13-24 / 25-48 / 49-72 months
    MonthlyChargeGroup   TEXT,               -- Low / Medium / High bill bucket
    TotalChargeGroup     TEXT,               -- lifetime spend quartile
    CustomerValueSegment TEXT                -- High / Medium / Low Value
);


-- ------------------------------------------------------------
-- Table 2: churn_predictions
-- One row per customer, from the machine learning model output.
-- ------------------------------------------------------------
DROP TABLE IF EXISTS churn_predictions;

CREATE TABLE churn_predictions (
    customerID           TEXT PRIMARY KEY,
    Actual_Churn         TEXT,               -- what really happened (Yes/No)
    Predicted_Churn      TEXT,               -- what the model predicted (Yes/No)
    Churn_Probability    REAL,               -- model probability, 0.0 - 1.0
    Risk_Level           TEXT,               -- High / Medium / Low
    Contract             TEXT,
    PaymentMethod        TEXT,
    InternetService      TEXT,
    tenure               INTEGER,
    MonthlyCharges       REAL,
    TotalCharges         REAL,
    TenureGroup          TEXT,
    MonthlyChargeGroup   TEXT,
    CustomerValueSegment TEXT
);
