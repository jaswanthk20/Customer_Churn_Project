# Power Query Steps — Customer Churn Dashboard

Everything that happens **before** the data reaches the report: importing,
data types, sort-order columns, and the optional merge that unlocks two extra
Page 3 visuals. Follow the click-by-click steps; the M code at the end is the
same thing for copy-paste people.

---

## Step 1 — Import the main table

1. Power BI Desktop → **Get data → Text/CSV**
2. Select `data/powerbi/churn_predictions_powerbi.csv`
3. Click **Transform Data** (NOT Load — we clean first). The Power Query
   editor opens.
4. In the **Query settings** pane (right), rename the query to
   **`churn_predictions_powerbi`** (Properties → Name).

## Step 2 — Confirm data types

Click the small type icon in each column header and set:

| Column | Type |
|---|---|
| customerID, Actual_Churn, Predicted_Churn, Risk_Level, Contract, PaymentMethod, InternetService, TenureGroup, MonthlyChargeGroup, CustomerValueSegment | **Text** |
| Churn_Probability | **Decimal Number** |
| MonthlyCharges, TotalCharges | **Decimal Number** (currency formatting is applied later on the measures, not here) |
| tenure | **Whole Number** |

> `Churn_Probability` stays a 0–1 decimal (e.g. 0.7342). Don't multiply by 100
> here — we format it as a percentage in the model instead (Step 8), which keeps
> the math in DAX measures correct.

## Step 3 — Risk Sort Order column

Problem: text sorts alphabetically → High, Low, Medium. We want High → Medium → Low.

1. **Add Column ribbon → Conditional Column**
2. New column name: `RiskSortOrder`
3. Rules:
   - If `Risk_Level` equals `High` → Output **1**
   - Else if `Risk_Level` equals `Medium` → Output **2**
   - Else → **3**
4. OK, then set the new column's type to **Whole Number**.

## Step 4 — Charge Group Sort Order column

`MonthlyChargeGroup` also sorts wrong alphabetically (High, Low, Medium).

1. **Add Column → Conditional Column**, name: `ChargeGroupSortOrder`
2. If `MonthlyChargeGroup` equals `Low (<$35)` → **1**;
   else if equals `Medium ($35-$70)` → **2**; else → **3**
3. Type: Whole Number.

> `TenureGroup` ("0-12 months" … "49-72 months") and `Contract`
> (Month-to-month → One year → Two year) already sort correctly
> alphabetically — no sort column needed.

## Step 5 — (Optional but recommended) Merge SeniorCitizen & PaperlessBilling

The predictions CSV doesn't include these two fields, but the cleaned dataset
does — merging them in unlocks two extra churn-driver visuals on Page 3
without touching the Python code.

1. **Get data → Text/CSV** → `data/processed/cleaned_customer_churn.csv`
   → **Transform Data**. Rename this query `customer_details`.
2. Right-click `customer_details` → **untick "Enable load"** (we only need it
   as a lookup, not as a table in the model).
3. Select the `churn_predictions_powerbi` query →
   **Home ribbon → Merge Queries** (not "Merge as New").
4. Match on `customerID` = `customerID`, Join kind: **Left Outer** → OK.
5. A new `customer_details` column appears. Click its expand icon (⇆) →
   tick only **SeniorCitizen** and **PaperlessBilling** →
   untick "Use original column name as prefix" → OK.
6. Set `SeniorCitizen` to Whole Number, `PaperlessBilling` to Text.
7. Nicer labels: **Add Column → Conditional Column**, name `SeniorCitizenLabel`:
   If `SeniorCitizen` equals `1` → `Senior`, else → `Non-Senior`. Type: Text.

## Step 6 — Import feature importance

1. **Get data → Text/CSV** → `outputs/feature_importance.csv` → Transform Data
2. Rename the query **`feature_importance`**
3. Types: `Feature` Text, `Importance` Decimal Number, `Model` Text.
4. Professional display names: double-click the headers and rename
   `Feature` → **Churn Driver**, `Importance` → **Importance Score**.
5. Optional polish — human-readable driver names:
   **Transform → Replace Values** on Churn Driver, one at a time:
   - `Contract_Month-to-month` → `Month-to-month contract`
   - `InternetService_Fiber optic` → `Fiber optic internet`
   - `PaymentMethod_Electronic check` → `Electronic check payment`
   - `TechSupport_No` → `No tech support`
   - `OnlineSecurity_No` → `No online security`
   - `tenure` → `Tenure (months)`
   - `MonthlyCharges` → `Monthly charges`
   - `TotalCharges` → `Total charges`

