# Metric behavior audit, batch 4: primary-source findings

## Scope and source policy

This note covers exactly `MAD`, `SD`, `SBF`, `U95`, `TS`, `NSE`, `NNSE`,
`RAE`, `VAF`, and `RSE`. Definitions are attributed to original papers,
standards bodies, government handbooks, or maintained scientific-software
documentation. Statements about this repository are implementation-derived
observations from `error_metrics/core.py`. Short names such as MAD, SD, RAE,
and VAF are not unique across disciplines; ambiguity is recorded rather than
resolved by silently choosing a nearby formula.

## Shared implemented contract

Implementation-derived: construction converts both inputs to floating-point
arrays, requires equal shapes, flattens them, removes every pair for which
either member is NaN or infinite, and raises `ValueError` if no pair remains.
These ten methods therefore receive at least one finite complete-case pair.
Several nevertheless become undefined on constant observations, a zero
observation mean, or nonpositive residual degrees of freedom.

## Findings by metric

### MAD — mean absolute difference

- **Canonical ambiguity.** “MAD” commonly denotes either mean absolute
  deviation/error, \(n^{-1}\sum_i|p_i-o_i|\), or median absolute deviation
  about a sample median. NIST calls the former the average absolute residual
  and gives it in the response variable's units
  ([NIST/SEMATECH, goodness-of-fit metrics](https://www.itl.nist.gov/div898/handbook/pri/section5/pri5992.htm));
  SciPy explicitly defines its robust `median_abs_deviation` as the median of
  absolute deviations from a center
  ([SciPy maintainers](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_abs_deviation.html)).
- **Implemented behavior.** The method computes
  \(100\,\operatorname{mean}|p-o|/\bar o\). This is a relative, percentage-
  scaled mean absolute error, not an unnormalized mean absolute difference.
  `_safe_divide` returns NaN for an exactly zero observation mean. A negative
  observation mean makes the result negative despite its absolute numerator.
- **Audit implication.** The registered full name disambiguates MAD away from
  median absolute deviation, but the implementation still has an undocumented
  normalization variant and percent unit. Its conventional nonnegative range
  holds only when the observation mean is positive.

### SD — standard deviation of residual

- **Canonical definition.** NIST defines residual standard deviation for a
  fitted model as \(\sqrt{\sum r_i^2/(n-p)}\), where `p` is the number of fitted
  coefficients, and notes that this assumes mean-zero residuals for an OLS
  model with a constant
  ([NIST/SEMATECH](https://www.itl.nist.gov/div898/handbook/pri/section5/pri599.htm)).
  Separately, NumPy defines population standard deviation with `ddof=0` and a
  divisor of `N`
  ([NumPy maintainers](https://numpy.org/doc/stable/reference/generated/numpy.std.html)).
- **Implemented behavior.** `SD` is
  \(100\sqrt{\operatorname{mean}(r^2)-\operatorname{mean}(r)^2}/\bar o\): the
  population standard deviation of the residual array, normalized by the
  signed observation mean and multiplied by 100. It has no degrees-of-freedom
  parameter. One pair or constant residuals produce zero when \(\bar o\ne0\);
  a zero observation mean produces NaN, and a negative mean reverses sign.
- **Audit implication.** This is a descriptive population residual spread,
  not the regression residual standard error. Centering also makes it
  insensitive to constant bias. The repository separately exposes `RSE` for
  a degrees-of-freedom-adjusted quantity.

### SBF — slope of best-fit line

- **Canonical definition.** Ordinary least-squares simple regression with an
  intercept has slope
  \(\sum(x_i-\bar x)(y_i-\bar y)/\sum(x_i-\bar x)^2\). NIST derives the
  least-squares estimates from minimizing squared residuals
  ([NIST/SEMATECH, linear least squares](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm));
  SciPy's maintained `linregress` identifies its returned slope as the
  least-squares regression-line slope
  ([SciPy maintainers](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)).
- **Implemented behavior.** With observations as `x` and predictions as `y`,
  the method matches the OLS-with-intercept slope formula. Constant
  observations make the denominator zero and return NaN, including exact
  constant agreement. Constant predictions with nonconstant observations
  return zero. The score is not symmetric; swapping inputs generally gives a
  different slope.
- **Audit implication.** The ordinary formula is consistent. A slope of one
  is not sufficient for agreement because the fitted intercept may be
  nonzero, and the method does not return or test that intercept.

### U95 — uncertainty at 95%

- **Published model-evaluation convention.** Recent uncertainty-analysis
  literature uses \(U_{95}=1.96\sqrt{SD^2+RMSE^2}\), describing 1.96 as the
  normal 95% factor and lower values as preferable
  ([Scientific Reports, 2025](https://doi.org/10.1038/s41598-025-20304-2)).
  This is an application-specific composite index, not a general confidence
  interval derived from a sampling distribution.
- **Implemented behavior.** The algebra matches that expression, but its
  ingredients are repository `SD` and `RMSD`, both already divided by the
  signed observation mean and multiplied by 100. Consequently `U95` is a
  relative percentage composite, not uncertainty in the original data units.
  A zero observation mean propagates NaN. Negative observation means make
  both ingredients negative, but squaring restores a nonnegative finite U95.
- **Audit implication.** The formula variant is recognizable, but the name
  must not promise calibrated 95% coverage. The component normalization and
  their zero-mean failure require explicit documentation.

### TS — t-statistic

- **Canonical application formula.** Jacovides and Kontoyiannis propose using
  MBE, RMSE, and
  \(t=\sqrt{(n-1)MBE^2/(RMSE^2-MBE^2)}\) together to evaluate
  evapotranspiration models
  ([*Agricultural Water Management*, 1995](https://doi.org/10.1016/0378-3774(95)01152-9)).
  This statistic tests mean residual bias because
  \(RMSE^2-MBE^2\) is the population residual variance.
- **Implemented behavior.** The method matches that algebra using repository
  `MBD` and `RMSD`. Their common signed percent normalization cancels whenever
  finite, so ordinary results equal those from dimensional MBE and RMSE. Zero
  observation mean makes both inputs NaN. Exact agreement gives `0/0` and NaN;
  constant nonzero residuals make the variance denominator zero and yield NaN
  through `_safe_divide` rather than positive infinity. A one-pair input also
  yields NaN.
- **Audit implication.** The formula is consistent with the cited specialized
  model-evaluation statistic, but “t-statistic” is overly generic. Its
  inferential interpretation assumes independent residuals and an appropriate
  reference t distribution; the method does not validate those assumptions or
  provide a p-value.

### NSE — Nash-Sutcliffe efficiency

- **Canonical definition.** Nash and Sutcliffe define efficiency by comparing
  squared model residuals with squared deviations from the observed mean,
  equivalent to
  \(1-\sum(p_i-o_i)^2/\sum(o_i-\bar o)^2\)
  ([Nash and Sutcliffe, 1970](https://doi.org/10.1016/0022-1694(70)90255-6)).
  One is perfect, zero means the observed-mean predictor is equally effective,
  and the statistic is unbounded below.
- **Implemented behavior.** The method matches the canonical formula after
  shared filtering. Constant observations (including one pair) make the
  denominator zero, and `_safe_divide` returns NaN even for exact agreement.
  It is asymmetric and invariant under a common nonzero scale and common
  additive shift.
- **Audit implication.** Ordinary behavior is consistent. The constant-series
  NaN is mathematically faithful to the undefined ratio, but must be documented.

### NNSE — normalized Nash-Sutcliffe efficiency

- **Published variant.** Hydrologic model evaluation uses the monotone
  transformation \(NNSE=1/(2-NSE)\), which maps finite NSE values below or
  equal to one into `(0,1]` and maps NSE zero to `0.5`
  ([NSE transformation documented in HESS](https://hess.copernicus.org/articles/23/4323/2019/)).
- **Implemented behavior.** The method exactly applies `1 / (2 - NSE)` using
  `_safe_divide`. It returns one at exact agreement on nonconstant
  observations and approaches zero for very poor finite NSE. Undefined NSE
  on constant observations propagates NaN.
- **Audit implication.** The transform is a recognized definition variant;
  calling it “more objective” is not established by the transformation alone.
  Its apparent `[0,1]` bound presumes the mathematically usual NSE `<= 1`.

### RAE — relative absolute error

- **Canonical definition.** Maintained `mlr3measures` documentation defines
  RAE as \(\sum|o_i-p_i|/\sum|o_i-\bar o|\), relative to the mean-prediction
  baseline
  ([mlr3measures maintainers](https://mlr3measures.mlr-org.com/reference/rae.html)).
- **Implemented behavior.** The method instead computes the Euclidean relative
  error \(\|p-o\|_2/\|o\|_2\). Thus it uses squared errors before the square
  root, no absolute-error sum, and a zero-vector rather than observed-mean
  baseline. An all-zero observation vector returns NaN; constant nonzero
  observations are accepted. Exact agreement is zero and the result is
  nonnegative and unbounded above.
- **Audit implication.** This is a substantive formula/name mismatch against
  conventional RAE. The implementation is a recognizable relative L2 norm,
  but its docstring's “root mean squared error” wording is also imprecise
  because both numerator and denominator are root *sums* of squares.

### VAF — variance accounted for

- **Canonical definition.** The standard explained-variance score is
  \(1-\operatorname{Var}(o-p)/\operatorname{Var}(o)\); maintained
  scikit-learn documentation notes that it is insensitive to systematic
  offsets and is non-finite for constant targets when finite-value coercion is
  disabled
  ([scikit-learn maintainers](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html)).
  VAF is commonly the percentage-scaled form of this ratio.
- **Implemented behavior.** The method computes
  \(100\sum(o-\bar o)(p-\bar p)/\sum(o-\bar o)^2\), exactly 100 times the OLS
  slope of predictions on observations. It does not compute residual variance.
  Constant observations return NaN. A prediction `p=2o` returns 200 even
  though canonical explained variance is zero; a constant offset `p=o+c`
  returns 100, consistent with offset-insensitivity.
- **Audit implication.** This is a possible formula defect and duplicates
  `100 * SBF`, not canonical VAF. Its documented upper bound of 100 is false:
  slopes above one yield values above 100, and arbitrary negative slopes yield
  negative values.

### RSE — residual standard error

- **Canonical definition and degrees of freedom.** NIST defines residual
  standard deviation as \(\sqrt{RSS/(n-k)}\), where `k` is the total number of
  fitted coefficients in the model
  ([NIST/SEMATECH](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm)).
  Equivalently, simple regression with `p` predictors plus an intercept uses
  denominator `n-p-1`.
- **Implemented behavior.** `RSE(p=1)` computes
  \(\sqrt{\sum(p_i-o_i)^2/(n-p-1)}\), matching that predictor-count convention
  if the supplied predictions came from a model fit to these same observations
  with an intercept. It does not validate `p`. Zero degrees of freedom raises
  `ZeroDivisionError` because Python scalar division occurs before `np.sqrt`;
  negative degrees of freedom produce NaN. A negative `p` is accepted and
  inflates degrees of freedom. The output remains in the data's units.
- **Audit implication.** The ordinary formula is consistent under its model-
  fitting assumptions, but `p` requires integer/range validation and clearer
  semantics. For arbitrary externally supplied predictions, subtracting fitted
  parameter degrees of freedom may not be justified.

## Batch-level conclusions

- `SBF`, `NSE`, `NNSE`, and ordinary-case `RSE` match recognized formulas,
  subject to degeneracy and assumption documentation.
- `MAD` and `SD` are percentage-normalized variants whose names imply
  dimensional statistics; negative or zero observation means are especially
  consequential.
- `U95` and `TS` use recognizable application formulas. `U95` is a composite
  index rather than guaranteed coverage, while TS's shared normalization
  cancels only when its components are finite.
- `RAE` implements a relative L2 norm rather than conventional relative
  absolute error. `VAF` is exactly `100 * SBF`, not variance accounted for.
- Constant observations make `SBF`, `NSE`, `NNSE`, and `VAF` undefined.
  Nonpositive `RSE` degrees of freedom and zero observation means across the
  normalized diagnostics need explicit characterization.
