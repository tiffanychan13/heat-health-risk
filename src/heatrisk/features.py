"""Build the decision-day table: one row per activation decision.

The decision
------------
Every morning (day t, at the 12 UTC / 8 a.m. forecast run) the city decides
whether to activate its heat response for a target day s = t + lead.

Each row of the table holds:
  * information available at decision time (forecasts issued that morning,
    ED visits and heat observed up to yesterday), used as model features;
  * what the city actually did (whether an NWS heat alert was in effect on s);
  * what happened on the target day (ED visits N_s, observed heat H_s), used
    only as the outcome, never as a feature.

Columns are named relative to the target day s:
    F_target   forecast max heat for day s           (issued at t)
    F_prev     forecast max heat for day s - 1       (latest forecast available at t)
    F_next     forecast max heat for day s + 1       (issued at t)
"""

import numpy as np
import pandas as pd

from heatrisk.data import NY_TZ

# Feature columns a model may use. All are known at decision time t.
FEATURES = ["F_target", "F_prev", "F_next", "N_lag1", "N_mean3", "H_lag1", "day_of_season"]

SEASON_START = (5, 1)   # May 1
SEASON_END = (9, 30)    # Sep 30


def heat_index(T, Td):
    """NWS heat index in F (Rothfusz regression with NWS adjustments).

    T is air temperature and Td is dewpoint, both in F.
    """
    T, Td = np.asarray(T, float), np.asarray(Td, float)
    tc, tdc = (T - 32) / 1.8, (Td - 32) / 1.8
    RH = 100 * np.exp(17.625 * tdc / (243.04 + tdc)) / np.exp(17.625 * tc / (243.04 + tc))
    simple = 0.5 * (T + 61 + (T - 68) * 1.2 + RH * 0.094)
    full = (-42.379 + 2.04901523 * T + 10.14333127 * RH - 0.22475541 * T * RH - 6.83783e-3 * T**2
            - 5.481717e-2 * RH**2 + 1.22874e-3 * T**2 * RH + 8.5282e-4 * T * RH**2
            - 1.99e-6 * T**2 * RH**2)
    full = np.where((RH < 13) & (T >= 80) & (T <= 112),
                    full - (13 - RH) / 4 * np.sqrt(np.clip((17 - np.abs(T - 95)) / 17, 0, None)), full)
    full = np.where((RH > 85) & (T >= 80) & (T <= 87), full + (RH - 85) / 10 * (87 - T) / 5, full)
    return np.where((simple + T) / 2 >= 80, full, simple)


def forecast_table(mos: pd.DataFrame, run_hour_utc: int = 12) -> pd.DataFrame:
    """Daily max-heat forecasts in long format: one row per (run day t, forecast day s).

    Uses the daytime-max rows (valid at 00 UTC, i.e. the evening of local day s)
    from the chosen run. F = max(heat index, temperature), which matches how
    the ED file defines observed heat H.

    Returns columns t, s, lead (= s - t in days), F.
    """
    fc = mos[(mos["runtime"].dt.hour == run_hour_utc) & (mos["ftime"].dt.hour == 0)].copy()
    fc["t"] = fc["runtime"].dt.tz_convert(NY_TZ).dt.tz_localize(None).dt.normalize()
    fc["s"] = fc["ftime"].dt.tz_convert(NY_TZ).dt.tz_localize(None).dt.normalize()
    fc["lead"] = (fc["s"] - fc["t"]).dt.days
    fc["F"] = np.maximum(heat_index(fc["n_x"], fc["dpt"]), fc["n_x"])
    return fc[["t", "s", "lead", "F"]].reset_index(drop=True)


def alert_in_effect(days: pd.DatetimeIndex, heat_alerts: pd.DataFrame) -> np.ndarray:
    """1 if any NWS heat advisory or warning covered part of each local calendar day."""
    start = days.tz_localize(NY_TZ).tz_convert("UTC")
    end = (days + pd.Timedelta(days=1)).tz_localize(NY_TZ).tz_convert("UTC")
    issued = heat_alerts["issued"].values
    expired = heat_alerts["expired"].values
    return np.array([int(((issued < e.to_datetime64()) & (expired > s.to_datetime64())).any())
                     for s, e in zip(start, end)])


def _in_season(days: pd.DatetimeIndex) -> np.ndarray:
    md = days.month * 100 + days.day
    return (md >= SEASON_START[0] * 100 + SEASON_START[1]) & (md <= SEASON_END[0] * 100 + SEASON_END[1])


def build_decision_table(ed: pd.DataFrame, mos: pd.DataFrame, heat_alerts: pd.DataFrame,
                         lead: int = 1, run_hour_utc: int = 12) -> pd.DataFrame:
    """One row per decision: on morning t, activate the heat response for day s = t + lead?

    Parameters
    ----------
    ed, mos, heat_alerts : tables from heatrisk.data
    lead : days between the decision and the target day (1 = decide for tomorrow).
           Must be between 1 and 6, so a forecast for s + 1 exists.
    run_hour_utc : which daily MOS run is the decision time (12 UTC = 8 a.m. in NYC).

    Rows are kept only when t and s are both inside the May-Sep surveillance
    season and every feature and the outcome are available.
    """
    if not 1 <= lead <= 6:
        raise ValueError("lead must be between 1 and 6 days.")

    fc = forecast_table(mos, run_hour_utc)
    F = fc.pivot_table(index="t", columns="lead", values="F")   # rows: run day t, cols: lead

    # Latest forecast for day t itself = yesterday's run at lead 1.
    F_today = fc[fc["lead"] == 1].set_index("s")["F"]

    cal = pd.date_range(ed["date"].min(), ed["date"].max())
    N = ed.set_index("date")["N"].reindex(cal)
    H = ed.set_index("date")["H"].reindex(cal)

    t = F.index
    d = pd.DataFrame(index=pd.DatetimeIndex(t, name="t"))
    d["s"] = d.index + pd.Timedelta(days=lead)
    d["lead"] = lead

    # --- features: known at decision time t -------------------------------
    d["F_target"] = F[lead].values
    d["F_next"] = F[lead + 1].values
    d["F_prev"] = F[lead - 1].values if lead > 1 else F_today.reindex(d.index).values
    d["N_lag1"] = N.shift(1).reindex(d.index).values                    # yesterday's ED visits
    d["N_mean3"] = N.shift(1).rolling(3).mean().reindex(d.index).values  # mean of last 3 days
    d["H_lag1"] = H.shift(1).reindex(d.index).values                    # yesterday's observed heat
    d["season"] = d.index.year
    d["day_of_season"] = (d["s"] - pd.to_datetime(d["season"].astype(str) + "-05-01")).dt.days

    # --- what the city actually did on the target day ----------------------
    d["nws_alert"] = alert_in_effect(pd.DatetimeIndex(d["s"]), heat_alerts)

    # --- outcome on the target day (never a feature) -----------------------
    d["N_target"] = N.reindex(d["s"]).values
    d["H_target"] = H.reindex(d["s"]).values

    keep = _in_season(d.index) & _in_season(pd.DatetimeIndex(d["s"]))
    d = d[keep].dropna(subset=FEATURES + ["N_target"])
    d["N_target"] = d["N_target"].astype(int)
    return d


def high_burden_threshold(ed: pd.DataFrame, seasons, q: float = 0.90) -> float:
    """kappa: the q-th percentile of daily ED visits in the given seasons.

    A target day with N_s >= kappa is a "high-burden day" (Y = 1). Compute it from
    training seasons only, so the test season's data never shapes the definition.
    """
    return float(ed.loc[ed["season"].isin(list(seasons)), "N"].quantile(q))
