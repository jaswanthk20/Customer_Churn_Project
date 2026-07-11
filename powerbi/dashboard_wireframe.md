# Dashboard Wireframe — Customer Churn Analytics

Canvas: **1280 × 720 px** on every page. Positions are given as
`x, y, width × height` — set them exactly in **Format → General → Properties →
Position/Size** and every page will align perfectly.

Shared skeleton on all 4 pages:
- **Nav rail:** navy rectangle `#172B4D`, `0, 0, 160 × 720`, with the project
  name at top and a Page Navigator button stack (see build guide §10)
- **Title block:** page title at `176, 16`, subtitle directly under it
- **Slicer row:** top-right, `y = 20`, 32 px tall dropdowns
- **Content area:** `x 176 → 1264`, `y 88 → 704`, 16 px gutters between cards

---

## Page 1 — Executive Overview
*Subtitle: "Churn, risk and revenue impact at a glance"*
*Slicers (top-right): Contract, InternetService, Risk_Level, TenureGroup (dropdowns, 120 px wide each)*

```
+--------++-----------------------------------------------------------------+
|        || Executive Overview            [Contract v][Internet v][Risk v][Tenure v]
|  NAV   || Churn, risk and revenue impact at a glance                      |
|        ||                                                                 |
| Churn  || +------+ +------+ +------+ +------+ +------+ +------+          |
| Analytics| |7,043 | |26.5% | |2,993 | |2,453 | |$110K | |$1.32M|          |
|        || |Total | |Churn | |Pred. | |High  | |Mo Rev| |Annual|          |
| ------ || |Cust. | |Rate  | |Churn | |Risk  | |atRisk| |atRisk|          |
| Overview|| +------+ +------+ +------+ +------+ +------+ +------+          |
| Risk   ||                                                                 |
| Center || +------------+  +-----------------+  +----------------------+  |
| Drivers|| |   DONUT    |  | BAR: Churn rate |  | BAR: Churn rate      |  |
| Strategy| |Churn split |  | by contract     |  | by payment method    |  |
|        || | 26.5% in   |  | M2M   ███ 42.7% |  | E-check   ███ 45.3%  |  |
|        || |  center    |  | 1yr   █   11.3% |  | Mailed    █   19.1%  |  |
|        || |red=churned |  | 2yr   ▏    2.8% |  | Bank      █   16.7%  |  |
|        || |teal=stayed |  |                 |  | Credit    █   15.2%  |  |
|        || +------------+  +-----------------+  +----------------------+  |
|        ||                                                                 |
|        || +-----------------+ +-----------------+ +-------------------+  |
|        || | INSIGHT ▬ blue  | | INSIGHT ▬ red   | | INSIGHT ▬ red     |  |
|        || | 15x             | | 47.4%           | | $110K / month     |  |
|        || | M2M customers   | | of first-year   | | of revenue sits   |  |
|        || | churn 15x more  | | customers churn | | with customers    |  |
|        || | than 2-yr ones  | |                 | | predicted to leave|  |
|        || +-----------------+ +-----------------+ +-------------------+  |
+--------++-----------------------------------------------------------------+
```

| # | Visual | Position | Fields | Formatting notes |
|---|---|---|---|---|
| 1.1 | Card ×6 | `176,88` … each `168×96`, 16 px apart (x = 176, 360, 544, 728, 912, 1096) | Measures: Total Customers · Actual Churn Rate · Predicted Churn Customers · High Risk Customers · Monthly Revenue at Risk · Annual Revenue at Risk | 26 pt navy values; churn-rate & at-risk values in red `#D64550`; 10 pt gray labels |
| 1.2 | Donut | `176,200, 320×280` | Legend: Actual_Churn · Values: Total Customers | Yes = `#D64550`, No = `#2A9D8F`; inner radius 60%; center label = Actual Churn Rate (26.5%); legend bottom |
| 1.3 | Bar (horizontal) | `512,200, 360×280` | Y: Contract · X: Actual Churn Rate | Bars `#D64550`; data labels %, 1 dec; X-axis off; sort desc |
| 1.4 | Bar (horizontal) | `888,200, 376×280` | Y: PaymentMethod · X: Actual Churn Rate | Same style as 1.3 |
| 1.5 | Insight card ×3 | `176,496 / 549,496 / 922,496`, each `352×192` (x = 176, 544, 912) | Text boxes on white cards | 4 px accent bar top edge; headline number 20 pt navy; body 9 pt gray |

