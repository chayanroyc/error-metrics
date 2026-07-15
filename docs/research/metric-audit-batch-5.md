# Metric audit batch 5: primary-source notes

Scope: exactly `KGE`, `KGE2012`, `KGEdp`, `DE`, `LME`, `LCEf`, `WIA`,
`WIAr`, `LCE`, and `KSI`. Here, (O_i) denotes observations, (P_i)
predictions/simulations, bars denote means, (s) denotes standard deviation,
and (r) is Pearson correlation. Equations below use prediction/observation
orientation, matching the library.

## KGE-family component definitions

| Metric | Original source | Definition and audit implications |
|---|---|---|
| `KGE` | Gupta, Kling, Yilmaz, and Martinez (2009), *Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling*, [doi:10.1016/j.jhydrol.2009.08.003](https://doi.org/10.1016/j.jhydrol.2009.08.003) | (1-\sqrt{(r-1)^2+(\alpha-1)^2+(\beta-1)^2}), with **variability ratio** (\alpha=s_P/s_O), **bias ratio** (\beta=\bar P/\bar O), and correlation (r). Thus constant (O) makes (\alpha) undefined; either constant series makes (r) undefined; zero (\bar O) makes (\beta) undefined/infinite. The natural component return is `(score, r, alpha, beta)`. |
| `KGE2012` (KGE′) | Kling, Fuchs, and Paulin (2012), *Runoff conditions in the upper Danube basin under an ensemble of climate change scenarios*, [doi:10.1016/j.jhydrol.2012.01.011](https://doi.org/10.1016/j.jhydrol.2012.01.011) | Same Euclidean form, but the variability component is **CV ratio** (\gamma=CV_P/CV_O=(s_P/\bar P)/(s_O/\bar O)), while (\beta=\bar P/\bar O). This must not be described as the original KGE (\alpha=s_P/s_O). Zero in either mean can make the CV term undefined even where original KGE's variability ratio is defined. The library calls this component `alpha`, but semantically it is the paper's (\gamma). |
| `KGEdp` (KGE″) | Tang, Clark, and Papalexiou (2021), *SC-Earth: A Station-Based Serially Complete Earth Dataset from 1950 to 2019*, [doi:10.1175/JCLI-D-21-0067.1](https://doi.org/10.1175/JCLI-D-21-0067.1) | (1-\sqrt{(r-1)^2+(\alpha-1)^2+\beta_n^2}), with (\alpha=s_P/s_O) and **normalized additive bias** (\beta_n=(\bar P-\bar O)/s_O), whose ideal is 0 (not 1). This avoids division by a near-zero observed mean, but not by zero observed standard deviation; constant series also destroy (r). Return `(score, r, alpha, beta_n)` and document the different ideal for the final component. |

The KGE variants are unbounded below and have optimum 1. Their components
are not interchangeable: 2009 uses standard-deviation ratio, 2012 uses
coefficient-of-variation ratio, and KGE″ returns to standard-deviation ratio
while replacing multiplicative mean bias by additive bias normalized by
observed standard deviation.

## Other efficiency/agreement metrics

### `DE`

Schwemmle, Demand, and Weiler (2021), *Technical note: Diagnostic efficiency –
specific evaluation of model performance*,
[doi:10.5194/hess-25-2187-2021](https://doi.org/10.5194/hess-25-2187-2021),
defines an **error/distance**

\[
DE=\sqrt{\bar B_{rel}^{2}+|B_{area}|^2+(r-1)^2},
\]

where (B_{rel}(i)=(Q_{sim}(i)-Q_{obs}(i))/Q_{obs}(i)) on independently
sorted flow-duration curves, (\bar B_{rel}) is constant error,
(B_{res}=B_{rel}-\bar B_{rel}), and

\[
|B_{area}|=\int_0^1 |B_{res}(i)|\,di.
\]

The paper's optimum is **0**, not 1, and its error distance is unbounded above.
The runtime's `1 - sqrt(...)` is an implementation-specific transformation;
this audit found no primary support for publishing that transformed score under
the same DE identity. Division by FDC
observations requires positive/nonzero flow; the paper explicitly says its
dynamic-error construction limits applicability to perennial streamflow.
Constant time series make (r) undefined. A useful component tuple is
`(DE or DE_prime, r, abs_B_area, mean_B_rel)`, with the score convention explicit.

### `LME`

Dedi Liu (2020), *A rational performance criterion for hydrological model*,
[doi:10.1016/j.jhydrol.2020.125488](https://doi.org/10.1016/j.jhydrol.2020.125488),
defines Liu Mean Efficiency

\[
LME=1-\sqrt{(r\alpha-1)^2+(\beta-1)^2},\qquad
\alpha=s_P/s_O,\quad\beta=\bar P/\bar O.
\]

The product (r\alpha) is the least-squares slope of predictions regressed on
observations (with an intercept). Constant observations make (\alpha) and the
slope undefined; either constant series makes (r) undefined; zero observed
mean makes (\beta) undefined. The criterion has non-unique perfect solutions
because only the product (r\alpha), rather than both terms independently, is
constrained. Return `(LME, r, alpha, beta, r_alpha)` if exposing components.

### `LCEf`

Lee and Choi (2022), *A rebalanced performance criterion for hydrological model
calibration*, [doi:10.1016/j.jhydrol.2021.127372](https://doi.org/10.1016/j.jhydrol.2021.127372),
calls the proposed metric **Least-squares Combined Efficiency (LCE)**:

\[
LCE=1-\sqrt{(r\alpha-1)^2+(r/\alpha-1)^2+(\beta-1)^2}.
\]

The library's `LCEf` name is useful only to disambiguate this metric from its
existing Legates `LCE`; it is not the paper's acronym. The two slopes correspond
to both regression directions. Consequently (s_O=0), (s_P=0), either
constant series, or (\bar O=0) causes an undefined/infinite component.
Return `(score, r, alpha, beta, r_alpha, r_over_alpha)`.

### `WIA`

Willmott (1981), *On the validation of models*,
[doi:10.1080/02723646.1981.10642213](https://doi.org/10.1080/02723646.1981.10642213),
introduced the index of agreement

\[
d=1-\frac{\sum(P_i-O_i)^2}
{\sum(|P_i-\bar O|+|O_i-\bar O|)^2}.
\]

Its intended range is [0, 1], optimum 1. If observations and predictions are
both the same constant, numerator and denominator are both zero; the formula
does not itself define that perfect-looking case. Squaring makes the index
sensitive to extremes, one motivation for later refinements.

### `WIAr`

Willmott, Robeson, and Matsuura (2012), *A refined index of model performance*,
[doi:10.1002/joc.2419](https://doi.org/10.1002/joc.2419), defines, with (c=2),
(A=\sum|P_i-O_i|), and (B=c\sum|O_i-\bar O|),

\[
d_r=\begin{cases}1-A/B,&A\le B,\\B/A-1,&A>B.\end{cases}
\]

The range is [-1, 1] and optimum 1. The second branch is **`B/A - 1`**, not
`1 - B/A`; the latter incorrectly remains nonnegative. If observations are
constant, (B=0): exact constant agreement gives (0/0), while any nonzero
absolute error belongs to the second branch and gives -1.

### `LCE`

Legates and McCabe (1999), *Evaluating the use of “goodness-of-fit” measures in
hydrologic and hydroclimatic model validation*,
[doi:10.1029/1998WR900018](https://doi.org/10.1029/1998WR900018), presents the
absolute-error modification of coefficient of efficiency,

\[
E_1=1-\frac{\sum|P_i-O_i|}{\sum|O_i-\bar O|}.
\]

`LCE` is a library alias/name rather than the paper's symbol. Its optimum is 1
and it is unbounded below. Constant observations make the denominator zero;
the primary equation supplies no special-case convention.

## `KSI`

Espinar et al. (2009), *Analysis of different comparison parameters applied to
solar radiation data from satellite and German radiometric stations*,
[doi:10.1016/j.solener.2008.07.009](https://doi.org/10.1016/j.solener.2008.07.009),
defines the Kolmogorov–Smirnov test integral as the area between two empirical
CDFs:

\[
KSI=\int_{x_{min}}^{x_{max}} |F_O(x)-F_P(x)|\,dx.
\]

The normalized percentage is (100KSI/a_{critical}), with
(a_{critical}=V_c(x_{max}-x_{min})) and, at the cited 99% confidence level,
(V_c=1.63/\sqrt N). Optimum is 0. The source describes numerical integration
over the discrete CDF grid (and permits trapezoidal integration); a left-step
sum on the sorted union of all sample values is also exact for right-continuous
ECDF step functions. Tests should pin the chosen endpoint convention and the
grid `unique(concatenate(O, P))`, especially with ties.

Raw KSI has the units and scale of the evaluated variable. Normalized KSI is
undefined when the combined range is zero because its critical area is zero.
Two distinct constants have raw KSI equal to their separation and a finite
normalized score because their pooled range is nonzero. The runtime does not
validate `normed` as Boolean: any truthy value, including a nonempty string,
selects normalized output, while a falsey value selects raw output.
The usual large-sample hypothesis-test interpretation is stated for (N\ge35);
outside that setting it remains a distribution-distance score, not evidence of
a passed/failed KS hypothesis test. KSI compares marginal distributions only,
so it is invariant to time ordering and does not diagnose paired timing error.

## Audit-critical source mismatches to verify

1. `DE`: the original paper's metric is a distance with optimum 0; `1 - distance`
   is a normalized DE′ convention.
2. `WIAr`: the poor-performance branch must be `B / A - 1`, not `1 - B / A`.
3. `LCEf`: Lee and Choi name their metric LCE; `LCEf` is local disambiguation.
4. `KGE2012`: its variability component is a CV ratio (usually (\gamma)), not
   the 2009 standard-deviation ratio (\alpha).
5. `KGEdp`: its bias component has ideal 0 and is squared directly; the other
   KGE bias ratios have ideal 1.
