# Error Metrics Library

Error Metrics compares paired predictions and observations with 89 registered
metrics for evaluating model performance and prediction accuracy.

## Features

- 89 registered error metrics for model evaluation
- Support for handling NaN and infinite values
- Type hints and comprehensive documentation
- Extensible metric registry system
- Efficient computation using NumPy and Bottleneck
- Comprehensive test coverage

## Installation

Error Metrics requires Python 3.9 or newer. Install the latest version
directly from GitHub:

```bash
python -m pip install "git+https://github.com/chayanroyc/error-metrics.git"
```

NumPy, SciPy, and Statsmodels are required dependencies. Bottleneck is
available through the optional `speed` extra:

```bash
python -m pip install "error-metrics[speed] @ git+https://github.com/chayanroyc/error-metrics.git"
```

To force an upgrade and reinstall from GitHub:

```bash
python -m pip install --upgrade --force-reinstall "git+https://github.com/chayanroyc/error-metrics.git"
```

## Quick start

```python
from error_metrics import ErrorMetrics

predictions = [1.2, 1.8, 3.2, 3.9, 5.1]
observations = [1.0, 2.0, 3.0, 4.0, 5.0]
metrics = ErrorMetrics(predictions, observations)

print(metrics.mean_absolute_error())
print(metrics.root_mean_squared_error())
print(metrics.get_metrics(["MAE", "RMSE", "MBF"]))
```

Direct calls use Python method names, such as `mean_absolute_error`. Registry
dispatch through `get_metrics` uses metric abbreviations, such as `MAE`.

## Available Metrics

The registry below is the authoritative dispatch reference. Range and ideal
values describe the implementation where a universal interpretation is
supported; otherwise they are marked context-dependent.

