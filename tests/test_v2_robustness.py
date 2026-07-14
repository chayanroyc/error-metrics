import numpy as np
import pytest

from error_metrics import ErrorMetrics


def test_rejects_same_size_arrays_with_different_shapes():
    with pytest.raises(
        ValueError,
        match=r"same shape; got \(2, 2\) and \(4,\)",
    ):
        ErrorMetrics(np.ones((2, 2)), np.ones(4))


def test_rejects_input_with_no_valid_pairs():
    with pytest.raises(ValueError, match="No valid data points"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])
