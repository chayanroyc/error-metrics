# Metric behavior audit, batch 3: primary-source findings

## Scope and source policy

This note covers exactly `MNAE`, `FB`, `FAE`, `MFB`, `MFE`, `MAGE`, `GMB`,
`FAC2`, `MBD`, and `RMSD`. Scientific definitions are attributed to original
papers, government guidance, or maintained standards documentation. Statements
about this repository are implementation-derived observations from
`error_metrics/core.py` and are labeled as such. Several names in this batch
are not uniquely standardized; that ambiguity is an audit finding rather than
a reason to silently select a convenient formula.

## Shared implemented contract

Implementation-derived: construction converts both inputs to floating-point
arrays, requires equal shapes, flattens them, and removes every pair for which
either member is NaN or infinite. It raises `ValueError` if no pair remains.
All ten metrics therefore operate on complete-case finite pairs before applying
their metric-specific zero, sign, and positivity rules.

## Findings by metric

### MNAE — mean normalized absolute error

- **Definition ambiguity.** No primary or authoritative source was identified
  that establishes a unique cross-disciplinary definition for the exact name
  “mean normalized absolute error.” Its canonical definition is therefore
  recorded as unknown rather than inferred from a nearby metric. The
  repository's expression is the observation-normalized
  absolute-percentage-error fraction,
  \(n^{-1}\sum_i |p_i-o_i|/o_i\), except that it is not multiplied by 100.
  For comparison only, maintained scikit-learn documentation defines MAPE with
  an *absolute* target denominator and reports a relative value, not percent
  units; that documentation does not establish an MNAE definition
  ([scikit-learn maintainers, `mean_absolute_percentage_error`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html)).
- **Implemented behavior.** Zero-observation pairs are replaced by NaN and
  omitted. The denominator is `observations`, not `abs(observations)`, so a
  negative observation contributes a negative term despite the absolute
  numerator. Consequently the result is not necessarily nonnegative. It is
  asymmetric, invariant to a common positive scale, and returns NaN when every
  observation is zero.
- **Audit implication.** On strictly positive nonzero observations it is a
  fractional MAPE-like score with ideal 0. On unrestricted real data it is not
  an absolute-error magnitude, and zero omission is an implementation-specific
  policy that can hide erroneous predictions at zero observations.

### FB — fractional bias

