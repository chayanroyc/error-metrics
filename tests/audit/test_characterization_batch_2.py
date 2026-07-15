import json
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("CRM", "RE", "EC", "MASE", "MAAPE", "A10", "CI", "ME", "R2", "MNB")


def test_batch_2_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    assert [
        abbreviation
        for abbreviation, record in inventory["metrics"].items()
        if record["status"] == "complete"
    ] == ["MB", "MAE", "MedAE", "RMSE", "R", "SpearmanR", "KendallTau", "LCCC", "EV", "NMSE", *BATCH]
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 69


def test_batch_2_metrics_match_hand_calculations_and_return_scalars():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])
    expected = {
        "coefficient_of_residual_mass": 2.0 / 7.0,
        "relative_error": 0.75,
        "efficiency_coefficient": -2.0 / 7.0,
        "mean_absolute_scaled_error": 8.0 / 9.0,
        "mean_arctangent_absolute_percentage_error": 50.0 * np.pi / 3.0 + (25.0 / 3.0) * np.arctan(0.25),
        "a10_index": 0.0,
        "confidence_index": np.sqrt(3.0 / 28.0) * (28.0 / 55.0),
        "max_error": 2.0,
        "coefficient_of_determination": -2.0 / 7.0,
        "mean_normalized_bias": 7.0 / 12.0,
    }
    for method, value in expected.items():
        result = getattr(metrics, method)()
        assert np.isscalar(result)
        assert not isinstance(result, np.ndarray)
        assert result == pytest.approx(value)


def test_perfect_varying_predictions_reach_implemented_ideals():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    for method in ("coefficient_of_residual_mass", "relative_error", "mean_absolute_scaled_error", "mean_arctangent_absolute_percentage_error", "max_error", "mean_normalized_bias"):
        assert getattr(metrics, method)() == pytest.approx(0.0)
    for method in ("efficiency_coefficient", "a10_index", "confidence_index", "coefficient_of_determination"):
        assert getattr(metrics, method)() == pytest.approx(1.0)


def test_zero_observations_are_omitted_or_counted_as_documented_by_runtime():
    mixed = ErrorMetrics([5.0, 2.0], [0.0, 1.0])
    assert mixed.coefficient_of_residual_mass() == pytest.approx(6.0)
    assert mixed.relative_error() == pytest.approx(1.0)
    assert mixed.mean_arctangent_absolute_percentage_error() == pytest.approx(25.0 * np.pi)
    assert mixed.mean_normalized_bias() == pytest.approx(1.0)
    assert mixed.a10_index() == pytest.approx(0.0)

    zeros = ErrorMetrics([0.0, 0.0], [0.0, 0.0])
    with np.errstate(all="ignore"):
        for method in ("coefficient_of_residual_mass", "relative_error", "mean_absolute_scaled_error", "mean_arctangent_absolute_percentage_error", "efficiency_coefficient", "coefficient_of_determination", "mean_normalized_bias"):
            assert np.isnan(getattr(zeros, method)())
    with pytest.warns(RuntimeWarning), pytest.raises(ZeroDivisionError):
        zeros.confidence_index()
    assert zeros.a10_index() == pytest.approx(0.0)
    assert zeros.max_error() == pytest.approx(0.0)


def test_constant_observations_make_scaled_and_efficiency_denominators_undefined():
    metrics = ErrorMetrics([1.0, 3.0, 5.0], [2.0, 2.0, 2.0])
    with np.errstate(all="ignore"):
        assert np.isnan(metrics.mean_absolute_scaled_error())
        assert np.isnan(metrics.efficiency_coefficient())
        assert np.isnan(metrics.coefficient_of_determination())
        assert np.isnan(metrics.confidence_index())


def test_mase_seasonality_parameter_is_accepted_but_ignored():
    metrics = ErrorMetrics([1.0, 2.0, 5.0, 8.0], [1.0, 3.0, 4.0, 10.0])
    assert metrics.mean_absolute_scaled_error() == pytest.approx(1.0 / 3.0)
    assert metrics.mean_absolute_scaled_error(m=2) == pytest.approx(1.0 / 3.0)
    assert metrics.mean_absolute_scaled_error(m=0) == pytest.approx(1.0 / 3.0)
    assert metrics.mean_absolute_scaled_error(m="ignored") == pytest.approx(1.0 / 3.0)


def test_r2_and_ec_do_not_fit_a_regression_and_match_each_other():
    metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 2.0, 3.0])
    assert metrics.efficiency_coefficient() == pytest.approx(-6.0)
    assert metrics.coefficient_of_determination() == pytest.approx(-6.0)
    slope, fitted_r2 = metrics.linear_regression()
    assert slope == pytest.approx(0.5)
    assert fitted_r2 == pytest.approx(1.0)


def test_nonfinite_pairs_are_removed_and_mase_warns_about_broken_spacing():
    filtered = ErrorMetrics([2.0, np.nan, 4.0, np.inf], [1.0, 3.0, 2.0, 8.0])
    direct = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    methods = ("coefficient_of_residual_mass", "relative_error", "efficiency_coefficient", "mean_arctangent_absolute_percentage_error", "a10_index", "confidence_index", "max_error", "coefficient_of_determination", "mean_normalized_bias")
    with np.errstate(all="ignore"):
        for method in methods:
            assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)(), nan_ok=True)
    with pytest.warns(RuntimeWarning, match="time-ordered"):
        assert filtered.mean_absolute_scaled_error() == pytest.approx(direct.mean_absolute_scaled_error())


def test_no_finite_pairs_are_rejected_before_batch_2_evaluation():
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])


def test_a10_source_scope_and_ci_range_are_recorded_precisely():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    a10 = inventory["metrics"]["A10"]
    ci = inventory["metrics"]["CI"]

    assert a10["scientific_basis"]["canonical_definition"].startswith("unknown:")
    assert "does not define or validate a canonical A10 index" in a10["scientific_basis"]["references"][0]["supports"]
    assert "[-1, 1]" in ci["output"]["implemented_range"]
    assert "NaN" in ci["output"]["implemented_range"]
    assert "ZeroDivisionError" in ci["output"]["implemented_range"]
