import numpy as np
import pytest

from error_metrics import ErrorMetrics, MetricRegistry


def test_mean_bias_factors_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_bias_factor(), 2.0)
    assert np.isclose(metrics.relative_mean_bias_factor(), 1.0)
    perfect = ErrorMetrics([1.0, 2.0], [1.0, 2.0])
    assert np.isclose(perfect.mean_bias_factor(), 1.0)
    assert np.isclose(perfect.relative_mean_bias_factor(), 0.0)


@pytest.mark.parametrize("predictions,observations", [
    ([0.0, 0.0], [1.0, 2.0]), ([1.0, 2.0], [0.0, 0.0]),
    ([-1.0, -2.0], [1.0, 2.0]), ([1.0, 2.0], [-1.0, -2.0]),
])
def test_mean_bias_factors_require_positive_means(predictions, observations):
    metrics = ErrorMetrics(predictions, observations)
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.mean_bias_factor()
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.relative_mean_bias_factor()


def test_mean_bias_factor_registry_mappings():
    assert MetricRegistry.get_metric("MBF").function.__name__ == "mean_bias_factor"
    assert MetricRegistry.get_metric("RMBF").function.__name__ == "relative_mean_bias_factor"


def test_mean_fractional_metrics_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_fractional_bias(), 2.0 / 3.0)
    assert np.isclose(metrics.mean_fractional_error(), 2.0 / 3.0)


def test_mean_fractional_metrics_handle_identical_zero_pair():
    metrics = ErrorMetrics([0.0, 1.0], [0.0, 1.0])
    assert metrics.mean_fractional_bias() == 0.0
    assert metrics.mean_fractional_error() == 0.0


def test_mean_fractional_metrics_reject_negatives_without_mutation():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    pred, obs = metrics.predictions.copy(), metrics.observations.copy()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_bias()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_error()
    assert np.array_equal(metrics.predictions, pred)
    assert np.array_equal(metrics.observations, obs)


def test_existing_fb_fae_and_new_registry_mappings_are_distinct():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    assert np.isclose(metrics.fb(), -8.0 / 3.0)
    assert np.isclose(metrics.fae(), 10.0 / 3.0)
    mappings = {k: v.function.__name__ for k, v in MetricRegistry.get_all_metrics().items()}
    assert {k: mappings[k] for k in ("MFB", "MFE", "FB", "FAE")} == {
        "MFB": "mean_fractional_bias", "MFE": "mean_fractional_error",
        "FB": "fb", "FAE": "fae",
    }


def test_phi_identical_and_separated_histograms():
    assert ErrorMetrics([0, 1, 2], [0, 1, 2]).phi(3) == 1.0
    assert ErrorMetrics([0, 0], [10, 10]).phi(2) == 0.0


def test_phi_bounds_validation_and_registry():
    metrics = ErrorMetrics([0, 1, 3], [0, 2, 3])
    assert 0.0 <= metrics.phi(3) <= 1.0
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.phi(invalid)
    assert MetricRegistry.get_metric("PHI").function.__name__ == "phi"


def test_nmaep_matches_p1_p2_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.nmaep(1.0), 1.0)
    assert np.isclose(metrics.nmaep(2.0), np.sqrt(2.5) / 1.5)


@pytest.mark.parametrize("p", [0.0, -1.0, np.inf, -np.inf, np.nan, True])
def test_nmaep_validation(p):
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    with pytest.raises(ValueError, match="finite and > 0"):
        metrics.nmaep(p)


def test_nmaep_zero_mean_and_registry():
    with pytest.raises(ValueError, match="observation mean is zero"):
        ErrorMetrics([1, 2], [-1, 1]).nmaep()
    assert MetricRegistry.get_metric("NMAEp").function.__name__ == "nmaep"


def test_suse_behavior_validation_and_registry():
    assert ErrorMetrics([0, 1, 2, 3], [0, 1, 2, 3]).suse(4) == 0.0
    value = ErrorMetrics([0, 0, 0, 3], [0, 1, 2, 3]).suse(4)
    assert value > 0.0 and np.isfinite(value)
    metrics = ErrorMetrics([0, 1], [0, 1])
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.suse(invalid)
    assert MetricRegistry.get_metric("SUSE").function.__name__ == "suse"


