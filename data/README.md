# Data

| Folder | Contents | Source | In Git? |
|---|---|---|---|
| `raw/ehdp/heat-syndrome/` | Daily citywide heat-syndrome ED visits + max daily heat index at LaGuardia, May–Sep 2017–2026 | NYC EH Data Portal (GitHub `nychealth/EHDP-data`) | Yes |
| `external/ehdp/heat-vulnerability-index/` | NYC Heat Vulnerability Index by neighborhood (NTA); NTA-to-ZIP lookup | NYC EH Data Portal (GitHub `nychealth/EHDP-data`) | Yes |
| `raw/` (other) | NWS MOS forecasts and heat advisories; NOAA daily observations | Iowa Environmental Mesonet, NOAA NCEI | Not yet downloaded |
| `processed/` | Cleaned, merged city-day and neighborhood tables produced by `src/heatrisk` | generated | No |

## Re-downloading the EHDP files

From the repo root:

```bash
python -m heatrisk.download            # exact version used in this project
python -m heatrisk.download --latest   # newest version on GitHub
```

Record the download date and source for every file in `docs/data_log.md`.
