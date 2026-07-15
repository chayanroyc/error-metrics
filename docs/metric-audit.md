# Metric Behavior Audit

This report is generated from `audit/metrics.yaml`. Do not edit it by hand.

## Audit summary

- Total registered metrics: 89
- Completed: 70
- Pending: 19

## bias

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MB` | Mean Bias | `mean_bias` | complete |
| `FB` | Fractional Bias | `fb` | complete |
| `MFB` | Mean Fractional Bias | `mean_fractional_bias` | complete |
| `GMB` | Geometric Mean Bias | `geometric_mean_bias` | complete |
| `MBD` | Mean Bias Difference | `mean_bias_difference` | complete |
| `TS` | t-Statistic | `t_statistic` | complete |
| `MBF` | Mean Bias Factor | `mean_bias_factor` | complete |
| `RMBF` | Relative Mean Bias Factor | `relative_mean_bias_factor` | complete |
| `NMBF` | Normalized Mean Bias Factor | `nmbf` | complete |
| `RNMBF` | Relative Normalized Mean Bias Factor | `rnmbf` | complete |

## core error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MAE` | Mean Absolute Error | `mean_absolute_error` | complete |
| `MedAE` | Median Absolute Error | `median_absolute_error` | complete |
| `RMSE` | Root Mean Squared Error | `root_mean_squared_error` | complete |
| `ME` | Max Error | `max_error` | complete |
| `RMSD` | Root Mean Square Difference | `root_mean_square_difference` | complete |
| `RSE` | Residual Standard Error | `residual_standard_error` | complete |

## correlation and agreement

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `R` | Correlation Coefficient | `correlation_coefficient` | complete |
| `SpearmanR` | Spearman Rank Correlation | `spearman_r` | complete |
| `KendallTau` | Kendall Tau Correlation | `kendall_tau` | complete |
| `LCCC` | Lin's Concordance Correlation | `lccc` | complete |
| `CI` | Confidence Index | `confidence_index` | complete |
| `SBF` | Slope of Best-Fit Line | `slope_of_best_fit_line` | complete |

## efficiency and environmental evaluation

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `EV` | Explained Variance | `ev` | complete |
| `EC` | Efficiency Coefficient | `efficiency_coefficient` | complete |
| `R2` | Coefficient of Determination | `coefficient_of_determination` | complete |
| `NSE` | Nash-Sutcliffe Efficiency | `nash_sutcliffe_efficiency` | complete |
| `NNSE` | Normalized NSE | `normalized_nse` | complete |
| `VAF` | Variance Accounted For | `variance_accounted_for` | complete |
| `KGE` | Kling-Gupta Efficiency | `kling_gupta_efficiency` | complete |
| `KGE2012` | Modified Kling-Gupta Efficiency | `modified_kling_gupta_efficiency` | complete |
| `KGEdp` | Kling-Gupta Efficiency Double Prime | `kling_gupta_efficiency_double_prime` | complete |
| `DE` | Diagnostic Efficiency | `diagnostic_efficiency` | complete |
| `LME` | Liu Model Efficiency | `liu_model_efficiency` | complete |
| `LCEf` | Least-squares Combined Efficiency | `least_squares_combined_efficiency` | complete |
| `WIA` | Willmott's Index of Agreement | `willmotts_index_of_agreement` | complete |
| `WIAr` | Refined Index of Agreement | `refined_index_of_agreement` | complete |
| `LCE` | Legates Coefficient of Efficiency | `legates_coefficient_of_efficiency` | complete |
| `CPI` | Combined Performance Index | `cpi` | complete |
| `SS` | Skill Score vs Climatology | `skill_score_against_climatology` | complete |

## normalized and relative error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `NMSE` | Normalized Mean Square Error | `nmse` | complete |
| `CRM` | Coefficient of Residual Mass | `coefficient_of_residual_mass` | complete |
| `RE` | Relative Error | `relative_error` | complete |
| `MASE` | Mean Absolute Scaled Error | `mean_absolute_scaled_error` | complete |
| `A10` | A10 Index | `a10_index` | complete |
| `MNB` | Mean Normalized Bias | `mean_normalized_bias` | complete |
| `MNAE` | Mean Normalized Absolute Error | `mean_normalized_absolute_error` | complete |
| `FAE` | Fractional Absolute Error | `fae` | complete |
| `MFE` | Mean Fractional Error | `mean_fractional_error` | complete |
| `MAGE` | Mean Absolute Gross Error | `mean_absolute_gross_error` | complete |
| `MAD` | Mean Absolute Difference | `mean_absolute_difference` | complete |
| `SD` | Standard Deviation of Residual | `standard_deviation_of_residual` | complete |
| `U95` | Uncertainty at 95% | `uncertainty_95` | complete |
| `RAE` | Relative Absolute Error | `relative_absolute_error` | complete |
| `RED` | Relative Euclidean Distance | `red` | complete |

## percentage error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MAAPE` | Mean Arctangent Absolute Percentage Error | `mean_arctangent_absolute_percentage_error` | complete |
| `FAC2` | Factor of Observations 2 | `factor_of_observations2` | complete |
| `MPE` | Mean Percentage Error | `mean_percentage_error` | complete |
| `MAPE` | Mean Absolute Percentage Error | `mean_absolute_percentage_error` | complete |

## distribution and statistical comparison

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `KSI` | Kolmogorov-Smirnov Test Integral | `ksi` | complete |
| `PHI` | Percentage of Histogram Intersection | `phi` | complete |
| `SUSE` | Scaled and Unscaled Shannon Entropy Difference | `suse` | complete |
| `OVER` | Over-estimation Metric | `over_metric` | complete |
| `IQR` | Interquartile Range | `IQR` | complete |
| `STD` | Standard Deviation | `STD` | complete |
| `nESkew` | Normalized Error Skewness | `normalized_error_skewness` | complete |
| `nEKurt` | Normalized Error Kurtosis | `normalized_error_kurtosis` | complete |
| `FoM` | Figure of Merit | `figure_of_merit` | complete |
| `AD` | Anderson-Darling Distance | `anderson_darling_distance` | complete |
| `KLD` | Kullback-Leibler Divergence | `kullback_leibler_divergence` | complete |

## diagnostic and decomposition

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| `MSDdec` | MSD Decomposition | `msd_decomposition` | complete |

## Pending audit

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
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
