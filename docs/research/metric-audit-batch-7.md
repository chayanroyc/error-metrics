# Metric audit research — Batch 7

Metrics: `RNMBF`, `CPI`, `RED`, `FoM`, `MSDdec`, `SS`, `AD`, `KLD`, `MPE`, and `MAPE`.

This note separates the formulas implemented in `error_metrics/core.py` from published definitions. The implementation first flattens equal-shaped inputs and removes every pair containing a non-finite value. Unless noted otherwise, all means and sums below therefore operate on the remaining paired finite samples.

## Findings by metric

### RNMBF — Relative Normalized Mean Bias Factor

- **Implemented:** `NMBF = mean(prediction) / mean(observation)` through `_safe_divide`, then `RNMBF = |NMBF - 1|`. It is dimensionless, nonnegative for finite ratios, and zero at equal means. A zero observation mean produces `NaN`; negative means are accepted, and can yield values without the usual positive-ratio interpretation.
- **Scientific basis:** no primary source was located for the exact registered name or the exact `|mean(P)/mean(O)-1|` formula. It is simply the absolute relative deviation of the ratio of means. The audit should record the canonical definition as **unknown**, rather than equating it with the distinct, signed piecewise “normalized mean bias factor” used in air-quality literature.
- **Behavioral classification:** documentation gap/source ambiguity, not enough evidence by itself to call the arithmetic defective.

### CPI — Combined Performance Index

