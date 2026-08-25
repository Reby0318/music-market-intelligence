# Signal vs. Noise
### Quantifying the Discovery Bottleneck in the Streaming Era, and What the Industry Should Measure Instead

**Author:** Rebecca Wu
**Date:** August 2026
**Repository:** https://github.com/Reby0318/music-market-intelligence
**Data:** Billboard Hot 100, 355,087 song-weeks, 4 Aug 1958 – 22 Aug 2026
**Tools:** Python (standard library only), Microsoft Excel, Tableau Public

---

## Executive Summary

The recorded music business is growing — global revenues reached **US$31.7 billion in 2025, up 6.4%, an eleventh consecutive year of growth** (IFPI, 2026). Yet the companies inside it are struggling with a problem that revenue growth conceals: **the industry's binding constraint has flipped from supply to verification.**

Producing and distributing music is now effectively free and effectively infinite. **106,000 new tracks reach streaming services every day**; the catalog has grown from 202 million to **253 million tracks in a single year**, and **120.5 million of those tracks earned ten streams or fewer in all of 2025** (Luminate, 2026). Meanwhile more than **half of everything uploaded to Deezer each day is now fully AI-generated** — roughly 90,000 tracks — and **85% of the streams those tracks attract are detected as fraudulent** (Deezer, 2026). The IFPI estimates streaming fraud drains close to **US$2 billion a year** from global royalties.

What is scarce is no longer music. What is scarce is **trustworthy evidence of durable human demand.** Every consequential decision in the industry — what to sign, what to playlist, what to market, what to pay out, what catalog to license to an AI model — rests on a demand signal that has become noisy, gameable, and increasingly synthetic.

This paper measures how far that signal has degraded, using the one continuous, free, public record of ranked consumer demand that spans both the physical and streaming eras: 68 years of the Billboard Hot 100.

**Five findings:**

1. **Hits now arrive pre-peaked.** The share of Top 40 hits that peak in their very first chart week rose from **0.6% in 2000 to 72.7% in 2024**. Release week is no longer the start of a story; it is the whole story.
2. **Commercial life has collapsed.** Median chart run for a Top 40 hit held rock-steady at **20 weeks for 23 consecutive years (1995–2017)**, then fell to **7 weeks by 2024** — a 65% reduction.
3. **The middle of the market has been hollowed out.** The classic "Slow Burn" hit — built over time, long-lived — fell from **72% of Top 40 songs in the CD era to 26% since 2018**, while the "Spike" (fast peak, short life) grew from **0.5% to 55.6%**.
4. **Older music is crowding out new music.** Chart slots held by songs that first charted 12+ months earlier ran below 2% for four decades; they reached **7.9% in 2025**. In December 2025, **21.2% of the chart was held by songs at least five years old**.
5. **Breaking a new artist is getting harder.** Artists reaching the Top 10 for the first time fell to **14 in 2025**, the lowest count since 2010–2011, against a 1960s baseline of ~50.

**The actionable result:** the metric the industry leans on hardest is the one that predicts least. Across all Top 40 hits from 2018–2024, **debut chart position has almost no relationship to how long a song ultimately lasts (r = +0.11 — and pointing the wrong way). Position at week eight is roughly three and a half times more informative (r = −0.38).** Songs still holding near their early peak at week eight go on to have a 26-week run **48% of the time; those that have collapsed do so only 17% of the time — a 2.8× difference.**

**Recommendation:** shift the primary evaluation metric from *release-week velocity* to *post-peak retention*. This paper proposes a **Week-8 Retention Ratio**, a segmentation model, and a Tableau decision dashboard that operationalise the shift for A&R, playlist, and catalog-acquisition teams.

---

## 1. The Problem the Industry Actually Needs to Solve

### 1.1 The market is healthy; the signal is not

It is easy to look at headline numbers and conclude nothing is wrong. Paid subscription streaming grew 8.8% in 2025 and now accounts for 52.4% of all recorded music revenue, with 837 million paid subscription accounts worldwide. Every region grew, four of them by double digits, led by Latin America at +17.1% (IFPI, 2026).

But underneath, the mechanics of how value is discovered and assigned have broken down in four connected ways.

### 1.2 Problem one: supply has become infinite, attention has not

Luminate's 2025 year-end data describes a market that has stopped functioning as a marketplace at the tail:

