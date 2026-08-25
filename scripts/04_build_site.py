"""
04_build_site.py
----------------
Generates docs/index.html - the free GitHub Pages project website - directly
from data/processed/, so the charts on the site can never drift from the data.

Charts are hand-built inline SVG: no chart library, no CDN, no tracking, and
the whole page is one self-contained file.

Run:  python3 scripts/04_build_site.py
No third-party libraries required.
"""

import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(HERE, "..", "data", "processed")
OUT = os.path.join(HERE, "..", "docs", "index.html")

# Categorical slots 1-4 from the validated default palette, in fixed order.
# Light / dark steps are declared as CSS variables in the page.
PALETTE = ["--series-1", "--series-2", "--series-3", "--series-4"]


def load(name):
    with open(os.path.join(PROC, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def line_chart(points, y_max, y_label, unit="%", accent="--series-1",
               fill=True, y_ticks=5, highlight=None):
    """points: list of (year:int, value:float). Returns an SVG string."""
    W, H = 720, 300
    ML, MR, MT, MB = 52, 18, 18, 34
    pw, ph = W - ML - MR, H - MT - MB
    xs = [p[0] for p in points]
    x0, x1 = min(xs), max(xs)

    def px(year):
        return ML + (year - x0) / (x1 - x0) * pw

    def py(val):
        return MT + ph - (val / y_max) * ph

    parts = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" '
             f'aria-label="{esc(y_label)} by year">']

    # horizontal gridlines + y axis labels (recessive)
    for i in range(y_ticks + 1):
        v = y_max * i / y_ticks
        y = py(v)
        parts.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W-MR}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{ML-8}" y="{y+4:.1f}" class="axis-y">{v:g}{unit}</text>')

    # x axis labels every 5 years
    for year in range(x0, x1 + 1):
        if year % 5 == 0:
            parts.append(f'<text x="{px(year):.1f}" y="{H-MB+20}" class="axis-x">{year}</text>')

    d = " ".join(("M" if i == 0 else "L") + f"{px(y_):.1f},{py(v):.1f}"
                 for i, (y_, v) in enumerate(points))
    if fill:
        area = (d + f" L{px(x1):.1f},{py(0):.1f} L{px(x0):.1f},{py(0):.1f} Z")
        parts.append(f'<path d="{area}" fill="var({accent})" opacity="0.12"/>')
    parts.append(f'<path d="{d}" fill="none" stroke="var({accent})" '
                 f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')

    # hover targets + markers
    for year, val in points:
        cx, cy = px(year), py(val)
        parts.append(
            f'<g class="pt"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="10" fill="transparent"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" class="dot" fill="var({accent})"/>'
            f'<title>{year}: {val:g}{unit}</title></g>')

    # one direct label on the most recent point
    if highlight:
        year, val, text = highlight
        anchor = "end" if px(year) > ML + pw * 0.6 else "start"
        dx = -10 if anchor == "end" else 10
        parts.append(f'<text x="{px(year)+dx:.1f}" y="{py(val)-12:.1f}" '
                     f'class="callout" text-anchor="{anchor}">{esc(text)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def stacked_bars(eras, segments, matrix):
    """100% stacked horizontal bars, one per era, with direct % labels."""
    W = 720
    row_h, gap, ML = 46, 16, 168
    H = len(eras) * (row_h + gap) + 40
    bw = W - ML - 20
    parts = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" '
             f'aria-label="Lifecycle segment mix by era">']
    for i, era in enumerate(eras):
        y = i * (row_h + gap) + 10
        parts.append(f'<text x="{ML-12}" y="{y+row_h/2+4}" class="axis-y">{esc(era)}</text>')
        x = ML
        for j, seg in enumerate(segments):
            share = matrix[era][seg]
            w = share * bw
            if w <= 0:
                continue
            # 2px surface gap between adjacent segments
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w-2,0.5):.1f}" '
                         f'height="{row_h}" rx="3" fill="var({PALETTE[j]})"/>')
            if share >= 0.07:   # direct label only where it fits
                parts.append(f'<text x="{x+w/2-1:.1f}" y="{y+row_h/2+4}" '
                             f'class="bar-label">{share*100:.0f}%</text>')
            x += w
    parts.append("</svg>")
    return "\n".join(parts)