- **Implemented:** `CPI = (KSI_raw + OVER_raw + 2 RMSE) / 4`. The method explicitly calls `ksi(normed=False)`, `over_metric(normed=False)`, and `root_mean_squared_error()`. Raw KSI and OVER are ECDF-area integrals over the pooled sorted support and have the data's units; RMSE has the same units, so this particular sum is dimensionally coherent. CPI is invariant to common permutation of paired samples only insofar as RMSE preserves pairing; independently permuting either series leaves KSI/OVER unchanged but generally changes RMSE.
- **Published variant:** solar-resource literature defines the same weighted combination using `KSI`, `OVER`, and twice **relative RMSD** so all terms are normalized percentages. Fernández-Peruchena et al. give `CPI = (KSI + OVER + 2 relRMSD)/4` and describe it as combining bias/dispersion and distribution likeness ([Remote Sensing 2020, Eq. 4](https://doi.org/10.3390/rs12132127)). The implementation instead deliberately selects the unnormalized forms of KSI/OVER and an unnormalized RMSE. This is a definition variant, not the published normalized CPI.
- **Dependencies and degeneracy:** constant pooled support makes the normed KSI/OVER denominator zero, but CPI avoids that denominator by requesting raw values. For identical constant series all three dependencies are zero, so CPI is zero. It can remain finite for unequal constant series because the raw ECDF integrals and RMSE remain defined.

### RED — Relative Euclidean Distance

- **Implemented:** `sqrt(mean(((prediction-observation)/observation)^2))`, after replacing exactly zero observations by `NaN`. It is therefore an RMS pointwise relative error, is pair-order sensitive, silently omits zero-observation pairs, returns `NaN` when every observation is zero, and accepts negative observations (the square removes the denominator sign).
- **Published metric with this name:** the Solar Forecast Arbiter defines RED from mean-bias, standard-deviation, and correlation discrepancies in quadrature: `sqrt(((mean(F)-mean(O))/mean(O))^2 + ((sd(F)-sd(O))/sd(O))^2 + (corr-1)^2)` ([EPRI Solar Forecast Arbiter metric documentation](https://forecastarbiter.epri.com/metrics/)). The implemented pointwise formula is not that definition; mathematically it is MAPE's squared/RMS analogue. Record a definition variant/possible naming defect.

### FoM — Figure of Merit

- **Implemented:** `100 * sum(min(O,P)) / (sum(min(O,P)) + sum(max(O-min(O,P),0)) + sum(max(P-min(O,P),0)))`. For nonnegative inputs this reduces exactly to `100 * sum(min(O,P)) / sum(max(O,P))`, a magnitude-weighted intersection over union. `_safe_divide` makes the all-zero union return `NaN`. Negative values are not rejected and break the intersection/union interpretation; for example, the overlap sum can be negative.
- **Canonical family:** Figure of Merit in Space is the percentage intersection of observed and predicted areas divided by their union, at a fixed threshold. Warner et al. give this definition and note the more general form may sum concentrations rather than physical areas ([Journal of Applied Meteorology 2004](https://doi.org/10.1175/1520-0450(2004)043%3C0058:UOTDMO%3E2.0.CO;2)). Thus the nonnegative implemented calculation is a reasonable concentration-weighted generalization, but its zero-union and negative-input behavior need explicit documentation.

### MSDdec — Mean Square Deviation decomposition

- **Implemented return order:** a four-tuple `(MSD, SB, NU, LC)`, where `MSD = mean((P-O)^2)`, `SB = mean(P-O)^2`, `NU = (1-b1)^2 * mean((P-mean(P))^2)`, and `LC = (1-r2) * mean((O-mean(O))^2)`. The regression helper fits **observations on predictions** (`O = b0 + b1 P`) and returns its slope and coefficient of determination.
- **Canonical decomposition:** Gauch, Hwang, and Fick propose the additive partition `MSD = SB + NU + LC` into squared bias, nonunity slope, and lack of correlation ([Agronomy Journal 2003](https://doi.org/10.2134/agronj2003.1442)). The paper is the primary source for the component meanings and additivity.
- **Degeneracy:** constant predictions make the regression slope and `r2` `NaN`, so `NU` and `LC` become `NaN`; constant observations make `r2` and hence `LC` `NaN`. The method can consequently return finite `MSD`/`SB` beside non-finite decomposition components. Tests should assert tuple order explicitly and check ordinary-case additivity numerically.

### SS — Skill Score against climatology

- **Implemented:** `1 - SSE_model / SSE_climatology`, where the reference forecast is the in-sample finite-observation mean repeated at every sample. Sums rather than means are used in both numerator and denominator, so their common sample count cancels. One is perfect, zero equals the climatological reference, and negative values are worse than climatology.
- **Scientific basis:** Murphy describes mean-square-error skill scores against alternative climatological reference standards ([Monthly Weather Review 1988](https://doi.org/10.1175/1520-0493(1988)116%3C2417:SSBOTM%3E2.0.CO;2)). The implementation is the usual `1 - MSE_forecast/MSE_reference` with an in-sample mean reference.
- **Denominator:** constant observations make `SSE_climatology = 0`; `_safe_divide` then returns `NaN`, including for a perfect constant prediction. A single remaining pair is also constant and has the same result. This is an undefined reference-skill denominator, not a zero skill score.

### AD — Anderson–Darling Distance

- **Implemented:** evaluate both ECDFs on pooled sorted unique values, set `w = 1/(F_obs(1-F_obs)+1e-10)`, and return the unintegrated discrete sum `sum((F_obs-F_pred)^2 w)`. Sorting makes it invariant to the order within either input series. However, the weight uses only the observation ECDF, so swapping the prediction and observation arguments can change the value. The `1e-10` constant makes tail contributions finite but scale/sample-grid dependent.
- **Canonical comparison:** Scholz and Stephens' k-sample Anderson–Darling tests are rank statistics for testing sample homogeneity and pool the samples symmetrically ([JASA 1987](https://doi.org/10.1080/01621459.1987.10478517); [author-hosted paper](https://faculty.washington.edu/fscholz/Papers/ADk.pdf)). The implementation is neither SciPy's standardized two-sample statistic nor a symmetric distance; it is a bespoke observation-weighted ECDF discrepancy. Record a definition variant and document argument ordering.

### KLD — Kullback–Leibler Divergence

- **Implemented normalization and direction:** take absolute values elementwise, divide each vector by its own `nansum`, then compute `sum(rel_entr(obs_probability, pred_probability))`. This is `D_KL(observation || prediction)`, because SciPy defines `rel_entr(x,y)=x log(x/y)` for positive inputs ([SciPy `rel_entr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.rel_entr.html)). The originating divergence is due to Kullback and Leibler ([Annals of Mathematical Statistics 1951](https://doi.org/10.1214/aoms/1177729694)).
- **Ordering:** the entries are treated as aligned probability categories, not as unordered samples or estimated distributions. Applying the same permutation to both vectors preserves the value, but independently reordering either vector generally changes it. Swapping prediction and observation also generally changes it because KL divergence is directional.
- **Zeros and signs:** negative magnitudes lose their sign. If `obs_i > 0` and the aligned normalized prediction is zero, `rel_entr` contributes `+inf`; if `obs_i = 0`, that coordinate contributes zero. An all-zero vector divides by zero before `rel_entr`; the resulting `NaN` entries are then ignored by `nansum`, which can produce a misleading finite value (often zero). No smoothing is applied. This is not a histogram or density estimate and should not be described as permutation-invariant distribution comparison.

### MPE — Mean Percentage Error

- **Implemented:** `100 * mean((P-O)/O)` over only entries whose observations are nonzero. The sign convention is prediction minus observation: positive means average overprediction and negative means average underprediction. Signed errors can cancel. Negative observations are accepted.
- **Zero behavior:** zero-observation pairs are silently excluded from both numerator and the effective sample count. If every observation is zero, `nanmean` returns `NaN` (and may warn, depending on the NumPy/Bottleneck backend). This omission policy differs from the mathematical definition, where percentage error is undefined at zero.

### MAPE — Mean Absolute Percentage Error

- **Implemented:** `100 * mean(abs((P-O)/O))`, again silently omitting zero-observation pairs. Negative observations work algebraically because the outer absolute value makes this equivalent to division by `|O|`. It is nonnegative but unbounded, and observations close to zero can dominate it.
- **Scientific basis and zeros:** Hyndman and Koehler discuss percentage-error accuracy measures and identify degeneracy in common situations ([International Journal of Forecasting 2006](https://doi.org/10.1016/j.ijforecast.2006.03.001)). Hyndman's first-party clarification states `MAPE = 100 mean(|y-yhat|/|y|)` ([author note](https://robjhyndman.com/hyndsight/smape/)). The formula is undefined/infinite at zero observations; silently dropping those cases is an implementation policy and changes the estimand and sample count. An all-zero observation series returns `NaN` here.

## Audit implications to preserve in characterization

1. `CPI` must be tested through its three actual dependencies and with raw, not normalized, KSI/OVER.
2. `MSDdec` is a four-tuple in the exact order `(MSD, SB, NU, LC)`; ordinary data should demonstrate additivity, while constant-series data expose regression-driven `NaN` components.
3. `SS` uses the in-sample observation mean as climatology and is undefined when its climatology SSE denominator is zero.
4. `AD` ignores sample ordering but is argument-order asymmetric; `KLD` is both directional and dependent on aligned entry ordering after separate absolute-value normalization.
5. `MPE`, `MAPE`, and pointwise `RED` drop zero-observation pairs rather than raising or retaining infinite errors; all-zero observations yield `NaN`.
6. The strongest source-backed definition variants are implemented `RED` versus published RED, bespoke `AD` versus the k-sample AD statistic, raw-unit `CPI` versus normalized-percentage CPI, and aligned-vector `KLD` versus a distribution estimate.
