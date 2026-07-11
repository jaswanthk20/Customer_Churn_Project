# Power BI Dashboard Build Guide — Customer Churn Prediction

This guide walks you through building the 3-page churn dashboard **step by step**,
even if you have never used Power BI before. Budget 60–90 minutes.

---

## Step 0 — Before You Start

1. Run the Python pipeline first so the data file exists:
   ```
   python scripts/data_cleaning.py
   python scripts/churn_model.py
   python scripts/generate_predictions.py
   ```
2. Confirm this file exists: `data/powerbi/churn_predictions_powerbi.csv`
3. Download **Power BI Desktop** (free): Microsoft Store → search "Power BI Desktop" → Install.

---

## Step 1 — Import the Data

1. Open **Power BI Desktop**.
2. Click **Get data** → **Text/CSV**.
3. Browse to `data/powerbi/churn_predictions_powerbi.csv` and click **Open**.
4. In the preview window, check the columns look right, then click **Load**.
5. In the **Data** pane (right side) you should now see a table named
   `churn_predictions_powerbi` with 14 columns and 7,043 rows.

**Check the data types** (Ribbon → Table view → select column → Data type):
- `Churn_Probability`, `MonthlyCharges`, `TotalCharges` → **Decimal number**
- `tenure` → **Whole number**
- Everything else → **Text**

---

## Step 2 — Create the DAX Measures

Open `powerbi/dax_measures.txt`. For **each** measure:

1. In the **Data** pane, right-click the table name → **New measure**.
2. Paste the formula and press **Enter**.
3. Set the format in the **Measure tools** ribbon:
   - `Churn Rate`, `Average Churn Probability`, `Model Accuracy` → **Percentage**, 1 decimal
   - `Average Monthly Charges`, `Revenue at Risk`, `Average Total Charges` → **Currency ($)**
   - Counts (`Total Customers`, etc.) → **Whole number**, thousands separator on

Create all 11 core measures (plus the 3 bonus ones if you want).

---

## Step 3 — Page 1: Executive Overview

Rename the page tab (bottom-left, double-click "Page 1") to **Executive Overview**.

### 3a. KPI Cards (top row, 5 cards side by side)

For each: **Visualizations pane → Card**, then drag the measure into **Fields**.

| Card # | Measure                 |
|--------|-------------------------|
| 1      | Total Customers         |
| 2      | Churned Customers       |
| 3      | Churn Rate              |
| 4      | Average Monthly Charges |
| 5      | Revenue at Risk         |

Resize each to about 2.5 cm tall and line them up across the top.

### 3b. Donut Chart — Churn Yes vs No

1. Click empty canvas → **Donut chart**.
2. **Legend** → `Actual_Churn`
3. **Values** → `Total Customers` (the measure)
4. Title: "Customer Churn Split".

### 3c. Bar Chart — Churn Rate by Contract

1. **Clustered bar chart**.
2. **Y-axis** → `Contract`
3. **X-axis** → `Churn Rate` (the measure — it recalculates per bar automatically)
4. Title: "Churn Rate by Contract Type". Sort descending
   (chart menu `…` → Sort axis → Churn Rate).

### 3d. Bar Chart — Churn Rate by Payment Method

Same as 3c but **Y-axis** → `PaymentMethod`. Title: "Churn Rate by Payment Method".

### 3e. Slicers (left edge, stacked vertically)

For each: **Slicer** visual, drag the field in, and in Format → Slicer settings
choose **Vertical list** (or Dropdown to save space).

- Slicer 1 → `Contract`
- Slicer 2 → `InternetService`
- Slicer 3 → `Risk_Level`

**Test it:** click "Month-to-month" in the Contract slicer — every card and chart
should update. That interactivity is what you demo in interviews.

---

## Step 4 — Page 2: Customer Risk Analysis

Add a page (+ at bottom), rename to **Customer Risk Analysis**.

### 4a. High-Risk Customer Table

1. **Table** visual, sized to fill the left half of the page.
2. Drag in: `customerID`, `Churn_Probability`, `Risk_Level`, `Contract`,
   `tenure`, `MonthlyCharges`.
3. Sort by `Churn_Probability` descending (click the column header).
4. Filter to high risk: with the table selected, open the **Filters** pane →
   drag `Risk_Level` into "Filters on this visual" → tick **High**.
5. Optional polish: select the table → Format → **Cell elements** →
   `Churn_Probability` → Data bars → red.

