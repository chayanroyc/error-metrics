# Metric Behavior Audit

This report is generated from `audit/metrics.yaml`. Do not edit it by hand.

## Audit summary

- Total registered metrics: 89
- Completed: 89
- Pending: 0

### Metrics by category

| Category | Metrics | Findings |
| --- | ---: | ---: |
| bias | 10 | 13 |
| core error | 9 | 11 |
| correlation and agreement | 11 | 13 |
| diagnostic and decomposition | 2 | 2 |
| distribution and statistical comparison | 13 | 17 |
| efficiency and environmental evaluation | 18 | 24 |
| normalized and relative error | 19 | 30 |
| percentage error | 5 | 7 |
| trend and direction | 2 | 3 |

### Findings by type

Priority is synthesis triage, not a change to the reviewed finding.

| Finding type | Count | Review priority |
| --- | ---: | --- |
| `possible-defect` | 17 | High |
| `definition-variant` | 26 | Medium |
| `validation-gap` | 20 | Medium |
| `duplicate-or-overlap` | 8 | Low |
| `test-gap` | 3 | Low |
| `documentation-gap` | 27 | Low |
| `consistent` | 19 | Low |

## bias

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-mb"></a>`MB` | Mean Bias | `mean_bias` | complete |
| <a id="metric-fb"></a>`FB` | Fractional Bias | `fb` | complete |
| <a id="metric-mfb"></a>`MFB` | Mean Fractional Bias | `mean_fractional_bias` | complete |
| <a id="metric-gmb"></a>`GMB` | Geometric Mean Bias | `geometric_mean_bias` | complete |
| <a id="metric-mbd"></a>`MBD` | Mean Bias Difference | `mean_bias_difference` | complete |
| <a id="metric-ts"></a>`TS` | t-Statistic | `t_statistic` | complete |
| <a id="metric-mbf"></a>`MBF` | Mean Bias Factor | `mean_bias_factor` | complete |
| <a id="metric-rmbf"></a>`RMBF` | Relative Mean Bias Factor | `relative_mean_bias_factor` | complete |
| <a id="metric-nmbf"></a>`NMBF` | Normalized Mean Bias Factor | `nmbf` | complete |
| <a id="metric-rnmbf"></a>`RNMBF` | Relative Normalized Mean Bias Factor | `rnmbf` | complete |

## core error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-mae"></a>`MAE` | Mean Absolute Error | `mean_absolute_error` | complete |
| <a id="metric-medae"></a>`MedAE` | Median Absolute Error | `median_absolute_error` | complete |
| <a id="metric-rmse"></a>`RMSE` | Root Mean Squared Error | `root_mean_squared_error` | complete |
| <a id="metric-me"></a>`ME` | Max Error | `max_error` | complete |
| <a id="metric-rmsd"></a>`RMSD` | Root Mean Square Difference | `root_mean_square_difference` | complete |
| <a id="metric-rse"></a>`RSE` | Residual Standard Error | `residual_standard_error` | complete |
| <a id="metric-crps"></a>`CRPS` | Continuous Ranked Probability Score | `continuous_ranked_probability_score` | complete |
| <a id="metric-crmse"></a>`CRMSE` | Centered Root Mean Square | `centered_root_mean_square` | complete |
| <a id="metric-msle"></a>`MSLE` | Mean Squared Logarithmic Error | `mean_squared_logarithmic_error` | complete |

