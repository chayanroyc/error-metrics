# Metric audit batch 6: primary-source notes

Scope: exactly `PHI`, `SUSE`, `OVER`, `IQR`, `STD`, `nESkew`, `nEKurt`,
`MBF`, `RMBF`, and `NMBF`. Here, \(O_i\) denotes observations, \(P_i\)
predictions/simulations, bars denote arithmetic means, and \(N\) is the
number of paired values. “Runtime” below describes the implementation being
audited, not a proposed correction.

## Histogram-distribution metrics

### `PHI`

Swain and Ballard (1991), *Color indexing*,
[doi:10.1007/BF00130487](https://doi.org/10.1007/BF00130487), introduced
histogram intersection. For two histograms \(p\) and \(o\) on the **same bin
edges**, normalized so each sums to one, the symmetric form used here is

\[
PHI=\sum_{j=1}^{B}\min(p_j,o_j)
   =1-\frac12\sum_{j=1}^{B}|p_j-o_j|.
\]

It ranges from 0 (disjoint binned support) to 1 (identical binned
probabilities), with optimum 1. The identity to total-variation distance also
shows why separate bin edges would make the comparison meaningless. The
number and placement of bins are estimator choices, not intrinsic constants;
coarse bins can hide distribution differences. The runtime's pooled-range,
equal-width edges and default `n_bins=10` are therefore explicit local
conventions. Its integer `n_bins >= 1` validation is sensible API validation,
not a restriction in the original method. A constant pooled distribution is a
valid degenerate histogram and gives 1 when both samples are that same
constant; two different constants depend on whether the requested binning
separates them.

The newer land-surface application calls the normalized overlap “Percentage
of Histogram Intersection” but reports a fraction rather than multiplying by
100: Lee et al. (2026), *Introducing the Model Fidelity Metric (MFM) for robust
and diagnostic land surface model evaluation*,
[doi:10.5194/hess-30-2651-2026](https://doi.org/10.5194/hess-30-2651-2026).
Thus “percentage” must not imply a `[0, 100]` runtime range.

### `SUSE`

Pechlivanidis et al. (2014), *Use of an entropy-based metric in multiobjective
calibration to improve model performance*,
[doi:10.1002/2013WR014537](https://doi.org/10.1002/2013WR014537), and the fuller
descriptor paper Pechlivanidis et al. (2016), *Robust informational
entropy-based descriptors of flow in catchment hydrology*,
[doi:10.1080/02626667.2014.983516](https://doi.org/10.1080/02626667.2014.983516),
define the Scaled and Unscaled Shannon Entropy difference. For histogram
probabilities \(p_j\), Shannon entropy is

\[
H(p)=-\sum_{j:p_j>0}p_j\log p_j,
\qquad
SUSE=\max\{|H^S_P-H^S_O|,|H^U_P-H^U_O|\}.
\]

The scaled term uses common bounds/edges so it responds to range as well as
shape; the unscaled term bins each series over its own range (equivalently,
after separate range scaling) so it responds to internal shape. Optimum is 0.
The cited hydrology work considers several estimators (linear bins,
equal-probability bins, multiple resolutions, and kernel density), so equal
width bins are one variant, not the unique definition. The runtime uses
natural-log entropy, common pooled equal-width edges for the scaled term,
separate equal-width edges for the unscaled term, and one resolution
`n_bins=10`.

Entropy base and normalization must be stated. Raw entropy has maximum
\(\log B\), so raw SUSE lies in \([0,\log B]\); changing log base rescales the
score. Dividing each entropy by \(\log B\) instead yields the paper's
dimensionless `[0, 1]` convention. The runtime does **not** divide by
`log(n_bins)`, so it implements the raw-natural-log variant and must not be
documented as generally bounded by 1. With one bin, or with a constant series
under its own degenerate range, entropy is 0. Consequently two different
constants can have SUSE 0 even though their locations differ; SUSE measures
entropy/variability, not ordinary paired error or location agreement.

### `OVER`

Espinar et al. (2009), *Analysis of different comparison parameters applied to
solar radiation data from satellite and German radiometric stations*,
[doi:10.1016/j.solener.2008.07.009](https://doi.org/10.1016/j.solener.2008.07.009),
defines OVER from the absolute empirical-CDF separation
\(D_N(x)=|F_P(x)-F_O(x)|\):

\[
V_c=\frac{1.63}{\sqrt N},\qquad
A_c=V_c(x_{max}-x_{min}),\qquad
OVER=\int_{x_{min}}^{x_{max}}\max(D_N(x)-V_c,0)\,dx,
\]

with normalized \(OVER_\%=100\,OVER/A_c\). The constant 1.63 is the cited 99%
two-sample KS critical coefficient, and the paper's large-sample use is for
\(N\ge35\). Raw OVER has the data's units, is nonnegative, and has optimum 0;
the normalized form is dimensionless percent and is undefined when the pooled
range is zero because \(A_c=0\). The statistic compares marginal distributions
and discards pairing/order.

The runtime is not this definition: it integrates
`max(F_prediction - F_observation, 0)` with no subtraction of \(V_c\). It is
directional, changes if prediction and observation are exchanged, and can be
positive for gaps below the KS threshold. Its `normed=True` branch still
divides by the canonical critical area, which does not restore the canonical
identity. Tests should distinguish these behaviors and pin the left-step ECDF
integration convention on the sorted union grid.

For the hand sample \(P=[0,2,4]\), \(O=[1,3,5]\), the runtime's positive
directional gaps integrate to 1; swapping prediction and observation makes
every selected directional gap zero, so runtime OVER becomes 0. The absolute
ECDF separation is only \(1/3\) at its maximum, while
\(V_c=1.63/\sqrt{3}\approx0.941\). Therefore every canonical integrand
\(\max(|F_P-F_O|-V_c,0)\) is zero and Espinar OVER is exactly 0 regardless of
orientation. This directly demonstrates both runtime asymmetry and the
missing canonical threshold rather than inferring them from formulas alone.

## Observation-only dispersion metrics

### `IQR`

The interquartile range is \(IQR=Q_{0.75}(O)-Q_{0.25}(O)\), nonnegative, in the
observation's units, and 0 for a constant sample. Sample quantiles have multiple
valid conventions. The runtime delegates to `numpy.percentile` without a
`method`, hence uses NumPy's default `method="linear"` (Hyndman--Fan type 7):
for sorted \(y\), interpolate at \(q(N-1)\) between adjacent values. This must
be characterized for short/even samples because another quartile convention
can return a different IQR. See the official
[NumPy percentile documentation](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html).

### `STD`

The runtime computes observation population standard deviation

\[
STD=\sqrt{\frac1N\sum_{i=1}^{N}(O_i-\bar O)^2},
\]

because `bottleneck.nanstd` defaults to `ddof=0`; the alternative sample
standard deviation uses divisor \(N-1\). See Bottleneck's official
[function reference](https://bottleneck.readthedocs.io/en/latest/reference.html#bottleneck.nanstd).
It is nonnegative, has the observation's units, and is 0 for a nonempty
constant series. Repository preprocessing removes nonfinite pairs first, so
the later “ignore NaN” behavior is normally moot.

## Normalized-error moments

No primary source located in this audit defines metrics named `nESkew` or
`nEKurt`. Correndo et al. (2021),
[doi:10.1016/j.agsy.2021.103194](https://doi.org/10.1016/j.agsy.2021.103194),
is *Revisiting linear regression to test agreement in continuous
predicted-observed datasets* and supports the repository's SMA regression
material; neither its identity nor the official `metrica` documentation
establishes these two names or the runtime normalization. The attribution
“Correndo et al. 2021” should therefore be treated as unverified for these
metrics.

The runtime first defines

\[
nE_i=\frac{P_i-O_i}{\max_j P_j}.
\]

This requires a finite, nonzero prediction maximum. A positive scale factor
does not change skewness or kurtosis; a negative maximum reverses skewness's
sign but not kurtosis. Thus the normalization is largely redundant for moments
and introduces a zero-maximum failure. Perfect predictions produce a constant
zero `nE` sample, whose standardized moments are undefined (zero variance),
not an optimum numerical score.

`nESkew` is SciPy's bias-corrected adjusted Fisher--Pearson coefficient

\[
G_1=\frac{\sqrt{N(N-1)}}{N-2}\frac{m_3}{m_2^{3/2}},\qquad
m_k=\frac1N\sum_i(nE_i-\overline{nE})^k,
\]

because the runtime calls `scipy.stats.skew(..., bias=False)`. It requires at
least three finite errors and nonzero variance. Zero indicates symmetry, not
model perfection; its range is context-dependent. See SciPy's official
[`skew` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html).

`nEKurt` calls `scipy.stats.kurtosis(..., fisher=True, bias=False)`: it is the
bias-corrected **Fisher excess kurtosis**, based on k-statistics, so a normal
population's reference is 0 rather than the Pearson value 3. It requires at
least four finite errors and nonzero variance and is unbounded above (with a
sample-size-dependent lower bound). See SciPy's official
[`kurtosis` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html).
Neither moment has a universal “lower is better” interpretation.

## Bias-factor metrics and name variants

### `MBF` and `RMBF`

The runtime defines

\[
MBF=\frac{\bar P}{\bar O},\qquad RMBF=|MBF-1|,
\]

and rejects either mean unless it is strictly positive. Under this local
orientation MBF is positive with optimum 1; values above/below 1 indicate mean
over/underprediction. RMBF is nonnegative with optimum 0 but is asymmetric in
factor space: twofold overprediction gives 1, while twofold underprediction
gives 0.5.

“Mean bias factor” has an orientation variant. For example, the precipitation
validation literature also defines MBF as
\(\sum O_i/\sum P_i=\bar O/\bar P\), the reciprocal of this runtime. Therefore
the prediction/observation orientation must always accompany the name; see
Tan et al. (2024), *Assessing precipitation event characteristics throughout
North Carolina derived from GPM IMERG data products*,
[doi:10.3389/frwa.2024.1296586](https://doi.org/10.3389/frwa.2024.1296586).
No authoritative source was located for `RMBF=abs(MBF-1)` under the expanded
name “Relative Mean Bias Factor”; it should be recorded as a local derived
metric, not conflated with the symmetric NMBF below.

### `NMBF`

Yu et al. (2006), *New unbiased symmetric metrics for evaluation of air quality
models*, [doi:10.1002/asl.125](https://doi.org/10.1002/asl.125), defines the
Normalized Mean Bias Factor for positive means as

\[
B_{NMBF}=\begin{cases}
\bar P/\bar O-1,&\bar P\ge\bar O,\\
1-\bar O/\bar P,&\bar P<\bar O.
\end{cases}
\]

Its optimum is 0 and range is \(( -\infty,\infty )\). Positive values mean
overprediction by factor \(B_{NMBF}+1\); negative values mean underprediction
by factor \(1-B_{NMBF}\). This piecewise form is symmetric in factor magnitude:
twofold overprediction gives +1 and twofold underprediction gives -1.

Gustafson and Yu (2012), *Generalized approach for using unbiased symmetric
metrics with negative values*,
[doi:10.1002/asl.393](https://doi.org/10.1002/asl.393), states that the original
form is valid only for positive means and extends it using absolute mean
magnitudes when both means are negative. Opposite-sign means have no meaningful
factor comparison and are reported not applicable; zero means likewise make a
ratio undefined.

The runtime `NMBF` returns only \(\bar P/\bar O\), without subtracting 1 or
using the underprediction branch. It is therefore identical to runtime `MBF`
on positive means (apart from MBF's validation), has apparent optimum 1, and is
not the primary-source NMBF. Zero observed mean yields safe-divide nonfinite
behavior; negative and opposite-sign means are accepted even though the factor
interpretation does not apply.

The reciprocal hand cases make the distinction concrete. With positive means
\(\bar P=1.5\), \(\bar O=3\), runtime MBF and NMBF both return \(1/2\), while
runtime RMBF returns \(|1/2-1|=1/2\); canonical Yu NMBF would return
\(1-3/1.5=-1\). With both means negative, \(\bar P=-1.5\) and \(\bar O=-3\),
runtime MBF/RMBF reject the means but runtime NMBF again returns the raw signed
ratio \(1/2\). Gustafson and Yu explicitly handle same-sign negative means via
absolute magnitudes in an extension of the piecewise canonical metric. The
test records the runtime result and this scientific distinction; it does not
implement or call the canonical extension.

## Audit-critical findings to verify

1. `OVER` omits the KS critical threshold and uses a directional rather than
   absolute CDF gap; it is not Espinar et al.'s OVER.
2. Runtime `NMBF` is a raw mean ratio, not Yu et al.'s piecewise normalized
   symmetric factor bias; on positive means it duplicates runtime `MBF`.
3. `SUSE` uses raw natural-log entropy, so its upper scale is `log(n_bins)`,
   not 1, and the bin estimator/resolution is part of the definition.
4. The Correndo et al. attribution for `nESkew`/`nEKurt` is unverified; their
   exact behavior instead comes from a local normalized error plus SciPy's
   bias-corrected Fisher moment conventions.
5. `RMBF=abs(MBF-1)` appears to be a local derived metric and is asymmetric
   between reciprocal over- and underprediction factors.
6. `IQR` is NumPy type-7 linear interpolation and `STD` is population
   (`ddof=0`) standard deviation; both choices must be explicit.
