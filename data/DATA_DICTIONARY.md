# Data Dictionary

Every field produced by the pipeline, what it means, and how it was derived.

---

## Source

| | |
|---|---|
| **Dataset** | Billboard Hot 100, complete weekly archive |
| **URL** | https://github.com/utdata/rwd-billboard-data |
| **File** | `data-out/hot-100-current.csv` |
| **Coverage** | 4 Aug 1958 – present (3,551 weekly charts as of Aug 2026) |
| **Raw rows** | 355,100 |
| **Cost / access** | Free, public, no account, no API key |
| **Refresh** | Weekly, via the maintainer's GitHub Actions job |
| **Why this source** | It is the only complete, free, login-free record of *ranked consumer demand* in the US market spanning both the physical and streaming eras. Chart rank is a relative demand measure, so it stays comparable across 68 years even though the underlying units (singles sold, downloads, streams) changed completely. |

### Raw columns

| Column | Description |
|---|---|
| `chart_week` | Date of the chart (Saturday-dated) |
| `current_week` | Position this week, 1–100 |
| `title` | Song title |
| `performer` | Full credited artist string |
| `last_week` | Position last week, `NA` on a song's first week |
| `peak_pos` | Best position reached as of that week |
| `wks_on_chart` | Cumulative weeks on chart as of that week |

---

## Cleaning applied (`scripts/02_clean_data.py`)

| # | Step | Rows affected |
|---|---|---|
| 1 | Trim whitespace, collapse repeated spaces, normalise curly apostrophes to `'` | all |
| 2 | Convert Billboard's literal `"NA"` in `last_week` to a true blank | 32,460 |
| 3 | Parse `chart_week` into a real date; derive year, month, decade, era | all |
| 4 | Range-check: rank 1–100, peak 1–100, weeks-on-chart ≥ 1 | 0 dropped |
| 5 | Drop exact duplicate (week, title, performer) rows | 13 dropped |
| 6 | Split guest credits off the performer string → `primary_artist` | all |
| 7 | Flag seasonal/holiday titles by keyword | all |

**Result: 355,087 clean rows, 32,688 unique songs, 8,837 unique primary artists.**
A full run report is written to `data/processed/cleaning_log.txt`.

### Note on step 6 — artist splitting
Billboard packs every credit into one free-text field. Guest artists are split
off only on explicit joiners: `Featuring`, `Feat.`, `Ft.`, `With`, `Duet With`,
`Introducing`, `Presents`, `vs.`

The script deliberately does **not** split on `&`, `,`, `+` or `X`, because
those are part of real act names — Kool & The Gang, Earth, Wind & Fire,
Florence + The Machine, Simon & Garfunkel. An earlier version did split on
them and shortened those acts to "Kool", "Earth", "Florence" and "Simon",
which corrupted the artist-level counts. The trade-off is that a genuine duo
billing such as "Post Malone & Swae Lee" is counted as a single act. This is
recorded in the paper's limitations.

---

## `chart_weeks_clean.csv` — one row per song per chart week (355,087 rows)

*Not committed to Git (~56 MB). Regenerate with `python3 scripts/02_clean_data.py`.*

| Field | Type | Description |
|---|---|---|
| `chart_week` | date | Chart date (YYYY-MM-DD) |
| `chart_year` | int | Year of the chart |
| `chart_month` | int | Month, 1–12 |
| `chart_decade` | text | e.g. `1990s` |
| `era` | text | Commercial era bucket (see below) |
| `title` | text | Cleaned song title |
| `performer` | text | Full credited artist string, cleaned |
| `primary_artist` | text | Lead act, guest credits removed |
| `n_credited_artists` | int | Number of separately credited acts |
| `is_collaboration` | 0/1 | 1 if the credit contains a guest artist |
| `song_key` | text | `title :: performer`, lowercased — the join key |
| `rank` | int | Chart position that week, 1–100 |
| `last_week_rank` | int/blank | Position the previous week; blank on debut |
| `peak_position_to_date` | int | Best position reached as of that week |
| `weeks_on_chart` | int | Cumulative weeks as of that week |
| `is_top10` | 0/1 | Rank ≤ 10 |
| `is_number_one` | 0/1 | Rank = 1 |
| `is_holiday_song` | 0/1 | Title matched a seasonal keyword |

### Era buckets
| Value | Years | Rationale |
|---|---|---|
| 1. Physical / Airplay | pre-1991 | Chart built from retail reports and radio surveys |
| 2. Soundscan CD Era | 1991–2004 | Point-of-sale scanning begins (Nov 1991) |
| 3. Download & Early Streaming | 2005–2013 | Paid downloads counted (2005), streams added (2007) |
| 4. Streaming Majority | 2014–2017 | On-demand + YouTube fully weighted |
| 5. Algorithmic / Social Era | 2018–present | Playlist and short-form-video-driven consumption |

