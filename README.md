# Error Metrics Library

A comprehensive Python library for calculating various error metrics between predictions and observations. This library provides a wide range of statistical measures to evaluate model performance and prediction accuracy.

## Features

- 40+ error metrics for model evaluation
- Support for handling NaN and infinite values
- Type hints and comprehensive documentation
- Extensible metric registry system
- Efficient computation using NumPy and Bottleneck
- Comprehensive test coverage

## Installation

```bash
pip install numpy bottleneck statsmodels scipy
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from error_metrics import ErrorMetrics

# Create sample data
predictions = [1.2, 1.8, 3.2, 3.9, 5.1]
observations = [1.0, 2.0, 3.0, 4.0, 5.0]

# Initialize ErrorMetrics
metrics = ErrorMetrics(predictions, observations)

# Calculate specific metrics
mb = metrics.mean_bias()  # Mean Bias
mae = metrics.mean_absolute_error()  # Mean Absolute Error
rmse = metrics.root_mean_squared_error()  # Root Mean Squared Error

# Get multiple metrics at once
results = metrics.get_metrics(['MB', 'MAE', 'RMSE'])

# Get all available metrics
all_metrics = metrics.all_metrics()
```

## Available Metrics

### Basic Metrics

- **Mean Bias (MB)**: Average difference between predictions and observations
  - Range: (-∞, ∞)
  - Perfect score: 0
  - Formula: mean(predictions - observations)

- **Mean Absolute Error (MAE)**: Average absolute difference
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: mean(|predictions - observations|)

- **Median Absolute Error (MedAE)**: Median absolute error (robust to outliers)
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: median(|predictions - observations|)

- **Root Mean Squared Error (RMSE)**: Square root of mean squared differences
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: sqrt(mean((predictions - observations)²))

- **Mean Absolute Gross Error (MAGE)**: Normalized mean absolute error
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: mean(|predictions - observations| / observations)

- **Geometric Mean Bias (GMB)**: Multiplicative bias measure
  - Range: (0, ∞)
  - Perfect score: 1
  - Formula: exp(mean(ln(predictions / observations)))
  - Note: Requires positive values for both predictions and observations

### Correlation Metrics

- **Correlation Coefficient (R)**: Pearson correlation coefficient
  - Range: [-1, 1]
  - Perfect score: 1
  - Formula: cov(predictions, observations) / (std(predictions) * std(observations))

- **Spearman Rank Correlation (SpearmanR)**: Non-parametric correlation
  - Range: [-1, 1]
  - Perfect score: 1
  - Formula: Spearman's rank correlation coefficient

- **Kendall Tau Correlation (KendallTau)**: Rank correlation based on concordant pairs
  - Range: [-1, 1]
  - Perfect score: 1
  - Formula: τ = (concordant pairs - discordant pairs) / total pairs
  - More robust to outliers and ties than Spearman

- **Lin's Concordance Correlation (LCCC)**: Measure of agreement
  - Range: [-1, 1]
  - Perfect score: 1
  - Formula: 2 * r * σx * σy / (σx² + σy² + (μx - μy)²)

- **Explained Variance (EV)**: Proportion of variance explained
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: 1 - var(residuals) / var(observations)

- **Distance Correlation (dCor)**: Distance-based correlation
  - Range: [0, 1]
  - Perfect score: 1
  - Captures both linear and non-linear dependence using distance covariance
  - References: Székely et al. (2007); Rizzo & Székely (2022)

- **Duveiller Agreement Coefficient (lambda)**: Symmetric agreement coefficient
  - Range: [-1, 1]
  - Perfect score: 1
  - Formula: λ = 1 - MSE / (Var(obs) + Var(pred) + MBE²)
  - Measures both accuracy and precision; equivalent to CCC when correlation ≥ 0
  - Reference: Duveiller et al. (2016)

### Normalized Metrics

- **Normalized Mean Square Error (NMSE)**: Normalized mean square error
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: mean((predictions - observations)²) / (mean(predictions) * mean(observations))

- **Inter-Quartile RMSE (iqRMSE)**: RMSE normalized by observation IQR
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: √mean((predictions - observations)²) / (Q3 - Q1)
  - Provides a scale-independent RMSE using the spread of the observations

