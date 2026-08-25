"""
03_build_kpis.py
----------------
Turns the cleaned song-week table into the three summary tables the
Tableau dashboards and the paper are built on.

OUTPUTS (all in data/processed/):
  song_summary.csv    one row per song      - lifecycle metrics + segment
  artist_summary.csv  one row per artist    - career metrics
  yearly_kpis.csv     one row per year      - the five headline KPIs

THE FIVE HEADLINE KPIs
  1. Debut-Peak Rate   % of Top 40 hits that peak in their first chart week.
                       High = demand is front-loaded into release week.
  2. Chart Half-Life   Median number of weeks a Top 40 hit stays on the chart.
                       Falling = shorter commercial life per hit.
  3. Durability Rate   % of Top 40 hits that last 26+ weeks.
  4. Catalog Crowding  % of chart slots held by songs first charted 12+
                       months ago. Rising = older music squeezes out new.
  5. Breakthrough Rate Number of artists reaching the Top 10 for the very
                       first time in that year. Falling = harder to break
                       a new artist.

Run:  python3 scripts/03_build_kpis.py
No third-party libraries required.
"""

import csv
import os
import statistics
import sys
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(HERE, "..", "data", "processed")
CLEAN = os.path.join(PROC, "chart_weeks_clean.csv")

# A song is "Fast" if it peaks within this many weeks of its debut.
FAST_PEAK_WEEKS = 2
# A song is "Long-lived" if it spends at least this many weeks on the chart.
LONG_RUN_WEEKS = 20
# Songs must reach at least this rank to enter the lifecycle analysis, so
# that one-off album tracks do not swamp the trend.
TOP40 = 40


def to_date(s):
    return date(*(int(x) for x in s.split("-")))


def segment(weeks_to_peak, total_weeks):
    """2x2 lifecycle segment: speed-to-peak x longevity."""
    fast = weeks_to_peak <= FAST_PEAK_WEEKS
    long_lived = total_weeks >= LONG_RUN_WEEKS
    if fast and not long_lived:
        return "Spike (fast peak, short life)"
    if fast and long_lived:
        return "Instant Standard (fast peak, long life)"
    if not fast and long_lived:
        return "Slow Burn (built over time, long life)"
    return "Grinder (slow climb, short life)"


