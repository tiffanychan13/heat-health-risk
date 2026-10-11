# Assumptions and open questions

## Scope revision (Milestone 2)
- Study area changed from Phoenix / Maricopa County to New York City, because NYC publishes machine-readable daily heat-related ED data at the city level.
- Prediction unit changed from county-day to **city-day**. Allocation unit is the **neighborhood** (NTA / community district).

## Working assumptions
- Forecast information is available 3–7 days ahead, enough time to make an activation decision.
- The NYC Heat Vulnerability Index is a reasonable proxy for neighborhood illness risk. It was built around heat *death* risk, and its inputs are one-time snapshots, so vulnerability is treated as slow-changing.
- Existing cooling-center capacity is large enough to matter for the highest-risk neighborhoods.
- Intervention effect is uncertain: modeled as roughly a 0–15% reduction in ED visits, based on mixed evidence in the literature.

## Data caveats
- Syndromic ED data counts suspected, not confirmed, heat illness and is best for trends.
- 2020 is dropped or flagged because of COVID-19.
- Heat alerts may raise short-term ED visits, which complicates ED visits as a success metric.

## Scope limits
- Claims are predictive/associational. The causal effect of activation is not estimated.

## Open questions
- Reporting lag and completeness of the daily ED series.
- How many years of archived MOS forecasts line up with the ED series.
