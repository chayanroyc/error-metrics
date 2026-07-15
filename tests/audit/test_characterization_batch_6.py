import json
import warnings
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("PHI", "SUSE", "OVER", "IQR", "STD", "nESkew", "nEKurt", "MBF", "RMBF", "NMBF")


def test_batch_6_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 60
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 29


def test_histogram_metrics_match_hand_calculation_and_validate_bins():
    metrics = ErrorMetrics([0, 0, 0, 3], [0, 1, 2, 3])
    assert metrics.phi(4) == pytest.approx(1 / 2)
    assert metrics.suse(4) == pytest.approx(np.log(4) - (np.log(4) - 3 / 4 * np.log(3)))
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.phi(invalid)
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.suse(invalid)


def test_histogram_entropy_distinguishes_common_and_separate_edges():
    metrics = ErrorMetrics([0, 0, 10, 10], [4, 5, 5, 6])
    common = np.histogram_bin_edges(np.r_[metrics.predictions, metrics.observations], bins=4)
    pred_edges = np.histogram_bin_edges(metrics.predictions, bins=4)
    obs_edges = np.histogram_bin_edges(metrics.observations, bins=4)
    scaled = abs(metrics._shannon_entropy(metrics.predictions, common) - metrics._shannon_entropy(metrics.observations, common))
    unscaled = abs(metrics._shannon_entropy(metrics.predictions, pred_edges) - metrics._shannon_entropy(metrics.observations, obs_edges))
    assert scaled != pytest.approx(unscaled)
    assert metrics.suse(4) == pytest.approx(max(scaled, unscaled))


def test_distribution_summary_and_moments_match_hand_calculations():
    summaries = ErrorMetrics([9, 9, 9, 9], [1, 2, 3, 4])
    assert summaries.IQR() == pytest.approx(3 / 2)
    assert summaries.STD() == pytest.approx(np.sqrt(5 / 4))

    moments = ErrorMetrics([1, 2, 3, 5], [1, 2, 3, 1])
    assert moments.normalized_error_skewness() == pytest.approx(2)
    assert moments.normalized_error_kurtosis() == pytest.approx(4)


def test_normalized_moments_use_prediction_max_and_unbiased_fisher_conventions():
    metrics = ErrorMetrics([-5, -4, -3, -1], [-5, -4, -3, -5])
    assert metrics.normalized_error_skewness() == pytest.approx(-2)
    assert metrics.normalized_error_kurtosis() == pytest.approx(4)
    assert np.isnan(ErrorMetrics([1, 2], [1, 1]).normalized_error_skewness())
    assert np.isnan(ErrorMetrics([1, 2, 3], [1, 1, 1]).normalized_error_kurtosis())
    assert np.isnan(ErrorMetrics([0, 0, 0, 0], [1, 2, 3, 4]).normalized_error_skewness())


def test_over_uses_directional_left_rectangle_area_and_fixed_normalizer():
    metrics = ErrorMetrics([0, 2, 4], [1, 3, 5])
    assert metrics.over_metric(normed=False) == pytest.approx(1)
    assert metrics.over_metric() == pytest.approx(100 / (1.63 * 5 / np.sqrt(3)))
    assert metrics.over_metric(normed="normalized") == pytest.approx(metrics.over_metric())


def test_constant_distributions_expose_metric_specific_behavior():
    identical = ErrorMetrics([2, 2, 2, 2], [2, 2, 2, 2])
    assert identical.phi() == pytest.approx(1)
    assert identical.suse() == pytest.approx(0)
    assert identical.IQR() == pytest.approx(0)
    assert identical.STD() == pytest.approx(0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        assert np.isnan(identical.normalized_error_skewness())
        assert np.isnan(identical.normalized_error_kurtosis())
        assert np.isnan(identical.over_metric())
    assert identical.over_metric(normed=False) == pytest.approx(0)


def test_bias_factors_distinguish_positive_domain_from_unrestricted_ratio():
    metrics = ErrorMetrics([2, 4], [1, 2])
    assert metrics.mean_bias_factor() == pytest.approx(2)
    assert metrics.relative_mean_bias_factor() == pytest.approx(1)
    assert metrics.nmbf() == pytest.approx(2)

    negative = ErrorMetrics([-2, -4], [1, 2])
    with pytest.raises(ValueError, match="strictly positive"):
        negative.mean_bias_factor()
    with pytest.raises(ValueError, match="strictly positive"):
        negative.relative_mean_bias_factor()
    assert negative.nmbf() == pytest.approx(-2)

    zero_observation_mean = ErrorMetrics([1, 3], [-1, 1])
    with pytest.raises(ValueError, match="strictly positive"):
        zero_observation_mean.mean_bias_factor()
    assert np.isnan(zero_observation_mean.nmbf())


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([1, np.nan, 2, 3, np.inf, 5], [1, 9, 2, 3, 8, 1])
    direct = ErrorMetrics([1, 2, 3, 5], [1, 2, 3, 1])
    for method in ("phi", "suse", "over_metric", "IQR", "STD", "normalized_error_skewness", "normalized_error_kurtosis", "mean_bias_factor", "relative_mean_bias_factor", "nmbf"):
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)())
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1, 2])