def main():
    if not os.path.exists(CLEAN):
        sys.exit("Clean file not found. Run: python3 scripts/02_clean_data.py")

    with open(CLEAN, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["d"] = to_date(r["chart_week"])
        r["rank"] = int(r["rank"])
        r["chart_year"] = int(r["chart_year"])

    # ---------------------------------------------------------------- songs
    weeks_by_song = defaultdict(list)
    for r in rows:
        weeks_by_song[r["song_key"]].append(r)

    songs = {}
    for key, weeks in weeks_by_song.items():
        weeks.sort(key=lambda r: r["d"])
        peak = min(r["rank"] for r in weeks)
        weeks_to_peak = next(i for i, r in enumerate(weeks) if r["rank"] == peak) + 1
        total = len(weeks)
        songs[key] = {
            "song_key": key,
            "title": weeks[0]["title"],
            "performer": weeks[0]["performer"],
            "primary_artist": weeks[0]["primary_artist"],
            "is_collaboration": weeks[0]["is_collaboration"],
            "is_holiday_song": weeks[0]["is_holiday_song"],
            "debut_date": weeks[0]["chart_week"],
            "debut_year": weeks[0]["chart_year"],
            "debut_decade": weeks[0]["chart_decade"],
            "era": weeks[0]["era"],
            "debut_rank": weeks[0]["rank"],
            "peak_position": peak,
            "weeks_to_peak": weeks_to_peak,
            "debut_is_peak": 1 if weeks_to_peak == 1 else 0,
            "total_weeks_on_chart": total,
            "weeks_in_top10": sum(1 for r in weeks if r["rank"] <= 10),
            "weeks_at_number_one": sum(1 for r in weeks if r["rank"] == 1),
            "last_chart_date": weeks[-1]["chart_week"],
            "chart_span_weeks": round((weeks[-1]["d"] - weeks[0]["d"]).days / 7) + 1,
            "reached_top40": 1 if peak <= TOP40 else 0,
            "lifecycle_segment": segment(weeks_to_peak, total),
        }
        # A re-entry gap means the song left the chart and came back.
        songs[key]["had_reentry"] = (
            1 if songs[key]["chart_span_weeks"] > total else 0
        )

    write_csv(os.path.join(PROC, "song_summary.csv"), sorted(
        songs.values(), key=lambda s: (s["debut_date"], s["peak_position"])))

    # -------------------------------------------------------------- artists
    by_artist = defaultdict(list)
    for s in songs.values():
        by_artist[s["primary_artist"]].append(s)

    weeks_by_artist = defaultdict(int)
    for r in rows:
        weeks_by_artist[r["primary_artist"]] += 1

    artists = []
    for name, s_list in by_artist.items():
        debuts = sorted(s["debut_date"] for s in s_list)
        lasts = sorted(s["last_chart_date"] for s in s_list)
        artists.append({
            "primary_artist": name,
            "first_chart_date": debuts[0],
            "first_chart_year": int(debuts[0][:4]),
            "last_chart_date": lasts[-1],
            "career_span_years": round(
                (to_date(lasts[-1]) - to_date(debuts[0])).days / 365.25, 1),
            "charted_songs": len(s_list),
            "top10_songs": sum(1 for s in s_list if s["peak_position"] <= 10),
            "number_one_songs": sum(1 for s in s_list if s["peak_position"] == 1),
            "total_chart_weeks": weeks_by_artist[name],
            "best_peak_position": min(s["peak_position"] for s in s_list),
            "avg_weeks_per_song": round(
                statistics.mean(s["total_weeks_on_chart"] for s in s_list), 1),
        })
    write_csv(os.path.join(PROC, "artist_summary.csv"), sorted(
        artists, key=lambda a: -a["total_chart_weeks"]))

    # ---------------------------------------------------- first Top 10 year
    first_top10 = {}
    for r in sorted(rows, key=lambda r: r["d"]):
        if r["rank"] <= 10:
            first_top10.setdefault(r["primary_artist"], r["chart_year"])
    breakthroughs = defaultdict(int)
    for year in first_top10.values():
        breakthroughs[year] += 1

    # --------------------------------------------------------- yearly KPIs
    rows_by_year = defaultdict(list)
    for r in rows:
        rows_by_year[r["chart_year"]].append(r)

    debut_lookup = {k: to_date(s["debut_date"]) for k, s in songs.items()}

    # RIGHT-CENSORING GUARD.
    # A song that is still climbing the chart on the last day of the dataset
    # has not finished its run, so its cohort's half-life and durability are
    # biased downwards. Any year whose cohort still has songs on the final
    # chart is flagged so it can be excluded from trend claims.
    # The rule is deliberately simple and stated in the paper: the two most
    # recent chart years are treated as incomplete. (Testing "does any song
    # from this year still chart?" instead flags stray years like 1996, where
    # a single seasonal re-entry returned decades later.)
    last_chart_day = max(r["d"] for r in rows)
    still_charting_years = {last_chart_day.year, last_chart_day.year - 1}

    yearly = []
    for year in sorted(rows_by_year):
        yr_rows = rows_by_year[year]
        slots = len(yr_rows)
        # Top 40 songs that DEBUTED this year drive the lifecycle KPIs.
        cohort = [s for s in songs.values()
                  if s["debut_year"] == year and s["reached_top40"]]
        old_slots = sum(
            1 for r in yr_rows
            if (r["d"] - debut_lookup[r["song_key"]]).days > 365)

        yearly.append({
            "chart_year": year,
            "chart_weeks_in_year": len({r["chart_week"] for r in yr_rows}),
            # 1 = this year's songs have not finished charting yet, so its
            #     lifecycle KPIs are incomplete. Exclude from trend claims.
            "cohort_censored": 1 if year in still_charting_years else 0,
            "chart_slots": slots,
            "unique_songs": len({r["song_key"] for r in yr_rows}),
            "new_song_debuts": len({s["song_key"] for s in songs.values()
                                    if s["debut_year"] == year}),
            "top40_debut_cohort": len(cohort),
            # KPI 1
            "kpi_debut_peak_rate_pct": pct(
                sum(s["debut_is_peak"] for s in cohort), len(cohort)),
            # KPI 2
            "kpi_chart_half_life_weeks": (
                round(statistics.median(s["total_weeks_on_chart"] for s in cohort), 1)
                if cohort else ""),
            # KPI 3
            "kpi_durability_rate_pct": pct(
                sum(1 for s in cohort if s["total_weeks_on_chart"] >= 26), len(cohort)),
            # KPI 4
            "kpi_catalog_crowding_pct": pct(old_slots, slots),
            # KPI 5
            "kpi_breakthrough_artists": breakthroughs.get(year, 0),
            "avg_weeks_on_chart_per_slot": round(
                statistics.mean(int(r["weeks_on_chart"]) for r in yr_rows), 1),
            "pct_slots_20wk_plus": pct(
                sum(1 for r in yr_rows if int(r["weeks_on_chart"]) > 20), slots),
            "pct_slots_52wk_plus": pct(
                sum(1 for r in yr_rows if int(r["weeks_on_chart"]) > 52), slots),
            "distinct_number_ones": len({r["song_key"] for r in yr_rows if r["rank"] == 1}),
            "pct_slots_collaboration": pct(
                sum(1 for r in yr_rows if r["is_collaboration"] == "1"), slots),
            "pct_slots_holiday": pct(
                sum(1 for r in yr_rows if r["is_holiday_song"] == "1"), slots),
        })
    write_csv(os.path.join(PROC, "yearly_kpis.csv"), yearly)

    # ------------------------------------------------- Tableau weekly extract
    # chart_weeks_clean.csv is ~55 MB, which is too large to keep in a Git
    # repository. This trimmed 1990-present extract holds the columns the
    # dashboards actually use and is small enough to commit.
    keep_cols = ["chart_week", "chart_year", "era", "title", "primary_artist",
                 "performer", "rank", "weeks_on_chart", "peak_position_to_date",
                 "is_top10", "is_number_one", "is_holiday_song"]
    extract = [{c: r[c] for c in keep_cols} for r in rows if r["chart_year"] >= 1990]
    write_csv(os.path.join(PROC, "chart_weeks_tableau.csv"), extract)

    print(f"chart_weeks_tableau.csv {len(extract):>7,} rows (1990-present)")
    print(f"song_summary.csv    {len(songs):>7,} rows")
    print(f"artist_summary.csv  {len(artists):>7,} rows")
    print(f"yearly_kpis.csv     {len(yearly):>7,} rows")
    print(f"\nWritten to {os.path.normpath(PROC)}")
    print("These four CSVs are what you connect Tableau to.")


def pct(numerator, denominator):
    return round(100 * numerator / denominator, 1) if denominator else ""


def write_csv(path, records):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
