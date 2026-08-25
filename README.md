# Signal vs. Noise
### Quantifying the Discovery Bottleneck in the Streaming Era

A business-intelligence analysis of **68 years of Billboard Hot 100 data (355,087 song-weeks, 1958–2026)**, measuring how the music industry's demand signal broke — and proposing a better metric to replace it.

**[Read the full paper →](paper/Signal-vs-Noise-Paper.md)** · **[Live project site →](https://USERNAME.github.io/music-market-intelligence/)** · **[Tableau dashboards →](YOUR_TABLEAU_URL)**

---

## The question

The recorded music business grew **6.4% to US$31.7 billion in 2025** — an eleventh straight year of growth (IFPI). Yet **106,000 new tracks now arrive on streaming services every day**, **more than half of everything uploaded to Deezer is AI-generated**, and **streaming fraud drains roughly US$2 billion a year** from royalties.

The industry's binding constraint has flipped from supply to verification. Music is infinite; **trustworthy evidence of durable human demand is scarce**. Signing, playlisting, marketing, royalty payment and AI catalog licensing all depend on a signal that has become noisy, gameable, and increasingly synthetic.

**So: has the relationship between early commercial performance and durable demand actually changed — and what should companies measure instead?**

---

## What the data shows

| Finding | Then | Now |
|---|---|---|
| Top 40 hits peaking in **week one** | 0.6% (2000) | **72.7% (2024)** |
| Median **chart life** of a hit | 20 weeks (every year 1995–2017) | **7 weeks (2024)** |
| **"Slow Burn"** hits (built over time) | 72% of the market (CD era) | **26% (2018–present)** |
| Chart held by music **over a year old** | under 2% for four decades | **7.9% (2025)** |
| Artists reaching the **Top 10 for the first time** | ~50/year (1960s) | **14 (2025)** |

**And the finding that matters commercially:** across all Top 40 hits from 2018–2024, **debut chart position barely predicts how long a song lasts (r = +0.11 — and pointing the wrong way). Position at week eight carries about 3.5× the information (r = −0.38).**

Songs still holding near their peak at week eight go on to a 26-week run **48%** of the time. Songs that have collapsed do so **17%** of the time — a **2.8× separation**, available early enough to act on.

> **Recommendation: move the A&R and playlist decision gate from release-week velocity to week-8 retention.**

---

## Repository contents

```
music-market-intelligence/
├── paper/          Full research paper (Markdown + Word-ready HTML)
├── scripts/        3-step Python pipeline (standard library only)
├── data/           Data dictionary + cleaned, analysis-ready CSVs
├── tableau/        Step-by-step build guide for 4 dashboards
├── excel/          Reproduce every finding in Excel alone
├── analysis/       Findings summary and full results tables
└── docs/           Project website (GitHub Pages)
```

---

## Reproduce it in three commands

No libraries to install. No API keys. No paid accounts. Python 3 only.

```bash
python3 scripts/01_download_data.py    # fetch the public Billboard archive
python3 scripts/02_clean_data.py       # clean + validate  -> 355,087 rows
python3 scripts/03_build_kpis.py       # build the analysis tables
```

**Outputs (in `data/processed/`):**

| File | Rows | Contents |
|---|---|---|
| `yearly_kpis.csv` | 69 | The five KPIs, one row per chart year |
| `song_summary.csv` | 32,688 | Lifecycle metrics + segment, one row per song |
| `artist_summary.csv` | 8,837 | Career metrics, one row per artist |
| `chart_weeks_tableau.csv` | 191,187 | 1990-present weekly extract for Tableau |
| `cleaning_log.txt` | — | Audit trail of every cleaning decision |

Connect Tableau or Excel directly to these files. Full field definitions: **[data/DATA_DICTIONARY.md](data/DATA_DICTIONARY.md)**.

---

## Method

**Source.** Billboard Hot 100 complete weekly archive — free, public, no login, refreshed weekly: [github.com/utdata/rwd-billboard-data](https://github.com/utdata/rwd-billboard-data)

**Why chart rank.** Stream counts are not comparable across decades because the units changed — singles sold, downloads, streams. **Chart rank is a relative measure of demand within a market at a point in time**, so 1975 and 2025 stay comparable. It is also the only complete, free, login-free demand record spanning both the physical and streaming eras, which makes this analysis fully reproducible by anyone.

**The five KPIs.**

| KPI | Definition |
|---|---|
| **Debut-Peak Rate** | % of a year's Top 40 debut cohort peaking in week 1 |
| **Chart Half-Life** | Median total chart weeks for that cohort |
| **Durability Rate** | % of that cohort lasting 26+ weeks |
| **Catalog Crowding** | % of chart slots held by songs first charted 12+ months earlier |
| **Breakthrough Rate** | Artists reaching the Top 10 for the first time ever |

**The segmentation model.** Every Top 40 song is placed on speed-to-peak × longevity:

|  | Short life | Long life |
|---|---|---|
| **Fast peak** | **Spike** — attention that never converted | **Instant Standard** — launched big and held |
| **Slow peak** | **Grinder** — climbed slowly, never caught | **Slow Burn** — the classic developing hit |

**Two analytical guards, applied throughout:**
- **Right-censoring.** Songs from the two most recent years have not finished charting, so their cohorts are flagged `cohort_censored = 1` and **all trend claims stop at 2024**.
- **Artist-name parsing.** Billboard packs all credits into one text field. Splitting on `&` destroys real act names (Kool & The Gang → "Kool"; Earth, Wind & Fire → "Earth"). The pipeline splits only on explicit guest joiners — a bug found, fixed, and documented rather than hidden.

---

## Tools

| Tool | Role |
|---|---|
| **Python 3** (standard library only) | Download, clean, validate, aggregate |
| **Tableau Public** (free) | Four interactive dashboards — [build guide](tableau/TABLEAU_BUILD_GUIDE.md) |
| **Microsoft Excel** | Independent reproduction of every finding — [guide](excel/EXCEL_ANALYSIS_GUIDE.md) |
| **GitHub Pages** (free) | Project website |

Deliberately no paid tools, no cloud warehouse, and no third-party Python packages, so anyone can clone this repository and reproduce every number in it in under five minutes.

---

## Limitations

Stated up front, because they bound what the findings support:

1. The Hot 100 is a **US chart** — it says nothing about Latin America, MENA or Africa, the fastest-growing markets of 2025.
2. **Billboard changed its methodology** during the study period (streaming added 2007, video 2013, album-track rules revised ~2019–2021). The 2018 structural break coincides with the algorithmic era but is not cleanly separable from chart-policy change.
3. **Rank is relative, not absolute** — it cannot measure the long tail, which is exactly where the AI and fraud problems concentrate.
4. The week-8 analysis **conditions on survival** (n = 1,004 songs that lasted 8+ weeks).
5. The 2025 partial reversion is **unexplained** and should not be read either way until 2027 data closes it.

Full discussion in **[§7 of the paper](paper/Signal-vs-Noise-Paper.md#7-limitations)**.

---

## Sources

Industry context is drawn from IFPI's *Global Music Report 2026*, Luminate's *2025 Year-End Music Report*, Deezer's AI-upload disclosures, and reporting from Music Business Worldwide, TechCrunch, WIPO and Forbes. All 15 sources are linked in **[§10 of the paper](paper/Signal-vs-Noise-Paper.md#10-sources)**.

---

## Author

**Rebecca Wu** — classically trained musician, Master of Music, MBA candidate. Working at the intersection of **music, business and data**.

*Portfolio: [add your portfolio URL]* · *LinkedIn: [add your LinkedIn URL]*

---

## License

Code and analysis: MIT (see [LICENSE](LICENSE)). Billboard chart data remains subject to the terms of its source archive and is used here for non-commercial research. Billboard is a trademark of Billboard Media, LLC, which is not affiliated with this project.
