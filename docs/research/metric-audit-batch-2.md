# Metric behavior audit, batch 2: primary-source findings

## Scope and source policy

This note covers exactly `CRM`, `RE`, `EC`, `MASE`, `MAAPE`, `A10`, `CI`,
`ME`, `R2`, and `MNB`. Scientific definitions are attributed to original
papers, government guidance, or maintained project documentation. Statements
about this repository are implementation-derived observations from
`error_metrics/core.py` and are labeled as such. Several short names in this
batch are field-dependent; where no unique authoritative definition exists,
that ambiguity is itself an audit finding.

## Shared implemented contract

Implementation-derived: construction converts both inputs to floating-point
arrays, requires equal shapes, flattens them, and removes every pair for which
either member is NaN or infinite. It raises `ValueError` if no pair remains.
All ten metrics therefore operate on complete-case finite pairs. This shared
filtering is particularly consequential for `MASE`, because removing an
interior pair changes which surviving observations become adjacent, and for
the pointwise normalized metrics, because their additional zero-observation
policies are applied only after shared filtering.

## Findings by metric

### CRM — coefficient of residual mass

- **Canonical definition and sign.** In the hydrologic/model-evaluation
  literature CRM is conventionally
  \(1-\sum_i p_i/\sum_i o_i=(\sum_i o_i-\sum_i p_i)/\sum_i o_i\), so positive
  CRM denotes overall underprediction and negative CRM overprediction
  ([Loague and Green, *Statistical and graphical methods for evaluating solute
  transport models: overview and application*, 1991](https://doi.org/10.1016/0022-1694(91)90038-N)).
- **Implemented behavior.** The repository computes the numerator in the
  opposite order, \((\sum p-\sum o)/\sum o\). Its magnitude matches the
  conventional CRM for a nonzero observation sum, but its sign and
  over/underprediction interpretation are reversed. `_safe_divide` returns
  NaN when the observation sum is exactly zero; otherwise negative or
  cancellation-prone observation sums are accepted.
- **Audit implication.** This is a formula/sign defect relative to the cited
  CRM convention, not merely an undocumented choice. Exact agreement is zero
  when the observation sum is nonzero, and a common nonzero scale cancels.

### RE — relative error

- **Definition ambiguity.** “Relative error” normally describes a pointwise
  ratio, not a uniquely standardized aggregate. The maintained scikit-learn
  MAPE definition aggregates \(|o_i-p_i|/|o_i|\), returns a relative value
  rather than multiplying by 100, and uses a finite machine-level substitute
  when an observation is zero rather than omitting that pair
  ([scikit-learn maintainers, `mean_absolute_percentage_error`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html)).
- **Implemented behavior.** `RE` returns the mean of
  \(|p_i-o_i|/|o_i|\) over only the retained pairs whose observation is
  nonzero. Thus it is an unscaled MAPE-like aggregate, not a single relative
  error. Zero-observation pairs silently receive no weight; if every retained
  observation is zero, `nanmean` returns NaN (and may warn). It is
  nonnegative, asymmetric in its arguments, and invariant to a common
  nonzero scale.
- **Audit implication.** The ordinary nonzero-data formula is recognizable,
  but the generic name and zero omission are implementation-specific and must
  be documented. Omitting zeros can make an erroneous zero-observation pair
  have no effect on the score.

### EC — efficiency coefficient

- **Canonical definition.** The Nash-Sutcliffe model-efficiency coefficient is
  \(1-\sum_i(o_i-p_i)^2/\sum_i(o_i-\bar o)^2\), with 1 denoting exact
  agreement; zero means the observed mean is equally effective, and negative
  values mean it is better than the model
  ([Nash and Sutcliffe, *River flow forecasting through conceptual models part
  I*, 1970](https://doi.org/10.1016/0022-1694(70)90255-6)).
- **Implemented behavior.** `EC` implements that formula after shared
  filtering. For constant observations, including a one-pair input, the total
  sum of squares is zero and `_safe_divide` makes the result NaN even for
  exact predictions. It is unbounded below, invariant to a common nonzero
  scale and common additive shift, and is not symmetric in its arguments.
- **Audit implication.** The implementation matches the cited efficiency
  coefficient on nonconstant observations. It is also algebraically identical
  to this repository's `R2`; the duplicate names do not denote different
  computations here.

### MASE — mean absolute scaled error

- **Canonical definition.** Hyndman and Koehler define MASE by scaling each
  forecast error by the in-sample MAE of a naive forecast. For nonseasonal
  series the scale is \((T-1)^{-1}\sum_{t=2}^T|y_t-y_{t-1}|\); for seasonal
  data the seasonal-naive scale uses lag \(m\),
  \((T-m)^{-1}\sum_{t=m+1}^T|y_t-y_{t-m}|\)
  ([Hyndman and Koehler, *Another look at measures of forecast accuracy*,
  2006](https://doi.org/10.1016/j.ijforecast.2006.03.001)).
- **Implemented behavior.** The numerator is the mean absolute paired error
  and the denominator is always the mean absolute lag-1 difference of the
  filtered observations. Although the public method accepts `m`, it never
  uses it. Fewer than two surviving observations make the scale empty/NaN;
  a constant observed sequence makes it zero and returns NaN. Removing
  invalid interior pairs creates new adjacencies; the method warns when any
  pair was removed but still computes the altered baseline.
- **Audit implication.** The default `m=1` formula is consistent when the
  supplied observations are the intended ordered scaling series. Any `m != 1`
  result is a parameter-behavior defect. The API also cannot distinguish the
  forecast-evaluation sample from the in-sample training series assumed by
  the original definition.

### MAAPE — mean arctangent absolute percentage error

- **Canonical definition.** MAAPE is
  \(n^{-1}\sum_i\arctan(|(o_i-p_i)/o_i|)\). The arctangent, rather than the
  percentage error itself, bounds each contribution below \(\pi/2\); its
  angle interpretation is the defining feature
  ([Kim and Kim, *A new metric of absolute percentage error for intermittent
  demand forecasts*, 2016](https://doi.org/10.1016/j.ijforecast.2015.12.003)).
- **Implemented behavior.** The repository instead computes
  \(100\,\operatorname{mean}(q_i\arctan q_i)\), where
  \(q_i=|p_i-o_i|/|o_i|\), and omits zero-observation pairs. Multiplication by
  \(q_i\) destroys the canonical bound: contributions grow approximately
  linearly for large errors. If all observations are zero the result is NaN.
- **Audit implication.** This is a substantive formula defect, not a scaling
  variant. The docstring, implementation, stated range, and original MAAPE
  definition disagree. The canonical zero-actual limit can be interpreted as
  \(\pi/2\) for nonzero error, whereas this implementation drops the pair.

### A10 — A10 index

- **Definition ambiguity.** `A10` is not a generally standardized regression
  statistic, and no foundational or standards source was identified that
  uniquely owns this abbreviation. Applied prediction papers commonly use an
  “a10-index” for the fraction satisfying
  \(0.9\le p_i/o_i\le1.1\), but that usage does not establish a universal
  metric. The canonical definition is therefore recorded as unknown, with
  this ambiguity explained rather than inferred from an adjacent tolerance
  API. NumPy's maintained `isclose` documentation provides useful
  [tolerance and near-zero context](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html),
  but does not define or validate an A10 index. The absence of a cited domain
  definition is material because ratios require positive, nonzero
  observations.
- **Implemented behavior.** The code tests
  \(|p_i-o_i|/|o_i|\le0.1\), which is equivalent to the ratio interval for
  positive observations. A zero observation is converted to NaN, but the
  subsequent comparison produces Boolean `False`; consequently zero pairs
  count as failures rather than being omitted. Negative observations are
  accepted under an absolute-denominator interpretation. The result lies in
  `[0, 1]`, includes the 10% boundary, and is asymmetric.
- **Audit implication.** Ordinary positive-data behavior matches the common
  operational meaning. The name needs a domain citation, and zero/negative
  handling is a documentation/validation gap rather than something a generic
  `A10` label can resolve.

### CI — confidence index

- **Canonical definition and ambiguity.** In Brazilian agrometeorological
  model evaluation, the Camargo-Sentelhas confidence/performance index is
  \(c=r d\), Pearson correlation multiplied by Willmott's index of agreement;
  its qualitative classes are application conventions rather than confidence
  intervals ([Camargo and Sentelhas, *Performance evaluation of different
  methods of estimating potential evapotranspiration in the State of São
  Paulo, Brazil*, 1997](https://www.agritempo.gov.br/publish/publicacoes/X/10.pdf)).
- **Implemented behavior.** `CI` multiplies the repository's Pearson `R` by
  its original Willmott index, so it implements that particular `c` index.
  Constant inputs make `R` NaN; the Willmott denominator can also be zero.
  For finite component results, \(d\) is in `[0,1]` and \(r\) in `[-1,1]`,
  so the product is in `[-1,1]`. CI can also be NaN when correlation is
  undefined, and the unguarded agreement denominator makes exact all-zero
  inputs raise `ZeroDivisionError`. Negative finite results are possible,
  despite several published class tables only describing nonnegative ranges.
- **Audit implication.** The formula is consistent with the cited regional
  convention, but “confidence index” is an overloaded name and must not be
  presented as statistical confidence or uncertainty. Its behavior inherits
  all degeneracies of both component metrics.

### ME — max error

- **Canonical definition.** Maintained scikit-learn documentation defines max
  error as the maximum absolute residual,
  \(\max_i|o_i-p_i|\), a nonnegative loss with optimum zero
  ([scikit-learn maintainers, `max_error`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.max_error.html)).
- **Implemented behavior.** `nanmax(abs(predictions - observations))` matches
  the scalar definition after shared filtering. Since construction guarantees
  at least one finite pair, its internal NaN-aware maximum normally sees a
  nonempty finite array. It is symmetric, translation invariant, scales by
  \(|a|\), is defined for one pair, and is dominated by the single largest
  residual.
- **Audit implication.** Formula and dependency-independent behavior agree.
  The abbreviation `ME` is ambiguous in model-evaluation literature, where it
  often means mean error; the registry's full name is therefore essential.

### R2 — coefficient of determination

- **Canonical definition.** For prediction scoring, R² is
  \(1-\sum_i(o_i-p_i)^2/\sum_i(o_i-\bar o)^2\), with best value 1 and values
  below zero possible. A constant target makes the raw score nonfinite;
  scikit-learn documents an optional finite-value repair for convenience
  ([scikit-learn maintainers, `r2_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)).
- **Implemented behavior.** The method uses the raw formula and maps every
  exactly zero target-variance denominator to NaN via `_safe_divide`, both for
  perfect and imperfect constant-target predictions. It does not square
  Pearson correlation and does not fit a regression line. On nonconstant
  observations it is exactly the same computation as `EC`.
- **Audit implication.** The implementation matches prediction-score R² for
  ordinary data and deliberately differs from scikit-learn's default finite
  repair on constant targets. Documentation should prevent confusion with
  squared correlation or in-sample OLS R².

### MNB — mean normalized bias

- **Canonical definition.** Air-quality model guidance defines MNB as the
  pointwise normalized bias averaged across pairs,
  \(n^{-1}\sum_i(p_i-o_i)/o_i\), commonly multiplied by 100 for percent units.
  EPA material also warns that normalization at each observation heavily
  weights low observed values and can yield a sign that conflicts with
  absolute bias ([U.S. EPA, *Model Evaluation*, 2012](https://gaftp.epa.gov/air/aqmg/SCRAM/workshops/2012_RSL_Modelers_Workshop/Presentations/9-2_Simon_ModelEval_May4.pdf)).
- **Implemented behavior.** The repository returns the fractional, not
  percentage, form and silently omits every zero-observation pair. Nonzero
  negative observations are accepted, so usual concentration-domain range
  interpretations do not apply. It is signed, asymmetric, invariant to a
  common nonzero scale, and returns NaN when all retained observations are
  zero.
- **Audit implication.** The nonzero-data computation matches fractional MNB,
  but units and the zero-observation exclusion need explicit documentation.
  `MNB` must not be confused with `NMB`: averaging ratios is not the same as
  dividing summed error by summed observations.

## Batch-level conclusions

- `EC`, `ME`, and ordinary-data prediction-score `R2` match their cited
  formulas; `EC` and `R2` are duplicate computations in this implementation.
- `CRM` reverses the conventional coefficient's sign, `MASE` ignores its
  seasonality parameter, and `MAAPE` implements a different, unbounded
  expression. These are formula/parameter defects rather than edge-policy
  choices.
- `RE`, `A10`, and `CI` have overloaded or domain-specific names. Their exact
  operational definitions must accompany the abbreviations.
- Zero observations are handled inconsistently: `RE`, `MAAPE`, and `MNB`
  omit them, while `A10` counts them as failures. Constant observations make
  `EC`/`R2` undefined, and component degeneracy propagates through `CI`.
- `MNB` is the mean of pointwise normalized biases and is distinct from NMB;
  its low-observation sensitivity is a known reason authoritative air-quality
  guidance discourages relying on it.
