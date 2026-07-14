import numpy as np
import pytest
from error_metrics import ErrorMetrics
import numpy.ma as ma
import numpy.random as rn
import bottleneck as bn
from scipy.stats import skew as scipy_skew, kurtosis as scipy_kurtosis

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
    # Each of these fixtures has only index 0 finite in both arrays.
    assert len(em.predictions) == 1
    assert len(em.observations) == 1
    assert not np.isnan(em.mean_bias())
    assert not np.isnan(em.mean_absolute_error())

def test_inf_handling(inf_data):
    obs, pred = inf_data
    em = ErrorMetrics(pred, obs)
    # Test that infinite values are properly handled
    # Each of these fixtures has only index 0 finite in both arrays.
    assert len(em.predictions) == 1
    assert len(em.observations) == 1
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
    # Both sample vectors have identical increasing rank order.
    assert np.isclose(error_metrics.spearman_r(), 1.0)
    assert np.isclose(error_metrics.lccc(), 0.9929789368104314)

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
    # DE should be <= 1 (higher is better, 1 is perfect)
    assert de <= 1
    
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
    lcef, r_lcef, alpha_lcef, beta_lcef, slope_1, slope_2 = error_metrics.least_squares_combined_efficiency()
    assert np.isclose(r_lcef, 0.993383264459765)  # r should be the same
    assert np.isclose(alpha_lcef, 0.9965942002640792)  # alpha should be same as KGE 2009 (std ratio)
    assert np.isclose(beta_lcef, 1.0133333333333334)  # beta should be same as KGE
    # slope_1 should be r * alpha
    assert np.isclose(slope_1, r_lcef * alpha_lcef)
    # slope_2 should be r / alpha
    assert np.isclose(slope_2, r_lcef / alpha_lcef)
    assert not np.isnan(lcef)
    # LCEf should be <= 1 (higher is better, 1 is perfect)
    assert lcef <= 1
    
    # Use the formula's computed value instead of a three-decimal loose estimate.
    assert np.isclose(
        error_metrics.willmotts_index_of_agreement(),
        0.9964771011575239,
    )

def test_msd_decomposition(sample_data):
    obs, pred = sample_data
    em = ErrorMetrics(pred, obs)
    msd, sb, nu, lc = em.msd_decomposition()
    assert np.isclose(msd, em.msd())
    assert np.isclose(sb, em.sb())
    assert np.isclose(nu, em.nu())
    assert np.isclose(lc, em.lc())
    assert np.isclose(msd, sb + nu + lc)
    
    # Test Refined Index of Agreement (Willmott et al. 2012)
    # Use the local instance; `error_metrics` is the fixture function at module scope.
    dr = em.refined_index_of_agreement()
    assert not np.isnan(dr)
    # dr should be in range [-1, 1]
    assert -1.0 <= dr <= 1.0

    # Test Duveiller Agreement Coefficient (lambda)
    lambda_coeff = em.duveiller_agreement_coefficient()
    assert -1.0 <= lambda_coeff <= 1.0
    # Lambda should equal 1 when predictions equal observations
    perfect_em = ErrorMetrics(obs, obs)
    assert np.isclose(perfect_em.duveiller_agreement_coefficient(), 1.0)

def test_interquartile_rmse(sample_data):
    obs, pred = sample_data
    em = ErrorMetrics(pred, obs)
    iqrmse = em.interquartile_rmse()
    assert iqrmse >= 0

    # If IQR is zero, metric should return inf
    obs_flat = np.ones(5)
    pred_flat = np.ones(5)
    em_flat = ErrorMetrics(pred_flat, obs_flat)
    assert np.isinf(em_flat.interquartile_rmse())

def test_normalized_error_skewness_kurtosis(sample_data):
    obs, pred = sample_data
    em = ErrorMetrics(pred, obs)
    ne = (pred - obs) / np.max(pred)
    expected_skew = scipy_skew(ne, bias=False)
    expected_kurt = scipy_kurtosis(ne, fisher=True, bias=False)
    assert np.isclose(em.normalized_error_skewness(), expected_skew)
    assert np.isclose(em.normalized_error_kurtosis(), expected_kurt)

def test_theils_u2_and_berry_mielke():
    obs = np.array([1.0, 2.0])
    pred = np.array([2.0, 1.0])
    em = ErrorMetrics(pred, obs)

    rmse = np.sqrt(np.mean((pred - obs) ** 2))
    obs_rms = np.sqrt(np.mean(obs ** 2))
    expected_u2 = rmse / obs_rms
    assert np.isclose(em.theils_u2(), expected_u2)

    delta = np.mean(np.abs(pred - obs))
    pairwise = np.abs(np.subtract.outer(pred, obs))
    expected_mu = (2 / (len(obs) ** 2)) * np.sum(pairwise)
    expected_bm = 1 - delta / expected_mu
    assert np.isclose(em.berry_mielke_score(), expected_bm)

