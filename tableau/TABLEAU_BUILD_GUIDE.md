# Tableau Build Guide

Build four dashboards in **Tableau Public** (free — no subscription, no trial expiry).
Published dashboards get a public URL you can put on a résumé or portfolio.

**Time required:** about 2–3 hours for all four.

---

## Step 0 — Setup

1. Download **Tableau Public** (free): https://public.tableau.com/app/discover
2. Create a free Tableau Public account. Saving is to the web, so every workbook you save gets a shareable link.
3. Run the pipeline once so the data files exist:
   ```
   python3 scripts/01_download_data.py
   python3 scripts/02_clean_data.py
   python3 scripts/03_build_kpis.py
   ```

### Connect the data
Open Tableau Public → **Connect → Text file** → choose files from `data/processed/`:

| File | Use it for |
|---|---|
| `yearly_kpis.csv` | Dashboards 1 and 3 (69 rows — instant) |
| `song_summary.csv` | Dashboard 2 (32,688 rows) |
| `chart_weeks_tableau.csv` | Dashboard 4 (191,187 rows) |
| `artist_summary.csv` | Optional artist explorer |

Keep them as **four separate data sources** — do not join them. Each dashboard uses one.

**Check after connecting:** click the *Data Source* tab and confirm `chart_year` is a **Number (whole)**, `chart_week`/`debut_date` are **Date**, and the `kpi_*` fields are **Number (decimal)**. If any KPI field imported as text, right-click → *Change Data Type → Number (decimal)*.

---

## Dashboard 1 — "The Signal Collapse"
*The headline story. If a hiring manager looks at only one screen, make it this one.*

**Data source:** `yearly_kpis.csv`

### Sheet 1.1 — Debut-Peak Rate over time (line)
- Columns: `chart_year` (right-click → Continuous → Dimension)
- Rows: `kpi_debut_peak_rate_pct`
- Filter: `chart_year` ≥ 1990, and `cohort_censored` = 0
- Add a reference line at 50% (Analytics pane → Reference Line → Constant 50)
- Title: **"By 2024, 73% of Top 40 hits peaked in their first week — up from 0.6% in 2000"**

### Sheet 1.2 — Chart Half-Life over time (line)
- Same setup, Rows: `kpi_chart_half_life_weeks`
- Annotate the 1995–2017 stretch: right-click the plot → *Annotate → Area* → "Flat at 20 weeks for 23 straight years"
- Title: **"Median commercial life of a hit fell from 20 weeks to 7"**

### Sheet 1.3 — Catalog Crowding (area chart)
- Columns: `chart_year` (continuous), Rows: `kpi_catalog_crowding_pct`
- Marks card → **Area**
- Title: **"Chart slots held by music over a year old"**

### Sheet 1.4 — Breakthrough Rate (bar)
- Columns: `chart_year` (discrete), Rows: `kpi_breakthrough_artists`
- Filter to 1990+; colour the bars by the measure (Marks → Color → drop `kpi_breakthrough_artists`)
- Title: **"First-time Top 10 artists per year"**

### Assemble
New Dashboard → size **1200 × 900 (Fixed size)**. Place the four sheets in a 2×2 grid.
Add a text object across the top:

> **THE SIGNAL COLLAPSE** — Four measures of how the US singles market changed after 2018.
> Source: Billboard Hot 100, 1958–2026 (355,087 song-weeks). Years still in progress are excluded.

**Formatting that makes it look professional:**
- Format → Workbook → Font: **Tableau Book, 10pt**
- Remove every gridline you do not need: Format → Lines → Grid Lines → **None**
- Use one accent colour for the current era and grey for history — not a rainbow palette
- Give every axis a plain-English title ("% of hits peaking in week 1", not "kpi_debut_peak_rate_pct")

---

## Dashboard 2 — "The Lifecycle Quadrant"
*The segmentation model, as a scatter plot people can explore.*

**Data source:** `song_summary.csv`

### Sheet 2.1 — The 2×2 scatter
- Columns: `weeks_to_peak` → **Dimension, Continuous**
- Rows: `total_weeks_on_chart` → **Dimension, Continuous**
- Marks: **Circle**, size small, opacity ~50%
- Detail: `title`, `performer` (so tooltips name the song)
- Colour: `lifecycle_segment`
- Filters: `reached_top40` = 1, and `era` (show as a filter card so viewers can switch eras)
- Reference lines: vertical constant at `weeks_to_peak` = 2, horizontal constant at `total_weeks_on_chart` = 20 — these draw the quadrant borders
- Tooltip: `<title>` by `<performer>`, peaked at #`<peak_position>` in week `<weeks_to_peak>`, lasted `<total_weeks_on_chart>` weeks