| Measure | 2024 | 2025 |
|---|---|---|
| Tracks available (ISRCs) | 202 million | **253 million** |
| New tracks per day | ~99,000 | **~106,000** |
| Tracks with 0–10 streams all year | — | **120.5 million (≈48%)** |
| Tracks with fewer than 1,000 streams | — | **88%** |
| Tracks above 1 billion streams | — | **29** |
| On-demand audio streams | 4.8 trillion | **5.1 trillion (+9.6%)** |

Half the catalog is commercially inert. Nearly all the value sits in a narrow band: tracks between 1 million and 50 million streams account for **49.4%** of all streaming. And most tellingly, **streaming of *current* music — releases 18 months old or newer — actually declined 1.6% in 2025** even as total streaming grew nearly 10%. Growth is coming from catalog, not from new music.

### 1.3 Problem two: a growing share of the signal is not human

Deezer began publishing AI-upload detection data in 2025, and the trajectory is the single most striking statistic in the industry:

| Date | AI-generated tracks uploaded per day | Share of all uploads |
|---|---|---|
| Early 2025 | ~10,000 | ~10% |
| April 2026 | ~75,000 | **44%** |
| July 2026 | ~90,000 | **>50%** |

Crucially, Deezer reports that AI tracks account for only **1–3% of actual streams**, and that **85% of those streams are detected as fraudulent and demonetised**. The purpose of most of this content is not to be listened to. It is to harvest royalties.

### 1.4 Problem three: fraud is a structural tax, not an edge case

Because streaming royalties are paid from a fixed monthly pool, every fraudulent stream is a direct transfer away from legitimate rightsholders. The IFPI puts the leakage at close to **US$2 billion annually**; the Music Fights Fraud Alliance estimates that **nearly 10% of all streams are fraudulent**. In one 2024 US case, a musician was indicted for using AI-generated songs and bot networks to extract over **US$10 million** in royalties.

Platforms have responded with blunt instruments. Spotify's royalty model change, live since **1 April 2024**, demonetises any track with fewer than 1,000 streams in a rolling 12 months, redirecting roughly **US$40 million a year** back into the pool, and charges labels and distributors a per-track monthly penalty where artificial streaming is detected. The policy is defensible as fraud deterrence, but it also **withholds royalties from the ~87% of tracks that never reach the threshold**, most of which are legitimate niche and emerging artists. This is what a broken verification layer forces: platforms cannot cheaply tell real small artists from fake ones, so they treat both the same.

### 1.5 Problem four: the AI licensing settlement makes signal quality a balance-sheet issue

The 2025–2026 wave of settlements changed the question from *whether* AI models may train on catalog to *what that catalog is worth*. Universal settled with Udio in October 2025; Warner settled with Suno in a first-of-its-kind deal under which Suno replaces its models with licensed versions during 2026. Sony's claims against Udio remain live, and Universal and Sony's case against Suno was still unresolved as of April 2026.

Licensing deals require valuing catalog. Valuing catalog requires knowing which recordings command **durable** demand rather than transient or manufactured attention. The verification problem is now priced into transactions.

### 1.6 The problem, stated precisely

> **The music industry's critical unsolved problem is that its demand signal no longer reliably distinguishes durable human fandom from transient, manufactured, or synthetic attention — and nearly every commercial decision in the business depends on that distinction.**

This is upstream of the fraud problem, the discovery problem, the artist-development problem, and the AI-valuation problem. It is the problem this project attacks.

---

## 2. Research Question and Hypothesis

**Research question.** Has the relationship between early commercial performance and durable demand changed measurably over time, and if so, what should companies measure instead?

**Hypothesis (H1).** In the algorithmic era, demand for new music has become *front-loaded*: songs arrive at their commercial peak immediately and decay quickly, so early performance metrics have lost predictive power over a song's ultimate value.

**Hypothesis (H2).** As the value of new releases has become harder to establish, consumption has shifted toward proven catalog, measurably crowding new music off the chart.

**Why the Hot 100 is the right instrument.** Stream counts are not comparable across decades — the units changed. **Chart rank is a relative measure of demand within a market at a point in time**, so 1975 and 2025 remain comparable. It is also the only complete, free, login-free demand record covering both eras, which makes this analysis fully reproducible by anyone.

---

## 3. Data and Method

### 3.1 Source

