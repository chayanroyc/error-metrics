import numpy as np
import pytest
from error_metrics import ErrorMetrics
import numpy.ma as ma
import numpy.random as rn
import bottleneck as bn

@pytest.fixture
def sample_data():
    # Create sample data with known properties for testing
    np.random.seed(42)
    observations = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    predictions = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    return observations, predictions

@pytest.fixture
def error_metrics(sample_data):
    observations, predictions = sample_data
    return ErrorMetrics(predictions, observations)

@pytest.fixture
def zero_data():
    # Test case with zeros
    return np.zeros(5), np.zeros(5)

@pytest.fixture
def negative_data():
    # Test case with negative values
    return np.array([-1.0, -2.0, -3.0, -4.0, -5.0]), np.array([-1.2, -1.8, -3.2, -3.9, -5.1])

@pytest.fixture
def mixed_data():
    # Test case with mixed positive and negative values
    return np.array([-1.0, 2.0, -3.0, 4.0, -5.0]), np.array([-1.2, 1.8, -3.2, 3.9, -5.1])

@pytest.fixture
def nan_data():
    # Test case with NaN values
    return np.array([1.0, np.nan, 3.0, np.nan, 5.0]), np.array([1.2, 1.8, np.nan, 3.9, np.nan])

@pytest.fixture
def inf_data():
    # Test case with infinite values
    return np.array([1.0, np.inf, 3.0, -np.inf, 5.0]), np.array([1.2, 1.8, np.inf, 3.9, -np.inf])

@pytest.fixture
def single_value():
    # Test case with single value
    return np.array([1.0]), np.array([1.0])

@pytest.fixture
def large_numbers():
    # Test case with large numbers
    return np.array([1e10, 2e10, 3e10]), np.array([1.2e10, 1.8e10, 3.2e10])

@pytest.fixture
def small_numbers():
    # Test case with small numbers
    return np.array([1e-10, 2e-10, 3e-10]), np.array([1.2e-10, 1.8e-10, 3.2e-10])

def test_initialization(error_metrics, sample_data):
    observations, predictions = sample_data
    assert np.array_equal(error_metrics.observations, observations)
    assert np.array_equal(error_metrics.predictions, predictions)
    assert error_metrics.N == len(observations)

def test_preprocess_data():
    # Test handling of NaN values
    predictions = np.array([1.0, np.nan, 3.0, 4.0, np.nan])
    observations = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
    em = ErrorMetrics(predictions, observations)
    assert len(em.predictions) == 2  # Only valid pairs should remain
    assert len(em.observations) == 2

def test_zero_values(zero_data):
    obs, pred = zero_data
    em = ErrorMetrics(pred, obs)
    # Test metrics that should handle zeros
    assert np.isclose(em.mean_bias(), 0.0)
    assert np.isclose(em.mean_absolute_error(), 0.0)
    assert np.isclose(em.root_mean_squared_error(), 0.0)
    # Test metrics that might have issues with zeros
    assert np.isnan(em.mean_normalized_bias())
    assert np.isnan(em.mean_normalized_absolute_error())

def test_negative_values(negative_data):
    obs, pred = negative_data
    em = ErrorMetrics(pred, obs)
    # Test metrics with negative values
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())
    assert not np.isnan(em.root_mean_squared_error())
    assert not np.isnan(em.correlation_coefficient())

def test_mixed_values(mixed_data):
    obs, pred = mixed_data
    em = ErrorMetrics(pred, obs)
    # Test metrics with mixed positive and negative values
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())
    assert not np.isnan(em.root_mean_squared_error())
    assert not np.isnan(em.correlation_coefficient())

def test_nan_handling(nan_data):
    obs, pred = nan_data
    em = ErrorMetrics(pred, obs)
    # Test that NaN values are properly handled
    assert len(em.predictions) == 2  # Only valid pairs should remain
    assert len(em.observations) == 2
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())

def test_inf_handling(inf_data):
    obs, pred = inf_data
    em = ErrorMetrics(pred, obs)
    # Test that infinite values are properly handled
    assert len(em.predictions) == 2  # Only valid pairs should remain
    assert len(em.observations) == 2
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())

def test_single_value_handling(single_value):
    obs, pred = single_value
    em = ErrorMetrics(pred, obs)
    # Test metrics with single value
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())
    assert np.isnan(em.correlation_coefficient())  # Correlation undefined for single value

def test_large_numbers(large_numbers):
    obs, pred = large_numbers
    em = ErrorMetrics(pred, obs)
    # Test metrics with large numbers
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())
    assert not np.isnan(em.root_mean_squared_error())

def test_small_numbers(small_numbers):
    obs, pred = small_numbers
    em = ErrorMetrics(pred, obs)
    # Test metrics with small numbers
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())
    assert not np.isnan(em.root_mean_squared_error())