<!-- metric-reference:start -->
| Abbreviation | Metric | Method | Purpose | Range | Ideal |
| --- | --- | --- | --- | --- | --- |
| `MB` | Mean Bias | `mean_bias` | Mean Bias | Unbounded | `0` |
| `MAE` | Mean Absolute Error | `mean_absolute_error` | Mean Absolute Error | [0, ∞) | `0` |
| `MedAE` | Median Absolute Error | `median_absolute_error` | Median Absolute Error | [0, ∞) | `0` |
| `RMSE` | Root Mean Squared Error | `root_mean_squared_error` | Root Mean Squared Error | [0, ∞) | `0` |
| `R` | Correlation Coefficient | `correlation_coefficient` | Pearson correlation coefficient | [-1, 1] | `1` |
| `SpearmanR` | Spearman Rank Correlation | `spearman_r` | Spearman rank correlation coefficient | [-1, 1] | `1` |
| `KendallTau` | Kendall Tau Correlation | `kendall_tau` | Kendall's tau rank correlation coefficient | [-1, 1] | `1` |
| `LCCC` | Lin's Concordance Correlation | `lccc` | Measure of agreement | [-1, 1] | `1` |
| `EV` | Explained Variance | `ev` | Proportion of variance explained | (-∞, 1] | `1` |
| `NMSE` | Normalized Mean Square Error | `nmse` | Normalized mean square error | Context-dependent | Context-dependent |
| `CRM` | Coefficient of Residual Mass | `coefficient_of_residual_mass` | Coefficient of Residual Mass | Unbounded | `0` |
| `RE` | Relative Error | `relative_error` | Relative Error | [0, ∞) | `0` |
| `EC` | Efficiency Coefficient | `efficiency_coefficient` | Efficiency Coefficient | (-∞, 1] | `1` |
| `MASE` | Mean Absolute Scaled Error | `mean_absolute_scaled_error` | Mean Absolute Scaled Error | [0, ∞) | `0` |
| `MAAPE` | Mean Arctangent Absolute Percentage Error | `mean_arctangent_absolute_percentage_error` | Mean Arctangent Absolute Percentage Error | [0, ∞) | `0` |
| `A10` | A10 Index | `a10_index` | A10 Index | [0, 1] | `1` |
| `CI` | Confidence Index | `confidence_index` | Confidence Index | [-1, 1] | `1` |
| `ME` | Max Error | `max_error` | Max Error | [0, ∞) | `0` |
| `R2` | Coefficient of Determination | `coefficient_of_determination` | R-squared | (-∞, 1] | `1` |
| `MNB` | Mean Normalized Bias | `mean_normalized_bias` | Mean Normalized Bias | Unbounded | `0` |
| `MNAE` | Mean Normalized Absolute Error | `mean_normalized_absolute_error` | Mean Normalized Absolute Error | Context-dependent | `0` |
| `FB` | Fractional Bias | `fb` | Measure of relative bias | Unbounded | `0` |
| `FAE` | Fractional Absolute Error | `fae` | Measure of relative absolute error | Context-dependent | Context-dependent |
| `MFB` | Mean Fractional Bias | `mean_fractional_bias` | Pointwise mean fractional bias; requires nonnegative paired inputs | [-2, 2] | `0` |
| `MFE` | Mean Fractional Error | `mean_fractional_error` | Pointwise mean fractional absolute error; requires nonnegative paired inputs | [0, 2] | `0` |
| `MAGE` | Mean Absolute Gross Error | `mean_absolute_gross_error` | Mean Absolute Gross Error | Context-dependent | `0` |
| `GMB` | Geometric Mean Bias | `geometric_mean_bias` | Geometric Mean Bias | (0, ∞) | `1` |
| `FAC2` | Factor of Observations 2 | `factor_of_observations2` | Factor of Observations 2 | [0, 100] | `100` |
| `MBD` | Mean Bias Difference | `mean_bias_difference` | Mean Bias Difference | Unbounded | `0` |
| `RMSD` | Root Mean Square Difference | `root_mean_square_difference` | Root Mean Square Difference | Context-dependent | `0` |
| `MAD` | Mean Absolute Difference | `mean_absolute_difference` | Mean Absolute Difference | Context-dependent | `0` |
| `SD` | Standard Deviation of Residual | `standard_deviation_of_residual` | Standard Deviation of Residual | Context-dependent | `0` |
| `SBF` | Slope of Best-Fit Line | `slope_of_best_fit_line` | Slope of Best-Fit Line | Unbounded | `1` |
| `U95` | Uncertainty at 95% | `uncertainty_95` | Uncertainty at 95% | [0, ∞) | `0` |
| `TS` | t-Statistic | `t_statistic` | t-Statistic | [0, ∞) | `0` |
| `NSE` | Nash-Sutcliffe Efficiency | `nash_sutcliffe_efficiency` | Nash-Sutcliffe Efficiency | (-∞, 1] | `1` |
| `NNSE` | Normalized NSE | `normalized_nse` | Normalized Nash-Sutcliffe Efficiency | [0, 1] | `1` |
| `RAE` | Relative Absolute Error | `relative_absolute_error` | Relative Absolute Error | [0, ∞) | `0` |
| `VAF` | Variance Accounted For | `variance_accounted_for` | Variance Accounted For | (-∞, 100] | `100` |
| `RSE` | Residual Standard Error | `residual_standard_error` | Residual Standard Error | [0, ∞) | `0` |
| `KGE` | Kling-Gupta Efficiency | `kling_gupta_efficiency` | Kling-Gupta Efficiency (2009 version) | (-∞, 1] | `1` |
| `KGE2012` | Modified Kling-Gupta Efficiency | `modified_kling_gupta_efficiency` | Kling-Gupta Efficiency (2012 version) | (-∞, 1] | `1` |
| `KGEdp` | Kling-Gupta Efficiency Double Prime | `kling_gupta_efficiency_double_prime` | Kling-Gupta Efficiency (Tang et al. 2021) | (-∞, 1] | `1` |
| `DE` | Diagnostic Efficiency | `diagnostic_efficiency` | Diagnostic Efficiency (Schwemmle et al. 2021) | (-∞, 1] | `1` |
| `LME` | Liu Model Efficiency | `liu_model_efficiency` | Liu Model Efficiency (Liu 2020) | (-∞, 1] | `1` |
| `LCEf` | Least-squares Combined Efficiency | `least_squares_combined_efficiency` | Least-squares Combined Efficiency (Lee & Choi 2022) | (-∞, 1] | `1` |
| `WIA` | Willmott's Index of Agreement | `willmotts_index_of_agreement` | Willmott's Index of Agreement | [0, 1] | `1` |
| `WIAr` | Refined Index of Agreement | `refined_index_of_agreement` | Refined Index of Agreement (Willmott et al. 2012) | [-1, 1] | `1` |
| `LCE` | Legates Coefficient of Efficiency | `legates_coefficient_of_efficiency` | Legates Coefficient of Efficiency | (-∞, 1] | `1` |
| `KSI` | Kolmogorov-Smirnov Test Integral | `ksi` | Measure of distribution similarity | [0, ∞) | `0` |
| `PHI` | Percentage of Histogram Intersection | `phi` | Histogram-overlap distribution similarity; requires integer `n_bins >= 1` | [0, 1] | `1` |
| `SUSE` | Scaled and Unscaled Shannon Entropy Difference | `suse` | Entropy-based variability similarity; requires integer `n_bins >= 1` | [0, ∞) | `0` |
| `OVER` | Over-estimation Metric | `over_metric` | Measure of over-estimation | [0, ∞) | `0` |
| `IQR` | Interquartile Range | `IQR` | Measure of statistical dispersion | [0, ∞) | Context-dependent |
| `STD` | Standard Deviation | `STD` | Measure of data spread | [0, ∞) | Context-dependent |
| `nESkew` | Normalized Error Skewness | `normalized_error_skewness` | Skewness of normalized error (Correndo et al. 2021) | Context-dependent | Context-dependent |
| `nEKurt` | Normalized Error Kurtosis | `normalized_error_kurtosis` | Kurtosis of normalized error (Correndo et al. 2021) | Context-dependent | Context-dependent |
| `MBF` | Mean Bias Factor | `mean_bias_factor` | Ratio of mean prediction to mean observation; requires strictly positive prediction and observation means | (0, ∞) | `1` |
| `RMBF` | Relative Mean Bias Factor | `relative_mean_bias_factor` | Absolute deviation of MBF from one; requires strictly positive prediction and observation means | [0, ∞) | `0` |
| `NMBF` | Normalized Mean Bias Factor | `nmbf` | Measure of bias factor | Context-dependent | `1` |
| `RNMBF` | Relative Normalized Mean Bias Factor | `rnmbf` | Measure of relative bias factor | [0, ∞) | `0` |
| `CPI` | Combined Performance Index | `cpi` | Overall performance measure | [0, ∞) | `0` |
| `RED` | Relative Euclidean Distance | `red` | Measure of relative distance | [0, ∞) | `0` |
| `FoM` | Figure of Merit | `figure_of_merit` | Measure of model performance | Context-dependent | Context-dependent |
| `MSDdec` | MSD Decomposition | `msd_decomposition` | Mean Square Deviation decomposition (Gauche) | Context-dependent | Context-dependent |
| `SS` | Skill Score vs Climatology | `skill_score_against_climatology` | Skill score against climatology | (-∞, 1] | `1` |
| `AD` | Anderson-Darling Distance | `anderson_darling_distance` | Anderson-Darling distance | [0, ∞) | `0` |
| `KLD` | Kullback-Leibler Divergence | `kullback_leibler_divergence` | Kullback-Leibler divergence | [0, ∞) | `0` |
| `MPE` | Mean Percentage Error | `mean_percentage_error` | Mean percentage error | Context-dependent | `0` |
| `MAPE` | Mean Absolute Percentage Error | `mean_absolute_percentage_error` | Mean absolute percentage error | [0, ∞) | `0` |
| `sMAPE` | Symmetric Mean Absolute Percentage Error | `symmetric_mean_absolute_percentage_error` | Symmetric mean absolute percentage error | [0, 200] | `0` |
| `CRPS` | Continuous Ranked Probability Score | `continuous_ranked_probability_score` | Continuous ranked probability score | [0, ∞) | `0` |
| `TAcc` | Trend Accuracy | `trend_accuracy` | Trend accuracy | (-∞, 1] | `1` |
| `U2` | Theil's Inequality Coefficient | `theils_u2` | Theil's U2 coefficient | [0, ∞) | `0` |
| `BM` | Berry-Mielke Index | `berry_mielke_score` | Berry & Mielke's agreement score | Context-dependent | `1` |
| `dCor` | Distance Correlation | `distance_correlation` | Distance correlation (Székely et al. 2007) | [0, 1] | `1` |
| `lambda` | Duveiller Agreement Coefficient | `duveiller_agreement_coefficient` | Symmetric agreement coefficient (Duveiller et al. 2016) | (-∞, 1] | `1` |
| `iqRMSE` | Inter-Quartile RMSE | `interquartile_rmse` | Inter-Quartile Root Mean Squared Error | [0, ∞) | `0` |
| `SMA` | SMA Regression Metrics | `sma_metrics` | SMA regression and error decomposition (Correndo et al. 2021) | Context-dependent | Context-dependent |
| `RNP` | Non-parametric KGE | `rnp` | Non-parametric Kling-Gupta efficiency | Context-dependent | `1` |
| `TSS` | Taylor Skill Score | `taylor_skill_score` | Taylor skill score | Context-dependent | `1` |
| `MEAN` | Mean Values | `meann` | Mean values of observations and predictions | Context-dependent | Context-dependent |
| `MEDIAN` | Median Values | `mediann` | Median values of observations and predictions | Context-dependent | Context-dependent |
| `CRMSE` | Centered Root Mean Square | `centered_root_mean_square` | Centered root mean square error | [0, ∞) | `0` |
| `MSLE` | Mean Squared Logarithmic Error | `mean_squared_logarithmic_error` | Mean squared logarithmic error | [0, ∞) | `0` |
| `NMAEp` | Normalized Mean Absolute p-Error | `nmaep` | Lp-norm accuracy normalized by mean observation; requires finite `p > 0` and nonzero observation mean | [0, ∞) | `0` |
| `NAE` | Normalized Absolute Error | `normalized_absolute_error` | Normalized Absolute Error | Context-dependent | `0` |
| `Gini` | Gini Coefficient | `gini_coefficient` | Gini coefficient for ranking evaluation | Context-dependent | `1` |
| `PCD` | Prediction of Change in Direction | `prediction_of_change_in_direction` | Prediction of Change in Direction | [0, 1] | `1` |
<!-- metric-reference:end -->

