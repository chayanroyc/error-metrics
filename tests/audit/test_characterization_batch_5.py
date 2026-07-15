import json
import warnings
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("KGE", "KGE2012", "KGEdp", "DE", "LME", "LCEf", "WIA", "WIAr", "LCE", "KSI")


def test_batch_5_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 50
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 39


def test_kge_family_distinguishes_component_definitions():
    metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])
    assert metrics.kling_gupta_efficiency() == pytest.approx((2 / 3, 1, 1, 4 / 3))
    assert metrics.modified_kling_gupta_efficiency() == pytest.approx((7 / 12, 1, 3 / 4, 4 / 3))
    assert metrics.kling_gupta_efficiency_double_prime() == pytest.approx(
        (1 - np.sqrt(3 / 8), 1, 1, np.sqrt(3 / 8))
    )


def test_composite_efficiencies_match_ordinary_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])
    assert metrics.diagnostic_efficiency() == pytest.approx(
        (1 - np.sqrt((23 / 45) ** 2 + (13 / 45) ** 2), 1, 13 / 45, 23 / 45)
    )
    assert metrics.liu_model_efficiency() == pytest.approx((2 / 3, 1, 1, 4 / 3, 1))
    assert metrics.least_squares_combined_efficiency() == pytest.approx((2 / 3, 1, 1, 4 / 3, 1, 1))


def test_agreement_efficiencies_match_ordinary_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])
    assert metrics.willmotts_index_of_agreement() == pytest.approx(32 / 35)
    assert metrics.refined_index_of_agreement() == pytest.approx(5 / 8)
    assert metrics.legates_coefficient_of_efficiency() == pytest.approx(1 / 4)


def test_refined_index_poor_fit_branch_has_implemented_positive_sign():
    metrics = ErrorMetrics([10.0, 10.0, 10.0], [1.0, 2.0, 3.0])
    assert metrics.refined_index_of_agreement() == pytest.approx(1 - 4 / 24)


def test_perfect_varying_series_reach_implemented_ideals_and_tuple_shapes():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    assert metrics.kling_gupta_efficiency() == pytest.approx((1, 1, 1, 1))
    assert metrics.modified_kling_gupta_efficiency() == pytest.approx((1, 1, 1, 1))
    assert metrics.kling_gupta_efficiency_double_prime() == pytest.approx((1, 1, 1, 0))
    assert metrics.diagnostic_efficiency() == pytest.approx((1, 1, 0, 0))
    assert metrics.liu_model_efficiency() == pytest.approx((1, 1, 1, 1, 1))
    assert metrics.least_squares_combined_efficiency() == pytest.approx((1, 1, 1, 1, 1, 1))
    for method in ("willmotts_index_of_agreement", "refined_index_of_agreement", "legates_coefficient_of_efficiency"):
        assert getattr(metrics, method)() == pytest.approx(1)
    assert metrics.ksi() == pytest.approx(0)


def test_constant_identical_series_expose_denominator_failures():
    metrics = ErrorMetrics([1.0, 1.0, 1.0], [1.0, 1.0, 1.0])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        assert np.isnan(metrics.kling_gupta_efficiency()[0])
        assert np.isnan(metrics.diagnostic_efficiency()[0])
        assert np.isnan(metrics.liu_model_efficiency()[0])
        assert np.isnan(metrics.least_squares_combined_efficiency()[0])
        assert np.isnan(metrics.legates_coefficient_of_efficiency())
        assert np.isnan(metrics.ksi())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for method in ("modified_kling_gupta_efficiency", "kling_gupta_efficiency_double_prime", "willmotts_index_of_agreement", "refined_index_of_agreement"):
            with pytest.raises(ZeroDivisionError):
                getattr(metrics, method)()


def test_zero_observation_mean_distinguishes_ratio_and_normalized_bias_variants():
    metrics = ErrorMetrics([1.0, 2.0, 3.0], [-1.0, 0.0, 1.0])
    with np.errstate(all="ignore"):
        assert np.isnan(metrics.kling_gupta_efficiency()[0])
        assert metrics.kling_gupta_efficiency_double_prime() == pytest.approx((1 - np.sqrt(6), 1, 1, np.sqrt(6)))
        assert metrics.liu_model_efficiency()[0] == -np.inf
        assert metrics.least_squares_combined_efficiency()[0] == -np.inf
    with pytest.raises(ZeroDivisionError):
        metrics.modified_kling_gupta_efficiency()


def test_diagnostic_efficiency_requires_two_positive_observations():
    metrics = ErrorMetrics([2.0, 3.0, 4.0], [-1.0, 0.0, 1.0])
    result = metrics.diagnostic_efficiency()
    assert np.isnan(result[0]) and result[1] == pytest.approx(1) and np.isnan(result[2]) and np.isnan(result[3])


def test_ksi_integrates_only_over_unique_sample_grid():
    metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])
    assert metrics.ksi(normed=False) == pytest.approx(1)
    assert metrics.ksi() == pytest.approx(100 / (1.63 * 5 / np.sqrt(3)))

    tied = ErrorMetrics([1.0, 2.0, 2.0], [1.0, 1.0, 3.0])
    assert tied.ksi(normed=False) == pytest.approx(2 / 3)


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([2.0, np.nan, 4.0, 6.0, np.inf], [1.0, 9.0, 3.0, 5.0, 8.0])
    direct = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])
    methods = ("kling_gupta_efficiency", "modified_kling_gupta_efficiency", "kling_gupta_efficiency_double_prime", "diagnostic_efficiency", "liu_model_efficiency", "least_squares_combined_efficiency", "willmotts_index_of_agreement", "refined_index_of_agreement", "legates_coefficient_of_efficiency", "ksi")
    for method in methods:
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)())
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])
