"""
01_download_data.py
-------------------
Downloads the raw Billboard Hot 100 chart archive (1958 - present).

Source : https://github.com/utdata/rwd-billboard-data
File   : data-out/hot-100-current.csv
Why    : It is free, public, requires no login or API key, and is refreshed
         weekly by GitHub Actions, so this project can be re-run at any time.

Run:  python3 scripts/01_download_data.py
No third-party libraries required.
"""

import os
import urllib.request

URL = ("https://raw.githubusercontent.com/utdata/rwd-billboard-data/"
       "main/data-out/hot-100-current.csv")

# Save next to this script, in ../data/raw/
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "data", "raw")
OUT_PATH = os.path.join(OUT_DIR, "hot-100-current.csv")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Downloading Billboard Hot 100 archive...\n  from: {URL}")
    urllib.request.urlretrieve(URL, OUT_PATH)

    size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
    with open(OUT_PATH, encoding="utf-8") as f:
        n_rows = sum(1 for _ in f) - 1  # minus the header row

    print(f"  saved to: {os.path.normpath(OUT_PATH)}")
    print(f"  size: {size_mb:.1f} MB   rows: {n_rows:,}")
    print("\nDone. Next step:  python3 scripts/02_clean_data.py")


if __name__ == "__main__":
    main()
