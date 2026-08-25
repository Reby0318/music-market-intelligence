# Excel Analysis Guide

How to reproduce and extend every finding in the paper using **Microsoft Excel alone** —
no Python required. This matters for two reasons: it proves the analysis independently,
and in an interview it lets you say *"here is the pivot table behind that number."*

---

## Which file to open

| File | Rows | Opens in Excel? |
|---|---|---|
| `yearly_kpis.csv` | 69 | Yes — instantly |
| `artist_summary.csv` | 8,837 | Yes |
| `song_summary.csv` | 32,688 | Yes |
| `chart_weeks_tableau.csv` | 191,187 | Yes (Excel handles ~1,048,576 rows) |
| `chart_weeks_clean.csv` | 355,087 | Yes, but slow — use Power Query |

**Always import, never double-click.** Double-clicking a CSV lets Excel guess data types, and
it will mangle dates and strip leading zeros. Instead:

**Data → Get Data → From File → From Text/CSV → Transform Data**

In the Power Query editor:
1. Set `chart_week` / `debut_date` to **Date**
2. Set all `kpi_*`, `rank`, `weeks_*` columns to **Decimal** or **Whole Number**
3. Set `title`, `performer`, `era`, `lifecycle_segment` to **Text**
4. **Close & Load To… → PivotTable Report**

---

## Analysis 1 — Reproduce the five headline KPIs

**File:** `yearly_kpis.csv`

1. Select all → **Insert → Table** (Ctrl+T), tick "My table has headers"
2. Add a filter on `cohort_censored` and set it to **0** (this removes the two incomplete years —
   the same guard the paper applies)
3. **Insert → PivotChart → Line**
   - Axis: `chart_year`
   - Values: `kpi_debut_peak_rate_pct` (set to **Average**, not Sum — one row per year)

Repeat for each KPI. Set every value field to **Average**; leaving it on Sum is the single most
common mistake with a pre-aggregated table like this one.

**Expected results (sanity check your work against these):**

| Year | Debut-Peak Rate | Chart Half-Life | Durability | Catalog Crowding | Breakthroughs |
|---|---|---|---|---|---|
| 2000 | 0.6% | 20 wks | 22.3% | 0.6% | 22 |
| 2010 | 33.5% | 20 wks | 21.3% | 2.1% | 13 |
| 2017 | 26.6% | 21 wks | 35.0% | 1.1% | 25 |
| 2024 | 72.7% | 7 wks | 19.1% | 5.1% | 23 |

---

## Analysis 2 — The lifecycle segment mix by era

**File:** `song_summary.csv`

1. Import as above → **Insert → PivotTable**
2. **Rows:** `era`
3. **Columns:** `lifecycle_segment`
4. **Values:** `song_key` → **Count**
5. **Filters:** `reached_top40` → set to **1**
6. Right-click any value → **Show Values As → % of Row Total**

You should get the table in §4.2 of the paper: Spike rising from 0.5% to 55.6%, Slow Burn
falling from 72.1% to 26.4%.

7. **Insert → PivotChart → 100% Stacked Column** to visualise it

---

## Analysis 3 — The December catalog takeover

**File:** `chart_weeks_tableau.csv`

1. Import via Power Query. Add a custom column for month:
   **Add Column → Date → Month → Month**
2. Load to a PivotTable
3. **Rows:** `chart_year`
4. **Columns:** the new `Month` field
5. **Values:** `is_holiday_song` → **Average** (a 0/1 column averaged gives you the share)
6. Format as a percentage, then **Home → Conditional Formatting → Color Scales**

The December column lights up from about 2019 onward. This one chart is the fastest way to
show a non-technical audience what "catalog crowding" means.

---

## Analysis 4 — Build the Week-8 Retention Ratio yourself

This is the paper's core recommendation, done in Excel. It is worth doing by hand because it
is the analysis an employer is most likely to ask you to explain.

**File:** `chart_weeks_tableau.csv`

1. Filter to a single year of debuts, e.g. songs whose first chart week falls in 2023
2. Sort by `title` then `chart_week` ascending
3. For each song, find:
   - **Best rank in weeks 1–4** → `=MINIFS(rank_column, title_column, "song name")` over the first 4 rows
   - **Rank at week 8** → the row where `weeks_on_chart` = 8
4. `Retention Ratio = (rank at week 8) / (best rank weeks 1-4)`
5. Sort ascending. Songs near 1.0 are holding; songs above 4.0 have collapsed.
6. Add a column `Durable = IF(total weeks >= 26, 1, 0)` and pivot `Retention Ratio` quintiles
   against `AVERAGE(Durable)`

**Expected:** roughly 48% durability in the best quintile, 17% in the worst.

**Faster route for a large batch:** in Power Query, **Group By** `title`, then use
`Table.Min` on rank for the first four rows. If that is unfamiliar, do it for 20–30 songs by
hand — it demonstrates the method just as well and is easier to talk through.

---

## Analysis 5 — Artist career explorer

**File:** `artist_summary.csv`

A quick, high-value pivot for interviews:

- **Rows:** `primary_artist`
- **Values:** `total_chart_weeks` (Sum), `top10_songs` (Sum), `career_span_years` (Max)
- **Sort:** by `total_chart_weeks` descending
- **Filter:** `first_chart_year` ≥ 2015 to see who has actually built a durable career in the streaming era

Compare that list to the all-time list. The contrast between long careers built pre-2010 and
the concentration of recent chart weeks in a handful of names is a strong talking point.

---

## Formatting for a portfolio-quality workbook

If you attach the Excel file to an application, treat it as a deliverable:

- **Sheet 1: `README`** — what the workbook contains, data source, date range, your name
- **Sheet 2: `Dashboard`** — 3–4 PivotCharts, no gridlines (View → uncheck Gridlines)
- **Sheet 3+: `Analysis_*`** — one pivot per sheet, each with a title cell in bold 14pt
- **Last sheet: `Data`** — the raw import, hidden or clearly labelled "source data — do not edit"
- Name every table and pivot (**PivotTable Analyze → PivotTable Name**)
- Use **Freeze Panes** on every data sheet
- Number formats: percentages to 1 decimal, weeks as whole numbers
- Delete unused sheets and leave the cursor in cell A1 of Sheet 1 before your final save

---

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| KPI values are absurdly large | Value field set to **Sum** on a pre-aggregated table | Change to **Average** |
| Dates show as text or as `45xxx` | CSV double-clicked instead of imported | Re-import via Power Query, set type to Date |
| Song counts look too high | Counting rows instead of distinct songs | In `chart_weeks_*` a song appears once per week — count from `song_summary.csv` instead |
| 2026 looks like a collapse | 2026 is a partial year (34 of 52 weeks) | Filter `cohort_censored = 0`, or exclude 2025–2026 |
| Artist names look truncated | Splitting credits on `&` | Use `primary_artist` from the pipeline, which handles this correctly |