def quintile_bars(rows):
    """rows: list of (label, ratio_range, median_run, durable_pct)."""
    W, ML, row_h, gap = 720, 150, 40, 14
    H = len(rows) * (row_h + gap) + 20
    bw = W - ML - 70
    parts = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" '
             f'aria-label="Durability by week-8 retention quintile">']
    # ordinal ramp: darkest = holding peak, lightest = collapsed (all >= 2:1)
    ramp = ["#1c5cab", "#256abf", "#3987e5", "#5598e7", "#86b6ef"]
    for i, (label, rng, med, pct) in enumerate(rows):
        y = i * (row_h + gap) + 6
        parts.append(f'<text x="{ML-12}" y="{y+row_h/2+4}" class="axis-y">{esc(label)}</text>')
        w = pct / 50 * bw
        parts.append(f'<rect x="{ML}" y="{y}" width="{w:.1f}" height="{row_h}" '
                     f'rx="4" fill="{ramp[i]}"><title>{esc(label)}: {pct}% reached 26+ weeks '
                     f'(ratio {rng}, median run {med})</title></rect>')
        parts.append(f'<text x="{ML+w+10:.1f}" y="{y+row_h/2+4}" class="value">{pct}%</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    kpis = load("yearly_kpis.csv")
    songs = load("song_summary.csv")

    def series(field, lo, hi):
        out = []
        for r in kpis:
            y = int(r["chart_year"])
            if lo <= y <= hi and r[field] not in ("", None):
                out.append((y, float(r[field])))
        return out

    # Trend charts stop at 2024 - the last uncensored cohort year.
    debut_peak = series("kpi_debut_peak_rate_pct", 1990, 2024)
    half_life = series("kpi_chart_half_life_weeks", 1990, 2024)
    # Catalog crowding is a within-year measure, so 2025 is complete.
    crowding = series("kpi_catalog_crowding_pct", 1990, 2025)
    breakthrough = series("kpi_breakthrough_artists", 1990, 2025)

    # segment mix by era
    counts = defaultdict(Counter)
    for r in songs:
        if r["reached_top40"] == "1":
            counts[r["era"]][r["lifecycle_segment"]] += 1
    seg_order = ["Spike (fast peak, short life)",
                 "Instant Standard (fast peak, long life)",
                 "Slow Burn (built over time, long life)",
                 "Grinder (slow climb, short life)"]
    short = {s: s.split(" (")[0] for s in seg_order}
    eras = sorted(counts)
    matrix = {e: {s: counts[e][s] / sum(counts[e].values()) for s in seg_order} for e in eras}
    era_labels = {e: e.split(". ", 1)[1] for e in eras}
    matrix_lbl = {era_labels[e]: matrix[e] for e in eras}

    charts = {
        "debut_peak": line_chart(
            debut_peak, 80, "Share of Top 40 hits peaking in week 1",
            highlight=(2024, 72.7, "2024: 72.7%")),
        "half_life": line_chart(
            half_life, 25, "Median chart run", unit=" wks", accent="--series-2",
            highlight=(2024, 7.0, "2024: 7 weeks")),
        "crowding": line_chart(
            crowding, 10, "Chart slots held by music 12+ months old",
            accent="--series-3", highlight=(2025, 7.9, "2025: 7.9%")),
        "breakthrough": line_chart(
            breakthrough, 50, "First-time Top 10 artists", unit="",
            accent="--series-7", fill=False, highlight=(2025, 14, "2025: 14")),
        "segments": stacked_bars(
            [era_labels[e] for e in eras], seg_order, matrix_lbl),
        "quintiles": quintile_bars([
            ("1 — holding peak", "0.07–0.74", "25 wks", 48),
            ("2", "0.74–1.08", "25 wks", 45),
            ("3", "1.08–2.00", "21 wks", 36),
            ("4", "2.00–4.33", "19 wks", 19),
            ("5 — collapsed", "4.38–70.0", "18 wks", 17)]),
    }
    legend = "".join(
        f'<span class="key"><i style="background:var({PALETTE[j]})"></i>{esc(short[s])}</span>'
        for j, s in enumerate(seg_order))

    html = TEMPLATE
    for key, svg in charts.items():
        html = html.replace("{{" + key + "}}", svg)
    html = html.replace("{{segment_legend}}", legend)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {os.path.normpath(OUT)} ({os.path.getsize(OUT)/1024:.0f} KB)")
    print("Preview locally:  python3 -m http.server -d docs 8000")


# The page shell lives in docs/_template.html so the layout can be edited
# without touching the chart code. Placeholders like {{debut_peak}} are
# replaced with generated SVG.
with open(os.path.join(HERE, "..", "docs", "_template.html"), encoding="utf-8") as _f:
    TEMPLATE = _f.read()

if __name__ == "__main__":
    main()