| | |
|---|---|
| Dataset | Billboard Hot 100, complete weekly archive |
| Provider | Public archive maintained at `github.com/utdata/rwd-billboard-data` |
| Coverage | 4 Aug 1958 – 22 Aug 2026 (3,551 weekly charts) |
| Volume | 355,100 raw song-week rows |
| Access | Free, public, no account or API key; refreshed weekly |

### 3.2 Cleaning

A three-script Python pipeline using **only the standard library**, so it runs on any machine with no installation:

| Script | Function |
|---|---|
| `01_download_data.py` | Retrieves the raw archive |
| `02_clean_data.py` | Cleans, validates, enriches → `chart_weeks_clean.csv` |
| `03_build_kpis.py` | Builds song, artist and yearly summary tables |

Cleaning steps: whitespace and apostrophe normalisation; conversion of Billboard's literal `"NA"` to true blanks (32,460 rows); date parsing and derivation of year, month, decade and era; range validation of ranks (1–100) and tenure (≥1); removal of exact duplicates (**13 rows**); separation of guest credits from lead credits; and seasonal-title flagging.

**Result: 355,087 clean rows, 32,688 unique songs, 8,837 unique primary artists.** A machine-written audit trail is saved to `cleaning_log.txt`.

One cleaning decision deserves emphasis, because getting it wrong silently corrupts every artist-level number. Billboard packs all credits into one free-text field. Splitting that field on `&` or `,` — the obvious approach — destroys legitimate act names: Kool & The Gang becomes "Kool", Earth, Wind & Fire becomes "Earth", Florence + The Machine becomes "Florence". The pipeline therefore splits **only** on explicit guest joiners (`Featuring`, `Feat.`, `With`, `Duet With`, `Introducing`, `Presents`, `vs.`), accepting that a genuine duo billing is counted as one act. This error was caught by inspecting the top of the artist table and is documented in §7.

### 3.3 The five KPIs

| KPI | Definition | Reads as |
|---|---|---|
| **1. Debut-Peak Rate** | % of a year's Top 40 debut cohort peaking in week 1 | How front-loaded demand is |
| **2. Chart Half-Life** | Median total chart weeks for that cohort | How long a hit stays commercially alive |
| **3. Durability Rate** | % of that cohort lasting 26+ weeks | How often a hit becomes an asset |
| **4. Catalog Crowding** | % of chart slots held by songs first charted 12+ months earlier | How far catalog displaces new music |
| **5. Breakthrough Rate** | Count of artists reaching the Top 10 for the first time ever | How permeable the market is to newcomers |

KPIs 1–3 are **cohort** measures (they follow songs that debuted in a given year). KPIs 4–5 are **within-year** measures. This distinction matters for censoring, below.

### 3.4 Segmentation model

Every Top 40 song is placed in a 2×2 on speed-to-peak (fast = peaked within 2 weeks) against longevity (long = 20+ weeks on chart):

|  | **Short life** | **Long life** |
|---|---|---|
| **Fast peak** | **Spike** — release-week attention that never converted | **Instant Standard** — launched big and held; rarest and most valuable |
| **Slow peak** | **Grinder** — climbed slowly, never caught | **Slow Burn** — audience built over time; the classic developing hit |

### 3.5 Right-censoring guard

A song still climbing the chart on the dataset's last day has not finished its run, which biases its cohort's half-life and durability downward. The pipeline flags the two most recent chart years (`cohort_censored = 1`) and **all trend claims in this paper stop at 2024.** 2025 and 2026 figures are shown for completeness and marked provisional. Note that this affects KPIs 1–3 only; KPIs 4 and 5 are complete for 2025 (a full 52-week year) and partial for 2026 (34 weeks).

---

## 4. Findings

### 4.1 Finding 1 — Hits now arrive pre-peaked

| Year | Debut-Peak Rate | Chart Half-Life | Durability Rate |
|---|---|---|---|
| 1985 | 0.0% | 17.5 wks | 1.9% |
| 1995 | 5.1% | 20 wks | 31.2% |
| 2000 | 0.6% | 20 wks | 22.3% |
| 2005 | 5.6% | 20 wks | 26.9% |
| 2010 | 33.5% | 20 wks | 21.3% |
| 2015 | 18.3% | 21 wks | 40.5% |
| 2017 | 26.6% | 21 wks | 35.0% |
| **2018** | **53.9%** | **15 wks** | 24.2% |
| 2020 | 63.5% | 13 wks | 15.5% |
| 2022 | 69.6% | 10 wks | 16.9% |
| 2023 | 69.9% | 8 wks | 13.3% |
| **2024** | **72.7%** | **7 wks** | 19.1% |
| *2025 (provisional)* | *55.7%* | *17 wks* | *28.1%* |