- **Mean Normalized Bias (MNB)**: Mean normalized bias
  - Range: (-∞, ∞)
  - Perfect score: 0
  - Formula: mean((predictions - observations) / observations)

- **Mean Normalized Absolute Error (MNAE)**: Mean normalized absolute error
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: mean(|predictions - observations| / observations)

- **Fractional Bias (FB)**: Measure of relative bias
  - Range: [-2, 2]
  - Perfect score: 0
  - Formula: 2 * mean((predictions - observations) / (predictions + observations))

- **Fractional Absolute Error (FAE)**: Measure of relative absolute error
  - Range: [0, 2]
  - Perfect score: 0
  - Formula: 2 * mean(|predictions - observations| / (predictions + observations))

### Efficiency Metrics

- **Nash-Sutcliffe Efficiency (NSE)**: Model efficiency coefficient
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: 1 - sum((predictions - observations)²) / sum((observations - mean(observations))²)

- **Kling-Gupta Efficiency (KGE)**: Original efficiency measure (2009 version)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components: correlation (r), variability ratio (alpha = std_pred/std_obs), and mean ratio (beta)
  - Formula: KGE = 1 - √((r-1)² + (α-1)² + (β-1)²)

- **Modified Kling-Gupta Efficiency (KGE2012)**: Modified efficiency measure (2012 version)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components: correlation (r), variability ratio (alpha = CV_pred/CV_obs), and mean ratio (beta)
  - Formula: KGE = 1 - √((r-1)² + (α-1)² + (β-1)²)
  - Difference from 2009 version: alpha uses coefficient of variation (CV) ratio instead of standard deviation ratio

- **Kling-Gupta Efficiency Double Prime (KGEdp)**: KGE'' variant by Tang et al. (2021)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components: correlation (r), variability ratio (alpha = std_pred/std_obs), and normalized bias (beta_n)
  - Formula: KGE'' = 1 - √((r-1)² + (α-1)² + β_n²)
  - beta_n = (mean_pred - mean_obs) / std_obs (normalized bias, not a ratio)
  - Advantage: More robust when mean values are close to zero, as it uses normalized bias instead of mean ratio

- **Diagnostic Efficiency (DE)**: Diagnostic efficiency by Schwemmle et al. (2021)
  - Range: (-∞, 1]
  - Perfect score: 1 (higher is better)
  - Components: correlation (r), dynamic error (B_area), and constant error (B_rel_mean)
  - Formula: DE = 1 - √(B_rel_mean² + B_area² + (r-1)²)
  - Decomposes errors into three types calculated on Flow Duration Curve (FDC):
    - **Constant Error (B_rel_mean)**: Mean relative bias on FDC - systematic bias
    - **Dynamic Error (B_area)**: Mean absolute residual bias after removing constant error - variability discrepancies
    - **Timing Error (r)**: Pearson correlation on original time series - temporal misalignments
  - Advantage: Provides diagnostic insights into which type of error dominates model performance
  - Note: Components are calculated on sorted (descending) data for FDC analysis, except correlation which uses original time series
  - Reference: https://doi.org/10.5194/hess-25-2187-2021

- **Liu Model Efficiency (LME)**: Performance criterion by Liu (2020)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components: correlation (r), variability ratio (alpha), bias ratio (beta), and slope term (r*alpha)
  - Formula: LME = 1 - √((r*α - 1)² + (β - 1)²)
  - Key difference from KGE: Uses combined term (r*alpha) instead of separate r and alpha terms
  - The slope_term (r*alpha) represents the regression slope and combines correlation and variability
  - Advantage: Provides a more integrated assessment by combining correlation and variability into a single term
  - Reference: https://www.sciencedirect.com/science/article/pii/S0022169420309483

- **Least-squares Combined Efficiency (LCEf)**: Performance criterion by Lee & Choi (2022)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components: correlation (r), variability ratio (alpha), bias ratio (beta), and two slope terms
  - Formula: LCEf = 1 - √((r*α - 1)² + (r/α - 1)² + (β - 1)²)
  - Slope terms:
    - **slope_1 (r*alpha)**: Sim vs Obs slope (forward regression)
    - **slope_2 (r/alpha)**: Obs vs Sim slope (inverse regression)
  - Key difference from LME: Includes both forward and inverse slope terms, making it symmetric
  - Advantage: Provides a more balanced and symmetric evaluation by considering both regression directions
  - Reference: "A rebalanced performance criterion for hydrological model calibration" (Lee & Choi 2022)

