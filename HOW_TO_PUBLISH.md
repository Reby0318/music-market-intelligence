# How to Publish This Project

Three things to put online, all free, no subscription, no trial that expires.
Budget about an hour end to end.

---

## 1. Push the repository to GitHub (~15 min)

### One-time setup
1. Create a free account at https://github.com if you do not have one.
2. Tell Git who you are (once per machine):
   ```bash
   git config --global user.name "Rebecca Wu"
   git config --global user.email "your@email.com"
   ```

### Create the remote repository
1. Go to https://github.com/new
2. **Repository name:** `music-market-intelligence`
3. **Description:** `Quantifying the discovery bottleneck in the streaming era — 68 years of Billboard Hot 100 data`
4. Set it to **Public** (hiring managers need to see it)
5. **Do not** tick "Add a README" — this project already has one
6. Click **Create repository**

### Push
From this folder:
```bash
cd ~/Projects/music-market-intelligence
git remote add origin https://github.com/YOUR_USERNAME/music-market-intelligence.git
git branch -M main
git push -u origin main
```
GitHub will ask you to sign in through your browser the first time.

### Then replace the placeholders
Search the repo for `USERNAME` and swap in your real GitHub username. It appears in:
- `README.md`
- `docs/_template.html` (then re-run `python3 scripts/04_build_site.py`)
- `paper/Signal-vs-Noise-Paper.md`

Commit and push again:
```bash
git add -A && git commit -m "Add live URLs" && git push
```

---

## 2. Turn on GitHub Pages (~5 min)

This publishes `docs/index.html` as a real website at no cost.

1. In your repository, go to **Settings → Pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main`, **Folder:** `/docs`
4. Click **Save**
5. Wait 1–2 minutes, then visit:
   **`https://YOUR_USERNAME.github.io/music-market-intelligence/`**

That URL is what you put on your résumé and in applications.

**If the page 404s:** confirm the folder is set to `/docs` and that `docs/index.html`
exists (`ls docs/`). Pages can take up to 10 minutes on a first deploy.

---

## 3. Publish the Tableau dashboards (~2 hours)

Follow **[tableau/TABLEAU_BUILD_GUIDE.md](tableau/TABLEAU_BUILD_GUIDE.md)** step by step.

Short version:
1. Install **Tableau Public** (free, permanent): https://public.tableau.com/app/discover
2. Connect to the CSVs in `data/processed/`
3. Build the four dashboards
4. **File → Save to Tableau Public As…** — this gives you a public URL
5. Paste that URL everywhere `YOUR_TABLEAU_URL` appears, then re-run
   `python3 scripts/04_build_site.py` and push

> Tableau Public makes every saved workbook publicly visible. That is what you want
> here — but never load private or client data into it.

---

## 4. Refreshing the data later

The Billboard archive updates weekly. To refresh everything:

```bash
python3 scripts/01_download_data.py
python3 scripts/02_clean_data.py
python3 scripts/03_build_kpis.py
python3 scripts/04_build_site.py
git add -A && git commit -m "Refresh data through $(date +%Y-%m-%d)" && git push
```

In Tableau Public, open the workbook and use **Data → Refresh** to pick up the new CSVs,
then save again.

---

## Placeholder checklist

Before you send this to anyone, make sure none of these are still in the repo:

- [ ] `USERNAME` → your GitHub username
- [ ] `YOUR_TABLEAU_URL` → your Tableau Public workbook link
- [ ] `[add your portfolio URL]` in `README.md`
- [ ] `[add your LinkedIn URL]` in `README.md`
- [ ] Your name is spelled correctly in `LICENSE`, `README.md`, the paper, and `docs/_template.html`

Quick way to find every remaining placeholder:
```bash
grep -rn "USERNAME\|YOUR_TABLEAU_URL\|\[add your" --include="*.md" --include="*.html" .
```

---

## What to say about this project in an interview

**The 30-second version:**
> "The music industry's real problem isn't that there's too much music — it's that
> nobody can tell durable demand from manufactured attention. I took 68 years of
> Billboard data and measured how far that signal degraded: 73% of hits now peak in
> week one, up from under 1% in 2000, and median chart life fell from 20 weeks to
> seven. Then I tested which early signal actually predicts durability. Debut position
> is basically noise. Week-eight retention predicts it 3.5× better, and separates
> durable hits from spikes at 2.8× resolution — early enough to reallocate spend."

**If they push on rigour, mention:**
- Right-censoring: you excluded years whose songs hadn't finished charting
- The artist-parsing bug you found and fixed (splitting on `&` broke band names)
- That you state the Billboard methodology change as a confound rather than claiming
  a clean causal break at 2018
- That the whole thing reproduces from a public source with no paid tools

Those four points are what separate an analysis from a chart.
