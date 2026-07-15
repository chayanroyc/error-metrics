import json
import warnings
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("RNMBF", "CPI", "RED", "FoM", "MSDdec", "SS", "AD", "KLD", "MPE", "MAPE")


def test_batch_7_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 70
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 19


def test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations():
    metrics = ErrorMetrics([2, 6], [1, 3])
    assert metrics.rnmbf() == pytest.approx(1)
    assert metrics.red() == pytest.approx(1)
    assert metrics.mean_percentage_error() == pytest.approx(100)
    assert metrics.mean_absolute_percentage_error() == pytest.approx(100)

    overlap = ErrorMetrics([1, 1, 4], [1, 3, 2])
    assert overlap.figure_of_merit() == pytest.approx(50)


def test_cpi_is_unscaled_average_of_ksi_over_and_double_rmse(monkeypatch):
    metrics = ErrorMetrics([1, 2], [1, 2])
    calls = []

    def ksi(normed=True):
        calls.append(("ksi", normed))
        return 2.0

    def over(normed=True):
        calls.append(("over", normed))
        return 4.0

    monkeypatch.setattr(metrics, "ksi", ksi)
    monkeypatch.setattr(metrics, "over_metric", over)
    monkeypatch.setattr(metrics, "root_mean_squared_error", lambda: 3.0)
    assert metrics.cpi() == pytest.approx(3.0)
    assert calls == [("ksi", False), ("over", False)]


def test_msd_decomposition_returns_runtime_components_in_documented_tuple_order():
    metrics = ErrorMetrics([1, 3, 5], [2, 3, 4])
    total, systematic_bias, nonuniformity, lack_of_correlation = metrics.msd_decomposition()
    assert total == pytest.approx(2 / 3)
    assert systematic_bias == pytest.approx(0)
    assert nonuniformity == pytest.approx(2 / 3)
    assert lack_of_correlation == pytest.approx(0)
    assert total == pytest.approx(systematic_bias + nonuniformity + lack_of_correlation)


def test_skill_score_uses_observation_mean_climatology_and_squared_error():
    metrics = ErrorMetrics([1, 2, 6], [1, 3, 5])
    assert metrics.skill_score_against_climatology() == pytest.approx(1 - 2 / 8)
    perfect = ErrorMetrics([1, 3, 5], [1, 3, 5])
    assert perfect.skill_score_against_climatology() == pytest.approx(1)


def test_ad_is_directional_and_uses_observation_ecdf_for_weights():
    predictions = [0, 1, 3]
    observations = [0, 2, 4]
    forward = ErrorMetrics(predictions, observations).anderson_darling_distance()
    reverse = ErrorMetrics(observations, predictions).anderson_darling_distance()
    assert forward == pytest.approx(1)
    assert reverse > 1e8
    assert reverse != pytest.approx(forward)


def test_kld_normalizes_absolute_magnitudes_and_orders_observations_first():
    metrics = ErrorMetrics([-1, -3], [2, 2])
    expected = 0.5 * np.log(0.5 / 0.25) + 0.5 * np.log(0.5 / 0.75)
    reverse = ErrorMetrics([2, 2], [-1, -3]).kullback_leibler_divergence()
    assert metrics.kullback_leibler_divergence() == pytest.approx(expected)
    assert reverse != pytest.approx(expected)


def test_zero_observations_are_omitted_from_red_mpe_and_mape():
    metrics = ErrorMetrics([100, 4, 1], [0, 2, 2])
    assert metrics.red() == pytest.approx(np.sqrt((1 + 0.25) / 2))
    assert metrics.mean_percentage_error() == pytest.approx(25)
    assert metrics.mean_absolute_percentage_error() == pytest.approx(75)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        all_zero = ErrorMetrics([1, 2], [0, 0])
        assert np.isnan(all_zero.red())
        assert np.isnan(all_zero.mean_percentage_error())
        assert np.isnan(all_zero.mean_absolute_percentage_error())


def test_constant_and_zero_denominators_expose_metric_specific_behavior():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        constant = ErrorMetrics([2, 2, 2], [1, 1, 1])
        assert np.isnan(constant.skill_score_against_climatology())
        assert np.isnan(ErrorMetrics([0, 0], [0, 0]).figure_of_merit())
        assert ErrorMetrics([0, 0], [0, 0]).kullback_leibler_divergence() == pytest.approx(0)


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([1, np.nan, 3, 5, np.inf], [2, 9, 3, 4, 8])
    direct = ErrorMetrics([1, 3, 5], [2, 3, 4])
    methods = ("rnmbf", "cpi", "red", "figure_of_merit", "skill_score_against_climatology", "anderson_darling_distance", "kullback_leibler_divergence", "mean_percentage_error", "mean_absolute_percentage_error")
    for method in methods:
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)(), nan_ok=True)
    assert filtered.msd_decomposition() == pytest.approx(direct.msd_decomposition(), nan_ok=True)
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1, 2])
