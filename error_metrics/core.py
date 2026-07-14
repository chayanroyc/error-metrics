#!/usr/bin/env python3

import numpy as np
try:
    import bottleneck as bn
except ImportError:
    bn = np
from typing import Dict, List, Tuple, Union, Callable, Optional
from dataclasses import dataclass
from functools import cached_property, wraps
import warnings
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.spatial.distance import pdist, squareform
from scipy.stats import skew as scipy_skew, kurtosis as scipy_kurtosis

def _safe_divide(numerator: float, denominator: float) -> float:
    """Return numerator divided by denominator, or NaN for a zero denominator."""
    if denominator == 0:
        return np.nan
    return numerator / denominator

@dataclass
class MetricInfo:
    """Information about a metric including its name, function, and description."""
    name: str
    function: Callable
    description: str
    abbreviation: str

class MetricRegistry:
    """Registry for error metrics to make the system extensible."""
    _metrics: Dict[str, MetricInfo] = {}

    @classmethod
    def register(cls, name: str, abbreviation: str, description: str = ""):
        """Decorator to register a new metric."""
        def decorator(func):
            if abbreviation in cls._metrics:
                existing = cls._metrics[abbreviation]
                if existing.function.__qualname__ != func.__qualname__:
                    raise ValueError(
                        f"Metric abbreviation '{abbreviation}' is already registered to "
                        f"'{existing.name}' ({existing.function.__qualname__}); cannot also "
                        f"register '{name}' ({func.__qualname__}) under the same abbreviation."
                    )
            cls._metrics[abbreviation] = MetricInfo(
                name=name,
                function=func,
                description=description,
                abbreviation=abbreviation
            )
            return func
        return decorator

    @classmethod
    def get_metric(cls, abbreviation: str) -> MetricInfo:
        """Get metric information by abbreviation."""
        if abbreviation not in cls._metrics:
            raise KeyError(f"Metric {abbreviation} not found in registry")
        return cls._metrics[abbreviation]

    @classmethod
    def get_all_metrics(cls) -> Dict[str, MetricInfo]:
        """Get all registered metrics."""
        return cls._metrics.copy()

