"""Checks that the data loaders and the decision table are built correctly.

These tests read the real files in data/, so they also catch problems if a
data file is changed or re-downloaded.
"""

import pandas as pd
import pytest

from heatrisk.data import load_ed, load_heat_alerts, load_mos
from heatrisk.features import FEATURES, build_decision_table, heat_index


# --- heat index ---------------------------------------------------------------

def test_heat_index_matches_nws_table():
    # NWS chart: 90 F at about 50% humidity (dewpoint 69.3 F) feels like about 95 F.
    assert heat_index(90, 69.3) == pytest.approx(95, abs=1)


def test_heat_index_is_close_to_temperature_when_mild():
    assert abs(float(heat_index(70, 50)) - 70) < 3


# --- loaders --------------------------------------------------------------------

@pytest.fixture(scope="module")
def ed():
    return load_ed()


@pytest.fixture(scope="module")
def heat_alerts():
    return load_heat_alerts()


@pytest.fixture(scope="module")
def table(ed, heat_alerts):
    return build_decision_table(ed, load_mos(), heat_alerts, lead=1)


def test_ed_has_one_row_per_day(ed):
    assert ed["date"].is_unique
    assert (ed["N"] >= 0).all()
    assert set(ed["season"]) == set(range(2017, 2027))


def test_heat_alerts_are_cleaned(heat_alerts):
    assert (heat_alerts["significance"] != "A").all()                 # no watches
    assert (heat_alerts["expired"] > heat_alerts["issued"]).all()     # no cancelled alerts
    assert not heat_alerts.duplicated(["vtec_year", "phenomena", "significance", "eventid"]).any()


# --- decision table ---------------------------------------------------------------

def test_target_day_is_one_day_after_decision(table):
    assert ((table["s"] - table.index).dt.days == 1).all()


def test_no_missing_features_or_outcomes(table):
    assert table[FEATURES + ["N_target"]].notna().all().all()


def test_lag_features_use_only_the_past(table, ed):
    # N_lag1 on decision day t must equal the ED count on day t - 1, never day t or later.
    N = ed.set_index("date")["N"]
    assert (table["N_lag1"] == N.reindex(table.index - pd.Timedelta(days=1)).values).all()


def test_outcome_is_ed_visits_on_target_day(table, ed):
    N = ed.set_index("date")["N"]
    assert (table["N_target"] == N.reindex(table["s"]).values).all()


def test_rows_stay_inside_the_season(table):
    assert table.index.month.isin(range(5, 10)).all()
    assert pd.DatetimeIndex(table["s"]).month.isin(range(5, 10)).all()