- **Willmott's Index of Agreement (WIA)**: Measure of agreement (original version)
  - Range: [0, 1]
  - Perfect score: 1
  - Formula: 1 - sum((predictions - observations)²) / sum((|predictions - mean(obs)| + |observations - mean(obs)|)²)

- **Refined Index of Agreement (dr)**: Refined version by Willmott et al. (2012)
  - Range: [-1.0, 1.0]
  - Perfect score: 1.0
  - Formula: 
    - A = sum(|predictions - observations|)
    - B = 2 * sum(|observations - mean_obs|)
    - if A ≤ B: dr = 1 - A / B
    - else: dr = 1 - B / A
  - Advantage: More rationally related to model accuracy, uses absolute differences instead of squared differences
  - Reference: Willmott, C.J., Robeson, S.M. and Matsuura, K. (2012). A refined index of model performance. International Journal of climatology, 32(13), pp.2088-2094. doi:10.1002/joc.2419

- **Legates Coefficient of Efficiency (LCE)**: Modified efficiency measure
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: 1 - sum(|predictions - observations|) / sum(|observations - mean_obs|)

### Distribution Metrics

- **Kolmogorov-Smirnov Test Integral (KSI)**: Measure of distribution similarity
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: Integral of absolute difference between CDFs

- **Over-estimation Metric (OVER)**: Measure of over-estimation
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: Integral of positive differences between CDFs

- **Anderson-Darling Distance (AD)**: Distribution distance measure
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: Weighted sum of squared differences between CDFs

- **Kullback-Leibler Divergence (KLD)**: Measure of relative entropy
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: sum(obs * log(obs/pred))
  - Measures how one probability distribution diverges from another

### Percentage Metrics

- **Mean Percentage Error (MPE)**: Average percentage error
  - Range: (-∞, ∞)
  - Perfect score: 0
  - Formula: mean((predictions - observations) / observations) * 100

- **Mean Absolute Percentage Error (MAPE)**: Average absolute percentage error
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: mean(|(predictions - observations) / observations|) * 100

- **Symmetric Mean Absolute Percentage Error (sMAPE)**: Symmetric percentage error
  - Range: [0, 200]
  - Perfect score: 0
  - Formula: mean(2|predictions - observations| / (|predictions| + |observations|)) * 100

### Advanced Metrics

- **Combined Performance Index (CPI)**: Overall performance measure
  - Range: [0, +∞)
  - Perfect score: 0 (lower is better)
  - Formula: CPI = (KSI + OVER + 2*RMSE) / 4
  - Components: KSI (Kolmogorov-Smirnov Test Integral), OVER (Over-estimation Metric), and RMSE (Root Mean Squared Error)

- **Theil's Inequality Coefficient (U2)**: Relative error against observation energy
  - Range: [0, +∞)
  - Perfect score: 0
  - Formula: U2 = RMSE / √(mean(observations²))
  - Measures deviation relative to observation magnitude

- **Berry-Mielke Index (BM)**: Agreement index from Berry & Mielke (1985)
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: BM = 1 - δ / μ, where δ = (1/n) Σ|pred - obs| and μ = (2/n²) ΣΣ |pred_j - obs_i|
  - Captures both pairwise and crosswise deviations between predictions and observations

- **SMA Regression Metrics (SMA)**: Standard Major Axis regression parameters and error decomposition
  - Outputs: SMA slope/intercept, Mean Lack of Accuracy (MLA), Mean Lack of Precision (MLP), and their percentages
  - Relationship: MSE = MLA + MLP
  - Reference: Correndo et al. (2021). https://doi.org/10.1016/j.agsy.2021.103194

- **Figure of Merit (FoM)**: Measure of model performance
  - Range: [0, 100]
  - Perfect score: 100
  - Formula: (Aov / (Aov + Afn + Afp)) * 100

- **Taylor Skill Score (TSS)**: Skill score based on Taylor diagram
  - Range: [0, 1]
  - Perfect score: 1
  - Formula: 4(1 + r)⁴ / ((1 + std_ratio)²(1 + r)²)

- **Skill Score vs Climatology (SS)**: Skill score against climatology
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: 1 - sum((predictions - observations)²) / sum((climatology - observations)²)

