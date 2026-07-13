# Dashboard Build Guide — Customer Churn Analytics

The complete, click-by-click recipe for building the 4-page dashboard.
Budget **2.5–3.5 hours** for a first build. Work with these files open:

| File | What you'll take from it |
|---|---|
| `dashboard_design_system.md` | Colors, fonts, card styling, theme JSON |
| `power_query_steps.md` | Data import & transformation steps |
| `dax_measures.txt` | All 28 measures with expected values |
| `dashboard_wireframe.md` | Exact position/size of every visual |

**Build order matters:** data → measures → theme → pages → interactivity → polish.

---

## Part 1 — Setup (15 min)

### 1.1 Install & open Power BI Desktop
Microsoft Store → search **Power BI Desktop** → Install (free) → open →
close the splash screen. Any 2023+ version works.

### 1.2 Generate the data (skip if already done)
```
python scripts/data_cleaning.py
python scripts/churn_model.py
python scripts/generate_predictions.py
```
Confirm `data/powerbi/churn_predictions_powerbi.csv` exists.

### 1.3 Apply the theme
Create `churn_theme.json` from the JSON block in `dashboard_design_system.md` §2,
then **View ribbon → Themes dropdown → Browse for themes** → select it.
This sets the palette and fonts once, for everything.

### 1.4 Import and transform the data
Follow **`power_query_steps.md`** end to end (Steps 1–8): import both CSVs,
fix types, add the two sort-order columns, do the optional merge, Close & Apply,
then set the model-side sort orders and disable Auto date/time.

**Checkpoint:** Data pane shows `churn_predictions_powerbi` (7,043 rows) and
`feature_importance`; Risk_Level sorts High → Medium → Low.

---

## Part 2 — Measures (25 min)

1. **Home → Enter data** → don't type anything → name it `_Measures` → Load.
2. Open **`dax_measures.txt`**. For each of the 28 measures:
   right-click `_Measures` → **New measure** → paste → Enter → set the format
   noted under the measure (Measure tools ribbon).
3. After the first measure exists, delete the placeholder "Column1" from
   `_Measures` — the table becomes a dedicated measure folder with a
   calculator icon.

**Checkpoint:** drop `Total Customers` and `Monthly Revenue at Risk` on a blank
canvas as cards → **7,043** and **$110,234**. Delete the test cards.
Every measure's expected value is listed in the DAX file — verify as you go.

---

## Part 3 — The page skeleton (15 min)

Build the shared frame ONCE on Page 1, then copy it to the other pages.

1. **Format page** (paintbrush with no visual selected):
   Canvas settings → 16:9. Canvas background → `#F6F8FB`, 0% transparency.
2. **Nav rail:** Insert → Shapes → Rectangle. Position `0,0`, size `160×720`,
   fill `#172B4D`, no border. Add a text box on it: "CHURN ANALYTICS",
   white, 12 pt Semibold, at `12,20`.
3. **Title:** text box at `176,16` — "Executive Overview", 18 pt Semibold navy.
   Subtitle text box under it — 10 pt, `#5E6C84`.
4. **View ribbon:** tick **Gridlines** and **Snap to grid**.

Create 3 more pages (＋ at bottom). Copy the rectangle + text boxes to each
(Ctrl+C, Ctrl+V keeps positions). Rename the page tabs:
**Overview · Risk Center · Churn Drivers · Retention Strategy**.
Retitle each page's title/subtitle per the wireframe.

---

## Part 4 — Page 1: Executive Overview (35 min)

Positions/sizes for every visual: **wireframe §Page 1**.

### 4.1 Six KPI cards
1. Click empty canvas → **Card** visual → drag `Total Customers` into Fields.
2. Style it per design system §4: white background, `#E5E9F0` rounded border
   (12 px), subtle shadow. Callout value 26 pt navy; category label off;
   add your own label as a small text box OR turn the label on at 10 pt gray.
3. Position `176,88`, size `168×96`.
4. **Copy-paste it 5×**, swap the measure, position at x = 360, 544, 728,
   912, 1096. Measures in order: Actual Churn Rate, Predicted Churn Customers,
   High Risk Customers, Monthly Revenue at Risk, Annual Revenue at Risk.
5. Recolor the value red `#D64550` on: Actual Churn Rate, Monthly Revenue at
   Risk, Annual Revenue at Risk (Format → Callout value → color).

### 4.2 Donut — churn split
Donut visual at `176,200, 320×280`. **Legend:** Actual_Churn ·
**Values:** Total Customers. Slice colors: Yes `#D64550`, No `#2A9D8F`
(Format → Slices). Inner radius ~60%. Legend: bottom center. Detail labels:
percent of total only. Title: "Customer churn split".
Center %: place a small transparent-background card with `Actual Churn Rate`
in the donut hole.

