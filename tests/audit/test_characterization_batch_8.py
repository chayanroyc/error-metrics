import json
import warnings
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.distance import pdist, squareform

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("sMAPE", "CRPS", "TAcc", "U2", "BM", "dCor", "lambda", "iqRMSE", "SMA", "RNP")


def test_batch_8_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 80
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 9


def test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations():
    metrics = ErrorMetrics([2, 4], [1, 3])
    expected_smape = 100 * ((1 / 1.5) + (1 / 3.5)) / 2
    assert metrics.symmetric_mean_absolute_percentage_error() == pytest.approx(expected_smape)
    assert metrics.continuous_ranked_probability_score() == pytest.approx(1)
    assert metrics.trend_accuracy() == pytest.approx(1)
    assert metrics.theils_u2() == pytest.approx(1 / np.sqrt(5))
    assert metrics.interquartile_rmse() == pytest.approx(1)


def test_berry_mielke_uses_cross_distance_matrix_and_parameter_c():
    metrics = ErrorMetrics([2, 4], [1, 3])
    # delta=1; cross-distance sum=|2-1|+|2-3|+|4-1|+|4-3|=6.
    assert metrics.berry_mielke_score() == pytest.approx(1 - 1 / 3)
    assert metrics.berry_mielke_score(c=1) == pytest.approx(1 - 1 / 1.5)
    assert metrics.berry_mielke_score(c=4) == pytest.approx(1 - 1 / 6)
    assert np.isnan(metrics.berry_mielke_score(c=0))


def test_distance_correlation_matches_biased_double_centered_distance_matrices():
    predictions = np.array([0.0, 1.0, 4.0])
    observations = np.array([0.0, 1.0, 2.0])

    def centered_distances(values):
        distances = squareform(pdist(values[:, None]))
        return distances - distances.mean(axis=1)[:, None] - distances.mean(axis=0)[None, :] + distances.mean()

    a = centered_distances(observations)
    b = centered_distances(predictions)
    expected = np.sqrt(np.mean(a * b)) / np.sqrt(np.sqrt(np.mean(a * a)) * np.sqrt(np.mean(b * b)))
    assert ErrorMetrics(predictions, observations).distance_correlation() == pytest.approx(expected)


def test_duveiller_coefficient_uses_population_variances_and_bias():
    metrics = ErrorMetrics([1, 3, 5], [2, 3, 4])
    # MSE=2/3, both population variances sum to 10/3, and mean bias is zero.
    assert metrics.duveiller_agreement_coefficient() == pytest.approx(1 - (2 / 3) / (10 / 3))
    assert ErrorMetrics([1, 2, 3], [3, 2, 1]).duveiller_agreement_coefficient() == pytest.approx(-1)


def test_sma_tuple_order_and_component_meanings_are_executable():
    result = ErrorMetrics([1, 3, 5], [2, 3, 4]).sma_metrics()
    slope, intercept, mse, mla, mlp, pla_percent, plp_percent = result
    assert result == pytest.approx((2, -3, 2 / 3, 2 / 3, 0, 100, 0))
    assert mse == pytest.approx(mla + mlp)
    assert pla_percent + plp_percent == pytest.approx(100)


def test_rnp_tuple_order_and_flow_duration_component_match_hand_calculation():
    score, rank, alpha, beta = ErrorMetrics([2, 4], [1, 3]).rnp()
    assert rank == pytest.approx(1)
    assert alpha == pytest.approx(1 - 0.5 * (abs(2 / 6 - 1 / 4) + abs(4 / 6 - 3 / 4)))
    assert beta == pytest.approx(3 / 2)
    assert score == pytest.approx(1 - np.sqrt((alpha - 1) ** 2 + (beta - 1) ** 2 + (rank - 1) ** 2))


def test_zero_short_constant_and_regression_failure_behaviors():
    zeros = ErrorMetrics([0, 0], [0, 0])
    assert np.isnan(zeros.symmetric_mean_absolute_percentage_error())
    assert zeros.continuous_ranked_probability_score() == pytest.approx(0)
    assert zeros.trend_accuracy() == pytest.approx(1)
    assert np.isnan(zeros.theils_u2())
    assert np.isnan(zeros.berry_mielke_score())
    assert zeros.distance_correlation() == pytest.approx(0)
    assert zeros.duveiller_agreement_coefficient() == pytest.approx(1)
    assert np.isinf(zeros.interquartile_rmse())

    one = ErrorMetrics([1], [2])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        with pytest.raises((SystemError, np.linalg.LinAlgError)):
            one.trend_accuracy()
    assert np.isnan(one.distance_correlation())

    constant = ErrorMetrics([2, 2, 2], [1, 1, 1])
    assert constant.distance_correlation() == pytest.approx(0)
    assert constant.duveiller_agreement_coefficient() == pytest.approx(0)
    assert np.isinf(constant.interquartile_rmse())


def test_constant_regression_and_rnp_components_preserve_runtime_nans():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sma = ErrorMetrics([2, 2, 2], [1, 1, 1]).sma_metrics()
        rnp = ErrorMetrics([2, 2, 2], [1, 1, 1]).rnp()
    assert sma == pytest.approx((0, 2, 1, 1, 0, 100, 0))
    assert np.isnan(rnp[0])
    assert np.isnan(rnp[1])
    assert rnp[2:] == pytest.approx((1, 2))


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([2, np.nan, 4, np.inf], [1, 8, 3, 9])
    direct = ErrorMetrics([2, 4], [1, 3])
    methods = (
        "symmetric_mean_absolute_percentage_error",
        "continuous_ranked_probability_score",
        "theils_u2",
        "berry_mielke_score",
        "distance_correlation",
        "duveiller_agreement_coefficient",
        "interquartile_rmse",
    )
    for method in methods:
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)(), nan_ok=True)
    with pytest.warns(RuntimeWarning, match="index was compressed"):
        assert filtered.trend_accuracy() == pytest.approx(direct.trend_accuracy())
    assert filtered.sma_metrics() == pytest.approx(direct.sma_metrics())
    assert filtered.rnp() == pytest.approx(direct.rnp())
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1, 2])
