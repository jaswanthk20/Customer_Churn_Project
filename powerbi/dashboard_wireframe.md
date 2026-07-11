# Dashboard Wireframe — Customer Churn Prediction

Text wireframes for the 3-page Power BI dashboard. Build instructions are in
`dashboard_build_guide.md`; DAX formulas are in `dax_measures.txt`.

---

## Page 1 — Executive Overview

```
+---------------------------------------------------------------------------+
|  CUSTOMER CHURN — EXECUTIVE OVERVIEW                                      |
+---------+-----------------------------------------------------------------+
|         |  +---------+ +---------+ +---------+ +----------+ +-----------+ |
| SLICERS |  |  7,043  | |  1,869  | |  26.5%  | |  $64.76  | |   $XX,XXX | |
|         |  |  Total  | | Churned | |  Churn  | |   Avg    | |  Revenue  | |
| Contract|  |Customers| |Customers| |  Rate   | | Monthly  | |  at Risk  | |
| [list]  |  +---------+ +---------+ +---------+ +----------+ +-----------+ |
|         |                                                                 |
| Internet|  +--------------------+  +-----------------------------------+  |
| Service |  |    DONUT CHART     |  |  BAR: Churn Rate by Contract      |  |
| [list]  |  |  Churn Yes vs No   |  |  Month-to-month  ############ 43% |  |
|         |  |                    |  |  One year        #### 11%         |  |
| Risk    |  |   (Yes=red 26.5%)  |  |  Two year        # 3%             |  |
| Level   |  |   (No=teal 73.5%)  |  +-----------------------------------+  |
| [list]  |  |                    |  +-----------------------------------+  |
|         |  |                    |  |  BAR: Churn Rate by Payment Method|  |
|         |  |                    |  |  Electronic check ########## 45%  |  |
|         |  |                    |  |  Mailed check     #### 19%        |  |
|         |  |                    |  |  Bank transfer    #### 17%        |  |
|         |  |                    |  |  Credit card      ### 15%         |  |
|         |  +--------------------+  +-----------------------------------+  |
+---------+-----------------------------------------------------------------+
```

---

## Page 2 — Customer Risk Analysis

```
+---------------------------------------------------------------------------+
|  CUSTOMER RISK ANALYSIS                                                   |
+---------------------------------+-----------------------------------------+
|  HIGH-RISK CUSTOMER TABLE       |  +-----------------------------------+  |
|  (sorted by probability desc,   |  |  COLUMN: Churn Probability        |  |
|   filtered Risk_Level = High)   |  |  Distribution (bins of 0.1)       |  |
|                                 |  |      ##                           |  |
|  ID      Prob  Risk  Contract   |  |  ### ## #                         |  |
|  1234-A  0.92  High  M-to-M     |  |  ## ### ## ## #  #                |  |
|  5678-B  0.90  High  M-to-M     |  |  0.0 0.2 0.4 0.6 0.8 1.0          |  |
|  9012-C  0.89  High  M-to-M     |  +-----------------------------------+  |
|  ...                            |  +----------------+------------------+  |
|                                 |  | DONUT:         | COLUMN: Avg      |  |
|  (probability shown with        |  | Risk Level     | Churn Prob by    |  |
|   red data bars)                |  | High/Med/Low   | Contract Type    |  |
|                                 |  | red/amber/green|                  |  |
|                                 |  +----------------+------------------+  |
|                                 |  +-----------------------------------+  |
|                                 |  |  LINE: Avg Churn Probability      |  |
|                                 |  |  by Tenure Group (declining)      |  |
|                                 |  +-----------------------------------+  |
+---------------------------------+-----------------------------------------+
```

---

## Page 3 — Business Insights

```
+---------------------------------------------------------------------------+
|  BUSINESS INSIGHTS & RECOMMENDATIONS                                      |
+------------------------------------+--------------------------------------+
|  +------------------------------+  |  +--------------------------------+  |
|  | COLUMN: Churn Rate by        |  |  | BAR: Feature Importance        |  |
|  | Tenure Group                 |  |  | (Top 10 churn drivers from ML) |  |
|  | 0-12m  ########## 48%        |  |  | Contract_Two year   ########   |  |
|  | 13-24m ###### 29%            |  |  | tenure              #######    |  |
|  | 25-48m #### 20%              |  |  | InternetSvc_Fiber   ######     |  |
|  | 49-72m ## 10%                |  |  | TotalCharges        #####      |  |
|  +------------------------------+  |  | ...                            |  |
|  +------------------------------+  |  +--------------------------------+  |
|  | COLUMN: Churn Rate by        |  |  +--------------------------------+  |
|  | Monthly Charge Group         |  |  | TEXT BOX:                      |  |
|  | Low / Medium / High          |  |  | RECOMMENDED RETENTION ACTIONS  |  |
|  +------------------------------+  |  | 1. Contract-upgrade discounts  |  |
|  +------------------------------+  |  | 2. 90-day onboarding program   |  |
|  | BAR: Churn Rate by           |  |  | 3. Outreach to High-risk list  |  |
|  | Internet Service             |  |  | 4. Review fiber pricing        |  |
|  | Fiber / DSL / None           |  |  | 5. Move e-check to auto-pay    |  |
|  +------------------------------+  |  +--------------------------------+  |
+------------------------------------+--------------------------------------+
```

---

## Color Legend

| Use                  | Color        | Hex       |
|----------------------|--------------|-----------|
| Stayed / positive    | Teal         | `#2A9D8F` |
| Churned / High risk  | Red          | `#D64550` |
| Medium risk          | Amber        | `#E8A33D` |
| Low risk             | Green        | `#3D9970` |
| Neutral bars         | Slate blue   | `#3D5A80` |
| Page background      | Light gray   | `#F5F7FA` |