## correlation and agreement

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-r"></a>`R` | Correlation Coefficient | `correlation_coefficient` | complete |
| <a id="metric-spearmanr"></a>`SpearmanR` | Spearman Rank Correlation | `spearman_r` | complete |
| <a id="metric-kendalltau"></a>`KendallTau` | Kendall Tau Correlation | `kendall_tau` | complete |
| <a id="metric-lccc"></a>`LCCC` | Lin's Concordance Correlation | `lccc` | complete |
| <a id="metric-ci"></a>`CI` | Confidence Index | `confidence_index` | complete |
| <a id="metric-sbf"></a>`SBF` | Slope of Best-Fit Line | `slope_of_best_fit_line` | complete |
| <a id="metric-bm"></a>`BM` | Berry-Mielke Index | `berry_mielke_score` | complete |
| <a id="metric-dcor"></a>`dCor` | Distance Correlation | `distance_correlation` | complete |
| <a id="metric-lambda"></a>`lambda` | Duveiller Agreement Coefficient | `duveiller_agreement_coefficient` | complete |
| <a id="metric-tss"></a>`TSS` | Taylor Skill Score | `taylor_skill_score` | complete |
| <a id="metric-gini"></a>`Gini` | Gini Coefficient | `gini_coefficient` | complete |

## efficiency and environmental evaluation

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-ev"></a>`EV` | Explained Variance | `ev` | complete |
| <a id="metric-ec"></a>`EC` | Efficiency Coefficient | `efficiency_coefficient` | complete |
| <a id="metric-r2"></a>`R2` | Coefficient of Determination | `coefficient_of_determination` | complete |
| <a id="metric-nse"></a>`NSE` | Nash-Sutcliffe Efficiency | `nash_sutcliffe_efficiency` | complete |
| <a id="metric-nnse"></a>`NNSE` | Normalized NSE | `normalized_nse` | complete |
| <a id="metric-vaf"></a>`VAF` | Variance Accounted For | `variance_accounted_for` | complete |
| <a id="metric-kge"></a>`KGE` | Kling-Gupta Efficiency | `kling_gupta_efficiency` | complete |
| <a id="metric-kge2012"></a>`KGE2012` | Modified Kling-Gupta Efficiency | `modified_kling_gupta_efficiency` | complete |
| <a id="metric-kgedp"></a>`KGEdp` | Kling-Gupta Efficiency Double Prime | `kling_gupta_efficiency_double_prime` | complete |
| <a id="metric-de"></a>`DE` | Diagnostic Efficiency | `diagnostic_efficiency` | complete |
| <a id="metric-lme"></a>`LME` | Liu Model Efficiency | `liu_model_efficiency` | complete |
| <a id="metric-lcef"></a>`LCEf` | Least-squares Combined Efficiency | `least_squares_combined_efficiency` | complete |
| <a id="metric-wia"></a>`WIA` | Willmott's Index of Agreement | `willmotts_index_of_agreement` | complete |
| <a id="metric-wiar"></a>`WIAr` | Refined Index of Agreement | `refined_index_of_agreement` | complete |
| <a id="metric-lce"></a>`LCE` | Legates Coefficient of Efficiency | `legates_coefficient_of_efficiency` | complete |
| <a id="metric-cpi"></a>`CPI` | Combined Performance Index | `cpi` | complete |
| <a id="metric-ss"></a>`SS` | Skill Score vs Climatology | `skill_score_against_climatology` | complete |
| <a id="metric-rnp"></a>`RNP` | Non-parametric KGE | `rnp` | complete |

