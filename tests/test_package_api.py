import error_metrics
from error_metrics.core import ErrorMetrics as CoreErrorMetrics


def test_package_exports_supported_api():
    assert error_metrics.ErrorMetrics is CoreErrorMetrics
    assert error_metrics.MetricRegistry is not None
    assert error_metrics.MetricInfo is not None
    assert set(error_metrics.__all__) == {
        "ErrorMetrics",
        "MetricInfo",
        "MetricRegistry",
    }