There is a clear structural break at **2018**. Before it, most hits climbed; after it, most hits land. By 2024, **almost three in four Top 40 hits never rose above their first week.**

The chart half-life result is the most striking, because of how stable the baseline was: **20 weeks every single year from 1995 to 2017**, through the CD boom, the Napster collapse, the iTunes era and the arrival of streaming. Then it fell to 7 weeks in six years.

The two findings together describe a market in which a song's commercial life is compressed into its launch, and everything after launch is decay.

### 4.2 Finding 2 — The developing hit has been hollowed out

Lifecycle segment mix of Top 40 songs by era:

| Era | Spike | Instant Standard | Slow Burn | Grinder |
|---|---|---|---|---|
| Physical / Airplay (pre-1991) | 0.5% | 0.0% | 14.6% | 84.9% |
| Soundscan CD (1991–2004) | 2.5% | 2.0% | **72.1%** | 23.4% |
| Download & Early Streaming (2005–2013) | 17.3% | 7.1% | 62.7% | 12.9% |
| Streaming Majority (2014–2017) | 19.1% | 5.3% | 67.1% | 8.4% |
| **Algorithmic / Social (2018–present)** | **55.6%** | 12.1% | **26.4%** | 5.9% |

The Slow Burn — a song that finds its audience over weeks and then holds it — was the *dominant* form of hit for a quarter century. It is now a minority case, displaced by the Spike.

One nuance worth reporting honestly: **Instant Standards more than doubled** (5.3% → 12.1%). The modern market has not only got worse. It has become **bimodal**. A small number of releases now launch enormously *and* hold — the longest chart runs in Hot 100 history are almost all recent: *Lose Control* (Teddy Swims, 112 weeks), *Heat Waves* (Glass Animals, 91), *Blinding Lights* (The Weeknd, 90), *Beautiful Things* (Benson Boone, 89). Meanwhile the majority spike and vanish. What has disappeared is the **middle**: the ordinary developing hit that used to be the industry's training ground for building careers.

### 4.3 Finding 3 — Catalog is crowding out new music

| Year | Chart slots held by songs 12+ months old |
|---|---|
| 1995 | 0.3% |
| 2005 | 0.1% |
| 2010 | 2.1% |
| 2015 | 0.7% |
| 2020 | 2.2% |
| 2022 | 6.4% |
| 2023 | 5.8% |
| 2024 | 5.1% |
| **2025** | **7.9%** |

For four decades this number was effectively zero — songs left the chart and did not return. Since 2021 it has moved into the 5–8% range.

The seasonal effect makes the mechanism visible. Share of the December chart held by songs at least **five years old**:

| December | 1995 | 2005 | 2015 | 2020 | 2023 | 2024 | **2025** |
|---|---|---|---|---|---|---|---|
| Share | 0.0% | 0.0% | 0.8% | 7.2% | 13.4% | 15.5% | **21.2%** |

Every December, more than a fifth of the US singles chart is now occupied by decades-old recordings. This is not a change in taste; it is a change in **plumbing**. On-demand access plus algorithmic and playlist reinforcement means proven catalog re-enters and holds — space that new releases used to occupy. It is the chart-level expression of Luminate's finding that current-music streaming *declined* 1.6% in a year when total streaming grew 9.6%.

### 4.4 Finding 4 — Fewer artists are breaking through

Artists reaching the Top 10 for the first time in their careers:

| Year | 1965 | 1975 | 1985 | 1995 | 2005 | 2015 | 2020 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| First-time Top 10 acts | 52 | 50 | 36 | 28 | 27 | 17 | 27 | 22 | 23 | **14** |

The long-run decline is partly structural — the chart itself became less permeable as tenure lengthened. But **14 in 2025 is the lowest figure since 2010–2011**, and it sits alongside the highest catalog-crowding reading in the series. Fewer slots turn over, so fewer newcomers get in. The number of distinct #1 songs tells the same story: **10 in 2025**, against 27 in 1965 and 35 in 1975.

### 4.5 Finding 5 — The metric the industry trusts most predicts least

