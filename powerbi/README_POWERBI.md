# Power BI Package — Customer Churn Analytics Dashboard

A 4-page executive dashboard built on the churn predictions produced by this
repository's Python ML pipeline. This folder contains everything needed to
recreate it exactly in Power BI Desktop.

---

## Dashboard overview

| Page | Audience | Answers |
|---|---|---|
| **Executive Overview** | Leadership | What's the churn situation? What's it costing us? |
| **Customer Risk Center** | Retention team | Who do we call first? (ranked call list) |
| **Churn Drivers & Segments** | Analysts | Why are customers leaving? |
| **Retention Strategy** | Program owners | What do we do about it, and what's it worth? |

Headline numbers (from the real data): **7,043 customers · 26.5% churn ·
$110K/month revenue at risk · 1,050 active high-risk customers · model
catches ~4 of 5 churners.**

## Required input files

Produced by running the Python pipeline from the repo root
(`python scripts/data_cleaning.py`, then `churn_model.py`, then
`generate_predictions.py`):

| File | Used for |
|---|---|
| `data/powerbi/churn_predictions_powerbi.csv` | Main table (7,043 rows × 14 cols) |
| `outputs/feature_importance.csv` | Page 3 churn-drivers chart |
| `data/processed/cleaned_customer_churn.csv` | Optional merge: SeniorCitizen + PaperlessBilling for two extra Page 3 visuals |

## Requirements

- **Power BI Desktop**, free, any release from 2023 onward
  (Microsoft Store → "Power BI Desktop"). No Pro license needed for
  local building and PDF export.
- Windows 10/11. No custom visuals — everything uses built-in visuals.

## Files in this folder

| File | Purpose |
|---|---|
| `customer_churn_dashboard.pbix` | **The finished dashboard** — open directly in Power BI Desktop |
| `churn_theme.json` | Color/font theme applied to the report |
| `screenshots/` | Page images used in the main project README |
| `README_POWERBI.md` | This file — start here |
| `dashboard_build_guide.md` | The main recipe — click-by-click build (2.5–3.5 h) |
| `dax_measures.txt` | 28 DAX measures with formulas, explanations, formats, and expected values |
| `power_query_steps.md` | Data import & transformation (clicks + full M code) |
| `dashboard_wireframe.md` | Pixel-exact layout of every visual on all 4 pages |
| `dashboard_design_system.md` | Colors, fonts, card styling, theme JSON |
| `dashboard_user_guide.md` | How a business user reads and uses the dashboard |

## How to build (short version)

Already built: open `customer_churn_dashboard.pbix` in Power BI Desktop. To
reproduce it from scratch:

1. Run the Python pipeline (see above) so the CSVs exist.
2. Open `dashboard_build_guide.md` and follow Parts 1–10 in order:
   theme → Power Query → measures → page skeleton → 4 pages →
   interactivity → polish → save as `customer_churn_dashboard.pbix`.
3. Verify your KPI cards against the expected-values table at the bottom of
   `dax_measures.txt`.

## DAX measures included

28 measures in 6 groups — counts (Total/Churned/Non-Churned Customers),
rates (Actual & Predicted Churn Rate, Retention Rate), risk segmentation
(High/Medium/Low, Active High Risk, Avg Churn Probability), revenue
(Monthly/Annual/Saveable Revenue at Risk, High Risk Revenue, Avg Revenue per
Customer), model quality (TP/TN/FP/FN, Accuracy, Recall), and display
helpers. Full formulas: `dax_measures.txt`.

## Screenshots

Page images live in `screenshots/` and are displayed in the main project README:

```
powerbi/screenshots/
├── page1_executive_overview.png
├── page2_customer_risk_center.png
├── page3_churn_drivers.png
└── page4_retention_strategy.png
```

To refresh them, open the `.pbix`, switch to Reading view, and re-export each page.

## Troubleshooting

| Problem | Fix |
|---|---|
| KPI shows a wrong number | Compare against the verification table in `dax_measures.txt`; check visual-level filters and that the CSV loaded 7,043 rows |
| Risk_Level sorts Low → Medium → High | You skipped the sort column: `power_query_steps.md` §3 + §8.1 |
| Churn_Probability shows 0.73 instead of 73% | Select the column → Column tools → Format: Percentage |
| "Couldn't find file" on refresh | The CSV path moved — Transform data → Data source settings → Change Source |
| SeniorCitizen / PaperlessBilling missing | They come from the optional merge (`power_query_steps.md` §5) — or skip those two Page 3 visuals |
| Measures error with "cannot find table" | Your table is named differently — rename the query to `churn_predictions_powerbi` in Power Query |
| Charts look default-Power-BI | Apply the theme JSON (`dashboard_design_system.md` §2) and do the Format Painter pass |

## Customizing

- **Rebrand:** change the six palette colors in one place — the theme JSON —
  and re-apply it.
- **New risk thresholds:** edit `assign_risk_level()` in
  `scripts/generate_predictions.py`, rerun the pipeline, refresh Power BI.
- **Different dataset:** any CSV with the same 14 columns drops straight in.
- **More pages:** copy the skeleton (nav rail + title band) and keep the
  design system rules.

## Design notes

- The dashboard is intentionally organized one audience per page: executives
  (Overview), the retention team (Risk Center), analysts (Churn Drivers),
  and program owners (Retention Strategy).
- Two design decisions drive the whole package: framing model output as
  **revenue at risk** rather than raw predictions, and selecting the model for
  **recall over accuracy** so it catches the customers worth retaining.
- Export a PDF (build guide, Part 10) for a static, shareable version of the
  report where opening a `.pbix` is not practical.
