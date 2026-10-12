# Data log

Record every dataset download here so results can be reproduced.

| Date downloaded | Files | Saved to | Source | Notes |
|---|---|---|---|---|
| 2026-10-11 | `previous_years.csv`, `edheat1720_supp.csv`, `edheat2021_live.csv` … `edheat2026_live.csv`, `README.md` | `data/raw/ehdp/heat-syndrome/` | [nychealth/EHDP-data](https://github.com/nychealth/EHDP-data/tree/08d6e68f6e1d744f31b54401ec3165520681bb95/key-topics/heat-syndrome), commit `08d6e68` | Daily heat-syndrome ED visits + max daily heat index (LaGuardia), May–Sep 2017–2026. Downloaded with `python -m heatrisk.download`. |
| 2026-10-11 | `hvi-nta-2020.csv`, `hvi-nta.csv`, `nta_zip_collapsed.json`, `README.md` | `data/external/ehdp/heat-vulnerability-index/` | [nychealth/EHDP-data](https://github.com/nychealth/EHDP-data/tree/08d6e68f6e1d744f31b54401ec3165520681bb95/key-topics/heat-vulnerability-index), commit `08d6e68` | Heat Vulnerability Index by neighborhood (NTA). `hvi-nta-2020.csv` uses 2020 NTA boundaries (198 rows) and is the primary file. |
| 2026-10-11 | `mos_mex_klga_2021.csv` … `mos_mex_klga_2026.csv` | `data/raw/iem/mos/` | [IEM MOS raw data download](https://mesonet.agron.iastate.edu/mos/fe.phtml) | NWS GFS Extended MOS (MEX) for LaGuardia (KLGA). Form settings: model GFS-X (MEX), May 1 00 UTC – Sep 30 12 UTC, one file per year. Runs at 00 and 12 UTC, forecasts 24–192 h ahead in 12 h steps (15 rows per run). |
| 2026-10-11 | `nws_alerts_NYZ072.csv` | `data/raw/iem/alerts/` | [IEM VTEC search by county/zone](https://mesonet.agron.iastate.edu/vtec/search.php) | All NWS watches/warnings/advisories for zone NYZ072 (New York / Manhattan), issued 2017-05-01 to 2026-10-01, CSV export. 472 alerts of all types; heat products are filtered in code. |
| 2026-10-11 | `cool_it_nyc_2020_cooling_sites.csv` | `data/external/nyc-open-data/` | [Cool It! NYC 2020 – Cooling Sites](https://data.cityofnewyork.us/d/h2bn-gu9k) (NYC Open Data) | 271 **outdoor** NYC Parks cooling features (misting stations, spray adapters, hydrant caps) with status and coordinates. Not indoor cooling centers. |
| 2026-10-11 | `cooling-locations.csv` | `data/external/nyc-open-data/` | NYC Open Data (exact dataset to be confirmed) | 4,610 NYC Parks drinking fountains (3,849) and spray showers (761), with borough and park name only. No coordinates. Not indoor cooling centers. |

## First observations

- **Three overlapping versions of the ED series.** `previous_years.csv` (2017–2025), `edheat1720_supp.csv` (2017–2020) and the yearly `edheat20XX_live.csv` files (2021–2026) overlap. Daily max temperature matches across all of them, but visit counts differ:
  - `previous_years` vs `edheat1720_supp`: 287 of 612 overlapping days differ. Likely the 2023 case-definition revision (the source README says the revised definition was applied to all years on the portal).
  - `previous_years` vs `live` files: 55 of 755 overlapping days differ. Recent data is not final and gets revised.
  - **Decision needed:** pick one consistent version and justify it.
- **Missing days:** 2023 ends Sep 28 (2 days missing); 2025 is missing 8 days.
- **Distribution:** median 2 visits/day, 25% of days are zero, max 156. 90th / 95th percentiles are 13 / 21 visits.
- **2020** is low (COVID). **2025–2026** average ~7.5 visits/day vs. 3–5 in earlier years; check whether this is weather or reporting.

### NWS MOS forecasts (MEX, KLGA)

- **Coverage limit:** IEM's MEX archive starts 2020-07-12, so 3–7 day forecasts exist only for 2021–2026 (6 seasons), not 2017–2019. Forecast-based modeling is restricted to 2021–2026.
- **Completeness:** 304–306 runs per season, 15 forecast steps per run, no missing temperatures. Missing runs: 2023-06-06 12Z, 2023-06-07 00Z, 2025-08-08 00Z, 2026-09-20 00Z (4 of ~1,830).
- **Key columns:** `runtime` (issue time = decision time), `ftime` (valid time), `n_x` (max temp at 00Z valid times, min temp at 12Z valid times), `tmp`, `dpt` (for forecast heat index). Times are UTC.

### NWS alerts (zone NYZ072)

- Heat alerts 2017–2026: 49 Heat Advisories, 5 Excessive Heat Warnings, 3 Excessive Heat Watches, 2 Extreme Heat Warnings, 2 Extreme Heat Watches. About 4–7 heat events per summer.
- NWS renamed "Excessive Heat" to "Extreme Heat" in 2025 (code EH → XH). Both must be treated as the same product.
- Some rows have an expiry earlier than their start time. These are watches/advisories that were cancelled or upgraded before they took effect, and need handling when building the daily "alert in effect" flag.
- `issued`/`expired` are UTC; convert to New York time before matching to ED dates.

### Cooling infrastructure

- **Neither file lists indoor cooling centers** (air-conditioned libraries, senior centers, etc.). NYC Emergency Management reported 622 registered cooling centers in 2024, but no downloadable location dataset was found.
- `cool_it_nyc_2020_cooling_sites.csv` covers only 2020 and four boroughs (no Staten Island). NYC Parks placed these features in HVI 4–5 neighborhoods, so using them to rank neighborhoods partly reflects HVI itself (circularity).