### 4.3 Churn rate by contract
Clustered **bar** chart at `512,200, 360×280`.
**Y-axis:** Contract · **X-axis:** Actual Churn Rate.
Format: bars `#D64550` → data labels ON (percentage) → X-axis OFF → Y-axis
title OFF → sort descending. Title: "Churn rate by contract type".
Expected: Month-to-month 42.7% · One year 11.3% · Two year 2.8%.

### 4.4 Churn rate by payment method
Copy-paste 4.3 to `888,200, 376×280`, swap Y-axis to PaymentMethod.
Expected top: Electronic check 45.3%.

### 4.5 Three insight cards
Per wireframe positions. Each = white rounded rectangle + a thin 4 px
accent-color rectangle on its top edge + a text box:
- **"15×"** — Month-to-month customers churn at 15× the two-year rate (blue bar)
- **"47.4%"** — of first-year customers churn — onboarding is the danger zone (red bar)
- **"$110K/mo"** — revenue sits with customers the model predicts will leave (red bar)

### 4.6 Slicers
Four **dropdown** slicers in the title band (top-right, y=20, each ~120×32):
Contract, InternetService, Risk_Level, TenureGroup. Style per design system §8.

**Checkpoint:** select "Month-to-month" in the Contract slicer — all six KPI
cards and both bars update. Clear it.

---

## Part 5 — Page 2: Customer Risk Center (35 min)

### 5.1 KPI cards + note
Cards for `Active High Risk Customers` (1,050) and `Saveable Revenue at Risk`
($110,234) at wireframe positions. Note card at `560,88, 704×96`: text box
reading *"ⓘ This page is a prioritized retention call list. Customers are
ranked by churn probability — work from the top down."*

### 5.2 The call-list table (the centerpiece)
1. **Table** visual at `176,200, 520×504`. Drag in, in order: customerID,
   Churn_Probability, Risk_Level, Contract, tenure, MonthlyCharges,
   TotalCharges, PaymentMethod, InternetService.
