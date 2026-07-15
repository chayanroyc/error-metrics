import json
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = (
    "MB",
    "MAE",
    "MedAE",
    "RMSE",
    "R",
    "SpearmanR",
    "KendallTau",
    "LCCC",
    "EV",
    "NMSE",
)


def test_batch_1_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())

    assert [
        abbreviation
        for abbreviation, record in inventory["metrics"].items()
        if record["status"] == "complete"
    ] == list(BATCH)
    assert sum(
        record["status"] == "pending"
        for record in inventory["metrics"].values()
    ) == 79


def test_foundational_errors_match_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])

    assert metrics.mean_bias() == pytest.approx(2.0 / 3.0)
    assert metrics.mean_absolute_error() == pytest.approx(4.0 / 3.0)
    assert metrics.median_absolute_error() == pytest.approx(1.0)
    assert metrics.root_mean_squared_error() == pytest.approx(np.sqrt(2.0))


def test_association_agreement_and_normalized_metrics_match_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])

    assert metrics.correlation_coefficient() == pytest.approx(np.sqrt(3.0 / 28.0))
    assert metrics.spearman_r() == pytest.approx(0.5)
    assert metrics.kendall_tau() == pytest.approx(1.0 / 3.0)
    assert metrics.lccc() == pytest.approx(0.25)
    assert metrics.ev() == pytest.approx(0.0)
    assert metrics.nmse() == pytest.approx(2.0 / 7.0)


def test_perfect_predictions_reach_implemented_ideal_values():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])

    assert metrics.mean_bias() == pytest.approx(0.0)
    assert metrics.mean_absolute_error() == pytest.approx(0.0)
    assert metrics.median_absolute_error() == pytest.approx(0.0)
    assert metrics.root_mean_squared_error() == pytest.approx(0.0)
    assert metrics.correlation_coefficient() == pytest.approx(1.0)
    assert metrics.spearman_r() == pytest.approx(1.0)
    assert metrics.kendall_tau() == pytest.approx(1.0)
    assert metrics.lccc() == pytest.approx(1.0)
    assert metrics.ev() == pytest.approx(1.0)
    assert metrics.nmse() == pytest.approx(0.0)


def test_constant_series_characterizes_undefined_association_and_agreement():
    metrics = ErrorMetrics([2.0, 2.0, 2.0], [2.0, 2.0, 2.0])

    with np.errstate(all="ignore"):
        assert np.isnan(metrics.correlation_coefficient())
        with pytest.warns(RuntimeWarning, match="constant"):
            assert np.isnan(metrics.spearman_r())
        assert np.isnan(metrics.kendall_tau())
        assert np.isnan(metrics.lccc())
        assert np.isnan(metrics.ev())
    assert metrics.nmse() == pytest.approx(0.0)


def test_kendall_tau_uses_tie_adjusted_tau_b():
    metrics = ErrorMetrics([1.0, 1.0, 2.0], [1.0, 2.0, 3.0])

    # P=2, Q=0, T=1, U=0: tau-b = (P-Q)/sqrt((P+Q+T)(P+Q+U)).
    assert metrics.kendall_tau() == pytest.approx(2.0 / np.sqrt(6.0))
    assert metrics.kendall_tau() != pytest.approx(2.0 / 3.0)

    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    assert (
        "tests/audit/test_characterization_batch_1.py::"
        "test_kendall_tau_uses_tie_adjusted_tau_b"
        in inventory["metrics"]["KendallTau"]["verification"][
            "characterization_tests"
        ]
    )


def test_nmse_zero_mean_denominator_returns_nan():
    metrics = ErrorMetrics([1.0, 3.0], [-1.0, 1.0])

    with np.errstate(all="raise"):
        assert np.isnan(metrics.nmse())


def test_nonfinite_pairs_are_dropped_before_batch_1_metrics_are_computed():
    filtered = ErrorMetrics([2.0, np.nan, 4.0, np.inf], [1.0, 3.0, 2.0, 8.0])
    direct = ErrorMetrics([2.0, 4.0], [1.0, 2.0])

    methods = (
        "mean_bias",
        "mean_absolute_error",
        "median_absolute_error",
        "root_mean_squared_error",
        "correlation_coefficient",
        "spearman_r",
        "kendall_tau",
        "lccc",
        "ev",
        "nmse",
    )
    for method in methods:
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)())


def test_no_finite_pairs_are_rejected_before_metric_evaluation():
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])