If demand is front-loaded, the practical question becomes: **which early signal actually forecasts durability?**

Testing every Top 40 song that debuted between 2018 and 2024 and survived at least eight weeks (n = 1,004), correlating chart position in each early week against eventual total chart run:

| Early signal | Correlation with total chart run |
|---|---|
| **Debut rank (week 1)** | **+0.107** |
| Rank at week 2 | +0.016 |
| Rank at week 4 | −0.149 |
| Rank at week 6 | −0.294 |
| **Rank at week 8** | **−0.380** |

Because rank is inverted (1 is best), a negative correlation is the intuitive one: a better position predicts a longer run. **Debut rank's correlation is not merely weak, it is positive — a stronger debut is very slightly associated with a *shorter* life.** Debut position is close to noise. Week-8 position carries roughly **three and a half times** the information, in the correct direction.

Turning this into a decision rule, define the **Week-8 Retention Ratio** = *(rank at week 8) ÷ (best rank achieved in weeks 1–4)*. A ratio near 1.0 means a song is holding its peak; 5.0 means it has fallen to a fifth of its early standing.

| Retention quintile | Ratio range | Median total run | Reached 26+ weeks |
|---|---|---|---|
| 1 (holding) | 0.07 – 0.74 | 25 wks | **48%** |
| 2 | 0.74 – 1.08 | 25 wks | 45% |
| 3 | 1.08 – 2.00 | 21 wks | 36% |
| 4 | 2.00 – 4.33 | 19 wks | 19% |
| 5 (collapsing) | 4.38 – 70.00 | 18 wks | **17%** |

A song in the top retention quintile is **2.8× more likely** to become a durable, 26-week asset than one in the bottom quintile. That is a decision-grade separation available **eight weeks after release** — early enough to reallocate marketing spend, playlist pitches, and tour and sync investment.

---

## 5. Interpretation: The Discovery Bottleneck

The five findings describe one mechanism.

**Distribution became free, so supply became infinite** — 106,000 tracks a day, half of them now machine-generated. **Discovery became algorithmic**, and algorithms reward immediate engagement, so promotional effort concentrated into release week. **Release-week concentration produced front-loaded demand curves** — 72.7% of hits peaking on debut — which **destroyed the informational content of early metrics**. With early signals unreliable and new releases decaying in weeks, **capital rationally retreated to proven catalog**, which now holds 7.9% of chart slots year-round and 21.2% of the December chart. Catalog occupying the chart **leaves fewer slots for newcomers** — 14 first-time Top 10 acts in 2025.

This is a bottleneck, not a decline. Demand is healthy; revenues grew 6.4%. What has failed is the **matching layer** between infinite supply and finite attention. And a matching layer that cannot verify demand is exactly the environment in which stream farms and AI upload floods flourish: they exploit the fact that nobody can cheaply tell a real emerging artist from a manufactured one.

Seen this way, the industry's separate crises are one crisis. Fraud detection, AI-content labelling, artist development, playlist strategy, and catalog valuation are all applications of the same missing capability: **measuring durable human demand.**

---

## 6. Strategic Recommendations

### 6.1 For streaming platforms (Spotify, Apple Music, Amazon Music, YouTube Music, Deezer)

1. **Replace release-week velocity with retention in editorial decisioning.** Playlist performance review at week 8, using a retention ratio rather than a raw stream count, separates durable from transient at 2.8× resolution. Applied to editorial slots, this reduces the churn that trains listeners to expect disposable music.
2. **Make retention the fraud filter, not volume.** A 1,000-stream threshold penalises the 87% of legitimate tracks below it. Retention shape — whether listening persists, repeats, and comes from returning listeners — is far harder to fake cheaply than raw volume, and does not tax small legitimate artists.
3. **Label AI-generated content and report it as a distinct consumption category.** Deezer already tags it and reports 1–3% of streams. Making that disclosure standard turns an existential unknown into a manageable, measured line item, and gives licensors a basis for pricing.
4. **Price the superfan tier on retention data, not on hope.** Spotify's own data shows ~2% of an artist's listeners drive 18% of streams, yet the "Music Pro" tier has stalled on product definition. Retention segmentation identifies exactly who those listeners are and what they persist with — the necessary input for a tier that has so far been defined by perks rather than by evidence.

### 6.2 For major labels (Universal, Sony, Warner)

