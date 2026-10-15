# Heat-Risk Activation: Forecast-Driven Decision Support for Heat-Response Interventions in New York City

Tiffany Chan, ESE 5971 Practicum in Data Analytics and Statistics

## Project objective

New York City can respond to forecast heat by issuing advisories, opening cooling centers, and sending outreach teams to vulnerable neighborhoods. These actions cost staff time and money, so the city has to decide when they are worth it.

This project asks: at the time a weather forecast is issued, how likely is it that citywide heat-related emergency department (ED) visits will be elevated 3 to 7 days later? The predicted probability is then used to recommend whether to escalate the heat response and how many neighborhoods to cover.

The project has two levels:

1. **When to act (citywide, learned from data).** Estimate p̂_t, the probability that daily heat-related ED visits exceed a threshold κ at least once in days t+3 to t+7, using NWS forecasts, recent heat, and recent ED counts.
2. **Where to focus (neighborhood, rule-based).** If the city escalates, neighborhoods are prioritized by the NYC Heat Vulnerability Index (HVI). Higher predicted risk extends the response from HVI 5 neighborhoods to HVI 4 and 5, then citywide.

Daily ED data are only published for the whole city, so the model does not predict neighborhood-level risk. The data also cannot show how much the interventions actually reduce ED visits, so that effect is treated as an assumed range (about 0 to 15 percent) rather than estimated. Results are predictive, not causal.

## Repository organization

```
heat-health-risk/
  README.md
  requirements.txt
  pyproject.toml
  notebooks/
    milestone2_analysis.ipynb   main Milestone 2 analysis
  src/heatrisk/
    data.py                     folder paths and a CSV loader
    download.py                 re-downloads the NYC Health files
    decision.py                 cost-based activation threshold (early version)
  tests/                        unit tests for decision.py
  data/
    README.md                   what each data folder contains
    raw/                        source files, unchanged
    external/                   reference data (HVI, cooling sites)
    processed/                  empty for now
  reports/
    figures/                    figures saved by the notebook
    milestones/                 milestone dossiers
  docs/
    data_log.md                 where each file came from and first checks
    assumptions.md              working assumptions and open questions
```

## Dependencies

Python 3.10 or newer. Packages are listed in `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, and Jupyter). To set up an environment:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## How to run

1. Clone the repository. All data needed for the analysis is already included under `data/`.
2. Install the dependencies (above).
3. Open `notebooks/milestone2_analysis.ipynb` in Jupyter or VS Code, choose Restart Kernel, then Run All. It takes under a minute and writes four figures to `reports/figures/`.
4. Optional: run `pytest` from the repository root to test `decision.py`.

Nothing has to be run before the notebook. It reads the raw files directly and builds the analysis table in memory.

## Data origin and access

All data are public and aggregated. No individual-level or confidential records are used. The files are small, so they are committed to the repository.

- **Heat-related ED visits** (`data/raw/ehdp/heat-syndrome/`): daily citywide counts of suspected heat-related ED visits and the daily maximum heat at LaGuardia, May to September, 2017 to 2026. Published by the NYC Department of Health on the Environment and Health Data Portal and its GitHub repository, nychealth/EHDP-data. The analysis uses `previous_years.csv` for 2017 to 2025 and `edheat2026_live.csv` for 2026. The other files in that folder are older or provisional versions of the same series and are kept only for reference.
- **NWS forecasts** (`data/raw/iem/mos/`): extended-range MOS (MEX) forecasts for LaGuardia, 2021 to 2026, from the Iowa Environmental Mesonet archive.
- **NWS heat alerts** (`data/raw/iem/alerts/`): watches, warnings, and advisories for forecast zone NYZ072, from the Iowa Environmental Mesonet.
- **Heat Vulnerability Index** (`data/external/ehdp/heat-vulnerability-index/`): neighborhood scores from 1 to 5, from the same NYC Health repository.
- **Cooling sites** (`data/external/nyc-open-data/`): NYC Parks outdoor cooling features from NYC Open Data. These are not indoor cooling centers and are not used in the model.

`data/README.md` describes each folder, and `docs/data_log.md` records the source link and download settings for every file.

## Known reproducibility limitations

- The NYC Health files are pinned to one commit of nychealth/EHDP-data, so `python -m heatrisk.download` returns the same files used here. NYC may revise the series later, and those revisions will not show up unless you download with `--latest`.
- The 2026 ED counts are provisional and may still change at the source.
- The forecast and alert files were downloaded through web forms on the Iowa Environmental Mesonet site, not by a script. `docs/data_log.md` lists the settings used.
- Archived MEX forecasts only start in July 2020, so the forecast-based analysis covers 2021 to 2026.
- The ED counts are revised values, not exactly what was available in real time, so the measured performance may be somewhat better than it would be in live use.
- `decision.py` still uses an earlier, simpler threshold formula. It will be updated to match the dossier in the next milestone.