---

## Page 2 — Customer Risk Center
*Subtitle: "Prioritized retention call list — highest churn probability first"*
*Slicers (top-right): Risk_Level (tile), Contract (dropdown), CustomerValueSegment (dropdown)*

```
+--------++-----------------------------------------------------------------+
|  NAV   || Customer Risk Center      [High|Med|Low] [Contract v][Segment v]|
|        || Prioritized retention call list - highest probability first    |
|        ||                                                                 |
|        || +---------+ +----------+ +----------------------------------+  |
|        || |  1,050  | | $110,234 | | ⓘ This page is a prioritized     |  |
|        || | Active  | | Saveable | |   retention call list. Work      |  |
|        || | High    | | Revenue  | |   top to bottom.                 |  |
|        || | Risk    | | at Risk  | |                                  |  |
|        || +---------+ +----------+ +----------------------------------+  |
|        ||                                                                 |
|        || +---------------------------+  +------------------------------+|
|        || | TABLE: call list          |  | BAR: Customers by risk level ||
|        || | ID | Prob▓▓ | Risk | Contr|  | High ███ 2,453 (red)         ||
|        || | 1) 100% High M2M  $105   |  | Med  ██  1,275 (amber)       ||
|        || | 2)  98% High M2M   $99   |  | Low  ███ 3,315 (green)       ||
|        || | 3)  97% High M2M   $95   |  +------------------------------+|
|        || |  ... (scrolls)           |  +------------------------------+|
|        || | data bars on Prob,       |  | COLUMN: probability          ||
|        || | color badges on Risk     |  | distribution (10% bins)      ||
|        || |                          |  +------------------------------+|
|        || | filtered: Actual=No,     |  +------------------------------+|
|        || | Risk = High or Medium    |  | SCATTER: charges vs tenure   ||
|        || | sorted by Prob desc      |  | colored by risk level        ||
|        || +---------------------------+  +------------------------------+|
+--------++-----------------------------------------------------------------+
```

| # | Visual | Position | Fields | Formatting notes |
|---|---|---|---|---|
| 2.1 | Card | `176,88, 168×96` | Active High Risk Customers | Red value |
| 2.2 | Card | `360,88, 184×96` | Saveable Revenue at Risk | Red value, currency |
| 2.3 | Note card | `560,88, 704×96` | Text box | "ⓘ This page is a prioritized retention call list…" 10 pt, `#5E6C84`, blue accent bar |
| 2.4 | Table | `176,200, 520×504` | customerID, Churn_Probability, Risk_Level, Contract, tenure, MonthlyCharges, TotalCharges, PaymentMethod, InternetService | Visual filters: Actual_Churn = No; Risk_Level = High or Medium. Sort Churn_Probability desc. Data bars (red) on probability; background badges on Risk_Level (red/amber text on tinted fill); $ on charges columns; row padding 4 px; wrap headers off |
| 2.5 | Bar | `712,200, 552×150` | Y: Risk_Level · X: Total Customers | Per-category colors High red / Med amber / Low green; data labels on |
| 2.6 | Column | `712,366, 552×150` | X: Churn_Probability **bins (0.1)** · Y: Total Customers | Single blue `#2F80ED`; title "Distribution of churn probability" |
| 2.7 | Scatter | `712,532, 552×172` | X: tenure · Y: MonthlyCharges · Legend: Risk_Level · Values: customerID | Risk colors; marker size 4; note the top-left cluster = new + expensive + high-risk |

---

## Page 3 — Churn Drivers & Segments
*Subtitle: "What the model and the data say is causing churn"*
*Slicers (top-right): Contract, InternetService (dropdowns)*