### Interpreting common errors

Absolute and squared errors are all minimized at zero, but they emphasize
mistakes differently. MAE and MedAE stay in the data's units; MedAE is less
sensitive to isolated outliers. RMSE and CRMSE weight large errors more heavily,
while CRMSE removes the mean bias before measuring scatter. Percentage and
normalized errors can ease comparisons across scales, but their denominators
and input restrictions matter.

### Interpreting the recovered metrics

The seven recovered registry metrics use these definitions:

- `MBF = mean(predictions) / mean(observations)`; `RMBF = abs(MBF - 1)`.
  Both require strictly positive prediction and observation means.
- `MFB = mean(2 * (predictions - observations) / (predictions + observations))`
  and `MFE = mean(2 * abs(predictions - observations) / (predictions + observations))`.
  Both require nonnegative paired inputs; an identical zero pair contributes
  zero.
- `PHI = sum(min(prediction histogram probability, observation histogram probability))`.
  It requires integer `n_bins >= 1`; one means identical histogram mass and zero
  means no overlap for the chosen common bins.
- `NMAEp = mean(abs(predictions - observations) ** p) ** (1 / p) / abs(mean(observations))`.
  It requires finite `p > 0` and a nonzero observation mean.
- `SUSE = max(abs(H(predictions; common bins) - H(observations; common bins)),
  abs(H(predictions; prediction bins) - H(observations; observation bins)))`.
  It requires integer `n_bins >= 1`. The common bins span the combined inputs;
  the separate bins are computed from each input independently. Here `H` is
  natural-log Shannon entropy of the nonzero histogram probabilities.

