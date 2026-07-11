-- ============================================================
-- BUSINESS QUERIES — Customer Churn Prediction Project
-- ============================================================
-- These queries answer real business questions a telecom
-- retention team would ask. They use BOTH tables:
--   customer_churn    -> cleaned customer data
--   churn_predictions -> machine learning model output
-- ============================================================


-- ------------------------------------------------------------
-- 1. Identify high-risk customers (from the ML model)
-- "Which active customers does the model say are most likely
--  to leave?" — this is the retention team's call list.
-- ------------------------------------------------------------
SELECT
    customerID,
    ROUND(Churn_Probability * 100.0, 1) AS churn_probability_pct,
    Risk_Level,
    Contract,
    PaymentMethod,
    tenure,
    MonthlyCharges
FROM churn_predictions
WHERE Risk_Level = 'High'
  AND Actual_Churn = 'No'           -- still a customer: we can save them
ORDER BY Churn_Probability DESC
LIMIT 50;


-- ------------------------------------------------------------
-- 2. Top customer segments by churn rate
-- "Which combination of contract + internet service loses the
--  most customers?" — shows where churn is concentrated.
-- ------------------------------------------------------------
SELECT
    Contract,
    InternetService,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY Contract, InternetService
HAVING COUNT(*) >= 100                -- ignore tiny segments
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 3. Churn rate by tenure group
-- "When in the customer lifecycle do we lose people?"
-- Expect churn to be highest in the first 12 months.
-- ------------------------------------------------------------
SELECT
    TenureGroup,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY TenureGroup
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 4. Churn rate by monthly charge group
-- "Do customers with bigger bills leave more often?"
-- ------------------------------------------------------------
SELECT
    MonthlyChargeGroup,
    COUNT(*)                          AS total_customers,
    SUM(ChurnFlag)                    AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100.0, 2)  AS churn_rate_pct
FROM customer_churn
GROUP BY MonthlyChargeGroup
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- 5. Revenue at risk from likely churners
-- "If every customer the model flags actually leaves,
--  how much monthly revenue do we lose?"
-- Only counts ACTIVE customers predicted to churn.
-- ------------------------------------------------------------
SELECT
    COUNT(*)                        AS at_risk_customers,
    ROUND(SUM(MonthlyCharges), 2)   AS monthly_revenue_at_risk,
    ROUND(SUM(MonthlyCharges) * 12, 2) AS annual_revenue_at_risk
FROM churn_predictions
WHERE Predicted_Churn = 'Yes'
  AND Actual_Churn = 'No';


-- ------------------------------------------------------------
-- 6. High monthly charges + month-to-month contract
-- "Show me the riskiest combination in the customer base."
-- These customers pay a lot AND can leave any time.
-- ------------------------------------------------------------
SELECT
    customerID,
    MonthlyCharges,
    tenure,
    InternetService,
    PaymentMethod,
    Churn
FROM customer_churn
WHERE Contract = 'Month-to-month'
  AND MonthlyCharges > 70
  AND Churn = 'No'                  -- still saveable
ORDER BY MonthlyCharges DESC
LIMIT 50;


-- ------------------------------------------------------------
-- 7. Retention priority list
-- "Who should we call FIRST?"
-- Ranks active customers by (churn probability x monthly bill),
-- so we prioritize customers who are both likely to leave AND
-- worth the most money.
-- ------------------------------------------------------------
SELECT
    customerID,
    Risk_Level,
    ROUND(Churn_Probability * 100.0, 1)              AS churn_probability_pct,
    MonthlyCharges,
    ROUND(Churn_Probability * MonthlyCharges, 2)     AS priority_score,
    Contract,
    tenure,
    CustomerValueSegment
FROM churn_predictions
WHERE Actual_Churn = 'No'
  AND Risk_Level IN ('High', 'Medium')
ORDER BY priority_score DESC
LIMIT 100;


-- ------------------------------------------------------------
-- 8. Model accuracy check in SQL (bonus)
-- "How often did the model's prediction match reality?"
-- ------------------------------------------------------------
SELECT
    ROUND(
        SUM(CASE WHEN Actual_Churn = Predicted_Churn THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS prediction_match_pct
FROM churn_predictions;
