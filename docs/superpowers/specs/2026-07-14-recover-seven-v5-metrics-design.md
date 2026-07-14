# Recover Seven v5 Metrics Design

## Goal

Recover seven metrics present in the local `error_metrics_v5.py` reference but
missing from the packaged `error_metrics/core.py`, without replacing the
current implementation or importing v5's broader policy and metadata systems.

The seven registry abbreviations are:

- `MBF` — Mean Bias Factor
- `RMBF` — Relative Mean Bias Factor
- `MFB` — Mean Fractional Bias
- `MFE` — Mean Fractional Error
- `PHI` — Percentage of Histogram Intersection
- `NMAEp` — Normalized Mean Absolute p-Error
- `SUSE` — Scaled and Unscaled Shannon Entropy Difference

The current package has 82 unique registered abbreviations. This cycle must
finish with exactly 89 while preserving every existing entry.

## Scope boundaries

This is a controlled metric-recovery cycle, not a wholesale v5 migration.

Included:

- the seven metric methods and their registry decorators;
- one private entropy helper used only by `SUSE`;
- strict metric-local nonnegative validation for `MFB` and `MFE`;
- focused formula, error, registry, regression, build, and installation tests;
- v5 method names, abbreviations, defaults, formulas, and relevant docstrings.

Excluded:

- v5 registry metadata fields and category finalization;
- named metric groups and metadata-query APIs;
- constructor-level `nonnegative_policy` and adjustment warnings;
- v5's general minimum-sample and error-handling framework;
- re-registering `MSD`, `SB`, `NU`, or `LC`;
- changing existing `FB` or `FAE` behavior;
- splitting or otherwise refactoring the large core module;
- adding any metric other than the seven listed above.

The excluded capabilities require separate designs and implementation cycles.

## Architecture

Implement the metrics in the existing `ErrorMetrics` class in
`error_metrics/core.py`. Keep the current package exports unchanged because
the new functionality is reached through `ErrorMetrics` and `MetricRegistry`.

Create `tests/test_v5_metrics.py` for the recovered metrics. Existing tests
remain regression coverage. A final inventory test will snapshot the 82
abbreviations present before this cycle, assert that none were removed, assert
the seven new mappings, and assert a total of 89 unique registrations.

Implementation proceeds in five independently reviewed slices:

1. `MBF` and `RMBF`;
2. `MFB` and `MFE`;
3. `PHI`;
4. `NMAEp`;
5. `SUSE`, followed by final inventory and packaging verification.

Each slice starts with focused failing tests, adds only the required methods,
runs the complete suite, and ends in a separate commit before the next slice.

## Metric behavior

### MBF and RMBF

`mean_bias_factor()` returns:

```text
MBF = mean(prediction) / mean(observation)
```

Both means must be strictly positive. If either is nonpositive, the method
raises `ValueError` because the conventional multiplicative interpretation is
undefined. `relative_mean_bias_factor()` returns `abs(MBF - 1)` by calling
`mean_bias_factor()` rather than duplicating its validation.

These methods are separate from the existing `NMBF` and `RNMBF` metrics.

### MFB and MFE

`mean_fractional_bias()` returns:

```text
MFB = mean(2 * (prediction - observation) / (prediction + observation))
```

`mean_fractional_error()` returns:

```text
MFE = mean(2 * abs(prediction - observation) / (prediction + observation))
```

Both metrics require nonnegative prediction and observation samples. Either
method raises `ValueError` when any retained pair contains a negative value.
This validation is local to the method and never mutates or filters stored
arrays. A pair `(0, 0)` contributes zero using masked `numpy.divide` because
its numerator and denominator are both zero.

The existing `FB` and `FAE` methods and registry entries remain unchanged;
`FAE` does not become an alias of `MFE` in this cycle.

### PHI

`phi(n_bins=10)` builds shared histogram edges across the pooled prediction and
observation range. Each histogram is normalized to sum to one. The result is
the sum of the binwise minima and therefore lies in `[0, 1]`, where one means
identical histograms.

`n_bins` must be an integer greater than or equal to one, otherwise the method
raises `ValueError`. Despite the name, PHI returns a fraction and is not
multiplied by 100.

### NMAEp

`nmaep(p=1.0)` returns:

```text
NMAEp = mean(abs(prediction - observation) ** p) ** (1 / p)
        / abs(mean(observation))
```

`p` must be finite and strictly positive. The method raises `ValueError` for
an invalid exponent or a zero observation mean.

### SUSE

`suse(n_bins=10)` computes Shannon entropy with natural logarithms. Its scaled
component uses shared pooled-range histogram edges; its unscaled component
uses separate prediction and observation ranges. SUSE is the maximum absolute
entropy difference between those two components and is nonnegative.

`n_bins` must be an integer greater than or equal to one. The only new helper,
`_shannon_entropy(data, edges)`, computes histogram entropy while excluding
empty bins from the logarithm.

## Errors and compatibility

New direct method calls raise `ValueError` for their documented invalid
arguments or domains. Existing `get_metrics()` behavior remains responsible
for converting metric exceptions to warnings and `NaN` results when metrics
are invoked through the registry.

No existing method signature, formula, abbreviation, return shape, dependency,
constructor behavior, or package import changes in this cycle.

## Testing and verification

`tests/test_v5_metrics.py` will cover:

- `MBF` and `RMBF` against hand-calculated positive-mean examples, the perfect
  ratio, and nonpositive means;
- `MFB` and `MFE` against hand calculations, identical values, `(0, 0)` pairs,
  negative-input rejection, and unchanged `FB`/`FAE` behavior;
- `PHI` for identical and separated histograms, bounds, and invalid bin counts;
- `NMAEp` for hand-calculated `p=1` and `p=2`, invalid exponents, and zero
  observation mean;
- `SUSE` for identical distributions, differing shapes, nonnegative output,
  and invalid bin counts;
- exact registry-to-method mappings for all seven abbreviations;
- preservation of the complete pre-cycle registry snapshot and an exact final
  count of 89 unique abbreviations.

After every slice, run the new focused tests and the complete existing suite.
The final verification builds wheel and source-distribution artifacts, installs
the wheel into a clean temporary target, imports `ErrorMetrics`, and computes
at least one recovered metric.

## Success criteria

The cycle is complete when:

- all seven metrics implement the documented formulas and validation;
- all seven are uniquely registered under the intended abbreviations;
- all 82 pre-cycle registry entries remain unchanged;
- the registry contains exactly 89 unique abbreviations;
- existing `FB`, `FAE`, `MSD`, `SB`, `NU`, and `LC` exposure is unchanged;
- all focused and regression tests pass; and
- wheel, source-distribution, and clean installed-wheel smoke verification
  succeed.
