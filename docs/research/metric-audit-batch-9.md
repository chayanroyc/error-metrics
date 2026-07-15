# Metric audit research — Batch 9

Metrics: `TSS`, `MEAN`, `MEDIAN`, `CRMSE`, `MSLE`, `NMAEp`, `NAE`,
`Gini`, and `PCD`.

This note distinguishes the formulas implemented in `error_metrics/core.py`
from published definitions. The implementation first flattens equal-shaped
inputs and removes every pair containing a non-finite value. Unless noted
otherwise, all summaries and successive differences below therefore use the
remaining paired finite samples; removal also compresses a time series before
`PCD` computes changes.

## Findings by metric

### `TSS` — Taylor Skill Score

- **Implemented:** with Pearson correlation `r` and population-standard-
  deviation ratio \(q=\sigma_P/\sigma_O\),
  \(4(1+r)^4/[(q+q^{-1})^2(1+1)^4]\). It fixes the maximum attainable
  correlation \(R_0\) at 1. The score is 1 for identical nonconstant series,
  zero for perfect anticorrelation, and tends toward zero as the variance ratio
  tends to zero or infinity.
- **Scientific basis:** this is Taylor's Eq. 5 skill score with \(R_0=1\), not
  his less correlation-sensitive Eq. 4. Taylor states that \(R_0\) is the
  maximum attainable correlation and should be reported whenever the score is
  used ([Taylor 2001, Eqs. 4–5](https://doi.org/10.1029/2000JD900719);
  [paper PDF](https://www.ncl.ucar.edu/Support/talk_archives/2012/att-2214/taylor2000.pdf)).
  Calling the fixed value canonical therefore assumes perfect correlation is
  attainable.
- **Degeneracy:** one-point or constant observations make both correlation and
  the variance ratio undefined; constant predictions make correlation
  undefined and `1/q` undefined. Runtime consequently returns `NaN`, including
  for two identical constant series. With ordinary nonconstant finite data,
  the formula is nonnegative and no greater than 1.

### `MEAN` — paired summary means

- **Implemented return contract:** the two-tuple
  `(mean(observations), mean(predictions))`, in that order. These are arithmetic
  means over the retained pairs, are expressed in the inputs' units, and do not
  themselves measure prediction error. A common permutation changes neither
  component; adding a common constant adds it to both.
- **Scientific basis:** this is the ordinary arithmetic mean. NumPy defines
  `mean` as the sum of elements divided by their count
  ([NumPy `mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)).
  The abbreviation and tuple order are local API conventions, so the audit
  should characterize them rather than assign an optimization direction.

### `MEDIAN` — paired summary medians

- **Implemented return contract:** the two-tuple
  `(median(observations), median(predictions))`, in that order, over retained
  pairs. Each component is invariant to ordering and has the inputs' units.
  For an even number of values the runtime uses the arithmetic mean of the two
  middle sorted values.
- **Scientific basis:** this matches NumPy's documented median convention
  ([NumPy `median`](https://numpy.org/doc/stable/reference/generated/numpy.median.html)).
  As with `MEAN`, the tuple is a pair of descriptive summaries rather than a
  scalar accuracy metric, and the return order is a local contract.

### `CRMSE` — Centered Root Mean Square Error

- **Implemented:**
  \(\sqrt{N^{-1}\sum_i[(P_i-\bar P)-(O_i-\bar O)]^2}\). It has the
  data's units, is nonnegative, and is zero whenever predictions differ from
  observations only by an additive constant. It is invariant to adding an
  arbitrary constant to either series, so it deliberately excludes mean bias.
- **Scientific basis:** Taylor defines the centered pattern RMS difference by
  exactly this mean-removed formula and shows that full mean-square difference
  decomposes into squared bias plus squared centered RMS difference
  ([Taylor 2001, Eqs. 2–3](https://doi.org/10.1029/2000JD900719)). The runtime
  uses population divisor `N`, consistent with that definition. A single
  retained pair and identical or offset constant series all return zero; that
  is algebraically defined but contains no information about pattern variation.

### `MSLE` — Mean Squared Logarithmic Error

- **Implemented:** \(N^{-1}\sum_i[\log(1+P_i)-\log(1+O_i)]^2\), except that
  `bn.nanmean` silently omits terms that become `NaN`. On its natural real
  domain, `P,O > -1`, it is nonnegative and zero for equality. Official
  scikit-learn documentation likewise describes MSLE as a nonnegative loss
  whose best value is zero
  ([scikit-learn API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html)).
- **Negative-domain behavior:** `numpy.log1p` is finite only above `-1`: at
  exactly `-1` it is `-inf` and below `-1` it is `NaN`
  ([NumPy `log1p`](https://numpy.org/doc/stable/reference/generated/numpy.log1p.html)).
  Runtime does not validate this domain. Thus one `-1` paired with a valid
  value can yield `inf`; equal `(-1,-1)` produces `NaN` through `-inf - -inf`
  and is omitted; values below `-1` are also omitted. If all terms are omitted,
  the result is `NaN`. These operations emit the repository's known divide,
  invalid-log, and invalid-subtraction runtime warnings. Silent omission means
  this is not equivalent to an API that rejects negative targets/predictions.

### `NMAEp` — Normalized Mean Absolute p-Error

- **Implemented:** for finite real `p > 0`,
  \([N^{-1}\sum_i|P_i-O_i|^p]^{1/p}/|\bar O|\). `p=1` is MAE divided by
  absolute observation mean and `p=2` is RMSE divided by that mean. It is
  dimensionless, nonnegative, zero for perfect agreement, and invariant to a
  common nonzero scaling. Boolean, nonfinite, zero, and negative `p` values
  raise `ValueError`; an exactly zero observation mean also raises.
- **Scientific basis and terminology:** the numerator is a power mean of
  absolute errors (an `L_p`-style average), but for `0 < p < 1` it is not a
  norm because the triangle inequality fails. No primary source was located
  for the exact registered name plus absolute-mean normalization and arbitrary
  positive `p`. The formula and validation should therefore be documented as
  a local generalized normalized-error contract, not silently attributed to a
  standard named index. A mean merely close to zero is accepted and can make
  the result arbitrarily large.

### `NAE` — Normalized Absolute Error

- **Implemented:** the mean of pairwise terms
  \(|P_i-O_i|/[0.5(P_i+O_i)]\). This is a symmetric paired-sum normalization,
  algebraically related to the absolute sMAPE term but **without absolute
  values around the denominator** and without percentage scaling.
- **Denominators and range:** a nonzero pair with `P_i+O_i=0` contributes
  positive infinity, while `(0,0)` produces `0/0 = NaN` and is omitted by
  `nanmean`. Negative paired sums create negative terms, so unrestricted finite
  inputs do not guarantee nonnegativity or the commonly implied `[0,2]` range.
  If both inputs are nonnegative, finite nonzero-sum terms lie in `[0,2]`.
- **Scientific basis:** no primary source was located for the exact registered
  name and formula. Because “normalized absolute error” is used for multiple
  observation-, range-, and aggregate-normalized errors, the audit should
  preserve this exact denominator as a local definition. In particular it is
  distinct from the absolute-denominator sMAPE variants whose competing forms
  are documented by Hyndman
  ([first-party note](https://robjhyndman.com/hyndsight/smape/)).

### `Gini` — unnormalized ranking Gini score

- **Implemented:** sort samples by predictions descending, accumulate the
  corresponding observation share and population share, sum their difference
  after each sample, and divide by `N`. This exactly follows the cited Ben
  Hamner MATLAB routine
  ([author's source code](https://github.com/benhamner/Metrics/blob/master/MATLAB/metrics/gini.m)).
  The observations are treated as nonnegative “loss” mass and predictions only
  determine ordering.
- **Interpretation:** this is the **unnormalized** area-style ranking score, not
  the classical Gini coefficient of the prediction distribution and not a
  normalized ranking Gini with perfect ordering forced to 1. Its attainable
  maximum depends on the observation mass and sample size; for example the
  repository's perfectly ordered three positives among five samples scores
  `0.2`, not 1. Reverse ordering can produce a negative score. Permetrics
  explicitly distinguishes normalized ranking Gini from residual-distribution
  Gini ([official Permetrics manual, GINI section](https://permetrics.readthedocs.io/_/downloads/en/stable/pdf/)).
- **Edge cases:** total observation mass zero returns `NaN`. Negative
  observations or negative total mass destroy the usual Lorenz/ranking
  interpretation and can leave the advertised range. Prediction ties depend on
  the ordering returned by NumPy's default `argsort`; because stable ordering
  is not requested, tied scores do not have a specified tie-averaging policy.
  A shared permutation is not guaranteed to preserve a tied-score result.

### `PCD` — Prediction of Change in Direction

- **Implemented:** for `N >= 2`,
  \((N-1)^{-1}\sum_{i=2}^N I[(P_i-P_{i-1})(O_i-O_{i-1})>0]\); for one
  retained pair it returns `NaN`. This matches the documented Permetrics
  formula and its `[0,1]`, higher-is-better orientation
  ([official Permetrics manual, PCD section](https://permetrics.readthedocs.io/_/downloads/en/stable/pdf/)).
- **Flat and ordering behavior:** the strict `> 0` condition scores zero if
  either series is flat over an interval, even when both correctly remain
  flat. Permetrics identifies this flatline ambiguity explicitly. The metric is
  inherently order-dependent: reversing both series preserves successive
  direction agreement, but arbitrary shared permutation generally changes it.
  Because preprocessing removes invalid pairs first, a missing interior time
  point creates a new artificial adjacent interval between its former
  neighbors; PCD is therefore computed on compressed rather than original
  time spacing.

## Audit implications to preserve in characterization

1. Pin exact tuple order `(observation, prediction)` for both `MEAN` and
   `MEDIAN`; neither tuple has a scalar optimization direction.
2. Distinguish TSS Eq. 5 with fixed `R0=1` from Taylor Eq. 4, and characterize
   constant-series `NaN` behavior.
3. Show that CRMSE removes additive bias and that a one-point/constant pattern
   returns zero despite containing no variation information.
4. Preserve MSLE's warning-producing domain behavior: `-1`, values below `-1`,
   `inf`, and silent omission of `NaN` log-error terms are distinct cases.
5. Exercise NMAEp at `p=1`, `p=2`, a valid `0<p<1`, invalid parameters, and
   zero versus near-zero observation means.
6. Exercise NAE at `(0,0)`, opposite-sign zero sums, and negative sums; its
   denominator is not absolute.
7. Treat Gini as Hamner's unnormalized ordering score, including reverse order,
   total-zero observations, and prediction ties—not as a `[0,1]` coefficient
   with perfect score 1.
8. Pin PCD's `N<2` result, strict flatline penalty, order dependence, and
   compressed adjacency after invalid-pair removal.
