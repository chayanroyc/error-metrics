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
| percentage error | 5 | 6 |
| trend and direction | 2 | 3 |

### Findings by type

Priority is synthesis triage, not a change to the reviewed finding.

| Finding type | Count | Review priority |
| --- | ---: | --- |
| `possible-defect` | 16 | High |
| `definition-variant` | 25 | Medium |
| `validation-gap` | 20 | Medium |
| `duplicate-or-overlap` | 8 | Low |
| `test-gap` | 3 | Low |
| `documentation-gap` | 27 | Low |
| `consistent` | 20 | Low |

## bias

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`MB`](#metric-mb) | Mean Bias | `mean_bias` | complete |
| [`FB`](#metric-fb) | Fractional Bias | `fb` | complete |
| [`MFB`](#metric-mfb) | Mean Fractional Bias | `mean_fractional_bias` | complete |
| [`GMB`](#metric-gmb) | Geometric Mean Bias | `geometric_mean_bias` | complete |
| [`MBD`](#metric-mbd) | Mean Bias Difference | `mean_bias_difference` | complete |
| [`TS`](#metric-ts) | t-Statistic | `t_statistic` | complete |
| [`MBF`](#metric-mbf) | Mean Bias Factor | `mean_bias_factor` | complete |
| [`RMBF`](#metric-rmbf) | Relative Mean Bias Factor | `relative_mean_bias_factor` | complete |
| [`NMBF`](#metric-nmbf) | Normalized Mean Bias Factor | `nmbf` | complete |
| [`RNMBF`](#metric-rnmbf) | Relative Normalized Mean Bias Factor | `rnmbf` | complete |

## core error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`MAE`](#metric-mae) | Mean Absolute Error | `mean_absolute_error` | complete |
| [`MedAE`](#metric-medae) | Median Absolute Error | `median_absolute_error` | complete |
| [`RMSE`](#metric-rmse) | Root Mean Squared Error | `root_mean_squared_error` | complete |
| [`ME`](#metric-me) | Max Error | `max_error` | complete |
| [`RMSD`](#metric-rmsd) | Root Mean Square Difference | `root_mean_square_difference` | complete |
| [`RSE`](#metric-rse) | Residual Standard Error | `residual_standard_error` | complete |
| [`CRPS`](#metric-crps) | Continuous Ranked Probability Score | `continuous_ranked_probability_score` | complete |
| [`CRMSE`](#metric-crmse) | Centered Root Mean Square | `centered_root_mean_square` | complete |
| [`MSLE`](#metric-msle) | Mean Squared Logarithmic Error | `mean_squared_logarithmic_error` | complete |

## correlation and agreement

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`R`](#metric-r) | Correlation Coefficient | `correlation_coefficient` | complete |
| [`SpearmanR`](#metric-spearmanr) | Spearman Rank Correlation | `spearman_r` | complete |
| [`KendallTau`](#metric-kendalltau) | Kendall Tau Correlation | `kendall_tau` | complete |
| [`LCCC`](#metric-lccc) | Lin's Concordance Correlation | `lccc` | complete |
| [`CI`](#metric-ci) | Confidence Index | `confidence_index` | complete |
| [`SBF`](#metric-sbf) | Slope of Best-Fit Line | `slope_of_best_fit_line` | complete |
| [`BM`](#metric-bm) | Berry-Mielke Index | `berry_mielke_score` | complete |
| [`dCor`](#metric-dcor) | Distance Correlation | `distance_correlation` | complete |
| [`lambda`](#metric-lambda) | Duveiller Agreement Coefficient | `duveiller_agreement_coefficient` | complete |
| [`TSS`](#metric-tss) | Taylor Skill Score | `taylor_skill_score` | complete |
| [`Gini`](#metric-gini) | Gini Coefficient | `gini_coefficient` | complete |

## efficiency and environmental evaluation

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`EV`](#metric-ev) | Explained Variance | `ev` | complete |
| [`EC`](#metric-ec) | Efficiency Coefficient | `efficiency_coefficient` | complete |
| [`R2`](#metric-r2) | Coefficient of Determination | `coefficient_of_determination` | complete |
| [`NSE`](#metric-nse) | Nash-Sutcliffe Efficiency | `nash_sutcliffe_efficiency` | complete |
| [`NNSE`](#metric-nnse) | Normalized NSE | `normalized_nse` | complete |
| [`VAF`](#metric-vaf) | Variance Accounted For | `variance_accounted_for` | complete |
| [`KGE`](#metric-kge) | Kling-Gupta Efficiency | `kling_gupta_efficiency` | complete |
| [`KGE2012`](#metric-kge2012) | Modified Kling-Gupta Efficiency | `modified_kling_gupta_efficiency` | complete |
| [`KGEdp`](#metric-kgedp) | Kling-Gupta Efficiency Double Prime | `kling_gupta_efficiency_double_prime` | complete |
| [`DE`](#metric-de) | Diagnostic Efficiency | `diagnostic_efficiency` | complete |
| [`LME`](#metric-lme) | Liu Model Efficiency | `liu_model_efficiency` | complete |
| [`LCEf`](#metric-lcef) | Least-squares Combined Efficiency | `least_squares_combined_efficiency` | complete |
| [`WIA`](#metric-wia) | Willmott's Index of Agreement | `willmotts_index_of_agreement` | complete |
| [`WIAr`](#metric-wiar) | Refined Index of Agreement | `refined_index_of_agreement` | complete |
| [`LCE`](#metric-lce) | Legates Coefficient of Efficiency | `legates_coefficient_of_efficiency` | complete |
| [`CPI`](#metric-cpi) | Combined Performance Index | `cpi` | complete |
| [`SS`](#metric-ss) | Skill Score vs Climatology | `skill_score_against_climatology` | complete |
| [`RNP`](#metric-rnp) | Non-parametric KGE | `rnp` | complete |

## normalized and relative error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`NMSE`](#metric-nmse) | Normalized Mean Square Error | `nmse` | complete |
| [`CRM`](#metric-crm) | Coefficient of Residual Mass | `coefficient_of_residual_mass` | complete |
| [`RE`](#metric-re) | Relative Error | `relative_error` | complete |
| [`MASE`](#metric-mase) | Mean Absolute Scaled Error | `mean_absolute_scaled_error` | complete |
| [`A10`](#metric-a10) | A10 Index | `a10_index` | complete |
| [`MNB`](#metric-mnb) | Mean Normalized Bias | `mean_normalized_bias` | complete |
| [`MNAE`](#metric-mnae) | Mean Normalized Absolute Error | `mean_normalized_absolute_error` | complete |
| [`FAE`](#metric-fae) | Fractional Absolute Error | `fae` | complete |
| [`MFE`](#metric-mfe) | Mean Fractional Error | `mean_fractional_error` | complete |
| [`MAGE`](#metric-mage) | Mean Absolute Gross Error | `mean_absolute_gross_error` | complete |
| [`MAD`](#metric-mad) | Mean Absolute Difference | `mean_absolute_difference` | complete |
| [`SD`](#metric-sd) | Standard Deviation of Residual | `standard_deviation_of_residual` | complete |
| [`U95`](#metric-u95) | Uncertainty at 95% | `uncertainty_95` | complete |
| [`RAE`](#metric-rae) | Relative Absolute Error | `relative_absolute_error` | complete |
| [`RED`](#metric-red) | Relative Euclidean Distance | `red` | complete |
| [`U2`](#metric-u2) | Theil's Inequality Coefficient | `theils_u2` | complete |
| [`iqRMSE`](#metric-iqrmse) | Inter-Quartile RMSE | `interquartile_rmse` | complete |
| [`NMAEp`](#metric-nmaep) | Normalized Mean Absolute p-Error | `nmaep` | complete |
| [`NAE`](#metric-nae) | Normalized Absolute Error | `normalized_absolute_error` | complete |

## percentage error

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`MAAPE`](#metric-maape) | Mean Arctangent Absolute Percentage Error | `mean_arctangent_absolute_percentage_error` | complete |
| [`FAC2`](#metric-fac2) | Factor of Observations 2 | `factor_of_observations2` | complete |
| [`MPE`](#metric-mpe) | Mean Percentage Error | `mean_percentage_error` | complete |
| [`MAPE`](#metric-mape) | Mean Absolute Percentage Error | `mean_absolute_percentage_error` | complete |
| [`sMAPE`](#metric-smape) | Symmetric Mean Absolute Percentage Error | `symmetric_mean_absolute_percentage_error` | complete |

## distribution and statistical comparison

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`KSI`](#metric-ksi) | Kolmogorov-Smirnov Test Integral | `ksi` | complete |
| [`PHI`](#metric-phi) | Percentage of Histogram Intersection | `phi` | complete |
| [`SUSE`](#metric-suse) | Scaled and Unscaled Shannon Entropy Difference | `suse` | complete |
| [`OVER`](#metric-over) | Over-estimation Metric | `over_metric` | complete |
| [`IQR`](#metric-iqr) | Interquartile Range | `IQR` | complete |
| [`STD`](#metric-std) | Standard Deviation | `STD` | complete |
| [`nESkew`](#metric-neskew) | Normalized Error Skewness | `normalized_error_skewness` | complete |
| [`nEKurt`](#metric-nekurt) | Normalized Error Kurtosis | `normalized_error_kurtosis` | complete |
| [`FoM`](#metric-fom) | Figure of Merit | `figure_of_merit` | complete |
| [`AD`](#metric-ad) | Anderson-Darling Distance | `anderson_darling_distance` | complete |
| [`KLD`](#metric-kld) | Kullback-Leibler Divergence | `kullback_leibler_divergence` | complete |
| [`MEAN`](#metric-mean) | Mean Values | `meann` | complete |
| [`MEDIAN`](#metric-median) | Median Values | `mediann` | complete |

## diagnostic and decomposition

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`MSDdec`](#metric-msddec) | MSD Decomposition | `msd_decomposition` | complete |
| [`SMA`](#metric-sma) | SMA Regression Metrics | `sma_metrics` | complete |

## trend and direction

| Abbreviation | Name | Method | Status |
| --- | --- | --- | --- |
| [`TAcc`](#metric-tacc) | Trend Accuracy | `trend_accuracy` | complete |
| [`PCD`](#metric-pcd) | Prediction of Change in Direction | `prediction_of_change_in_direction` | complete |

## Detailed metric records

<a id="metric-mb"></a>
### `MB` — Mean Bias

- Registered method: `mean_bias`
- Category: bias
- Return shape: scalar
- Implemented range: (-infinity, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: mean(predictions) - mean(observations), equivalently mean(predictions - observations)
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - NumPy array conversion and finite-pair mask
  - Bottleneck nanmean when installed, otherwise NumPy nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before evaluation; remaining finite pairs determine the result.
- Zero inputs or denominators: No division occurs; all-zero paired inputs return 0.
- Negative inputs: Accepted; the signed result preserves the prediction-minus-observation direction.
- Constant series: Defined as the difference between the two constants.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: Mean signed prediction error, with the sign determined by the declared prediction-minus-observation convention.
- References:
  - [Reassessment of the Interagency Workgroup on Air Quality Modeling Phase 2 Summary Report](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1004TD4.TXT) — U.S. Environmental Protection Agency (2009), authoritative. Supports: Air-model evaluation uses prediction-minus-observation signed differences, supporting the implemented bias direction.
- Known variants:
  - Some fields define bias with observation minus prediction, reversing the sign.

#### Characterization and tests

- Ordinary case: For predictions [2, 4, 3] and observations [1, 2, 4], errors [1, 2, -1] have MB 2/3.
- Edge case: After dropping nonfinite pairs, [2, 4] versus [1, 2] returns MB 3/2; no finite pairs raise ValueError.
- Existing tests:
  - tests/test_error_metrics.py::test_zero_values
  - tests/test_error_metrics.py::test_negative_values
  - tests/test_error_metrics.py::test_metric_scale_dependence
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_foundational_errors_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_perfect_predictions_reach_implemented_ideal_values

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The method docstring says only 'Calculate mean bias' and does not state the subtraction direction.
  - Impact: Users can interpret the sign backwards because both conventions exist.
  - Recommended future action: Document the prediction-minus-observation convention without changing runtime behavior.

<a id="metric-mae"></a>
### `MAE` — Mean Absolute Error

- Registered method: `mean_absolute_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: mean(abs(predictions - observations))
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - NumPy absolute value
  - Bottleneck nanmean when installed, otherwise NumPy nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before evaluation.
- Zero inputs or denominators: No denominator; exact agreement, including zeros, returns 0.
- Negative inputs: Accepted because residual magnitudes are used.
- Constant series: Defined as the absolute difference between constants.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: The arithmetic mean of absolute paired residuals; a nonnegative loss minimized at zero.
- References:
  - [Metrics and scoring: Mean absolute error](https://scikit-learn.org/stable/modules/model_evaluation.html#mean-absolute-error) — scikit-learn maintainers (unknown), authoritative. Supports: Defines MAE as the mean absolute residual with best value zero.
- Known variants:
  - Weighted and multioutput reductions are common; this implementation is unweighted and scalar.

#### Characterization and tests

- Ordinary case: Errors [1, 2, -1] have absolute errors [1, 2, 1], so MAE is 4/3.
- Edge case: Exact agreement returns 0; retained finite pairs alone contribute after complete-case filtering.
- Existing tests:
  - tests/test_error_metrics.py::test_zero_values
  - tests/test_error_metrics.py::test_metric_properties
  - tests/test_error_metrics.py::test_median_absolute_error_outliers
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_foundational_errors_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_nonfinite_pairs_are_dropped_before_batch_1_metrics_are_computed

#### Findings and recommended future action

- `consistent`
  - Evidence: The implementation directly evaluates the canonical unweighted scalar formula.
  - Impact: Reported MAE has the expected original-unit interpretation.
  - Recommended future action: Retain the characterization baseline.

<a id="metric-medae"></a>
### `MedAE` — Median Absolute Error

- Registered method: `median_absolute_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: median(abs(predictions - observations))
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - NumPy absolute value
  - Bottleneck nanmedian when installed, otherwise NumPy nanmedian

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before evaluation.
- Zero inputs or denominators: No denominator; exact agreement returns 0.
- Negative inputs: Accepted because residual magnitudes are used.
- Constant series: Defined as the absolute difference between constants.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: The median of the absolute paired residuals; a nonnegative loss minimized at zero.
- References:
  - [median_absolute_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.median_absolute_error.html) — scikit-learn maintainers (unknown), authoritative. Supports: Defines median absolute error as the median absolute residual and identifies zero as optimal.
- Known variants:
  - For even sample counts, median implementations conventionally average the two middle ordered residual magnitudes.

#### Characterization and tests

- Ordinary case: Absolute errors [1, 2, 1] sort to [1, 1, 2], so MedAE is 1.
- Edge case: A single retained finite pair returns that pair's absolute residual; no retained pair raises ValueError.
- Existing tests:
  - tests/test_error_metrics.py::test_median_absolute_error
  - tests/test_error_metrics.py::test_median_absolute_error_perfect
  - tests/test_error_metrics.py::test_median_absolute_error_outliers
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_foundational_errors_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_perfect_predictions_reach_implemented_ideal_values

#### Findings and recommended future action

- `consistent`
  - Evidence: The implementation directly evaluates the canonical unweighted scalar formula.
  - Impact: Reported MedAE has the expected robust location-loss interpretation.
  - Recommended future action: Retain the characterization baseline.

<a id="metric-rmse"></a>
### `RMSE` — Root Mean Squared Error

- Registered method: `root_mean_squared_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity), with floating-point overflow possible
- Ideal value: 0

#### Implemented behavior

- Formula: sqrt(mean((predictions - observations)^2))
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - NumPy square root
  - Bottleneck nanmean when installed, otherwise NumPy nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs are removed; finite residuals large enough to overflow during squaring can produce infinity.
- Zero inputs or denominators: No denominator; exact agreement returns 0.
- Negative inputs: Accepted because residuals are squared.
- Constant series: Defined as the absolute difference between constants.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: The square root of the arithmetic mean of squared paired residuals; a nonnegative loss minimized at zero.
- References:
  - [root_mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html) — scikit-learn maintainers (unknown), authoritative. Supports: Defines RMSE as a nonnegative regression loss with best value zero.
- Known variants:
  - Weighted and multioutput reductions exist; this implementation is unweighted and scalar.

#### Characterization and tests

- Ordinary case: Squared errors [1, 4, 1] have mean 2, so RMSE is sqrt(2).
- Edge case: Exact agreement returns 0; finite-pair filtering occurs before residual squaring.
- Existing tests:
  - tests/test_error_metrics.py::test_zero_values
  - tests/test_error_metrics.py::test_metric_properties
  - tests/test_error_metrics.py::test_mae_rmse_relationship
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_foundational_errors_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_perfect_predictions_reach_implemented_ideal_values

#### Findings and recommended future action

- `consistent`
  - Evidence: The implementation directly evaluates the canonical unweighted scalar formula.
  - Impact: Reported RMSE has the expected original-unit, large-error-sensitive interpretation.
  - Recommended future action: Retain the characterization baseline.

<a id="metric-r"></a>
### `R` — Correlation Coefficient

- Registered method: `correlation_coefficient`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [-1, 1] for defined finite data; NaN when undefined
- Ideal value: 1 for perfect positive association

#### Implemented behavior

- Formula: numpy.corrcoef(predictions, observations)[0, 1] for at least two retained pairs; otherwise NaN
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - NumPy corrcoef
  - Python cached_property

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before correlation; one retained pair returns NaN.
- Zero inputs or denominators: Zero variance in either input makes the standardized covariance undefined and returns NaN.
- Negative inputs: Accepted; correlation depends on centered co-movement, not positivity.
- Constant series: Returns NaN when either retained series has zero variance.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: Pearson product-moment correlation is covariance divided by the product of standard deviations.
- References:
  - [numpy.corrcoef](https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html) — NumPy maintainers (unknown), authoritative. Supports: Defines the delegated correlation calculation and its covariance-standardization formula.
- Known variants:
  - Population and sample covariance divisors cancel in correlation when used consistently.

#### Characterization and tests

- Ordinary case: For centered covariance 1/3 and population variances 2/3 and 14/9, R is sqrt(3/28).
- Edge case: Equal nonzero constant series return NaN rather than 1 because both standard deviations are zero.
- Existing tests:
  - tests/test_error_metrics.py::test_correlation_metrics
  - tests/test_error_metrics.py::test_single_value_handling
  - tests/test_v2_robustness.py::test_pearson_calculation_is_cached
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_constant_series_characterizes_undefined_association_and_agreement

#### Findings and recommended future action

- `consistent`
  - Evidence: The method delegates the standard product-moment calculation to NumPy and explicitly handles fewer than two pairs.
  - Impact: Nondegenerate results have the expected linear-association interpretation.
  - Recommended future action: Document that constant series are undefined and retain the characterization baseline.

<a id="metric-spearmanr"></a>
### `SpearmanR` — Spearman Rank Correlation

- Registered method: `spearman_r`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [-1, 1] for defined finite data; NaN when undefined
- Ideal value: 1 for identical rank order

#### Implemented behavior

- Formula: scipy.stats.spearmanr(predictions, observations)[0] using SciPy default tie ranking
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - SciPy stats.spearmanr

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before SciPy evaluation; too few retained pairs return NaN.
- Zero inputs or denominators: Values of zero are ordinary ranks; zero rank variance is undefined.
- Negative inputs: Accepted and ranked with all other values.
- Constant series: SciPy returns NaN and emits ConstantInputWarning when an input is constant.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: A rank-based coefficient measuring monotonic association, reaching +1 or -1 for exact increasing or decreasing rank order.
- References:
  - [The Proof and Measurement of Association between Two Things](https://doi.org/10.2307/1412159) — Charles Spearman (1904), primary. Supports: Introduces rank-based measurement of association.
  - [scipy.stats.spearmanr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) — SciPy maintainers (unknown), authoritative. Supports: Defines the delegated coefficient, range, monotonic interpretation, tie handling dependency, and constant-input warning/NaN behavior.
- Known variants:
  - Tie-ranking and p-value algorithms vary; runtime follows the installed SciPy version.

#### Characterization and tests

- Ordinary case: Rank vectors [1, 3, 2] and [1, 2, 3] have SpearmanR 1 - 6(0^2+1^2+(-1)^2)/(3(3^2-1)) = 1/2.
- Edge case: Equal constant series return NaN and emit SciPy's constant-input warning.
- Existing tests:
  - tests/test_error_metrics.py::test_correlation_metrics
  - tests/test_error_metrics.py::test_metric_symmetry
  - tests/test_error_metrics.py::test_metric_scale_invariance
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_constant_series_characterizes_undefined_association_and_agreement

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The method docstring does not state that SciPy tie semantics are inherited or that constant input warns and returns NaN.
  - Impact: Users may expect a defined perfect score for identical constants or version-independent tie behavior.
  - Recommended future action: Document the delegated SciPy semantics without changing runtime behavior.

<a id="metric-kendalltau"></a>
### `KendallTau` — Kendall Tau Correlation

- Registered method: `kendall_tau`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [-1, 1] for defined finite data; NaN when undefined
- Ideal value: 1 for identical order

#### Implemented behavior

- Formula: scipy.stats.kendalltau(observations, predictions, nan_policy='omit') statistic using default variant='b'
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - SciPy stats.kendalltau

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Constructor filtering removes nonfinite pairs before SciPy's omit policy is applied.
- Zero inputs or denominators: Zero values are ordinary ranks; an all-tied denominator yields NaN.
- Negative inputs: Accepted and ordered with all other values.
- Constant series: Returns NaN when either series is entirely tied.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: Kendall rank association compares concordant and discordant pairs; tie-aware tau-b adjusts the denominator for ties.
- References:
  - [A New Measure of Rank Correlation](https://doi.org/10.1093/biomet/30.1-2.81) — M. G. Kendall (1938), primary. Supports: Introduces concordant/discordant-pair rank correlation.
  - [scipy.stats.kendalltau](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html) — SciPy maintainers (unknown), authoritative. Supports: Documents default tau-b, its tie-adjusted formula, and undefined constant-input behavior.
- Known variants:
  - Tau-a omits tie adjustments; tau-b is the implemented default and equals tau-a when there are no ties.
  - SciPy also supports tau-c for rectangular tables.

#### Characterization and tests

- Ordinary case: Among three untied pairs there are two concordant and one discordant pair, so tau is (2-1)/3 = 1/3.
- Edge case: For predictions [1, 1, 2] and observations [1, 2, 3], P=2, Q=0, T=1, U=0, so tau-b is 2/sqrt(6), not the no-ties 2/3; equal constant series return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_kendall_tau
  - tests/test_error_metrics.py::test_kendall_tau_perfect_correlations
  - tests/test_error_metrics.py::test_kendall_tau_partial_correlation
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_constant_series_characterizes_undefined_association_and_agreement
  - tests/audit/test_characterization_batch_1.py::test_kendall_tau_uses_tie_adjusted_tau_b

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime uses SciPy's default tau-b, while the method docstring displays the untied tau-a-style denominator 'total pairs'.
  - Impact: Results with ties do not follow the displayed formula even though tau-b is a standard variant.
  - Recommended future action: Update documentation to name tau-b and show or link its tie-adjusted denominator.

<a id="metric-lccc"></a>
### `LCCC` — Lin's Concordance Correlation

- Registered method: `lccc`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [-1, 1] for defined finite data; NaN when undefined
- Ideal value: 1

#### Implemented behavior

- Formula: 2 * R * population_std(predictions) * population_std(observations) / (var(predictions) + var(observations) + (mean(predictions) - mean(observations))^2)
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - Cached NumPy Pearson correlation
  - Bottleneck nanstd/nanmean when installed, otherwise NumPy

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before all moments are computed.
- Zero inputs or denominators: A zero final denominator returns NaN; a NaN Pearson numerator also propagates.
- Negative inputs: Accepted; concordance evaluates location, scale, and association rather than positivity.
- Constant series: Returns NaN when either series is constant because Pearson R is undefined, including equal constants.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: Lin's coefficient is 2 cov(prediction, observation) divided by the sum of their variances and squared mean difference, measuring agreement with the 45-degree identity line.
- References:
  - [A Concordance Correlation Coefficient to Evaluate Reproducibility](https://doi.org/10.2307/2532051) — Lawrence I-Kuei Lin (1989), primary. Supports: Introduces concordance correlation as agreement with the identity line and provides its covariance/location-scale form.
- Known variants:
  - Equivalent expressions use Pearson R times an accuracy factor or twice the covariance directly.

#### Characterization and tests

- Ordinary case: Twice the population covariance is 2/3 and the variance-plus-location denominator is 8/3, so LCCC is 1/4.
- Edge case: Identical [2, 2, 2] series return NaN rather than 1 because Pearson R is undefined.
- Existing tests:
  - tests/test_error_metrics.py::test_correlation_metrics
  - tests/test_error_metrics.py::test_metric_symmetry
  - tests/test_v2_robustness.py::test_pearson_calculation_is_cached
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_constant_series_characterizes_undefined_association_and_agreement

#### Findings and recommended future action

- `consistent`
  - Evidence: For nondegenerate data the Pearson-times-standard-deviations expression is algebraically Lin's coefficient.
  - Impact: The metric penalizes location and scale disagreement that Pearson correlation alone ignores.
  - Recommended future action: Retain the formula and document undefined constant-series behavior.

<a id="metric-ev"></a>
### `EV` — Explained Variance

- Registered method: `ev`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1] for nonconstant observations; NaN for constant observations
- Ideal value: 1 for zero residual variance

#### Implemented behavior

- Formula: 1 - population_var(predictions - observations) / population_var(observations)
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - Bottleneck nanvar when installed, otherwise NumPy nanvar
  - _safe_divide zero-denominator policy

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before variance calculation.
- Zero inputs or denominators: Zero observation variance makes the denominator zero. Perfect constant predictions and constant-offset predictions have zero residual variance (raw 0/0); varying imperfect predictions have positive residual variance (raw positive/0). The implementation returns NaN for all of these cases.
- Negative inputs: Accepted; only centered variances of observations and residuals enter.
- Constant series: Any constant observation series returns NaN under the package's zero-denominator policy.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: Regression explained variance is one minus residual variance divided by target variance; best value is one and constant offsets are not penalized for nonconstant targets.
- References:
  - [Metrics and scoring: Explained variance score](https://scikit-learn.org/stable/modules/model_evaluation.html#explained-variance-score) — scikit-learn maintainers (unknown), authoritative. Supports: Defines the variance-ratio score, best value, constant-offset property, and nonfinite constant-target raw cases.
- Known variants:
  - For constant targets the raw formula is NaN when residual variance is zero, including perfect and constant-offset predictions, and negative infinity when residual variance is positive; some APIs map these cases to finite convenience scores, while this package returns NaN for every zero target variance.

#### Characterization and tests

- Ordinary case: Residual and observation population variances are both 14/9, so EV is 1 - 1 = 0.
- Edge case: Perfect equal constants produce 0/0 and return NaN rather than the ordinary ideal value 1.
- Existing tests:
  - tests/test_v2_robustness.py::test_zero_denominator_metrics_return_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_constant_series_characterizes_undefined_association_and_agreement

#### Findings and recommended future action

- `definition-variant`
  - Evidence: The package's shared safe division maps all constant-target denominators to NaN. The raw formula is already NaN for zero residual variance (perfect or constant-offset predictions), but is negative infinity for positive residual variance; some APIs instead force finite scores.
  - Impact: The implementation collapses raw negative-infinity varying-prediction cases into NaN, while preserving NaN for raw 0/0 cases.
  - Recommended future action: Document the current NaN policy before considering any future behavior change.

<a id="metric-nmse"></a>
### `NMSE` — Normalized Mean Square Error

- Registered method: `nmse`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: Context-dependent: nonnegative for same-sign nonzero means, negative for opposite-sign means, NaN for a zero mean
- Ideal value: 0 for exact agreement when the product of means is nonzero

#### Implemented behavior

- Formula: mean((predictions - observations)^2) / (mean(predictions) * mean(observations))
- Preprocessing:
  - Convert both inputs to float arrays and require equal shapes.
  - Flatten inputs and drop every pair containing NaN or infinity.
  - Raise ValueError when no finite pair remains.
- Dependencies:
  - Bottleneck nanmean when installed, otherwise NumPy nanmean
  - _safe_divide zero-denominator policy

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before means and mean square error are computed.
- Zero inputs or denominators: A zero prediction or observation mean makes the product denominator zero and returns NaN, including exact zero-mean agreement.
- Negative inputs: Accepted; opposite-sign means produce a negative value despite the squared numerator.
- Constant series: Defined when both constants are nonzero; exact equal nonzero constants return 0, while a zero constant denominator returns NaN.
- No data after preprocessing: ErrorMetrics construction raises ValueError before evaluation.

#### Scientific basis

- Canonical or reference definition: In air-quality model evaluation, one established NMSE is paired mean squared error normalized by the product of predicted and observed means.
- References:
  - [On the use of the normalized mean square error in evaluating dispersion model performance](https://doi.org/10.1016/0960-1686(93)90410-Z) — A. A. Poli and M. C. Cirillo (1993), primary. Supports: Analyzes the implemented product-of-means NMSE and warns of counterintuitive behavior.
  - [Air quality model performance evaluation](https://doi.org/10.1007/s00703-003-0070-7) — J. C. Chang and S. R. Hanna (2004), primary. Supports: Reviews NMSE as an air-quality model-performance measure.
- Known variants:
  - NMSE is also normalized by target variance, target energy, range, or other scale factors in other fields.
  - The implemented variant has a nonnegative error interpretation only when the two means have a positive product.

#### Characterization and tests

- Ordinary case: MSE is 2 and mean(predictions)*mean(observations) is 3*(7/3)=7, so NMSE is 2/7.
- Edge case: Observations [-1, 1] have zero mean, so predictions [1, 3] produce NaN despite finite nonzero squared error.
- Existing tests:
  - tests/test_v2_robustness.py::test_zero_denominator_metrics_return_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_1.py::test_association_agreement_and_normalized_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_1.py::test_nmse_zero_mean_denominator_returns_nan
  - tests/audit/test_characterization_batch_1.py::test_perfect_predictions_reach_implemented_ideal_values

#### Findings and recommended future action

- `definition-variant`
  - Evidence: The generic name NMSE does not identify the implemented air-quality product-of-means normalization among several established normalizations.
  - Impact: Users can compare incompatible quantities under the same abbreviation.
  - Recommended future action: Document the exact denominator and application domain.
- `validation-gap`
  - Evidence: The implementation accepts opposite-sign means and returns a negative normalized squared error, while zero means silently return NaN.
  - Impact: Without a positive-mean domain, lower-is-better and nonnegative-error interpretations break down.
  - Recommended future action: Document the unrestricted behavior now; consider explicit domain validation only in a separately reviewed behavior change.

<a id="metric-crm"></a>
### `CRM` — Coefficient of Residual Mass

- Registered method: `coefficient_of_residual_mass`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: (sum(predictions) - sum(observations)) / sum(observations)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero observation sum returns NaN.
- Negative inputs: Accepted.
- Constant series: Defined for nonzero observation constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Conventional CRM is (sum observations - sum predictions) / sum observations.
- References:
  - [Statistical and graphical methods for evaluating solute transport models](https://doi.org/10.1016/0022-1694(91)90038-N) — Loague and Green (1991), primary. Supports: Defines conventional CRM and its sign.
- Known variants:
  - The implementation reverses the conventional numerator sign.

#### Characterization and tests

- Ordinary case: Sums 9 and 7 give implemented CRM 2/7.
- Edge case: All-zero observations return NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_zero_denominator_metrics_return_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_zero_observations_are_omitted_or_counted_as_documented_by_runtime

#### Findings and recommended future action

- `definition-variant`
  - Evidence: The numerator sign is opposite Loague and Green.
  - Impact: Bias direction is reversed.
  - Recommended future action: Document the sign or change it only in a versioned fix.

<a id="metric-re"></a>
### `RE` — Relative Error

- Registered method: `relative_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: mean(abs(error) / abs(observation)), omitting zero observations
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy where and absolute
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero-observation pairs are omitted; all-zero observations return NaN.
- Negative inputs: Accepted using absolute denominators.
- Constant series: Defined for nonzero constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Absolute relative error scales absolute residual by reference magnitude.
- References:
  - [mean_absolute_percentage_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html) — scikit-learn maintainers (unknown), authoritative. Supports: Documents mean absolute relative error and zero-reference sensitivity.
- Known variants:
  - Relative error may be pointwise rather than mean; zero policies vary.

#### Characterization and tests

- Ordinary case: Ratios [1, 1, 1/4] average to 3/4.
- Edge case: For observations [0, 1], the zero pair is omitted.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_zero_observations_are_omitted_or_counted_as_documented_by_runtime

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The scalar reduction and zero omission are not apparent from the name.
  - Impact: Shape and weighting can surprise callers.
  - Recommended future action: Document reduction and omission.

<a id="metric-ec"></a>
### `EC` — Efficiency Coefficient

- Registered method: `efficiency_coefficient`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1 - SSE / sum((observations - mean(observations))^2)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero target variance returns NaN.
- Negative inputs: Accepted.
- Constant series: Constant observations return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Nash-Sutcliffe efficiency compares SSE with observed deviations from their mean.
- References:
  - [River flow forecasting through conceptual models part I](https://doi.org/10.1016/0022-1694(70)90255-6) — Nash and Sutcliffe (1970), primary. Supports: Introduces the implemented efficiency formula.
- Known variants:
  - The same algebra is named NSE; R2 is identical here.

#### Characterization and tests

- Ordinary case: SSE 6 and target total 14/3 give -2/7.
- Edge case: Constant observations return NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_zero_denominator_metrics_return_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_constant_observations_make_scaled_and_efficiency_denominators_undefined
  - tests/audit/test_characterization_batch_2.py::test_r2_and_ec_do_not_fit_a_regression_and_match_each_other

#### Findings and recommended future action

- `duplicate-or-overlap`
  - Evidence: EC and R2 have identical formulas.
  - Impact: Two identities return the same number.
  - Recommended future action: Document the overlap.

<a id="metric-mase"></a>
### `MASE` — Mean Absolute Scaled Error

- Registered method: `mean_absolute_scaled_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: MAE / mean(abs(diff(observations))); m is ignored
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs, warning that spacing changed.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy diff
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `m` | `1` | any runtime object | None; the parameter is never inspected. | No value is rejected and every value is ignored. |

#### Edge cases

- NaN and infinity: Pairs are dropped and RuntimeWarning is emitted.
- Zero inputs or denominators: Constant observations give zero scale and NaN.
- Negative inputs: Accepted.
- Constant series: Returns NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: MASE scales forecast MAE by in-sample naive MAE, using seasonal lag m when applicable.
- References:
  - [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001) — Hyndman and Koehler (2006), primary. Supports: Introduces MASE and seasonal scaling.
- Known variants:
  - Runtime uses evaluation observations and always lag 1.

#### Characterization and tests

- Ordinary case: MAE 4/3 divided by scale 3/2 gives 8/9.
- Edge case: m=2, zero, or a string produces the default result.
- Existing tests:
  - tests/test_v2_robustness.py::test_time_ordered_metric_warns_after_pairs_are_dropped
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_mase_seasonality_parameter_is_accepted_but_ignored
  - tests/audit/test_characterization_batch_2.py::test_nonfinite_pairs_are_removed_and_mase_warns_about_broken_spacing

#### Findings and recommended future action

- `possible-defect`
  - Evidence: The public m parameter is ignored and unvalidated.
  - Impact: Seasonal requests silently use lag 1.
  - Recommended future action: Validate and implement m separately.
- `definition-variant`
  - Evidence: Scaling uses evaluation observations rather than a training series.
  - Impact: Results can differ from forecast MASE.
  - Recommended future action: Document the available-data variant.

<a id="metric-maape"></a>
### `MAAPE` — Mean Arctangent Absolute Percentage Error

- Registered method: `mean_arctangent_absolute_percentage_error`
- Category: percentage error
- Return shape: scalar
- Implemented range: [0, pi/2] radians
- Ideal value: 0

#### Implemented behavior

- Formula: mean(arctan(abs(error/observation)))
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy arctan
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: A zero observation with nonzero error contributes pi/2; a zero-zero pair contributes 0.
- Negative inputs: Accepted.
- Constant series: Defined for nonzero constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Published MAAPE is mean(arctan(abs(error/actual))), bounded by pi/2.
- References:
  - [A new metric of absolute percentage error for intermittent demand forecasts](https://doi.org/10.1016/j.ijforecast.2015.12.003) — Kim and Kim (2016), primary. Supports: Defines bounded MAAPE and zero-actual limits.
- Known variants:
  - None

#### Characterization and tests

- Ordinary case: (pi/4 + pi/4 + atan(1/4)) / 3
- Edge case: A zero observation with nonzero error contributes pi/2; a zero-zero pair contributes 0.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_maape_uses_canonical_zero_actual_contributions
  - tests/audit/test_characterization_batch_2.py::test_maape_is_bounded_for_large_errors

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime follows the MAAPE definition and zero-actual limits in Kim and Kim (2016).
  - Impact: The implementation is bounded and uses the published zero policy.
  - Recommended future action: Maintain the Kim and Kim (2016) behavior in future changes.

<a id="metric-a10"></a>
### `A10` — A10 Index

- Registered method: `a10_index`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, 1]
- Ideal value: 1

#### Implemented behavior

- Formula: mean(abs(error/observation) <= 0.1), with zero observations producing False
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy comparison
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero-reference pairs count as misses, including exact zero-zero.
- Negative inputs: Accepted using signed observation division before absolute value.
- Constant series: Exact nonzero constants return 1; zero constants return 0.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: unknown: no primary or authoritative source was established that uniquely defines an A10 index; the implemented rule is the fraction of pairs with absolute relative error at most 0.1.
- References:
  - [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) — NumPy maintainers (unknown), authoritative. Supports: Provides tolerance-comparison and near-zero context only; it does not define or validate a canonical A10 index.
- Known variants:
  - Symmetric denominators, absolute tolerance, and zero omission are alternatives.

#### Characterization and tests

- Ordinary case: Ratios [1,1,1/4] all exceed 0.1, giving 0.
- Edge case: Exact all-zero pairs return 0.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_zero_observations_are_omitted_or_counted_as_documented_by_runtime

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: No primary or authoritative source was established that uniquely owns the A10 name or definition.
  - Impact: The abbreviation cannot support a universal canonical interpretation.
  - Recommended future action: Document the exact implemented threshold rule and application domain; add a domain source only when provenance is established.
- `validation-gap`
  - Evidence: Undefined zero-reference ratios silently count as failures.
  - Impact: Exact zero predictions are penalized.
  - Recommended future action: Define and document a zero policy.

<a id="metric-ci"></a>
### `CI` — Confidence Index

- Registered method: `confidence_index`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [-1, 1] for finite component results; NaN when Pearson correlation is undefined; may raise ZeroDivisionError when the agreement denominator is zero
- Ideal value: 1

#### Implemented behavior

- Formula: Pearson R * Willmott index of agreement
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Cached NumPy Pearson correlation
  - willmotts_index_of_agreement

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Exact all-zero inputs raise ZeroDivisionError in WIA.
- Negative inputs: Accepted.
- Constant series: Pearson R is NaN; zero constants additionally raise.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Camargo-Sentelhas confidence index multiplies Pearson r by Willmott d.
- References:
  - [Performance evaluation of different methods of estimating potential evapotranspiration in the State of Sao Paulo, Brazil](https://www.agritempo.gov.br/publish/publicacoes/X/10.pdf) — Camargo and Sentelhas (1997), primary. Supports: Defines the composite confidence index.
- Known variants:
  - Interpretation bands are application-specific.

#### Characterization and tests

- Ordinary case: R=sqrt(3/28), d=28/55, so CI is their product.
- Edge case: Exact all-zero inputs raise ZeroDivisionError.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_zero_observations_are_omitted_or_counted_as_documented_by_runtime
  - tests/audit/test_characterization_batch_2.py::test_constant_observations_make_scaled_and_efficiency_denominators_undefined

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Delegated WIA divides by zero for all-zero agreement.
  - Impact: CI raises instead of returning a score.
  - Recommended future action: Address WIA separately.
- `documentation-gap`
  - Evidence: Categorical bands lack source context.
  - Impact: Contextual bands may be treated as universal.
  - Recommended future action: Cite and qualify the bands.

<a id="metric-me"></a>
### `ME` — Max Error

- Registered method: `max_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: max(abs(predictions - observations))
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy absolute
  - Bottleneck nanmax

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: No denominator; exact zero agreement returns 0.
- Negative inputs: Accepted.
- Constant series: Absolute difference between constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Maximum error is the largest absolute paired residual.
- References:
  - [max_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.max_error.html) — scikit-learn maintainers (unknown), authoritative. Supports: Defines scalar maximum absolute residual.
- Known variants:
  - Multioutput APIs may return per-output values; inputs here are flattened.

#### Characterization and tests

- Ordinary case: Residual magnitudes [1,2,1] give 2.
- Edge case: Exact zero agreement returns 0.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_perfect_varying_predictions_reach_implemented_ideals

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime is scalar maximum absolute residual.
  - Impact: Behavior matches the authoritative definition.
  - Recommended future action: Retain behavior and coverage.

<a id="metric-r2"></a>
### `R2` — Coefficient of Determination

- Registered method: `coefficient_of_determination`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1 - SSE / sum((observations - mean(observations))^2); no regression is fitted
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero target variance returns NaN.
- Negative inputs: Accepted.
- Constant series: Constant observations return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Prediction-score R2 compares supplied SSE with target total sum of squares.
- References:
  - [r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html) — scikit-learn maintainers (unknown), authoritative. Supports: Defines prediction-score R2, negative scores, and constant-target cases.
- Known variants:
  - Fitted OLS R-squared is related but distinct; constant-target policies vary.

#### Characterization and tests

- Ordinary case: SSE 6 and target total 14/3 give -2/7.
- Edge case: Predictions twice observations score -6 although a fitted line has R2=1.
- Existing tests:
  - tests/test_error_metrics.py::test_correlation_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_constant_observations_make_scaled_and_efficiency_denominators_undefined
  - tests/audit/test_characterization_batch_2.py::test_r2_and_ec_do_not_fit_a_regression_and_match_each_other

#### Findings and recommended future action

- `consistent`
  - Evidence: Prediction-score formula permits negative values and fits no line.
  - Impact: The generic name can imply regression fitting.
  - Recommended future action: Document that no fit occurs.
- `duplicate-or-overlap`
  - Evidence: R2 and EC are identical.
  - Impact: Two identities duplicate results.
  - Recommended future action: Document the overlap.

<a id="metric-mnb"></a>
### `MNB` — Mean Normalized Bias

- Registered method: `mean_normalized_bias`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: mean((prediction - observation) / observation), omitting zero observations
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy where
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero-observation pairs are omitted; all-zero observations return NaN.
- Negative inputs: Accepted.
- Constant series: Defined for nonzero constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: MNB averages pointwise prediction-minus-observation residuals normalized by observations, often as percent.
- References:
  - [Reassessment of the Interagency Workgroup on Air Quality Modeling Phase 2 Summary Report](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1004TD4.TXT) — U.S. EPA (2009), authoritative. Supports: Documents air-quality MNB definition and percent reporting.
- Known variants:
  - Runtime returns a fraction; aggregate NMB uses ratio of sums.

#### Characterization and tests

- Ordinary case: Ratios [1,1,-1/4] average to 7/12.
- Edge case: For observations [0,1], the zero pair is omitted.
- Existing tests:
  - tests/test_error_metrics.py::test_zero_values
- Characterization tests:
  - tests/audit/test_characterization_batch_2.py::test_batch_2_metrics_match_hand_calculations_and_return_scalars
  - tests/audit/test_characterization_batch_2.py::test_zero_observations_are_omitted_or_counted_as_documented_by_runtime

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime returns a fraction rather than percent units.
  - Impact: Values differ by factor 100 from percent reports.
  - Recommended future action: Document units.
- `validation-gap`
  - Evidence: Zero observations are silently omitted.
  - Impact: Effective sample size changes.
  - Recommended future action: Document omission.

<a id="metric-mnae"></a>
### `MNAE` — Mean Normalized Absolute Error

- Registered method: `mean_normalized_absolute_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN; nonnegative for positive observations
- Ideal value: 0

#### Implemented behavior

- Formula: mean(abs(prediction - observation) / observation), omitting zero observations
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy where
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero-observation pairs are omitted; all-zero observations return NaN.
- Negative inputs: Accepted; a negative observation contributes a negative term despite the absolute numerator.
- Constant series: Defined when the constant observation is nonzero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: unknown: no primary or authoritative source was identified that establishes a unique cross-disciplinary definition for the exact name Mean Normalized Absolute Error; the runtime expression is therefore recorded without treating nearby MAPE nomenclature as canonical.
- References:
  - [mean_absolute_percentage_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html) — scikit-learn maintainers (2026), authoritative. Supports: Provides only a nearby comparison: MAPE uses an absolute target denominator and relative output units; it does not establish a canonical MNAE definition.
- Known variants:
  - Normalization may use observations, an absolute mean, range, or ratio of sums.
  - Percent reporting multiplies a fractional result by 100.

#### Characterization and tests

- Ordinary case: For predictions [2,4,3] and observations [1,2,4], mean absolute normalized error is (1+1+1/4)/3 = 3/4.
- Edge case: A zero observation is omitted; a negative observation supplies a signed denominator.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_observation_normalized_metrics_omit_zeros_and_accept_negative_denominators

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: No primary or authoritative source was identified that uniquely defines the exact MNAE name.
  - Impact: The registry name alone does not establish the denominator or units.
  - Recommended future action: Document the runtime formula and cite a domain-specific definition if one is intended.
- `validation-gap`
  - Evidence: The method accepts negative observations, allowing an absolute-error score below zero.
  - Impact: The implemented range and interpretation differ outside the positive concentration domain.
  - Recommended future action: Document or validate the positive-observation domain.
- `duplicate-or-overlap`
  - Evidence: MNAE and MAGE execute the same expression.
  - Impact: Two registry names return identical values for every accepted input.
  - Recommended future action: Document the alias-like overlap.

<a id="metric-fb"></a>
### `FB` — Fractional Bias

- Registered method: `fb`
- Category: bias
- Return shape: scalar
- Implemented range: unbounded, including signed infinity or NaN, with unrestricted signed inputs; [-2, 2] for nonnegative inputs except all-(0,0) data return NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 2 * nanmean((prediction - observation) / (prediction + observation)); 0/0 pairs become NaN and are omitted, while nonzero cancellation divisions remain signed infinity
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite input pairs.
  - Raise ValueError if no finite input pair remains.
- Dependencies:
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed, but infinities created during metric division are retained by nanmean.
- Zero inputs or denominators: Only 0/0 pairs such as (0,0) become NaN and are omitted. A nonzero prediction equal to negative observation yields signed infinity, which remains in isolated or mixed means.
- Negative inputs: Accepted; signed cancellation denominators can produce positive or negative infinity.
- Constant series: Equal zero constants return NaN; nonzero prediction and observation constants that cancel return signed infinity; other constant pairs are defined.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Air-dispersion FB compares predicted and observed means as 2(mean observation - mean prediction)/(mean observation + mean prediction).
- References:
  - [Air quality model performance evaluation](https://doi.org/10.1007/s00703-003-0070-7) — Chang and Hanna (2004), primary. Supports: Defines ratio-of-means fractional bias with observation-minus-prediction sign.
- Known variants:
  - Pointwise mean fractional bias averages per-pair fractions.
  - Sign orientation can be reversed by swapping model and observation.

#### Characterization and tests

- Ordinary case: Pointwise terms [2/3,2/3,-2/7] average to 22/63.
- Edge case: A (0,0) term is omitted, but (1,-1) yields positive infinity and (-1,1) yields negative infinity; generated infinities remain in mixed means.
- Existing tests:
  - tests/test_v5_metrics.py::test_existing_fb_fae_and_new_registry_mappings_are_distinct
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_fractional_metrics_distinguish_zero_pair_and_negative_policies
  - tests/audit/test_characterization_batch_3.py::test_fb_and_fae_retain_nonzero_cancellation_infinities

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Signed inputs are accepted although the bounded interpretation assumes nonnegative concentrations.
  - Impact: Values can exceed [-2,2].
  - Recommended future action: Document or validate the nonnegative domain.
- `possible-defect`
  - Evidence: Runtime uses a prediction-minus-observation pointwise mean, while cited FB is an observation-minus-prediction ratio of means.
  - Impact: Both aggregation and sign differ from canonical FB.
  - Recommended future action: Confirm intended convention before changing runtime behavior.

<a id="metric-fae"></a>
### `FAE` — Fractional Absolute Error

- Registered method: `fae`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: unbounded, including infinity, and possibly negative or NaN with unrestricted signed inputs; [0, 2] for nonnegative inputs except all-(0,0) data return NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 2 * nanmean(abs(prediction - observation) / (prediction + observation)); 0/0 pairs become NaN and are omitted, while nonzero cancellation divisions remain positive infinity
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite input pairs.
  - Raise ValueError if no finite input pair remains.
- Dependencies:
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed, but infinities created during metric division are retained by nanmean.
- Zero inputs or denominators: Only 0/0 pairs such as (0,0) become NaN and are omitted. A nonzero prediction equal to negative observation yields positive infinity, which remains in isolated or mixed means.
- Negative inputs: Accepted; a negative pair sum can produce negative finite terms, while a nonzero cancellation produces positive infinity.
- Constant series: Equal zero constants return NaN; nonzero prediction and observation constants that cancel return positive infinity; other constant pairs are defined.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Fractional absolute/gross error averages twice the absolute paired difference divided by the pair sum for nonnegative concentrations.
- References:
  - [PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models](https://doi.org/10.1016/j.atmosenv.2005.09.087) — Boylan and Russell (2006), primary. Supports: Defines the pointwise mean fractional error expression and percentage reporting.
- Known variants:
  - The statistic is also abbreviated FE, MFE, or called fractional gross error.

#### Characterization and tests

- Ordinary case: Pointwise absolute terms [2/3,2/3,2/7] average to 34/63.
- Edge case: A (0,0) term is omitted, but either nonzero cancellation orientation yields positive infinity which remains in mixed means.
- Existing tests:
  - tests/test_v5_metrics.py::test_existing_fb_fae_and_new_registry_mappings_are_distinct
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_fractional_metrics_distinguish_zero_pair_and_negative_policies
  - tests/audit/test_characterization_batch_3.py::test_fb_and_fae_retain_nonzero_cancellation_infinities

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Negative inputs are accepted although nonnegativity is needed for the advertised bounded absolute-error interpretation.
  - Impact: FAE can be negative or exceed 2.
  - Recommended future action: Document or validate input domain.

<a id="metric-mfb"></a>
### `MFB` — Mean Fractional Bias

- Registered method: `mean_fractional_bias`
- Category: bias
- Return shape: scalar
- Implemented range: [-2, 2]
- Ideal value: 0

#### Implemented behavior

- Formula: mean(2 * (prediction - observation) / (prediction + observation)); a (0,0) pair contributes 0
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Reject any negative retained value.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy divide
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before validation.
- Zero inputs or denominators: The only permitted zero denominator is (0,0), which contributes zero and remains in the averaging count.
- Negative inputs: Any retained negative prediction or observation raises ValueError.
- Constant series: Defined for nonnegative constants, including all-zero pairs.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Mean fractional bias averages the symmetric paired fractional bias over nonnegative model-observation pairs.
- References:
  - [PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models](https://doi.org/10.1016/j.atmosenv.2005.09.087) — Boylan and Russell (2006), primary. Supports: Defines pointwise mean fractional bias and percentage performance thresholds.
- Known variants:
  - Some sources use FB for related ratio-of-means bias.
  - Percent form multiplies runtime fractions by 100.

#### Characterization and tests

- Ordinary case: Pointwise terms [2/3,2/3,-2/7] average to 22/63.
- Edge case: For [(0,0),(2,1)], terms [0,2/3] average to 1/3.
- Existing tests:
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_match_hand_calculation
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_handle_identical_zero_pair
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_reject_negatives_without_mutation
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_fractional_metrics_distinguish_zero_pair_and_negative_policies

#### Findings and recommended future action

- `definition-variant`
  - Evidence: A (0,0) pair contributes zero and remains in N, unlike legacy FB which omits it.
  - Impact: MFB and FB differ when zero pairs occur despite sharing the ordinary-data formula.
  - Recommended future action: Document zero-pair weighting and naming distinction.

<a id="metric-mfe"></a>
### `MFE` — Mean Fractional Error

- Registered method: `mean_fractional_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, 2]
- Ideal value: 0

#### Implemented behavior

- Formula: mean(2 * abs(prediction - observation) / (prediction + observation)); a (0,0) pair contributes 0
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Reject any negative retained value.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy divide
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before validation.
- Zero inputs or denominators: A (0,0) pair contributes zero and remains in the averaging count.
- Negative inputs: Any retained negative prediction or observation raises ValueError.
- Constant series: Defined for nonnegative constants, including all-zero pairs.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Mean fractional error averages twice the absolute paired difference divided by the pair sum for nonnegative data.
- References:
  - [PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models](https://doi.org/10.1016/j.atmosenv.2005.09.087) — Boylan and Russell (2006), primary. Supports: Defines pointwise mean fractional error and percentage performance thresholds.
- Known variants:
  - The same expression is often abbreviated FE or FAE.
  - Percent form multiplies runtime fractions by 100.

#### Characterization and tests

- Ordinary case: Pointwise terms [2/3,2/3,2/7] average to 34/63.
- Edge case: For [(0,0),(2,1)], terms [0,2/3] average to 1/3.
- Existing tests:
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_match_hand_calculation
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_handle_identical_zero_pair
  - tests/test_v5_metrics.py::test_mean_fractional_metrics_reject_negatives_without_mutation
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_fractional_metrics_distinguish_zero_pair_and_negative_policies

#### Findings and recommended future action

- `definition-variant`
  - Evidence: A (0,0) pair counts as zero, whereas FAE omits it.
  - Impact: MFE and FAE differ only for zero pairs or negative-domain validation.
  - Recommended future action: Document the distinction.

<a id="metric-mage"></a>
### `MAGE` — Mean Absolute Gross Error

- Registered method: `mean_absolute_gross_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN; nonnegative for positive observations
- Ideal value: 0

#### Implemented behavior

- Formula: mean(abs(prediction - observation) / observation), omitting zero observations
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy where
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero-observation pairs are omitted; all-zero observations return NaN.
- Negative inputs: Accepted; negative observations yield negative contributions.
- Constant series: Defined for nonzero observation constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: EPA's MAGE is the unnormalized mean absolute residual in the data units; normalized percentage gross error is separately named MANGE or MNGE.
- References:
  - [Meteorological Model Evaluation Protocol](https://www.epa.gov/sites/default/files/2020-10/documents/tesche_2002_evaluation_protocol.pdf) — U.S. EPA (2002), authoritative. Supports: Defines dimensional MAGE separately from mean absolute normalized gross error.
- Known variants:
  - Normalized gross-error metrics use an observation denominator and may report percent.

#### Characterization and tests

- Ordinary case: The three normalized absolute terms average to 3/4.
- Edge case: Zero observations are omitted and negative observations contribute negative terms.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_observation_normalized_metrics_omit_zeros_and_accept_negative_denominators

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Runtime divides each absolute residual by observation, while authoritative MAGE is unnormalized.
  - Impact: The method implements a fractional normalized metric rather than dimensional MAGE.
  - Recommended future action: Confirm the intended registry name and formula before changing behavior.
- `duplicate-or-overlap`
  - Evidence: Implementation is exactly identical to MNAE.
  - Impact: The two names cannot distinguish scientific conventions at runtime.
  - Recommended future action: Document the overlap.

<a id="metric-gmb"></a>
### `GMB` — Geometric Mean Bias

- Registered method: `geometric_mean_bias`
- Category: bias
- Return shape: scalar
- Implemented range: (0, infinity), or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: exp(mean(log(prediction / observation))) over strictly positive pairs
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Warn and replace every nonpositive pair with NaN.
  - Raise ValueError if no finite pair remains before metric-specific filtering.
- Dependencies:
  - NumPy log and exp
  - Bottleneck nanmean
  - warnings

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before evaluation.
- Zero inputs or denominators: Any pair containing zero is warned about and omitted; if no positive pair remains the result is NaN.
- Negative inputs: Any pair containing a negative value is warned about and omitted.
- Constant series: Positive constants are defined; exact positive agreement returns 1.
- No data after preprocessing: Construction raises ValueError; metric-specific removal of every pair instead returns NaN with warnings.

#### Scientific basis

- Canonical or reference definition: Geometric mean bias is the exponential of the mean log prediction-to-observation ratio and requires strictly positive included pairs.
- References:
  - [Atmospheric Dispersion in Nuclear Power Plant Siting and Emergency Planning](https://www-pub.iaea.org/MTCD/Publications/PDF/TE-1738_web.pdf) — International Atomic Energy Agency (2014), authoritative. Supports: Defines the geometric mean bias/log-ratio statistic and ideal agreement.
- Known variants:
  - Some air-dispersion sources use MG and reverse the ratio orientation.

#### Characterization and tests

- Ordinary case: Ratios [2,2,3/4] have product 3, so GMB is cube root of 3.
- Edge case: With ratios [2, invalid, invalid], the two nonpositive pairs are omitted and GMB is 2.
- Existing tests:
  - tests/test_error_metrics.py::test_geometric_mean_bias
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_gmb_omits_nonpositive_pairs_and_requires_one_positive_pair

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Nonpositive pairs are omitted after a warning instead of rejecting the input.
  - Impact: The statistic may describe only an undocumented subset.
  - Recommended future action: Document effective-sample behavior or require strictly positive inputs.

<a id="metric-fac2"></a>
### `FAC2` — Factor of Observations 2

- Registered method: `factor_of_observations2`
- Category: percentage error
- Return shape: scalar
- Implemented range: [0, 100]
- Ideal value: 100

#### Implemented behavior

- Formula: 100 * count(0.5 <= prediction / observation <= 2) / N
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy division
  - Bottleneck nansum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: A zero observation yields NaN or infinity and the pair counts as a failure, including (0,0).
- Negative inputs: Accepted; two negative values with a ratio in [0.5,2] count as success.
- Constant series: Defined, including constant-zero observations which produce failures.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: FAC2 is the fraction of predictions satisfying the inclusive factor-of-two ratio interval 0.5 through 2.
- References:
  - [Air quality model performance evaluation](https://doi.org/10.1007/s00703-003-0070-7) — Chang and Hanna (2004), primary. Supports: Discusses FAC2 as a robust air-quality model evaluation index.
  - [Atmospheric Dispersion in Nuclear Power Plant Siting and Emergency Planning](https://www-pub.iaea.org/MTCD/Publications/PDF/TE-1738_web.pdf) — International Atomic Energy Agency (2014), authoritative. Supports: States the inclusive factor-of-two condition and fractional ideal of 1.
- Known variants:
  - Canonical reporting may use fraction [0,1] rather than percent [0,100].

#### Characterization and tests

- Ordinary case: Ratios [2,2,3/4] all satisfy the inclusive interval, producing 100.
- Edge case: Ratios exactly 0.5 and 2 pass; 0.49 and 2.01 fail, producing 50.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_fac2_includes_boundaries_and_counts_zero_divisions_as_failures
  - tests/audit/test_characterization_batch_3.py::test_perfect_positive_predictions_reach_implemented_ideals

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime multiplies the conventional fraction by 100.
  - Impact: Values and ideal differ by factor 100.
  - Recommended future action: Document percentage units.
- `validation-gap`
  - Evidence: Zero-observation and negative pairs remain in N rather than enforcing a positive ratio domain.
  - Impact: Undefined ratios fail and negative pairs may pass.
  - Recommended future action: Document or validate the positive domain.

<a id="metric-mbd"></a>
### `MBD` — Mean Bias Difference

- Registered method: `mean_bias_difference`
- Category: bias
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 100 * mean(prediction - observation) / mean(observation)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: An exactly zero observation mean returns NaN.
- Negative inputs: Accepted; a negative observation mean reverses the normalized sign interpretation.
- Constant series: Defined for nonzero observation constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Dimensional MBD is the mean prediction-minus-observation difference; relative MBD divides by mean reference observation and is commonly expressed in percent.
- References:
  - [Validation of the SARAH-E Satellite-Based Surface Solar Radiation Estimates over India](https://doi.org/10.3390/rs10030392) — Muller et al. (2018), primary. Supports: Defines dimensional MBD and its percentage relative variant.
- Known variants:
  - Sign orientation may be observation minus prediction.
  - Unqualified MBD is dimensional rather than percent-normalized.

#### Characterization and tests

- Ordinary case: Mean residual 2/3 divided by observation mean 7/3 and multiplied by 100 gives 200/7.
- Edge case: An observation mean of zero returns NaN; a negative mean reverses the normalized sign.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_percent_normalized_differences_follow_signed_observation_mean

#### Findings and recommended future action

- `definition-variant`
  - Evidence: The implementation is percentage relative MBD despite the unqualified dimensional name.
  - Impact: Output units and scale differ from MBD by division by the observation mean and factor 100.
  - Recommended future action: Rename or document the normalization and units.

<a id="metric-rmsd"></a>
### `RMSD` — Root Mean Square Difference

- Registered method: `root_mean_square_difference`
- Category: core error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN; nonnegative for positive observation means
- Ideal value: 0

#### Implemented behavior

- Formula: 100 * sqrt(mean((prediction - observation)^2)) / mean(observation)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy sqrt
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: An exactly zero observation mean returns NaN.
- Negative inputs: Accepted; a negative observation mean makes the result negative.
- Constant series: Defined for nonzero observation constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Dimensional RMSD is the square root of mean squared paired differences; relative RMSD divides by mean reference observation and is often expressed in percent.
- References:
  - [Validation of the SARAH-E Satellite-Based Surface Solar Radiation Estimates over India](https://doi.org/10.3390/rs10030392) — Muller et al. (2018), primary. Supports: Defines dimensional RMSD and its percentage relative variant.
- Known variants:
  - Normalization may use an absolute mean or another scale.

#### Characterization and tests

- Ordinary case: RMSE sqrt(2) divided by observation mean 7/3 and multiplied by 100 gives 300 sqrt(2)/7.
- Edge case: A negative observation mean produces a negative RMSD; a zero mean returns NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_3.py::test_batch_3_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_3.py::test_percent_normalized_differences_follow_signed_observation_mean

#### Findings and recommended future action

- `definition-variant`
  - Evidence: The implementation returns percentage relative RMSD despite the unqualified dimensional name.
  - Impact: Scale and units differ from canonical RMSD.
  - Recommended future action: Rename or document the normalization.
- `validation-gap`
  - Evidence: The denominator is signed rather than absolute.
  - Impact: Negative-mean observations produce a negative error magnitude.
  - Recommended future action: Document or restrict the reference domain.

<a id="metric-mad"></a>
### `MAD` — Mean Absolute Difference

- Registered method: `mean_absolute_difference`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN; nonnegative for positive observation means
- Ideal value: 0

#### Implemented behavior

- Formula: 100 * mean(abs(prediction - observation)) / mean(observation)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: An exactly zero observation mean returns NaN.
- Negative inputs: Accepted; a negative observation mean makes the result negative.
- Constant series: Defined for a nonzero observation constant.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Mean absolute difference is the dimensional mean of absolute paired differences.
- References:
  - [Goodness of Fit Metrics](https://www.itl.nist.gov/div898/handbook/pri/section5/pri5992.htm) — NIST/SEMATECH (2012), authoritative. Supports: Defines average absolute residual in response-variable units.
- Known variants:
  - MAD can instead abbreviate median absolute deviation.
  - Relative variants divide by an observation scale and may report percent.

#### Characterization and tests

- Ordinary case: Mean absolute residual 4/3 divided by observation mean 7/3 and multiplied by 100 gives 400/7.
- Edge case: A negative observation mean produces a negative value; a zero mean returns NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_percent_residual_metrics_use_signed_observation_mean

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime adds signed-mean normalization and factor 100 to dimensional mean absolute difference.
  - Impact: Output units, scale, and range differ from the registered name.
  - Recommended future action: Document percentage-relative normalization or rename the metric.
- `validation-gap`
  - Evidence: The normalizer is the signed observation mean.
  - Impact: Negative means make an absolute error negative and zero means are undefined.
  - Recommended future action: Document or validate the intended positive-mean domain.

<a id="metric-sd"></a>
### `SD` — Standard Deviation of Residual

- Registered method: `standard_deviation_of_residual`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN; nonnegative for positive observation means
- Ideal value: 0

#### Implemented behavior

- Formula: 100 * sqrt(mean(residual^2) - mean(residual)^2) / mean(observation)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy sqrt
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: An exactly zero observation mean returns NaN.
- Negative inputs: Accepted; a negative observation mean reverses the sign.
- Constant series: Constant residuals have zero spread when the observation mean is nonzero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Population residual standard deviation is the square root of the mean squared centered residual; regression residual standard error instead uses residual degrees of freedom.
- References:
  - [numpy.std](https://numpy.org/doc/stable/reference/generated/numpy.std.html) — NumPy maintainers (2026), authoritative. Supports: Defines population standard deviation with divisor N when ddof is zero.
  - [Residual Standard Deviation](https://www.itl.nist.gov/div898/handbook/pri/section5/pri599.htm) — NIST/SEMATECH (2012), authoritative. Supports: Defines fitted-model residual standard deviation with degrees-of-freedom adjustment.
- Known variants:
  - Regression residual SD may be uncentered and degrees-of-freedom adjusted.

#### Characterization and tests

- Ordinary case: Residual population SD sqrt(14)/3 divided by 7/3 and multiplied by 100 gives 100 sqrt(14)/7.
- Edge case: Residuals [3,7] have population SD 2; division by observation mean -2 gives -100.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_percent_residual_metrics_use_signed_observation_mean

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime computes percent-normalized population residual spread without a degrees-of-freedom correction.
  - Impact: It differs from fitted-model residual standard deviation and is insensitive to constant bias.
  - Recommended future action: Document the population convention, normalization, and distinction from RSE.
- `validation-gap`
  - Evidence: The denominator is the signed observation mean.
  - Impact: Negative means reverse sign and zero means return NaN.
  - Recommended future action: Document or validate the positive-mean domain.

<a id="metric-sbf"></a>
### `SBF` — Slope of Best-Fit Line

- Registered method: `slope_of_best_fit_line`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: sum((prediction - mean(prediction)) * (observation - mean(observation))) / sum((observation - mean(observation))^2)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: Constant observations make the centered denominator zero and return NaN.
- Negative inputs: Accepted; negative association can produce a negative slope.
- Constant series: Constant observations return NaN; constant predictions with varying observations return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The OLS-with-intercept slope of predictions on observations is centered cross-product divided by centered observation sum of squares.
- References:
  - [Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) — NIST/SEMATECH (2012), authoritative. Supports: Derives least-squares line estimates by minimizing squared residuals.
- Known variants:
  - Axis orientation and whether an intercept is fitted vary.

#### Characterization and tests

- Ordinary case: Centered cross-product 1 divided by observation sum of squares 14/3 gives 3/14.
- Edge case: Constant observations make regression slope undefined and return NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_constant_observations_make_centered_denominators_undefined

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime matches the OLS-with-intercept slope with observations as x and predictions as y.
  - Impact: Ordinary slope values have the expected interpretation.
  - Recommended future action: Document axis orientation and constant-observation NaN.
- `documentation-gap`
  - Evidence: A slope of one does not establish agreement when the unreported fitted intercept is nonzero.
  - Impact: Users may overinterpret the ideal value.
  - Recommended future action: Document that slope assesses proportional response, not agreement alone.

<a id="metric-u95"></a>
### `U95` — Uncertainty at 95%

- Registered method: `uncertainty_95`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 1.96 * sqrt(SD^2 + RMSD^2), using this package's percentage-normalized SD and RMSD
- Preprocessing:
  - Use shared finite-pair preprocessing.
  - Call standard_deviation_of_residual and root_mean_square_difference.
- Dependencies:
  - SD
  - RMSD
  - NumPy sqrt

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed before component evaluation.
- Zero inputs or denominators: A zero observation mean makes both components and U95 NaN.
- Negative inputs: Accepted; squared signed components yield a nonnegative result when finite.
- Constant series: Defined for nonzero observation constants; exact agreement gives zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: A model-evaluation convention defines U95 as 1.96 times the square root of SD squared plus RMSE squared; it is a composite index, not a general calibrated confidence interval.
- References:
  - [Uncertainty analysis of empirical models](https://doi.org/10.1038/s41598-025-20304-2) — Scientific Reports authors (2025), primary. Supports: Uses U95 = 1.96 sqrt(SD^2 + RMSE^2) and describes 1.96 as the normal 95% factor.
- Known variants:
  - Components may be dimensional rather than percentage normalized.

#### Characterization and tests

- Ordinary case: Combining SD 100 sqrt(14)/7 and RMSD 300 sqrt(2)/7 gives 112 sqrt(2).
- Edge case: A negative observation mean makes signed components negative, but squaring produces finite nonnegative U95.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_uncertainty_and_t_statistic_follow_composed_percent_formulas

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime uses percentage-normalized components rather than dimensional SD and RMSE.
  - Impact: Output is a relative percent composite rather than data-unit uncertainty.
  - Recommended future action: Document component units and formula.
- `documentation-gap`
  - Evidence: The name does not state the assumptions required for 95% coverage.
  - Impact: Users may interpret the index as a calibrated interval.
  - Recommended future action: Describe U95 as a model-evaluation composite, not guaranteed coverage.

<a id="metric-ts"></a>
### `TS` — t-Statistic

- Registered method: `t_statistic`
- Category: bias
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0 conceptually; exact agreement returns NaN

#### Implemented behavior

- Formula: sqrt((N - 1) * MBD^2 / (RMSD^2 - MBD^2)), using package percentage MBD and RMSD
- Preprocessing:
  - Use shared finite-pair preprocessing.
  - Call mean_bias_difference and root_mean_square_difference.
- Dependencies:
  - MBD
  - RMSD
  - _safe_divide
  - NumPy sqrt

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed before component evaluation.
- Zero inputs or denominators: A zero observation mean, exact agreement, one pair, or zero residual variance returns NaN.
- Negative inputs: Accepted; common signed normalization cancels when finite.
- Constant series: Constant nonzero residuals make the variance denominator zero and return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: A specialized model-evaluation t statistic is sqrt((n-1) MBE^2 / (RMSE^2-MBE^2)).
- References:
  - [Statistical procedures for the evaluation of evapotranspiration computing models](https://doi.org/10.1016/0378-3774(95)01152-9) — Jacovides and Kontoyiannis (1995), primary. Supports: Proposes the MBE/RMSE t-statistic formula for model evaluation.
- Known variants:
  - Generic t-statistics use other estimators and standard errors.

#### Characterization and tests

- Ordinary case: With N=3, MBD^2=40000/49 and RMSD^2-MBD^2=140000/49, TS is 2/sqrt(7).
- Edge case: Exact agreement supplies 0/0 and returns NaN rather than conceptual ideal zero.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_perfect_varying_series_reach_implemented_ideals
  - tests/audit/test_characterization_batch_4.py::test_uncertainty_and_t_statistic_follow_composed_percent_formulas

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime algebra matches the cited specialized MBE/RMSE statistic when components are finite.
  - Impact: Ordinary values follow the published convention.
  - Recommended future action: Document the application-specific meaning and assumptions.
- `possible-defect`
  - Evidence: Exact agreement yields 0/0 and NaN despite a documented ideal of zero.
  - Impact: The best possible input does not return the stated ideal.
  - Recommended future action: Decide separately whether exact zero residuals should map to zero.

<a id="metric-nse"></a>
### `NSE` — Nash-Sutcliffe Efficiency

- Registered method: `nash_sutcliffe_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1 - sum((prediction - observation)^2) / sum((observation - mean(observation))^2)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: Constant observations make the efficiency denominator zero and return NaN.
- Negative inputs: Accepted without domain restriction.
- Constant series: Constant observations, including exact constant agreement, return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: NSE is one minus residual sum of squares divided by observed deviations from their mean.
- References:
  - [River flow forecasting through conceptual models part I](https://doi.org/10.1016/0022-1694(70)90255-6) — Nash and Sutcliffe (1970), primary. Supports: Introduces the efficiency based on squared model errors relative to observed variance.
- Known variants:
  - None

#### Characterization and tests

- Ordinary case: Residual sum of squares 6 divided by observed centered sum 14/3 gives NSE -2/7.
- Edge case: Constant observations make the reference denominator zero and return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
  - tests/test_error_metrics.py::test_metric_bounds
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_constant_observations_make_centered_denominators_undefined

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime matches the Nash-Sutcliffe squared-error efficiency formula.
  - Impact: Ordinary behavior and range are canonical.
  - Recommended future action: Document constant-observation NaN.

<a id="metric-nnse"></a>
### `NNSE` — Normalized NSE

- Registered method: `normalized_nse`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (0, 1], or NaN for canonical finite NSE inputs
- Ideal value: 1

#### Implemented behavior

- Formula: 1 / (2 - NSE)
- Preprocessing:
  - Use shared finite-pair preprocessing.
  - Call nash_sutcliffe_efficiency.
- Dependencies:
  - NSE
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed before NSE evaluation.
- Zero inputs or denominators: Undefined NSE from constant observations propagates NaN.
- Negative inputs: Accepted without domain restriction.
- Constant series: Constant observations return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: NNSE is the monotone transform 1/(2-NSE), mapping finite NSE at most one into (0,1].
- References:
  - [Hyper Resolution Modeling of Urban Flood Inundation](https://doi.org/10.25923/9t55-tn77) — Michael Smith, Nathan Patrick, Nels Frazier, Jongkwan Kim, Trey Flowers, and Fred Ogden; United States National Weather Service (2020), authoritative. Supports: NOAA Technical Report NWS 56, section 8.2 on report pages 13-14 (PDF pages 18-19), explicitly defines NNSE as 1/(2-NSE), states its 0-to-1 range, and maps NSE=0 to NNSE=0.5.
- Known variants:
  - Other normalizations of efficiency exist.

#### Characterization and tests

- Ordinary case: NSE -2/7 transforms to 1/(2+2/7)=7/16.
- Edge case: Undefined NSE on constant observations propagates NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_constant_observations_make_centered_denominators_undefined

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime exactly applies the published monotone NSE transform.
  - Impact: Finite canonical NSE values map to the stated normalized interval.
  - Recommended future action: Document that NSE zero maps to 0.5 and constant targets remain undefined.
- `documentation-gap`
  - Evidence: The docstring calls the transformation more objective without source support.
  - Impact: A mathematical remapping may be mistaken for an improved evidential criterion.
  - Recommended future action: Remove or substantiate the objectivity claim in a separately approved documentation change.

<a id="metric-rae"></a>
### `RAE` — Relative Absolute Error

- Registered method: `relative_absolute_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: sqrt(sum((prediction - observation)^2)) / sqrt(sum(observation^2))
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy sqrt
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: An all-zero observation vector makes the denominator zero and returns NaN.
- Negative inputs: Accepted; squares remove sign.
- Constant series: Defined for nonzero constant observations.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Conventional RAE is sum of absolute errors divided by sum of absolute deviations of observations from their mean.
- References:
  - [Relative Absolute Error](https://mlr3measures.mlr-org.com/reference/rae.html) — mlr3measures maintainers (2026), authoritative. Supports: Defines RAE relative to the mean-prediction absolute-error baseline.
- Known variants:
  - Relative L2 error uses Euclidean norms instead of absolute-error sums.

#### Characterization and tests

- Ordinary case: Euclidean error norm sqrt(6) divided by observation norm sqrt(21) gives sqrt(2/7).
- Edge case: An all-zero observation vector returns NaN regardless of nonzero errors.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_efficiency_and_relative_error_denominator_failures

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Runtime computes relative L2 error, not conventional relative absolute error against the observed-mean baseline.
  - Impact: Ranking, denominator failure, and numeric values differ from RAE.
  - Recommended future action: Confirm intended metric before any separately approved rename or formula change.
- `documentation-gap`
  - Evidence: The docstring says RMSE over root sum of squared observations, while the numerator is root sum of squares.
  - Impact: The stated formula differs by a factor involving sample size.
  - Recommended future action: Correct the formula description separately.

<a id="metric-vaf"></a>
### `VAF` — Variance Accounted For

- Registered method: `variance_accounted_for`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, infinity), or NaN
- Ideal value: 100

#### Implemented behavior

- Formula: 100 * sum((observation - mean(observation)) * (prediction - mean(prediction))) / sum((observation - mean(observation))^2)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nanmean and nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed.
- Zero inputs or denominators: Constant observations make the denominator zero and return NaN.
- Negative inputs: Accepted; negative fitted slopes produce negative values.
- Constant series: Constant observations return NaN; constant predictions with varying observations return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Variance accounted for is commonly 100 times one minus residual variance divided by observed variance.
- References:
  - [explained_variance_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html) — scikit-learn maintainers (2026), authoritative. Supports: Defines explained variance as 1 - Var(y_true-y_pred)/Var(y_true) and documents constant-target behavior.
- Known variants:
  - Some fields use related R-squared or squared-correlation definitions.

#### Characterization and tests

- Ordinary case: Centered cross-product 1 divided by observed centered sum 14/3 and multiplied by 100 gives 150/7.
- Edge case: Constant observations make the denominator zero and return NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_constant_observations_make_centered_denominators_undefined

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Runtime equals 100 times SBF rather than 100 * (1 - Var(error)/Var(observation)).
  - Impact: It can exceed 100 and measures regression slope, not accounted variance.
  - Recommended future action: Confirm intended convention before any separately approved formula change.
- `duplicate-or-overlap`
  - Evidence: For every accepted input, VAF is algebraically exactly 100 * SBF.
  - Impact: Two names expose the same slope information on different scales.
  - Recommended future action: Document the overlap and review registry intent.

<a id="metric-rse"></a>
### `RSE` — Residual Standard Error

- Registered method: `residual_standard_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity) for positive degrees of freedom; ZeroDivisionError at zero degrees of freedom; NaN for negative degrees of freedom
- Ideal value: 0 when degrees of freedom are positive

#### Implemented behavior

- Formula: sqrt(sum((prediction - observation)^2) / (N - p - 1))
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - Bottleneck nansum
  - NumPy sqrt

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `p` | `1` | Values supporting subtraction from an integer | None; p is subtracted with one intercept from filtered N. | Values producing zero degrees of freedom raise ZeroDivisionError; negative degrees of freedom return NaN with a RuntimeWarning; incompatible types raise TypeError. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed and N is the surviving count.
- Zero inputs or denominators: Zero degrees of freedom raises ZeroDivisionError because scalar division occurs before NumPy sqrt.
- Negative inputs: Negative data are accepted; negative p is also accepted and inflates degrees of freedom.
- Constant series: Defined when degrees of freedom are positive; exact agreement gives zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Residual standard error is sqrt(RSS/(n-k)); with p predictors and an intercept, k=p+1.
- References:
  - [Residual standard deviation](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm) — NIST/SEMATECH (2012), authoritative. Supports: Defines residual standard deviation using residual sum of squares and n minus fitted coefficients.
- Known variants:
  - Some APIs define p as total fitted coefficients rather than predictors excluding intercept.

#### Characterization and tests

- Ordinary case: RSS 6 divided by N-p-1 = 1 at default p=1 gives sqrt(6).
- Edge case: For N=3, p=2 raises ZeroDivisionError and p=3 returns NaN with a RuntimeWarning.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_4.py::test_batch_4_metrics_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_4.py::test_residual_standard_error_degrees_of_freedom_are_unvalidated

#### Findings and recommended future action

- `consistent`
  - Evidence: For valid predictor count and same-sample fitted predictions, runtime matches sqrt(RSS/(n-p-1)).
  - Impact: Ordinary values follow the standard regression formula.
  - Recommended future action: Document that p excludes the intercept and predictions should derive from the fitted model.
- `validation-gap`
  - Evidence: p accepts values producing zero or negative degrees of freedom, nonintegers, and negative counts.
  - Impact: Calls can raise ZeroDivisionError or return NaN and can use nonsensical degrees of freedom.
  - Recommended future action: Validate p as a nonnegative integer satisfying p < N-1 in a separately approved runtime change.

<a id="metric-kge"></a>
### `KGE` — Kling-Gupta Efficiency

- Registered method: `kling_gupta_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: 4-tuple (score, correlation, standard-deviation ratio, mean ratio)
- Implemented range: score (-infinity, 1] when defined; components may be nonfinite
- Ideal value: (1, 1, 1, 1)

#### Implemented behavior

- Formula: 1 - sqrt((r-1)^2 + (alpha-1)^2 + (beta-1)^2), alpha=std(prediction)/std(observation), beta=mean(prediction)/mean(observation)
- Preprocessing:
  - Convert to equal-shaped float arrays.
  - Flatten and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy corrcoef and sqrt
  - Bottleneck nanstd
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed; computed nonfinite components propagate.
- Zero inputs or denominators: Zero observed standard deviation or mean makes alpha or beta NaN through _safe_divide.
- Negative inputs: Accepted; a negative or zero observed mean can make beta negative or undefined.
- Constant series: Correlation is NaN and exact constant agreement returns (NaN, NaN, NaN, 1).
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The 2009 KGE uses correlation r, variability ratio alpha=sigma_s/sigma_o, and bias ratio beta=mu_s/mu_o in Euclidean distance from (1,1,1).
- References:
  - [Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling](https://doi.org/10.1016/j.jhydrol.2009.08.003) — Gupta, Kling, Yilmaz, and Martinez (2009), primary. Supports: Introduces the three-component KGE construction.
- Known variants:
  - KGE2012 replaces the standard-deviation ratio with a coefficient-of-variation ratio; KGE double prime replaces the mean ratio with normalized additive bias.

#### Characterization and tests

- Ordinary case: For prediction [2,4,6] and observation [1,3,5], r=1, alpha=1, beta=4/3, and KGE=2/3.
- Edge case: Exact constant agreement returns a NaN score because correlation and alpha are undefined.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_kge_family_distinguishes_component_definitions
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `consistent`
  - Evidence: The returned components and score match the original 2009 definition for nondegenerate data.
  - Impact: The tuple makes each diagnostic component visible.
  - Recommended future action: Document tuple order and undefined constant/zero-mean cases.

<a id="metric-kge2012"></a>
### `KGE2012` — Modified Kling-Gupta Efficiency

- Registered method: `modified_kling_gupta_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: 4-tuple (score, correlation, coefficient-of-variation ratio, mean ratio)
- Implemented range: score (-infinity, 1] when defined; ZeroDivisionError is possible
- Ideal value: (1, 1, 1, 1)

#### Implemented behavior

- Formula: 1 - sqrt((r-1)^2 + (gamma-1)^2 + (beta-1)^2), gamma=(std(prediction)/mean(prediction))/(std(observation)/mean(observation)), beta=mean(prediction)/mean(observation)
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy corrcoef and sqrt
  - Bottleneck nanstd

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed; computed NaN propagates.
- Zero inputs or denominators: Python-float division by a zero observed mean or coefficient of variation raises ZeroDivisionError.
- Negative inputs: Accepted; signed means affect both gamma and beta.
- Constant series: Exact nonzero constant agreement raises ZeroDivisionError while forming gamma.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: KGE prime retains r and beta but uses gamma=CV_s/CV_o as its variability component.
- References:
  - [Runoff conditions in the upper Danube basin under an ensemble of climate change scenarios](https://doi.org/10.1016/j.jhydrol.2012.01.011) — Kling, Fuchs, and Paulin (2012), primary. Supports: Defines modified KGE with coefficient-of-variation ratio gamma.
- Known variants:
  - The implementation calls the third tuple member alpha although the source commonly denotes this CV ratio gamma.

#### Characterization and tests

- Ordinary case: The ordinary sample has r=1, gamma=3/4, beta=4/3, and score 7/12.
- Edge case: A zero observation mean raises ZeroDivisionError rather than returning a nonfinite tuple.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_kge_family_distinguishes_component_definitions
  - tests/audit/test_characterization_batch_5.py::test_zero_observation_mean_distinguishes_ratio_and_normalized_bias_variants

#### Findings and recommended future action

- `consistent`
  - Evidence: The ordinary formula uses the published CV ratio and mean ratio.
  - Impact: It is distinct from KGE 2009 despite the local alpha variable name.
  - Recommended future action: Document the third returned component as gamma/CV ratio.
- `validation-gap`
  - Evidence: Zero means and constant agreement can raise raw ZeroDivisionError.
  - Impact: Degenerate inputs do not return a stable tuple shape.
  - Recommended future action: Consider explicit denominator handling in a separately approved runtime change.

<a id="metric-kgedp"></a>
### `KGEdp` — Kling-Gupta Efficiency Double Prime

- Registered method: `kling_gupta_efficiency_double_prime`
- Category: efficiency and environmental evaluation
- Return shape: 4-tuple (score, correlation, standard-deviation ratio, normalized bias)
- Implemented range: score (-infinity, 1] when defined; ZeroDivisionError is possible
- Ideal value: (1, 1, 1, 0)

#### Implemented behavior

- Formula: 1 - sqrt((r-1)^2 + (alpha-1)^2 + beta_n^2), alpha=std(prediction)/std(observation), beta_n=(mean(prediction)-mean(observation))/std(observation)
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Raise ValueError if no finite pair remains.
- Dependencies:
  - NumPy corrcoef and sqrt
  - Bottleneck nanstd

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero observed standard deviation raises ZeroDivisionError; zero observed mean alone is supported.
- Negative inputs: Accepted without a mean-ratio singularity.
- Constant series: Zero observed spread raises ZeroDivisionError.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: KGE double prime uses r, standard-deviation ratio alpha, and normalized additive bias beta_n whose ideal is zero.
- References:
  - [SC-Earth: A Station-Based Serially Complete Earth Dataset from 1950 to 2019](https://doi.org/10.1175/JCLI-D-21-0067.1) — Tang, Clark, and Papalexiou (2021), primary. Supports: Defines the 2021 KGE double-prime components, including normalized bias.
- Known variants:
  - Unlike KGE and KGE prime, beta_n is squared directly because its ideal is zero.

#### Characterization and tests

- Ordinary case: The ordinary sample gives r=alpha=1, beta_n=sqrt(3/8), and score 1-sqrt(3/8).
- Edge case: With observation mean zero but nonzero spread, the score remains defined; constant observations raise ZeroDivisionError.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_kge_family_distinguishes_component_definitions
  - tests/audit/test_characterization_batch_5.py::test_zero_observation_mean_distinguishes_ratio_and_normalized_bias_variants

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime uses additive normalized bias with ideal zero, distinct from both earlier KGE variants.
  - Impact: Zero-mean observations can be evaluated when their spread is nonzero.
  - Recommended future action: Document the component's zero ideal and constant-series failure.

<a id="metric-de"></a>
### `DE` — Diagnostic Efficiency

- Registered method: `diagnostic_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: 4-tuple (score, correlation, dynamic FDC bias, mean FDC bias)
- Implemented range: (-infinity, 1] score, or NaN
- Ideal value: 1 after the implementation-specific 1-DE transformation; canonical DE ideal is 0

#### Implemented behavior

- Formula: 1 - sqrt(B_rel_mean^2 + B_area^2 + (r-1)^2), with independently descending positive-observation FDCs and trapezoidal integration of absolute residual relative bias
- Preprocessing:
  - Shared finite-pair filtering.
  - Keep only positions with positive observations for FDC components.
  - Sort retained predictions and observations independently descending.
- Dependencies:
  - NumPy corrcoef, sort, linspace, trapz

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before all calculations.
- Zero inputs or denominators: Zero/nonpositive observations are excluded from the FDC; fewer than two positive observations returns NaN components except r.
- Negative inputs: Negative observations are excluded from FDC components but remain in timing correlation.
- Constant series: A constant input makes r NaN and therefore score NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Schwemmle DE is the unbounded Euclidean error distance of constant, dynamic, and timing errors and has ideal zero.
- References:
  - [Technical note: Diagnostic efficiency – specific evaluation of model performance](https://doi.org/10.5194/hess-25-2187-2021) — Schwemmle, Demand, and Weiler (2021), primary. Supports: Defines DE, its FDC components, unbounded error range, and zero optimum.
- Known variants:
  - Runtime applies an implementation-specific 1-DE transformation; no primary source was established for naming that transformed score DE.

#### Characterization and tests

- Ordinary case: The ordinary sample gives B_rel_mean=23/45, B_area=13/45, r=1, and implemented score 1-sqrt((23/45)^2+(13/45)^2).
- Edge case: Only one positive observation returns (NaN, r, NaN, NaN).
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_composite_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_diagnostic_efficiency_requires_two_positive_observations

#### Findings and recommended future action

- `possible-defect`
  - Evidence: The primary paper defines unbounded DE as a distance with ideal zero; runtime silently returns the implementation-specific transformation 1-DE under the same DE identity, and no primary support was established for that naming.
  - Impact: The score's direction, ideal, numeric value, and range differ from canonical DE although its components are recognizable.
  - Recommended future action: Confirm intent before either restoring canonical DE or explicitly renaming and documenting the transformed score in a separately approved runtime change.

<a id="metric-lme"></a>
### `LME` — Liu Model Efficiency

- Registered method: `liu_model_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: 5-tuple (score, correlation, variability ratio, bias ratio, forward slope)
- Implemented range: (-infinity, 1] score, including -infinity; NaN possible
- Ideal value: (1, 1, 1, 1, 1)

#### Implemented behavior

- Formula: 1 - sqrt((r*alpha-1)^2 + (beta-1)^2)
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
- Dependencies:
  - NumPy corrcoef and sqrt
  - Bottleneck nanstd

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed; calculated infinities/NaNs remain.
- Zero inputs or denominators: Zero observed mean maps beta to 1 if both means are zero, otherwise infinity; zero observed spread similarly maps alpha.
- Negative inputs: Accepted; signed mean ratio affects beta.
- Constant series: Correlation is NaN even when alpha is forced to one, so score is NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Liu mean efficiency combines forward least-squares slope r*alpha and mean ratio beta.
- References:
  - [A rational performance criterion for hydrological model](https://doi.org/10.1016/j.jhydrol.2020.125488) — Dedi Liu (2020), primary. Supports: Introduces Liu mean efficiency and its combined slope/bias formula.
- Known variants:
  - None

#### Characterization and tests

- Ordinary case: r=alpha=slope=1 and beta=4/3 give LME=2/3.
- Edge case: A nonzero prediction mean with zero observation mean yields beta infinity and score negative infinity.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_composite_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_zero_observation_mean_distinguishes_ratio_and_normalized_bias_variants

#### Findings and recommended future action

- `consistent`
  - Evidence: Ordinary behavior matches the published combined forward-slope and bias formula.
  - Impact: Five returned values expose the calculation.
  - Recommended future action: Document tuple order and nonfinite degeneracies.

<a id="metric-lcef"></a>
### `LCEf` — Least-squares Combined Efficiency

- Registered method: `least_squares_combined_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: 6-tuple (score, correlation, variability ratio, bias ratio, forward slope, reverse slope)
- Implemented range: (-infinity, 1] score, including -infinity; NaN possible
- Ideal value: (1, 1, 1, 1, 1, 1)

#### Implemented behavior

- Formula: 1 - sqrt((r*alpha-1)^2 + (r/alpha-1)^2 + (beta-1)^2)
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
- Dependencies:
  - NumPy corrcoef and sqrt
  - Bottleneck nanstd

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed; computed NaN remains.
- Zero inputs or denominators: Zero mean or observed spread is mapped to explicit ratios; alpha zero makes reverse slope infinity and score negative infinity.
- Negative inputs: Accepted; signed mean ratio affects beta.
- Constant series: Correlation and both slopes are NaN for exact constant agreement.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Least-squares combined efficiency adds forward and reverse regression slope distances to mean-ratio distance.
- References:
  - [A rebalanced performance criterion for hydrological model calibration](https://doi.org/10.1016/j.jhydrol.2021.127372) — Lee and Choi (2022), primary. Supports: Introduces LCE using r*alpha, r/alpha, and beta.
- Known variants:
  - The paper calls the metric LCE; this registry uses LCEf to avoid collision with its Legates metric abbreviation.

#### Characterization and tests

- Ordinary case: Both slopes equal one and beta=4/3, giving score 2/3.
- Edge case: Exact constant agreement returns NaN score and slopes despite forced alpha and beta of one.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_composite_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `consistent`
  - Evidence: Ordinary runtime matches Lee and Choi's bidirectional-slope formula.
  - Impact: The local abbreviation differs only to disambiguate registry identities.
  - Recommended future action: Document that LCEf corresponds to published LCE.

<a id="metric-wia"></a>
### `WIA` — Willmott's Index of Agreement

- Registered method: `willmotts_index_of_agreement`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: [0, 1] for defined finite data; ZeroDivisionError possible
- Ideal value: 1

#### Implemented behavior

- Formula: 1 - sum((prediction-observation)^2) / sum((abs(prediction-mean(observation))+abs(observation-mean(observation)))^2)
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
- Dependencies:
  - Bottleneck nansum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: An exactly zero potential-error denominator raises ZeroDivisionError.
- Negative inputs: Accepted without domain restriction.
- Constant series: Exact constant agreement raises ZeroDivisionError.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Willmott's original d is one minus squared error divided by squared potential error about the observed mean.
- References:
  - [On the validation of models](https://doi.org/10.1080/02723646.1981.10642213) — Willmott (1981), primary. Supports: Introduces the index of agreement and potential-error denominator.
- Known variants:
  - Absolute-error modified and refined indices reduce squared-error sensitivity.

#### Characterization and tests

- Ordinary case: Squared error 3 and potential-error sum 35 give d=32/35.
- Edge case: Exact constant agreement attempts 0/0 and raises ZeroDivisionError.
- Existing tests:
  - tests/test_error_metrics.py::test_efficiency_metrics
  - tests/test_error_metrics.py::test_metric_bounds
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_agreement_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `consistent`
  - Evidence: The nondegenerate formula matches the original squared index of agreement.
  - Impact: Ordinary values have the established interpretation.
  - Recommended future action: Document the exact-constant exception.

<a id="metric-wiar"></a>
### `WIAr` — Refined Index of Agreement

- Registered method: `refined_index_of_agreement`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: [0, 1] for finite nondegenerate data; source range is [-1, 1]; ZeroDivisionError possible
- Ideal value: 1

#### Implemented behavior

- Formula: A=sum(abs(prediction-observation)); B=2*sum(abs(observation-mean(observation))); if A<=B return 1-A/B, else return 1-B/A
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
- Dependencies:
  - Bottleneck nansum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: A=B=0 raises ZeroDivisionError in the first branch.
- Negative inputs: Accepted without domain restriction.
- Constant series: Exact constant agreement raises ZeroDivisionError; imperfect constants enter the second branch and return one.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Refined d_r returns 1-A/B when A<=B and B/A-1 when A>B, yielding range [-1,1].
- References:
  - [A refined index of model performance](https://doi.org/10.1002/joc.2419) — Willmott, Robeson, and Matsuura (2012), primary. Supports: Defines the piecewise refined index and its negative second branch.
- Known variants:
  - None

#### Characterization and tests

- Ordinary case: A=3 and B=8 use the first branch and return 5/8.
- Edge case: Exact constant agreement raises ZeroDivisionError; A>B cases have the opposite sign from the source formula.
- Existing tests:
  - tests/test_error_metrics.py::test_msd_decomposition
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_agreement_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_refined_index_poor_fit_branch_has_implemented_positive_sign
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `possible-defect`
  - Evidence: The source's A>B branch is B/A-1, but runtime returns 1-B/A.
  - Impact: Poor fits that should be negative are reported positive, collapsing implemented range to nonnegative values.
  - Recommended future action: Correct the branch only in a separately approved behavior change with migration notes.

<a id="metric-lce"></a>
### `LCE` — Legates Coefficient of Efficiency

- Registered method: `legates_coefficient_of_efficiency`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1 - sum(abs(prediction-observation)) / sum(abs(observation-mean(observation)))
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
- Dependencies:
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed.
- Zero inputs or denominators: Zero observed absolute-deviation denominator returns NaN.
- Negative inputs: Accepted without domain restriction.
- Constant series: Any constant observation series returns NaN, including exact agreement.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The modified coefficient E1 uses absolute residuals relative to absolute deviations from the observed mean.
- References:
  - [Evaluating the use of goodness-of-fit measures in hydrologic and hydroclimatic model validation](https://doi.org/10.1029/1998WR900018) — Legates and McCabe (1999), primary. Supports: Presents the absolute-error modified coefficient of efficiency.
- Known variants:
  - Published notation is commonly E1 rather than LCE; LCE also names Lee and Choi's different least-squares metric.

#### Characterization and tests

- Ordinary case: Absolute error 3 divided by observed absolute deviation 4 gives 1/4.
- Edge case: Constant observations make the reference denominator zero and return NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_agreement_efficiencies_match_ordinary_hand_calculations
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `consistent`
  - Evidence: Runtime matches the Legates-McCabe absolute-error efficiency formula.
  - Impact: It is less outlier-sensitive than squared NSE.
  - Recommended future action: Document the E1 literature notation and constant-series NaN.
- `documentation-gap`
  - Evidence: The abbreviation LCE is not the paper's standard notation and overlaps conceptually with published least-squares combined efficiency.
  - Impact: Users may confuse two unrelated metrics.
  - Recommended future action: Cross-reference E1 and disambiguate LCE versus LCEf.

<a id="metric-ksi"></a>
### `KSI` — Kolmogorov-Smirnov Test Integral

- Registered method: `ksi`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity) raw; [0, infinity) percent when normalization is defined; NaN on zero range
- Ideal value: 0

#### Implemented behavior

- Formula: sum(abs(ECDF_observation(x_i)-ECDF_prediction(x_i)) * (x_(i+1)-x_i)) over the sorted unique pooled grid; normalized value is 100*KSI/(1.63/sqrt(N)*(max(x)-min(x)))
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Build ECDFs on filtered samples.
  - Use sorted unique pooled sample values as the integration grid.
- Dependencies:
  - Statsmodels ECDF
  - NumPy unique and diff
  - _safe_divide

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `normed` | `True` | Any value interpreted by Python truth testing | None. | Truthiness selects normalized versus raw output; no strict boolean validation. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before constructing ECDFs.
- Zero inputs or denominators: A zero pooled range makes normalized critical area zero and returns NaN; raw KSI is zero.
- Negative inputs: Accepted; only pooled spacing and ranks matter.
- Constant series: Normalized output is NaN for a common constant; distinct constants have positive range and finite output.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: KSI integrates absolute separation between two empirical CDFs; percent KSI divides by a Kolmogorov-Smirnov critical area.
- References:
  - [Analysis of different comparison parameters applied to solar radiation data from satellite and German radiometric stations](https://doi.org/10.1016/j.solener.2008.07.009) — Espinar and coauthors (2009), primary. Supports: Introduces KSI as integrated ECDF separation and normalized critical-area percentage.
- Known variants:
  - Critical constants vary with confidence level and sample-size convention; runtime fixes 1.63 and uses only observation N.

#### Characterization and tests

- Ordinary case: On pooled grid [1,2,3,4,5,6], left-rectangle ECDF gaps integrate to raw KSI 1 and normalized KSI 100/(1.63*5/sqrt(3)).
- Edge case: Identical constants have raw area zero but normalized 0/0 returns NaN; distinct constants give raw area 1 and finite normalized output; a truthy string selects normalization.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_5.py::test_ksi_integrates_only_over_unique_sample_grid
  - tests/audit/test_characterization_batch_5.py::test_ksi_distinct_constants_and_truthy_non_boolean_normed
  - tests/audit/test_characterization_batch_5.py::test_constant_identical_series_expose_denominator_failures

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime uses a left-rectangle sum on the pooled discontinuity grid and fixed 1.63 critical factor; source presentations describe the integral and commonly trapezoidal numerical evaluation.
  - Impact: Discrete numerical values and normalization depend on grid and convention.
  - Recommended future action: Document the exact grid, rectangle rule, confidence factor, and one-sample N convention.
- `validation-gap`
  - Evidence: normed is truth-tested rather than validated as bool.
  - Impact: Unexpected truthy values silently request normalized output.
  - Recommended future action: Validate the parameter in a separately approved runtime change.

<a id="metric-phi"></a>
### `PHI` — Percentage of Histogram Intersection

- Registered method: `phi`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, 1]
- Ideal value: 1

#### Implemented behavior

- Formula: Sum over common pooled-range bins of min(prediction relative frequency, observation relative frequency).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Construct equal-width common edges from pooled filtered values.
- Dependencies:
  - NumPy histogram_bin_edges and histogram

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `n_bins` | `10` | int excluding bool | Must be an integer >= 1. | Raises ValueError. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before binning.
- Zero inputs or denominators: Filtered nonempty samples make both count sums positive.
- Negative inputs: Accepted; pooled edges span signed values.
- Constant series: Identical constants return one; separated constants can return zero depending on bins.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Histogram intersection sums the componentwise minima of two normalized histograms.
- References:
  - [Color indexing](https://doi.org/10.1007/BF00130487) — Swain and Ballard (1991), primary. Supports: Introduces histogram intersection for distribution similarity.
- Known variants:
  - Some presentations multiply the normalized fraction by 100; runtime returns a fraction despite Percentage in its name.

#### Characterization and tests

- Ordinary case: Counts [3,0,0,1] versus [1,1,1,1] normalize to overlap 1/2.
- Edge case: A common constant distribution returns one; invalid bin counts raise ValueError.
- Existing tests:
  - tests/test_v5_metrics.py::test_phi_identical_and_separated_histograms
  - tests/test_v5_metrics.py::test_phi_bounds_validation_and_registry
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_histogram_metrics_match_hand_calculation_and_validate_bins
  - tests/audit/test_characterization_batch_6.py::test_constant_distributions_expose_metric_specific_behavior

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The registered name says Percentage although runtime returns the conventional normalized fraction without multiplying by 100.
  - Impact: Users may interpret 0.5 as 0.5 percent instead of 50 percent.
  - Recommended future action: Document fraction units and bin sensitivity.

<a id="metric-suse"></a>
### `SUSE` — Scaled and Unscaled Shannon Entropy Difference

- Registered method: `suse`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, log(n_bins)]
- Ideal value: 0

#### Implemented behavior

- Formula: max(abs(H_prediction-H_observation) on common pooled edges, abs(H_prediction-H_observation) on separate per-series edges), where H=-sum(p*ln(p)).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Discard zero-probability bins before logarithms.
- Dependencies:
  - NumPy histogram_bin_edges, histogram, and log

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `n_bins` | `10` | int excluding bool | Must be an integer >= 1. | Raises ValueError. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before entropy calculation.
- Zero inputs or denominators: Nonempty count totals prevent division by zero.
- Negative inputs: Accepted; entropy depends on bin occupancy.
- Constant series: Each constant series has entropy zero, so even distinct constants return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: SUSE is the maximum of common-range scaled and separate-range unscaled Shannon entropy differences.
- References:
  - [Use of an entropy-based metric in multiobjective calibration to improve model performance](https://doi.org/10.1002/2013WR014537) — Pechlivanidis and coauthors (2014), primary. Supports: Introduces the combined scaled and unscaled entropy comparison.
  - [Robust informational entropy-based descriptors of flow in catchment hydrology](https://doi.org/10.1080/02626667.2014.983516) — Pechlivanidis and coauthors (2016), primary. Supports: Defines SUSE estimator and normalization variants.
  - [A Mathematical Theory of Communication](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x) — Claude E. Shannon (1948), primary. Supports: Defines discrete entropy as the negative probability-weighted logarithm sum.
- Known variants:
  - The published normalized dimensionless convention divides by log(n_bins); runtime returns raw natural-log entropy difference.
  - Logarithm base and bin estimator change the numerical scale.

#### Characterization and tests

- Ordinary case: A [3,0,0,1] occupancy versus four equal occupancies gives entropy difference log(4)-(log(4)-3/4*log(3)).
- Edge case: Distinct constant series both have zero entropy and therefore return zero.
- Existing tests:
  - tests/test_v5_metrics.py::test_suse_behavior_validation_and_registry
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_histogram_metrics_match_hand_calculation_and_validate_bins
  - tests/audit/test_characterization_batch_6.py::test_histogram_entropy_distinguishes_common_and_separate_edges

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime fixes natural logarithms and NumPy equal-width automatic ranges; published entropy comparisons permit bin-resolution and normalization choices.
  - Impact: Values are resolution- and convention-dependent.
  - Recommended future action: Document natural-log units and exact common/separate edge construction.
- `validation-gap`
  - Evidence: n_bins is validated but no sample-size suitability rule is enforced.
  - Impact: Many empty bins can make small-sample entropy unstable while still returning a value.
  - Recommended future action: Document bin-count sensitivity without changing runtime behavior.

<a id="metric-over"></a>
### `OVER` — Over-estimation Metric

- Registered method: `over_metric`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity) raw or normalized percent; NaN when normalized pooled range is zero
- Ideal value: 0

#### Implemented behavior

- Formula: Left-rectangle integral over the pooled unique grid of max(ECDF_prediction-ECDF_observation,0); normalized as 100*area/(1.63/sqrt(N)*pooled range).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Construct paired-sample marginal ECDFs.
- Dependencies:
  - Statsmodels ECDF
  - NumPy unique and diff
  - _safe_divide

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `normed` | `True` | Any value interpreted by Python truth testing | None. | Truthiness selects normalized versus raw output. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before ECDF construction.
- Zero inputs or denominators: Zero pooled range returns NaN normalized and zero raw.
- Negative inputs: Accepted; only ECDF ordering and spacing matter.
- Constant series: Identical constants return zero raw and NaN normalized; distinct constants can return positive directional area.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Espinar OVER integrates max(abs(F_prediction-F_observation)-1.63/sqrt(N),0) and normalizes by the corresponding KS critical area.
- References:
  - [Analysis of different comparison parameters applied to solar radiation data from satellite and German radiometric stations](https://doi.org/10.1016/j.solener.2008.07.009) — Espinar and coauthors (2009), primary. Supports: Defines absolute ECDF-gap OVER, the subtracted 1.63/sqrt(N) threshold, and critical-area normalization.
- Known variants:
  - Runtime instead integrates the directional positive prediction-minus-observation ECDF gap and does not subtract the KS threshold.

#### Characterization and tests

- Ordinary case: Predictions [0,2,4] and observations [1,3,5] give runtime raw area one, while swapping the arrays gives zero. Every absolute ECDF gap is at most 1/3, below canonical Vc=1.63/sqrt(3), so Espinar's thresholded OVER is zero in both orientations.
- Edge case: Identical constants give zero raw but NaN after zero-range normalization.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_over_uses_directional_left_rectangle_area_and_fixed_normalizer
  - tests/audit/test_characterization_batch_6.py::test_over_is_directional_while_canonical_thresholded_gap_is_zero
  - tests/audit/test_characterization_batch_6.py::test_constant_distributions_expose_metric_specific_behavior

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Espinar OVER uses max(abs(F_prediction-F_observation)-Vc,0); runtime omits Vc and uses max(F_prediction-F_observation,0).
  - Impact: Runtime is directional and reports area for gaps below the canonical threshold, so it is not canonical OVER.
  - Recommended future action: Confirm intent before correcting or renaming in a separately approved runtime change.
- `validation-gap`
  - Evidence: normed is truth-tested rather than validated as bool.
  - Impact: Unexpected truthy values silently select normalized output.
  - Recommended future action: Validate in a separately approved runtime change.

<a id="metric-iqr"></a>
### `IQR` — Interquartile Range

- Registered method: `IQR`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: context-dependent

#### Implemented behavior

- Formula: NumPy percentile(observations,75) - percentile(observations,25), using the installed default linear percentile method.
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Ignore predictions after pair filtering.
- Dependencies:
  - NumPy percentile

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed, including their paired finite observations.
- Zero inputs or denominators: No division; all-zero observations return zero.
- Negative inputs: Accepted.
- Constant series: Returns zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: IQR is the 75th percentile minus the 25th percentile.
- References:
  - [numpy.percentile documentation](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html) — NumPy developers (2026), authoritative. Supports: Defines percentile calculation and the default linear method used by runtime.
- Known variants:
  - Sample quantile interpolation methods differ for finite samples.

#### Characterization and tests

- Ordinary case: Observations [1,2,3,4] have linearly interpolated quartiles 1.75 and 3.25, hence IQR 1.5.
- Edge case: Constant observations return zero.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_distribution_summary_and_moments_match_hand_calculations
  - tests/audit/test_characterization_batch_6.py::test_constant_distributions_expose_metric_specific_behavior

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime inherits NumPy's installed default quantile interpolation, one of multiple accepted sample-quantile conventions.
  - Impact: Small-sample IQR can vary across conventions or dependency-era defaults.
  - Recommended future action: Document the linear percentile convention.

<a id="metric-std"></a>
### `STD` — Standard Deviation

- Registered method: `STD`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: context-dependent

#### Implemented behavior

- Formula: Population standard deviation of filtered observations with divisor N (ddof=0).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Ignore predictions after pair filtering.
- Dependencies:
  - Bottleneck nanstd, or NumPy nanstd fallback

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before calculation.
- Zero inputs or denominators: A one-element or all-zero observation series returns zero.
- Negative inputs: Accepted.
- Constant series: Returns zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Standard deviation is the square root of the mean squared deviation; population and sample divisor conventions differ.
- References:
  - [numpy.std documentation](https://numpy.org/doc/stable/reference/generated/numpy.std.html) — NumPy developers (2026), authoritative. Supports: Defines the ddof=0 population normalization used by the compatible implementation.
- Known variants:
  - Sample standard deviation uses N-1 rather than runtime's population divisor N.

#### Characterization and tests

- Ordinary case: Observations [1,2,3,4] have population variance 5/4 and STD sqrt(5/4).
- Edge case: Constant observations return zero.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_distribution_summary_and_moments_match_hand_calculations
  - tests/audit/test_characterization_batch_6.py::test_constant_distributions_expose_metric_specific_behavior

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The method name does not state that runtime uses population normalization ddof=0 and observations only.
  - Impact: Users expecting sample standard deviation obtain a smaller value.
  - Recommended future action: Document observations-only scope and ddof=0.

<a id="metric-neskew"></a>
### `nESkew` — Normalized Error Skewness

- Registered method: `normalized_error_skewness`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: unbounded signed scalar or NaN
- Ideal value: 0 for symmetric normalized errors

#### Implemented behavior

- Formula: SciPy bias-corrected sample skewness of nE=(prediction-observation)/max(prediction).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - If max prediction is numerically zero, replace all normalized errors by NaN.
  - Keep finite normalized errors and require at least three.
- Dependencies:
  - SciPy skew with bias=False
  - NumPy nanmax and isclose

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs are removed; calculated nonfinite normalized errors are removed.
- Zero inputs or denominators: A numerically zero maximum prediction returns NaN.
- Negative inputs: Accepted; a negative maximum reverses normalized-error signs and therefore skewness sign.
- Constant series: Constant normalized errors have undefined skewness and return NaN with a SciPy warning.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: No primary source was located for nESkew under this name or normalization; skewness itself is the standardized third central moment and runtime uses SciPy's bias-corrected sample coefficient.
- References:
  - [scipy.stats.skew documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html) — SciPy developers (2026), authoritative. Supports: Defines the adjusted Fisher-Pearson standardized moment returned with bias=False.
- Known variants:
  - The registry's Correndo et al. 2021 attribution could not be verified.
  - Population versus bias-corrected sample skewness differ; normalization is immaterial for positive scale but reverses skew under negative scale.

#### Characterization and tests

- Ordinary case: Normalized errors proportional to [0,0,0,4] have bias-corrected skewness 2.
- Edge case: Negative max prediction reverses the sign to -2; fewer than three finite values or zero max returns NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_normalized_error_shape_metrics_return_nan_for_zero_predictions
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_distribution_summary_and_moments_match_hand_calculations
  - tests/audit/test_characterization_batch_6.py::test_normalized_moments_use_prediction_max_and_unbiased_fisher_conventions

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime normalizes by signed max(prediction), so all-negative predictions reverse skewness sign although positive rescaling normally leaves skewness invariant.
  - Impact: Reported asymmetry direction depends on prediction sign convention.
  - Recommended future action: Confirm and document the normalization definition before any behavior change.
- `documentation-gap`
  - Evidence: The Correndo et al. attribution could not be verified; runtime uses local normalization plus bias-corrected sample skewness and requires three points.
  - Impact: Users lack a traceable scientific identity and small samples differ from population-moment calculations.
  - Recommended future action: Correct the attribution if a source is found; meanwhile document SciPy bias=False and minimum sample size.

<a id="metric-nekurt"></a>
### `nEKurt` — Normalized Error Kurtosis

- Registered method: `normalized_error_kurtosis`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: unbounded scalar or NaN
- Ideal value: 0 for normal-distribution excess kurtosis

#### Implemented behavior

- Formula: SciPy bias-corrected Fisher excess kurtosis of nE=(prediction-observation)/max(prediction).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - If max prediction is numerically zero, replace all normalized errors by NaN.
  - Keep finite normalized errors and require at least four.
- Dependencies:
  - SciPy kurtosis with fisher=True and bias=False
  - NumPy nanmax and isclose

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs are removed; calculated nonfinite normalized errors are removed.
- Zero inputs or denominators: A numerically zero maximum prediction returns NaN.
- Negative inputs: Accepted; sign reversal does not change kurtosis.
- Constant series: Constant normalized errors have undefined kurtosis and return NaN with a SciPy warning.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: No primary source was located for nEKurt under this name or normalization; kurtosis is the standardized fourth central moment, and runtime returns SciPy bias-corrected Fisher excess.
- References:
  - [scipy.stats.kurtosis documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html) — SciPy developers (2026), authoritative. Supports: Defines Fisher versus Pearson conventions and bias correction.
- Known variants:
  - The registry's Correndo et al. 2021 attribution could not be verified.
  - Pearson kurtosis has normal ideal 3; runtime returns Fisher excess with normal ideal 0.

#### Characterization and tests

- Ordinary case: Normalized errors proportional to [0,0,0,4] have bias-corrected Fisher excess kurtosis 4.
- Edge case: Fewer than four finite values or a zero prediction maximum returns NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_normalized_error_shape_metrics_return_nan_for_zero_predictions
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_distribution_summary_and_moments_match_hand_calculations
  - tests/audit/test_characterization_batch_6.py::test_normalized_moments_use_prediction_max_and_unbiased_fisher_conventions

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The Correndo et al. attribution could not be verified; runtime returns bias-corrected Fisher excess kurtosis and requires four points.
  - Impact: Users lack a traceable scientific identity, and values differ by three from Pearson convention and from biased estimates.
  - Recommended future action: Correct the attribution if a source is found; meanwhile document fisher=True, bias=False, and minimum sample size.

<a id="metric-mbf"></a>
### `MBF` — Mean Bias Factor

- Registered method: `mean_bias_factor`
- Category: bias
- Return shape: scalar
- Implemented range: (0, infinity)
- Ideal value: 1

#### Implemented behavior

- Formula: mean(predictions)/mean(observations), after requiring both means strictly positive.
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Compute arithmetic means on filtered pairs.
- Dependencies:
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before means.
- Zero inputs or denominators: Either nonpositive mean raises ValueError, including zero observed mean.
- Negative inputs: Individual negatives are accepted only when both final means remain positive.
- Constant series: Positive constants return their ratio; zero or negative constants raise ValueError.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Mean bias factor is a ratio of modeled and observed arithmetic means, with unity indicating equal means; orientation varies by source.
- References:
  - [Assessing precipitation event characteristics throughout North Carolina derived from GPM IMERG data products](https://doi.org/10.3389/frwa.2024.1296586) — Tan and coauthors (2024), primary. Supports: Defines the reciprocal observation/prediction MBF orientation, demonstrating that orientation must be explicit.
- Known variants:
  - Runtime uses prediction/observation, the reciprocal of the cited precipitation convention.
  - Runtime deliberately restricts both means to positive values.

#### Characterization and tests

- Ordinary case: Prediction mean 3 divided by observation mean 1.5 gives MBF 2; reciprocal twofold underprediction gives MBF 1/2.
- Edge case: Both-negative means (-1.5 and -3) raise ValueError, although their raw mean ratio is 1/2.
- Existing tests:
  - tests/test_v5_metrics.py::test_mean_bias_factors_match_hand_calculation
  - tests/test_v5_metrics.py::test_mean_bias_factors_require_positive_means
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_distinguish_positive_domain_from_unrestricted_ratio
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_pin_reciprocal_underprediction_and_same_sign_negative_means

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime computes prediction mean divided by observation mean; the cited MBF source uses the reciprocal orientation.
  - Impact: Over- and underprediction interpretation reverses across otherwise recognizable MBF definitions.
  - Recommended future action: Document prediction/observation orientation and that the positivity restriction applies to means, not every individual value.

<a id="metric-rmbf"></a>
### `RMBF` — Relative Mean Bias Factor

- Registered method: `relative_mean_bias_factor`
- Category: bias
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: abs(MBF-1), where MBF=mean(predictions)/mean(observations) and both means must be positive.
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Delegate mean-domain validation to MBF.
- Dependencies:
  - mean_bias_factor
  - NumPy abs

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before delegated means.
- Zero inputs or denominators: Either nonpositive mean raises ValueError through MBF.
- Negative inputs: Individual negatives are accepted only when both means remain positive.
- Constant series: Positive constants return absolute ratio distance from one; nonpositive constants raise ValueError.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Runtime defines RMBF locally as unsigned absolute distance of the mean ratio from unity.
- References:
  - [ErrorMetrics public API and source](https://github.com/chayandatta/error-metrics) — error-metrics maintainers (2026), authoritative. Supports: Owns the RMBF identity and defines it as abs(MBF-1).
- Known variants:
  - Relative bias factor may instead preserve direction or symmetrize reciprocal over- and underprediction; no independent primary source was established for this exact RMBF name.

#### Characterization and tests

- Ordinary case: MBF 2 gives RMBF 1, whereas reciprocal MBF 1/2 gives RMBF 1/2, demonstrating factor-space asymmetry.
- Edge case: Both-negative means raise ValueError through MBF rather than producing the local absolute ratio distance.
- Existing tests:
  - tests/test_v5_metrics.py::test_mean_bias_factors_match_hand_calculation
  - tests/test_v5_metrics.py::test_mean_bias_factors_require_positive_means
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_distinguish_positive_domain_from_unrestricted_ratio
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_pin_reciprocal_underprediction_and_same_sign_negative_means

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: No independent primary scientific source was established for the exact unsigned abs(MBF-1) quantity under the RMBF name.
  - Impact: Users cannot assume equivalence to other relative or symmetric bias-factor definitions.
  - Recommended future action: Present RMBF explicitly as the package's unsigned transformation of MBF.

<a id="metric-nmbf"></a>
### `NMBF` — Normalized Mean Bias Factor

- Registered method: `nmbf`
- Category: bias
- Return shape: scalar
- Implemented range: unbounded signed scalar or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: mean(predictions)/mean(observations), with zero denominator mapped to NaN and no sign restriction.
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Compute arithmetic means on filtered pairs.
- Dependencies:
  - Bottleneck nanmean
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before means.
- Zero inputs or denominators: Zero observation mean returns NaN, including 0/0.
- Negative inputs: Accepted; result can be negative or positive according to mean signs.
- Constant series: Returns the constant ratio when observation is nonzero; zero observation constant returns NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Yu NMBF is a piecewise symmetric positive-domain factor bias with ideal zero: prediction/observation-1 for overprediction and 1-observation/prediction for underprediction.
- References:
  - [New unbiased symmetric metrics for evaluation of air quality models](https://doi.org/10.1002/asl.125) — Yu and coauthors (2006), primary. Supports: Defines the piecewise symmetric NMBF and its zero ideal.
  - [Generalized approach for using unbiased symmetric metrics with negative values](https://doi.org/10.1002/asl.393) — Gustafson and Yu (2012), primary. Supports: Extends the original positive-domain metric to same-sign negative means and excludes opposite signs.
- Known variants:
  - Runtime instead returns the raw prediction/observation ratio with ideal one and no sign-domain validation.

#### Characterization and tests

- Ordinary case: Prediction mean 3 divided by observation mean 1.5 returns 2; reciprocal twofold underprediction returns the raw ratio 1/2 rather than canonical NMBF -1.
- Edge case: Both-negative means -1.5 and -3 return raw ratio 1/2. Gustafson-Yu instead treats same-sign negatives through an absolute-magnitude extension of canonical piecewise NMBF; runtime does not implement that extension. Zero observation mean returns NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_duplicate_abbreviations_use_documented_scalar_methods
  - tests/test_v2_robustness.py::test_zero_denominator_metrics_return_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_distinguish_positive_domain_from_unrestricted_ratio
  - tests/audit/test_characterization_batch_6.py::test_bias_factors_pin_reciprocal_underprediction_and_same_sign_negative_means

#### Findings and recommended future action

- `duplicate-or-overlap`
  - Evidence: For positive means NMBF and MBF execute the same mean ratio; they differ only because MBF validates positive means.
  - Impact: Two registry identities return identical ordinary-domain values but advertise different domain behavior.
  - Recommended future action: Cross-reference the overlap and domain distinction.
- `possible-defect`
  - Evidence: Runtime NMBF returns a raw ratio with ideal one; Yu et al. define a piecewise symmetric factor bias with ideal zero.
  - Impact: Runtime values, ideal, symmetry, and domain handling differ from the named primary-source metric.
  - Recommended future action: Confirm intent before restoring the canonical piecewise formula or renaming in a separately approved runtime change.

<a id="metric-rnmbf"></a>
### `RNMBF` — Relative Normalized Mean Bias Factor

- Registered method: `rnmbf`
- Category: bias
- Return shape: scalar
- Implemented range: [0, infinity) or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: abs(mean(predictions)/mean(observations)-1).
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Delegate zero-denominator handling to NMBF.
- Dependencies:
  - nmbf
  - NumPy abs

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before means.
- Zero inputs or denominators: Zero observation mean returns NaN through NMBF.
- Negative inputs: Accepted without sign-domain validation.
- Constant series: Returns absolute ratio distance from one unless observation is zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Runtime defines RNMBF locally as absolute distance of its raw mean ratio from unity; no independent canonical source was established for this exact name.
- References:
  - [ErrorMetrics public API and source](https://github.com/chayandatta/error-metrics) — error-metrics maintainers (2026), authoritative. Supports: Owns the RNMBF identity and local transformation.
- Known variants:
  - Canonical Yu NMBF is piecewise symmetric with ideal zero, so applying this transformation to it would have a different meaning.

#### Characterization and tests

- Ordinary case: Prediction mean 4 and observation mean 2 give raw NMBF 2 and RNMBF 1.
- Edge case: Zero observation mean returns NaN.
- Existing tests:
  - tests/test_v2_robustness.py::test_duplicate_abbreviations_use_documented_scalar_methods
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `duplicate-or-overlap`
  - Evidence: RNMBF is exactly abs(NMBF-1), while runtime NMBF is the unrestricted raw mean ratio.
  - Impact: It overlaps RMBF on positive means but inherits a different domain policy.
  - Recommended future action: Cross-reference RNMBF, RMBF, and NMBF and document their domain distinction.

<a id="metric-cpi"></a>
### `CPI` — Combined Performance Index

- Registered method: `cpi`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: [0, infinity) for finite ordinary inputs
- Ideal value: 0

#### Implemented behavior

- Formula: (KSI(normed=False)+OVER(normed=False)+2*RMSE)/4.
- Preprocessing:
  - Convert, flatten, and drop nonfinite pairs.
  - Evaluate KSI and OVER on the pooled empirical-CDF grid.
- Dependencies:
  - ksi(normed=False)
  - over_metric(normed=False)
  - root_mean_squared_error

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: Unnormalized dependencies avoid their normalization denominators; all-zero identical series return zero.
- Negative inputs: Accepted, but the component sum is scale- and unit-dependent.
- Constant series: Identical constants return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Published solar-resource CPI combines normalized-percentage KSI, OVER, and twice relative RMSD with weights 1:1:2.
- References:
  - [Site-adaptation of modeled solar radiation: Quality assessment and global performance index](https://doi.org/10.3390/rs12132127) — Fernández-Peruchena and coauthors (2020), primary. Supports: Defines CPI=(KSI+OVER+2 relRMSD)/4 with normalized components.
- Known variants:
  - Runtime preserves the weights but uses raw unit-bearing KSI, OVER, and RMSE.

#### Characterization and tests

- Ordinary case: Stubbed KSI=2, OVER=4, RMSE=3 yields CPI=(2+4+6)/4=3 and proves both distribution components receive normed=False.
- Edge case: Identical all-zero and identical nonzero constant series yield zero because all three unnormalized dependencies are zero.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_cpi_is_unscaled_average_of_ksi_over_and_double_rmse
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Published CPI uses normalized KSI/OVER and relative RMSD; runtime explicitly requests raw KSI/OVER and raw RMSE.
  - Impact: Runtime CPI has data units and is not comparable to the published percentage index.
  - Recommended future action: Document the raw-unit variant and dependency settings before considering any separately approved change.

<a id="metric-red"></a>
### `RED` — Relative Euclidean Distance

- Registered method: `red`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity) or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: sqrt(mean(((prediction-observation)/observation)^2)) over nonzero observations.
- Preprocessing:
  - Drop nonfinite pairs.
  - Replace zero observations with NaN before Bottleneck nanmean.
- Dependencies:
  - Bottleneck nanmean
  - NumPy sqrt

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs and zero-observation ratios are omitted.
- Zero inputs or denominators: Zero-observation pairs are omitted; all-zero observations return NaN.
- Negative inputs: Accepted; squaring removes ratio sign.
- Constant series: Finite for a nonzero observation constant; zero observations return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Published forecast-evaluation RED combines relative discrepancies in mean, standard deviation, and correlation in quadrature.
- References:
  - [Solar Forecast Arbiter metric documentation](https://forecastarbiter.epri.com/metrics/) — Electric Power Research Institute (2026), authoritative. Supports: Defines RED from mean bias, spread difference, and correlation components.
- Known variants:
  - Runtime instead computes RMS pointwise relative error.

#### Characterization and tests

- Ordinary case: [2,6] versus [1,3] has two relative errors of one and RED 1.
- Edge case: With one zero observation that pair is omitted; if all observations are zero RED is NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_7.py::test_zero_observations_are_omitted_from_red_mpe_and_mape

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime computes RMS pointwise relative error; the cited EPRI RED instead takes the quadrature of normalized mean difference, normalized spread difference, and correlation discrepancy.
  - Impact: Runtime measures paired pointwise relative residuals, while cited RED summarizes differences in mean, variability, and association; their values and interpretation are not interchangeable.
  - Recommended future action: Document the exact RMS-relative formula or rename before any runtime change.

<a id="metric-fom"></a>
### `FoM` — Figure of Merit

- Registered method: `figure_of_merit`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: nominally [0, 100] for nonnegative inputs; otherwise unbounded or NaN
- Ideal value: 100

#### Implemented behavior

- Formula: 100*sum(min(observation,prediction))/sum(max(observation,prediction)).
- Preprocessing:
  - Drop nonfinite pairs.
  - Compute elementwise overlap, false-negative, and false-positive areas.
- Dependencies:
  - NumPy minimum and maximum
  - Bottleneck nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: All-zero inputs produce NaN.
- Negative inputs: Accepted but violate the area interpretation and can leave the nominal range.
- Constant series: Positive constants return the smaller/larger ratio times 100.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: For nonnegative spatial fields, figure of merit in space is intersection area divided by union area, commonly expressed as a percentage.
- References:
  - [Use of two-dimensional measures of effectiveness for the evaluation of regional-scale models](https://doi.org/10.1175/1520-0450(2004)043%3C0058:UOTDMO%3E2.0.CO;2) — Warner and coauthors (2004), primary. Supports: Defines intersection-over-union Figure of Merit in Space and discusses concentration-weighted generalization.
- Known variants:
  - Binary-set overlap and continuous nonnegative min/max overlap are distinct variants.

#### Characterization and tests

- Ordinary case: [1,1,4] versus [1,3,2] has min sum 4 and max sum 8, giving 50 percent.
- Edge case: All-zero fields have a zero union and return NaN; signed constants [-3,-3] versus [-3,-2] return 120, outside the nominal range.
- Existing tests:
  - tests/test_error_metrics.py::test_additional_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Negative values are accepted although the min/max overlap is only bounded and area-like for nonnegative fields.
  - Impact: FoM may be outside 0-100 or misleading for signed data.
  - Recommended future action: Document the nonnegative domain and consider separate validation approval.

<a id="metric-msddec"></a>
### `MSDdec` — MSD Decomposition

- Registered method: `msd_decomposition`
- Category: diagnostic and decomposition
- Return shape: 4-tuple (MSD, SB, NU, LC)
- Implemented range: four nominally nonnegative scalars; components may be NaN
- Ideal value: (0, 0, 0, 0)

#### Implemented behavior

- Formula: MSD=mean(error^2); SB=mean(error)^2; NU=(1-slope(observation on prediction))^2*variance(prediction); LC=(1-R2)*variance(observation).
- Preprocessing:
  - Drop nonfinite pairs.
  - Fit observation as a linear function of prediction with intercept.
- Dependencies:
  - msd
  - sb
  - nu
  - lc
  - linear_regression

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: Perfect all-zero series have MSD and SB zero but regression-derived components NaN.
- Negative inputs: Accepted.
- Constant series: Constant predictions make slope and R2 undefined, so NU and LC are NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Gauch and coauthors decompose mean squared deviation into squared bias, nonunity slope, and lack-of-correlation components that add to MSD.
- References:
  - [Model evaluation by comparison of model-based predictions and measured values](https://doi.org/10.2134/agronj2003.1442) — Gauch, Hwang, and Fick (2003), primary. Supports: Defines the three-component MSD decomposition and additivity.
- Known variants:
  - Regression orientation and component labels must be explicit; runtime regresses observation on prediction.

#### Characterization and tests

- Ordinary case: [1,3,5] versus [2,3,4] returns (2/3,0,2/3,0), in the documented tuple order and with additive components.
- Edge case: Constant predictions [2,2,2] leave NU and LC undefined while MSD=2/3 and SB=0 remain finite.
- Existing tests:
  - tests/test_error_metrics.py::test_msd_decomposition
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_msd_decomposition_returns_runtime_components_in_documented_tuple_order
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The tuple exposes four unlabeled positional scalars and regression orientation is only discoverable from helper code.
  - Impact: Callers can transpose component meaning or compare against the reciprocal regression convention.
  - Recommended future action: Document tuple order and observation-on-prediction regression orientation prominently.

<a id="metric-ss"></a>
### `SS` — Skill Score vs Climatology

- Registered method: `skill_score_against_climatology`
- Category: efficiency and environmental evaluation
- Return shape: scalar
- Implemented range: (-infinity, 1] or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1-sum((prediction-observation)^2)/sum((observation-mean(observation))^2).
- Preprocessing:
  - Drop nonfinite pairs.
  - Construct in-sample observation-mean climatology.
- Dependencies:
  - Bottleneck nanmean and nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed before climatology.
- Zero inputs or denominators: Constant observations give zero climatology error and return NaN.
- Negative inputs: Accepted.
- Constant series: Constant observations make the score undefined, including perfect constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: A skill score compares forecast score to a reference score as 1-score_forecast/score_reference; with squared error and mean climatology this equals Nash-Sutcliffe efficiency.
- References:
  - [River flow forecasting through conceptual models part I — A discussion of principles](https://doi.org/10.1016/0022-1694(70)90255-6) — Nash and Sutcliffe (1970), primary. Supports: Defines the same squared-error ratio against deviations from the observed mean.
- Known variants:
  - Forecast skill scores may use out-of-sample or seasonal climatology and other proper scores.

#### Characterization and tests

- Ordinary case: [1,2,6] versus [1,3,5] has squared error 2 and climatology squared error 8, giving 0.75.
- Edge case: A constant observation series has zero climatology denominator and returns NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_additional_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_skill_score_uses_observation_mean_climatology_and_squared_error

#### Findings and recommended future action

- `duplicate-or-overlap`
  - Evidence: Runtime SS is algebraically identical to registered NSE on the same filtered pairs.
  - Impact: Two registry identities expose the same calculation without explaining the overlap.
  - Recommended future action: Cross-reference SS and NSE and distinguish generic skill-score terminology from this implementation.

<a id="metric-ad"></a>
### `AD` — Anderson-Darling Distance

- Registered method: `anderson_darling_distance`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: sum((F_obs(x)-F_pred(x))^2/(F_obs(x)*(1-F_obs(x))+1e-10)) over pooled unique sample values.
- Preprocessing:
  - Drop nonfinite pairs.
  - Build right-continuous empirical CDFs and evaluate at pooled unique values.
- Dependencies:
  - Statsmodels ECDF
  - NumPy unique and sort

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: A fixed 1e-10 stabilizer replaces zero tail denominators.
- Negative inputs: Accepted as ordered sample values.
- Constant series: Identical constants return zero; separated constants can produce about 1e10.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The k-sample Anderson-Darling statistic is a rank-based, sample-size-normalized integral of squared ECDF differences weighted by a pooled distribution denominator.
- References:
  - [A k-sample Anderson-Darling test](https://doi.org/10.1080/01621459.1987.10478517) — Scholz and Stephens (1987), primary. Supports: Defines the symmetric pooled-distribution k-sample Anderson-Darling statistic.
- Known variants:
  - Runtime weights only by observation ECDF, uses an unscaled grid sum, and is directional rather than the symmetric k-sample statistic.

#### Characterization and tests

- Ordinary case: [0,1,3] versus [0,2,4] returns approximately 1 from two nonzero pooled-grid contributions of approximately 0.5 each.
- Edge case: Swapping prediction and observation changes the weights and produces a value above 1e8; separated constants return approximately 1e10.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_ad_is_directional_and_uses_observation_ecdf_for_weights
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Runtime is directional and lacks pooled-CDF integration and sample-size normalization used by the named k-sample Anderson-Darling statistic.
  - Impact: Magnitude and even symmetry differ from standard AD two-sample interpretations.
  - Recommended future action: Confirm whether a custom distance was intended; otherwise consider a separately approved canonical implementation or rename.

<a id="metric-kld"></a>
### `KLD` — Kullback-Leibler Divergence

- Registered method: `kullback_leibler_divergence`
- Category: distribution and statistical comparison
- Return shape: scalar
- Implemented range: [0, infinity] in the probability domain; all-zero inputs return 0
- Ideal value: 0

#### Implemented behavior

- Formula: sum(rel_entr(abs(observation)/sum(abs(observation)), abs(prediction)/sum(abs(prediction)))).
- Preprocessing:
  - Drop nonfinite pairs.
  - Take absolute element magnitudes and independently normalize each vector to unit sum.
- Dependencies:
  - SciPy special.rel_entr
  - Bottleneck nansum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs are removed; NaN terms from zero-sum normalization are suppressed by nansum.
- Zero inputs or denominators: Positive observation mass where prediction mass is zero yields infinity; both all-zero vectors return 0.
- Negative inputs: Signs are discarded before normalization.
- Constant series: Nonzero constants normalize uniformly and return zero even when magnitudes differ.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Relative entropy D(P||Q)=sum P log(P/Q) is directional and defined for probability distributions, with infinite divergence where P has mass and Q has none.
- References:
  - [On information and sufficiency](https://doi.org/10.1214/aoms/1177729694) — Kullback and Leibler (1951), primary. Supports: Introduces the directional information divergence.
  - [scipy.special.rel_entr documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.rel_entr.html) — SciPy developers (2026), authoritative. Supports: Defines elementwise x*log(x/y) and boundary behavior used by runtime.
- Known variants:
  - Raw samples normally require density estimation or binning before KLD; runtime treats array positions as categories and discards signs.

#### Characterization and tests

- Ordinary case: Absolute prediction [1,3] and observation [2,2] normalize to Q=[.25,.75], P=[.5,.5], giving .5 ln 2 + .5 ln(2/3).
- Edge case: Observation mass aligned with zero prediction mass produces +infinity; both all-zero arrays normalize to NaNs whose nansum is 0.
- Existing tests:
  - tests/test_error_metrics.py::test_distribution_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_kld_normalizes_absolute_magnitudes_and_orders_observations_first
  - tests/audit/test_characterization_batch_7.py::test_reviewed_edge_behaviors_are_executable

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Runtime silently converts signed arbitrary vectors to categorical distributions by absolute value and normalization; zero-sum NaNs collapse to zero.
  - Impact: Distinct invalid/undefined inputs can appear identical, and ordering semantics are easy to misread.
  - Recommended future action: Document D(observation||prediction), positional-category semantics, absolute conversion, and zero-sum behavior.

<a id="metric-mpe"></a>
### `MPE` — Mean Percentage Error

- Registered method: `mean_percentage_error`
- Category: percentage error
- Return shape: scalar
- Implemented range: unbounded signed percentage or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 100*mean((prediction-observation)/observation) over nonzero observations.
- Preprocessing:
  - Drop nonfinite pairs.
  - Replace exactly zero observations with NaN and omit those ratios.
- Dependencies:
  - NumPy where
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed and zero-observation ratios omitted.
- Zero inputs or denominators: Zero observations are omitted; all-zero observations return NaN.
- Negative inputs: Accepted; denominator sign affects error direction.
- Constant series: Returns the constant relative bias percentage when observation is nonzero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Mean percentage error averages signed forecast error divided by actual value and is undefined when an actual value is zero.
- References:
  - [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001) — Hyndman and Koehler (2006), primary. Supports: Reviews percentage-error measures and their degeneracy at zero actual values.
- Known variants:
  - Libraries may raise, return infinity, add an epsilon, or omit zero actuals; runtime omits them.

#### Characterization and tests

- Ordinary case: Two 100-percent overpredictions average to MPE 100.
- Edge case: For [100,4,1] versus [0,2,2], the zero-observation pair is omitted and (+100%-50%)/2=25%; all-zero observations return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_percentage_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_7.py::test_zero_observations_are_omitted_from_red_mpe_and_mape

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime omits zero-observation cases from both numerator and effective count without documenting that sample-dependent policy.
  - Impact: Large errors at zeros disappear and results may look better as zero frequency rises.
  - Recommended future action: Document omission and effective sample behavior.

<a id="metric-mape"></a>
### `MAPE` — Mean Absolute Percentage Error

- Registered method: `mean_absolute_percentage_error`
- Category: percentage error
- Return shape: scalar
- Implemented range: [0, infinity) percentage or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 100*mean(abs((prediction-observation)/observation)) over nonzero observations.
- Preprocessing:
  - Drop nonfinite pairs.
  - Replace exactly zero observations with NaN and omit those ratios.
- Dependencies:
  - NumPy where and abs
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed and zero-observation ratios omitted.
- Zero inputs or denominators: Zero observations are omitted; all-zero observations return NaN.
- Negative inputs: Accepted; absolute value makes each contribution nonnegative but negative actuals retain magnitude scaling.
- Constant series: Returns the absolute constant relative error percentage when observation is nonzero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: MAPE is the arithmetic mean of absolute errors divided by actual values, usually multiplied by 100; it is undefined for zero actuals and asymmetric under over/underforecasting.
- References:
  - [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001) — Hyndman and Koehler (2006), primary. Supports: Reviews MAPE, its zero-value undefinedness, and asymmetry limitations.
- Known variants:
  - Zero actuals may be rejected, omitted, epsilon-clipped, or handled by symmetric alternatives; runtime omits them.

#### Characterization and tests

- Ordinary case: Two 100-percent overpredictions give MAPE 100.
- Edge case: For [100,4,1] versus [0,2,2], the zero-observation pair is omitted and (100%+50%)/2=75%; all-zero observations return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_percentage_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_7.py::test_bias_distance_overlap_and_percentage_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_7.py::test_zero_observations_are_omitted_from_red_mpe_and_mape

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime silently omits zero actuals rather than treating canonical MAPE as undefined for the dataset.
  - Impact: Errors at zeros are invisible and the averaging population changes.
  - Recommended future action: Document zero omission and MAPE's asymmetry; consider explicit policy only in a separately approved runtime change.

<a id="metric-smape"></a>
### `sMAPE` — Symmetric Mean Absolute Percentage Error

- Registered method: `symmetric_mean_absolute_percentage_error`
- Category: percentage error
- Return shape: scalar
- Implemented range: [0, 200] percentage or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: 100*mean(|prediction-observation|/((|observation|+|prediction|)/2)), omitting zero denominators.
- Preprocessing:
  - Drop nonfinite pairs.
  - Replace pairs where both values are zero with NaN contributions.
- Dependencies:
  - NumPy abs and where
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: Pairs that are both zero are omitted; an all-zero pair set returns NaN.
- Negative inputs: Accepted; absolute magnitudes keep each finite contribution in [0,2].
- Constant series: Equal nonzero constants return zero; unequal constants return their symmetric percentage difference.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The common sMAPE form averages 2|forecast-actual|/(|actual|+|forecast|), usually as a percentage, but published naming and scaling conventions vary.
- References:
  - [The M3-Competition: results, conclusions and implications](https://doi.org/10.1016/S0169-2070(00)00057-1) — Makridakis and Hibon (2000), primary. Supports: Uses symmetric absolute percentage error in forecast-comparison practice.
- Known variants:
  - Factors of 100 versus 200 and signed versus absolute denominators occur in the literature.
  - Undefined 0/0 pairs may be rejected, assigned zero, or omitted; runtime omits them.

#### Characterization and tests

- Ordinary case: [2,4] versus [1,3] gives 100*((1/1.5)+(1/3.5))/2 = 47.6190476.
- Edge case: Two all-zero pairs have only omitted 0/0 contributions and return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_metrics_not_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime silently omits pairs where prediction and observation are both zero.
  - Impact: The effective sample count changes and perfect zero forecasts do not contribute zero error; an all-zero perfect series returns NaN.
  - Recommended future action: Document the zero-pair policy and exact 0-200 scaling.

<a id="metric-crps"></a>
### `CRPS` — Continuous Ranked Probability Score

- Registered method: `continuous_ranked_probability_score`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: mean(|prediction-observation|); deterministic CRPS is delegated exactly to MAE.
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - mean_absolute_error

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: All-zero finite pairs return zero.
- Negative inputs: Accepted.
- Constant series: Returns the absolute difference between constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: CRPS is the integral over thresholds of the squared difference between a predictive CDF and the observation step CDF; for a point-mass forecast it equals absolute error.
- References:
  - [Strictly proper scoring rules, prediction, and estimation](https://doi.org/10.1198/016214506000001437) — Gneiting and Raftery (2007), primary. Supports: Defines CRPS and its deterministic absolute-error reduction.
- Known variants:
  - Ensemble and parametric-distribution CRPS require forecast-distribution input not represented by this API.

#### Characterization and tests

- Ordinary case: Deterministic forecasts [2,4] versus [1,3] reduce to MAE=(1+1)/2=1.
- Edge case: Identical all-zero deterministic forecasts return zero.
- Existing tests:
  - tests/test_error_metrics.py::test_metrics_not_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The registered probabilistic name accepts only one scalar prediction per observation and computes MAE.
  - Impact: Users cannot evaluate ensemble or distribution forecasts and may infer probabilistic support that is absent.
  - Recommended future action: Document that this is deterministic point-mass CRPS only.

<a id="metric-tacc"></a>
### `TAcc` — Trend Accuracy

- Registered method: `trend_accuracy`
- Category: trend and direction
- Return shape: scalar
- Implemented range: unbounded signed scalar
- Ideal value: 1

#### Implemented behavior

- Formula: 1-|OLS slope(observation on index)-OLS slope(prediction on index)|/(|observation slope|+1e-10).
- Preprocessing:
  - Drop nonfinite pairs and compress the remaining sample index.
  - Fit independent degree-one polynomials against indices 0..N-1.
- Dependencies:
  - NumPy polyfit

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed and a RuntimeWarning explains index compression.
- Zero inputs or denominators: A fixed 1e-10 stabilizer makes equal flat zero trends return one but nonflat predictions against flat observations extremely negative.
- Negative inputs: Accepted; only slopes affect the result.
- Constant series: Equal constants return near/exact one; unequal fitted roundoff can perturb one; a varying prediction against constant observations can be about -1e10.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: No primary source was located for this exact registered name and relative slope-difference formula.
- References:
  - [numpy.polyfit documentation](https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html) — NumPy developers (2026), authoritative. Supports: Defines the least-squares polynomial slope calculation used by runtime.
- Known variants:
  - Trend or direction accuracy commonly compares signs of successive changes rather than relative fitted slopes.

#### Characterization and tests

- Ordinary case: [2,4] and [1,3] both have fitted slope 2, giving one.
- Edge case: One remaining pair makes polyfit fail; a nonzero prediction slope divided by a zero observation slope plus 1e-10 produces a huge negative score.
- Existing tests:
  - tests/test_v2_robustness.py::test_order_sensitive_metrics_warn_when_filtering_compresses_index
  - tests/test_error_metrics.py::test_metrics_not_nan
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors
  - tests/audit/test_characterization_batch_8.py::test_nonfinite_pairs_are_removed_and_empty_filtered_data_is_rejected

#### Findings and recommended future action

- `possible-defect`
  - Evidence: The 1e-10 stabilizer makes a varying forecast against a flat observation trend return roughly -1e10, and one-point input reaches a low-level polyfit failure.
  - Impact: The score is numerically unstable near a zero observed slope and short inputs fail unclearly.
  - Recommended future action: Define the intended zero-trend and minimum-length policy before a separately approved runtime fix.
- `documentation-gap`
  - Evidence: No source for the exact formula was located.
  - Impact: Its scientific identity and interpretation are unclear.
  - Recommended future action: Document the formula as a fitted-slope similarity and source it if possible.

<a id="metric-u2"></a>
### `U2` — Theil's Inequality Coefficient

- Registered method: `theils_u2`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity) or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: RMSE(prediction,observation)/sqrt(mean(observation^2)).
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - root_mean_squared_error
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: An all-zero observation RMS returns NaN.
- Negative inputs: Accepted; squares remove signs from normalization.
- Constant series: Defined for nonzero constant observations; all-zero observations are undefined.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Theil's U2 normally compares forecast RMSE with a naive no-change forecast RMSE, where one denotes parity with the naive forecast.
- References:
  - [Applied Economic Forecasting](https://archive.org/details/appliedeconomicf0000thei) — Henri Theil (1966), primary. Supports: Introduces Theil inequality coefficients for forecast evaluation.
- Known variants:
  - The implemented RMSE divided by observation RMS is commonly associated with a normalized RMSE/Theil U1 component, not the lagged-naive U2 benchmark.

#### Characterization and tests

- Ordinary case: [2,4] versus [1,3] has RMSE 1 and observation RMS sqrt(5), giving 1/sqrt(5).
- Edge case: All-zero observations have zero RMS and return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_theils_u2_and_berry_mielke
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime normalizes by observation RMS rather than by the error of a lagged naive forecast.
  - Impact: Zero and one do not carry canonical U2's naive-benchmark interpretation.
  - Recommended future action: Rename or document the implemented normalized RMSE; change behavior only with compatibility approval.

<a id="metric-bm"></a>
### `BM` — Berry-Mielke Index

- Registered method: `berry_mielke_score`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: unbounded below through 1, or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 1-mean(|paired prediction-observation|)/((c/N^2)*sum_ij|prediction_j-observation_i|).
- Preprocessing:
  - Drop nonfinite pairs.
  - Construct the full N by N cross-distance matrix.
- Dependencies:
  - NumPy subtract.outer
  - Bottleneck nanmean

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `c` | `2.0` | Numeric values supporting multiplication and division | None; the scientifically supported default is not enforced. | Zero makes mu zero and returns NaN; negative values can produce scores above one; incompatible values raise TypeError. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: Zero cross-distance mu, including identical constants or c=0, returns NaN.
- Negative inputs: Accepted because distances are absolute.
- Constant series: Identical constants return NaN; unequal constants return 1-1/c.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Berry-Mielke agreement compares paired absolute disagreement with expected disagreement from all cross-pairs, using the conventional factor two.
- References:
  - [A generalization of Cohen's kappa agreement measure to interval measurement and multiple raters](https://doi.org/10.1177/0013164488484007) — Berry and Mielke (1988), primary. Supports: Develops the interval-scale agreement measure based on observed and expected disagreement.
- Known variants:
  - Distance powers and multi-rater formulations vary; runtime exposes the conventional factor as arbitrary parameter c.

#### Characterization and tests

- Ordinary case: [2,4] versus [1,3] has paired delta 1 and cross-distance sum 6; c=2 gives mu=3 and score 2/3.
- Edge case: c=0 or identical constant series makes mu zero and returns NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_theils_u2_and_berry_mielke
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_berry_mielke_uses_cross_distance_matrix_and_parameter_c
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `validation-gap`
  - Evidence: Any c is accepted even though nonpositive values destroy the agreement-scale interpretation.
  - Impact: c=0 returns NaN and negative c can produce scores above one.
  - Recommended future action: Document c=2 as the scientifically supported setting and consider positive-value validation separately.

<a id="metric-dcor"></a>
### `dCor` — Distance Correlation

- Registered method: `distance_correlation`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: [0, 1] or NaN
- Ideal value: 1 for perfect dependence; 0 for zero sample distance variance

#### Implemented behavior

- Formula: Biased sample distance correlation from double-centered pairwise Euclidean distance matrices.
- Preprocessing:
  - Drop nonfinite pairs.
  - Build N by N scalar Euclidean distance matrices and double-center each with row and grand means.
- Dependencies:
  - SciPy pdist and squareform
  - NumPy mean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: If either centered distance variance is zero, return zero.
- Negative inputs: Accepted; Euclidean distances are translation and reflection invariant.
- Constant series: Returns zero if either series is constant, including two identical constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Distance correlation normalizes distance covariance by the two distance variances and detects general dependence; the empirical biased version uses double-centered pairwise distance matrices.
- References:
  - [Measuring and testing dependence by correlation of distances](https://doi.org/10.1214/009053607000000505) — Székely, Rizzo, and Bakirov (2007), primary. Supports: Introduces distance covariance/correlation and empirical distance-matrix computation.
- Known variants:
  - Bias-corrected/U-centered estimators differ at finite sample sizes.

#### Characterization and tests

- Ordinary case: For [0,1,4] versus [0,1,2], the test independently double-centers both 3x3 distance matrices and reproduces runtime normalization.
- Edge case: One pair returns NaN by explicit length guard; any constant input at length at least two returns zero.
- Existing tests:
  - tests/test_error_metrics.py::test_distance_correlation_metric
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_distance_correlation_matches_biased_double_centered_distance_matrices
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime uses the biased empirical estimator and returns zero for degenerate constant inputs without identifying the estimator convention.
  - Impact: Finite-sample values differ from unbiased variants and zero does not establish independence for a constant variable.
  - Recommended future action: Document biased double-centering and constant-series semantics.

<a id="metric-lambda"></a>
### `lambda` — Duveiller Agreement Coefficient

- Registered method: `duveiller_agreement_coefficient`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: nominally [-1, 1] with runtime roundoff possible
- Ideal value: 1

#### Implemented behavior

- Formula: 1-MSE/(population variance(observation)+population variance(prediction)+(mean(observation)-mean(prediction))^2).
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: If the entire denominator is exactly zero, return one.
- Negative inputs: Accepted; common translation and sign reversal preserve agreement.
- Constant series: Equal constants return one; unequal constants return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Duveiller's corrected symmetric lambda adds a nonnegative-covariance correction kappa to the variance-and-bias denominator, making lambda equal CCC for nonnegative covariance and zero rather than negative for negative covariance.
- References:
  - [Revisiting the concept of a symmetric index of agreement for continuous datasets](https://doi.org/10.1038/srep19401) — Duveiller, Fasbender, and Meroni (2016), primary. Supports: Defines the symmetric lambda agreement coefficient including the negative-covariance correction.
  - [Author Correction: Revisiting the concept of a symmetric index of agreement for continuous datasets](https://doi.org/10.1038/s41598-022-23771-z) — Duveiller, Fasbender, and Meroni (2022), primary. Supports: Corrects the published kappa equation and confirms that kappa is not divided by sample size.
- Known variants:
  - Runtime omits kappa and is algebraically Lin's CCC when its denominator is nonzero.

#### Characterization and tests

- Ordinary case: [1,3,5] versus [2,3,4] has MSE 2/3, variance sum 10/3, zero bias, and lambda 0.8.
- Edge case: Perfect negative association [1,2,3] versus [3,2,1] returns -1 rather than corrected lambda zero; identical constants return one.
- Existing tests:
  - tests/test_error_metrics.py::test_duveiller_agreement_coefficient
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_duveiller_coefficient_uses_population_variances_and_bias
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime omits Duveiller's kappa correction and therefore equals CCC; perfect negative association returns -1 while corrected lambda is zero.
  - Impact: Negative-covariance datasets leave canonical lambda's [0,1] range and have a different interpretation.
  - Recommended future action: Document the CCC-like runtime formula and consider the corrected coefficient only as a separately approved compatibility change.

<a id="metric-iqrmse"></a>
### `iqRMSE` — Inter-Quartile RMSE

- Registered method: `interquartile_rmse`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity]
- Ideal value: 0

#### Implemented behavior

- Formula: RMSE/(75th percentile(observation)-25th percentile(observation)).
- Preprocessing:
  - Drop nonfinite pairs.
  - Use NumPy's default linear percentile interpolation.
- Dependencies:
  - root_mean_squared_error
  - NumPy percentile

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: A zero observation IQR returns positive infinity even when RMSE is zero.
- Negative inputs: Accepted; IQR is translation invariant and nonnegative.
- Constant series: Always returns infinity for constant observations, including perfect constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: iqRMSE normalizes root mean squared error by the observed interquartile range to provide a robust scale-relative error.
- References:
  - [The power of machine learning to predict crop yields and nitrogen losses](https://doi.org/10.1016/j.agsy.2021.103194) — Correndo and coauthors (2021), primary. Supports: Reports interquartile-range-normalized RMSE among model evaluation metrics.
- Known variants:
  - Quantile interpolation conventions differ for small samples.
  - Undefined zero-IQR cases may return NaN rather than infinity.

#### Characterization and tests

- Ordinary case: For [2,4] versus [1,3], RMSE is 1 and NumPy's two-point IQR is 1, giving one.
- Edge case: Constant observations have IQR zero and return infinity, including a perfect all-zero forecast.
- Existing tests:
  - tests/test_error_metrics.py::test_interquartile_rmse
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_percentage_probabilistic_trend_and_scale_metrics_match_hand_calculations
  - tests/audit/test_characterization_batch_8.py::test_zero_short_constant_and_regression_failure_behaviors

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Runtime returns infinity for 0/0 when both RMSE and observed IQR are zero.
  - Impact: A perfect constant forecast is reported as infinitely bad rather than undefined or perfect.
  - Recommended future action: Specify zero-IQR semantics before any separately approved runtime change.

<a id="metric-sma"></a>
### `SMA` — SMA Regression Metrics

- Registered method: `sma_metrics`
- Category: diagnostic and decomposition
- Return shape: 7-tuple (slope, intercept, MSE, MLA, MLP, PLA%, PLP%)
- Implemented range: mixed signed/nonnegative components; NaNs possible
- Ideal value: (1, 0, 0, 0, 0, 0, 0) for a perfect nonconstant fit

#### Implemented behavior

- Formula: slope=sign(r)*population SD(prediction)/population SD(observation); intercept=mean(prediction)-slope*mean(observation); MLA=(mean difference)^2+(SD difference)^2; MLP=2*SDpred*SDobs*(1-r); percentages divide each component by MSE.
- Preprocessing:
  - Drop nonfinite pairs.
  - Replace NaN Pearson correlation with zero.
  - Replace zero observation SD slope with zero.
- Dependencies:
  - correlation_coefficient
  - Bottleneck nanmean and nanstd

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed; NaN correlation is replaced by zero, though underlying calculation may warn.
- Zero inputs or denominators: Perfect zero data return seven zeros, including slope zero rather than one.
- Negative inputs: Accepted; correlation sign controls slope sign.
- Constant series: Constant observations force slope zero; constant-series correlation becomes zero; component percentages can remain finite.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Standardized major axis regression uses the sign of correlation times the response-to-predictor standard-deviation ratio; the reported MLA/MLP decomposition separates accuracy and precision contributions to MSE.
- References:
  - [The power of machine learning to predict crop yields and nitrogen losses](https://doi.org/10.1016/j.agsy.2021.103194) — Correndo and coauthors (2021), primary. Supports: Uses SMA-based accuracy/precision decomposition for model evaluation.
- Known variants:
  - Regression orientation determines which standard-deviation ratio is the slope; runtime models prediction as a function of observation.

#### Characterization and tests

- Ordinary case: [1,3,5] versus [2,3,4] returns (2,-3,2/3,2/3,0,100,0), and MLA+MLP=MSE.
- Edge case: Constant predictions 2 versus constant observations 1 return (0,2,1,1,0,100,0) after replacing undefined correlation with zero.
- Existing tests:
  - tests/test_error_metrics.py::test_sma_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_sma_tuple_order_and_component_meanings_are_executable
  - tests/audit/test_characterization_batch_8.py::test_constant_regression_and_rnp_components_preserve_runtime_nans

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Seven positional components, regression orientation, population SD convention, and NaN-correlation replacement are not exposed by the registry description.
  - Impact: Callers can transpose slope orientation or tuple meanings and miss constant-series substitution.
  - Recommended future action: Document tuple order and degeneracy policy prominently.

<a id="metric-rnp"></a>
### `RNP` — Non-parametric KGE

- Registered method: `rnp`
- Category: efficiency and environmental evaluation
- Return shape: 4-tuple (RNP, Spearman r, FDC alpha, mean-ratio beta)
- Implemented range: score unbounded below through 1; components may be NaN
- Ideal value: (1, 1, 1, 1)

#### Implemented behavior

- Formula: alpha=1-0.5*sum(|sort(pred/(mean(pred)*N))-sort(obs/(mean(obs)*N))|); beta=mean(pred)/mean(obs); r=Spearman(pred,obs); RNP=1-Euclidean distance of (alpha,beta,r) from (1,1,1).
- Preprocessing:
  - Drop nonfinite pairs.
  - Sort separately normalized flow-duration vectors for alpha while retaining original pairing for Spearman correlation.
- Dependencies:
  - SciPy spearmanr
  - Bottleneck nanmean and nansum
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: A zero mean makes its normalized FDC and beta undefined; nansum can still make alpha equal one.
- Negative inputs: Accepted algebraically, though zero/canceling means remain singular.
- Constant series: Spearman r and overall RNP are NaN; alpha can be one and beta finite.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Non-parametric KGE combines Spearman rank correlation, normalized flow-duration-curve similarity, and mean-flow bias in Euclidean component space.
- References:
  - [A simple and objective method for selecting rainfall-runoff model evaluation criteria](https://doi.org/10.1080/02626667.2018.1552002) — Pool, Vis, Knight, and Seibert (2018), primary. Supports: Defines the non-parametric KGE components based on Spearman correlation, flow-duration curves, and bias.
- Known variants:
  - Component labels and ordering differ across software; runtime returns score, r, alpha, beta.

#### Characterization and tests

- Ordinary case: [2,4] versus [1,3] returns r=1, alpha=11/12, beta=3/2, then score 1-sqrt((alpha-1)^2+(beta-1)^2).
- Edge case: Unequal positive constants produce alpha one and finite beta but Spearman r and the overall score are NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_8.py::test_rnp_tuple_order_and_flow_duration_component_match_hand_calculation
  - tests/audit/test_characterization_batch_8.py::test_constant_regression_and_rnp_components_preserve_runtime_nans

#### Findings and recommended future action

- `test-gap`
  - Evidence: No pre-audit test directly exercised RNP or its four-component tuple.
  - Impact: Component order, normalized FDC arithmetic, and degeneracies could regress unnoticed.
  - Recommended future action: Retain the characterization tests and document tuple component order.
- `validation-gap`
  - Evidence: Zero-mean normalization yields NaNs that nansum can convert into alpha=1 while beta and the score remain NaN.
  - Impact: The component tuple mixes a misleading perfect alpha with undefined components.
  - Recommended future action: Document positive nonzero-mean domain and define validation separately.

<a id="metric-tss"></a>
### `TSS` — Taylor Skill Score

- Registered method: `taylor_skill_score`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: nominally [0, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: 4*(1+r)^4 / (((1/std_ratio)+std_ratio)^2*(1+1)^4), where std_ratio=population SD(prediction)/population SD(observation).
- Preprocessing:
  - Drop nonfinite pairs.
  - Use Pearson correlation and population standard deviations.
- Dependencies:
  - correlation_coefficient
  - NumPy std
  - _safe_divide

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: A zero standard deviation makes the ratio or its reciprocal undefined and returns NaN.
- Negative inputs: Accepted; common translation does not change the score.
- Constant series: Returns NaN when either series is constant because the correlation and/or SD ratio is undefined.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Taylor's skill score combines pattern correlation and the ratio of modeled to observed standard deviations; the reference correlation is commonly set to one.
- References:
  - [Summarizing multiple aspects of model performance in a single diagram](https://doi.org/10.1029/2000JD900719) — Karl E. Taylor (2001), primary. Supports: Introduces the skill score based on correlation and relative standard deviation alongside the Taylor diagram.
- Known variants:
  - The exponent on the correlation term and the reference correlation can be configured in generalized forms; runtime fixes exponent four and reference correlation one.

#### Characterization and tests

- Ordinary case: For predictions [2,4,6] and observations [1,2,3], r=1 and SD ratio=2, giving 4/(2.5^2)=0.64.
- Edge case: Either constant series makes correlation or the standard-deviation ratio undefined and returns NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_advanced_metrics
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_taylor_skill_score_uses_correlation_and_population_standard_deviation_ratio

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime fixes the Taylor-score exponent and reference correlation without exposing those conventions.
  - Impact: Values cannot be compared safely with generalized Taylor skill-score variants unless conventions are known.
  - Recommended future action: Document exponent four, reference correlation one, and population-SD behavior.

<a id="metric-mean"></a>
### `MEAN` — Mean Values

- Registered method: `meann`
- Category: distribution and statistical comparison
- Return shape: 2-tuple (observation mean, prediction mean)
- Implemented range: each component is any finite real value
- Ideal value: equal components

#### Implemented behavior

- Formula: Return (mean(observation), mean(prediction)).
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - Cached Bottleneck nanmean values

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: All-zero data return (0,0).
- Negative inputs: Accepted.
- Constant series: Returns the two constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The arithmetic mean is the sum of observations divided by their count.
- References:
  - [NIST/SEMATECH e-Handbook of Statistical Methods: Measures of Location](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm) — National Institute of Standards and Technology (2012), authoritative. Supports: Defines the sample mean as a measure of location and distinguishes it from the median.
- Known variants:
  - Weighted, geometric, and trimmed means are distinct summaries; runtime uses the unweighted arithmetic mean.

#### Characterization and tests

- Ordinary case: Predictions [2,4,9] and observations [1,5,6] return (4,5) in observation-first order.
- Edge case: Constant observations 1 and predictions 2 return (1,2).
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_summary_tuples_and_centered_error_match_hand_calculations

#### Findings and recommended future action

- `test-gap`
  - Evidence: No pre-audit test pinned the observation-first two-tuple order.
  - Impact: Callers could silently transpose the two summaries.
  - Recommended future action: Document and retain the tuple-order characterization.

<a id="metric-median"></a>
### `MEDIAN` — Median Values

- Registered method: `mediann`
- Category: distribution and statistical comparison
- Return shape: 2-tuple (observation median, prediction median)
- Implemented range: each component is any finite real value
- Ideal value: equal components

#### Implemented behavior

- Formula: Return (median(observation), median(prediction)).
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - Bottleneck nanmedian

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: All-zero data return (0,0).
- Negative inputs: Accepted.
- Constant series: Returns the two constants.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The median is the middle ordered value, averaging the two middle values for an even sample under the usual sample convention.
- References:
  - [NIST/SEMATECH e-Handbook of Statistical Methods: Measures of Location](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm) — National Institute of Standards and Technology (2012), authoritative. Supports: Defines the median as a robust measure of location.
- Known variants:
  - Even-sample and weighted-median conventions can differ; Bottleneck uses the average of the middle order statistics.

#### Characterization and tests

- Ordinary case: Predictions [2,4,9] and observations [1,5,6] return (5,4) in observation-first order.
- Edge case: Constant observations 1 and predictions 2 return (1,2).
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_summary_tuples_and_centered_error_match_hand_calculations

#### Findings and recommended future action

- `test-gap`
  - Evidence: No pre-audit test pinned the observation-first two-tuple order.
  - Impact: Callers could silently transpose the two summaries.
  - Recommended future action: Document and retain the tuple-order characterization.

<a id="metric-crmse"></a>
### `CRMSE` — Centered Root Mean Square

- Registered method: `centered_root_mean_square`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: sqrt(mean(((prediction-mean(prediction))-(observation-mean(observation)))^2)).
- Preprocessing:
  - Drop nonfinite pairs.
  - Center each series by its own arithmetic mean.
- Dependencies:
  - NumPy mean and sqrt

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: All-zero data return zero.
- Negative inputs: Accepted; independent additive offsets are removed by centering.
- Constant series: Any two constant series return zero even when their levels differ.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Centered RMS difference is the root mean square difference after removing each field's mean and measures centered-pattern disagreement.
- References:
  - [Summarizing multiple aspects of model performance in a single diagram](https://doi.org/10.1029/2000JD900719) — Karl E. Taylor (2001), primary. Supports: Defines centered RMS difference and its relationship to correlation and standard deviations.
- Known variants:
  - Sample-weighted spatial fields and degrees-of-freedom corrections are possible; runtime uses an unweighted population mean square.

#### Characterization and tests

- Ordinary case: For predictions [2,4,9] and observations [1,5,6], centered differences are [0,-2,2], giving sqrt(8/3).
- Edge case: Adding 10 to every prediction leaves CRMSE unchanged; unequal constants return zero.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_summary_tuples_and_centered_error_match_hand_calculations

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: The registered description does not explain that independent mean biases are removed.
  - Impact: A zero score can occur for predictions with an arbitrarily large constant offset.
  - Recommended future action: Document CRMSE as centered-pattern error and pair it with a bias summary.

<a id="metric-msle"></a>
### `MSLE` — Mean Squared Logarithmic Error

- Registered method: `mean_squared_logarithmic_error`
- Category: core error
- Return shape: scalar
- Implemented range: [0, infinity), or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: nanmean((log1p(prediction)-log1p(observation))^2).
- Preprocessing:
  - Drop nonfinite pairs.
  - Apply natural log after adding one.
  - Omit NaN log-domain contributions through nanmean.
- Dependencies:
  - NumPy log1p
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Input nonfinite pairs are removed; log-domain NaNs created afterward are omitted, while infinities can create NaN differences.
- Zero inputs or denominators: Zeros are valid because log1p(0)=0.
- Negative inputs: Values below -1 produce RuntimeWarning and NaN contributions that nanmean omits; exactly -1 produces negative infinity and may yield infinite or NaN differences.
- Constant series: Equal constants greater than -1 return zero; equal -1 constants warn and return NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: MSLE averages squared differences of log(1+prediction) and log(1+observation) and therefore requires both values to be nonnegative in standard regression APIs.
- References:
  - [mean_squared_log_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html) — scikit-learn developers (2026), authoritative. Supports: Documents the log(1+x) squared-error definition and rejects negative targets or predictions.
- Known variants:
  - Some log errors use log values without the +1 shift or explicitly validate nonnegative inputs; runtime uses log1p without validation.

#### Characterization and tests

- Ordinary case: Predictions [1,3] versus observations [0,1] give the mean of two squared log(2) differences.
- Edge case: For predictions [-2,0] versus [0,0], the invalid first contribution warns and is omitted, leaving a reported zero; equal -1 values warn and return NaN.
- Existing tests:
  - tests/test_error_metrics.py::test_mean_squared_logarithmic_error
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_msle_matches_log1p_hand_calculation_and_preserves_negative_domain_warnings

#### Findings and recommended future action

- `possible-defect`
  - Evidence: Negative values are not rejected; domain-invalid contributions can be omitted by nanmean and make a partially invalid dataset appear perfect.
  - Impact: MSLE can return a finite misleading value after runtime warnings.
  - Recommended future action: Specify a nonnegative input contract and consider explicit validation only in a separately approved runtime change.

<a id="metric-nmaep"></a>
### `NMAEp` — Normalized Mean Absolute p-Error

- Registered method: `nmaep`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: [0, infinity)
- Ideal value: 0

#### Implemented behavior

- Formula: mean(|prediction-observation|^p)^(1/p) / |mean(observation)|.
- Preprocessing:
  - Drop nonfinite pairs.
- Dependencies:
  - Bottleneck nanmean
  - NumPy abs and isfinite

#### Parameters

| Name | Default | Accepted types | Validation | Invalid behavior |
| --- | --- | --- | --- | --- |
| `p` | `1.0` | Finite real numeric values greater than zero, excluding bool and numpy.bool_ | Reject bool, nonfinite, zero, and negative values with ValueError. | Raises ValueError with 'p must be finite and > 0'. |

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed; nonfinite p is rejected.
- Zero inputs or denominators: A zero observation mean raises ValueError, including nonzero observations that cancel.
- Negative inputs: Accepted; errors and the normalizing observation mean are made absolute.
- Constant series: Defined when the observation constant is nonzero; zero observations raise ValueError.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: A mean absolute p-error is the power mean of absolute errors; normalization by an observed location or scale is an application-specific relative-error convention.
- References:
  - [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html) — NumPy developers (2026), authoritative. Supports: Documents vector p-norm conventions that motivate the p-root of powered absolute errors.
- Known variants:
  - Lp norms usually use a sum rather than a mean, and normalized errors use many denominators; runtime uses the power mean divided by absolute observation mean.

#### Characterization and tests

- Ordinary case: Predictions [2,4] versus observations [1,2] give p=1 score 1, p=2 score sqrt(2.5)/1.5, and p=0.5 the corresponding power mean divided by 1.5.
- Edge case: Observations [-1,1] have zero mean and raise ValueError despite nonzero magnitudes; a nonzero mean near zero is accepted and produces a score above 10^12.
- Existing tests:
  - tests/test_v5_metrics.py::test_nmaep_matches_p1_p2_hand_calculations
  - tests/test_v5_metrics.py::test_nmaep_validation
  - tests/test_v5_metrics.py::test_nmaep_zero_mean_and_registry
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_nmaep_parameter_and_zero_mean_validation

#### Findings and recommended future action

- `definition-variant`
  - Evidence: No located primary source establishes the exact name NMAEp with normalization by absolute observation mean.
  - Impact: The metric can be mistaken for a standard Lp norm or for other normalized p-error denominators.
  - Recommended future action: Document the exact power-mean numerator and mean-observation denominator without implying a universal convention.

<a id="metric-nae"></a>
### `NAE` — Normalized Absolute Error

- Registered method: `normalized_absolute_error`
- Category: normalized and relative error
- Return shape: scalar
- Implemented range: unbounded signed real, infinity, or NaN
- Ideal value: 0

#### Implemented behavior

- Formula: nanmean(|prediction-observation| / (0.5*(prediction+observation))).
- Preprocessing:
  - Drop nonfinite pairs.
  - Form a signed pairwise arithmetic-mean denominator.
- Dependencies:
  - NumPy abs
  - Bottleneck nanmean

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite input pairs are removed; division can create infinities retained by nanmean and NaNs omitted by nanmean.
- Zero inputs or denominators: Opposite-signed pairs with zero sum yield infinity; (0,0) yields NaN and is omitted; all-zero data return NaN.
- Negative inputs: A negative pair sum creates a negative contribution despite the absolute numerator.
- Constant series: Equal constants return zero unless both are zero, which returns NaN.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Normalized absolute-error names cover multiple denominators; a symmetric relative difference commonly uses absolute magnitudes in the denominator to retain nonnegativity.
- References:
  - [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001) — Hyndman and Koehler (2006), primary. Supports: Reviews scale-free absolute and symmetric percentage errors and their denominator pathologies.
- Known variants:
  - Normalization may use mean observation, observation range, L1 observation total, or the sum of absolute prediction and observation; runtime uses each pair's signed half-sum.

#### Characterization and tests

- Ordinary case: Predictions [3,6] versus observations [1,2] yield two contributions equal to one and score one.
- Edge case: All-negative proportional pairs return -1; opposite-signed zero-sum pairs return infinity; all-zero pairs return NaN.
- Existing tests:
  - None
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_nae_uses_signed_pairwise_half_sum_denominators

#### Findings and recommended future action

- `possible-defect`
  - Evidence: The denominator is the signed half-sum rather than a magnitude, so a named absolute error can be negative and can diverge at opposite-signed pairs.
  - Impact: The documented nonnegative error interpretation and comparisons across signed data are unreliable.
  - Recommended future action: Document the signed denominator immediately; evaluate an absolute-denominator alternative only as a separately approved compatibility change.

<a id="metric-gini"></a>
### `Gini` — Gini Coefficient

- Registered method: `gini_coefficient`
- Category: correlation and agreement
- Return shape: scalar
- Implemented range: data-dependent signed real, or NaN
- Ideal value: maximum attainable value for the fixed observations

#### Implemented behavior

- Formula: Sort pairs by descending prediction; accumulate observation/total_observation minus 1/N at each rank; return the accumulated sum divided by N.
- Preprocessing:
  - Drop nonfinite pairs.
  - Order by descending predictions with NumPy argsort.
- Dependencies:
  - NumPy argsort
  - Bottleneck nansum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first.
- Zero inputs or denominators: A zero observation total returns NaN.
- Negative inputs: Negative predictions only determine ordering; an all-negative nonzero observation total can produce the same score as a sign-flipped positive outcome vector, while mixed signs can leave standard Lorenz interpretations.
- Constant series: Constant predictions use argsort's tie order, so the score can depend on input order; constant nonzero observations return zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: The concentration/Gini ranking statistic is twice the area between a cumulative outcome curve ordered by model score and the equality line; normalized Gini divides by the perfect-order statistic.
- References:
  - [Economic Inequality and Income Distribution](https://archive.org/details/economicinequali0000sena) — Amartya Sen (1973), primary. Supports: Develops the Lorenz-curve and Gini-area interpretation for nonnegative distributions.
  - [MATLAB Gini metric implementation](https://github.com/benhamner/Metrics/blob/master/MATLAB/metrics/gini.m) — Ben Hamner Metrics repository (2012), authoritative. Supports: Implements the exact descending-prediction cumulative-loss ranking algorithm reproduced by the runtime.
- Known variants:
  - Competition Gini is often normalized by the perfect ranking; runtime returns an unnormalized discrete area.
  - Tie handling can average ranks or preserve input order; runtime relies on argsort ordering.

#### Characterization and tests

- Ordinary case: For outcomes [1,1,0,0,0], descending perfect ordering scores 0.3 and reversed ordering scores -0.3.
- Edge case: A zero outcome total returns NaN; prediction ties can make result depend on original row order.
- Existing tests:
  - tests/test_error_metrics.py::test_gini_coefficient
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_gini_depends_on_descending_prediction_order_and_observation_total

#### Findings and recommended future action

- `definition-variant`
  - Evidence: Runtime returns an unnormalized discrete ranking Gini rather than a [0,1] normalized Gini coefficient.
  - Impact: Perfect ranking depends on outcome prevalence (0.3 in the characterization), and reversed ranking is negative.
  - Recommended future action: Document unnormalized signed scale, outcome-domain restrictions, and tie behavior; do not claim range [0,1].

<a id="metric-pcd"></a>
### `PCD` — Prediction of Change in Direction

- Registered method: `prediction_of_change_in_direction`
- Category: trend and direction
- Return shape: scalar
- Implemented range: [0, 1], or NaN
- Ideal value: 1

#### Implemented behavior

- Formula: sum(((prediction[t]-prediction[t-1])*(observation[t]-observation[t-1]))>0)/(N-1).
- Preprocessing:
  - Drop nonfinite pairs before taking adjacent differences; removed pairs compress time.
- Dependencies:
  - NumPy sum

#### Parameters

No public parameters.

#### Edge cases

- NaN and infinity: Nonfinite pairs are removed first, potentially making formerly nonadjacent values adjacent.
- Zero inputs or denominators: A one-point series returns NaN by explicit guard.
- Negative inputs: Accepted; only successive difference signs matter.
- Constant series: Every flat transition scores false, including when both series are flat, so a length-at-least-two flat perfect series returns zero.
- No data after preprocessing: Construction raises ValueError.

#### Scientific basis

- Canonical or reference definition: Directional accuracy counts cases where forecast and actual changes have the same sign; exact treatments of zero change vary.
- References:
  - [Directional accuracy tests](https://doi.org/10.1080/07350015.1992.10509990) — Pesaran and Timmermann (1992), primary. Supports: Develops evaluation of whether predictions correctly identify the direction of change.
  - [Prediction of Change in Direction (PCD)](https://permetrics.readthedocs.io/en/latest/pages/regression/PCD.html) — Permetrics developers (2026), authoritative. Supports: Documents the successive-change product indicator used by the runtime implementation.
- Known variants:
  - Zero changes may count as agreement when both are flat, be excluded, or count as incorrect; runtime counts every zero-product transition as incorrect.

#### Characterization and tests

- Ordinary case: Predictions [1,2,1,3] and observations [1,3,2,4] have three matching strict directions and score one.
- Edge case: One point returns NaN; identical [1,1,2] series score 0.5 because their shared flat transition is counted incorrect; filtering an interior invalid pair creates a new adjacent transition, and a shared permutation can change the score.
- Existing tests:
  - tests/test_error_metrics.py::test_prediction_of_change_in_direction
- Characterization tests:
  - tests/audit/test_characterization_batch_9.py::test_pcd_short_flat_and_strict_direction_behavior
  - tests/audit/test_characterization_batch_9.py::test_pcd_pair_filtering_compresses_adjacency_and_retains_order_dependence

#### Findings and recommended future action

- `documentation-gap`
  - Evidence: Runtime requires a strictly positive product, so matching flat transitions do not count as correct, and preprocessing can compress time.
  - Impact: Perfect series with plateaus score below one and missing-value removal changes which transitions are evaluated.
  - Recommended future action: Document strict-direction and time-compression semantics.