```
+--------++-----------------------------------------------------------------+
|  NAV   || Churn Drivers & Segments        [Contract v][Internet v]        |
|        || What the model and the data say is causing churn                |
|        ||                                                                 |
|        || +---------------------------+  +-----------+  +-----------+    |
|        || | BAR: Top 10 churn drivers |  | Churn rate |  | Churn rate|    |
|        || | (feature importance)      |  | by tenure  |  | by charge |    |
|        || | M2M contract ██████████   |  | group      |  | group     |    |
|        || | Tenure       ███          |  | (column)   |  | (column)  |    |
|        || | Fiber optic  ███          |  +-----------+  +-----------+    |
|        || | Monthly chgs ██           |  +-----------+  +-----------+    |
|        || | ...                       |  | Churn rate |  | Churn rate|    |
|        || +---------------------------+  | by internet|  | by senior |    |
|        || +---------------------------+  | service    |  | citizen   |    |
|        || | MATRIX HEATMAP            |  +-----------+  +-----------+    |
|        || | Contract x InternetService|  +-----------+  +-----------+    |
|        || | values = churn rate       |  | Churn rate |  | TEXT:     |    |
|        || | M2M+Fiber = 54.6% (dark   |  | by paperless| | Top churn |    |
|        || | red hotspot)              |  | billing    |  | drivers   |    |
|        || +---------------------------+  +-----------+  +-----------+    |
+--------++-----------------------------------------------------------------+
```

| # | Visual | Position | Fields | Formatting notes |
|---|---|---|---|---|
| 3.1 | Bar | `176,88, 520×300` | Y: Churn Driver · X: Importance Score (from `feature_importance`) | Top N filter = 10 by Importance Score; bars `#2F80ED`; title "Top 10 churn drivers (from the ML model)" |
| 3.2 | Matrix | `176,404, 520×300` | Rows: Contract · Columns: InternetService · Values: Actual Churn Rate | Cell elements → Background color scale white `#FFFFFF` → red `#D64550`; this is the heatmap. Expect hotspot: M2M + Fiber = 54.6% |
| 3.3 | Column | `712,88, 268×192` | X: TenureGroup · Y: Actual Churn Rate | Red bars, data labels, expect 47.4% → 9.5% downward staircase |
| 3.4 | Column | `996,88, 268×192` | X: MonthlyChargeGroup · Y: Actual Churn Rate | Red bars (sorted Low→High via sort column) |
| 3.5 | Bar | `712,296, 268×192` | Y: InternetService · X: Actual Churn Rate | Red bars |
| 3.6 | Column | `996,296, 268×192` | X: SeniorCitizenLabel · Y: Actual Churn Rate | Needs the Power Query merge (power_query_steps.md §5) |
| 3.7 | Column | `712,504, 268×200` | X: PaperlessBilling · Y: Actual Churn Rate | Needs the merge; title "Churn rate by paperless billing" |
| 3.8 | Text card | `996,504, 268×200` | Text box: "**Top churn drivers** — ① Month-to-month contract ② Short tenure ③ Fiber optic service ④ High monthly charges ⑤ Electronic check payment" | 9 pt, navy headline, gray body |

---

## Page 4 — Retention Strategy
*Subtitle: "From prediction to action — what to do and what it's worth"*
*Slicers: none (this page is a fixed narrative; keep it stable)*

```
+--------++-----------------------------------------------------------------+
|  NAV   || Retention Strategy                                              |
|        || From prediction to action - what to do and what it's worth      |
|        ||                                                                 |
|        || +---------+ +----------+ +----------------------------------+  |
|        || |  1,050  | | $110,234 | | 79% of churners caught by model  |  |
|        || | Cust.   | | Est. Mo. | | -> proactive retention becomes   |  |
|        || | Targeted| | Rev@Risk | |    possible for the first time   |  |
|        || +---------+ +----------+ +----------------------------------+  |
|        ||                                                                 |
|        || +-------------------------------------------------------------+|
|        || | ACTION TABLE (Enter-data table, 5 rows)                     ||
|        || | Pri | Segment        | Risk  | Problem     | Action | Impact||
|        || |  1  | M2M customers  | 42.7% | no lock-in  | ...    | $92K  ||
|        || |  2  | New (<12 mo)   | 47.4% | onboarding  | ...    | ...   ||
|        || |  3  | High-risk list | ...   | ...         | ...    | ...   ||
|        || |  4  | Fiber optic    | 41.9% | ...         | ...    | ...   ||
|        || |  5  | E-check payers | 45.3% | ...         | ...    | ...   ||
|        || +-------------------------------------------------------------+|
|        ||                                                                 |
|        || +------------------+ +------------------+ +-------------------+|
|        || | BAR: Revenue at  | | BAR: High-risk   | | BUSINESS IMPACT   ||
|        || | risk by contract | | customers by     | | Saving 1 in 4     ||
|        || | M2M ████ $92K    | | value segment    | | at-risk customers ||
|        || | 1yr █    $13K    | | Med ███ 411      | | protects ~$28K/mo ||
|        || | 2yr ▏     $5K    | | Low ██  336      | | = ~$330K/year     ||
|        || +------------------+ | High ██ 303      | +-------------------+|
|        ||                      +------------------+                      |
+--------++-----------------------------------------------------------------+
```