1. **Move the A&R decision gate from week 1 to week 8.** Signing and marketing escalation triggered by debut performance is triggered by noise (r = +0.11). Rebuild the gate on retention. This is a scheduling change, not a technology purchase.
2. **Budget explicitly against the Spike.** If 55.6% of Top 40 songs are now Spikes and only 12.1% are Instant Standards, marketing plans that assume a long tail are mispriced for the majority of releases. Model the two outcomes separately.
3. **Rebuild the middle of the funnel.** The Slow Burn's fall from 72% to 26% removed the development path that produced durable careers. Artist development now has to be *funded* deliberately, because the market no longer produces it as a by-product.
4. **Use durability, not volume, to price AI licensing and catalog acquisition.** With the Suno and Udio settlements moving toward licensed models in 2026, catalog valuation is live commercial work. Durability metrics — retention, re-entry behaviour, seasonal persistence — describe which recordings hold value; cumulative stream counts, inflated by an era of fraud, do not.

### 6.3 For independent artists, managers, and distributors

1. **Stop optimising for release day.** The evidence says debut position carries almost no information about outcomes. Concentrating an entire budget into week 1 buys the least predictive part of the curve.
2. **Hold budget for weeks 4–12.** That is where the separation between a 48% and a 17% chance of durability actually becomes visible, and where reallocating spend can still change the outcome.
3. **Treat catalog as an asset with a season.** With 21.2% of the December chart held by five-year-old songs, seasonal and evergreen re-marketing of existing recordings is a higher-return activity than it was even five years ago.

### 6.4 For AI music platforms (Suno, Udio, and licensed successors)

1. **Adopt provenance labelling before it is imposed.** Deezer's tagging has turned "how much of this is AI?" from an unanswerable question into a reported statistic. Voluntary provenance is the cheapest available route to platform trust.
2. **Compete on retention, not on upload volume.** 90,000 uploads a day producing 1–3% of streams, 85% of it flagged fraudulent, is not a demand signal — it is a cost centre for everyone in the chain, including the generators.

---

## 7. Limitations

Stated plainly, because they bound what these findings support.

1. **The Hot 100 is a US chart.** Findings describe the US market. The fastest-growing markets in 2025 were Latin America (+17.1%), MENA (+15.2%) and Sub-Saharan Africa (+15.2%), and this dataset says nothing about them.
2. **Billboard's methodology changed during the study period.** Streaming entered the formula in 2007, on-demand and video weighting in 2013, and rules limiting how many tracks from one album may chart simultaneously were revised around 2019–2021. **The 2018 structural break coincides with the algorithmic era but is not cleanly separable from chart-policy change.** The direction and magnitude of the trend are robust; the exact break year is not attributable to consumer behaviour alone.
3. **Rank is relative, not absolute.** The chart shows demand *ranking*, not demand *volume*. It cannot measure the long tail — which is precisely where the AI and fraud problems concentrate. External sources are used for that layer.
4. **Duo billings are counted as one act.** Splitting on `&` would corrupt band names (§3.2), so "Post Malone & Swae Lee" is one act here. This slightly understates collaboration counts and breakthrough counts, since an artist first appearing via a shared billing is not counted separately.
5. **The week-8 analysis conditions on survival.** Only songs that lasted at least eight weeks can be measured at week eight (n = 1,004), so the correlations describe songs that survived, not all releases. The effect on non-survivors is likely larger, not smaller.
6. **The 2025 partial reversion is unexplained.** Debut-Peak Rate fell to 55.7% and half-life rose to 17 weeks in 2025. As a censored cohort, this may be an artefact; it may also be a genuine turn. It should not be read either way until 2027 data closes it.
7. **Correlation is not causation.** Week-8 retention predicts durability; it does not establish what causes durability.

---

## 8. Future Work

1. **Add a global layer.** The Spotify Top 50 daily charts for 73 countries (Kaggle, free) would test whether front-loading is a US phenomenon or a platform-wide one, and add audio features.
2. **Model AI-content share directly** as Deezer-style provenance data becomes available, and test whether it changes retention distributions.
3. **Build a live scoring tool.** The Week-8 Retention Ratio is simple enough to run weekly in Excel against new chart data and flag which current entries are tracking toward durability.
4. **Validate against revenue.** Chart durability is a proxy for value. Pairing it with royalty or sync-licensing data would convert it into a financial forecasting metric.

