# Dashboard Design System — Customer Churn Analytics

This file defines every color, font, size, and spacing rule used in the dashboard.
Follow it exactly and all 4 pages will look like one consistent product —
that consistency is what separates a professional BI dashboard from a student project.

---

## 1. Canvas

| Setting | Value | Where to set |
|---|---|---|
| Page size | 16:9 — **1280 × 720 px** | Format page → Canvas settings |
| Canvas background | `#F6F8FB` | Format page → Canvas background (transparency 0%) |
| Wallpaper | `#F6F8FB` | Format page → Wallpaper |

## 2. Color Palette

Use **only** these colors. If a visual needs a color not listed here, use Accent Blue.

| Role | Hex | Used for |
|---|---|---|
| Page background | `#F6F8FB` | Canvas + wallpaper |
| Card background | `#FFFFFF` | All visual backgrounds |
| Primary text | `#172B4D` | Titles, KPI values, axis labels |
| Secondary text | `#5E6C84` | Subtitles, KPI labels, axis titles |
| Churn / High risk | `#D64550` | Churn bars, High risk, negative KPIs |
| Medium risk | `#F2A93B` | Medium risk only |
| Low risk / positive | `#2EAD70` | Low risk, retention-positive values |
| Retained / stayed | `#2A9D8F` | "Stayed" segments |
| Accent blue | `#2F80ED` | Neutral bars, selected slicer state, buttons |
| Border / gridline | `#E5E9F0` | Card borders, gridlines, dividers |
| Sidebar navy | `#172B4D` | Left navigation rail background |

**Semantic rule:** red always means churn/risk, green always means safe/retained,
blue is always neutral. Never swap these.

### Set the palette once as a theme (recommended)

Save this as `churn_theme.json`, then **View ribbon → Themes → Browse for themes**:

```json
{
  "name": "Churn Analytics",
  "dataColors": ["#2F80ED", "#D64550", "#2EAD70", "#F2A93B", "#2A9D8F", "#5E6C84"],
  "background": "#FFFFFF",
  "foreground": "#172B4D",
  "tableAccent": "#2F80ED",
  "textClasses": {
    "title":    { "color": "#172B4D", "fontFace": "Segoe UI Semibold", "fontSize": 12 },
    "label":    { "color": "#5E6C84", "fontFace": "Segoe UI", "fontSize": 9 },
    "callout":  { "color": "#172B4D", "fontFace": "Segoe UI Semibold", "fontSize": 26 }
  },
  "visualStyles": {
    "*": { "*": {
      "background": [{ "color": { "solid": { "color": "#FFFFFF" } }, "transparency": 0 }],
      "visualHeader": [{ "show": true }]
    }}
  }
}
```

## 3. Typography

Font family everywhere: **Segoe UI** (default in Power BI — no install needed).

| Element | Font | Size | Color |
|---|---|---|---|
| Page title | Segoe UI Semibold | 18 pt | `#172B4D` |
| Page subtitle | Segoe UI | 10 pt | `#5E6C84` |
| KPI value (callout) | Segoe UI Semibold | 26 pt | `#172B4D` (red/green when semantic) |
| KPI label | Segoe UI | 10 pt | `#5E6C84` |
| Visual titles | Segoe UI Semibold | 11 pt | `#172B4D` |
| Axis labels / legends | Segoe UI | 9 pt | `#5E6C84` |
| Table text | Segoe UI | 9–10 pt | `#172B4D` |
| Data labels | Segoe UI | 9 pt | `#5E6C84` |

**Title style rule:** write plain-English business titles in sentence case —
"Churn rate by contract type", never "ChurnRate by Contract" or ALL CAPS.

## 4. Card Style (apply to every visual)

Select each visual → **Format → General**:

| Property | Value |
|---|---|
| Effects → Background | `#FFFFFF`, 0% transparency |
| Effects → Visual border | On, `#E5E9F0`, **rounded corners 12 px** |
| Effects → Shadow | On, preset "Bottom right", color `#172B4D`, ~85% transparency |
| Padding | 12 px all sides (Format → General → Properties → Padding) |

Shortcut: format ONE visual perfectly, then use **Format Painter** (Home ribbon)
to copy the style to every other visual.

## 5. Layout Grid

All pages share the same skeleton so navigation feels seamless:

```
x=0            x=160  x=176                                        x=1264
+--------------+  +--------------------------------------------------+
|              |  |  PAGE TITLE (18pt)                    [slicers]  |   y=16..64
|  NAV RAIL    |  |  subtitle (10pt, #5E6C84)                        |
|  (#172B4D)   |  +--------------------------------------------------+
|  160px wide  |  |                                                  |
|  full height |  |              CONTENT AREA                        |   y=80..704
|              |  |     (cards on a 16px spacing grid)               |
+--------------+  +--------------------------------------------------+
```

- **Nav rail:** rectangle shape, `#172B4D`, x=0 y=0 w=160 h=720, on every page.
- **Gutter:** 16 px between all cards. Never let cards touch.
- **Alignment:** select visuals → Format ribbon → Align. Turn on **View → Gridlines**
  and **Snap to grid** before you start.
- **KPI card size:** 168 × 96 px (Page 1 uses six across the top).
- Turn OFF the visual header "more options" icons for viewers:
  File → Options → Report settings → hide the visual header in reading view.

## 6. Chart Rules

1. **One idea per chart.** If a chart needs a paragraph to explain, split it.
2. **Bars over pies.** The only donut allowed is the single Actual-Churn split
  (2 categories max, center label showing the %).
3. **Kill default clutter:** remove legends that repeat the title, remove axis
   titles when the chart title already says it, remove vertical gridlines,
   keep horizontal gridlines in `#E5E9F0`.
4. **Data labels on, axis off** for simple bar charts — labels carry the numbers,
   so the axis scale is redundant.
5. **Sort by value** (descending) unless the axis has a natural order
   (tenure groups, charge groups — sort by the Sort Order column instead).
6. **Conditional color:** churn-rate bars use red `#D64550`; neutral count bars
   use blue `#2F80ED`; risk-level visuals use the 3 risk colors exactly.

## 7. Number Formats

| Metric type | Format | Example |
|---|---|---|
| Customer counts | Whole number, thousands separator | 7,043 |
| Rates / probabilities | Percentage, 1 decimal | 26.5% |
| Monthly money | Currency $, 0 decimals (K when > 100K) | $110,234 |
| Annual money | Currency $, 0 decimals, display units **Millions**, 2 dec | $1.32M |
| Tenure | Whole number + "mo" suffix in title | 32 |

Set formats on the **measure** (Measure tools ribbon), not per-visual — then every
visual inherits it automatically.

## 8. Slicer Style

- Style: **Tile** for Risk_Level (3 buttons), **Dropdown** for everything else.
- Placement: top-right of the content area, in one row, 32 px tall.
- Selected state: fill `#2F80ED`, white text. Unselected: white fill, `#5E6C84` text,
  `#E5E9F0` border.
- Always show "Select all" on dropdowns; single-select OFF.

## 9. Icon & Insight Callouts

Insight cards (Page 1) are **text boxes** on white rounded rectangles:
- A 4 px tall accent bar (thin rectangle, `#2F80ED` / `#D64550`) on the top edge
- Bold headline number in 14 pt `#172B4D`
- One-sentence takeaway in 9 pt `#5E6C84`

Use Unicode arrows/symbols sparingly: ▲ ▼ ● (colored via text color). No emoji
on executive pages.