- **Continuous Ranked Probability Score (CRPS)**: Proper scoring rule for probabilistic forecasts
  - Range: [0, +inf)
  - Perfect score: 0
  - Formula: For deterministic forecasts, reduces to MAE
  - Note: For probabilistic forecasts, use the properscoring library

### Factor Metrics

- **Factor of Observations 2 (FAC2)**: Percentage of predictions within a factor of 2 of observations
  - Range: [0, 100]
  - Perfect score: 100
  - Formula: 100 * sum(0.5 ≤ predictions/observations ≤ 2.0) / N

### Difference Metrics

- **Mean Bias Difference (MBD)**: Mean bias expressed as a percentage
  - Range: (-∞, ∞)
  - Perfect score: 0
  - Formula: (100 / mean_obs) * mean(predictions - observations)

- **Root Mean Square Difference (RMSD)**: Root mean square difference as a percentage
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: (100 / mean_obs) * sqrt(mean((predictions - observations)²))

- **Mean Absolute Difference (MAD)**: Mean absolute difference as a percentage
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: (100 / mean_obs) * mean(|predictions - observations|)

- **Standard Deviation of Residual (SD)**: Standard deviation of the residual
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: (100 / mean_obs) * sqrt(mean(residual²) - mean(residual)²)

- **Normalized Error Skewness (nESkew)**: Skewness of normalized error (Correndo et al. 2021)
  - Normalized error: nE = (predictions - observations) / max(predictions)
  - Measures asymmetry of nE distribution (unbounded)
  - Perfect score: 0

- **Normalized Error Kurtosis (nEKurt)**: Kurtosis of normalized error (Correndo et al. 2021)
  - Uses same nE definition as above
  - Measures tail heaviness (Fisher kurtosis, 0 for normal distribution)
  - Perfect score: 0

- **Slope of Best-Fit Line (SBF)**: Slope of the best-fit line
  - Range: (-∞, ∞)
  - Perfect score: 1
  - Formula: cov(predictions, observations) / var(observations)

- **MSD Decomposition (MSDdec)**: Gauche decomposition of Mean Square Deviation
  - Components returned: MSD, Systematic Bias (SB), Non-uniformity (NU), Lack of Correlation (LC)
  - Relationship: MSD = SB + NU + LC
  - Note: MSD, SB, NU, and LC are only available through this decomposition method, not as separate registered metrics
  - Use this to analyze how each component contributes to the overall MSD

- **Uncertainty at 95% (U95)**: 95% uncertainty interval
  - Range: [0, ∞)
  - Perfect score: 0
  - Formula: 1.96 * sqrt(mean((predictions - observations)²))

- **t-Statistic (TS)**: t-statistic for the difference
  - Range: (-∞, ∞)
  - Perfect score: 0
  - Formula: mean(predictions - observations) / (std(predictions - observations) / sqrt(N))

### Statistical Measures

- **Interquartile Range (IQR)**: Measure of statistical dispersion of observations
  - Range: [0, ∞)
  - Formula: Q3 - Q1 (75th percentile - 25th percentile of observations)

- **Normalized Error Skewness (nESkew)**: Skewness of normalized error distribution
  - Uses normalized error nE = (prediction - observation) / max(prediction)
  - Formula: skew = [N / ((N-1)(N-2))] * Σ ((nE - mean_nE) / SD)^3

- **Normalized Error Kurtosis (nEKurt)**: Kurtosis of normalized error distribution
  - Uses unbiased sample kurtosis formula on the normalized error
  - Formula: kurt = [N(N+1)/((N-1)(N-2)(N-3))] * Σ z^4 - [3(N-1)^2/((N-2)(N-3))]

### Engineering Metrics

- **A10 Index (A10)**: Proportion of predictions within ±10% of actual values
  - Range: [0, 1]
  - Perfect score: 1
  - Formula: (1/n) ∑{1 if |ŷ_i - y_i|/y_i ≤ 0.1 else 0}
  - Interpretation: Higher values indicate better model performance

