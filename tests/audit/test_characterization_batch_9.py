import json
import warnings
from pathlib import Path

import numpy as np
import pytest

from error_metrics import ErrorMetrics


ROOT = Path(__file__).resolve().parents[2]
BATCH = ("TSS", "MEAN", "MEDIAN", "CRMSE", "MSLE", "NMAEp", "NAE", "Gini", "PCD")


def test_batch_9_inventory_records_are_complete():
    inventory = json.loads((ROOT / "audit" / "metrics.yaml").read_text())
    completed = [key for key, record in inventory["metrics"].items() if record["status"] == "complete"]
    assert completed[-len(BATCH):] == list(BATCH)
    assert len(completed) == 89
    assert sum(record["status"] == "pending" for record in inventory["metrics"].values()) == 0


def test_summary_tuples_and_centered_error_match_hand_calculations():
    metrics = ErrorMetrics([2, 4, 9], [1, 5, 6])
    assert metrics.meann() == pytest.approx((4, 5))
    assert metrics.mediann() == pytest.approx((5, 4))
    # Centered errors are [0, -2, 2], so CRMSE=sqrt(8/3).
    assert metrics.centered_root_mean_square() == pytest.approx(np.sqrt(8 / 3))
    # Adding a common offset to predictions changes bias but not centered error.
    shifted = ErrorMetrics([12, 14, 19], [1, 5, 6])
    assert shifted.centered_root_mean_square() == pytest.approx(np.sqrt(8 / 3))


def test_taylor_skill_score_uses_correlation_and_population_standard_deviation_ratio():
    metrics = ErrorMetrics([1, 3, 6], [1, 2, 4])
    r = np.corrcoef([1, 3, 6], [1, 2, 4])[0, 1]
    ratio = np.std([1, 3, 6]) / np.std([1, 2, 4])
    expected = 4 * (1 + r) ** 4 / ((1 / ratio + ratio) ** 2 * 16)
    assert metrics.taylor_skill_score() == pytest.approx(expected)
    assert ErrorMetrics([2, 4, 6], [1, 2, 3]).taylor_skill_score() == pytest.approx(0.64)


def test_msle_matches_log1p_hand_calculation_and_preserves_negative_domain_warnings():
    metrics = ErrorMetrics([1, 3], [0, 1])
    expected = ((np.log(2) - np.log(1)) ** 2 + (np.log(4) - np.log(2)) ** 2) / 2
    assert metrics.mean_squared_logarithmic_error() == pytest.approx(expected)

    with pytest.warns(RuntimeWarning):
        # The invalid first contribution is silently omitted by nanmean.
        assert ErrorMetrics([-2, 0], [0, 0]).mean_squared_logarithmic_error() == pytest.approx(0)
    with pytest.warns(RuntimeWarning):
        assert np.isnan(ErrorMetrics([-1], [-1]).mean_squared_logarithmic_error())


def test_nmaep_parameter_and_zero_mean_validation():
    metrics = ErrorMetrics([2, 4], [1, 2])
    assert metrics.nmaep() == pytest.approx(1)
    assert metrics.nmaep(2) == pytest.approx(np.sqrt(2.5) / 1.5)
    for invalid in (True, 0, -1, np.inf, np.nan):
        with pytest.raises(ValueError, match="finite and > 0"):
            metrics.nmaep(invalid)
    with pytest.raises(ValueError, match="observation mean is zero"):
        ErrorMetrics([1, 2], [-1, 1]).nmaep()


def test_nae_uses_signed_pairwise_half_sum_denominators():
    assert ErrorMetrics([3, 6], [1, 2]).normalized_absolute_error() == pytest.approx(1)
    # Contributions are 2/(0.5*(-4))=-1 and 4/(0.5*(-8))=-1.
    assert ErrorMetrics([-3, -6], [-1, -2]).normalized_absolute_error() == pytest.approx(-1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        assert np.isinf(ErrorMetrics([1, 2], [-1, 1]).normalized_absolute_error())
        assert np.isnan(ErrorMetrics([0, 0], [0, 0]).normalized_absolute_error())


def test_gini_depends_on_descending_prediction_order_and_observation_total():
    observations = [1, 1, 0, 0, 0]
    assert ErrorMetrics([5, 4, 3, 2, 1], observations).gini_coefficient() == pytest.approx(0.3)
    assert ErrorMetrics([1, 2, 3, 4, 5], observations).gini_coefficient() == pytest.approx(-0.3)
    assert ErrorMetrics([5, 4, 3, 2, 1], [-1, -1, 0, 0, 0]).gini_coefficient() == pytest.approx(0.3)
    assert np.isnan(ErrorMetrics([3, 2, 1], [0, 0, 0]).gini_coefficient())


def test_pcd_short_flat_and_strict_direction_behavior():
    assert ErrorMetrics([1, 2, 1, 3], [1, 3, 2, 4]).prediction_of_change_in_direction() == pytest.approx(1)
    assert np.isnan(ErrorMetrics([1], [1]).prediction_of_change_in_direction())
    assert ErrorMetrics([1, 1, 2], [1, 1, 2]).prediction_of_change_in_direction() == pytest.approx(0.5)
    assert ErrorMetrics([1, 1, 1], [2, 2, 2]).prediction_of_change_in_direction() == pytest.approx(0)


def test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected():
    filtered = ErrorMetrics([2, np.nan, 4, np.inf], [1, 8, 2, 9])
    direct = ErrorMetrics([2, 4], [1, 2])
    for method in (
        "taylor_skill_score",
        "meann",
        "mediann",
        "centered_root_mean_square",
        "mean_squared_logarithmic_error",
        "nmaep",
        "normalized_absolute_error",
        "gini_coefficient",
        "prediction_of_change_in_direction",
    ):
        assert getattr(filtered, method)() == pytest.approx(getattr(direct, method)(), nan_ok=True)
    with pytest.raises(ValueError, match="No valid data points after preprocessing"):
        ErrorMetrics([np.nan, np.inf], [1, 2])
