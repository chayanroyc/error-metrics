#!/usr/bin/env python3

import numpy as np
import bottleneck as bn
from typing import Dict, List, Tuple, Union, Callable
from dataclasses import dataclass
from functools import wraps
import warnings
from statsmodels.distributions.empirical_distribution import ECDF

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
        self.predictions = np.array(predictions, dtype=float).ravel()
        self.observations = np.array(observations, dtype=float).ravel()
        self._preprocess_data()
        
        self.N = len(self.predictions)
        if self.N == 0:
            raise ValueError("No valid data points after preprocessing")
            
        self.diff = self.predictions - self.observations
        self.sum_ = self.predictions + self.observations
        self.pred_mean = bn.nanmean(self.predictions)
        self.obs_mean = bn.nanmean(self.observations)

    def _preprocess_data(self):
        """Remove NaNs and infinities from predictions and observations."""
        mask = np.isfinite(self.predictions) & np.isfinite(self.observations)
        self.predictions = self.predictions[mask]
        self.observations = self.observations[mask]

    @MetricRegistry.register("Mean Bias", "MB", "Mean Bias")
    def mean_bias(self) -> float:
        """Calculate mean bias."""
        return self.pred_mean - self.obs_mean

    @MetricRegistry.register("Mean Absolute Error", "MAE", "Mean Absolute Error")
    def mean_absolute_error(self) -> float:
        """Calculate mean absolute error."""
        return bn.nanmean(np.abs(self.diff))

    @MetricRegistry.register("Root Mean Squared Error", "RMSE", "Root Mean Squared Error")
    def root_mean_squared_error(self) -> float:
        """Calculate root mean squared error."""
        return np.sqrt(bn.nanmean(self.diff ** 2))

    @MetricRegistry.register("Correlation Coefficient", "R", "Pearson correlation coefficient")
    def correlation_coefficient(self) -> float:
        """Calculate Pearson correlation coefficient."""
        if self.N < 2:  # Need at least 2 points for correlation
            return np.nan
        return np.corrcoef(self.predictions, self.observations)[0, 1]

    @MetricRegistry.register("Spearman Rank Correlation", "SpearmanR", "Spearman rank correlation coefficient")
    def spearman_r(self) -> float:
        """Calculate Spearman rank correlation coefficient."""
        from scipy import stats
        return stats.spearmanr(self.predictions, self.observations)[0]

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
        return numerator / denominator

    @MetricRegistry.register("Explained Variance", "EV", "Proportion of variance explained")
    def ev(self) -> float:
        """Calculate Explained Variance."""
        return 1 - bn.nanvar(self.diff) / bn.nanvar(self.observations)

    @MetricRegistry.register("Normalized Mean Square Error", "NMSE", "Normalized mean square error")
    def nmse(self) -> float:
        """Calculate Normalized Mean Square Error."""
        return bn.nanmean(self.diff**2) / (bn.nanmean(self.predictions) * bn.nanmean(self.observations))

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
        return (sum_predictions - sum_observations) / sum_observations

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
        return 1 - (ss_res / ss_tot)

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
        # Calculate mean absolute error
        mae = bn.nanmean(np.abs(self.diff))
        
        # Calculate mean absolute difference of observations
        mad = bn.nanmean(np.abs(np.diff(self.observations)))
        
        # Calculate MASE
        return mae / mad

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
        return 1 - (ss_res / ss_tot)

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

    @MetricRegistry.register("Mean Absolute Gross Error", "MAGE", "Mean Absolute Gross Error")
    def mean_absolute_gross_error(self) -> float:
        """Calculate mean absolute gross error."""
        return bn.nanmean(np.abs(self.diff))

    @MetricRegistry.register("Factor of Observations 2", "FAC2", "Factor of Observations 2")
    def factor_of_observations2(self) -> float:
        """Calculate factor of observations 2 (FAC2)."""
        ratio = self.predictions / self.observations
        valid = (ratio >= 0.5) & (ratio <= 2.0)
        return 100 * bn.nansum(valid) / self.N

    @MetricRegistry.register("Mean Bias Difference", "MBD", "Mean Bias Difference")
    def mean_bias_difference(self) -> float:
        """Calculate mean bias difference."""
        return (100 / self.obs_mean) * bn.nanmean(self.diff)

    @MetricRegistry.register("Root Mean Square Difference", "RMSD", "Root Mean Square Difference")
    def root_mean_square_difference(self) -> float:
        """Calculate root mean square difference."""
        return (100 / self.obs_mean) * np.sqrt(bn.nanmean(self.diff ** 2))

    @MetricRegistry.register("Mean Absolute Difference", "MAD", "Mean Absolute Difference")
    def mean_absolute_difference(self) -> float:
        """Calculate mean absolute difference."""
        return (100 / self.obs_mean) * bn.nanmean(np.abs(self.diff))

    @MetricRegistry.register("Standard Deviation of Residual", "SD", "Standard Deviation of Residual")
    def standard_deviation_of_residual(self) -> float:
        """Calculate standard deviation of the residual."""
        residual = self.diff
        return (100 / self.obs_mean) * np.sqrt(bn.nanmean(residual ** 2) - (bn.nanmean(residual) ** 2))

    @MetricRegistry.register("Slope of Best-Fit Line", "SBF", "Slope of Best-Fit Line")
    def slope_of_best_fit_line(self) -> float:
        """Calculate slope of best-fit line."""
        numerator = bn.nansum((self.predictions - self.pred_mean) * (self.observations - self.obs_mean))
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return numerator / denominator

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
        return np.sqrt((self.N - 1) * (mbd ** 2) / (rmsd ** 2 - mbd ** 2))

    @MetricRegistry.register("Nash-Sutcliffe Efficiency", "NSE", "Nash-Sutcliffe Efficiency")
    def nash_sutcliffe_efficiency(self) -> float:
        """Calculate Nash-Sutcliffe efficiency."""
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return 1 - (numerator / denominator)

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
        return 1 / (2 - nse)

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
        return numerator / denominator

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
        return 100 * (numerator / denominator)

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

    @MetricRegistry.register("Kling-Gupta Efficiency", "KGE", "Kling-Gupta Efficiency")
    def kling_gupta_efficiency(self) -> Tuple[float, float, float, float]:
        """Calculate Kling-Gupta efficiency and its components."""
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        alpha = std_pred / std_obs
        beta = self.pred_mean / self.obs_mean
        kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        return kge, r, alpha, beta

    @MetricRegistry.register("Willmott's Index of Agreement", "WIA", "Willmott's Index of Agreement")
    def willmotts_index_of_agreement(self) -> float:
        """Calculate Willmott's index of agreement."""
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((np.abs(self.predictions - self.obs_mean) + 
                               np.abs(self.observations - self.obs_mean)) ** 2)
        return 1 - (numerator / denominator)

    @MetricRegistry.register("Legates Coefficient of Efficiency", "LCE", "Legates Coefficient of Efficiency")
    def legates_coefficient_of_efficiency(self) -> float:
        """Calculate Legates coefficient of efficiency."""
        numerator = bn.nansum(np.abs(self.predictions - self.observations))
        denominator = bn.nansum(np.abs(self.observations))
        return 1 - (numerator / denominator)

    @MetricRegistry.register("Kolmogorov-Smirnov Test Integral", "KSI", "Measure of distribution similarity")
    def ksi(self, normed: bool = True) -> float:
        """
        Calculate Kolmogorov-Smirnov Test Integral (KSI).
        
        Args:
            normed: If True, return the normalized KSI [%]
            
        Returns:
            KSI value
        """
        ecdf_obs = ECDF(self.observations)
        ecdf_fx = ECDF(self.predictions)

        x = np.unique(np.concatenate((self.observations, self.predictions)))
        y_o = ecdf_obs(x)
        y_f = ecdf_fx(x)

        D = np.abs(y_o - y_f)
        ksi = np.sum(D[:-1] * np.diff(x))

        if normed:
            Vc = 1.63 / np.sqrt(len(self.observations))
            a_critical = Vc * (x.max() - x.min())
            return ksi * 100 / a_critical
        return ksi

    @MetricRegistry.register("Over-estimation Metric", "OVER", "Measure of over-estimation")
    def over_metric(self, normed: bool = True) -> float:
        """
        Calculate Over-estimation (oVER) Metric.
        
        Args:
            normed: If True, return the normalized OVER [%]
            
        Returns:
            Over-estimation value
        """
        ecdf_obs = ECDF(self.observations)
        ecdf_fx = ECDF(self.predictions)

        x = np.unique(np.concatenate((self.observations, self.predictions)))
        y_o = ecdf_obs(x)
        y_f = ecdf_fx(x)

        D = np.maximum(y_f - y_o, 0)
        over = np.sum(D[:-1] * np.diff(x))

        if normed:
            Vc = 1.63 / np.sqrt(len(self.observations))
            a_critical = Vc * (x.max() - x.min())
            return over * 100 / a_critical
        return over

    @MetricRegistry.register("Interquartile Range", "IQR", "Measure of statistical dispersion")
    def IQR(self) -> float:
        """Calculate Interquartile Range."""
        return np.percentile(self.observations, 75) - np.percentile(self.observations, 25)

    @MetricRegistry.register("Standard Deviation", "STD", "Measure of data spread")
    def STD(self) -> float:
        """Calculate Standard Deviation."""
        return bn.nanstd(self.observations)

    @MetricRegistry.register("Mean Square Deviation", "MSD", "Average of squared deviations")
    def msd(self) -> float:
        """Calculate Mean Square Deviation."""
        return bn.nanmean(self.diff ** 2)

    @MetricRegistry.register("Systematic Bias", "SB", "Measure of systematic error")
    def sb(self) -> float:
        """Calculate Systematic Bias."""
        return bn.nanmean(self.diff) ** 2

    @MetricRegistry.register("Normalized Mean Bias Factor", "NMBF", "Measure of bias factor")
    def nmbf(self) -> float:
        """Calculate Normalized Mean Bias Factor."""
        return bn.nanmean(self.predictions) / bn.nanmean(self.observations)

    @MetricRegistry.register("Relative Normalized Mean Bias Factor", "RNMBF", "Measure of relative bias factor")
    def rnmbf(self) -> float:
        """Calculate Relative Normalized Mean Bias Factor."""
        return np.abs(self.nmbf() - 1)

    @MetricRegistry.register("Combined Performance Index", "CPI", "Overall performance measure")
    def cpi(self) -> float:
        """Calculate Combined Performance Index."""
        return 1 - (self.mean_bias() / self.obs_mean) ** 2

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

        return (Aov_sum / (Aov_sum + Afn_sum + Afp_sum)) * 100

    @MetricRegistry.register("Non-uniformity", "NU", "Measure of non-uniformity")
    def nu(self) -> float:
        """Calculate Non-uniformity."""
        b1, _ = self.linear_regression()
        return (1 - b1) ** 2 * bn.nanmean((self.predictions - bn.nanmean(self.predictions)) ** 2)

    @MetricRegistry.register("Lack of Correlation", "LC", "Measure of correlation deficiency")
    def lc(self) -> float:
        """Calculate Lack of Correlation."""
        _, r2 = self.linear_regression()
        return (1 - r2) * bn.nanmean((self.observations - bn.nanmean(self.observations)) ** 2)

    @MetricRegistry.register("Skill Score vs Climatology", "SS", "Skill score against climatology")
    def skill_score_against_climatology(self) -> float:
        """Calculate skill score against climatology."""
        climatology = np.full_like(self.observations, bn.nanmean(self.observations))
        ss_res = bn.nansum((self.predictions - self.observations) ** 2)
        ss_clim = bn.nansum((climatology - self.observations) ** 2)
        return 1 - (ss_res / ss_clim)

    @MetricRegistry.register("Anderson-Darling Distance", "AD", "Anderson-Darling distance")
    def anderson_darling_distance(self) -> float:
        """Calculate Anderson-Darling distance."""
        ecdf_obs = ECDF(self.observations)
        ecdf_pred = ECDF(self.predictions)
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
        obs_trend = np.polyfit(np.arange(len(self.observations)), self.observations, 1)[0]
        pred_trend = np.polyfit(np.arange(len(self.predictions)), self.predictions, 1)[0]
        return 1 - abs(obs_trend - pred_trend) / (abs(obs_trend) + 1e-10)

    def linear_regression(self) -> Tuple[float, float]:
        """Perform linear regression of observations on predictions."""
        x = self.predictions
        y = self.observations
        x_mean = bn.nanmean(x)
        y_mean = bn.nanmean(y)
        
        # Calculate slope (b1) and intercept (b0)
        b1 = bn.nansum((x - x_mean) * (y - y_mean)) / bn.nansum((x - x_mean) ** 2)
        b0 = y_mean - b1 * x_mean
        
        # Calculate R-squared
        ss_total = bn.nansum((y - y_mean) ** 2)
        ss_residual = bn.nansum((y - (b0 + b1 * x)) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        
        return b1, r2

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
        rnp_beta = mean_sim / mean_obs
        
        # Calculate r component (Spearman correlation)
        from scipy.stats import spearmanr
        rnp_r = spearmanr(self.predictions, self.observations)[0]
        
        # Calculate RNP value
        rnp = 1 - np.sqrt((rnp_alpha - 1)**2 + (rnp_beta - 1)**2 + (rnp_r - 1)**2)
        
        return rnp, rnp_r, rnp_alpha, rnp_beta

    @MetricRegistry.register("Taylor Skill Score", "TSS", "Taylor skill score")
    def taylor_skill_score(self) -> float:
        """Calculate Taylor skill score."""
        r = self.correlation_coefficient()
        std_ratio = np.std(self.predictions) / np.std(self.observations)
        return 4 * (1 + r)**4 / ((std_ratio + 1/std_ratio)**2 * (1 + 1)**4)

    @MetricRegistry.register("Mean Values", "MEAN", "Mean values of observations and predictions")
    def meann(self) -> Tuple[float, float]:
        """Return means of observations and predictions."""
        return self.obs_mean, self.pred_mean

    @MetricRegistry.register("Median Values", "MEDIAN", "Median values of observations and predictions")
    def mediann(self) -> Tuple[float, float]:
        """Return medians of observations and predictions."""
        return bn.nanmedian(self.observations), bn.nanmedian(self.predictions)

    @MetricRegistry.register("Normed Mean Bias Factor", "NMBF", "Normed Mean Bias Factor")
    def normed_mean_bias_factor(self) -> Tuple[float, float]:
        """Calculate Normed Mean Bias Factor and Normalized Mean Absolute Error Factor."""
        mage = self.mean_absolute_gross_error()
        if self.pred_mean >= self.obs_mean:
            nmbf = bn.nansum(self.predictions) / bn.nansum(self.observations) - 1
            nmaef = mage / self.obs_mean
        else:
            nmbf = 1 - bn.nansum(self.observations) / bn.nansum(self.predictions)
            nmaef = mage / self.pred_mean
        return nmbf, nmaef

    @MetricRegistry.register("Revised Normed Mean Bias Factor", "RNMBF", "Revised Normed Mean Bias Factor")
    def revised_nmbf(self) -> Tuple[float, float]:
        """Calculate Revised Normed Mean Bias Factor and Normalized Mean Absolute Error Factor."""
        mage = self.mean_absolute_gross_error()
        pred_ratio = self.pred_mean / np.abs(self.pred_mean)
        obs_ratio = self.obs_mean / np.abs(self.obs_mean)

        if self.pred_mean >= self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = np.abs(bn.nansum(self.predictions) / bn.nansum(self.observations)) - 1
            nmaef = mage / np.abs(self.obs_mean)
        elif self.pred_mean < self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = 1 - np.abs(bn.nansum(self.observations) / bn.nansum(self.predictions))
            nmaef = mage / np.abs(self.pred_mean)
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