- **Confidence Index (CI)**: Combined measure of correlation and agreement
  - Range: (-∞, 1]
  - Perfect score: 1
  - Formula: R * WI (Pearson correlation * Willmott's Index)
  - Interpretation:
    - > 0.85: Excellent Model
    - 0.76-0.85: Very good
    - 0.66-0.75: Good
    - 0.61-0.65: Satisfactory
    - 0.51-0.60: Poor
    - 0.41-0.50: Bad
    - < 0.40: Very bad

- **Max Error (ME)**: Maximum residual error
  - Range: [0, +inf)
  - Perfect score: 0
  - Formula: max(|y_i - ŷ_i|)
  - Interpretation: Captures the worst case error between predictions and observations

### Non-parametric Metrics

- **Non-parametric KGE (RNP)**: Non-parametric version of Kling-Gupta efficiency
  - Range: (-∞, 1]
  - Perfect score: 1
  - Components:
    - r: Spearman rank correlation
    - alpha: Flow duration curve similarity
    - beta: Mean ratio
  - Formula: 1 - √((α-1)² + (β-1)² + (r-1)²)
  - Returns: (RNP value, r component, alpha component, beta component)

### Normalized Metrics

- **Normalized NSE (NNSE)**: Normalized version of Nash-Sutcliffe efficiency
  - Range: [0, 1]
  - Perfect score: 1
  - Formula: 1/(2 - NSE)
  - Interpretation: Provides a more objective measure of model performance

- **Relative Absolute Error (RAE)**: Ratio of root mean squared error to root sum of squared observations
  - Range: [0, +inf)
  - Perfect score: 0
  - Formula: √(∑(ŷ_i - y_i)²) / √(∑y_i²)

### Variance Metrics

- **Variance Accounted For (VAF)**: Proportion of variance explained by predictions
  - Range: (-∞, 100%]
  - Perfect score: 100%
  - Formula: 100% * ∑(y_i - ȳ)(f_i - ḟ) / ∑(y_i - ȳ)²

- **Residual Standard Error (RSE)**: Average distance between observed and predicted values
  - Range: [0, +inf)
  - Perfect score: 0
  - Formula: √(∑(y_i - ŷ_i)² / (n-p-1))
  - Note: p is the number of predictors in the model

### Percentage Error Metrics

- **Mean Arctangent Absolute Percentage Error (MAAPE)**: Alternative to MAPE using arctangent
  - Range: [0, +inf)
  - Perfect score: 0
  - Formula: (100/n) ∑|(A_i - F_i)/A_i| * arctan(|(A_i - F_i)/A_i|)
  - Advantage: Avoids division by zero issues present in MAPE

## Usage Examples

### Basic Usage
```python
from error_metrics import ErrorMetrics

# Create sample data
predictions = [1.2, 1.8, 3.2, 3.9, 5.1]
observations = [1.0, 2.0, 3.0, 4.0, 5.0]

# Initialize ErrorMetrics
metrics = ErrorMetrics(predictions, observations)

# Calculate specific metrics
a10 = metrics.a10_index()  # A10 Index
ci = metrics.confidence_index()  # Confidence Index
me = metrics.max_error()  # Max Error

# Get multiple metrics at once
results = metrics.get_metrics(['A10', 'CI', 'ME', 'RMSE', 'NSE'])

# Get all available metrics
all_metrics = metrics.all_metrics()
```

### Advanced Usage
```python
# Calculate metrics with specific parameters
rse = metrics.residual_standard_error(p=2)  # RSE with 2 predictors
mase = metrics.mean_absolute_scaled_error(m=12)  # MASE with 12-month seasonality

# Get interpretation of Confidence Index
ci = metrics.confidence_index()
if ci > 0.85:
    print("Excellent Model")
elif ci > 0.76:
    print("Very good model")
# ... and so on

# Get components of RNP
rnp, r, alpha, beta = metrics.rnp()
print(f"RNP: {rnp:.3f}")
print(f"Spearman correlation (r): {r:.3f}")
print(f"Flow duration curve similarity (alpha): {alpha:.3f}")
print(f"Mean ratio (beta): {beta:.3f}")
```

## Error Handling

The library handles various edge cases:
- NaN values are automatically removed
- Infinite values are filtered out
- Zero values are handled appropriately for each metric
- Single value cases are handled with appropriate warnings
- Large and small numbers are processed with numerical stability

## Performance

The library uses:
- NumPy for efficient array operations
- Bottleneck for fast statistical computations
- Vectorized operations for optimal performance
- Efficient memory usage with in-place operations

## Testing

Run the test suite:
```bash
pytest test_error_metrics.py
```

The test suite includes:
- Unit tests for each metric
- Edge case testing
- Numerical stability tests
- Property verification tests
- Performance benchmarks

## Adding New Metrics

The library is designed to be easily extensible. Here's how to add a new metric:

1. Create a new method in the `ErrorMetrics` class
2. Decorate it with `@MetricRegistry.register`
3. Use the class's pre-processed data attributes

Here are examples of adding new metrics:

### Example 1: Simple Metric (Returns Single Value)

```python
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
```

### Example 2: Metric Returning Tuple (Multiple Components)

For metrics that return multiple components (like KGE, LME, LCEf, DE), use a tuple return type:

```python
from typing import Tuple

@MetricRegistry.register("Example Efficiency Metric", "EEM", "Example Efficiency Metric")
def example_efficiency_metric(self) -> Tuple[float, float, float, float]:
    """
    Calculate an example efficiency metric with multiple components.
    
    Formula:
        r = Pearson correlation coefficient
        alpha = std(predictions) / std(observations)
        beta = mean(predictions) / mean(observations)
        EEM = 1 - sqrt((r-1)² + (alpha-1)² + (beta-1)²)
    
    Returns:
        Tuple[float, float, float, float]: (EEM value, r component, alpha component, beta component)
    """
    std_obs = bn.nanstd(self.observations)
    std_pred = bn.nanstd(self.predictions)
    r = np.corrcoef(self.observations, self.predictions)[0, 1]
    alpha = std_pred / std_obs
    beta = self.pred_mean / self.obs_mean
    eem = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
    return eem, r, alpha, beta
```

### Example 3: Metric with Parameters

For metrics that require additional parameters:

```python
@MetricRegistry.register("Parameterized Metric", "PM", "Parameterized Metric")
def parameterized_metric(self, threshold: float = 0.1) -> float:
    """
    Calculate a parameterized metric with an optional threshold.
    
    Args:
        threshold: Threshold value for the calculation (default: 0.1)
    
    Returns:
        float: Parameterized metric value
    """
    # Note: Parameters are not part of the registry, so this metric
    # should be called directly: metrics.parameterized_metric(threshold=0.2)
    # It won't work with get_metrics(['PM']) if parameters are needed
    return bn.nanmean(np.abs(self.diff) / (self.observations + threshold))
```

Key points when adding new metrics:

1. **Use Class Attributes**: 
   - `self.predictions`: Array of predicted values
   - `self.observations`: Array of observed values
   - `self.diff`: Pre-calculated differences (predictions - observations)
   - `self.N`: Number of valid data points

2. **Handle NaN Values**:
   - Use `bn.nanmean()`, `bn.nanstd()`, etc. for calculations
   - The class automatically handles NaN and infinite values in `_preprocess_data()`

3. **Type Hints**:
   - Add return type hints (e.g., `-> float` or `-> Tuple[float, float]`)
   - Use proper type hints for any parameters

4. **Documentation**:
   - Add a clear docstring explaining the metric
   - Include the formula if applicable
   - Specify the range and perfect score

5. **Registration**:
   - Use `@MetricRegistry.register(name, abbreviation, description)`
   - Choose a unique abbreviation
   - Provide a clear description

After adding a new metric, it will be automatically available through:
- Direct method call: `metrics.your_new_metric()`
- `get_metrics()`: `metrics.get_metrics(['YOUR_ABBR'])`
- `all_metrics()`: Will include your new metric
- `print_abbreviations()`: Will show your metric's abbreviation

**Note for tuple-returning metrics**: When using `get_metrics()`, tuple values are automatically rounded. To access individual components, call the method directly:

```python
# For tuple-returning metrics
kge, r, alpha, beta = metrics.kling_gupta_efficiency()

# Or get all components via get_metrics (returns tuple)
results = metrics.get_metrics(['KGE'])
kge_tuple = results['KGE']  # This will be a tuple
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Add tests for new metrics
5. Submit a pull request

## License

MIT License

## Citation

If you use this library in your research, please cite:
```
@software{error_metrics_library,
  author = {Chayan Roychoudhury},
  title = {Error Metrics Library},
  year = {2024},
  url = {https://github.com/yourusername/error_metrics}
}
``` 