- **Canonical air-dispersion definition.** Chang and Hanna's review uses
  fractional bias to compare the predicted and observed *means*, conventionally
  \(2(\bar o-\bar p)/(\bar o+\bar p)\); zero is ideal and, for nonnegative
  concentration data with a positive denominator, the range is `[-2, 2]`
  ([Chang and Hanna, *Air quality model performance evaluation*, 2004](https://doi.org/10.1007/s00703-003-0070-7)).
  EPA guidance describes FB as equally weighting positive and negative bias
  estimates and notes the drawback that prediction occurs in both numerator
  and denominator
  ([U.S. EPA, *Technical Support Document for the Clear Skies Act*, 2003](https://archive.epa.gov/air/clearskies/web/pdf/aq_modeling_tsd_csa2003.pdf)).
- **Implemented behavior.** The method instead computes the mean of pointwise
  fractions, \(n^{-1}\sum_i2(p_i-o_i)/(p_i+o_i)\), with the opposite
  prediction-minus-observation sign. Thus it is algebraically the commonly
  named `MFB`/modified normalized mean bias, not ratio-of-means FB. Only a
  `0/0` pair such as `(0,0)` contributes NaN to `nanmean` and is omitted. A
  nonzero cancellation pair produces signed infinity (`(1,-1)` positive and
  `(-1,1)` negative), which is retained both alone and alongside finite terms.
  Negative data destroy the usual `[-2,2]` bound.
- **Audit implication.** This is a definition-variant and sign mismatch against
  the cited FB convention. Exact positive-data agreement is 0, but the generic
  FB label does not accurately distinguish the implemented pointwise average.

### FAE — fractional absolute error

- **Canonical relationship.** EPA guidance defines fractional error as FB's
  pointwise-style relative error with the difference replaced by its absolute
  value, so the error is nonnegative
  ([U.S. EPA, *Technical Support Document for the Clear Skies Act*, 2003](https://archive.epa.gov/air/clearskies/web/pdf/aq_modeling_tsd_csa2003.pdf)).
  In the air-quality literature this is also called fractional gross error or
  mean fractional error; the pointwise expression is
  \(n^{-1}\sum_i2|p_i-o_i|/(p_i+o_i)\)
  ([Boylan and Russell, *PM and light extinction model performance metrics*,
  2006](https://doi.org/10.1016/j.atmosenv.2005.09.087)).
- **Implemented behavior.** `FAE` computes that pointwise expression without
  enforcing nonnegative inputs. For nonnegative data, a `0/0` pair becomes NaN
  and is omitted. With negative inputs, denominators can be negative or zero:
  finite results can be negative, while either orientation of a nonzero
  cancellation pair produces positive infinity that remains in isolated and
  mixed means.
- **Audit implication.** On nonnegative concentration data it has ideal 0 and
  range `[0,2]`, subject to this implementation's omission of zero-zero pairs.
  It is numerically the same formula as repository `MFE` away from zero-zero
  pairs, but lacks `MFE`'s domain validation and uses a different zero-pair
  policy.

### MFB — mean fractional bias

- **Canonical definition.** Boylan and Russell define mean fractional bias as
  the mean of the pairwise symmetric fractions,
  \(n^{-1}\sum_i2(p_i-o_i)/(p_i+o_i)\), expressed as a percentage in their
  performance criteria; their goal and criterion are based on `±30%` and
  `±60%`, respectively
  ([Boylan and Russell, 2006](https://doi.org/10.1016/j.atmosenv.2005.09.087)).
- **Implemented behavior.** The method matches the fractional (not
  percentage-scaled) pointwise formula and explicitly rejects any negative
  prediction or observation. It assigns a zero contribution to an exact
  zero-zero pair rather than omitting it. With nonnegative data it lies in
  `[-2,2]`, is 0 at exact agreement, and reverses sign when arguments are
  exchanged.
- **Audit implication.** Formula and nonnegative concentration domain are
  consistent. The unit must be documented: `0.3`, not `30`, represents 30%.
  Its zero-zero convention is reasonable but not forced by the undefined
  algebraic fraction.

### MFE — mean fractional error

- **Canonical definition.** Mean fractional error is
  \(n^{-1}\sum_i2|p_i-o_i|/(p_i+o_i)\); Boylan and Russell express it in
  percent and propose a `50%` performance goal and `75%` criterion
  ([Boylan and Russell, 2006](https://doi.org/10.1016/j.atmosenv.2005.09.087)).
- **Implemented behavior.** The method matches the fractional pointwise
  expression, rejects negative inputs, and assigns zero to an exact zero-zero
  pair. On its admitted domain its range is `[0,2]`, ideal is 0, it is
  symmetric, and common positive scaling cancels.
- **Audit implication.** `MFE` is the domain-checked version of the same core
  formula used by `FAE`, but it differs at zero-zero pairs (`0` contribution
  versus omission) and for negative inputs (`ValueError` versus an often
  nonsensical numeric result).

### MAGE — mean absolute gross error

- **Canonical definition.** EPA model-evaluation protocol defines mean
  absolute gross error as the unnormalized mean absolute residual,
  \(n^{-1}\sum_i|p_i-o_i|\), in the data's units. It separately names the
  observation-normalized percentage statistic mean absolute normalized gross
  error (`MANGE`/`MNGE`)
  ([U.S. EPA, *Meteorological Model Evaluation Protocol*, 2002](https://www.epa.gov/sites/default/files/2020-10/documents/tesche_2002_evaluation_protocol.pdf)).
- **Implemented behavior.** `MAGE` is exactly the same implementation as
  `MNAE`: `mean(abs(pred-obs) / obs)` after omitting zero-observation pairs. It
  is not multiplied by 100 and it accepts negative observations, which create
  negative contributions.
- **Audit implication.** This is a substantive formula/name defect: the method
  implements fractional MNAE/MNGE rather than dimensional MAGE. Its ideal is 0
  only under a positive-observation interpretation. In this repository `MAGE`
  and `MNAE` are duplicate computations; neither enforces the domain that makes
  the normalized “absolute” interpretation valid.

### GMB — geometric mean bias

- **Canonical definition and domain.** Air-dispersion model evaluation uses a
  geometric mean bias (often `MG`) based on log ratios,
  \(\exp[n^{-1}\sum_i\ln(p_i/o_i)]\). A perfect set of predictions gives 1
  ([IAEA, *Atmospheric Dispersion in Nuclear Power Plant Siting and Emergency
  Planning*, TECDOC-1738](https://www-pub.iaea.org/MTCD/Publications/PDF/TE-1738_web.pdf)).
  Because real logarithms and ratios are used, both members of every included
  pair must be strictly positive.
- **Implemented behavior.** The method warns if any retained value is
  nonpositive, converts every such pair's ratio to NaN, and averages logs over
  only the remaining positive pairs. If at least one positive pair remains,
  invalid pairs are silently excluded after the warning; if none remains the
  result is NaN. Its positive-data range is `(0, +∞)`, ideal is 1, and swapping
  arguments takes the reciprocal.
- **Audit implication.** The positive-pair formula is consistent, but partial
  omission is a consequential implementation policy: the returned statistic
  may describe only a subset of the constructor's already filtered data.

### FAC2 — factor of two

- **Canonical definition and boundaries.** FAC2 is the fraction of paired
  predictions within a factor of two of observations, conventionally the
  proportion satisfying the inclusive condition
  \(0.5\le p_i/o_i\le2.0\). Chang and Hanna discuss it as a robust
  air-quality evaluation index
  ([Chang and Hanna, 2004](https://doi.org/10.1007/s00703-003-0070-7)); the
  maintained IAEA guide states that perfect predictions give FAC2 equal to 1
  ([IAEA TECDOC-1738](https://www-pub.iaea.org/MTCD/Publications/PDF/TE-1738_web.pdf)).
- **Implemented behavior.** The inequalities are inclusive, so ratios exactly
  `0.5` and `2.0` pass. The method multiplies the fraction by 100, making its
  range `[0,100]` and ideal 100 rather than the canonical fraction's `[0,1]`
  and ideal 1. Division by a zero observation yields NaN or infinity; either
  fails the Boolean interval and remains in the denominator as a failure.
  Negative equal pairs have ratio 1 and pass, even though factor-of-two
  concentration reasoning assumes positive values.
- **Audit implication.** Boundary inclusion is correct, but percentage units
  and the zero/negative policies require explicit documentation. FAC2 is not a
  distance: values outside the interval fail equally regardless of magnitude.

### MBD — mean bias difference

- **Canonical definition and normalized variant.** Solar-radiation validation
  literature defines dimensional MBD as
  \(n^{-1}\sum_i(p_i-o_i)\), with zero ideal, and reports relative MBD by
  dividing by the mean reference observation and multiplying by 100
  ([Müller et al., *Validation of the SARAH-E Satellite-Based Surface Solar
  Radiation Estimates over India*, 2018](https://doi.org/10.3390/rs10030392)).
- **Implemented behavior.** Despite its unqualified name, the method computes
  the percentage relative MBD,
  \(100\,\operatorname{mean}(p-o)/\bar o\). `_safe_divide` returns NaN when
  the observation mean is exactly zero. A negative observation mean reverses
  the ordinary over/underprediction sign interpretation.
- **Audit implication.** The formula is a recognized *relative* MBD variant,
  not dimensional MBD. It is signed and unbounded, with ideal 0 when
  \(\bar o\ne0\); its normalization and percent units should be in the name or
  documentation.

### RMSD — root mean square difference

- **Canonical definition and normalized variant.** Dimensional RMSD is
  \(\sqrt{n^{-1}\sum_i(p_i-o_i)^2}\); relative RMSD divides by the mean
  reference value and commonly multiplies by 100
  ([Müller et al., 2018](https://doi.org/10.3390/rs10030392)). It is an error
  magnitude with ideal zero on the usual positive-reference domain.
- **Implemented behavior.** The method computes percentage relative RMSD,
  \(100\sqrt{\operatorname{mean}(p-o)^2}/\bar o\), and returns NaN for an
  exactly zero observation mean. Since the denominator is not absolute, a
  negative observation mean makes the result negative even though the
  numerator is a magnitude.
- **Audit implication.** On positive-mean observations it is a recognized
  normalized RMSD with ideal 0 and range `[0,+∞)`. The unqualified `RMSD` name
  hides both normalization and percent scaling; unrestricted negative data
  violate the expected nonnegative range.

## Batch-level conclusions

- `FB` is not the conventional ratio-of-means FB: it uses a pointwise average,
  the conventional `MFB` shape, and the opposite sign to Chang and Hanna's FB.
- On nonnegative data `FAE` and `MFE` use the same pointwise absolute-fraction
  formula, while `FB` and `MFB` use the same signed pointwise formula. Their
  observable differences are domain enforcement and zero-zero handling.
- `MNAE` and `MAGE` are exact implementation duplicates. Canonical MAGE is
  instead unnormalized MAE, so `MAGE` is a formula/name defect. Their signed
  denominator makes negative observations produce negative contributions, and
  zero-observation errors are omitted.
- `GMB` is mathematically defined only for strictly positive pairs; this
  implementation warns and subsets rather than rejecting the whole input.
- `FAC2` includes both factor-of-two boundaries and reports percent. Zero
  observations count as failures; unrestricted negative pairs can pass based
  solely on their positive ratio.
- `MBD` and `RMSD` implement percent-normalized relative variants despite
  unqualified names. Both are undefined at zero observation mean, and `RMSD`
  becomes negative when that mean is negative.
