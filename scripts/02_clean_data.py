"""
02_clean_data.py
----------------
Cleans the raw Billboard Hot 100 archive and writes an analysis-ready
"one row per song-week" table.

CLEANING DECISIONS (all documented in data/DATA_DICTIONARY.md):
  1. Trim whitespace and collapse double spaces in title / performer.
  2. Convert Billboard's literal "NA" strings to empty values.
  3. Cast chart_week to a real date; derive year, month, decade, era.
  4. Drop exact duplicate (chart_week, title, performer) rows.
  5. Split the performer string into a primary artist plus collaborators
     ("Featuring", "With", "&", "x", "Duet With", ...), because Billboard
     stores all credits in one free-text field.
  6. Flag seasonal/holiday titles, which behave completely differently
     from ordinary releases and would otherwise distort trend lines.
  7. Range-check ranks (1-100) and weeks-on-chart (>= 1).

Run:  python3 scripts/02_clean_data.py
No third-party libraries required.
"""

import csv
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw", "hot-100-current.csv")
OUT = os.path.join(HERE, "..", "data", "processed", "chart_weeks_clean.csv")
LOG = os.path.join(HERE, "..", "data", "processed", "cleaning_log.txt")

# Words Billboard uses to attach a GUEST artist to a lead credit.
#
# Deliberately conservative: we do NOT split on "&", ",", "+" or "X", because
# those characters are part of thousands of legitimate act names -
# "Kool & The Gang", "Earth, Wind & Fire", "Florence + The Machine",
# "Simon & Garfunkel". Splitting on them shortened those acts to "Kool",
# "Earth", "Florence" and "Simon" in an earlier version of this script.
# The trade-off is that a genuine duo credit such as "Post Malone & Swae Lee"
# is counted as one act. This is recorded in the paper's limitations.
SPLIT_PATTERN = re.compile(
    r"\s+(?:Featuring|Feat\.?|Ft\.?|With|Duet With|Introducing|Presents|vs\.?)\s+",
    flags=re.IGNORECASE,
)

HOLIDAY_WORDS = [
    "christmas", "santa", "jingle", "holiday", "sleigh", "mistletoe",
    "silent night", "rudolph", "feliz navidad", "auld lang syne",
    "winter wonderland", "let it snow", "noel", "hanukkah",
]


def era_for(year):
    """Group chart years into the commercial eras used throughout the paper."""
    if year < 1991:
        return "1. Physical / Airplay (pre-1991)"
    if year < 2005:
        return "2. Soundscan CD Era (1991-2004)"
    if year < 2014:
        return "3. Download & Early Streaming (2005-2013)"
    if year < 2018:
        return "4. Streaming Majority (2014-2017)"
    return "5. Algorithmic / Social Era (2018-present)"


def clean_text(value):
    """Trim, collapse internal whitespace, and normalise curly apostrophes."""
    value = (value or "").replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", value).strip()


def split_artists(performer):
    """Return (primary_artist, n_credited_artists) from a Billboard credit."""
    parts = [p.strip() for p in SPLIT_PATTERN.split(performer) if p.strip()]
    if not parts:
        return performer, 1
    return parts[0], len(parts)


def is_holiday(title):
    low = title.lower()
    return any(word in low for word in HOLIDAY_WORDS)


def main():
    if not os.path.exists(RAW):
        sys.exit("Raw file not found. Run: python3 scripts/01_download_data.py")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    stats = {
        "rows_in": 0, "dropped_duplicate": 0, "dropped_bad_rank": 0,
        "dropped_bad_date": 0, "na_last_week_blanked": 0, "rows_out": 0,
    }
    seen = set()
    cleaned = []

    with open(RAW, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            stats["rows_in"] += 1

            title = clean_text(row["title"])
            performer = clean_text(row["performer"])

            # --- date ---
            try:
                y, m, d = (int(x) for x in row["chart_week"].split("-"))
                chart_date = date(y, m, d)
            except (ValueError, AttributeError):
                stats["dropped_bad_date"] += 1
                continue

            # --- numeric range checks ---
            try:
                rank = int(row["current_week"])
                peak = int(row["peak_pos"])
                weeks_on = int(row["wks_on_chart"])
            except ValueError:
                stats["dropped_bad_rank"] += 1
                continue
            if not (1 <= rank <= 100) or not (1 <= peak <= 100) or weeks_on < 1:
                stats["dropped_bad_rank"] += 1
                continue

            # --- Billboard writes "NA" for a song's first week ---
            last_week_raw = (row.get("last_week") or "").strip()
            if last_week_raw in ("NA", ""):
                last_week = ""
                stats["na_last_week_blanked"] += 1
            else:
                last_week = last_week_raw

            # --- de-duplicate ---
            key = (row["chart_week"], title.lower(), performer.lower())
            if key in seen:
                stats["dropped_duplicate"] += 1
                continue
            seen.add(key)

            primary, n_artists = split_artists(performer)

            cleaned.append({
                "chart_week": chart_date.isoformat(),
                "chart_year": chart_date.year,
                "chart_month": chart_date.month,
                "chart_decade": f"{chart_date.year // 10 * 10}s",
                "era": era_for(chart_date.year),
                "title": title,
                "performer": performer,
                "primary_artist": primary,
                "n_credited_artists": n_artists,
                "is_collaboration": 1 if n_artists > 1 else 0,
                "song_key": f"{title.lower()} :: {performer.lower()}",
                "rank": rank,
                "last_week_rank": last_week,
                "peak_position_to_date": peak,
                "weeks_on_chart": weeks_on,
                "is_top10": 1 if rank <= 10 else 0,
                "is_number_one": 1 if rank == 1 else 0,
                "is_holiday_song": 1 if is_holiday(title) else 0,
            })

    stats["rows_out"] = len(cleaned)
    cleaned.sort(key=lambda r: (r["chart_week"], r["rank"]))

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned[0].keys()))
        writer.writeheader()
        writer.writerows(cleaned)

    report = [
        "BILLBOARD HOT 100 - CLEANING LOG",
        "=" * 44,
        f"Rows read from raw file      : {stats['rows_in']:,}",
        f"Dropped - unparseable date   : {stats['dropped_bad_date']:,}",
        f"Dropped - out-of-range values: {stats['dropped_bad_rank']:,}",
        f"Dropped - exact duplicates   : {stats['dropped_duplicate']:,}",
        f'"NA" last_week set to blank  : {stats["na_last_week_blanked"]:,}',
        f"Rows written to clean file   : {stats['rows_out']:,}",
        f"Date range                   : {cleaned[0]['chart_week']} to {cleaned[-1]['chart_week']}",
        f"Unique songs                 : {len({r['song_key'] for r in cleaned}):,}",
        f"Unique performers            : {len({r['performer'] for r in cleaned}):,}",
    ]
    text = "\n".join(report)
    with open(LOG, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)
    print(f"\nClean file: {os.path.normpath(OUT)}")
    print("Next step:  python3 scripts/03_build_kpis.py")


if __name__ == "__main__":
    main()