### Sheet 2.2 — Segment mix by era (100% stacked bar)
- Columns: `era`, Rows: `CNT(song_key)`
- Colour: `lifecycle_segment`
- Right-click the measure axis → *Add Table Calculation → Percent of Total → Table (down)*
- Filter `reached_top40` = 1

### Assemble
Dashboard 1200 × 800. Scatter on the left, stacked bar on the right, `era` filter applied to **both** sheets (filter dropdown → *Apply to Worksheets → Selected Worksheets*).

Title: **"The Slow Burn hit fell from 72% of the market to 26%"**

---

## Dashboard 3 — "The Decision Tool"
*This is the one that shows business judgement, not just charting.*

**Data source:** `song_summary.csv`

### Sheet 3.1 — Durability by debut rank band
Create a calculated field, `Debut Rank Band`:
```
IF [Debut Rank] <= 10 THEN "1. Debut Top 10"
ELSEIF [Debut Rank] <= 25 THEN "2. Debut 11-25"
ELSEIF [Debut Rank] <= 50 THEN "3. Debut 26-50"
ELSE "4. Debut 51-100"
END
```
Create `Is Durable`:
```
IF [Total Weeks On Chart] >= 26 THEN 1 ELSE 0 END
```
- Columns: `Debut Rank Band`, Rows: `AVG([Is Durable])` formatted as a percentage
- Filter: `reached_top40` = 1, `debut_year` between 2018 and 2024
- Title: **"Debut position barely predicts durability"** — the bars come out close to level, which *is* the finding

### Sheet 3.2 — Predictive power comparison (bar)
Manually enter the correlation results from the paper (§4.5) — Tableau cannot compute them from this file. Data → **New Data Source → Paste** this small table:

| Signal | Correlation with total run |
|---|---|
| Debut rank (week 1) | 0.107 |
| Rank at week 2 | 0.016 |
| Rank at week 4 | -0.149 |
| Rank at week 6 | -0.294 |
| Rank at week 8 | -0.380 |

- Horizontal bar chart, sorted, negative bars in the accent colour
- Title: **"Week-8 position carries 3.5× the information of debut position"**

Add a text box stating the business rule:
> **Move the A&R decision gate from week 1 to week 8.** Songs still holding near their peak at week 8 become 26-week assets 48% of the time. Songs that have collapsed do so 17% of the time.

---

## Dashboard 4 — "Catalog Takeover"
*The most visually striking one.*

**Data source:** `chart_weeks_tableau.csv`

### Sheet 4.1 — Holiday share of the chart by month (heat map)
- Columns: `chart_week` → **Year** (discrete)
- Rows: `chart_week` → **Month** (discrete)
- Marks: **Square**, Colour: `AVG(is_holiday_song)` formatted as a percentage
- Colour palette: single-hue sequential (Blue or Orange), not red-green
- Title: **"Seasonal catalog now takes over the chart every December"**

### Sheet 4.2 — Longest chart runs (bar)
- Switch to `song_summary.csv`
- Rows: `title` (sorted descending by `total_weeks_on_chart`), Columns: `total_weeks_on_chart`
- Filter: Top 15 by `total_weeks_on_chart`
- Colour by `debut_decade` — almost every bar will be 2010s/2020s, which is the point
- Title: **"The longest chart runs in 68 years are nearly all recent"**

---

## Publishing (free)

1. **File → Save to Tableau Public As…**
2. Name it clearly: `Signal vs Noise - The Discovery Bottleneck (Rebecca Wu)`
3. On your Tableau Public profile, set the workbook thumbnail to Dashboard 1
4. Copy the public URL and paste it into:
   - `README.md` (top of the repo)
   - `docs/index.html` (replace `YOUR_TABLEAU_URL`)
   - your portfolio site

**Note on Tableau Public:** every workbook you save is publicly visible — that is the point here, but never load private or client data into it.

---

## Checklist before you show anyone

- [ ] Every axis has a plain-English title
- [ ] Every dashboard has a source note with the row count and date range
- [ ] Censored years (2025–2026) are filtered out of trend charts, or clearly marked provisional
- [ ] Tooltips read as sentences, not field names
- [ ] Colour is used to mean something, and works in greyscale
- [ ] No default Tableau blue-orange everywhere — pick two colours and stay with them
- [ ] Each dashboard title states a **finding**, not a topic
