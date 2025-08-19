#!/glade/work/chayan/conda-envs/gpu/bin/python3.9

import numpy as np
import os
import sys
import bottleneck as bn

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class ErrorMetrics:
    def __init__(self, predictions, observations):

        self.predictions = np.array(predictions).ravel()
        self.observations = np.array(observations).ravel()
        self._preprocess_data()

        self.N = len(self.predictions)

        self.diff = self.predictions - self.observations
        self.sum_ = self.predictions + self.observations
        self.pred_mean = bn.nanmean(self.predictions)
        self.obs_mean = bn.nanmean(self.observations)

    def _preprocess_data(self):
        """Remove NaNs from predictions and observations."""
        mask = np.isfinite(self.predictions) & np.isfinite(self.observations)
        self.predictions = self.predictions[mask]
        self.observations = self.observations[mask]

    def figure_of_merit(self):
        "Figure of Merit, FMS, Warren 2003"

        # Aov = np.nanmin(
        #     np.array([self.observations, self.predictions]), axis=0).ravel()
        # Afn = np.maximum(self.observations.ravel() - Aov, 0)
        # Afp = np.maximum(self.predictions.ravel() - Aov, 0)

        # Aov = bn.nansum(Aov)
        # Afn = bn.nansum(Afn)
        # Afp = bn.nansum(Afp)

        # return (Aov / (Aov + Afn + Afp)) * 1e2

        Aov = np.minimum(self.observations, self.predictions)
        Afn = np.maximum(self.observations - Aov, 0)
        Afp = np.maximum(self.predictions - Aov, 0)

        Aov_sum = bn.nansum(Aov)
        Afn_sum = bn.nansum(Afn)
        Afp_sum = bn.nansum(Afp)

        return (Aov_sum / (Aov_sum + Afn_sum + Afp_sum)) * 100

    def mean_bias(self):
        """Mean Bias (MB)"""
        return self.pred_mean - self.obs_mean

    def mean_absolute_error(self):
        """Mean Absolute Error (MAE)"""
        return bn.nanmean(np.abs(self.diff))

    def root_mean_squared_error(self):
        """Root Mean Squared Error (RMSE)"""
        return np.sqrt(bn.nanmean(self.diff ** 2))

    def correlation_coefficient(self):
        if self.N == 0:
            return np.nan
        return np.corrcoef(self.predictions, self.observations)[0, 1]

    def mean_normalized_bias(self):
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return bn.nanmean(self.diff / safe_obs)

    def mean_normalized_absolute_error(self):
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return bn.nanmean(np.abs(self.diff) / safe_obs)

    def fractional_bias(self):
        safe_sum = np.where(self.sum_ == 0, np.nan, self.sum_)
        return 2 * bn.nanmean(self.diff / safe_sum)

    def fractional_absolute_error(self):
        safe_sum = np.where(self.sum_ == 0, np.nan, self.sum_)
        return 2 * bn.nanmean(np.abs(self.diff) / safe_sum)

    def mean_absolute_gross_error(self):
        return bn.nanmean(np.abs(self.diff))

    def normed_mean_bias_factor(self):
        """Normed Mean Bias Factor"""
        mage = self.mean_absolute_gross_error()
        if self.pred_mean >= self.obs_mean:
            nmbf = bn.nansum(self.predictions) / \
                             bn.nansum(self.observations) - 1
            nmaef = mage / self.obs_mean
        else:
            nmbf = 1 - bn.nansum(self.observations) / \
                                 bn.nansum(self.predictions)
            nmaef = mage / self.pred_mean
        return nmbf, nmaef

    def revised_nmbf(self):
        """Revised NMBF"""
        mage = self.mean_absolute_gross_error()
        pred_ratio = self.pred_mean / np.abs(self.pred_mean)
        obs_ratio = self.obs_mean / np.abs(self.obs_mean)

        if self.pred_mean >= self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = np.abs(bn.nansum(self.predictions) /
                          bn.nansum(self.observations)) - 1
            nmaef = mage / np.abs(self.obs_mean)
        elif self.pred_mean < self.obs_mean and np.allclose(pred_ratio, obs_ratio):
            nmbf = 1 - np.abs(bn.nansum(self.observations) /
                              bn.nansum(self.predictions))
            nmaef = mage / np.abs(self.pred_mean)
        else:
            nmbf, nmaef = np.nan, np.nan

        return nmbf, nmaef

    def factor_of_observations2(self):
        """Factor of Observations 2 (FAC2)"""
        ratio = self.predictions / self.observations
        valid = (ratio >= 0.5) & (ratio <= 2.0)
        return 100 * bn.nansum(valid) / self.N

    def mean_bias_difference(self):
        """Mean Bias Difference (MBD)"""
        return (100 / self.obs_mean) * bn.nanmean(self.diff)

    def root_mean_square_difference(self):
        """Root Mean Square Difference (RMSD)"""
        return (100 / self.obs_mean) * np.sqrt(bn.nanmean(self.diff ** 2))

    def mean_absolute_difference(self):
        """Mean Absolute Difference (MAD)"""
        return (100 / self.obs_mean) * bn.nanmean(np.abs(self.diff))

    def standard_deviation_of_residual(self):
        """Standard Deviation of the Residual (SD)"""
        residual = self.diff
        return (100 / self.obs_mean) * np.sqrt(bn.nanmean(residual ** 2) - (bn.nanmean(residual) ** 2))

    def coefficient_of_determination(self):
        """Coefficient of Determination (R^2)"""
        ss_tot = bn.nansum((self.observations - self.obs_mean) ** 2)
        ss_res = bn.nansum((self.observations - self.predictions) ** 2)
        return 1 - (ss_res / ss_tot)

    def slope_of_best_fit_line(self):
        """Slope of Best-Fit Line (SBF)"""
        numerator = bn.nansum((self.predictions - self.pred_mean)
                              * (self.observations - self.obs_mean))
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return numerator / denominator

    def uncertainty_95(self):
        """Uncertainty at 95% (U95)"""
        sd = self.standard_deviation_of_residual()
        rmsd = self.root_mean_square_difference()
        return 1.96 * np.sqrt(sd ** 2 + rmsd ** 2)

    def t_statistic(self):
        """t-Statistic (TS)"""
        mbd = self.mean_bias_difference()
        rmsd = self.root_mean_square_difference()
        return np.sqrt((self.N - 1) * (mbd ** 2) / (rmsd ** 2 - mbd ** 2))

    def nash_sutcliffe_efficiency(self):
        """Nash-Sutcliffe Efficiency (NSE)"""
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((self.observations - self.obs_mean) ** 2)
        return 1 - (numerator / denominator)

    def kling_gupta_efficiency(self):
        std_obs = bn.nanstd(self.observations)
        std_pred = bn.nanstd(self.predictions)
        r = np.corrcoef(self.observations, self.predictions)[0, 1]
        alpha = std_pred / std_obs
        beta = self.pred_mean / self.obs_mean
        kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        return kge, r, alpha, beta

    def willmotts_index_of_agreement(self):
        numerator = bn.nansum((self.predictions - self.observations) ** 2)
        denominator = bn.nansum((np.abs(
            self.predictions - self.obs_mean) + np.abs(self.observations - self.obs_mean)) ** 2)
        return 1 - (numerator / denominator)

    def legates_coefficient_of_efficiency(self):
        numerator = bn.nansum(np.abs(self.predictions - self.observations))
        denominator = bn.nansum(np.abs(self.observations))
        return 1 - (numerator / denominator)

    def meann(self):
        """Return means of observations and predictions"""
        return self.obs_mean, self.pred_mean

    def mediann(self):
        """Return medians of observations and predictions"""
        return bn.nanmedian(self.observations), bn.nanmedian(self.predictions)

    def ksi(self, normed=True):
        from statsmodels.distributions.empirical_distribution import ECDF

        """
        Kolmogorov-Smirnov Test Integral (KSI)

        Parameters:
        observations (array-like): Observed values
        predictions (array-like): Forecasted values
        normed (bool, optional): If True, return the normalized KSI [%]

        Returns:
        float: KSI value
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
        else:
            return ksi

    def over_metric(self, normed=True):
        from statsmodels.distributions.empirical_distribution import ECDF

        """
        Over-estimation (oVER) Metric

        Parameters:
        observations (array-like): Observed values
        predictions (array-like): Forecasted values

        Returns:
        float: Over-estimation value
        """
        ecdf_obs = ECDF(self.observations)
        ecdf_fx = ECDF(self.predictions)

        x = np.unique(np.concatenate((self.observations, self.predictions)))
        y_o = ecdf_obs(x)
        y_f = ecdf_fx(x)

        D = np.abs(y_o - y_f)
        Vc = 1.63 / np.sqrt(len(self.observations))
        Dstar = D - Vc
        Dstar[D <= Vc] = 0.0
        over = np.sum(Dstar[:-1] * np.diff(x))

        if normed:
            a_critical = Vc * (x.max() - x.min())
            return over * 100 / a_critical
        else:
            return over

    def combined_performance_index(self):
        """
        Combined Performance Index (CPI) metric.

        .. math::  \\text{CPI} = (\\text{KSI} + \\text{OVER} + 2 * \\text{RMSE}) / 4

        Parameters
        ----------
        obs : (n,) array-like
        Observed values.
        fx : (n,) array-like
        Forecasted values.

        Returns
        -------
        cpi : float
        The CPI between the true and predicted values.

        """
        ksi = self.ksi()
        ov = self.over_metric()
        rmsd = self.root_mean_square_difference()
        cpi = (ksi + ov + 2 * rmsd) / 4.0

        return cpi

    def relative_euclidean_distance(self):
        """
        Relative Euclidean Distance (D) metric.
        Reference: Wu et al. (2012), JGR Atmospheres 117, D12202
        """
        mean_obs = self.obs_mean
        mean_pred = self.pred_mean
    
        std_obs = np.std(self.observations)
        std_pred = np.std(self.predictions)
        
        correlation = self.correlation_coefficient()
    
        term1 = ((mean_pred - mean_obs) / mean_obs) ** 2
        term2 = ((std_pred - std_obs) / std_obs) ** 2
        term3 = (1 - correlation) ** 2
    
        distance = np.sqrt(term1 + term2 + term3)
         
        return distance


    def IQR(self):
        from scipy.stats import iqr
    
        return iqr(self.observations), iqr(self.predictions)

    def STD(self):
        return np.std(self.observations), np.std(self.predictions)

    def normalized_mean_square_error(self):
        # "https://link.springer.com/article/10.1007/s00703-003-0070-7"

        # normalized mean square error NMSE

        numerator = bn.nanmean(self.predictions - self.observations) ** 2
        denominator = bn.nanmean(self.observations) * \
        bn.nanmean(self.predictions)

        return numerator / denominator

    def centered_root_mean_square(self):
        """
        Centered (unbiased) root mean square error (CRMSE):

        .. math:: \\text{CRMSE} = \\sqrt{1/n \\sum_{i=1}^n (
            (\\text{fx}_i - \\text{fx}_\\text{avg}) -
            (\\text{obs}_i - \\text{obs}_\\text{avg}))^2 }

        where:

        .. math:: \\text{fx}_\\text{avg} = 1/n \\sum_{i=1} \\text{fx}_i
        .. math:: \\text{obs}_\\text{avg} = 1/n \\sum_{i=1} \\text{obs}_i

        Parameters
        ----------
        obs : (n,) array-like
            Observed values.
        fx : (n,) array-like
            Forecasted values.

        Returns
        -------
        crmse : float
            The CRMSE of the forecast.

        """

        return np.sqrt(
            np.mean(
                (
                    (self.predictions - np.mean(self.predictions))
                    - (self.observations - np.mean(self.observations))
                )
                ** 2
            )
        )

    def spearmanR(self):
        from scipy import stats
        res = stats.spearmanr(self.predictions, self.observations)
        return res.statistic


    def lins_concordance_correlation_coefficient(self):
        """
        Compute Lin's Concordance Correlation Coefficient between two datasets.
    
        Parameters:
        x : array-like
            First dataset.
        y : array-like
            Second dataset.
    
        Returns:
        rho_c : float
            Lin's Concordance Correlation Coefficient.
        """
        if len(self.observations) != len(self.predictions):
            raise ValueError("Datasets must have the same length")
    
        # Means
        mu_x = np.mean(self.predictions)
        mu_y = np.mean(self.observations)
    
        # Standard deviations
        sigma_x = np.std(self.predictions, ddof=1)
        sigma_y = np.std(self.observations, ddof=1)
    
        # Pearson correlation coefficient
        rho_xy = self.correlation_coefficient()
    
        # Lin's Concordance Correlation Coefficient
        rho_c = (2 * rho_xy * sigma_x * sigma_y) / \
        (sigma_x**2 + sigma_y**2 + (mu_x - mu_y)**2)
    
        return rho_c
    
    def msd(self):
        """
        Mean Squared Deviation (MSD)
        :return: float, MSD
        """
        return np.mean((self.observations - self.predictions) ** 2)

    def sb(self):
        """
        Systematic Bias (SB)
        :return: float, SB
        """
        return (np.mean(self.predictions) - np.mean(self.observations)) ** 2

    def linear_regression(self):
        """
        Perform linear regression of observations on predictions
        :return: tuple, slope (b1) and R-squared (r2)
        """
        x = self.predictions
        y = self.observations
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calculate slope (b1) and intercept (b0)
        b1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        b0 = y_mean - b1 * x_mean
        
        # Calculate R-squared
        ss_total = np.sum((y - y_mean) ** 2)
        ss_residual = np.sum((y - (b0 + b1 * x)) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        
        return b1, r2

    def nu(self):
        """
        Non-uniformity (NU)
        :return: float, NU
        """
        b1, _ = self.linear_regression()
        return (1 - b1) ** 2 * np.mean((self.predictions - np.mean(self.predictions)) ** 2)

    def lc(self):
        """
        Lack of Correlation (LC)
        :return: float, LC
        """
        _, r2 = self.linear_regression()
        return (1 - r2) * np.mean((self.observations - np.mean(self.observations)) ** 2)


    def rnp(self):

        """
        Pool et al., 2018
        Compute the Non-Parametric Efficiency (RNP) metric.
        
        RNP consists of three components: 
        - Mean discharge (beta component)
        - Normalized flow duration curve (alpha component)
        - Spearman rank correlation (r component)
        
        A perfect fit will result in an RNP value of 1.
        
        Parameters:
        sim (array-like): Simulated discharge (or any hydrologic variable) time series.
        obs (array-like): Observed discharge time series.
        
        Returns:
        float: The RNP metric.
        """

        # Calculate normalized flow duration curves
        # Note: In the R script, the data are normalized by (mean * length)
        
        # Sort normalized values
        fdc_sim = np.sort(self.predictions / (self.pred_mean * self.N))
        fdc_obs = np.sort(self.observations / (self.obs_mean * self.N))

        # Calculate alpha component:  
        # RNP.alpha = 1 - 0.5 * sum(|fdc_sim - fdc_obs|)
        RNP_alpha = 1 - 0.5 * np.sum(np.abs(fdc_sim - fdc_obs))
        
        # Calculate beta component: mean ratio
        RNP_beta = self.pred_mean / self.obs_mean
        
        # Calculate r component: Spearman rank correlation
        RNP_r = self.spearmanR()
        
        # Calculate overall RNP: 1 - sqrt( (alpha-1)^2 + (beta-1)^2 + (r-1)^2 )
        rnp_value = 1 - np.sqrt((RNP_alpha - 1)**2 + (RNP_beta - 1)**2 + (RNP_r - 1)**2)

        return rnp_value, RNP_alpha, RNP_beta, RNP_r

    def explained_variance(self):
        var_obs = np.nanvar(self.observations)
        var_res = np.nanvar(self.observations - self.predictions)
        return 1 - var_res / var_obs

    def taylor_skill_score(self):
        r = self.correlation_coefficient()
        std_pred = np.std(self.predictions)
        std_obs = np.std(self.observations)
        return (4 * (r ** 2)) / ((1 + (std_pred / std_obs) ** 2) * (1 + r ** 2))

    def skill_score_against_climatology(self):
        climatology = np.full_like(self.observations, bn.nanmean(self.observations))
        ss_res = bn.nansum((self.predictions - self.observations) ** 2)
        ss_clim = bn.nansum((climatology - self.observations) ** 2)
        return 1 - (ss_res / ss_clim)

    def kullback_leibler_divergence(self):
        from scipy.special import rel_entr
    
        pred = self.predictions.copy()
        obs = self.observations.copy()
    
        # Convert to probability distributions
        pred = np.abs(pred)
        obs = np.abs(obs)
        
        pred = pred / bn.nansum(pred)
        obs = obs / bn.nansum(obs)
    
        return bn.nansum(rel_entr(np.abs(obs), pred))


    def anderson_darling_distance(self):
        from statsmodels.distributions.empirical_distribution import ECDF

        ecdf_obs = ECDF(self.observations)
        ecdf_pred = ECDF(self.predictions)
        x = np.sort(np.unique(np.concatenate((self.observations, self.predictions))))
        
        F = ecdf_obs(x)
        G = ecdf_pred(x)
        w = 1.0 / (F * (1 - F) + 1e-10)  # avoid divide-by-zero
        return np.sum((F - G) ** 2 * w)

    def mean_percentage_error(self):
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return 100 * bn.nanmean((self.predictions - self.observations) / safe_obs)

    def mean_absolute_percentage_error(self):
        safe_obs = np.where(self.observations == 0, np.nan, self.observations)
        return 100 * bn.nanmean(np.abs((self.predictions - self.observations) / safe_obs))

    def symmetric_mean_absolute_percentage_error(self):
        denom = (np.abs(self.observations) + np.abs(self.predictions)) / 2
        safe_denom = np.where(denom == 0, np.nan, denom)
        return 100 * bn.nanmean(np.abs(self.predictions - self.observations) / safe_denom)

    def continuous_ranked_probability_score(self):
        """
        Continuous Ranked Probability Score (CRPS)
        Measures the squared difference between the predicted and observed cumulative distributions.
        Lower values indicate better agreement. Range: [0, ∞)

        Returns:
            float: CRPS score

        Example Interpretation:
            A CRPS of 0.05 means the predictive distribution is tightly aligned with the observed distribution.
        """
        from statsmodels.distributions.empirical_distribution import ECDF
        x = np.sort(np.unique(np.concatenate((self.observations, self.predictions))))
        ecdf_obs = ECDF(self.observations)(x)
        ecdf_pred = ECDF(self.predictions)(x)
        return np.sum((ecdf_obs - ecdf_pred) ** 2) / len(x)

    def trend_accuracy(self):
        """
        Trend Accuracy (TAcc)
        Measures the percentage of times the predicted trend direction matches the observed trend.
        Higher values indicate better temporal trend agreement. Range: [0, 100]

        Returns:
            float: Trend accuracy as a percentage

        Example Interpretation:
            A TAcc of 85% means the model correctly captured the trend direction in 85% of the steps.
        """
        diff_obs = np.sign(np.diff(self.observations))
        diff_pred = np.sign(np.diff(self.predictions))
        return 100 * np.mean(diff_obs == diff_pred)


    # def get_metrics(self, metric_names, round_factor=2):
    #     """Return only the specified metrics as a dictionary."""
    #     available_metrics = self.all_metrics(round_factor=round_factor)

    #     selected_metrics = {
    #         name: np.round(available_metrics[name], round_factor)
    #         for name in metric_names
    #         if name in available_metrics
    #     }
    #     return selected_metrics

    def get_metrics(self, metric_names, round_factor=2):
        """
        Returns only selected metrics specified in the `metric_names` list.

        Args:
            metric_names (list of str): List of abbreviations (e.g., ['MB', 'RMSE'])
            round_factor (int): Number of decimals to round to

        Returns:
            dict: Dictionary of selected metric abbreviation and value
        """
    
        abbr_map = self.print_abbreviations()
        reverse_abbr = {v: k for k, v in abbr_map.items()}

        full_method_map = {
            "Mean Bias": self.mean_bias(),
            "Root Mean Squared Error": self.root_mean_squared_error(),
            "Correlation Coefficient": self.correlation_coefficient(),
            "Normalized Mean Bias Factor": self.normed_mean_bias_factor()[0],
            "Normalized Mean Absolute Error Factor": self.normed_mean_bias_factor()[1],
            "Revised Normalized Mean Bias Factor": self.revised_nmbf()[0],
            "Revised Normalized Mean Absolute Error Factor": self.revised_nmbf()[1],
            "Fractional Bias": self.fractional_absolute_error(),
            "Fractional Absolute Error": self.fractional_bias(),
            "Figure of Merit": self.figure_of_merit(),
            "Factor of Observations 2": self.factor_of_observations2(),
            "Mean Bias Difference": self.mean_bias_difference(),
            "Root Mean Square Difference": self.root_mean_square_difference(),
            "Mean Absolute Difference": self.mean_absolute_difference(),
            "Standard Deviation of the Residual": self.standard_deviation_of_residual(),
            "Coefficient of Determination": self.coefficient_of_determination(),
            "Slope of Best-Fit Line": self.slope_of_best_fit_line(),
            "Uncertainty at 95%": self.uncertainty_95(),
            "t-Statistic": self.t_statistic(),
            "Nash-Sutcliffe Efficiency": self.nash_sutcliffe_efficiency(),
            "Kling-Gupta Efficiency": self.kling_gupta_efficiency()[0],
            "Kling-Gupta Efficiency_R" : self.kling_gupta_efficiency()[1],
            "Kling-Gupta Efficiency_Var" : self.kling_gupta_efficiency()[2],
            "Kling-Gupta Efficiency_Mean" : self.kling_gupta_efficiency()[3],
            "Willmott's Index of Agreement": self.willmotts_index_of_agreement(),
            "Non Parametric KGE" : self.rnp()[0],
            "Legates's Coefficient of Efficiency": self.legates_coefficient_of_efficiency(),
            "Observation Mean": self.meann()[0],
            "Prediction Mean": self.meann()[1],
            "Observation Median": self.mediann()[0],
            "Prediction Median": self.mediann()[1],
            "Observation IQR": self.IQR()[0],
            "Prediction IQR": self.IQR()[1],
            "Observation STD": self.IQR()[0],
            "Prediction STD": self.IQR()[1],
            "KSI": self.ksi(),
            "OVER": self.over_metric(),
            "CPI": self.combined_performance_index(),
            "Relative Euclidean Distance": self.relative_euclidean_distance(),
            "NMSE": self.normalized_mean_square_error(),
            'CRMSE': self.centered_root_mean_square(),
            'Spearman R': self.spearmanR(),
            'LinRho': self.lins_concordance_correlation_coefficient(),
            'Mean Square Deviation': self.msd(),
            'Systematic Bias': self.sb(),
            'Non-uniformity': self.nu(),
            'Lack of Correlation': self.lc(),
            'N' : self.N,
            "Explained Variance": self.explained_variance(),
            "Taylor Skill Score": self.taylor_skill_score(),
            "Skill Score vs Climatology": self.skill_score_against_climatology(),
            "Anderson-Darling Distance": self.anderson_darling_distance(),
            "Kullback-Leibler Divergence": self.kullback_leibler_divergence(),
             "Mean Percentage Error": self.mean_percentage_error(),
            "Mean Absolute Percentage Error": self.mean_absolute_percentage_error(),
            "Symmetric Mean Absolute Percentage Error": self.symmetric_mean_absolute_percentage_error(),
            "Continuous Ranked Probability Score": self.continuous_ranked_probability_score(),
                "Trend Accuracy": self.trend_accuracy()
        }

        results = {}
        for abbr in metric_names:
            full_name = reverse_abbr.get(abbr)
            func = full_method_map.get(full_name)
            if func is not None:
                results[abbr] = round(func, round_factor)
            else:
                results[abbr] = None  # or raise warning/log missing metric
        return results
        

    def print_abbreviations(self, verbose=False):
        
        metrics_abbreviations = {
            "Mean Bias": "MB",
            "Mean Absolute Error": "MAE",
            "Root Mean Squared Error": "RMSE",
            "Correlation Coefficient": "R",
            "Mean Normalized Bias": "MNB",
            "Mean Normalized Absolute Error": "MNAE",
            "Fractional Bias": "FB",
            "Fractional Absolute Error": "FAE",
            "Normalized Mean Bias Factor": "NMBF",
            "Normalized Mean Absolute Error Factor": "NMAEF",
            "Revised Normalized Mean Bias Factor": "RNMBF",
            "Revised Normalized Mean Absolute Error Factor": "RNMAEF",
            "Figure of Merit": "FoM",
            "Factor of Observations 2": "Fac2",
            "Mean Bias Difference": "MBD",
            "Root Mean Square Difference": "RMSD",
            "Mean Absolute Difference": "MAD",
            "Standard Deviation of the Residual": "SDR",
            "Coefficient of Determination": "R²",
            "Slope of Best-Fit Line": "SBF",
            "Uncertainty at 95%": "U95",
            "t-Statistic": "TS",
            "Nash-Sutcliffe Efficiency": "NSE",
            "Kling-Gupta Efficiency" : "KGE",
            "Kling-Gupta Efficiency_R" : "KGE_R",
            "Kling-Gupta Efficiency_Var" : "KGE_VAR",
            "Kling-Gupta Efficiency_Mean" : "KGE_MEAN",
            "Non Parametric KGE" : "RNP",
            "Willmott's Index of Agreement": "WIA",
            "Legates's Coefficient of Efficiency": "LCE",
            "Observation Mean": "ObsMean",
            "Prediction Mean": "PredMean",
            "Observation Median": "ObsMedian",
            "Prediction Median": "PredMedian",
            "Observation IQR": "ObsIQR",
            "Prediction IQR": "PredIQR",
            "Observation STD": "ObsSTD",
            "Prediction STD": "PredSTD",
            "KSI": "KSI",
            "OVER": "OVER",
            "CPI": "CPI",
            "Relative Euclidean Distance": "RED",
            "NMSE": "NMSE",
            'CRMSE': 'CRMSE',
            'Spearman R': 'Rsp',
            "LinRho": 'LinRho',
             'Mean Square Deviation' : 'MSD',
            'Systematic Bias': 'SB',
            'Non-uniformity': 'NU',
            'Lack of Correlation': 'LC',
            'N' : 'N',
            "Explained Variance": "EV",
            "Taylor Skill Score": "TSS",
            "Skill Score vs Climatology": "SS",
            "Anderson-Darling Distance": "AD",
            "Kullback-Leibler Divergence": "KLD",
             "Mean Percentage Error": "MPE",
            "Mean Absolute Percentage Error": "MAPE",
            "Symmetric Mean Absolute Percentage Error": "sMAPE",
            "Continuous Ranked Probability Score": "CRPS",
             "Trend Accuracy": "TAcc"
        }

        if verbose:
            # Example usage
            for metric, abbreviation in metrics_abbreviations.items():
                print(f"{metric}: {abbreviation}")

        return metrics_abbreviations

    def all_metrics(self, round_factor=2):
        """Return all metrics as a dictionary."""
     
        all_metrics_dict = {
            "Mean Bias": self.mean_bias(),
            "Root Mean Squared Error": self.root_mean_squared_error(),
            "Correlation Coefficient": self.correlation_coefficient(),
            "Normalized Mean Bias Factor": self.normed_mean_bias_factor()[0],
            "Normalized Mean Absolute Error Factor": self.normed_mean_bias_factor()[1],
            "Revised Normalized Mean Bias Factor": self.revised_nmbf()[0],
            "Revised Normalized Mean Absolute Error Factor": self.revised_nmbf()[1],
            "Fractional Bias": self.fractional_absolute_error(),
            "Fractional Absolute Error": self.fractional_bias(),
            "Figure of Merit": self.figure_of_merit(),
            "Factor of Observations 2": self.factor_of_observations2(),
            "Mean Bias Difference": self.mean_bias_difference(),
            "Root Mean Square Difference": self.root_mean_square_difference(),
            "Mean Absolute Difference": self.mean_absolute_difference(),
            "Standard Deviation of the Residual": self.standard_deviation_of_residual(),
            "Coefficient of Determination": self.coefficient_of_determination(),
            "Slope of Best-Fit Line": self.slope_of_best_fit_line(),
            "Uncertainty at 95%": self.uncertainty_95(),
            "t-Statistic": self.t_statistic(),
            "Nash-Sutcliffe Efficiency": self.nash_sutcliffe_efficiency(),
            "Kling-Gupta Efficiency": self.kling_gupta_efficiency()[0],
            "Kling-Gupta Efficiency_R" : self.kling_gupta_efficiency()[1],
            "Kling-Gupta Efficiency_Var" : self.kling_gupta_efficiency()[2],
            "Kling-Gupta Efficiency_Mean" : self.kling_gupta_efficiency()[3],
            "Willmott's Index of Agreement": self.willmotts_index_of_agreement(),
            "Non Parametric KGE" : self.rnp(),
            "Legates's Coefficient of Efficiency": self.legates_coefficient_of_efficiency(),
            "Observation Mean": self.meann()[0],
            "Prediction Mean": self.meann()[1],
            "Observation Median": self.mediann()[0],
            "Prediction Median": self.mediann()[1],
            "Observation IQR": self.IQR()[0],
            "Prediction IQR": self.IQR()[1],
            "Observation STD": self.IQR()[0],
            "Prediction STD": self.IQR()[1],
            "KSI": self.ksi(),
            "OVER": self.over_metric(),
            "CPI": self.combined_performance_index(),
            "Relative Euclidean Distance": self.relative_euclidean_distance(),
            "NMSE": self.normalized_mean_square_error(),
            'CMRSE': self.centered_root_mean_square(),
            'Spearman R': self.spearmanR(),
            'LinRho': self.lins_concordance_correlation_coefficient(),
            'Mean Square Deviation': self.msd(),
            'Systematic Bias': self.sb(),
            'Non-uniformity': self.nu(),
            'Lack of Correlation': self.lc(),
            'N' : self.N,
            "Explained Variance": self.explained_variance(),
            "Taylor Skill Score": self.taylor_skill_score(),
            "Skill Score vs Climatology": self.skill_score_against_climatology(),
            "Anderson-Darling Distance": self.anderson_darling_distance(),
            "Kullback-Leibler Divergence": self.kullback_leibler_divergence(),
             "Mean Percentage Error": self.mean_percentage_error(),
            "Mean Absolute Percentage Error": self.mean_absolute_percentage_error(),
            "Symmetric Mean Absolute Percentage Error": self.symmetric_mean_absolute_percentage_error(),
            "Continuous Ranked Probability Score": self.continuous_ranked_probability_score(),
                "Trend Accuracy": self.trend_accuracy()
        }
        
        abbr = self.print_abbreviations()
        
        all_metrics_dict = {abbr.get(k, k): round(v, round_factor) for k, v in all_metrics_dict.items()}
        
        return all_metrics_dict
        

# # Example usage:
# predictions = [1, 2, 3, np.nan, 5]
# observations = [1, 2, 2.5, 4, np.nan]

# np.random.seed(316)
# noise = np.random.normal(size=256, loc = 0, scale=12)
# observations = np.arange(1,256+1,1)

# predictions = observations + noise

# metrics = ErrorMetrics(predictions, observations)
# #metrics.print_available_metrics()
# print(metrics.all_metrics(2))
# # # rint(metrics.get_metrics(['Mean Bias', 'Root Mean Squared Error', 'Figure of Merit', 'Mean Bias Difference'], 2))
