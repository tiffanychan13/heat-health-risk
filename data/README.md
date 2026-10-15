# Data

All files here are public, aggregated data. They are committed to the repository so the notebook runs without any downloads.

## raw/

`raw/ehdp/heat-syndrome/`
Daily citywide heat-related ED visits (`HEAT_ED_VISIT_COUNT`) and the daily maximum heat at LaGuardia (`MAX_DAILY_TEMP`, the higher of heat index and air temperature), May to September. Source: NYC Environment and Health Data Portal, GitHub repository nychealth/EHDP-data.

- `previous_years.csv` (2017 to 2025) and `edheat2026_live.csv` (2026) are the files used in the analysis. `previous_years.csv` applies NYC's revised 2023 case definition to every year.
- `edheat1720_supp.csv` and `edheat2021_live.csv` to `edheat2025_live.csv` are other versions of the same days. Their counts differ, so they are kept for reference but not used.

`raw/iem/mos/`
NWS extended-range MOS (MEX) forecasts for LaGuardia (KLGA), one file per season, 2021 to 2026. Runs at 00Z and 12Z, forecasts out to 8 days. Source: Iowa Environmental Mesonet. Times are in UTC.

`raw/iem/alerts/`
All NWS watches, warnings, and advisories for forecast zone NYZ072 (Manhattan), 2017 to 2026. Heat products are the rows with phenomena code HT, EH, or XH. Source: Iowa Environmental Mesonet. Times are in UTC.

## external/

`external/ehdp/heat-vulnerability-index/`
NYC Heat Vulnerability Index for 198 neighborhoods. `hvi-nta-2020.csv` (2020 neighborhood boundaries) is the file used. `nta_zip_collapsed.json` maps neighborhoods to ZIP codes. Source: nychealth/EHDP-data.

`external/nyc-open-data/`
NYC Parks outdoor cooling features from 2020 and a list of drinking fountains and spray showers. Source: NYC Open Data. These do not include indoor cooling centers and are not used in the model.

## processed/

Empty for now. The notebook builds its analysis table in memory.

## Re-downloading

The NYC Health files can be downloaded again from the repository root:

```bash
python -m heatrisk.download            # same version used in this project
python -m heatrisk.download --latest   # newest version
```

The Iowa Environmental Mesonet and NYC Open Data files were downloaded through their websites. The settings used are in `docs/data_log.md`.