def test_correlation_metrics(error_metrics):
    # Test correlation-based metrics
    assert np.isclose(error_metrics.correlation_coefficient(), 0.993383264459765)
    assert np.isclose(error_metrics.coefficient_of_determination(), 0.986)
    assert np.isclose(error_metrics.spearman_r(), 0.9)
    assert np.isclose(error_metrics.lccc(), 0.991)

def test_efficiency_metrics(error_metrics):
    # Test efficiency metrics
    assert np.isclose(error_metrics.nash_sutcliffe_efficiency(), 0.986)
    kge, r, alpha, beta = error_metrics.kling_gupta_efficiency()
    assert np.isclose(kge, 0.9847304735231118)
    assert np.isclose(r, 0.993383264459765)
    assert np.isclose(alpha, 0.9965942002640792)
    assert np.isclose(beta, 1.0133333333333334)
    
    # Test Modified KGE (2012 version)
    kge2012, r2012, alpha2012, beta2012 = error_metrics.modified_kling_gupta_efficiency()
    assert np.isclose(r2012, 0.993383264459765)  # r should be the same
    assert np.isclose(beta2012, 1.0133333333333334)  # beta should be the same
    # alpha should be different (CV ratio vs std ratio)
    assert not np.isclose(alpha2012, alpha)  # alpha should differ
    assert not np.isnan(kge2012)
    assert not np.isnan(alpha2012)
    
    # Test KGE'' (Tang et al. 2021)
    kgedp, rdp, alphadp, beta_ndp = error_metrics.kling_gupta_efficiency_double_prime()
    assert np.isclose(rdp, 0.993383264459765)  # r should be the same
    assert np.isclose(alphadp, 0.9965942002640792)  # alpha should be same as 2009 version (std ratio)
    # beta_n should be different (normalized bias vs mean ratio)
    assert not np.isclose(beta_ndp, beta)  # beta_n should differ from beta
    assert not np.isnan(kgedp)
    assert not np.isnan(beta_ndp)
    
    # Test Diagnostic Efficiency (Schwemmle et al. 2021)
    de, r_de, b_area, b_rel_mean = error_metrics.diagnostic_efficiency()
    assert np.isclose(r_de, 0.993383264459765)  # r should be the same (correlation on original time series)
    # DE is calculated on Flow Duration Curve (sorted data), so components will differ
    assert not np.isnan(de)
    assert not np.isnan(b_area)
    assert not np.isnan(b_rel_mean)
    # DE should be >= 0 (lower is better, 0 is perfect)
    assert de >= 0
    
    # Test Liu Model Efficiency (Liu 2020)
    lme, r_lme, alpha_lme, beta_lme, slope_term = error_metrics.liu_model_efficiency()
    assert np.isclose(r_lme, 0.993383264459765)  # r should be the same
    assert np.isclose(alpha_lme, 0.9965942002640792)  # alpha should be same as KGE 2009 (std ratio)
    assert np.isclose(beta_lme, 1.0133333333333334)  # beta should be same as KGE
    # slope_term should be r * alpha
    assert np.isclose(slope_term, r_lme * alpha_lme)
    assert not np.isnan(lme)
    # LME should be <= 1 (higher is better, 1 is perfect)
    assert lme <= 1
    
    # Test Least-squares Combined Efficiency (Lee & Choi 2022)
    lce, r_lce, alpha_lce, beta_lce, slope_1, slope_2 = error_metrics.least_squares_combined_efficiency()
    assert np.isclose(r_lce, 0.993383264459765)  # r should be the same
    assert np.isclose(alpha_lce, 0.9965942002640792)  # alpha should be same as KGE 2009 (std ratio)
    assert np.isclose(beta_lce, 1.0133333333333334)  # beta should be same as KGE
    # slope_1 should be r * alpha
    assert np.isclose(slope_1, r_lce * alpha_lce)
    # slope_2 should be r / alpha
    assert np.isclose(slope_2, r_lce / alpha_lce)
    assert not np.isnan(lce)
    # LCE should be <= 1 (higher is better, 1 is perfect)
    assert lce <= 1
    
    assert np.isclose(error_metrics.willmotts_index_of_agreement(), 0.993)

def test_distribution_metrics(error_metrics):
    # Test distribution-based metrics
    assert not np.isnan(error_metrics.ksi())
    assert not np.isnan(error_metrics.over_metric())
    assert not np.isnan(error_metrics.anderson_darling_distance())
    assert not np.isnan(error_metrics.kullback_leibler_divergence())

def test_percentage_metrics(error_metrics):
    # Test percentage-based metrics
    assert not np.isnan(error_metrics.mean_percentage_error())
    assert not np.isnan(error_metrics.mean_absolute_percentage_error())
    assert not np.isnan(error_metrics.symmetric_mean_absolute_percentage_error())

