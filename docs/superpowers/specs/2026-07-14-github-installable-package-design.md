# GitHub-Installable Error Metrics Package Design

## Goal

Convert the existing `chayanroyc/error-metrics` repository into a conventional
Python package that can be installed directly from GitHub while preserving the
public API:

```python
from error_metrics import ErrorMetrics
```

The package will support Python 3.9 and newer. PyPI publication and release
automation are outside this work.

## Baseline and compatibility

The current GitHub implementation is the feature baseline because it contains
metrics added after the local `error_metrics_v2.py`. No current metric, public
method name, registry abbreviation, or return shape will be intentionally
removed or changed.

The local v2 implementation is the source for targeted robustness and
performance improvements. These changes will be merged into the current
GitHub implementation rather than replacing it wholesale.

## Package structure

The repository will use a root-level package layout:

```text
error-metrics/
├── error_metrics/
│   ├── __init__.py
│   └── core.py
├── tests/
│   └── test_error_metrics.py
├── pyproject.toml
├── README.md
└── LICENSE
```

`error_metrics.core` will hold the implementation. `error_metrics.__init__`
will explicitly export `ErrorMetrics`, `MetricRegistry`, `MetricInfo`, and any
other names required to preserve the current supported API. The existing
top-level `error_metrics.py` will be removed after its content is migrated so
there is only one import target.

The `pyproject.toml` file will contain build-system configuration, project
metadata, the `>=3.9` Python requirement, and runtime dependencies. SciPy and
Statsmodels remain required because metrics depend on them. Bottleneck becomes
an optional acceleration dependency with a NumPy fallback. Pandas will only be
listed if implementation inspection confirms a runtime use.

## Implementation behavior

The merge will preserve the full current metric set and incorporate these v2
behaviors:

- Compare the original prediction and observation shapes before flattening.
- Reject input when no valid paired values remain after preprocessing.
- Filter paired NaN and infinite values as the current API does.
- Track dropped pairs and warn when a time-ordered metric is evaluated after
  filtering has changed sequence continuity.
- Use a consistent safe-division policy for v2-covered undefined denominators,
  returning `NaN` instead of producing incidental division failures.
- Cache shared Pearson correlation, empirical CDF, and linear-regression
  calculations on each `ErrorMetrics` instance.
- Fall back to NumPy reductions when Bottleneck is not installed.
- Detect conflicting metric abbreviations while still permitting safe module
  reloads in notebook workflows.

The current implementation registers `nESkew`, `nEKurt`, `NMBF`, and `RNMBF`
more than once. Each collision will be compared and consolidated into one
canonical registered implementation before enabling strict collision checks.
Consolidation must preserve the behavior covered by the existing tests and
documented API.

Changes will be surgical: no new metrics, unrelated refactoring, or speculative
extension points are included.

## Data flow and errors

Construction converts both inputs to floating-point NumPy arrays, checks their
original shapes, flattens them, and filters invalid pairs. It then computes the
basic shared fields used by metric methods. Metric calls operate on this
validated paired data and may reuse cached shared calculations.

Invalid construction inputs raise `ValueError` with actionable messages:

- prediction and observation shapes differ; or
- preprocessing leaves no valid paired observations.

Mathematically undefined metric results follow the v2 policy and return `NaN`
where safe division applies. Filtering remains silent for order-independent
metrics. Time-ordered metrics warn when dropped pairs may alter lag or trend
interpretation.

## Testing and verification

The existing test suite will move under `tests/` and remain regression
coverage. Focused tests will be added for:

- mismatched original shapes;
- empty data after invalid-pair filtering;
- v2 zero-denominator behavior;
- operation without Bottleneck;
- registry conflicts and safe reload behavior;
- reuse of cached calculations;
- warnings from time-ordered metrics after filtering; and
- public imports from `error_metrics`.

Packaging verification will:

1. run the complete test suite;
2. build both wheel and source-distribution artifacts;
3. install the wheel in a clean temporary environment; and
4. run a smoke test using the documented import and a basic metric.

The README will document Python support, dependencies, optional Bottleneck
acceleration, the preserved quick-start API, and direct GitHub installation:

```bash
pip install git+https://github.com/chayanroyc/error-metrics.git
```

## Success criteria

The work is complete when:

- `pip install git+https://github.com/chayanroyc/error-metrics.git` is supported
  by repository metadata;
- `from error_metrics import ErrorMetrics` remains valid;
- all current metrics remain available under their existing public names;
- all existing and new focused tests pass; and
- clean build, wheel installation, import, and smoke-test verification pass.
