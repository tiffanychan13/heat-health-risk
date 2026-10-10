import numpy as np
import pytest

from heatrisk.decision import activate, cost_threshold


def test_equal_costs_give_half():
    assert cost_threshold(1, 1) == 0.5


def test_expensive_miss_lowers_threshold():
    assert cost_threshold(1, 9) == pytest.approx(0.1)


def test_activate():
    out = activate([0.05, 0.1, 0.8], eta=0.1)
    assert np.array_equal(out, [False, True, True])


def test_negative_cost_rejected():
    with pytest.raises(ValueError):
        cost_threshold(-1, 1)