def test_advanced_metrics(error_metrics):
    # Test advanced metrics
    assert not np.isnan(error_metrics.figure_of_merit())
    assert not np.isnan(error_metrics.nu())
    assert not np.isnan(error_metrics.lc())
    assert not np.isnan(error_metrics.skill_score_against_climatology())
    assert not np.isnan(error_metrics.taylor_skill_score())
    assert not np.isnan(error_metrics.trend_accuracy())
    assert not np.isnan(error_metrics.continuous_ranked_probability_score())

def test_metric_bounds():
    # Test that metrics stay within expected bounds
    obs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    em = ErrorMetrics(pred, obs)
    
    # Perfect prediction case
    assert np.isclose(em.correlation_coefficient(), 1.0)
    assert np.isclose(em.coefficient_of_determination(), 1.0)
    assert np.isclose(em.nash_sutcliffe_efficiency(), 1.0)
    assert np.isclose(em.willmotts_index_of_agreement(), 1.0)
    
    # Worst prediction case
    pred_worst = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    em_worst = ErrorMetrics(pred_worst, obs)
    assert em_worst.correlation_coefficient() < 0
    assert em_worst.nash_sutcliffe_efficiency() < 0

def test_metric_consistency():
    # Test that related metrics are consistent
    obs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    pred = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    em = ErrorMetrics(pred, obs)
    
    # Test that MAE is always less than or equal to RMSE
    assert em.mean_absolute_error() <= em.root_mean_squared_error()
    
    # Test that R² is always less than or equal to 1
    assert em.coefficient_of_determination() <= 1.0
    
    # Test that NSE is always less than or equal to 1
    assert em.nash_sutcliffe_efficiency() <= 1.0

def test_metric_symmetry():
    # Test that metrics are symmetric where appropriate
    obs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    pred = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    em1 = ErrorMetrics(pred, obs)
    em2 = ErrorMetrics(obs, pred)
    
    # Test symmetric metrics
    assert np.isclose(em1.correlation_coefficient(), em2.correlation_coefficient())
    assert np.isclose(em1.spearman_r(), em2.spearman_r())
    assert np.isclose(em1.lccc(), em2.lccc())
    
    # Test asymmetric metrics
    assert not np.isclose(em1.mean_bias(), em2.mean_bias())
    assert not np.isclose(em1.mean_normalized_bias(), em2.mean_normalized_bias())

def test_metric_scale_invariance():
    # Test that metrics are scale-invariant where appropriate
    obs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    pred = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    em1 = ErrorMetrics(pred, obs)
    em2 = ErrorMetrics(pred * 2, obs * 2)
    
    # Test scale-invariant metrics
    assert np.isclose(em1.correlation_coefficient(), em2.correlation_coefficient())
    assert np.isclose(em1.spearman_r(), em2.spearman_r())
    assert np.isclose(em1.lccc(), em2.lccc())
    assert np.isclose(em1.nash_sutcliffe_efficiency(), em2.nash_sutcliffe_efficiency())
    
    # Test scale-dependent metrics
    assert not np.isclose(em1.mean_bias(), em2.mean_bias())
    assert not np.isclose(em1.mean_absolute_error(), em2.mean_absolute_error())

def test_mean_squared_logarithmic_error():
    """Test Mean Squared Logarithmic Error (MSLE) calculation."""
    # Test case 1: Perfect predictions
    predictions = np.array([1.0, 2.0, 3.0])
    observations = np.array([1.0, 2.0, 3.0])
    metrics = ErrorMetrics(predictions, observations)
    assert metrics.mean_squared_logarithmic_error() == 0.0

    # Test case 2: Predictions with some error
    predictions = np.array([1.1, 2.2, 3.3])
    observations = np.array([1.0, 2.0, 3.0])
    metrics = ErrorMetrics(predictions, observations)
    msle = metrics.mean_squared_logarithmic_error()
    assert msle > 0.0
    assert not np.isnan(msle)
    assert not np.isinf(msle)

    # Test case 3: Handle zero values
    predictions = np.array([0.0, 1.0, 2.0])
    observations = np.array([0.0, 1.0, 2.0])
    metrics = ErrorMetrics(predictions, observations)
    msle = metrics.mean_squared_logarithmic_error()
    assert msle == 0.0

    # Test case 4: Handle negative values
    predictions = np.array([-1.0, 0.0, 1.0])
    observations = np.array([-1.0, 0.0, 1.0])
    metrics = ErrorMetrics(predictions, observations)
    msle = metrics.mean_squared_logarithmic_error()
    assert not np.isnan(msle)
    assert not np.isinf(msle) 