## Public API

Call a metric directly by its method name when you need one result:

```python
mae = metrics.mean_absolute_error()
rmse = metrics.root_mean_squared_error()
```

Use registered abbreviations to calculate a selected group, or calculate all
registered metrics:

```python
selected = metrics.get_metrics(["MAE", "RMSE"])
all_results = metrics.all_metrics()
```

Inspect the registry without creating an `ErrorMetrics` instance:

```python
from error_metrics import MetricRegistry

registered_metrics = MetricRegistry.get_all_metrics()
```

Methods with parameters are called directly. For example:

```python
phi_score = metrics.phi(n_bins=10)
normalized_error = metrics.nmaep(p=2.0)
suse_score = metrics.suse(n_bins=10)
```

## Input validation and missing values

`ErrorMetrics` converts both inputs to float arrays, requires their original
shapes to match, and then stores them as one-dimensional arrays. A whole pair
is removed during initialization if either member is non-finite; initialization
fails if no valid pairs remain. Individual metrics may impose additional
positivity, nonzero-denominator, or parameter restrictions.

NaN handling is metric-specific. Although many calculations use NaN-aware
NumPy or Bottleneck operations, callers should check the documentation and
result of the metric they use rather than assume one policy for every metric.

## Performance

Metric calculations primarily use vectorized NumPy operations. If Bottleneck
is installed, compatible reductions use it; otherwise the package falls back
to NumPy. Install the optional `speed` extra to enable Bottleneck.

## Development

```bash
python -m pip install -e ".[dev]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
python -m build
```

## Adding New Metrics

Add the method to `ErrorMetrics` and register its unique abbreviation. For a
scalar metric:

```python
@MetricRegistry.register("Mean Signed Cubic Error", "MSCE", "Mean cubed residual")
def mean_signed_cubic_error(self) -> float:
    return float(np.nanmean((self.predictions - self.observations) ** 3))
```

Methods may accept parameters when direct callers need to control a
calculation:

```python
@MetricRegistry.register("Threshold Exceedance Rate", "TER", "Fraction above a threshold")
def threshold_exceedance_rate(self, threshold: float = 1.0) -> float:
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("threshold must be finite and >= 0")
    return float(np.nanmean(np.abs(self.predictions - self.observations) > threshold))
```

Parameterized metrics should be called directly when nondefault arguments are
needed. Each new metric needs direct calculation and validation tests, plus a
test that confirms its registry mapping or dispatch behavior. These snippets
are contributor examples only; they are not part of the installed package.

## Contributing

Keep changes focused, add or update tests for behavior changes, run the
development checks above, and submit a pull request describing the change and
its verification.

## Citation

If you use Error Metrics in research, cite the repository:

```bibtex
@software{error_metrics_library,
  author = {Roy, Chayan},
  title = {Error Metrics Library},
  url = {https://github.com/chayanroyc/error-metrics}
}
```

## License

This project is licensed under the [MIT License](LICENSE).