## normalized and relative error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-nmse"></a>`NMSE` | Normalized Mean Square Error | `nmse` | complete |
| <a id="metric-crm"></a>`CRM` | Coefficient of Residual Mass | `coefficient_of_residual_mass` | complete |
| <a id="metric-re"></a>`RE` | Relative Error | `relative_error` | complete |
| <a id="metric-mase"></a>`MASE` | Mean Absolute Scaled Error | `mean_absolute_scaled_error` | complete |
| <a id="metric-a10"></a>`A10` | A10 Index | `a10_index` | complete |
| <a id="metric-mnb"></a>`MNB` | Mean Normalized Bias | `mean_normalized_bias` | complete |
| <a id="metric-mnae"></a>`MNAE` | Mean Normalized Absolute Error | `mean_normalized_absolute_error` | complete |
| <a id="metric-fae"></a>`FAE` | Fractional Absolute Error | `fae` | complete |
| <a id="metric-mfe"></a>`MFE` | Mean Fractional Error | `mean_fractional_error` | complete |
| <a id="metric-mage"></a>`MAGE` | Mean Absolute Gross Error | `mean_absolute_gross_error` | complete |
| <a id="metric-mad"></a>`MAD` | Mean Absolute Difference | `mean_absolute_difference` | complete |
| <a id="metric-sd"></a>`SD` | Standard Deviation of Residual | `standard_deviation_of_residual` | complete |
| <a id="metric-u95"></a>`U95` | Uncertainty at 95% | `uncertainty_95` | complete |
| <a id="metric-rae"></a>`RAE` | Relative Absolute Error | `relative_absolute_error` | complete |
| <a id="metric-red"></a>`RED` | Relative Euclidean Distance | `red` | complete |
| <a id="metric-u2"></a>`U2` | Theil's Inequality Coefficient | `theils_u2` | complete |
| <a id="metric-iqrmse"></a>`iqRMSE` | Inter-Quartile RMSE | `interquartile_rmse` | complete |
| <a id="metric-nmaep"></a>`NMAEp` | Normalized Mean Absolute p-Error | `nmaep` | complete |
| <a id="metric-nae"></a>`NAE` | Normalized Absolute Error | `normalized_absolute_error` | complete |

## percentage error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-maape"></a>`MAAPE` | Mean Arctangent Absolute Percentage Error | `mean_arctangent_absolute_percentage_error` | complete |
| <a id="metric-fac2"></a>`FAC2` | Factor of Observations 2 | `factor_of_observations2` | complete |
| <a id="metric-mpe"></a>`MPE` | Mean Percentage Error | `mean_percentage_error` | complete |
| <a id="metric-mape"></a>`MAPE` | Mean Absolute Percentage Error | `mean_absolute_percentage_error` | complete |
| <a id="metric-smape"></a>`sMAPE` | Symmetric Mean Absolute Percentage Error | `symmetric_mean_absolute_percentage_error` | complete |

## distribution and statistical comparison

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-ksi"></a>`KSI` | Kolmogorov-Smirnov Test Integral | `ksi` | complete |
| <a id="metric-phi"></a>`PHI` | Percentage of Histogram Intersection | `phi` | complete |
| <a id="metric-suse"></a>`SUSE` | Scaled and Unscaled Shannon Entropy Difference | `suse` | complete |
| <a id="metric-over"></a>`OVER` | Over-estimation Metric | `over_metric` | complete |
| <a id="metric-iqr"></a>`IQR` | Interquartile Range | `IQR` | complete |
| <a id="metric-std"></a>`STD` | Standard Deviation | `STD` | complete |
| <a id="metric-neskew"></a>`nESkew` | Normalized Error Skewness | `normalized_error_skewness` | complete |
| <a id="metric-nekurt"></a>`nEKurt` | Normalized Error Kurtosis | `normalized_error_kurtosis` | complete |
| <a id="metric-fom"></a>`FoM` | Figure of Merit | `figure_of_merit` | complete |
| <a id="metric-ad"></a>`AD` | Anderson-Darling Distance | `anderson_darling_distance` | complete |
| <a id="metric-kld"></a>`KLD` | Kullback-Leibler Divergence | `kullback_leibler_divergence` | complete |
| <a id="metric-mean"></a>`MEAN` | Mean Values | `meann` | complete |
| <a id="metric-median"></a>`MEDIAN` | Median Values | `mediann` | complete |

## diagnostic and decomposition

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-msddec"></a>`MSDdec` | MSD Decomposition | `msd_decomposition` | complete |
| <a id="metric-sma"></a>`SMA` | SMA Regression Metrics | `sma_metrics` | complete |

## trend and direction

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| <a id="metric-tacc"></a>`TAcc` | Trend Accuracy | `trend_accuracy` | complete |
| <a id="metric-pcd"></a>`PCD` | Prediction of Change in Direction | `prediction_of_change_in_direction` | complete |