---

## 9. Conclusion

The recorded music industry is growing and simultaneously losing its ability to tell what is working. Sixty-eight years of chart data show a market that has moved from *building* hits to *launching* them: 72.7% of Top 40 hits now peak in week one, their median commercial life has fallen from 20 weeks to 7, and the developing hit that once made up 72% of the market now makes up 26%. In its place, proven catalog has taken 7.9% of the chart year-round and over a fifth of it each December, while the number of artists breaking into the Top 10 fell to 14 in 2025.

Against that backdrop, 106,000 new tracks a day and an upload stream that is now more than half machine-generated are not the disease. They are what happens when the cost of supply falls to zero and no reliable verification layer exists.

The industry's most valuable unsolved problem is measurement: **separating durable human demand from manufactured attention.** This analysis shows that the separation is achievable with data companies already hold, that the metric currently relied on is close to noise, and that a better one is available eight weeks after release with a 2.8× lift in predictive power.

The scarce resource is no longer music. It is proof that anyone actually wants it.

---

## 10. Sources

**Primary data**
- Billboard Hot 100 complete weekly archive — https://github.com/utdata/rwd-billboard-data

**Industry data and reporting**
- IFPI, *Global Music Report 2026* — https://www.ifpi.org/global-music-report-2026-global-recorded-music-revenues-grow-6-4-as-record-companies-drive-innovation/
- Music Business Worldwide, "Global recorded music revenues hit $31.7B in 2025, up 6.4% YoY; paid subscriptions reach 837M" — https://www.musicbusinessworldwide.com/global-recorded-music-revenues-hit-31-7bn-in-2025-up-6-4-yoy-users-of-paid-music-subscriptions-reach-837m/
- Luminate, *2025 Year-End Music Report* — https://luminatedata.com/reports/yearend-music-industry-report-2025/
- Music Ally, "5.1tn annual music streams… but 120.5m tracks had 10 or fewer" — https://musically.com/2026/01/15/5-1tn-annual-music-streams-but-120-5m-tracks-had-10-or-fewer/
- Deezer Newsroom, "AI music tops 50% of daily uploads" (July 2026) — https://newsroom-deezer.com/2026/07/ai-music-exceeds-50-percent-daily-uploads-deezer/
- Deezer Newsroom, "AI-generated tracks represent 44% of new uploaded music" (April 2026) — https://newsroom-deezer.com/2026/04/ai-generated-tracks-represent-44-of-new-uploaded-music/
- TechCrunch, "Music streamer Deezer says more than 50% of daily uploads are AI-generated" — https://techcrunch.com/2026/07/21/music-streamer-deezer-says-more-than-50-of-daily-uploads-are-ai-generated/
- WIPO Magazine, "How AI-generated songs are fueling the rise of streaming farms" — https://www.wipo.int/en/web/wipo-magazine/articles/how-ai-generated-songs-are-fueling-the-rise-of-streaming-farms-74310
- Forbes, "How AI-Generated Music Became A $4 Billion Fraud Machine" — https://www.forbes.com/sites/virginieberger/2026/05/05/how-ai-generated-music-became-a-4-billion-fraud-machine/
- Music Business Worldwide, "Changes to Spotify's royalty model, including the 1,000 annual streams policy, are officially live" — https://www.musicbusinessworldwide.com/changes-to-spotifys-royalty-model-including-the-1000-annual-streams-royalty-policy-are-officially-live/
- Spotify for Artists, *Royalties Guide* — https://artists.spotify.com/royalties-guide
- Music Business Worldwide, "Warner Music Group strikes 'landmark' deal with Suno" — https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/
- Music Business Worldwide, "Spotify to launch 'Music Pro' service with superfan perks" — https://www.musicbusinessworldwide.com/spotify-to-launch-music-pro-service-with-superfan-perks-like-early-access-tickets-and-ai-remix-tool-for-up-to-5-99-more-per-month-report/
- Music Business Worldwide, "Quarter of a billion tracks now sit on music streaming services" — https://www.musicbusinessworldwide.com/quarter-of-a-billion-tracks-now-sit-on-music-streaming-services-where-does-it-end/

---

*All figures derived from the Hot 100 in this paper are reproducible by running the three scripts in `/scripts` against the public source data. Analysis code and cleaned datasets: `github.com/Reby0318/music-market-intelligence`.*