## Step 7 — Close & Apply

**Home → Close & Apply.** Both tables load (7,043 rows in the main table —
verify in the Data view row count).

## Step 8 — Model-side settings (Table view, after loading)

1. **Sort orders:** select `Risk_Level` column → Column tools →
   **Sort by column** → `RiskSortOrder`. Repeat: `MonthlyChargeGroup` →
   sort by `ChargeGroupSortOrder`.
2. **Percentage display:** select `Churn_Probability` → Column tools →
   Format **Percentage**, 1 decimal. (The stored value stays 0–1.)
3. **Hide helper columns** from report view (right-click → Hide):
   `RiskSortOrder`, `ChargeGroupSortOrder`, `SeniorCitizen` (keep the Label).
4. **No relationships needed** — `feature_importance` is standalone (its only
   visual doesn't cross-filter with customer data). If Power BI auto-created
   a relationship, delete it in Model view.
5. **Disable Auto date/time** (removes hidden calendar tables that bloat
   the file): File → Options and settings → Options → Current file →
   Data Load → untick **Auto date/time**.

---

## Full M code (alternative to the clicks)

Paste via **Home → Advanced Editor** if you prefer. Adjust the two file paths.

### Query: churn_predictions_powerbi

```m
let
    Source = Csv.Document(
        File.Contents("C:\...\Customer_Churn_Project\data\powerbi\churn_predictions_powerbi.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"customerID", type text}, {"Actual_Churn", type text},
        {"Predicted_Churn", type text}, {"Churn_Probability", type number},
        {"Risk_Level", type text}, {"Contract", type text},
        {"PaymentMethod", type text}, {"InternetService", type text},
        {"tenure", Int64.Type}, {"MonthlyCharges", type number},
        {"TotalCharges", type number}, {"TenureGroup", type text},
        {"MonthlyChargeGroup", type text}, {"CustomerValueSegment", type text}}),
    RiskSort = Table.AddColumn(Typed, "RiskSortOrder",
        each if [Risk_Level] = "High" then 1
             else if [Risk_Level] = "Medium" then 2 else 3, Int64.Type),
    ChargeSort = Table.AddColumn(RiskSort, "ChargeGroupSortOrder",
        each if [MonthlyChargeGroup] = "Low (<$35)" then 1
             else if [MonthlyChargeGroup] = "Medium ($35-$70)" then 2 else 3, Int64.Type),
    Merged = Table.NestedJoin(ChargeSort, {"customerID"},
        customer_details, {"customerID"}, "cd", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "cd",
        {"SeniorCitizen", "PaperlessBilling"}, {"SeniorCitizen", "PaperlessBilling"}),
    SeniorLabel = Table.AddColumn(Expanded, "SeniorCitizenLabel",
        each if [SeniorCitizen] = 1 then "Senior" else "Non-Senior", type text)
in
    SeniorLabel
```

### Query: customer_details  (load disabled)

```m
let
    Source = Csv.Document(
        File.Contents("C:\...\Customer_Churn_Project\data\processed\cleaned_customer_churn.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Kept = Table.SelectColumns(Promoted, {"customerID", "SeniorCitizen", "PaperlessBilling"}),
    Typed = Table.TransformColumnTypes(Kept, {
        {"customerID", type text}, {"SeniorCitizen", Int64.Type},
        {"PaperlessBilling", type text}})
in
    Typed
```

### Query: feature_importance

```m
let
    Source = Csv.Document(
        File.Contents("C:\...\Customer_Churn_Project\outputs\feature_importance.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"Feature", type text}, {"Importance", type number}, {"Model", type text}}),
    Renamed = Table.RenameColumns(Typed,
        {{"Feature", "Churn Driver"}, {"Importance", "Importance Score"}}),
    Friendly = Table.ReplaceValue(
        Table.ReplaceValue(
            Table.ReplaceValue(Renamed,
                "Contract_Month-to-month", "Month-to-month contract",
                Replacer.ReplaceText, {"Churn Driver"}),
            "InternetService_Fiber optic", "Fiber optic internet",
            Replacer.ReplaceText, {"Churn Driver"}),
        "PaymentMethod_Electronic check", "Electronic check payment",
        Replacer.ReplaceText, {"Churn Driver"})
in
    Friendly
```

---

## Sanity checks after loading

| Check | Expected |
|---|---|
| churn_predictions_powerbi row count | 7,043 |
| Risk_Level values sort as | High, Medium, Low |
| Churn_Probability shows as | 73.4% style percentages |
| feature_importance top row | Month-to-month contract (~0.56) |
