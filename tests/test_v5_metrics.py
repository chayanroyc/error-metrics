import numpy as np
import pytest

from error_metrics import ErrorMetrics, MetricRegistry


def test_mean_bias_factors_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_bias_factor(), 2.0)
    assert np.isclose(metrics.relative_mean_bias_factor(), 1.0)
    perfect = ErrorMetrics([1.0, 2.0], [1.0, 2.0])
    assert np.isclose(perfect.mean_bias_factor(), 1.0)
    assert np.isclose(perfect.relative_mean_bias_factor(), 0.0)


@pytest.mark.parametrize("predictions,observations", [
    ([0.0, 0.0], [1.0, 2.0]), ([1.0, 2.0], [0.0, 0.0]),
    ([-1.0, -2.0], [1.0, 2.0]), ([1.0, 2.0], [-1.0, -2.0]),
])
def test_mean_bias_factors_require_positive_means(predictions, observations):
    metrics = ErrorMetrics(predictions, observations)
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.mean_bias_factor()
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.relative_mean_bias_factor()


def test_mean_bias_factor_registry_mappings():
    assert MetricRegistry.get_metric("MBF").function.__name__ == "mean_bias_factor"
    assert MetricRegistry.get_metric("RMBF").function.__name__ == "relative_mean_bias_factor"


def test_mean_fractional_metrics_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_fractional_bias(), 2.0 / 3.0)
    assert np.isclose(metrics.mean_fractional_error(), 2.0 / 3.0)


def test_mean_fractional_metrics_handle_identical_zero_pair():
    metrics = ErrorMetrics([0.0, 1.0], [0.0, 1.0])
    assert metrics.mean_fractional_bias() == 0.0
    assert metrics.mean_fractional_error() == 0.0


def test_mean_fractional_metrics_reject_negatives_without_mutation():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    pred, obs = metrics.predictions.copy(), metrics.observations.copy()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_bias()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_error()
    assert np.array_equal(metrics.predictions, pred)
    assert np.array_equal(metrics.observations, obs)


def test_existing_fb_fae_and_new_registry_mappings_are_distinct():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    assert np.isclose(metrics.fb(), -8.0 / 3.0)
    assert np.isclose(metrics.fae(), 10.0 / 3.0)
    mappings = {k: v.function.__name__ for k, v in MetricRegistry.get_all_metrics().items()}
    assert {k: mappings[k] for k in ("MFB", "MFE", "FB", "FAE")} == {
        "MFB": "mean_fractional_bias", "MFE": "mean_fractional_error",
        "FB": "fb", "FAE": "fae",
    }


def test_phi_identical_and_separated_histograms():
    assert ErrorMetrics([0, 1, 2], [0, 1, 2]).phi(3) == 1.0
    assert ErrorMetrics([0, 0], [10, 10]).phi(2) == 0.0


def test_phi_bounds_validation_and_registry():
    metrics = ErrorMetrics([0, 1, 3], [0, 2, 3])
    assert 0.0 <= metrics.phi(3) <= 1.0
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.phi(invalid)
    assert MetricRegistry.get_metric("PHI").function.__name__ == "phi"


def test_nmaep_matches_p1_p2_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.nmaep(1.0), 1.0)
    assert np.isclose(metrics.nmaep(2.0), np.sqrt(2.5) / 1.5)


@pytest.mark.parametrize("p", [0.0, -1.0, np.inf, -np.inf, np.nan])
def test_nmaep_validation(p):
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    with pytest.raises(ValueError, match="finite and > 0"):
        metrics.nmaep(p)


def test_nmaep_zero_mean_and_registry():
    with pytest.raises(ValueError, match="observation mean is zero"):
        ErrorMetrics([1, 2], [-1, 1]).nmaep()
    assert MetricRegistry.get_metric("NMAEp").function.__name__ == "nmaep"
