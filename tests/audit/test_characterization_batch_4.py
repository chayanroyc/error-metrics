import json
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("MAD", "SD", "SBF", "U95", "TS", "NSE", "NNSE", "RAE", "VAF", "RSE")


def test_batch_4_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 40
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 49


def test_batch_4_metrics_match_ordinary_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])
    expected = {
        "mean_absolute_difference": 400.0 / 7.0,
        "standard_deviation_of_residual": 100.0 * np.sqrt(14.0) / 7.0,
        "slope_of_best_fit_line": 3.0 / 14.0,
        "uncertainty_95": 112.0 * np.sqrt(2.0),
        "t_statistic": 2.0 / np.sqrt(7.0),
        "nash_sutcliffe_efficiency": -2.0 / 7.0,
        "normalized_nse": 7.0 / 16.0,
        "relative_absolute_error": np.sqrt(2.0 / 7.0),
        "variance_accounted_for": 150.0 / 7.0,
        "residual_standard_error": np.sqrt(6.0),
    }
    for method, expected_value in expected.items():
        result = getattr(metrics, method)()
        assert np.isscalar(result)
        assert result == pytest.approx(expected_value)


def test_perfect_varying_series_reach_implemented_ideals():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    for method in ("mean_absolute_difference", "standard_deviation_of_residual", "uncertainty_95", "relative_absolute_error", "residual_standard_error"):
        assert getattr(metrics, method)() == pytest.approx(0.0)
    for method in ("slope_of_best_fit_line", "nash_sutcliffe_efficiency", "normalized_nse"):
        assert getattr(metrics, method)() == pytest.approx(1.0)
    assert metrics.variance_accounted_for() == pytest.approx(100.0)
    assert np.isnan(metrics.t_statistic())


def test_constant_observations_make_centered_denominators_undefined():
    metrics = ErrorMetrics([1.0, 3.0, 5.0], [2.0, 2.0, 2.0])
    with np.errstate(all="ignore"):
        assert np.isnan(metrics.slope_of_best_fit_line())
        assert np.isnan(metrics.nash_sutcliffe_efficiency())
        assert np.isnan(metrics.normalized_nse())
        assert np.isnan(metrics.variance_accounted_for())

    scaled = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 2.0, 3.0])
    assert scaled.slope_of_best_fit_line() == pytest.approx(2.0)
    assert scaled.variance_accounted_for() == pytest.approx(200.0)


def test_percent_residual_metrics_use_signed_observation_mean():
    negative = ErrorMetrics([2.0, 4.0], [-1.0, -3.0])
    assert negative.mean_absolute_difference() == pytest.approx(-250.0)
    assert negative.standard_deviation_of_residual() == pytest.approx(-100.0)
    assert negative.uncertainty_95() == pytest.approx(98.0 * np.sqrt(33.0))
    assert negative.t_statistic() == pytest.approx(5.0 / 2.0)

    zero_mean = ErrorMetrics([2.0, 2.0], [-1.0, 1.0])
    with np.errstate(all="ignore"):
        for method in ("mean_absolute_difference", "standard_deviation_of_residual", "uncertainty_95", "t_statistic"):
            assert np.isnan(getattr(zero_mean, method)())


def test_uncertainty_and_t_statistic_follow_composed_percent_formulas():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])
    sd = metrics.standard_deviation_of_residual()
    rmsd = metrics.root_mean_square_difference()
    mbd = metrics.mean_bias_difference()
    assert metrics.uncertainty_95() == pytest.approx(1.96 * np.sqrt(sd**2 + rmsd**2))
    assert metrics.t_statistic() == pytest.approx(np.sqrt((metrics.N - 1) * mbd**2 / (rmsd**2 - mbd**2)))


def test_efficiency_and_relative_error_denominator_failures():
    zero_observations = ErrorMetrics([1.0, 2.0], [0.0, 0.0])
    with np.errstate(all="ignore"):
        assert np.isnan(zero_observations.nash_sutcliffe_efficiency())
        assert np.isnan(zero_observations.normalized_nse())
        assert np.isnan(zero_observations.relative_absolute_error())
        assert np.isnan(zero_observations.variance_accounted_for())

    shifted = ErrorMetrics([2.0, 3.0, 4.0], [1.0, 2.0, 3.0])
    assert shifted.nash_sutcliffe_efficiency() == pytest.approx(-0.5)
    assert shifted.normalized_nse() == pytest.approx(0.4)
    assert shifted.relative_absolute_error() == pytest.approx(np.sqrt(3.0 / 14.0))


def test_residual_standard_error_degrees_of_freedom_are_unvalidated():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])
    assert metrics.residual_standard_error(p=0) == pytest.approx(np.sqrt(3.0))
    assert metrics.residual_standard_error(p=1) == pytest.approx(np.sqrt(6.0))
    with pytest.raises(ZeroDivisionError):
        metrics.residual_standard_error(p=2)
    with pytest.warns(RuntimeWarning, match="invalid value"):
        assert np.isnan(metrics.residual_standard_error(p=3))


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([2.0, np.nan, 4.0, np.inf], [1.0, 3.0, 2.0, 8.0])
    direct = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    methods = ("mean_absolute_difference", "standard_deviation_of_residual", "slope_of_best_fit_line", "uncertainty_95", "t_statistic", "nash_sutcliffe_efficiency", "normalized_nse", "relative_absolute_error", "variance_accounted_for")
    with np.errstate(all="ignore"):
        for method in methods:
            assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)(), nan_ok=True)
    with pytest.raises(ZeroDivisionError):
        filtered.residual_standard_error()
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])