def test_sma_metrics(sample_data):
    obs, pred = sample_data
    em = ErrorMetrics(pred, obs)
    slope, intercept, mse, mla, mlp, pla, plp = em.sma_metrics()
    assert isinstance(slope, float)
    assert isinstance(intercept, float)
    assert np.isclose(mse, em.root_mean_squared_error() ** 2)
    assert np.isclose(mse, mla + mlp)
    if mse > 0:
        assert np.isclose(pla + plp, 100)

def test_normalized_error_skewness_kurtosis(sample_data):
    obs, pred = sample_data
    em = ErrorMetrics(pred, obs)

    nE = (pred - obs) / np.max(pred)
    mean_nE = np.mean(nE)
    sd_nE = np.std(nE)
    z = (nE - mean_nE) / sd_nE
    N = len(nE)
    manual_skew = (N / ((N - 1) * (N - 2))) * np.sum(z ** 3)
    manual_kurt = (N * (N + 1)) / ((N - 1) * (N - 2) * (N - 3)) * np.sum(z ** 4) - \
        (3 * (N - 1) ** 2) / ((N - 2) * (N - 3))

    assert np.isclose(em.normalized_error_skewness(), manual_skew)
    assert np.isclose(em.normalized_error_kurtosis(), manual_kurt)

def test_distance_correlation_metric():
    # Strong non-linear relationship (parabola)
    x = np.linspace(-5, 5, 50)
    y = x ** 2
    em = ErrorMetrics(y, x)
    dcor = em.distance_correlation()
    # A symmetric parabola is dependent on x but is not expected to be near 1 under
    # the finite-sample distance-correlation definition.
    assert 0.45 < dcor < 0.55

    # Nearly independent relationship
    rng = np.random.RandomState(0)
    obs = np.linspace(0, 1, 50)
    random_preds = rng.rand(50)
    em_rand = ErrorMetrics(random_preds, obs)
    dcor_rand = em_rand.distance_correlation()
    assert dcor_rand < 0.7

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

def test_geometric_mean_bias():
    # Test Geometric Mean Bias
    predictions = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    observations = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    metrics = ErrorMetrics(predictions, observations)
    gmb = metrics.geometric_mean_bias()
    assert not np.isnan(gmb)
    assert gmb > 0  # GMB should be positive
    
    # Test perfect case (predictions = observations)
    perfect_metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    gmb_perfect = perfect_metrics.geometric_mean_bias()
    assert np.isclose(gmb_perfect, 1.0, rtol=1e-10)  # Should be exactly 1.0
    
    # Test over-prediction case
    over_metrics = ErrorMetrics([2.0, 4.0, 6.0], [1.0, 2.0, 3.0])
    gmb_over = over_metrics.geometric_mean_bias()
    assert gmb_over > 1.0  # Should indicate over-prediction
    
    # Test under-prediction case  
    under_metrics = ErrorMetrics([0.5, 1.0, 1.5], [1.0, 2.0, 3.0])
    gmb_under = under_metrics.geometric_mean_bias()
    assert gmb_under < 1.0  # Should indicate under-prediction