2. **Filter to the actionable set** — Filters pane, "Filters on this visual":
   - Actual_Churn **is No** (can't save someone who already left)
   - Risk_Level **is High or Medium**
3. **Sort:** click the Churn_Probability header → descending.
4. **Conditional formatting** (Format → Cell elements, pick the column):
   - Churn_Probability → **Data bars** ON → bar color `#D64550`
   - Risk_Level → **Background color** ON → Format style: Rules →
     Rule 1 `If value is "High" then #FADBD8` · Rule 2 `"Medium" → #FDEBD0`
     (field value rules on text: choose "Rules", base on Risk_Level).
     Then Font color rules: High → `#D64550`, Medium → `#B9770E`.
   - MonthlyCharges / TotalCharges → already $ if you formatted the columns;
     otherwise select the column in Data pane → Format → Currency.
5. Style: Format → Style presets → **Minimal**; grid → row padding 4;
   header: fill `#F6F8FB`, text `#5E6C84`, 9 pt.

### 5.3 Right column — three charts
- **Customers by risk level** — bar, `712,200, 552×150`. Y: Risk_Level ·
  X: Total Customers. Colors per category: High `#D64550`, Medium `#F2A93B`,
  Low `#2EAD70` (Format → Bars → turn "Show all" on). Data labels on.
- **Probability distribution** — column, `712,366, 552×150`. Right-click
  `Churn_Probability` in Data pane → **New group** → Bin → size **0.1**.
  X: the new bins field · Y: Total Customers. Bars `#2F80ED`.
- **Charges vs tenure scatter** — scatter, `712,532, 552×172`.
  X: tenure · Y: MonthlyCharges · Legend: Risk_Level · **Values: customerID**
  (forces one dot per customer). Marker size 4. The story: the red cloud sits
  top-left = **new + expensive + high risk**.

### 5.4 Slicers
Risk_Level as **Tile** style; Contract and CustomerValueSegment as dropdowns.

---

## Part 6 — Page 3: Churn Drivers & Segments (30 min)

Follow wireframe §Page 3 positions.

1. **Top 10 churn drivers** — bar chart. Y: `Churn Driver` ·
   X: `Importance Score` (from the `feature_importance` table).
   Filters pane → Churn Driver → **Top N** → Top 10 by Importance Score →
   Apply. Bars `#2F80ED`. Title: "Top 10 churn drivers (from the ML model)".
2. **Heatmap matrix** — Matrix visual. Rows: Contract · Columns:
   InternetService · Values: **Actual Churn Rate**. Format → Cell elements →
   Background color → ON → Advanced: minimum `#FFFFFF`, maximum `#D64550`.
   Turn off row/column subtotals. The M2M + Fiber cell (54.6%) should glow red.
3. **Four small churn-rate charts** — build one column chart
   (X: TenureGroup · Y: Actual Churn Rate, red bars, data labels), then
   copy-paste and swap the X field: MonthlyChargeGroup, InternetService (use
   bar orientation), SeniorCitizenLabel, PaperlessBilling.
   *(SeniorCitizenLabel and PaperlessBilling require the Power Query merge —
   `power_query_steps.md` §5. If you skipped it, drop those two charts and
   enlarge the others.)*
4. **"Top churn drivers" text card** — the ①–⑤ list from the wireframe.

---

## Part 7 — Page 4: Retention Strategy (25 min)

1. **Action table data:** Home → **Enter data** → build the 6-column,
   5-row `retention_actions` table exactly as written in wireframe §Page 4 →
   Load.
2. **Table visual** at `176,200, 1088×256` with all 6 columns. Format:
   header fill `#172B4D`, white 10 pt header text; word wrap on values;
   column widths — give Recommended Action and Expected Impact the most room.
   Sort by Priority ascending.
3. **KPI cards** — `Active High Risk Customers` (relabel "Customers Targeted")
   and `Monthly Revenue at Risk`, plus the model one-liner text card.
4. **Revenue at risk by contract** — bar, Y: Contract ·
   X: Monthly Revenue at Risk, red bars.
   Expected: $92,432 / $12,786 / $5,016 — the chart itself argues for Action #1.
5. **High-risk customers by value segment** — bar, Y: CustomerValueSegment ·
   X: Active High Risk Customers, blue bars. Expected: 411 / 336 / 303.
6. **Business impact text card**:
   > *"If retention outreach saves just 1 in 4 targeted customers, the company
   > protects ≈ $28K of monthly revenue — about $330K per year — from a
   > one-time modeling project and a dashboard."*

---

## Part 8 — Interactivity (30 min)

### 8.1 Page navigation
1. On Page 1's navy rail: **Insert → Buttons → Navigator → Page navigator**.
2. Position on the rail (`8,120, 144×220`). Format → Grid layout →
   Vertical. Style states: Default — fill `#172B4D`, text white 10 pt;
   Selected — fill `#2F80ED`; Hover — fill `#2F3F5E`.
3. Copy the navigator to all pages (it highlights the current page
   automatically). **Ctrl+Click** navigates in Desktop; plain click after publish.

### 8.2 Tooltip page
1. New page, rename "Tooltip — Risk". Format page → Page information →
   **Allow use as tooltip: On**; Canvas settings → Type: **Tooltip**.
2. Add per wireframe §Tooltip: Risk_Level card, Average Churn Probability card,
   Total Customers card, explainer text.
3. Attach: select the Page 2 scatter + risk bar and Page 1 donut →
   Format → General → Tooltips → Type **Report page** → Page: Tooltip — Risk.
4. Right-click the tooltip page tab → **Hide page**.

### 8.3 Drill-through (optional, +20 min)
New page "Segment detail" → drag `Contract` into **Drill through** field well →
add KPI cards + the call-list table → hide the page. Now right-clicking any
contract bar offers "Drill through → Segment detail", auto-filtered, with a
back button.

### 8.4 Bookmarks (optional)
View → **Bookmarks pane** + Selection pane. On Page 1:
1. Clear all slicers → Add bookmark → rename **All Customers**
2. Risk_Level = High → Add bookmark → **High Risk Only** → clear
3. Contract = Month-to-month → **Month-to-Month Focus** → clear
4. InternetService = Fiber optic → **Fiber Optic Focus** → clear
Wire them to buttons if you like: Insert → Buttons → Blank → Action: Bookmark.

### 8.5 Interaction sanity pass
Click a bar on each page and watch the other visuals cross-filter. If a visual
shouldn't react (e.g., the Page 4 action table), select the clicked visual →
Format ribbon → **Edit interactions** → set that target to "None".

---

## Part 9 — Final polish (20 min)

- **Format Painter pass:** one perfectly styled visual per type → copy the
  style everywhere.
- **Alignment pass:** rubber-band-select rows of visuals → Format ribbon →
  Align → Distribute horizontally.
- **Title pass:** every visual has a sentence-case business title; no
  default "Sum of X by Y" titles anywhere.
- **Tooltip text pass:** the six metric explanations in
  `dashboard_user_guide.md` §KPI dictionary — put each into its visual's
  description or a header-icon tooltip (Format → General → Header icons →
  Help tooltip text).
- **Reading view check:** View → Reading view; tab through all 4 pages.

## Part 10 — Save & export

- **Save:** File → Save As → `powerbi/customer_churn_dashboard.pbix`.
- **PDF export:** File → Export → **Export to PDF**
  (exports all visible pages with current filter state — clear slicers first).
- **Screenshots for the GitHub README:** maximize each page in Reading view,
  Win+Shift+S, save into `powerbi/screenshots/` as `page1_executive_overview.png`,
  `page2_customer_risk_center.png`, and so on.
