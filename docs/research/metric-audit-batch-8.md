# Metric audit research — Batch 8

Metrics: `sMAPE`, `CRPS`, `TAcc`, `U2`, `BM`, `dCor`, `lambda`,
`iqRMSE`, `SMA`, and `RNP`.

This note distinguishes the formulas implemented in `error_metrics/core.py`
from published definitions. The implementation first flattens equal-shaped
inputs and removes every pair containing a non-finite value. Unless noted
otherwise, all means, variances, ranks, and distance matrices below therefore
use the remaining paired finite samples.

## Findings by metric

### `sMAPE` — Symmetric Mean Absolute Percentage Error

- **Implemented:**
  \(100N^{-1}\sum_i |P_i-O_i|/[(|O_i|+|P_i|)/2]\), equivalently
  \(200N^{-1}\sum_i |P_i-O_i|/(|O_i|+|P_i|)\). A pair for which both
  values are zero is changed to `NaN` and omitted from the mean. On all other
  finite pairs each term is in `[0, 200]`; negative values are accepted because
  both denominator terms are absolute. If every pair is `(0, 0)`, the result is
  `NaN`, rather than the natural limiting/perfect-agreement value zero.
- **Scientific basis and variants:** Makridakis proposed a symmetric
  percentage error to remove the observation-only denominator of MAPE
  ([Makridakis 1993](https://doi.org/10.1016/0169-2070(93)90079-3)). Hyndman's
  first-party historical analysis documents multiple incompatible formulas
  called sMAPE, including missing absolute values in the denominator and
  factors of 100 versus 200
  ([Hyndman, “Errors on percentage errors”](https://robjhyndman.com/hyndsight/smape/)).
  The runtime is the absolute-denominator, `[0, 200]` variant. Its omission of
  `(0,0)` pairs is a local policy, not part of the mathematical definition.

### `CRPS` — Continuous Ranked Probability Score

- **Canonical definition:** for predictive CDF \(F\) and realized value \(x\),
  the loss-oriented score is
  \(\int_{-\infty}^{\infty}(F(y)-\mathbf 1\{y\ge x\})^2\,dy\).
  It is proper, nonnegative in this orientation, has the observation's units,
  and is zero for a perfect point mass. For finite-first-moment distributions
  it is also \(E|X-x|-\tfrac12E|X-X'|\). Gneiting and Raftery state explicitly
  that a deterministic (point-mass) forecast reduces CRPS to absolute error
  ([JASA 2007, §4.2](https://doi.org/10.1198/016214506000001437);
  [author-hosted paper](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf)).
- **Implemented:** simply calls paired MAE. This is canonical **only if each
  prediction is interpreted as a deterministic point-mass forecast** and the
  returned value averages CRPS over forecast cases. The API accepts no CDF,
  ensemble, samples-per-case, or distribution parameters, so it is not a
  general probabilistic CRPS implementation. Record a documentation gap rather
  than an arithmetic defect under the deterministic interpretation.

### `TAcc` — Trend Accuracy

- **Implemented:** independently fit least-squares slopes against the compressed
  sample index and return
  \(1-|b_O-b_P|/(|b_O|+10^{-10})\). It is asymmetric, dimensionless, one for
  equal fitted slopes, unbounded below, and can be very negative when the
  observation slope is zero or nearly zero. It compares only global linear
  slopes, not the signs of adjacent changes. `numpy.polyfit` fails on an empty
  series and cannot meaningfully fit a one-point slope; removed invalid pairs
  compress time and trigger a runtime warning.
- **Scientific basis:** no primary source was located for the exact name and
  formula. It must not be silently equated with directional/trend accuracy
  measures that count correctly predicted successive changes. Canonical
  definition should be recorded as unknown, with the implemented formula fully
  documented.

### `U2` — registered as Theil's U2 coefficient

- **Implemented:** \(RMSE(P,O)/\sqrt{N^{-1}\sum_i O_i^2}\). It is a normalized
  RMSE of levels: zero is perfect, it is nonnegative and unbounded, and it is
  `NaN` when observations have zero RMS. It does not use time differences or a
  naïve forecast.
- **Published U2:** Theil's second inequality coefficient compares forecast
  RMSE with the RMSE of a no-change forecast, commonly
  \(\sqrt{\sum_{t=2}^N(P_t-O_t)^2/\sum_{t=2}^N(O_t-O_{t-1})^2}\) (with
  relative-change variants also reported). Thus 1 means parity with the naïve
  forecast, below 1 is better, and above 1 is worse. This interpretation and
  denominator are documented in an institutional applied source citing Theil
  ([World Bank report, §7.3](https://documents.worldbank.org/curated/en/668141468766790899/pdf/multi-page.pdf))
  and the competing U1/U2 specifications are reviewed by Cook
  ([Economics Network](https://economicsnetwork.ac.uk/showcase/cook_theil)).
  The runtime formula has no naïve baseline and is therefore a strong
  definition/name variant, not canonical U2.

### `BM` — Berry–Mielke agreement index

- **Implemented:** for configurable `c` (default 2),
  \(\delta=N^{-1}\sum_i|P_i-O_i|\),
  \(\mu=cN^{-2}\sum_{i,j}|P_j-O_i|\), and \(BM=1-\delta/\mu\).
  The cross-distance denominator is symmetric under swapping series, while the
  paired numerator makes common pairing significant. Perfect identical data
  have both `delta=0` and `mu=0`, and runtime returns `NaN`. No validation is
  applied to `c`: zero returns `NaN`, and a negative value reverses the intended
  reference scale.
- **Scientific basis:** Mielke's permutation-based agreement family uses the
  paired deviation divided by a reference deviation formed from every
  cross-pair. Duveiller, Fasbender, and Meroni reproduce the general family and
  explain its symmetry and permutation baseline
  ([Scientific Reports 2016, background equations](https://doi.org/10.1038/srep19401)).
  Berry and Mielke's interval/multiple-rater generalization is the originating
  agreement literature
  ([Educational and Psychological Measurement 1988](https://doi.org/10.1177/0013164488484007)).
  The audit should retain `c=2` as an explicit runtime convention and avoid
  claiming behavior for arbitrary `c` as canonical.

### `dCor` — Distance Correlation

- **Canonical sample statistic:** construct Euclidean distance matrices
  \(a_{ij}=|O_i-O_j|\), \(b_{ij}=|P_i-P_j|\), double-center them to `A` and
  `B`, set \(V_N^2(O,P)=N^{-2}\sum_{ij}A_{ij}B_{ij}\), and normalize by the
  two distance variances. The empirical distance correlation is the square
  root of that normalized squared quantity, with value zero when either
  distance variance is zero. This is Definition 5 of Székely, Rizzo, and
  Bakirov ([Annals of Statistics 2007](https://doi.org/10.1214/009053607000000505);
  [paper PDF](https://pages.stat.wisc.edu/~wahba/stat860/pdf1/szekely.rizzo.bakirov.2007.pdf)).
- **Implemented:** matches the original biased/V-statistic sample estimator:
  full `N x N` Euclidean distance matrices, ordinary double-centering, and the
  square-root normalization. It returns `NaN` for fewer than two pairs and 0
  when either series is constant. A shared permutation of pairs preserves it;
  independently permuting one series generally changes it. The population
  statement “zero iff independent” must not be overread as a finite-sample
  guarantee, and newer unbiased/U-centered estimators are distinct variants.

### `lambda` — Duveiller agreement coefficient

- **Implemented:**
  \(1-MSE/[\sigma_O^2+\sigma_P^2+(\bar O-\bar P)^2]\), using population
  variances. Algebraically this is Lin's concordance correlation coefficient,
  \(2\operatorname{cov}(O,P)/[\sigma_O^2+\sigma_P^2+(\bar O-\bar P)^2]\),
  whenever the denominator is nonzero. Runtime special-cases a zero denominator
  to 1, so two identical constants return 1. It is symmetric and can be
  negative for negative covariance.
- **Canonical corrected lambda:** Duveiller et al. add a nonnegative covariance
  correction `kappa` to the denominator; it is zero for nonnegative covariance
  and offsets negative covariance so lambda remains zero rather than negative.
  Consequently lambda equals CCC when correlation is nonnegative, remains in
  `[0,1]`, and downweights correlation for magnitude bias
  ([Scientific Reports 2016](https://doi.org/10.1038/srep19401)). The authors'
  2022 correction gives the corrected equation explicitly and notes that
  `kappa` is **not** multiplied by `1/N`
  ([Author Correction](https://doi.org/10.1038/s41598-022-23771-z)). The runtime
  omits `kappa`; it matches canonical lambda only for nonnegative covariance and
  is a definition variant for negatively correlated data.

### `iqRMSE` — Inter-quartile normalized RMSE

- **Implemented and documented definition:**
  \(iqRMSE=RMSE/[Q_{0.75}(O)-Q_{0.25}(O)]\). The `metrica` authors document
  exactly this normalization
  ([metrica metric catalogue](https://adriancorrendo.github.io/metrica/articles/available_metrics_regression.html);
  [function documentation](https://rdrr.io/github/adriancorrendo/metrica/man/iqRMSE.html)).
  It is dimensionless, nonnegative, scale-invariant under nonzero common
  scaling, and zero is ideal.
- **Runtime conventions:** observation quartiles use NumPy's default linear
  sample-percentile interpolation. If observation IQR is zero, runtime returns
  positive infinity unconditionally—even when RMSE is zero—so identical
  constant series yield `inf`. This is an explicit degeneracy policy rather
  than a finite canonical score. The direct reciprocal measure `IQR/RMSE` is
  often called RPIQ, so the direction must be kept explicit.

### `SMA` — Standard Major Axis regression metrics

- **Implemented return order:** `(slope, intercept, MSE, MLA, MLP, PLA, PLP)`.
  It uses population standard deviations and Pearson `r`, replacing an
  undefined `r` with zero. The line is prediction on observation:
  \(b=\operatorname{sign}(r)s_P/s_O\), \(a=\bar P-b\bar O\). The decomposition
  is \(MLA=(\bar P-\bar O)^2+(s_P-s_O)^2\),
  \(MLP=2s_Ps_O(1-r)\), with percentages `100*component/MSE`. These components
  add to MSE algebraically when the same population moments and correlation are
  defined.
- **Scientific basis:** Correndo et al. advocate symmetric regression for
  predicted-observed agreement and the accuracy/precision decomposition
  ([Agricultural Systems 2021](https://doi.org/10.1016/j.agsy.2021.103194)).
  The authors' metric catalogue gives the same MLA and MLP formulas and SMA
  coefficients
  ([metrica catalogue](https://adriancorrendo.github.io/metrica/articles/available_metrics_regression.html)).
  For constant observations runtime forces slope to 0; for constant series the
  substituted `r=0` creates finite local conventions rather than a meaningful
  SMA fit. Perfect agreement returns percentages `(0,0)` rather than undefined
  `0/0` shares.

### `RNP` — Non-parametric Kling–Gupta efficiency

- **Canonical definition and tuple meanings:** Pool, Vis, and Seibert replace
  KGE's Pearson correlation with Spearman rank correlation and replace the
  standard-deviation variability ratio with similarity of normalized sorted
  flow-duration curves, retaining the mean ratio. The resulting efficiency is
  \(1-\sqrt{(r_s-1)^2+(\alpha_{NP}-1)^2+(\beta-1)^2}\), with
  \(\beta=\bar P/\bar O\) and
  \(\alpha_{NP}=1-\tfrac12\sum_i|P_{(i)}/(N\bar P)-O_{(i)}/(N\bar O)|\).
  See Pool, Vis, and Seibert
  ([Hydrological Sciences Journal 2018](https://doi.org/10.1080/02626667.2018.1552002)).
- **Implemented:** matches those formulas and returns the four-tuple
  `(RNP, r_s, alpha_NP, beta)`. The FDC component ignores time ordering, while
  Spearman correlation preserves paired ordering. Zero means make normalized
  FDCs nonfinite and/or beta undefined; tied or constant series make Spearman
  correlation `NaN`, which propagates to RNP even when other components are
  finite. Negative means are accepted algebraically but lose the usual
  nonnegative-flow interpretation.

## Audit implications to preserve in characterization

1. Treat runtime CRPS as deterministic-average CRPS/MAE, not as support for a
   general predictive distribution interface.
2. Distinguish runtime normalized level RMSE from canonical naïve-baseline U2,
   and runtime CCC-like `lambda` from corrected Duveiller lambda at negative
   correlation.
3. Pin sMAPE's `(0,0)` omission, iqRMSE's zero-IQR `inf`, BM's perfect-constant
   `NaN`, and RNP's constant/tied-series rank failures.
4. Characterize `dCor` with its full distance matrices and shared-versus-
   independent permutations; it is the original biased estimator.
5. Preserve tuple order and component meanings exactly for SMA and RNP.
6. Record TAcc's canonical source as unknown; its asymmetric fitted-slope
   formula must not be relabeled as directional accuracy.
