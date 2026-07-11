-- ============================================================
-- EXPLORATORY ANALYSIS — Customer Churn Prediction Project
-- ============================================================
-- Run against the customer_churn table (see create_tables.sql).
-- Every query is standard SQL and works in SQLite, PostgreSQL,
-- MySQL, and BigQuery.
--
-- Tip: ROUND(x, 2) keeps percentages readable.
-- ChurnFlag = 1 means the customer churned, so AVG(ChurnFlag)
-- is the churn RATE — a trick used throughout this file.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Total customers
-- How many customers are in the dataset?
-- ------------------------------------------------------------
SELECT COUNT(*) AS total_customers
FROM customer_churn;


-- ------------------------------------------------------------
-- 2. Churned customers
-- How many customers have left the company?
-- ------------------------------------------------------------
SELECT COUNT(*) AS churned_customers
FROM customer_churn
WHERE Churn = 'Yes';


-- ------------------------------------------------------------
-- 3. Overall churn rate
-- What percentage of all customers churned?
-- AVG of a 0/1 flag = proportion of 1s, so AVG(ChurnFlag)*100 = churn %.
-- ------------------------------------------------------------
SELECT
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn;


-- ------------------------------------------------------------
-- 4. Churn by contract type
-- Do month-to-month customers churn more than contract customers?
-- ------------------------------------------------------------
SELECT
    Contract,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 5. Churn by payment method
-- Which payment method has the highest churn?
-- ------------------------------------------------------------
SELECT
    PaymentMethod,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 6. Churn by internet service
-- Is fiber optic churn worse than DSL?
-- ------------------------------------------------------------
SELECT
    InternetService,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 7. Average monthly charges: churned vs stayed
-- Do churners pay more per month than loyal customers?
-- ------------------------------------------------------------
SELECT
    Churn,
    COUNT(*)                       AS customers,
    ROUND(AVG(MonthlyCharges), 2)  AS avg_monthly_charges
FROM customer_churn
GROUP BY Churn;


-- ------------------------------------------------------------
-- 8. Average tenure: churned vs stayed
-- Do churners leave early in their customer life?
-- ------------------------------------------------------------
SELECT
    Churn,
    COUNT(*)                    AS customers,
    ROUND(AVG(tenure), 1)       AS avg_tenure_months
FROM customer_churn
GROUP BY Churn;


-- ------------------------------------------------------------
-- 9. Churn by senior citizen
-- Do senior citizens churn at a higher rate?
-- ------------------------------------------------------------
SELECT
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END AS customer_age_group,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY customer_age_group
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 10. Churn by paperless billing
-- Is paperless billing linked to higher churn?
-- ------------------------------------------------------------
SELECT
    PaperlessBilling,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY PaperlessBilling
ORDER BY churn_rate_pct DESC;
