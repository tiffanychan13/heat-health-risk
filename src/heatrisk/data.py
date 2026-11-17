"""Load the raw and external data files into tidy pandas tables.

Every notebook and script should load data through these functions, so that
cleaning choices (which ED file version to use, how to treat cancelled alerts,
time zones) are made once and applied the same way everywhere.
"""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTERNAL_DIR = DATA_DIR / "external"
PROCESSED_DIR = DATA_DIR / "processed"

NY_TZ = "America/New_York"

# NWS heat products for the NYC zone. "Excessive Heat" (EH) was renamed
# "Extreme Heat" (XH) in 2025, so both codes mean the same product.
HEAT_PHENOMENA = {"HT": "Heat", "EH": "Extreme Heat", "XH": "Extreme Heat"}


def load_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Read a CSV, raising a clear error if the file has not been downloaded yet."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download it first; see data/README.md."
        )
    return pd.read_csv(path, **kwargs)


def load_ed(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Daily citywide heat-related ED visits and observed max heat, 2017-2026.

    Uses previous_years.csv (2017-2025, NYC's revised 2023 case definition applied
    to every year) plus edheat2026_live.csv (2026, provisional). The other files
    in the folder are older versions of the same days and are not used.

    Returns columns:
        date    calendar day
        N       suspected heat-related ED visits that day (citywide)
        H       observed max heat at LaGuardia, max(heat index, temperature), F
        season  year
    """
    folder = Path(raw_dir) / "ehdp/heat-syndrome"
    prev = load_csv(folder / "previous_years.csv", parse_dates=["END_DATE"])
    live26 = load_csv(folder / "edheat2026_live.csv", parse_dates=["END_DATE"])
    ed = pd.concat([prev, live26], ignore_index=True).rename(
        columns={"END_DATE": "date", "HEAT_ED_VISIT_COUNT": "N", "MAX_DAILY_TEMP": "H"}
    )
    ed = ed.drop_duplicates("date", keep="first").sort_values("date").reset_index(drop=True)
    ed["season"] = ed["date"].dt.year
    return ed[["date", "N", "H", "season"]]


def load_mos(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """NWS extended MOS (MEX) forecasts for LaGuardia, 2021-2026.

    One row per (forecast run, valid time). runtime and ftime are UTC.
    """
    files = sorted((Path(raw_dir) / "iem/mos").glob("mos_mex_klga_*.csv"))
    if not files:
        raise FileNotFoundError("No MOS files found under data/raw/iem/mos/.")
    mos = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    mos["runtime"] = pd.to_datetime(mos["runtime"]).dt.tz_localize("UTC")
    mos["ftime"] = pd.to_datetime(mos["ftime"]).dt.tz_localize("UTC")
    return mos


def load_alerts(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """All NWS watches, warnings and advisories for zone NYZ072 (Manhattan), UTC times."""
    alerts = load_csv(Path(raw_dir) / "iem/alerts/nws_alerts_NYZ072.csv")
    alerts["issued"] = pd.to_datetime(alerts["iso_issued"], utc=True)
    alerts["expired"] = pd.to_datetime(alerts["iso_expired"], utc=True)
    return alerts


def load_heat_alerts(raw_dir: Path = RAW_DIR, include_watches: bool = False) -> pd.DataFrame:
    """NWS heat advisories and warnings that actually took effect.

    These are the record of when the city's heat response was triggered in
    practice. Watches (a heads-up that a warning *may* follow) are excluded by
    default. Alerts that expired before they were issued were cancelled or
    upgraded before taking effect, so they are dropped, as are duplicates.
    """
    alerts = load_alerts(raw_dir)
    heat = alerts[alerts["phenomena"].isin(HEAT_PHENOMENA)].copy()
    if not include_watches:
        heat = heat[heat["significance"] != "A"]  # A = watch
    heat = heat[heat["expired"] > heat["issued"]]
    heat = heat.drop_duplicates(["vtec_year", "phenomena", "significance", "eventid"])
    heat["product"] = heat["phenomena"].map(HEAT_PHENOMENA) + " " + heat["sig_name"]
    return heat.reset_index(drop=True)


def load_hvi(external_dir: Path = EXTERNAL_DIR) -> pd.DataFrame:
    """NYC Heat Vulnerability Index by neighborhood (2020 NTA boundaries), 1-5."""
    return load_csv(Path(external_dir) / "ehdp/heat-vulnerability-index/hvi-nta-2020.csv")
