import json
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("MNAE", "FB", "FAE", "MFB", "MFE", "MAGE", "GMB", "FAC2", "MBD", "RMSD")


def test_batch_3_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 30
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 59


def test_batch_3_metrics_match_ordinary_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 3.0], [1.0, 2.0, 4.0])
    expected = {
        "mean_normalized_absolute_error": 3.0 / 4.0,
        "fb": 22.0 / 63.0,
        "fae": 34.0 / 63.0,
        "mean_fractional_bias": 22.0 / 63.0,
        "mean_fractional_error": 34.0 / 63.0,
        "mean_absolute_gross_error": 3.0 / 4.0,
        "geometric_mean_bias": np.cbrt(3.0),
        "factor_of_observations2": 100.0,
        "mean_bias_difference": 200.0 / 7.0,
        "root_mean_square_difference": 300.0 * np.sqrt(2.0) / 7.0,
    }
    for method, expected_value in expected.items():
        result = getattr(metrics, method)()
        assert np.isscalar(result)
        assert result == pytest.approx(expected_value)


def test_perfect_positive_predictions_reach_implemented_ideals():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    for method in ("mean_normalized_absolute_error", "fb", "fae", "mean_fractional_bias", "mean_fractional_error", "mean_absolute_gross_error", "mean_bias_difference", "root_mean_square_difference"):
        assert getattr(metrics, method)() == pytest.approx(0.0)
    assert metrics.geometric_mean_bias() == pytest.approx(1.0)
    assert metrics.factor_of_observations2() == pytest.approx(100.0)


def test_fractional_metrics_distinguish_zero_pair_and_negative_policies():
    zeros = ErrorMetrics([0.0, 2.0], [0.0, 1.0])
    with np.errstate(all="ignore"):
        assert zeros.fb() == pytest.approx(2.0 / 3.0)
        assert zeros.fae() == pytest.approx(2.0 / 3.0)
    assert zeros.mean_fractional_bias() == pytest.approx(1.0 / 3.0)
    assert zeros.mean_fractional_error() == pytest.approx(1.0 / 3.0)

    negative = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    assert negative.fb() == pytest.approx(-8.0 / 3.0)
    assert negative.fae() == pytest.approx(10.0 / 3.0)
    with pytest.raises(ValueError, match="nonnegative"):
        negative.mean_fractional_bias()
    with pytest.raises(ValueError, match="nonnegative"):
        negative.mean_fractional_error()


def test_fb_and_fae_retain_nonzero_cancellation_infinities():
    positive = ErrorMetrics([1.0], [-1.0])
    negative = ErrorMetrics([-1.0], [1.0])
    mixed = ErrorMetrics([1.0, 2.0], [-1.0, 1.0])
    with np.errstate(all="ignore"):
        assert np.isposinf(positive.fb())
        assert np.isneginf(negative.fb())
        assert np.isposinf(positive.fae())
        assert np.isposinf(negative.fae())
        assert np.isposinf(mixed.fb())
        assert np.isposinf(mixed.fae())

    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    test_id = (
        "tests/audit/test_characterization_batch_3.py::"
        "test_fb_and_fae_retain_nonzero_cancellation_infinities"
    )
    for abbreviation in ("FB", "FAE"):
        assert test_id in inventory["metrics"][abbreviation]["verification"]["characterization_tests"]


def test_observation_normalized_metrics_omit_zeros_and_accept_negative_denominators():
    mixed = ErrorMetrics([5.0, -1.0, 2.0], [0.0, -2.0, 1.0])
    assert mixed.mean_normalized_absolute_error() == pytest.approx(0.25)
    assert mixed.mean_absolute_gross_error() == pytest.approx(0.25)

    zeros = ErrorMetrics([1.0, 0.0], [0.0, 0.0])
    with np.errstate(all="ignore"):
        assert np.isnan(zeros.mean_normalized_absolute_error())
        assert np.isnan(zeros.mean_absolute_gross_error())


def test_gmb_omits_nonpositive_pairs_and_requires_one_positive_pair():
    mixed = ErrorMetrics([2.0, 0.0, -3.0], [1.0, 4.0, 2.0])
    with pytest.warns(UserWarning, match="positive"):
        assert mixed.geometric_mean_bias() == pytest.approx(2.0)
    nonpositive = ErrorMetrics([0.0, -1.0], [1.0, 2.0])
    with pytest.warns(UserWarning, match="positive"), np.errstate(all="ignore"):
        assert np.isnan(nonpositive.geometric_mean_bias())


def test_fac2_includes_boundaries_and_counts_zero_divisions_as_failures():
    boundaries = ErrorMetrics([0.5, 2.0, 0.49, 2.01], [1.0, 1.0, 1.0, 1.0])
    assert boundaries.factor_of_observations2() == pytest.approx(50.0)
    zeros = ErrorMetrics([0.0, 1.0, 0.0], [0.0, 0.0, 1.0])
    with np.errstate(all="ignore"):
        assert zeros.factor_of_observations2() == pytest.approx(0.0)


def test_percent_normalized_differences_follow_signed_observation_mean():
    metrics = ErrorMetrics([2.0, 4.0], [-1.0, -3.0])
    assert metrics.mean_bias_difference() == pytest.approx(-250.0)
    assert metrics.root_mean_square_difference() == pytest.approx(-50.0 * np.sqrt(29.0))
    zero_mean = ErrorMetrics([2.0, 2.0], [-1.0, 1.0])
    assert np.isnan(zero_mean.mean_bias_difference())
    assert np.isnan(zero_mean.root_mean_square_difference())


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([2.0, np.nan, 4.0, np.inf], [1.0, 3.0, 2.0, 8.0])
    direct = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    methods = ("mean_normalized_absolute_error", "fb", "fae", "mean_fractional_bias", "mean_fractional_error", "mean_absolute_gross_error", "geometric_mean_bias", "factor_of_observations2", "mean_bias_difference", "root_mean_square_difference")
    for method in methods:
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)())
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])