### 4b. Churn Probability Distribution

1. **Stacked column chart** (a histogram substitute).
2. **X-axis** → `Churn_Probability`
   - Power BI groups decimals poorly, so create bins: right-click
     `Churn_Probability` in the Data pane → **New group** → Bin size **0.1** → OK.
   - Use the new "Churn_Probability (bins)" field on the X-axis.
3. **Y-axis** → `Total Customers`
4. Title: "Distribution of Churn Probability".

### 4c. Risk Level Breakdown

1. **Donut chart** (or stacked bar).
2. **Legend** → `Risk_Level`, **Values** → `Total Customers`.
3. Set the colors (Format → Slices): High = red `#D64550`,
   Medium = amber `#E8A33D`, Low = green `#3D9970`.

### 4d. Churn Probability by Contract Type

1. **Clustered column chart**.
2. **X-axis** → `Contract`, **Y-axis** → `Average Churn Probability`.

### 4e. Churn Probability by Tenure Group

1. **Line chart** (shows the lifecycle trend nicely).
2. **X-axis** → `TenureGroup`, **Y-axis** → `Average Churn Probability`.
3. If the groups sort alphabetically instead of logically, click the chart's
   `…` menu → Sort axis → TenureGroup → ascending (the labels start with
   numbers, so they sort correctly).

---

## Step 5 — Page 3: Business Insights

Add a page, rename to **Business Insights**.

### 5a. Churn Rate by Tenure Group
**Clustered column chart** — X: `TenureGroup`, Y: `Churn Rate`.

### 5b. Churn Rate by Monthly Charge Group
**Clustered column chart** — X: `MonthlyChargeGroup`, Y: `Churn Rate`.

### 5c. Churn Rate by Internet Service
**Clustered bar chart** — Y: `InternetService`, X: `Churn Rate`.

### 5d. Feature Importance Chart

This uses a **second CSV**:
1. **Get data → Text/CSV** → `outputs/feature_importance.csv` → Load.
2. **Clustered bar chart** — Y-axis: `Feature`, X-axis: `Importance`
   (set aggregation to **Sum** if asked).
3. Filter to the top 10: Filters pane → `Feature` → Filter type **Top N** →
   Show items: Top 10 → By value: `Importance` → Apply.
4. Title: "What Drives Churn? (Model Feature Importance)".

### 5e. Recommended Retention Actions (text box)

Insert → **Text box**, and type:

> **Recommended Actions**
> 1. Convert month-to-month customers to annual contracts with discounts
> 2. Launch a 90-day onboarding program for new customers
> 3. Proactively contact High-risk customers with loyalty offers
> 4. Review fiber optic pricing and service quality
> 5. Move electronic-check payers to auto-pay

---

## Step 6 — Professional Formatting

**Colors (keep it simple and consistent):**
- Stayed / positive: teal `#2A9D8F` • Churned / negative: red `#D64550`
- Neutral bars: slate blue `#3D5A80` • Background: white or `#F5F7FA`
- Set once: View ribbon → Themes → Customize current theme.

**Layout rules:**
- Cards across the top, slicers down the left, charts in a grid — align with
  Format ribbon → Align.
- One idea per chart; give every chart a plain-English title
  ("Churn Rate by Contract Type", not "ChurnRate by Contract").
- Turn off visual clutter: Format → remove legends that repeat the title,
  turn on Data labels for bar charts.
- Add a dashboard title on each page: Insert → Text box → e.g.
  "Customer Churn — Executive Overview", 20pt bold.

**Final step:** File → Save As → `powerbi/customer_churn_dashboard.pbix`.

---

## Step 7 — How to Present This in an Interview

Walk the pages in order — it tells a story:

1. **Executive Overview** — "Churn is ~27%, which puts roughly $X of monthly
   revenue at risk. The donut and contract chart show churn concentrates in
   month-to-month customers." *(Click a slicer live to show interactivity.)*
2. **Risk Analysis** — "This page is for the retention team. The table is a
   ranked call list from my machine learning model — highest churn probability
   first, filtered to still-active customers."
3. **Business Insights** — "This page answers WHY. Feature importance from the
   model shows contract type, tenure, and monthly charges drive churn — so my
   recommendations target exactly those levers."

Key line to say: *"I designed each page for a different audience — executives,
the retention team, and strategy — all fed by one ML pipeline."*
