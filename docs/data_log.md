# Data log

Record every dataset download here so results can be reproduced.

| Date downloaded | Files | Saved to | Source | Notes |
|---|---|---|---|---|
| 2026-10-11 | `previous_years.csv`, `edheat1720_supp.csv`, `edheat2021_live.csv` … `edheat2026_live.csv`, `README.md` | `data/raw/ehdp/heat-syndrome/` | [nychealth/EHDP-data](https://github.com/nychealth/EHDP-data/tree/08d6e68f6e1d744f31b54401ec3165520681bb95/key-topics/heat-syndrome), commit `08d6e68` | Daily heat-syndrome ED visits + max daily heat index (LaGuardia), May–Sep 2017–2026. Downloaded with `python -m heatrisk.download`. |
| 2026-10-11 | `hvi-nta-2020.csv`, `hvi-nta.csv`, `nta_zip_collapsed.json`, `README.md` | `data/external/ehdp/heat-vulnerability-index/` | [nychealth/EHDP-data](https://github.com/nychealth/EHDP-data/tree/08d6e68f6e1d744f31b54401ec3165520681bb95/key-topics/heat-vulnerability-index), commit `08d6e68` | Heat Vulnerability Index by neighborhood (NTA). `hvi-nta-2020.csv` uses 2020 NTA boundaries (198 rows) and is the primary file. |

## First observations (2026-10-11)

- **Three overlapping versions of the ED series.** `previous_years.csv` (2017–2025), `edheat1720_supp.csv` (2017–2020) and the yearly `edheat20XX_live.csv` files (2021–2026) overlap. Daily max temperature matches across all of them, but visit counts differ:
  - `previous_years` vs `edheat1720_supp`: 287 of 612 overlapping days differ. Likely the 2023 case-definition revision (the source README says the revised definition was applied to all years on the portal).
  - `previous_years` vs `live` files: 55 of 755 overlapping days differ. Recent data is not final and gets revised.
  - **Decision needed:** pick one consistent version and justify it.
- **Missing days:** 2023 ends Sep 28 (2 days missing); 2025 is missing 8 days.
- **Distribution:** median 2 visits/day, 25% of days are zero, max 156. 90th / 95th percentiles are 13 / 21 visits.
- **2020** is low (COVID). **2025–2026** average ~7.5 visits/day vs. 3–5 in earlier years; check whether this is weather or reporting.