---

## `song_summary.csv` — one row per song (32,688 rows)

| Field | Type | Description |
|---|---|---|
| `song_key` | text | Join key |
| `title`, `performer`, `primary_artist` | text | Identity |
| `is_collaboration`, `is_holiday_song` | 0/1 | Flags carried from the week table |
| `debut_date` | date | First week on the Hot 100 |
| `debut_year`, `debut_decade`, `era` | | Cohort assignment |
| `debut_rank` | int | Position in its first week |
| `peak_position` | int | Best position ever reached |
| `weeks_to_peak` | int | Chart weeks from debut to peak (1 = peaked on debut) |
| `debut_is_peak` | 0/1 | 1 if `weeks_to_peak` = 1 |
| `total_weeks_on_chart` | int | Count of weeks appearing on the chart |
| `weeks_in_top10` | int | Weeks at rank ≤ 10 |
| `weeks_at_number_one` | int | Weeks at rank 1 |
| `last_chart_date` | date | Final week on the chart |
| `chart_span_weeks` | int | Calendar weeks from debut to last appearance |
| `had_reentry` | 0/1 | 1 if `chart_span_weeks` > `total_weeks_on_chart` (left and returned) |
| `reached_top40` | 0/1 | Peak ≤ 40. Filters out one-off album tracks |
| `lifecycle_segment` | text | 2×2 segment, below |

### `lifecycle_segment` definition
Speed-to-peak × longevity. Fast = peaked within 2 weeks. Long-lived = 20+ weeks on chart.

| Segment | Speed | Longevity | Commercial meaning |
|---|---|---|---|
| **Spike** | Fast | Short | Release-week attention that did not convert to demand |
| **Instant Standard** | Fast | Long | Launched big *and* held — the rarest and most valuable |
| **Slow Burn** | Slow | Long | Audience built over time; the classic developing hit |
| **Grinder** | Slow | Short | Climbed slowly, never caught |

---

## `artist_summary.csv` — one row per primary artist (8,837 rows)

| Field | Description |
|---|---|
| `primary_artist` | Lead act name |
| `first_chart_date`, `first_chart_year` | Career start on the Hot 100 |
| `last_chart_date` | Most recent appearance |
| `career_span_years` | Years between first and last appearance |
| `charted_songs` | Distinct songs charted as lead |
| `top10_songs`, `number_one_songs` | Peak-based counts |
| `total_chart_weeks` | Total song-weeks accumulated |
| `best_peak_position` | Career-best rank |
| `avg_weeks_per_song` | Mean chart run per song |

---

## `yearly_kpis.csv` — one row per chart year (69 rows, 1958–2026)

| Field | Description |
|---|---|
| `chart_year` | Year |
| `chart_weeks_in_year` | Charts published (normally 52) |
| `cohort_censored` | **1 = incomplete year, exclude from trend claims.** The two most recent years are flagged, because songs that debuted in them have not finished their chart runs, which biases half-life and durability downward |
| `chart_slots` | Rows available that year (weeks × 100) |
| `unique_songs` | Distinct songs appearing |
| `new_song_debuts` | Songs charting for the first time |
| `top40_debut_cohort` | Songs debuting that year that reached the Top 40 — the denominator for KPIs 1–3 |
| `kpi_debut_peak_rate_pct` | **KPI 1.** % of the Top-40 cohort that peaked in week 1 |
| `kpi_chart_half_life_weeks` | **KPI 2.** Median chart run of the Top-40 cohort |
| `kpi_durability_rate_pct` | **KPI 3.** % of the cohort lasting 26+ weeks |
| `kpi_catalog_crowding_pct` | **KPI 4.** % of chart slots held by songs that first charted 12+ months earlier |
| `kpi_breakthrough_artists` | **KPI 5.** Artists reaching the Top 10 for the first time ever |
| `avg_weeks_on_chart_per_slot` | Mean tenure of songs occupying the chart |
| `pct_slots_20wk_plus` / `pct_slots_52wk_plus` | Share of slots held by long-tenured songs |
| `distinct_number_ones` | Songs reaching #1 |
| `pct_slots_collaboration` | Share of slots with a guest credit |
| `pct_slots_holiday` | Share of slots held by seasonal titles |

---

## `chart_weeks_tableau.csv` — 1990-present extract (191,187 rows)

Same fields as `chart_weeks_clean.csv`, trimmed to the 12 columns the
dashboards use and filtered to 1990 onward, so it is small enough (~21 MB)
to live in the repository. **Connect Tableau to this file.**
