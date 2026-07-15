# Metric behavior audit, batch 1: primary-source findings

## Scope and source policy

This note covers exactly `MB`, `MAE`, `MedAE`, `RMSE`, `R`, `SpearmanR`,
`KendallTau`, `LCCC`, `EV`, and `NMSE`. Scientific definitions are attributed
to original papers or maintained project documentation. Statements about this
repository are implementation-derived observations from `error_metrics/core.py`
and the relevant tests and are labeled as such.

## Shared implemented contract

Implementation-derived: construction converts both inputs to floating-point
arrays, requires equal shapes, flattens them, and removes every pair for which
either member is NaN or infinite. It raises `ValueError` if no pair remains.
Consequently, all ten metrics use complete-case pairs, including the SciPy
calls whose own NaN policies would otherwise differ. Pre-batch tests covered
the shared filtering, all-invalid input, and a one-valid-pair case only for
selected metrics. The final Batch 1 characterization applies shared finite-pair
and all-invalid checks across all ten methods.

## Findings by metric

### MB — mean bias

- **Canonical definition.** For paired predictions \(p_i\) and observations
  \(o_i\), mean bias is \(n^{-1}\sum_i(p_i-o_i)=\bar p-\bar o\). The direction
  depends on the declared subtraction convention; WMO model-evaluation
  training material defines it with the prediction-minus-observation
  convention and identifies positive bias with overprediction
  ([World Meteorological Organization, *Model Evaluation*, 2024](https://etrp.wmo.int/pluginfile.php/86185/mod_folder/content/0/S82b_Sep25_2024_Model_Evaluation.final.Sep25.2024.pdf)).
- **Implemented behavior.** `pred_mean - obs_mean` is algebraically the stated
  prediction-minus-observation mean bias. It is signed and unbounded, changes
  sign when the arguments are exchanged, is invariant to a common additive
  shift, and is zero for a perfect match. Negative and zero data require no
  special treatment.
- **Audit implication.** Formula behavior is consistent once the sign
  convention is documented. Pre-batch tests covered zeros, negative/mixed
  values, finite filtering, scale dependence, and argument-order asymmetry.
  The final Batch 1 characterization adds a direct nonzero hand calculation,
  the varying-data ideal, shared finite-pair filtering, and all-invalid input.

### MAE — mean absolute error

- **Canonical definition.** \(\mathrm{MAE}=n^{-1}\sum_i|o_i-p_i|\); it is a
  nonnegative loss with optimum zero
  ([scikit-learn maintainers, *Metrics and scoring: Mean absolute error*,
  current documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#mean-absolute-error)).
- **Implemented behavior.** `mean(abs(predictions - observations))` matches the
  unweighted scalar definition after shared filtering. It is symmetric in the
  two inputs, translation invariant, scales by \(|a|\) under common
  multiplication by \(a\), and is defined for one remaining pair.
- **Audit implication.** Canonical formula and implementation agree. Pre-batch
  tests covered perfect/zero, negative, mixed, very large/small, filtered, and
  outlier examples. The final Batch 1 characterization adds a standalone
  ordinary hand calculation, varying-data ideal, finite filtering, and
  all-invalid input.

### MedAE — median absolute error

- **Canonical definition.** Median absolute error is the median of the
  per-sample absolute residuals; it is nonnegative and has optimum zero
  ([scikit-learn maintainers, `median_absolute_error`, current API
  documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.median_absolute_error.html)).
- **Implemented behavior.** `median(abs(predictions - observations))` matches
  the unweighted scalar definition after filtering. For an even sample count,
  NumPy/Bottleneck median semantics average the two central ordered errors.
- **Audit implication.** Formula behavior is consistent. Pre-batch tests
  covered perfect prediction, range, and reduced sensitivity to one large
  outlier. The final Batch 1 characterization adds an ordinary hand
  calculation, varying-data ideal, finite filtering, and all-invalid input;
  even-sample median semantics and a one-retained-pair case remain uncovered.

### RMSE — root mean squared error

- **Canonical definition.** RMSE is
  \(\sqrt{n^{-1}\sum_i(o_i-p_i)^2}\), a nonnegative loss with optimum zero;
  scikit-learn's official regression guide defines MSE as the mean squared
  residual and its official RMSE API identifies the square-root loss and its
  zero optimum
  ([scikit-learn maintainers, *Metrics and scoring: Mean squared error*](https://scikit-learn.org/stable/modules/model_evaluation.html#mean-squared-error),
  [`root_mean_squared_error` API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html)).
- **Implemented behavior.** `sqrt(mean(diff ** 2))` matches the unweighted
  scalar definition after filtering. It is symmetric, translation invariant,
  and scales by \(|a|\). The mathematical inequality MAE \(\leq\) RMSE is
  asserted for one ordinary dataset.
- **Audit implication.** Canonical formula and implementation agree. Pre-batch
  tests covered perfect/zero, sign-mixed, scale, magnitude, and consistency
  properties. The final Batch 1 characterization adds a direct nonzero hand
  calculation, varying-data ideal, finite filtering, and all-invalid input;
  overflow near the floating-point limit remains uncovered.

### R — Pearson product-moment correlation

- **Canonical definition.** Pearson correlation standardizes covariance:
  \(r=C_{po}/\sqrt{C_{pp}C_{oo}}\), with values in \([-1,1]\)
  ([NumPy maintainers, `numpy.corrcoef`, current official documentation](https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html)).
  The maintained SciPy reference makes the degenerate cases explicit: at least
  two observations are required, a constant input yields NaN with a warning,
  and a near-constant input can trigger a numerical-accuracy warning
  ([SciPy maintainers, `scipy.stats.pearsonr`, current official
  documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html)).
- **Implemented behavior.** For at least two retained pairs the method returns
  `numpy.corrcoef(predictions, observations)[0, 1]`, so it delegates the
  canonical sample product-moment calculation to NumPy. It explicitly returns
  NaN for fewer than two pairs; NumPy also yields NaN for a constant input
  because its variance term is zero. The cached value is reused by `LCCC`.
- **Audit implication.** Formula/dependency choice is consistent. Pre-batch
  tests covered an ordinary value, perfect positive and negative relationships
  indirectly, argument symmetry, scale invariance, one pair, and caching. The
  final Batch 1 characterization adds a hand calculation, varying-data ideal,
  equal-constant NaN behavior, finite filtering, and all-invalid input;
  near-constant numerical-warning behavior remains uncovered.

### SpearmanR — Spearman rank correlation

- **Canonical definition.** Spearman introduced rank-based association in
  1904 ([C. Spearman, *The Proof and Measurement of Association between Two
  Things*, 1904, DOI 10.2307/1412159](https://doi.org/10.2307/1412159)). The
  maintained SciPy API defines its coefficient as a nonparametric measure of
  monotonicity in \([-1,1]\), with \(\pm1\) denoting exact monotonic
  relationships; constant input is undefined and returns NaN with a warning
  ([SciPy maintainers, `scipy.stats.spearmanr`, current official
  documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html)).
- **Implemented behavior.** The method returns the statistic from
  `scipy.stats.spearmanr(predictions, observations)` using SciPy defaults. Thus
  tie ranking and constant-input behavior belong to the installed SciPy
  version. Shared preprocessing removes nonfinite pairs before the call, so
  the default SciPy `nan_policy='propagate'` is not observable for original
  NaNs unless fewer than two finite pairs remain.
- **Audit implication.** The delegation is authoritative and the intended
  monotonic-association meaning is consistent. Pre-batch tests covered an
  exact increasing ranking, symmetry, and scale invariance. The final Batch 1
  characterization adds a nontrivial hand calculation, varying-data ideal,
  equal-constant NaN plus warning behavior, finite filtering, and all-invalid
  input; partially tied nonconstant ranks and one retained pair remain
  uncovered.

### KendallTau — Kendall rank correlation

- **Canonical definition and variant.** Kendall's original measure counts
  concordant and discordant pairs
  ([M. G. Kendall, *A New Measure of Rank Correlation*, 1938](https://doi.org/10.1093/biomet/30.1-2.81)).
  Kendall subsequently formalized treatment of ties
  ([M. G. Kendall, *The Treatment of Ties in Ranking Problems*, 1945](https://doi.org/10.1093/biomet/33.3.239)).
  With ties, SciPy's default is tau-b,
  \((P-Q)/\sqrt{(P+Q+T)(P+Q+U)}\), not the docstring's untied tau-a-style
  denominator; SciPy does not expose tau-a separately because tau-b and tau-c
  reduce to tau-a without ties
  ([SciPy maintainers, `scipy.stats.kendalltau`, current official
  documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html)).
- **Implemented behavior.** The method calls `kendalltau(observations,
  predictions, nan_policy='omit')` and does not pass `variant`, therefore it
  computes SciPy's default tau-b. Argument reversal does not alter the
  statistic. Constructor filtering makes the explicit omit policy redundant
  for original NaNs. Constant/all-tied inputs produce an undefined denominator
  and NaN.
- **Audit implication.** Runtime behavior is a defensible canonical tie-aware
  variant, but the method docstring's displayed formula is incomplete when
  ties exist: this is a documentation gap/definition-variant, not evidence of
  a runtime defect. Pre-batch tests covered ordinary, perfect
  increasing/decreasing, and partially discordant untied examples. The final
  Batch 1 characterization adds an untied hand calculation, varying-data
  ideal, equal-constant NaN behavior, and the partially tied case
  `[1,1,2]` versus `[1,2,3]`: \(P=2,Q=0,T=1,U=0\), so SciPy's documented
  tau-b formula gives \(2/\sqrt{6}\), distinctly not the no-ties \(2/3\).

### LCCC — Lin's concordance correlation coefficient

- **Canonical definition.** Lin introduced the coefficient as a reproducibility
  index measuring how paired readings conform to the 45-degree line through
  the origin
  ([L. I-K. Lin, *A Concordance Correlation Coefficient to Evaluate
  Reproducibility*, 1989, DOI 10.2307/2532051](https://doi.org/10.2307/2532051)).
  Its population form is
  \(2\operatorname{cov}(p,o)/(\sigma_p^2+\sigma_o^2+(\mu_p-\mu_o)^2)\),
  equivalently Pearson \(r\) times a location/scale accuracy factor.
- **Implemented behavior.** The repository computes the equivalent expression
  \(2r\sigma_p\sigma_o/(\sigma_p^2+\sigma_o^2+(\bar p-\bar o)^2)\) using
  population standard deviations (`ddof=0`) consistently for both series.
  It is symmetric and invariant to a common nonzero scale, but unlike Pearson
  correlation penalizes unequal means and scales. If both series are constant,
  Pearson `r` is NaN; `_safe_divide` only handles an exactly zero final
  denominator and cannot turn a NaN numerator into a defined concordance.
- **Audit implication.** The implemented algebra matches Lin's coefficient for
  nondegenerate paired data. Pre-batch tests covered an ordinary value,
  symmetry, common scaling, caching, and all-zero NaN. The final Batch 1
  characterization adds a hand calculation, varying-data ideal, equal nonzero
  constant NaN behavior, finite filtering, and all-invalid input; one-constant,
  pure-location-shift, and pure-scale-shift cases remain uncovered.

### EV — explained variance

- **Canonical definition.** The regression explained-variance score is
  \(1-\operatorname{Var}(o-p)/\operatorname{Var}(o)\), with best value 1.
  It does not penalize a systematic constant offset when the target variance
  is nonzero. For a constant target, perfect predictions and constant-offset
  predictions both have zero residual variance and therefore raw \(0/0\)
  (NaN); only varying imperfect predictions have positive residual variance
  and therefore raw negative infinity. Scikit-learn optionally maps these to
  finite convenience values
  ([scikit-learn maintainers, *Metrics and scoring: Explained variance
  score*, current documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#explained-variance-score)).
- **Implemented behavior.** `1 - var(predictions - observations) /
  var(observations)` matches the raw unweighted scalar formula, with population
  variance in numerator and denominator (the common divisor cancels). However,
  `_safe_divide` returns NaN whenever the observation variance is exactly zero.
  Thus it preserves NaN for the raw \(0/0\) perfect and constant-offset cases,
  but maps the raw negative-infinity varying-prediction cases to NaN rather
  than preserving them or adopting scikit-learn's finite mapping.
- **Audit implication.** Ordinary-data formula is consistent, while the
  constant-target policy is an implementation-specific variant that needs
  explicit documentation. Pre-batch tests asserted NaN only for an all-zero
  perfect case. The final Batch 1 characterization adds an ordinary hand
  calculation, varying-data ideal, equal nonzero constant NaN behavior,
  finite filtering, and all-invalid input; varying imperfect predictions
  against a constant target remain uncovered.

### NMSE — normalized mean square error

- **Canonical definition and variants.** “NMSE” is not a unique normalization.
  In air-quality dispersion-model evaluation, the established form examined by
  Poli and Cirillo and reviewed by Chang and Hanna is mean squared paired error
  normalized by the product of the predicted and observed means
  ([A. A. Poli and M. C. Cirillo, *On the use of the normalized mean square
  error in evaluating dispersion model performance*, 1993, DOI
  10.1016/0960-1686(93)90410-Z](https://doi.org/10.1016/0960-1686(93)90410-Z);
  [J. C. Chang and S. R. Hanna, *Air quality model performance evaluation*,
  2004, DOI 10.1007/s00703-003-0070-7](https://doi.org/10.1007/s00703-003-0070-7)).
  The 1993 primary paper specifically warns that this index can behave
  counterintuitively, so its limitations should not be hidden by the generic
  name.
- **Implemented behavior.** The method implements exactly
  \(\operatorname{mean}((p-o)^2)/(\bar p\,\bar o)\). It is zero for exact
  agreement and invariant to a common nonzero scale. `_safe_divide` returns NaN
  when either mean is exactly zero. With means of opposite sign the result is
  negative, so the frequently assumed nonnegative “error” interpretation only
  holds under a positive-product domain; no such domain validation exists.
- **Audit implication.** The implementation matches the air-quality NMSE
  variant but the name alone is ambiguous and its unrestricted negative/zero-
  mean behavior is a validation/documentation gap. Pre-batch tests covered
  only the all-zero denominator case. The final Batch 1 characterization adds
  an ordinary positive hand calculation, varying-data ideal, an observation-
  mean-zero case with nonzero error, finite filtering, and all-invalid input;
  scale invariance, opposite-sign means, and a nontrivial exact zero-mean
  agreement case remain uncovered.

## Batch-level conclusions

- `MB`, `MAE`, `MedAE`, `RMSE`, and ordinary-data `R` match their stated
  definitions after the repository's complete-case preprocessing.
- `SpearmanR` and `KendallTau` deliberately inherit SciPy semantics. The key
  missing documentation is tie behavior, especially that `KendallTau` is
  tau-b despite a simplified no-ties formula in its docstring.
- `LCCC` matches Lin's agreement coefficient on nondegenerate data and should
  not be described as interchangeable with Pearson correlation.
- `EV` matches the raw formula on nonconstant observations but deliberately
  collapses every zero-variance denominator to NaN.
- `NMSE` matches a recognized air-quality definition, but “NMSE” has multiple
  field-specific normalizations and this variant needs positive-mean domain
  caveats to retain a nonnegative error interpretation.