BASELINE_ABBREVIATIONS = {
    "MB", "MAE", "MedAE", "RMSE", "R", "SpearmanR", "KendallTau", "LCCC", "EV", "NMSE", "CRM", "RE", "EC", "MASE", "MAAPE", "A10", "CI", "ME", "R2", "MNB", "MNAE", "FB", "FAE", "MAGE", "GMB", "FAC2", "MBD", "RMSD", "MAD", "SD", "SBF", "U95", "TS", "NSE", "NNSE", "RAE", "VAF", "RSE", "KGE", "KGE2012", "KGEdp", "DE", "LME", "LCEf", "WIA", "WIAr", "LCE", "KSI", "OVER", "IQR", "STD", "nESkew", "nEKurt", "NMBF", "RNMBF", "CPI", "RED", "FoM", "MSDdec", "SS", "AD", "KLD", "MPE", "MAPE", "sMAPE", "CRPS", "TAcc", "U2", "BM", "dCor", "lambda", "iqRMSE", "SMA", "RNP", "TSS", "MEAN", "MEDIAN", "CRMSE", "MSLE", "NAE", "Gini", "PCD",
}
BASELINE_MAPPINGS = {
    "MB": "mean_bias", "MAE": "mean_absolute_error", "MedAE": "median_absolute_error", "RMSE": "root_mean_squared_error", "R": "correlation_coefficient", "SpearmanR": "spearman_r", "KendallTau": "kendall_tau", "LCCC": "lccc", "EV": "ev", "NMSE": "nmse", "CRM": "coefficient_of_residual_mass", "RE": "relative_error", "EC": "efficiency_coefficient", "MASE": "mean_absolute_scaled_error", "MAAPE": "mean_arctangent_absolute_percentage_error", "A10": "a10_index", "CI": "confidence_index", "ME": "max_error", "R2": "coefficient_of_determination", "MNB": "mean_normalized_bias", "MNAE": "mean_normalized_absolute_error", "FB": "fb", "FAE": "fae", "MAGE": "mean_absolute_gross_error", "GMB": "geometric_mean_bias", "FAC2": "factor_of_observations2", "MBD": "mean_bias_difference", "RMSD": "root_mean_square_difference", "MAD": "mean_absolute_difference", "SD": "standard_deviation_of_residual", "SBF": "slope_of_best_fit_line", "U95": "uncertainty_95", "TS": "t_statistic", "NSE": "nash_sutcliffe_efficiency", "NNSE": "normalized_nse", "RAE": "relative_absolute_error", "VAF": "variance_accounted_for", "RSE": "residual_standard_error", "KGE": "kling_gupta_efficiency", "KGE2012": "modified_kling_gupta_efficiency", "KGEdp": "kling_gupta_efficiency_double_prime", "DE": "diagnostic_efficiency", "LME": "liu_model_efficiency", "LCEf": "least_squares_combined_efficiency", "WIA": "willmotts_index_of_agreement", "WIAr": "refined_index_of_agreement", "LCE": "legates_coefficient_of_efficiency", "KSI": "ksi", "OVER": "over_metric", "IQR": "IQR", "STD": "STD", "nESkew": "normalized_error_skewness", "nEKurt": "normalized_error_kurtosis", "NMBF": "nmbf", "RNMBF": "rnmbf", "CPI": "cpi", "RED": "red", "FoM": "figure_of_merit", "MSDdec": "msd_decomposition", "SS": "skill_score_against_climatology", "AD": "anderson_darling_distance", "KLD": "kullback_leibler_divergence", "MPE": "mean_percentage_error", "MAPE": "mean_absolute_percentage_error", "sMAPE": "symmetric_mean_absolute_percentage_error", "CRPS": "continuous_ranked_probability_score", "TAcc": "trend_accuracy", "U2": "theils_u2", "BM": "berry_mielke_score", "dCor": "distance_correlation", "lambda": "duveiller_agreement_coefficient", "iqRMSE": "interquartile_rmse", "SMA": "sma_metrics", "RNP": "rnp", "TSS": "taylor_skill_score", "MEAN": "meann", "MEDIAN": "mediann", "CRMSE": "centered_root_mean_square", "MSLE": "mean_squared_logarithmic_error", "NAE": "normalized_absolute_error", "Gini": "gini_coefficient", "PCD": "prediction_of_change_in_direction",
}
RECOVERED_MAPPINGS = {"MBF": "mean_bias_factor", "RMBF": "relative_mean_bias_factor", "MFB": "mean_fractional_bias", "MFE": "mean_fractional_error", "PHI": "phi", "NMAEp": "nmaep", "SUSE": "suse"}


def test_registry_is_exact_89_metric_superset():
    registry = MetricRegistry.get_all_metrics()
    mappings = {key: info.function.__name__ for key, info in registry.items()}
    assert len(BASELINE_ABBREVIATIONS) == 82
    assert set(BASELINE_MAPPINGS) == BASELINE_ABBREVIATIONS
    assert {key: mappings[key] for key in BASELINE_MAPPINGS} == BASELINE_MAPPINGS
    assert {key: mappings[key] for key in RECOVERED_MAPPINGS} == RECOVERED_MAPPINGS
    assert len(registry) == len(set(registry)) == 89
    assert not {"MSD", "SB", "NU", "LC"} & registry.keys()
