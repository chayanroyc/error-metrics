# Metric Behavior Audit

This report is generated from `audit/metrics.yaml`. Do not edit it by hand.

## Audit summary

- Total registered metrics: 89
- Completed: 10
- Pending: 79

## bias

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MB` | Mean Bias | `mean_bias` | complete |

## core error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MAE` | Mean Absolute Error | `mean_absolute_error` | complete |
| `MedAE` | Median Absolute Error | `median_absolute_error` | complete |
| `RMSE` | Root Mean Squared Error | `root_mean_squared_error` | complete |

## correlation and agreement

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `R` | Correlation Coefficient | `correlation_coefficient` | complete |
| `SpearmanR` | Spearman Rank Correlation | `spearman_r` | complete |
| `KendallTau` | Kendall Tau Correlation | `kendall_tau` | complete |
| `LCCC` | Lin's Concordance Correlation | `lccc` | complete |

## efficiency and environmental evaluation

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `EV` | Explained Variance | `ev` | complete |

## normalized and relative error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `NMSE` | Normalized Mean Square Error | `nmse` | complete |

## Pending audit

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `CRM` | Coefficient of Residual Mass | `coefficient_of_residual_mass` | pending |
| `RE` | Relative Error | `relative_error` | pending |
| `EC` | Efficiency Coefficient | `efficiency_coefficient` | pending |
| `MASE` | Mean Absolute Scaled Error | `mean_absolute_scaled_error` | pending |
| `MAAPE` | Mean Arctangent Absolute Percentage Error | `mean_arctangent_absolute_percentage_error` | pending |
| `A10` | A10 Index | `a10_index` | pending |
| `CI` | Confidence Index | `confidence_index` | pending |
| `ME` | Max Error | `max_error` | pending |
| `R2` | Coefficient of Determination | `coefficient_of_determination` | pending |
| `MNB` | Mean Normalized Bias | `mean_normalized_bias` | pending |
| `MNAE` | Mean Normalized Absolute Error | `mean_normalized_absolute_error` | pending |
| `FB` | Fractional Bias | `fb` | pending |
| `FAE` | Fractional Absolute Error | `fae` | pending |
| `MFB` | Mean Fractional Bias | `mean_fractional_bias` | pending |
| `MFE` | Mean Fractional Error | `mean_fractional_error` | pending |
| `MAGE` | Mean Absolute Gross Error | `mean_absolute_gross_error` | pending |
| `GMB` | Geometric Mean Bias | `geometric_mean_bias` | pending |
| `FAC2` | Factor of Observations 2 | `factor_of_observations2` | pending |
| `MBD` | Mean Bias Difference | `mean_bias_difference` | pending |
| `RMSD` | Root Mean Square Difference | `root_mean_square_difference` | pending |
| `MAD` | Mean Absolute Difference | `mean_absolute_difference` | pending |
| `SD` | Standard Deviation of Residual | `standard_deviation_of_residual` | pending |
| `SBF` | Slope of Best-Fit Line | `slope_of_best_fit_line` | pending |
| `U95` | Uncertainty at 95% | `uncertainty_95` | pending |
| `TS` | t-Statistic | `t_statistic` | pending |
| `NSE` | Nash-Sutcliffe Efficiency | `nash_sutcliffe_efficiency` | pending |
| `NNSE` | Normalized NSE | `normalized_nse` | pending |
| `RAE` | Relative Absolute Error | `relative_absolute_error` | pending |
| `VAF` | Variance Accounted For | `variance_accounted_for` | pending |
| `RSE` | Residual Standard Error | `residual_standard_error` | pending |
| `KGE` | Kling-Gupta Efficiency | `kling_gupta_efficiency` | pending |
| `KGE2012` | Modified Kling-Gupta Efficiency | `modified_kling_gupta_efficiency` | pending |
| `KGEdp` | Kling-Gupta Efficiency Double Prime | `kling_gupta_efficiency_double_prime` | pending |
| `DE` | Diagnostic Efficiency | `diagnostic_efficiency` | pending |
| `LME` | Liu Model Efficiency | `liu_model_efficiency` | pending |
| `LCEf` | Least-squares Combined Efficiency | `least_squares_combined_efficiency` | pending |
| `WIA` | Willmott's Index of Agreement | `willmotts_index_of_agreement` | pending |
| `WIAr` | Refined Index of Agreement | `refined_index_of_agreement` | pending |
| `LCE` | Legates Coefficient of Efficiency | `legates_coefficient_of_efficiency` | pending |
| `KSI` | Kolmogorov-Smirnov Test Integral | `ksi` | pending |
| `PHI` | Percentage of Histogram Intersection | `phi` | pending |
| `SUSE` | Scaled and Unscaled Shannon Entropy Difference | `suse` | pending |
| `OVER` | Over-estimation Metric | `over_metric` | pending |
| `IQR` | Interquartile Range | `IQR` | pending |
| `STD` | Standard Deviation | `STD` | pending |
| `nESkew` | Normalized Error Skewness | `normalized_error_skewness` | pending |
| `nEKurt` | Normalized Error Kurtosis | `normalized_error_kurtosis` | pending |
| `MBF` | Mean Bias Factor | `mean_bias_factor` | pending |
| `RMBF` | Relative Mean Bias Factor | `relative_mean_bias_factor` | pending |
| `NMBF` | Normalized Mean Bias Factor | `nmbf` | pending |
| `RNMBF` | Relative Normalized Mean Bias Factor | `rnmbf` | pending |
| `CPI` | Combined Performance Index | `cpi` | pending |
| `RED` | Relative Euclidean Distance | `red` | pending |
| `FoM` | Figure of Merit | `figure_of_merit` | pending |
| `MSDdec` | MSD Decomposition | `msd_decomposition` | pending |
| `SS` | Skill Score vs Climatology | `skill_score_against_climatology` | pending |
| `AD` | Anderson-Darling Distance | `anderson_darling_distance` | pending |
| `KLD` | Kullback-Leibler Divergence | `kullback_leibler_divergence` | pending |
| `MPE` | Mean Percentage Error | `mean_percentage_error` | pending |
| `MAPE` | Mean Absolute Percentage Error | `mean_absolute_percentage_error` | pending |
| `sMAPE` | Symmetric Mean Absolute Percentage Error | `symmetric_mean_absolute_percentage_error` | pending |
| `CRPS` | Continuous Ranked Probability Score | `continuous_ranked_probability_score` | pending |
| `TAcc` | Trend Accuracy | `trend_accuracy` | pending |
| `U2` | Theil's Inequality Coefficient | `theils_u2` | pending |
| `BM` | Berry-Mielke Index | `berry_mielke_score` | pending |
| `dCor` | Distance Correlation | `distance_correlation` | pending |
| `lambda` | Duveiller Agreement Coefficient | `duveiller_agreement_coefficient` | pending |
| `iqRMSE` | Inter-Quartile RMSE | `interquartile_rmse` | pending |
| `SMA` | SMA Regression Metrics | `sma_metrics` | pending |
| `RNP` | Non-parametric KGE | `rnp` | pending |
| `TSS` | Taylor Skill Score | `taylor_skill_score` | pending |
| `MEAN` | Mean Values | `meann` | pending |
| `MEDIAN` | Median Values | `mediann` | pending |
| `CRMSE` | Centered Root Mean Square | `centered_root_mean_square` | pending |
| `MSLE` | Mean Squared Logarithmic Error | `mean_squared_logarithmic_error` | pending |
| `NMAEp` | Normalized Mean Absolute p-Error | `nmaep` | pending |
| `NAE` | Normalized Absolute Error | `normalized_absolute_error` | pending |
| `Gini` | Gini Coefficient | `gini_coefficient` | pending |
| `PCD` | Prediction of Change in Direction | `prediction_of_change_in_direction` | pending |
