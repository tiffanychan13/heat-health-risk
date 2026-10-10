# Heat–Health Risk Early Warning

Semester project for **Practicum in Data Analytics and Statistics** (M.S. Engineering Data Analytics and Statistics).

## Problem

Estimate the probability that a county's heat-related emergency-department (ED) visit rate will exceed a threshold within a short forecast horizon (3–7 days), using forecasted heat conditions and county-level illness and vulnerability history. The pilot focuses on Phoenix / Maricopa County, AZ.

**Analytical system:** estimates

$$\hat p_{z,t} = \Pr(Y_{z,t+\Delta} = 1 \mid X_{z,t})$$

for zone *z* at time *t*.

**Decision system (built on top):** translates $\hat p$ into a cooling-center activation decision via a cost-based threshold $\eta$.

## Data sources

| Source | Use |
|---|---|
| CDC Heat & Health Tracker | Historical county-level heat-related ED visits / hospitalizations; heat-wave forecasts |
| CDC/ATSDR Social Vulnerability Index (SVI) | County / tract vulnerability indicators |
| NWS heat forecast products | Forecasted heat index |
| City open-data portals | Cooling-center locations and capacity |

Raw data is **not** committed to this repo. See `data/README.md`.

## Repository layout

```
data/
  raw/          # untouched downloads (git-ignored)
  external/     # third-party reference data, e.g. SVI (git-ignored)
  processed/    # cleaned, model-ready tables (git-ignored)
notebooks/      # exploratory analysis, numbered by milestone/week
src/heatrisk/   # reusable code: data loading, features, models, decision rule
tests/          # unit tests for src/
reports/
  figures/      # generated plots
  milestones/   # dossiers and slide decks
docs/           # assumptions, data dictionary, notes
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest
```

## Work plan

| Weeks | Milestone |
|---|---|
| 4–5 | Data acquisition |
| 6–7 | Data understanding & quality assessment |
| 8–9 | Exploratory analysis |
| 10–11 | Baseline (logistic regression) and gradient-boosted model; time-based and cross-county holdout |
| 12 | Decision-rule integration (threshold $\eta$) |
| 13 | Uncertainty quantification: calibration, sensitivity on $\eta$ |
| 14 | Reproducibility: end-to-end pipeline |
| 15 | Final technical defense |

## Author

Tiffany Chan
