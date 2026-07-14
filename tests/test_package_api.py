import subprocess
import sys

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


def test_imports_and_calculates_without_bottleneck():
    code = r'''\
import importlib.abc
import sys

class BlockBottleneck(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "bottleneck":
            raise ModuleNotFoundError("blocked for fallback test")
        return None

sys.meta_path.insert(0, BlockBottleneck())
from error_metrics import ErrorMetrics
from error_metrics.core import bn
import numpy as np
assert bn is np
assert ErrorMetrics([1, 2], [1, 1]).mean_absolute_error() == 0.5
'''
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
