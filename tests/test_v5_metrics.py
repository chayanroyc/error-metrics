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
