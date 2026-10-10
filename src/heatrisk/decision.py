"""Decision rule: turn predicted risk p-hat into a cooling-center activation decision."""

import numpy as np


def cost_threshold(cost_false_alarm: float, cost_miss: float) -> float:
    """Bayes-optimal threshold eta for activating when p-hat >= eta.

    Activate if the expected cost of not activating (p * cost_miss) is at least
    the expected cost of activating needlessly ((1 - p) * cost_false_alarm),
    which gives eta = cost_false_alarm / (cost_false_alarm + cost_miss).
    """
    if cost_false_alarm < 0 or cost_miss < 0:
        raise ValueError("Costs must be non-negative.")
    total = cost_false_alarm + cost_miss
    if total == 0:
        raise ValueError("At least one cost must be positive.")
    return cost_false_alarm / total


def activate(p_hat, eta: float) -> np.ndarray:
    """Return a boolean array: True where activation is recommended."""
    return np.asarray(p_hat) >= eta