| # | Visual | Position | Fields | Formatting notes |
|---|---|---|---|---|
| 4.1 | Card | `176,88, 168×96` | Active High Risk Customers (label it "Customers Targeted") | Navy value |
| 4.2 | Card | `360,88, 184×96` | Monthly Revenue at Risk | Red value |
| 4.3 | Text card | `560,88, 704×96` | Model quality one-liner | Quote test-set numbers: "The model catches ~79% of real churners (test-set recall)" |
| 4.4 | Table | `176,200, 1088×256` | `retention_actions` table (Enter data — rows below) | Header fill `#172B4D`, white header text; Priority column center-aligned; word wrap on |
| 4.5 | Bar | `176,472, 360×232` | Y: Contract · X: Monthly Revenue at Risk | Red bars; expect $92,432 / $12,786 / $5,016 |
| 4.6 | Bar | `552,472, 360×232` | Y: CustomerValueSegment · X: Active High Risk Customers | Blue bars; expect Medium 411 / Low 336 / High 303 |
| 4.7 | Text card | `928,472, 336×232` | "Business impact" narrative | See user guide for wording |

**Rows for the `retention_actions` Enter-data table** (Home → Enter data,
name it `retention_actions`):

| Priority | Segment | Churn Risk | Problem | Recommended Action | Expected Impact |
|---|---|---|---|---|---|
| 1 | Month-to-month customers | 42.7% churn | No lock-in; leave anytime | Discounted 1–2 year contract upgrade campaign | Protects ~$92K/mo at-risk revenue |
| 2 | New customers (0–12 months) | 47.4% churn | Weak onboarding; early cancellations | 90-day onboarding: welcome call, setup help, first-bill review | Cuts first-year churn, the largest churn pool |
| 3 | Model-flagged high-risk (1,050 active) | ≥60% probability | Multiple risk factors stacked | Retention-team outreach with tailored loyalty offers | Saving 25% ≈ $28K/mo retained |
| 4 | Fiber optic subscribers | 41.9% churn | Price/quality dissatisfaction | Service-quality audit + price-match review | Protects the premium (highest-bill) tier |
| 5 | Electronic-check payers | 45.3% churn | Payment friction, failed payments | Auto-pay migration campaign with small incentive | Reduces churn in the highest-churn payment group |

---

## Extra pages (small, hidden)

### Tooltip page — "Risk explainer"
- Page information → **Allow use as tooltip = On**; Canvas type **Tooltip** (320×240)
- Background white, 12 px padding
- Contents: Risk_Level (card), Average Churn Probability (card),
  Total Customers (card), one line of text: "High = ≥60% probability →
  contact this week. Medium = 30–59% → automated offer. Low = <30% → no action."
- Attach: on Page 1–2 visuals → Format → General → Tooltips → Type: Report page → this page.

### Drill-through page — "Segment detail" (optional)
- Hidden page; **Drill through field:** Contract (add InternetService too if desired)
- Contents: title, the 6 KPI cards from Page 1 (copy-paste), plus the Page 2
  table filtered by the drilled value
- Usage: right-click any Contract bar → Drill through → Segment detail.
  A back button is added automatically — style it white on the navy rail.
