# Heat-Risk Activation: Decision-Support System for Municipal Heat-Response Interventions

Semester project for **Practicum in Data Analytics and Statistics** (M.S. Engineering Data Analytics and Statistics).

## Problem

Heat-related illness is a serious and growing public-health burden in New York City. This project builds a decision-support system that helps the city decide **when** to activate heat-response interventions (heat advisories, cooling centers, outreach) and **where** to focus them.

## Two-level design

Public daily heat-related emergency-department (ED) data for NYC is **citywide only**, so the decision is split into two levels.

**Level 1: When to act (city-day, modeled).** The analytical system estimates

$$\hat p_t = \Pr(Y_{t+\Delta} = 1 \mid X_t)$$

the probability that citywide heat-related ED visits exceed a threshold within the next 3–7 days, given forecast heat conditions, recent ED trends, and day-of-season. Activation happens when $\hat p_t \ge \eta$, where $\eta$ comes from an explicit cost trade-off between false alarms and missed events.

**Level 2: Where to focus (neighborhood, rule-based).** Once activated, neighborhoods are ranked by the NYC Heat Vulnerability Index (HVI) and existing cooling-center coverage. Response is tiered by severity:

| Predicted severity | Neighborhoods covered |
|---|---|
| Elevated | HVI 5 |
| High | HVI 4–5 |
| Extreme | All neighborhoods |

## Data sources

| Source | Use |
|---|---|
| NYC EH Data Portal, real-time heat-related illness | Primary outcome: daily citywide heat-related ED visits (syndromic surveillance) |
| Iowa Environmental Mesonet (IEM) | Archived NWS MOS forecasts and heat advisory/warning records |
| NOAA NCEI daily summaries | Observed temperature and humidity |
| NYC Heat Vulnerability Index (NYC Open Data) | Neighborhood vulnerability ranking (1–5) |
| Cool It! NYC cooling sites (NYC Open Data) | Cooling-center locations |
| NYS Heat Stress data | Secondary outcome: heat-related hospitalizations |

Raw data is **not** committed to this repo. See `data/README.md`.

## Key caveats

- Syndromic ED data counts suspected, not confirmed, heat illness.
- 2020 is dropped or flagged because COVID-19 depressed ED visits.
- How much interventions actually reduce ED visits is uncertain in the literature. The effect is treated as an uncertain parameter (about 0–15% reduction), and the analysis shows how the optimal $\eta$ shifts across that range.
- Claims are predictive, not causal.

See `docs/assumptions.md` for the full list.

## Repository layout

```
data/
  raw/          # untouched downloads (git-ignored)
  external/     # reference data, e.g. HVI, cooling sites (git-ignored)
  processed/    # cleaned, model-ready city-day tables (git-ignored)
notebooks/      # exploratory analysis, numbered by milestone
src/heatrisk/   # reusable code: data loading, features, models, decision rule
tests/          # unit tests for src/
reports/
  figures/      # generated plots
  milestones/   # dossiers and slide decks
docs/           # assumptions, data log, notes
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

| Phase | Work |
|---|---|
| Data acquisition | Pull ED, forecast, observation, advisory, HVI and cooling-site data; merge into one city-day table |
| Data understanding | Reporting lag and completeness, missingness, forecast vs. observed alignment |
| Exploratory analysis | Relationship between forecast heat and ED visits; lagged effects |
| Modeling | Logistic regression baseline and gradient-boosted trees; time-based holdout validation |
| Decision rule | Cost-based threshold $\eta$; tiered neighborhood allocation |
| Uncertainty | Calibration; sensitivity of $\eta$ to costs and intervention effect |
| Reproducibility | End-to-end pipeline from data pull to decision |
| Final defense | Present and defend the system |

## Author

Tiffany Chan
