import numpy as np
import pytest

from error_metrics import ErrorMetrics, MetricRegistry


def test_rejects_same_size_arrays_with_different_shapes():
    with pytest.raises(
        ValueError,
        match=r"same shape; got \(2, 2\) and \(4,\)",
    ):
        ErrorMetrics(np.ones((2, 2)), np.ones(4))


def test_rejects_input_with_no_valid_pairs():
    with pytest.raises(ValueError, match="No valid data points"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])


def test_duplicate_abbreviations_use_documented_scalar_methods():
    assert MetricRegistry.get_metric("nESkew").function.__name__ == "normalized_error_skewness"
    assert MetricRegistry.get_metric("nEKurt").function.__name__ == "normalized_error_kurtosis"
    assert MetricRegistry.get_metric("NMBF").function.__name__ == "nmbf"
    assert MetricRegistry.get_metric("RNMBF").function.__name__ == "rnmbf"


def test_normalized_error_shape_metrics_return_nan_for_zero_predictions():
    metrics = ErrorMetrics([0, 0, 0, 0], [0, 0, 0, 0])

    assert np.isnan(metrics.normalized_error_skewness())
    assert np.isnan(metrics.normalized_error_kurtosis())


def test_registry_rejects_different_function_for_existing_abbreviation():
    abbreviation = "__test_conflict__"

    @MetricRegistry.register("First", abbreviation)
    def first(self):
        return 1.0

    with pytest.raises(ValueError, match="already registered"):

        @MetricRegistry.register("Second", abbreviation)
        def second(self):
            return 2.0

    MetricRegistry._metrics.pop(abbreviation)


def test_registry_allows_same_qualified_method_to_reregister():
    abbreviation = "__test_reload__"

    def original(self):
        return 1.0

    replacement = lambda self: 2.0
    replacement.__qualname__ = original.__qualname__
    MetricRegistry.register("Original", abbreviation)(original)
    MetricRegistry.register("Replacement", abbreviation)(replacement)
    assert MetricRegistry.get_metric(abbreviation).function is replacement
    MetricRegistry._metrics.pop(abbreviation)


def test_pearson_calculation_is_cached(monkeypatch):
    calls = 0
    original = np.corrcoef

    def counting_corrcoef(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(np, "corrcoef", counting_corrcoef)
    metrics = ErrorMetrics([1.1, 2.0, 3.2], [1.0, 2.0, 3.0])
    metrics.correlation_coefficient()
    metrics.lccc()
    assert calls == 1


@pytest.mark.parametrize(
    "method_name",
    ["mean_absolute_scaled_error", "trend_accuracy"],
)
def test_time_ordered_metric_warns_after_pairs_are_dropped(method_name):
    metrics = ErrorMetrics([1.0, np.nan, 3.0, 4.0], [1.0, 2.0, 2.5, 4.2])
    with pytest.warns(RuntimeWarning, match="time|trend|ordered"):
        getattr(metrics, method_name)()


def test_safe_divide_returns_nan_for_zero_denominator():
    from error_metrics.core import _safe_divide

    with np.errstate(all="raise"):
        assert np.isnan(_safe_divide(1.0, 0.0))


def test_zero_denominator_metrics_return_nan():
    metrics = ErrorMetrics([0.0, 0.0], [0.0, 0.0])
    with np.errstate(all="ignore"):
        assert np.isnan(metrics.lccc())
        assert np.isnan(metrics.ev())
        assert np.isnan(metrics.nmse())
        assert np.isnan(metrics.coefficient_of_residual_mass())
        assert np.isnan(metrics.efficiency_coefficient())
        assert np.isnan(metrics.coefficient_of_determination())
