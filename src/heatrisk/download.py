"""Download source data from the NYC Environment & Health Data Portal GitHub repo.

Usage (from the repo root):
    python -m heatrisk.download            # pinned version used in this project
    python -m heatrisk.download --latest   # newest version on GitHub

Files are saved under data/raw/ehdp/ and data/external/ehdp/, keeping the
same folder names as the source repo (nychealth/EHDP-data).
"""

import argparse
import urllib.request
from pathlib import Path

from heatrisk.data import EXTERNAL_DIR, RAW_DIR

REPO = "nychealth/EHDP-data"

# Commit of nychealth/EHDP-data that this project's data was taken from
# (downloaded 2026-10-11). Pinning it means everyone gets identical files.
PINNED_COMMIT = "08d6e68f6e1d744f31b54401ec3165520681bb95"

# (source path in EHDP-data, destination folder in this repo)
FILES = [
    # Daily heat-syndrome ED visits + max daily heat index at LaGuardia
    ("key-topics/heat-syndrome/README.md", RAW_DIR / "ehdp/heat-syndrome"),
    ("key-topics/heat-syndrome/previous_years.csv", RAW_DIR / "ehdp/heat-syndrome"),
    ("key-topics/heat-syndrome/edheat1720_supp.csv", RAW_DIR / "ehdp/heat-syndrome"),
    *[
        (f"key-topics/heat-syndrome/edheat{year}_live.csv", RAW_DIR / "ehdp/heat-syndrome")
        for year in range(2021, 2027)
    ],
    # Heat Vulnerability Index by neighborhood (NTA)
    ("key-topics/heat-vulnerability-index/README.md", EXTERNAL_DIR / "ehdp/heat-vulnerability-index"),
    ("key-topics/heat-vulnerability-index/hvi-nta-2020.csv", EXTERNAL_DIR / "ehdp/heat-vulnerability-index"),
    ("key-topics/heat-vulnerability-index/hvi-nta.csv", EXTERNAL_DIR / "ehdp/heat-vulnerability-index"),
    ("key-topics/heat-vulnerability-index/nta_zip_collapsed.json", EXTERNAL_DIR / "ehdp/heat-vulnerability-index"),
]


def download(ref: str = PINNED_COMMIT) -> None:
    for src, dest_dir in FILES:
        url = f"https://raw.githubusercontent.com/{REPO}/{ref}/{src}"
        dest = dest_dir / Path(src).name
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"  {src}  ->  {dest.relative_to(dest_dir.parents[2])}")
        urllib.request.urlretrieve(url, dest)
    print(f"Done. Downloaded {len(FILES)} files from {REPO}@{ref[:7]}.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--latest",
        action="store_true",
        help="download the newest files instead of the pinned version",
    )
    args = parser.parse_args()
    download("production" if args.latest else PINNED_COMMIT)


if __name__ == "__main__":
    main()