class ErrorMetrics:
    """Class for calculating various error metrics between predictions and observations."""
    
    def __init__(self, predictions: Union[np.ndarray, List[float]], 
                 observations: Union[np.ndarray, List[float]]):
        """
        Initialize ErrorMetrics with predictions and observations.
        
        Args:
            predictions: Array-like of predicted values
            observations: Array-like of observed values
        """
        predictions = np.asarray(predictions, dtype=float)
        observations = np.asarray(observations, dtype=float)
        if predictions.shape != observations.shape:
            raise ValueError(
                "predictions and observations must have the same shape; got "
                f"{predictions.shape} and {observations.shape}."
            )
        self.predictions = predictions.ravel()
        self.observations = observations.ravel()
        self._preprocess_data()
        
        self.N = len(self.predictions)
        if self.N == 0:
            raise ValueError("No valid data points after preprocessing")
            
        self.diff = self.predictions - self.observations
        self.sum_ = self.predictions + self.observations
        self.pred_mean = bn.nanmean(self.predictions)
        self.obs_mean = bn.nanmean(self.observations)

    def _normalized_error(self) -> np.ndarray:
        """Compute normalized error nE = (pred - obs) / max(pred)."""
        max_pred = np.nanmax(self.predictions) if self.N > 0 else np.nan
        if np.isnan(max_pred) or np.isclose(max_pred, 0):
            return np.full_like(self.predictions, np.nan, dtype=float)
        return (self.predictions - self.observations) / max_pred

    def _preprocess_data(self):
        """Remove NaNs and infinities from predictions and observations."""
        mask = np.isfinite(self.predictions) & np.isfinite(self.observations)
        self._n_dropped = int((~mask).sum())
        self.predictions = self.predictions[mask]
        self.observations = self.observations[mask]

    @cached_property
    def _pearson_r(self) -> float:
        if self.N < 2:
            return np.nan
        return np.corrcoef(self.predictions, self.observations)[0, 1]

    @cached_property
    def _ecdf_obs(self) -> ECDF:
        return ECDF(self.observations)

    @cached_property
    def _ecdf_pred(self) -> ECDF:
        return ECDF(self.predictions)

    @cached_property
    def _linreg(self) -> Tuple[float, float]:
        x = self.predictions
        y = self.observations
        x_mean = bn.nanmean(x)
        y_mean = bn.nanmean(y)
        denominator = bn.nansum((x - x_mean) ** 2)
        if denominator == 0 or not np.isfinite(denominator):
            return np.nan, np.nan
        numerator = bn.nansum((x - x_mean) * (y - y_mean))
        b1 = _safe_divide(numerator, denominator)
        b0 = y_mean - b1 * x_mean
        ss_total = bn.nansum((y - y_mean) ** 2)
        if ss_total == 0 or not np.isfinite(ss_total):
            return b1, np.nan
        ss_residual = bn.nansum((y - (b0 + b1 * x)) ** 2)
        r2 = 1 - _safe_divide(ss_residual, ss_total)
        return b1, r2

    @MetricRegistry.register("Mean Bias", "MB", "Mean Bias")
    def mean_bias(self) -> float:
        """Calculate mean bias."""
        return self.pred_mean - self.obs_mean

    @MetricRegistry.register("Mean Absolute Error", "MAE", "Mean Absolute Error")
    def mean_absolute_error(self) -> float:
        """Calculate mean absolute error."""
        return bn.nanmean(np.abs(self.diff))

    @MetricRegistry.register("Median Absolute Error", "MedAE", "Median Absolute Error")
    def median_absolute_error(self) -> float:
        """
        Calculate Median Absolute Error (MedAE).
        
        Formula: MedAE = median(|predictions - observations|)
        
        MedAE is more robust to outliers than MAE as it uses the median
        instead of the mean of absolute errors.
        
        Range: [0, +∞)
        Perfect score: 0
        """
        return bn.nanmedian(np.abs(self.diff))

    @MetricRegistry.register("Root Mean Squared Error", "RMSE", "Root Mean Squared Error")
    def root_mean_squared_error(self) -> float:
        """Calculate root mean squared error."""
        return np.sqrt(bn.nanmean(self.diff ** 2))

    @MetricRegistry.register("Correlation Coefficient", "R", "Pearson correlation coefficient")
    def correlation_coefficient(self) -> float:
        """Calculate Pearson correlation coefficient."""
        return self._pearson_r

    @MetricRegistry.register("Spearman Rank Correlation", "SpearmanR", "Spearman rank correlation coefficient")
    def spearman_r(self) -> float:
        """Calculate Spearman rank correlation coefficient."""
        from scipy import stats
        return stats.spearmanr(self.predictions, self.observations)[0]

    @MetricRegistry.register("Kendall Tau Correlation", "KendallTau", "Kendall's tau rank correlation coefficient")
    def kendall_tau(self) -> float:
        """
        Calculate Kendall's Tau rank correlation coefficient.
        
        Kendall's tau measures the ordinal association between two variables
        based on the number of concordant and discordant pairs.
        
        Formula: τ = (concordant pairs - discordant pairs) / total pairs
        
        Range: [-1, 1]
        Perfect score: 1 (or -1 for perfect negative correlation)
        
        Advantages:
        - More robust to outliers than Pearson correlation
        - Has direct interpretation in terms of probability
        - Less sensitive to ties than Spearman correlation
        """
        from scipy.stats import kendalltau
        correlation, _ = kendalltau(self.observations, self.predictions, nan_policy='omit')
        return correlation

    @MetricRegistry.register("Lin's Concordance Correlation", "LCCC", "Measure of agreement")
    def lccc(self) -> float:
        """Calculate Lin's Concordance Correlation Coefficient."""
        r = self.correlation_coefficient()
        pred_std = bn.nanstd(self.predictions)
        obs_std = bn.nanstd(self.observations)
        pred_mean = bn.nanmean(self.predictions)
        obs_mean = bn.nanmean(self.observations)
        
        numerator = 2 * r * pred_std * obs_std
        denominator = pred_std**2 + obs_std**2 + (pred_mean - obs_mean)**2
        return _safe_divide(numerator, denominator)

    @MetricRegistry.register("Explained Variance", "EV", "Proportion of variance explained")
    def ev(self) -> float:
        """Calculate Explained Variance."""
        return 1 - _safe_divide(bn.nanvar(self.diff), bn.nanvar(self.observations))

    @MetricRegistry.register("Normalized Mean Square Error", "NMSE", "Normalized mean square error")
    def nmse(self) -> float:
        """Calculate Normalized Mean Square Error."""
        return _safe_divide(
            bn.nanmean(self.diff**2),
            bn.nanmean(self.predictions) * bn.nanmean(self.observations),
        )

    @MetricRegistry.register("Coefficient of Residual Mass", "CRM", "Coefficient of Residual Mass")
    def coefficient_of_residual_mass(self) -> float:
        """
        Calculate Coefficient of Residual Mass (CRM).
        
        CRM is a measure of model accuracy in predicting values, commonly used in
        environmental engineering and hydrology. Best possible value is 0,
        smaller value is better. Range = (-inf, +inf)
        
        Formula: CRM = (∑Ŷ - ∑Y)/∑Y
        where Ŷ are the predictions and Y are the observations
        
        Returns:
            float: CRM value
        """
        # Calculate sum of predictions
        sum_predictions = bn.nansum(self.predictions)
        
        # Calculate sum of observations
        sum_observations = bn.nansum(self.observations)
        
        # Calculate CRM using the formula (∑Ŷ - ∑Y)/∑Y
        return _safe_divide(sum_predictions - sum_observations, sum_observations)

    @MetricRegistry.register("Relative Error", "RE", "Relative Error")
    def relative_error(self) -> float:
        """
        Calculate Relative Error (RE).
        
        RE measures the ratio of the absolute error to the actual value.
        Best possible score is 0.0, smaller value is better. Range = [0, +inf)
        
        Formula: RE = |y_i - ŷ_i| / |y_i|
        
        Returns:
            float: Mean relative error
        """
        # Handle zero values in observations
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        
        # Calculate relative error
        re = np.abs(self.diff) / np.abs(safe_obs)
        
        # Return mean relative error
        return bn.nanmean(re)

    @MetricRegistry.register("Efficiency Coefficient", "EC", "Efficiency Coefficient")
    def efficiency_coefficient(self) -> float:
        """
        Calculate Efficiency Coefficient (EC).
        
        EC evaluates the accuracy of a regression model in predicting continuous values.
        Best possible value is 1, bigger value is better. Range = [-inf, 1]
        
        Formula: EC = 1 - ∑(y_i - ŷ_i)² / ∑(y_i - mean(Y))²
        
        Returns:
            float: EC value
        """
        # Calculate sum of squared errors
        ss_res = bn.nansum(self.diff ** 2)
        
        # Calculate sum of squared deviations from mean
        ss_tot = bn.nansum((self.observations - self.obs_mean) ** 2)
        
        # Calculate EC
        return 1 - _safe_divide(ss_res, ss_tot)

    @MetricRegistry.register("Mean Absolute Scaled Error", "MASE", "Mean Absolute Scaled Error")
    def mean_absolute_scaled_error(self, m: int = 1) -> float:
        """
        Calculate Mean Absolute Scaled Error (MASE).
        
        MASE is a scale-independent error metric that can be used to compare
        forecast methods on a single series and also to compare forecast accuracy
        between series. Best possible score is 0.0, smaller value is better.
        Range = [0, +inf)
        
        Formula: MASE = (1/N ∑|y_i - ŷ_i|) / (1/(N-1) ∑|y_i - y_{i-1}|)
        
        Args:
            m: Seasonality period (default=1 for non-seasonal data)
            
        Returns:
            float: MASE value
        """
        if self._n_dropped:
            warnings.warn(
                f"MASE assumes evenly-spaced, time-ordered data, but {self._n_dropped} "
                "invalid pair(s) were removed before calculating lags.",
                RuntimeWarning,
                stacklevel=2,
            )

        # Calculate mean absolute error
        mae = bn.nanmean(np.abs(self.diff))
        
        # Calculate mean absolute difference of observations
        mad = bn.nanmean(np.abs(np.diff(self.observations)))
        
        # Calculate MASE
        return _safe_divide(mae, mad)

    @MetricRegistry.register("Mean Arctangent Absolute Percentage Error", "MAAPE", "Mean Arctangent Absolute Percentage Error")
    def mean_arctangent_absolute_percentage_error(self) -> float:
        """
        Calculate Mean Arctangent Absolute Percentage Error (MAAPE).
        
        MAAPE is an alternative to MAPE that avoids the issue of dividing by zero
        when the actual value is zero. It uses the arctangent function to transform
        percentage errors into a bounded range. Best possible score is 0.0,
        smaller value is better. Range = [0, +inf)
        
        Formula: MAAPE = (100/n) ∑|(A_i - F_i)/A_i| * arctan(|(A_i - F_i)/A_i|)
        where A_i is the i-th actual value and F_i is the i-th forecasted value
        
        Returns:
            float: MAAPE value as a percentage
        """
        # Handle zero values in observations
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        
        # Calculate percentage errors
        pct_errors = np.abs(self.diff / safe_obs)
        
        # Calculate arctangent of percentage errors
        arctan_errors = np.arctan(pct_errors)
        
        # Calculate MAAPE
        return 100 * bn.nanmean(pct_errors * arctan_errors)

    @MetricRegistry.register("A10 Index", "A10", "A10 Index")
    def a10_index(self) -> float:
        """
        Calculate A10 Index.
        
        A10 index is an engineering metric for evaluating AI models by showing the
        proportion of predictions within ±10% of the actual values.
        Best possible score is 1.0, bigger value is better. Range = [0, 1]
        
        Formula: A10 = (1/n) ∑{1 if |ŷ_i - y_i|/y_i ≤ 0.1 else 0}
        
        Returns:
            float: A10 index value
        """
        # Handle zero values in observations
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        
        # Calculate relative errors
        rel_errors = np.abs(self.diff / safe_obs)
        
        # Count predictions within 10% of actual values
        within_threshold = rel_errors <= 0.1
        
        # Calculate A10 index
        return bn.nanmean(within_threshold)

    @MetricRegistry.register("Confidence Index", "CI", "Confidence Index")
    def confidence_index(self) -> float:
        """
        Calculate Confidence Index (CI).
        
        CI is a performance metric that combines Pearson correlation (R) and
        Willmott's Index (WI) to provide a comprehensive measure of model performance.
        Best possible score is 1.0, bigger value is better. Range = (-inf, 1]
        
        Interpretation:
        > 0.85          Excellent Model
        0.76-0.85       Very good
        0.66-0.75       Good
        0.61-0.65       Satisfactory
        0.51-0.60       Poor
        0.41-0.50       Bad
        < 0.40          Very bad
        
        Formula: CI = R * WI
        where R is Pearson correlation coefficient and WI is Willmott's Index
        
        Returns:
            float: Confidence Index value
        """
        # Calculate Pearson correlation (R)
        r = self.correlation_coefficient()
        
        # Calculate Willmott's Index (WI)
        wi = self.willmotts_index_of_agreement()
        
        # Calculate Confidence Index
        return r * wi

    @MetricRegistry.register("Max Error", "ME", "Max Error")
    def max_error(self) -> float:
        """
        Calculate Max Error (ME).
        
        ME computes the maximum residual error, capturing the worst case error between
        the predicted value and the true value. In a perfectly fitted model, max_error
        would be 0, though this is highly unlikely in real-world scenarios.
        Best possible score is 0.0, smaller value is better. Range = [0, +inf)
        
        Formula: ME = max(|y_i - ŷ_i|)
        
        Returns:
            float: Maximum error value
        """
        # Calculate absolute differences
        abs_diff = np.abs(self.diff)
        
        # Return maximum error
        return bn.nanmax(abs_diff)

    @MetricRegistry.register("Coefficient of Determination", "R2", "R-squared")
    def coefficient_of_determination(self) -> float:
        """Calculate coefficient of determination (R²)."""
        ss_tot = bn.nansum((self.observations - self.obs_mean) ** 2)
        ss_res = bn.nansum((self.observations - self.predictions) ** 2)
        return 1 - _safe_divide(ss_res, ss_tot)

    @MetricRegistry.register("Mean Normalized Bias", "MNB", "Mean Normalized Bias")
    def mean_normalized_bias(self) -> float:
        """Calculate mean normalized bias."""
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return bn.nanmean(self.diff / safe_obs)

    @MetricRegistry.register("Mean Normalized Absolute Error", "MNAE", "Mean Normalized Absolute Error")
    def mean_normalized_absolute_error(self) -> float:
        """Calculate mean normalized absolute error."""
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return bn.nanmean(np.abs(self.diff) / safe_obs)

    @MetricRegistry.register("Fractional Bias", "FB", "Measure of relative bias")
    def fb(self) -> float:
        """Calculate Fractional Bias."""
        return 2 * bn.nanmean(self.diff / self.sum_)

    @MetricRegistry.register("Fractional Absolute Error", "FAE", "Measure of relative absolute error")
    def fae(self) -> float:
        """Calculate Fractional Absolute Error."""
        return 2 * bn.nanmean(np.abs(self.diff) / self.sum_)

    @MetricRegistry.register("Mean Fractional Bias", "MFB", "Pointwise mean fractional bias")
    def mean_fractional_bias(self) -> float:
        """Return pointwise mean fractional bias for nonnegative data."""
        if np.any(self.predictions < 0) or np.any(self.observations < 0):
            raise ValueError("MFB requires nonnegative predictions and observations.")
        denominator = self.predictions + self.observations
        ratio = np.divide(2.0 * self.diff, denominator, out=np.zeros_like(self.diff), where=denominator != 0)
        return float(bn.nanmean(ratio))

    @MetricRegistry.register("Mean Fractional Error", "MFE", "Pointwise mean fractional absolute error")
    def mean_fractional_error(self) -> float:
        """Return pointwise mean fractional absolute error for nonnegative data."""
        if np.any(self.predictions < 0) or np.any(self.observations < 0):
            raise ValueError("MFE requires nonnegative predictions and observations.")
        denominator = self.predictions + self.observations
        ratio = np.divide(2.0 * np.abs(self.diff), denominator, out=np.zeros_like(self.diff), where=denominator != 0)
        return float(bn.nanmean(ratio))

    @MetricRegistry.register("Mean Absolute Gross Error", "MAGE", "Mean Absolute Gross Error")
    def mean_absolute_gross_error(self) -> float:
        """
        Calculate Mean Absolute Gross Error (MAGE).
        
        Formula: MAGE = mean(|predictions - observations| / observations)
        
        This is the normalized version of MAE, expressing error as a fraction of observations.
        """
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return bn.nanmean(np.abs(self.diff) / safe_obs)

    @MetricRegistry.register("Geometric Mean Bias", "GMB", "Geometric Mean Bias")
    def geometric_mean_bias(self) -> float:
        """
        Calculate Geometric Mean Bias (GMB).
        
        Formula: GMB = exp(mean(ln(predictions / observations)))
        
        GMB measures multiplicative bias:
        - GMB = 1: No bias (perfect)
        - GMB > 1: Over-prediction bias
        - GMB < 1: Under-prediction bias
        
        Range: (0, +∞)
        Perfect score: 1
        
        Note: Requires positive values for both predictions and observations.
        """
        # Check for non-positive values
        if np.any(self.predictions <= 0) or np.any(self.observations <= 0):
            warnings.warn("GMB requires positive values. Non-positive values will be treated as NaN.")
        
        # Calculate ratio, handling non-positive values
        ratio = self.predictions / self.observations
        ratio = np.where((self.predictions <= 0) | (self.observations <= 0), np.nan, ratio)
        
        # Calculate geometric mean bias
        log_ratio = np.log(ratio)
        return np.exp(bn.nanmean(log_ratio))

    @MetricRegistry.register("Factor of Observations 2", "FAC2", "Factor of Observations 2")
    def factor_of_observations2(self) -> float:
        """Calculate factor of observations 2 (FAC2)."""
        ratio = self.predictions / self.observations
        valid = (ratio >= 0.5) & (ratio <= 2.0)
        return 100 * bn.nansum(valid) / self.N

    @MetricRegistry.register("Mean Bias Difference", "MBD", "Mean Bias Difference")
    def mean_bias_difference(self) -> float:
        """Calculate mean bias difference."""
        return 100 * _safe_divide(bn.nanmean(self.diff), self.obs_mean)

    @MetricRegistry.register("Root Mean Square Difference", "RMSD", "Root Mean Square Difference")
    def root_mean_square_difference(self) -> float:
        """Calculate root mean square difference."""
        return 100 * _safe_divide(np.sqrt(bn.nanmean(self.diff ** 2)), self.obs_mean)

    @MetricRegistry.register("Mean Absolute Difference", "MAD", "Mean Absolute Difference")
    def mean_absolute_difference(self) -> float:
        """Calculate mean absolute difference."""
        return 100 * _safe_divide(bn.nanmean(np.abs(self.diff)), self.obs_mean)

    @MetricRegistry.register("Standard Deviation of Residual", "SD", "Standard Deviation of Residual")
    def standard_deviation_of_residual(self) -> float:
        """Calculate standard deviation of the residual."""
        residual = self.diff
        return 100 * _safe_divide(
            np.sqrt(bn.nanmean(residual ** 2) - (bn.nanmean(residual) ** 2)),
            self.obs_mean,
        )

    @MetricRegistry.register("Slope of Best-Fit Line", "SBF", "Slope of Best-Fit Line")
    def slope_of_best_fit_line(self) -> float:
        """Calculate slope of best-fit line."""
        numerator = bn.nansum((self.predictions - self.pred_mean) * (self.observations - self.obs_mean))
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return _safe_divide(numerator, denominator)

    @MetricRegistry.register("Uncertainty at 95%", "U95", "Uncertainty at 95%")
    def uncertainty_95(self) -> float:
        """Calculate uncertainty at 95%."""
        sd = self.standard_deviation_of_residual()
        rmsd = self.root_mean_square_difference()
        return 1.96 * np.sqrt(sd ** 2 + rmsd ** 2)

    @MetricRegistry.register("t-Statistic", "TS", "t-Statistic")
    def t_statistic(self) -> float:
        """Calculate t-statistic."""
        mbd = self.mean_bias_difference()
        rmsd = self.root_mean_square_difference()
        return np.sqrt(_safe_divide((self.N - 1) * (mbd ** 2), rmsd ** 2 - mbd ** 2))

    @MetricRegistry.register("Nash-Sutcliffe Efficiency", "NSE", "Nash-Sutcliffe Efficiency")
    def nash_sutcliffe_efficiency(self) -> float:
        """Calculate Nash-Sutcliffe efficiency."""
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return 1 - _safe_divide(numerator, denominator)

    @MetricRegistry.register("Normalized NSE", "NNSE", "Normalized Nash-Sutcliffe Efficiency")
    def normalized_nse(self) -> float:
        """
        Calculate Normalized Nash-Sutcliffe Efficiency (NNSE).
        
        NNSE is a variant of NSE that provides a more objective measure of model performance.
        The normalization ensures the metric is bounded between 0 and 1, with 1 being the best score.
        
        Returns:
            float: NNSE value in range [0, 1]
        """
        nse = self.nash_sutcliffe_efficiency()
        return _safe_divide(1, 2 - nse)

    @MetricRegistry.register("Relative Absolute Error", "RAE", "Relative Absolute Error")
    def relative_absolute_error(self) -> float:
        """
        Calculate Relative Absolute Error (RAE).
        
        RAE measures the ratio of the root mean squared error to the root sum of squared observations.
        Best possible score is 0.0, smaller value is better. Range = [0, +inf)
        
        Returns:
            float: RAE value
        """
        numerator = np.sqrt(bn.nansum(self.diff ** 2))
        denominator = np.sqrt(bn.nansum(self.observations ** 2))
        return _safe_divide(numerator, denominator)

    @MetricRegistry.register("Variance Accounted For", "VAF", "Variance Accounted For")
    def variance_accounted_for(self) -> float:
        """
        Calculate Variance Accounted For (VAF).
        
        VAF measures the proportion of the total variance in the actual values that is accounted for
        by the variance in the predicted values. Best possible score is 100% (identical signals),
        bigger value is better. Range = (-inf, 100%]
        
        Returns:
            float: VAF value as a percentage
        """
        # Calculate means
        obs_mean = bn.nanmean(self.observations)
        pred_mean = bn.nanmean(self.predictions)
        
        # Calculate numerator: sum of cross-products of centered values
        numerator = bn.nansum((self.observations - obs_mean) * (self.predictions - pred_mean))
        
        # Calculate denominator: sum of squared centered observations
        denominator = bn.nansum((self.observations - obs_mean) ** 2)
        
        # Calculate VAF as percentage
        return 100 * _safe_divide(numerator, denominator)

    @MetricRegistry.register("Residual Standard Error", "RSE", "Residual Standard Error")
    def residual_standard_error(self, p: int = 1) -> float:
        """
        Calculate Residual Standard Error (RSE).
        
        RSE measures the average distance between observed values and predicted values,
        taking into account the degrees of freedom. Best possible score is 0.0,
        smaller value is better. Range = [0, +inf)
        
        Args:
            p: Number of predictors in the model (default=1 for simple regression)
            
        Returns:
            float: RSE value
        """
        # Calculate sum of squared residuals
        ss_res = bn.nansum(self.diff ** 2)
        
        # Calculate degrees of freedom (n - p - 1)
        df = self.N - p - 1
        
        # Calculate RSE
        return np.sqrt(ss_res / df)

    @MetricRegistry.register("Kling-Gupta Efficiency", "KGE", "Kling-Gupta Efficiency (2009 version)")
    def kling_gupta_efficiency(self) -> Tuple[float, float, float, float]:
        """
        Calculate Kling-Gupta efficiency (2009 version) and its components.
        
        This is the original formulation from Kling et al. (2009) where alpha is the
        ratio of standard deviations.
        
        Returns:
            Tuple[float, float, float, float]: (KGE value, r component, alpha component, beta component)
        """
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        alpha = _safe_divide(std_pred, std_obs)
        beta = _safe_divide(self.pred_mean, self.obs_mean)
        kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        return kge, r, alpha, beta

    @MetricRegistry.register("Modified Kling-Gupta Efficiency", "KGE2012", "Kling-Gupta Efficiency (2012 version)")
    def modified_kling_gupta_efficiency(self) -> Tuple[float, float, float, float]:
        """
        Calculate Modified Kling-Gupta efficiency (2012 version) and its components.
        https://doi.org/10.1016/j.jhydrol.2012.01.011
        
        This is the modified formulation from Gupta et al. (2012) where alpha is the
        ratio of coefficients of variation (CV) instead of standard deviations.
        
        Formula:
            r = Pearson correlation coefficient
            alpha = CV(predictions) / CV(observations) = (std_pred / mean_pred) / (std_obs / mean_obs)
            beta = mean(predictions) / mean(observations)
            KGE = 1 - sqrt((r - 1)² + (alpha - 1)² + (beta - 1)²)
        
        Returns:
            Tuple[float, float, float, float]: (KGE value, r component, alpha component, beta component)
        """
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        # Alpha is ratio of coefficients of variation (CV)
        cv_pred = std_pred / self.pred_mean
        cv_obs = std_obs / self.obs_mean
        alpha = cv_pred / cv_obs
        beta = self.pred_mean / self.obs_mean
        kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        return kge, r, alpha, beta

    @MetricRegistry.register("Kling-Gupta Efficiency Double Prime", "KGEdp", "Kling-Gupta Efficiency (Tang et al. 2021)")
    def kling_gupta_efficiency_double_prime(self) -> Tuple[float, float, float, float]:
        """
        Calculate Kling-Gupta Efficiency double prime (KGE'') by Tang et al. (2021).
        https://journals.ametsoc.org/view/journals/clim/34/16/JCLI-D-21-0067.1.xml
        
        This variant uses a normalized bias ratio instead of the mean ratio, which makes
        it more robust when mean values are close to zero.
        
        Formula:
            r = Pearson correlation coefficient
            alpha = std(predictions) / std(observations)
            beta_n = (mean(predictions) - mean(observations)) / std(observations)
            KGE'' = 1 - sqrt((r - 1)² + (alpha - 1)² + beta_n²)
        
        Note: beta_n is squared directly (not (beta_n - 1)²) because it's a normalized
        difference rather than a ratio.
        
        Returns:
            Tuple[float, float, float, float]: (KGE'' value, r component, alpha component, beta_n component)
        """
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        alpha = std_pred / std_obs
        # Normalized bias: (mean_pred - mean_obs) / std_obs
        beta_n = (self.pred_mean - self.obs_mean) / std_obs
        # Note: beta_n is squared directly, not (beta_n - 1)²
        kge_dp = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + beta_n ** 2)
        return kge_dp, r, alpha, beta_n

    @MetricRegistry.register("Diagnostic Efficiency", "DE", "Diagnostic Efficiency (Schwemmle et al. 2021)")
    def diagnostic_efficiency(self) -> Tuple[float, float, float, float]:
        """
        Calculate Diagnostic Efficiency (DE) by Schwemmle et al. (2021).
        https://doi.org/10.5194/hess-25-2187-2021
        
        DE decomposes model errors into three distinct components to provide diagnostic
        insights into model performance:
        
        1. Constant Error (B_rel_mean): Systematic bias calculated on Flow Duration Curve
        2. Dynamic Error (B_area): Variability discrepancies after removing constant error
        3. Timing Error (r): Temporal misalignments via correlation on original time series
        
        Formula:
            DE = sqrt(B_rel_mean² + B_area² + (r - 1)²)
        
        Note: Lower values are better, with 0 being perfect.
        
        Returns:
            Tuple[float, float, float, float]: (DE, r, B_area, B_rel_mean)
        """
        obs = self.observations
        sim = self.predictions
        
        # --- 1. Timing Error (r) ---
        # Check for constant arrays (zero variance)
        if np.std(obs) == 0 or np.std(sim) == 0:
            r = np.nan
        else:
            r = np.corrcoef(obs, sim)[0, 1]
        
        # --- Pre-processing: Remove zeros before FDC construction ---
        valid = obs > 0
        if np.sum(valid) < 2:
            return np.nan, r, np.nan, np.nan
        
        obs_valid = obs[valid]
        sim_valid = sim[valid]
        
        # Sort independently in descending order for FDC
        obs_fdc = np.sort(obs_valid)[::-1]
        sim_fdc = np.sort(sim_valid)[::-1]
        
        # --- 2. Constant Error (B_rel_mean) ---
        # B_rel(i) = (Qsim(i) - Qobs(i)) / Qobs(i)
        b_rel = (sim_fdc - obs_fdc) / obs_fdc
        b_rel_mean = np.mean(b_rel)
        
        # --- 3. Dynamic Error (B_area) ---
        # Residual bias after removing constant error
        b_res = b_rel - b_rel_mean
        
        # Integrate using trapezoidal rule over normalized domain [0, 1]
        n = len(b_res)
        exceedance_prob = np.linspace(0, 1, n)
        b_area = np.trapz(np.abs(b_res), exceedance_prob)
        
        # --- Final Calculation ---
        de = 1 - np.sqrt(b_rel_mean**2 + b_area**2 + (r - 1)**2)
        
        return de, r, b_area, b_rel_mean

    @MetricRegistry.register("Liu Model Efficiency", "LME", "Liu Model Efficiency (Liu 2020)")
    def liu_model_efficiency(self) -> Tuple[float, float, float, float, float]:
        """
        Calculate Liu Model Efficiency (LME) by Liu (2020).
        https://www.sciencedirect.com/science/article/pii/S0022169420309483
        
        LME is a performance criterion that combines correlation and variability into
        a single slope term, providing a more integrated assessment of model performance.
        
        Formula:
            r = Pearson correlation coefficient
            alpha = std(predictions) / std(observations)  (variability ratio)
            beta = mean(predictions) / mean(observations)  (bias ratio)
            slope_term = r * alpha  (regression slope)
            LME = 1 - sqrt((r*alpha - 1)² + (beta - 1)²)
        
        The key difference from KGE is that LME uses the combined term (r*alpha)
        instead of separate r and alpha terms. This slope_term represents the slope
        of the regression line and combines both correlation and variability.
        
        Range: (-∞, 1]
        Perfect score: 1
        
        Returns:
            Tuple[float, float, float, float, float]: (LME value, r component, alpha component, beta component, slope_term component)
        """
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        
        # Beta (Bias ratio)
        if self.obs_mean == 0:
            # If both are 0, beta is 1 (perfect). If only obs is 0, beta is inf.
            beta = 1.0 if self.pred_mean == 0 else np.inf
        else:
            beta = self.pred_mean / self.obs_mean
        
        # Alpha (Variability ratio)
        if std_obs == 0:
            alpha = 1.0 if std_pred == 0 else np.inf
        else:
            alpha = std_pred / std_obs
        
        # Slope Term (r * alpha)
        # This represents the slope of the regression line (sim = k * obs + c)
        slope_term = r * alpha
        
        # LME Calculation
        # LME = 1 - sqrt((r*alpha - 1)² + (beta - 1)²)
        # We use Euclidean distance of the components from the ideal point (1, 1)
        euclidean_dist = np.sqrt((slope_term - 1) ** 2 + (beta - 1) ** 2)
        lme = 1 - euclidean_dist
        
        return lme, r, alpha, beta, slope_term

    @MetricRegistry.register("Least-squares Combined Efficiency", "LCEf", "Least-squares Combined Efficiency (Lee & Choi 2022)")
    def least_squares_combined_efficiency(self) -> Tuple[float, float, float, float, float, float]:
        """
        Calculate Least-squares Combined Efficiency (LCEf) by Lee & Choi (2022).
        
        LCEf is a rebalanced performance criterion that considers both forward and
        inverse regression slopes, providing a more symmetric evaluation of model performance.
        
        Formula:
            r = Pearson correlation coefficient
            alpha = std(predictions) / std(observations)  (variability ratio)
            beta = mean(predictions) / mean(observations)  (bias ratio)
            slope_1 = r * alpha  (Sim vs Obs slope)
            slope_2 = r / alpha  (Obs vs Sim slope term)
            LCEf = 1 - sqrt((r*alpha - 1)² + (r/alpha - 1)² + (beta - 1)²)
        
        The key difference from LME is that LCEf includes both forward (r*alpha) and
        inverse (r/alpha) slope terms, making it symmetric and more balanced.
        
        Range: (-∞, 1]
        Perfect score: 1
        
        Returns:
            Tuple[float, float, float, float, float, float]: (LCEf value, r component, alpha component, beta component, slope_1 component, slope_2 component)
        """
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        
        # Beta (Bias ratio)
        if self.obs_mean == 0:
            beta = 1.0 if self.pred_mean == 0 else np.inf
        else:
            beta = self.pred_mean / self.obs_mean
        
        # Alpha (Variability ratio)
        if std_obs == 0:
            alpha = 1.0 if std_pred == 0 else np.inf
        else:
            alpha = std_pred / std_obs
        
        # Slope Terms
        slope_1 = r * alpha  # Sim vs Obs slope
        
        # Handle division by zero for slope_2
        if alpha == 0:
            # If alpha is 0 (flat simulation), slope_2 is undefined/infinite
            slope_2 = np.inf
        else:
            slope_2 = r / alpha  # Obs vs Sim slope term
        
        # LCEf Calculation
        # LCEf  = 1 - Euclidean distance of components from (1, 1, 1)
        # If any component is inf, LCEf is -inf
        if np.isinf(slope_2) or np.isinf(beta) or np.isinf(alpha):
            lcef = -np.inf
        else:
            euclidean_dist = np.sqrt(
                (slope_1 - 1) ** 2 +
                (slope_2 - 1) ** 2 +
                (beta - 1) ** 2
            )
            lcef = 1 - euclidean_dist
        
        return lcef, r, alpha, beta, slope_1, slope_2

    @MetricRegistry.register("Willmott's Index of Agreement", "WIA", "Willmott's Index of Agreement")
    def willmotts_index_of_agreement(self) -> float:
        """Calculate Willmott's index of agreement."""
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((np.abs(self.predictions - self.obs_mean) + 
                               np.abs(self.observations - self.obs_mean)) ** 2)
        return 1 - (numerator / denominator)

    @MetricRegistry.register("Refined Index of Agreement", "WIAr", "Refined Index of Agreement (Willmott et al. 2012)")
    def refined_index_of_agreement(self) -> float:
        """
        Calculate Refined Index of Agreement (dr) by Willmott et al. (2012).
        
        Reference: Willmott, C.J., Robeson, S.M. and Matsuura, K. (2012). 
        A refined index of model performance. International Journal of climatology, 
        32(13), pp.2088-2094. doi:10.1002/joc.2419
        
        In contrast to the original Index of Agreement (d), which ranges from 0 to 1.0,
        the Refined Index of Agreement (dr) is bounded by -1.0 and 1.0. The closer to 1
        the better the performance of the model.
        
        Formula:
            A = sum(|predictions - observations|)
            B = c * sum(|observations - mean_obs|)  where c = 2
            if A <= B: dr = 1 - A / B
            else: dr = 1 - B / A
        
        Range: [-1.0, 1.0]
        Perfect score: 1.0
        
        Returns:
            float: Refined Index of Agreement (dr)
        """
        # Mean of observed values
        Om = self.obs_mean
        
        # Constant 'c' value
        c = 2
        
        # Components of the formula
        A = bn.nansum(np.abs(self.predictions - self.observations))
        B = c * bn.nansum(np.abs(self.observations - Om))
        
        if A <= B:
            dr = 1 - A / B
        else:
            dr = 1 - B / A
        
        return dr

    @MetricRegistry.register("Legates Coefficient of Efficiency", "LCE", "Legates Coefficient of Efficiency")
    def legates_coefficient_of_efficiency(self) -> float:
        """Calculate Legates coefficient of efficiency."""
        numerator = bn.nansum(np.abs(self.predictions - self.observations))
        denominator = bn.nansum(np.abs(self.observations - self.obs_mean))
        return 1 - _safe_divide(numerator, denominator)

    @MetricRegistry.register("Kolmogorov-Smirnov Test Integral", "KSI", "Measure of distribution similarity")
    def ksi(self, normed: bool = True) -> float:
        """
        Calculate Kolmogorov-Smirnov Test Integral (KSI).
        
        Args:
            normed: If True, return the normalized KSI [%]
            
        Returns:
            KSI value
        """
        ecdf_obs = self._ecdf_obs
        ecdf_fx = self._ecdf_pred

        x = np.unique(np.concatenate((self.observations, self.predictions)))
        y_o = ecdf_obs(x)
        y_f = ecdf_fx(x)

        D = np.abs(y_o - y_f)
        ksi = np.sum(D[:-1] * np.diff(x))

        if normed:
            Vc = _safe_divide(1.63, np.sqrt(len(self.observations)))
            a_critical = Vc * (x.max() - x.min())
            return 100 * _safe_divide(ksi, a_critical)
        return ksi

    @MetricRegistry.register("Percentage of Histogram Intersection", "PHI", "Histogram-overlap distribution similarity")
    def phi(self, n_bins: int = 10) -> float:
        """Return normalized histogram intersection as a fraction in [0, 1]."""
        if isinstance(n_bins, bool) or not isinstance(n_bins, int) or n_bins < 1:
            raise ValueError("n_bins must be an integer >= 1")
        edges = np.histogram_bin_edges(np.concatenate((self.predictions, self.observations)), bins=n_bins)
        pred_counts, _ = np.histogram(self.predictions, bins=edges)
        obs_counts, _ = np.histogram(self.observations, bins=edges)
        pred_probability = pred_counts / pred_counts.sum()
        obs_probability = obs_counts / obs_counts.sum()
        return float(np.sum(np.minimum(pred_probability, obs_probability)))

    @MetricRegistry.register("Over-estimation Metric", "OVER", "Measure of over-estimation")
    def over_metric(self, normed: bool = True) -> float:
        """
        Calculate Over-estimation (oVER) Metric.
        
        Args:
            normed: If True, return the normalized OVER [%]
            
        Returns:
            Over-estimation value
        """
        ecdf_obs = self._ecdf_obs
        ecdf_fx = self._ecdf_pred

        x = np.unique(np.concatenate((self.observations, self.predictions)))
        y_o = ecdf_obs(x)
        y_f = ecdf_fx(x)

        D = np.maximum(y_f - y_o, 0)
        over = np.sum(D[:-1] * np.diff(x))

        if normed:
            Vc = _safe_divide(1.63, np.sqrt(len(self.observations)))
            a_critical = Vc * (x.max() - x.min())
            return 100 * _safe_divide(over, a_critical)
        return over

    @MetricRegistry.register("Interquartile Range", "IQR", "Measure of statistical dispersion")
    def IQR(self) -> float:
        """Calculate Interquartile Range."""
        return np.percentile(self.observations, 75) - np.percentile(self.observations, 25)

    @MetricRegistry.register("Standard Deviation", "STD", "Measure of data spread")
    def STD(self) -> float:
        """Calculate Standard Deviation."""
        return bn.nanstd(self.observations)

    @MetricRegistry.register("Normalized Error Skewness", "nESkew", "Skewness of normalized error (Correndo et al. 2021)")
    def normalized_error_skewness(self) -> float:
        """Calculate skewness of the normalized error."""
        ne = self._normalized_error()
        if ne is None:
            return np.nan
        ne = ne[np.isfinite(ne)]
        if len(ne) < 3:
            return np.nan
        return scipy_skew(ne, bias=False)

    @MetricRegistry.register("Normalized Error Kurtosis", "nEKurt", "Kurtosis of normalized error (Correndo et al. 2021)")
    def normalized_error_kurtosis(self) -> float:
        """Calculate kurtosis of the normalized error."""
        ne = self._normalized_error()
        if ne is None:
            return np.nan
        ne = ne[np.isfinite(ne)]
        if len(ne) < 4:
            return np.nan
        return scipy_kurtosis(ne, fisher=True, bias=False)

    def msd(self) -> float:
        """Calculate Mean Square Deviation. Available through msd_decomposition()."""
        return bn.nanmean(self.diff ** 2)

    def sb(self) -> float:
        """Calculate Systematic Bias. Available through msd_decomposition()."""
        return bn.nanmean(self.diff) ** 2

    @MetricRegistry.register("Mean Bias Factor", "MBF", "Ratio of mean prediction to mean observation")
    def mean_bias_factor(self) -> float:
        """Return mean prediction divided by mean observation."""
        if self.pred_mean <= 0 or self.obs_mean <= 0:
            raise ValueError("MBF requires strictly positive prediction and observation means.")
        return float(self.pred_mean / self.obs_mean)

    @MetricRegistry.register("Relative Mean Bias Factor", "RMBF", "Absolute deviation of MBF from one")
    def relative_mean_bias_factor(self) -> float:
        """Return the absolute deviation of MBF from one."""
        return float(np.abs(self.mean_bias_factor() - 1.0))

    @MetricRegistry.register("Normalized Mean Bias Factor", "NMBF", "Measure of bias factor")
    def nmbf(self) -> float:
        """Calculate Normalized Mean Bias Factor."""
        return _safe_divide(bn.nanmean(self.predictions), bn.nanmean(self.observations))

    @MetricRegistry.register("Relative Normalized Mean Bias Factor", "RNMBF", "Measure of relative bias factor")
    def rnmbf(self) -> float:
        """Calculate Relative Normalized Mean Bias Factor."""
        return np.abs(self.nmbf() - 1)

    @MetricRegistry.register("Combined Performance Index", "CPI", "Overall performance measure")
    def cpi(self) -> float:
        """
        Calculate Combined Performance Index.
        
        Formula: CPI = (KSI + OVER + 2*RMSE) / 4
        
        Where:
            KSI: Kolmogorov-Smirnov Test Integral
            OVER: Over-estimation Metric
            RMSE: Root Mean Squared Error
        """
        ksi_val = self.ksi(normed=False)
        over_val = self.over_metric(normed=False)
        rmse_val = self.root_mean_squared_error()
        return (ksi_val + over_val + 2 * rmse_val) / 4

    @MetricRegistry.register("Relative Euclidean Distance", "RED", "Measure of relative distance")
    def red(self) -> float:
        """Calculate Relative Euclidean Distance."""
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return np.sqrt(bn.nanmean((self.diff / safe_obs) ** 2))

    @MetricRegistry.register("Figure of Merit", "FoM", "Measure of model performance")
    def figure_of_merit(self) -> float:
        """Calculate Figure of Merit."""
        Aov = np.minimum(self.observations, self.predictions)
        Afn = np.maximum(self.observations - Aov, 0)
        Afp = np.maximum(self.predictions - Aov, 0)

        Aov_sum = bn.nansum(Aov)
        Afn_sum = bn.nansum(Afn)
        Afp_sum = bn.nansum(Afp)

        return 100 * _safe_divide(Aov_sum, Aov_sum + Afn_sum + Afp_sum)

    def nu(self) -> float:
        """Calculate Non-uniformity. Available through msd_decomposition()."""
        b1, _ = self.linear_regression()
        return (1 - b1) ** 2 * bn.nanmean((self.predictions - bn.nanmean(self.predictions)) ** 2)

    def lc(self) -> float:
        """Calculate Lack of Correlation. Available through msd_decomposition()."""
        _, r2 = self.linear_regression()
        return (1 - r2) * bn.nanmean((self.observations - bn.nanmean(self.observations)) ** 2)

    @MetricRegistry.register("MSD Decomposition", "MSDdec", "Mean Square Deviation decomposition (Gauche)")
    def msd_decomposition(self) -> Tuple[float, float, float, float]:
        """
        Calculate the Mean Square Deviation (MSD) decomposition from Gauche.
        Gauch, H. G., Hwang, J. T. G., & Fick, G. W. (2003). Model evaluation by comparison of model-based predictions and measured values. Agronomy Journal, 95(6), 1442–1446. 
        https://doi.org/10.2134/agronj2003.1442↩︎

        MSD can be decomposed into three additive components:
            MSD = SB + NU + LC
        where:
            SB: Systematic Bias component
            NU: Non-uniformity component
            LC: Lack of Correlation component

        Returns:
            Tuple[float, float, float, float]: (MSD, SB, NU, LC)
        """
        total_msd = self.msd()
        sb_component = self.sb()
        nu_component = self.nu()
        lc_component = self.lc()
        return total_msd, sb_component, nu_component, lc_component

    @MetricRegistry.register("Skill Score vs Climatology", "SS", "Skill score against climatology")
    def skill_score_against_climatology(self) -> float:
        """Calculate skill score against climatology."""
        climatology = np.full_like(self.observations, bn.nanmean(self.observations))
        ss_res = bn.nansum((self.predictions - self.observations) ** 2)
        ss_clim = bn.nansum((climatology - self.observations) ** 2)
        return 1 - _safe_divide(ss_res, ss_clim)

    @MetricRegistry.register("Anderson-Darling Distance", "AD", "Anderson-Darling distance")
    def anderson_darling_distance(self) -> float:
        """Calculate Anderson-Darling distance."""
        ecdf_obs = self._ecdf_obs
        ecdf_pred = self._ecdf_pred
        x = np.sort(np.unique(np.concatenate((self.observations, self.predictions))))
        
        F = ecdf_obs(x)
        G = ecdf_pred(x)
        w = 1.0 / (F * (1 - F) + 1e-10)  # avoid divide-by-zero
        return np.sum((F - G) ** 2 * w)

    @MetricRegistry.register("Kullback-Leibler Divergence", "KLD", "Kullback-Leibler divergence")
    def kullback_leibler_divergence(self) -> float:
        """Calculate Kullback-Leibler divergence."""
        from scipy.special import rel_entr
    
        pred = self.predictions.copy()
        obs = self.observations.copy()
    
        # Convert to probability distributions
        pred = np.abs(pred)
        obs = np.abs(obs)
        
        pred = pred / bn.nansum(pred)
        obs = obs / bn.nansum(obs)
    
        return bn.nansum(rel_entr(np.abs(obs), pred))

    @MetricRegistry.register("Mean Percentage Error", "MPE", "Mean percentage error")
    def mean_percentage_error(self) -> float:
        """Calculate mean percentage error."""
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return 100 * bn.nanmean((self.predictions - self.observations) / safe_obs)

    @MetricRegistry.register("Mean Absolute Percentage Error", "MAPE", "Mean absolute percentage error")
    def mean_absolute_percentage_error(self) -> float:
        """Calculate mean absolute percentage error."""
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return 100 * bn.nanmean(np.abs((self.predictions - self.observations) / safe_obs))

    @MetricRegistry.register("Symmetric Mean Absolute Percentage Error", "sMAPE", "Symmetric mean absolute percentage error")
    def symmetric_mean_absolute_percentage_error(self) -> float:
        """Calculate symmetric mean absolute percentage error."""
        denom = (np.abs(self.observations) + np.abs(self.predictions)) / 2
        safe_denom = np.where(denom == 0, np.nan, denom)
        return 100 * bn.nanmean(np.abs(self.predictions - self.observations) / safe_denom)

    @MetricRegistry.register("Continuous Ranked Probability Score", "CRPS", "Continuous ranked probability score")
    def continuous_ranked_probability_score(self) -> float:
        """
        Calculate Continuous Ranked Probability Score (CRPS).
        
        CRPS is a proper scoring rule for evaluating probabilistic forecasts. It measures the
        difference between the predicted and observed cumulative distribution functions.
        Best possible score is 0.0, smaller value is better. Range = [0, +inf)
        
        For deterministic forecasts, CRPS reduces to the mean absolute error.
        
        Returns:
            float: CRPS value
        """
        # For deterministic forecasts, CRPS reduces to MAE
        return self.mean_absolute_error()

    @MetricRegistry.register("Trend Accuracy", "TAcc", "Trend accuracy")
    def trend_accuracy(self) -> float:
        """Calculate trend accuracy."""
        if self._n_dropped:
            warnings.warn(
                f"trend_accuracy fits a trend against sample index, but {self._n_dropped} "
                "invalid pair(s) were removed and the index was compressed.",
                RuntimeWarning,
                stacklevel=2,
            )
        obs_trend = np.polyfit(np.arange(len(self.observations)), self.observations, 1)[0]
        pred_trend = np.polyfit(np.arange(len(self.predictions)), self.predictions, 1)[0]
        return 1 - abs(obs_trend - pred_trend) / (abs(obs_trend) + 1e-10)

    @MetricRegistry.register("Theil's Inequality Coefficient", "U2", "Theil's U2 coefficient")
    def theils_u2(self) -> float:
        """
        Calculate Theil's Inequality Coefficient (U2).

        U2 = RMSE / sqrt(mean(observation^2))
        """
        rmse = self.root_mean_squared_error()
        obs_rms = np.sqrt(bn.nanmean(self.observations ** 2))
        if obs_rms == 0 or np.isnan(obs_rms):
            return np.nan
        return rmse / obs_rms

    @MetricRegistry.register("Berry-Mielke Index", "BM", "Berry & Mielke's agreement score")
    def berry_mielke_score(self, c: float = 2.0) -> float:
        """
        Calculate Berry and Mielke's agreement index.

        delta = n^-1 * Σ |F_i - A_i|
        mu    = (c / n^2) * Σ Σ |F_j - A_i|
        R     = 1 - delta / mu

        Args:
            c: Scaling constant (default=2) balancing numerator and denominator.
        """
        if self.N == 0:
            return np.nan

        delta = bn.nanmean(np.abs(self.predictions - self.observations))
        pairwise = np.abs(np.subtract.outer(self.predictions, self.observations))
        mu = (c / (self.N ** 2)) * np.nansum(pairwise)

        if mu == 0 or np.isnan(mu):
            return np.nan
        return 1 - (delta / mu)

    @MetricRegistry.register("Distance Correlation", "dCor", "Distance correlation (Székely et al. 2007)")
    def distance_correlation(self) -> float:
        """
        Calculate the distance correlation between predictions and observations.

        Distance correlation detects both linear and non-linear associations.

        References:
            - Székely, G. J., Rizzo, M. L., & Bakirov, N. K. (2007).
              Measuring and testing dependence by correlation of distances.
              Annals of Statistics, 35(6), 2769–2794.
            - Rizzo, M. L., & Székely, G. J. (2022). Energy statistics for
              independent variables. Statistics & Probability Letters.

        Returns:
            float: Distance correlation in [0, 1]. 0 implies independence,
                   1 implies perfect dependence.
        """
        if self.N < 2:
            return np.nan

        obs = self.observations[:, None]
        preds = self.predictions[:, None]

        # Compute pairwise Euclidean distance matrices
        a = squareform(pdist(obs, metric="euclidean"))
        b = squareform(pdist(preds, metric="euclidean"))

        # Double centering
        mu_a = np.mean(a)
        mu_b = np.mean(b)
        mu_a_row = np.mean(a, axis=1)
        mu_b_row = np.mean(b, axis=1)

        A = a - mu_a_row[:, None] - mu_a_row[None, :] + mu_a
        B = b - mu_b_row[:, None] - mu_b_row[None, :] + mu_b

        # Distance covariance components
        dcov2_xy = max(np.mean(A * B), 0.0)
        dcov2_xx = max(np.mean(A * A), 0.0)
        dcov2_yy = max(np.mean(B * B), 0.0)

        if dcov2_xx == 0 or dcov2_yy == 0:
            return 0.0

        dcov_xy = np.sqrt(dcov2_xy)
        dcov_xx = np.sqrt(dcov2_xx)
        dcov_yy = np.sqrt(dcov2_yy)

        return dcov_xy / np.sqrt(dcov_xx * dcov_yy)

    @MetricRegistry.register("Duveiller Agreement Coefficient", "lambda", "Symmetric agreement coefficient (Duveiller et al. 2016)")
    def duveiller_agreement_coefficient(self) -> float:
        """
        Calculate Duveiller's agreement coefficient (lambda).

        Reference:
            Duveiller, G., Fasbender, D., & Meroni, M. (2016).
            Revisiting the concept of a symmetric index of agreement for continuous datasets.
            Scientific Reports, 6, 19401. https://doi.org/10.1038/srep19401

        Formula:
            lambda = 1 - MSE / (Var(obs) + Var(pred) + MBE^2)

        Where:
            MSE = mean squared error between predictions and observations
            Var(obs) and Var(pred) are population variances (mean of squared deviations)
            MBE = mean(obs) - mean(pred) (mean bias error)

        Returns:
            float: Duveiller's agreement coefficient in (-inf, 1], where 1 indicates perfect agreement.
        """
        mse = bn.nanmean(self.diff ** 2)
        var_obs = bn.nanmean((self.observations - self.obs_mean) ** 2)
        var_pred = bn.nanmean((self.predictions - self.pred_mean) ** 2)
        mbe = self.obs_mean - self.pred_mean

        denominator = var_obs + var_pred + mbe ** 2
        if denominator == 0:
            return 1.0
        return 1 - (mse / denominator)

    @MetricRegistry.register("Inter-Quartile RMSE", "iqRMSE", "Inter-Quartile Root Mean Squared Error")
    def interquartile_rmse(self) -> float:
        """
        Calculate the inter-quartile Root Mean Squared Error (iqRMSE).

        iqRMSE normalizes RMSE by the inter-quartile range (IQR) of observations.
        Reference: Correndo et al., metrica package (https://adriancorrendo.github.io/metrica/).

        Returns:
            float: iqRMSE value. Lower is better.
        """
        rmse = self.root_mean_squared_error()
        q75 = np.percentile(self.observations, 75)
        q25 = np.percentile(self.observations, 25)
        iqr = q75 - q25
        if iqr == 0:
            return np.inf
        return rmse / iqr

    @MetricRegistry.register("SMA Regression Metrics", "SMA", "SMA regression and error decomposition (Correndo et al. 2021)")
    def sma_metrics(self) -> Tuple[float, float, float, float, float, float, float]:
        """
        Calculate SMA regression parameters and MSE decomposition (MLA/MLP).

        Reference:
            Correndo et al. (2021). https://doi.org/10.1016/j.agsy.2021.103194

        Returns:
            Tuple containing:
                - smaslope: SMA slope
                - smaintercept: SMA intercept
                - mse: Mean Squared Error
                - mla: Mean Lack of Accuracy (systematic error)
                - mlp: Mean Lack of Precision (unsystematic error)
                - pla_percent: Percentage contribution of MLA
                - plp_percent: Percentage contribution of MLP
        """
        mean_obs = self.obs_mean
        mean_sim = self.pred_mean

        std_obs = bn.nanstd(self.observations)
        std_sim = bn.nanstd(self.predictions)

        r = self.correlation_coefficient()
        if np.isnan(r):
            r = 0.0

        slope_sma = np.sign(r) * (std_sim / std_obs) if std_obs != 0 else 0.0
        intercept_sma = mean_sim - (slope_sma * mean_obs)

        mse = bn.nanmean(self.diff ** 2)
        mla = (mean_sim - mean_obs) ** 2 + (std_sim - std_obs) ** 2
        mlp = 2 * std_sim * std_obs * (1 - r)

        if mse == 0:
            pla = 0.0
            plp = 0.0
        else:
            pla = (mla / mse) * 100
            plp = (mlp / mse) * 100

        return slope_sma, intercept_sma, mse, mla, mlp, pla, plp

    def linear_regression(self) -> Tuple[float, float]:
        """Perform linear regression of observations on predictions."""
        return self._linreg

    @MetricRegistry.register("Non-parametric KGE", "RNP", "Non-parametric Kling-Gupta efficiency")
    def rnp(self) -> Tuple[float, float, float, float]:
        """
        Calculate non-parametric Kling-Gupta efficiency (RNP).
        
        RNP consists of three components:
        - mean discharge (beta component)
        - normalized flow duration curve (alpha component)
        - Spearman rank correlation (r component)
        
        A perfect fit results in a RNP value of 1.
        
        Returns:
            Tuple[float, float, float, float]: (RNP value, r component, alpha component, beta component)
        """
        # Calculate means
        mean_sim = bn.nanmean(self.predictions)
        mean_obs = bn.nanmean(self.observations)
        
        # Calculate normalized flow duration curves
        fdc_sim = np.sort(self.predictions / (mean_sim * self.N))
        fdc_obs = np.sort(self.observations / (mean_obs * self.N))
        
        # Calculate alpha component (flow duration curve similarity)
        rnp_alpha = 1 - 0.5 * bn.nansum(np.abs(fdc_sim - fdc_obs))
        
        # Calculate beta component (mean ratio)
        rnp_beta = _safe_divide(mean_sim, mean_obs)
        
        # Calculate r component (Spearman correlation)
        from scipy.stats import spearmanr
        rnp_r = spearmanr(self.predictions, self.observations)[0]
        
        # Calculate RNP value
        rnp = 1 - np.sqrt((rnp_alpha - 1)**2 + (rnp_beta - 1)**2 + (rnp_r - 1)**2)
        
        return rnp, rnp_r, rnp_alpha, rnp_beta

    def _normalized_error(self) -> Optional[np.ndarray]:
        """Return normalized error array nE = (pred - obs) / max(pred)."""
        if hasattr(self, "_normalized_error_cache"):
            return self._normalized_error_cache

        max_pred = bn.nanmax(self.predictions)
        if not np.isfinite(max_pred) or np.isclose(max_pred, 0.0):
            self._normalized_error_cache = None
            return self._normalized_error_cache

        self._normalized_error_cache = (self.predictions - self.observations) / max_pred
        return self._normalized_error_cache

    @MetricRegistry.register("Taylor Skill Score", "TSS", "Taylor skill score")
    def taylor_skill_score(self) -> float:
        """Calculate Taylor skill score."""
        r = self.correlation_coefficient()
        std_ratio = _safe_divide(np.std(self.predictions), np.std(self.observations))
        return _safe_divide(
            4 * (1 + r)**4,
            (_safe_divide(1, std_ratio) + std_ratio)**2 * (1 + 1)**4,
        )

    @MetricRegistry.register("Mean Values", "MEAN", "Mean values of observations and predictions")
    def meann(self) -> Tuple[float, float]:
        """Return means of observations and predictions."""
        return self.obs_mean, self.pred_mean

    @MetricRegistry.register("Median Values", "MEDIAN", "Median values of observations and predictions")
    def mediann(self) -> Tuple[float, float]:
        """Return medians of observations and predictions."""
        return bn.nanmedian(self.observations), bn.nanmedian(self.predictions)

    def normed_mean_bias_factor(self) -> Tuple[float, float]:
        """Calculate Normed Mean Bias Factor and Normalized Mean Absolute Error Factor."""
        mage = self.mean_absolute_gross_error()
        if self.pred_mean >= self.obs_mean:
            nmbf = _safe_divide(bn.nansum(self.predictions), bn.nansum(self.observations)) - 1
            nmaef = _safe_divide(mage, self.obs_mean)
        else:
            nmbf = 1 - _safe_divide(bn.nansum(self.observations), bn.nansum(self.predictions))
            nmaef = _safe_divide(mage, self.pred_mean)
        return nmbf, nmaef

    def revised_nmbf(self) -> Tuple[float, float]:
        """Calculate Revised Normed Mean Bias Factor and Normalized Mean Absolute Error Factor."""
        mage = self.mean_absolute_gross_error()
        pred_ratio = _safe_divide(self.pred_mean, np.abs(self.pred_mean))
        obs_ratio = _safe_divide(self.obs_mean, np.abs(self.obs_mean))

        if self.pred_mean >= self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = np.abs(_safe_divide(bn.nansum(self.predictions), bn.nansum(self.observations))) - 1
            nmaef = _safe_divide(mage, np.abs(self.obs_mean))
        elif self.pred_mean < self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = 1 - np.abs(_safe_divide(bn.nansum(self.observations), bn.nansum(self.predictions)))
            nmaef = _safe_divide(mage, np.abs(self.pred_mean))
        else:
            nmbf, nmaef = np.nan, np.nan

        return nmbf, nmaef

    @MetricRegistry.register("Centered Root Mean Square", "CRMSE", "Centered root mean square error")
    def centered_root_mean_square(self) -> float:
        """Calculate centered (unbiased) root mean square error."""
        return np.sqrt(
            np.mean(
                (
                    (self.predictions - np.mean(self.predictions))
                    - (self.observations - np.mean(self.observations))
                )
                ** 2
            )
        )

    @MetricRegistry.register("Mean Squared Logarithmic Error", "MSLE", "Mean squared logarithmic error")
    def mean_squared_logarithmic_error(self) -> float:
        """
        Calculate Mean Squared Logarithmic Error (MSLE).
        
        MSLE is similar to MSE but uses the natural logarithm of the predictions and observations.
        This metric is useful when you want to penalize underestimates more than overestimates.
        
        Returns:
            float: The MSLE value
        """
        # Add 1 to avoid log(0)
        log_pred = np.log1p(self.predictions)
        log_obs = np.log1p(self.observations)
        return bn.nanmean((log_pred - log_obs) ** 2)

    @MetricRegistry.register("Normalized Absolute Error", "NAE", "Normalized Absolute Error")
    def normalized_absolute_error(self) -> float:
        """
        Calculate the Normalized Absolute Error (NAE) between predictions and observations.
        
        NAE is calculated as the mean of absolute differences divided by the mean of the sum
        of predictions and observations.
        
        Returns:
            float: Normalized Absolute Error (NAE)
        """
        nae = np.abs(self.diff) / (0.5 * (self.predictions + self.observations))
        return bn.nanmean(nae)

    @MetricRegistry.register("Gini Coefficient", "Gini", "Gini coefficient for ranking evaluation")
    def gini_coefficient(self) -> float:
        """
        Calculate Gini coefficient for ranking evaluation.
        
        Based on Ben Hamner's implementation:
        https://github.com/benhamner/Metrics/blob/master/MATLAB/metrics/gini.m
        
        The Gini coefficient measures the inequality of a distribution and is commonly
        used in machine learning competitions for ranking problems.
        
        Algorithm:
        1. Sort predictions in descending order
        2. Calculate cumulative population and loss percentages  
        3. Compute area between Lorenz curve and diagonal
        
        Range: [0, 1]
        Perfect score: 1 (maximum inequality/perfect ranking)
        
        Note: Higher values indicate better ranking ability.
        """
        if self.N == 0:
            return np.nan
            
        # Sort by predictions in descending order
        sort_indices = np.argsort(-self.predictions)
        
        population_delta = 1.0 / self.N
        accumulated_population_percentage_sum = 0.0
        accumulated_loss_percentage_sum = 0.0
        score = 0.0
        total_losses = bn.nansum(self.observations)
        
        if total_losses == 0:
            return np.nan
            
        for i in range(self.N):
            loc = sort_indices[i]
            accumulated_loss_percentage_sum += self.observations[loc] / total_losses
            accumulated_population_percentage_sum += population_delta
            score += accumulated_loss_percentage_sum - accumulated_population_percentage_sum
            
        return score / self.N

    @MetricRegistry.register("Prediction of Change in Direction", "PCD", "Prediction of Change in Direction")
    def prediction_of_change_in_direction(self) -> float:
        """
        Calculate Prediction of Change in Direction (PCD).
        
        Based on Permetrics implementation:
        https://permetrics.readthedocs.io/en/latest/pages/regression/PCD.html
        
        PCD evaluates how well a model predicts the direction of change in a time series.
        It measures the proportion of times the model correctly predicts whether the 
        target variable will increase or decrease.
        
        Formula: PCD = (1/(n-1)) × ∑[I((f_i - f_{i-1})(y_i - y_{i-1}) > 0)]
        
        Where:
        - f_i is the predicted value at time i
        - y_i is the actual value at time i
        - I(·) is the indicator function (1 if true, 0 if false)
        
        Range: [0, 1]
        Perfect score: 1.0 (bigger is better)
        
        Note: Requires at least 2 data points for calculation.
        """
        if self.N < 2:
            return np.nan
            
        # Calculate differences between consecutive points
        pred_diff = self.predictions[1:] - self.predictions[:-1]
        obs_diff = self.observations[1:] - self.observations[:-1]
        
        # Check if direction changes match (both positive or both negative)
        # This is equivalent to checking if their product is positive
        direction_matches = (pred_diff * obs_diff) > 0
        
        # Calculate PCD as proportion of correct direction predictions
        return np.sum(direction_matches) / (self.N - 1)

    def get_metrics(self, metric_names: List[str], round_factor: int = 2) -> Dict[str, float]:
        """
        Calculate specified metrics.
        
        Args:
            metric_names: List of metric abbreviations to calculate
            round_factor: Number of decimal places to round results
            
        Returns:
            Dictionary of metric names and their values
        """
        results = {}
        for name in metric_names:
            try:
                metric_info = MetricRegistry.get_metric(name)
                value = metric_info.function(self)
                if isinstance(value, tuple):
                    results[name] = tuple(round(v, round_factor) if isinstance(v, float) else v 
                                        for v in value)
                else:
                    results[name] = round(value, round_factor) if isinstance(value, float) else value
            except Exception as e:
                warnings.warn(f"Failed to calculate {name}: {str(e)}")
                results[name] = np.nan
        return results

    def all_metrics(self, round_factor: int = 2) -> Dict[str, float]:
        """
        Calculate all available metrics.
        
        Args:
            round_factor: Number of decimal places to round results
            
        Returns:
            Dictionary of all metric names and their values
        """
        return self.get_metrics(list(MetricRegistry.get_all_metrics().keys()), round_factor)

    def print_abbreviations(self, verbose: bool = False) -> None:
        """
        Print available metric abbreviations and their descriptions.
        
        Args:
            verbose: If True, print detailed descriptions
        """
        for abbr, info in MetricRegistry.get_all_metrics().items():
            if verbose:
                print(f"{abbr}: {info.name} - {info.description}")
            else:
                print(f"{abbr}: {info.name}")