def test_median_absolute_error():
    # Test Median Absolute Error
    predictions = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    observations = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    metrics = ErrorMetrics(predictions, observations)
    medae = metrics.median_absolute_error()
    assert not np.isnan(medae)
    assert medae >= 0  # MedAE should be non-negative
    
    # Test perfect case (predictions = observations)
    perfect_metrics = ErrorMetrics([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    medae_perfect = perfect_metrics.median_absolute_error()
    assert medae_perfect == 0.0  # Should be exactly 0.0
    
    # Test with outliers - MedAE should be more robust than MAE
    outlier_predictions = np.array([1.0, 2.0, 3.0, 100.0])  # Large outlier
    outlier_observations = np.array([1.0, 2.0, 3.0, 4.0])
    outlier_metrics = ErrorMetrics(outlier_predictions, outlier_observations)
    medae_outlier = outlier_metrics.median_absolute_error()
    mae_outlier = outlier_metrics.mean_absolute_error()
    
    # MedAE should be less affected by the outlier than MAE
    assert medae_outlier < mae_outlier

def test_kendall_tau():
    # Test Kendall's Tau correlation
    predictions = np.array([1.2, 1.8, 3.2, 3.9, 5.1])
    observations = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    metrics = ErrorMetrics(predictions, observations)
    tau = metrics.kendall_tau()
    assert not np.isnan(tau)
    assert -1 <= tau <= 1  # Tau should be in [-1, 1]
    
    # Test perfect positive correlation
    perfect_metrics = ErrorMetrics([1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0])
    tau_perfect = perfect_metrics.kendall_tau()
    assert np.isclose(tau_perfect, 1.0, rtol=1e-10)  # Should be exactly 1.0
    
    # Test perfect negative correlation
    negative_metrics = ErrorMetrics([4.0, 3.0, 2.0, 1.0], [1.0, 2.0, 3.0, 4.0])
    tau_negative = negative_metrics.kendall_tau()
    assert np.isclose(tau_negative, -1.0, rtol=1e-10)  # Should be exactly -1.0
    
    # Test no correlation (random)
    no_corr_metrics = ErrorMetrics([1.0, 3.0, 2.0, 4.0], [1.0, 2.0, 3.0, 4.0])
    tau_no_corr = no_corr_metrics.kendall_tau()
    assert not np.isnan(tau_no_corr)
    assert -1 <= tau_no_corr <= 1

def test_gini_coefficient():
    # Test Gini coefficient
    predictions = np.array([0.9, 0.8, 0.7, 0.6, 0.5])
    observations = np.array([1.0, 1.0, 0.0, 0.0, 0.0])
    metrics = ErrorMetrics(predictions, observations)
    gini = metrics.gini_coefficient()
    assert not np.isnan(gini)
    assert 0 <= gini <= 1  # Gini should be in [0, 1]
    
    # Test perfect ranking case (should give high Gini)
    perfect_pred = np.array([1.0, 0.9, 0.8, 0.1, 0.0])
    perfect_obs = np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    perfect_metrics = ErrorMetrics(perfect_pred, perfect_obs)
    gini_perfect = perfect_metrics.gini_coefficient()
    # For five observations containing three positives, this implementation's
    # perfect-order Gini score is 0.2.
    assert np.isclose(gini_perfect, 0.2)
    
    # Test random ranking case (should give lower Gini)
    random_pred = np.array([0.5, 0.4, 0.6, 0.3, 0.7])
    random_obs = np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    random_metrics = ErrorMetrics(random_pred, random_obs)
    gini_random = random_metrics.gini_coefficient()
    assert gini_random < gini_perfect  # Random should be worse than perfect ranking
    
    # Test edge case: all zeros
    zero_metrics = ErrorMetrics([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    gini_zero = zero_metrics.gini_coefficient()
    assert np.isnan(gini_zero)  # Should return NaN for zero total

def test_prediction_of_change_in_direction():
    # Test PCD with perfect directional prediction
    predictions = np.array([1.0, 2.0, 3.0, 2.5, 4.0])  # up, up, down, up
    observations = np.array([1.1, 2.1, 3.1, 2.6, 4.1])  # up, up, down, up (same directions)
    metrics = ErrorMetrics(predictions, observations)
    pcd = metrics.prediction_of_change_in_direction()
    assert np.isclose(pcd, 1.0)  # Perfect directional prediction
    
    # Test PCD with completely wrong directional prediction
    wrong_predictions = np.array([1.0, 0.5, 0.0, 0.5, 0.0])  # down, down, up, down
    correct_observations = np.array([1.0, 2.0, 3.0, 4.0, 5.0])  # up, up, up, up (opposite directions)
    wrong_metrics = ErrorMetrics(wrong_predictions, correct_observations)
    pcd_wrong = wrong_metrics.prediction_of_change_in_direction()
    # The increments down, down, up, down contain one match against four upward
    # observation increments.
    assert np.isclose(pcd_wrong, 0.25)
    
    # Test PCD with mixed directional prediction
    mixed_pred = np.array([1.0, 2.0, 1.5, 3.0])  # up, down, up
    mixed_obs = np.array([1.0, 2.0, 3.0, 2.0])   # up, up, down (1 out of 3 correct)
    mixed_metrics = ErrorMetrics(mixed_pred, mixed_obs)
    pcd_mixed = mixed_metrics.prediction_of_change_in_direction()
    assert np.isclose(pcd_mixed, 1.0/3.0)  # 1 out of 3 correct
    
    # Test edge case: insufficient data
    short_metrics = ErrorMetrics([1.0], [1.0])
    pcd_short = short_metrics.prediction_of_change_in_direction()
    assert np.isnan(pcd_short)  # Should return NaN for < 2 points
    
    # Test range validation
    assert 0 <= pcd <= 1
    assert 0 <= pcd_mixed <= 1
