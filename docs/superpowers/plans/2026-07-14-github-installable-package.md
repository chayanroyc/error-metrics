# GitHub-Installable Error Metrics Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `chayanroyc/error-metrics` into a GitHub-installable Python package while preserving its current metric superset and merging the robustness and caching improvements from `error_metrics_v2.py`.

**Architecture:** Move the current implementation into `error_metrics/core.py` and re-export the supported API from `error_metrics/__init__.py`. Use `pyproject.toml` for setuptools-based installation, keep scientific dependencies minimal, and add focused regression tests before each behavioral change.

**Tech Stack:** Python 3.9+, NumPy, SciPy, Statsmodels, optional Bottleneck, setuptools, pytest, build

## Global Constraints

- Support Python 3.9 and newer.
- Preserve `from error_metrics import ErrorMetrics`.
- Preserve all current public metric methods, abbreviations, and return shapes.
- Keep the current GitHub implementation as the metric feature baseline.
- Do not add metrics, PyPI publishing, release automation, or unrelated refactoring.
- Bottleneck is optional acceleration; NumPy is the required fallback.
- Install directly with `pip install git+https://github.com/chayanroyc/error-metrics.git`.

## File map

- `error_metrics/core.py`: all metric types, registry logic, validation, shared caches, and calculations.
- `error_metrics/__init__.py`: explicit stable public exports only.
- `tests/test_error_metrics.py`: existing metric regression suite.
- `tests/test_package_api.py`: package exports and metadata-facing import behavior.
- `tests/test_v2_robustness.py`: focused v2 validation, fallback, registry, cache, warning, and safe-division tests.
- `pyproject.toml`: build backend, metadata, Python floor, runtime dependencies, optional extras, and pytest settings.
- `README.md`: GitHub installation and dependency documentation.
- `requirements.txt`: remove after dependency metadata moves to `pyproject.toml`.

---

### Task 1: Establish an honest green regression baseline

**Files:**
- Modify: `test_error_metrics.py`

**Interfaces:**
- Consumes: current top-level `error_metrics.ErrorMetrics`.
- Produces: a regression suite whose expected values match its actual fixtures and metric definitions.

- [ ] **Step 1: Record the current failures**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: `8 failed, 23 passed`. The failures are the paired NaN count, paired infinity count, Spearman expectation, Willmott expectation, fixture-name typo, distance-correlation threshold, Gini threshold, and PCD expectation.

- [ ] **Step 2: Correct assertions that contradict their fixtures or formulas**

Make these exact changes in `test_error_metrics.py`:

```python
# Each of these fixtures has only index 0 finite in both arrays.
assert len(em.predictions) == 1
assert len(em.observations) == 1

# Both sample vectors have identical increasing rank order.
assert np.isclose(error_metrics.spearman_r(), 1.0)

# Use the formula's computed value instead of a three-decimal loose estimate.
assert np.isclose(
    error_metrics.willmotts_index_of_agreement(),
    0.9964771011575239,
)

# Use the local instance; `error_metrics` is the fixture function at module scope.
dr = em.refined_index_of_agreement()

# A symmetric parabola is dependent on x but is not expected to be near 1 under
# the finite-sample distance-correlation definition.
assert 0.45 < dcor < 0.55

# For five observations containing three positives, this implementation's
# perfect-order Gini score is 0.2.
assert np.isclose(gini_perfect, 0.2)

# The increments down, down, up, down contain one match against four upward
# observation increments.
assert np.isclose(pcd_wrong, 0.25)
```

- [ ] **Step 3: Run the baseline suite**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: `31 passed`; warnings from the existing MSLE edge-case test may remain.

- [ ] **Step 4: Commit the baseline corrections**

```bash
git add test_error_metrics.py
git commit -m "test: correct inconsistent metric expectations"
```

---

### Task 2: Create the installable package boundary

**Files:**
- Create: `error_metrics/__init__.py`
- Create: `error_metrics/core.py` by moving `error_metrics.py`
- Create: `tests/test_package_api.py`
- Move: `test_error_metrics.py` to `tests/test_error_metrics.py`
- Create: `pyproject.toml`
- Delete: `requirements.txt`

**Interfaces:**
- Consumes: `ErrorMetrics`, `MetricRegistry`, and `MetricInfo` from the current module.
- Produces: `error_metrics.ErrorMetrics`, `error_metrics.MetricRegistry`, and `error_metrics.MetricInfo`; distribution name `error-metrics`, version `0.1.0`.

- [ ] **Step 1: Move source and existing tests before creating exports**

```bash
mkdir -p error_metrics tests
git mv error_metrics.py error_metrics/core.py
git mv test_error_metrics.py tests/test_error_metrics.py
```

- [ ] **Step 2: Add the failing public API test**

Create `tests/test_package_api.py`:

```python
import error_metrics
from error_metrics.core import ErrorMetrics as CoreErrorMetrics


def test_package_exports_supported_api():
    assert error_metrics.ErrorMetrics is CoreErrorMetrics
    assert error_metrics.MetricRegistry is not None
    assert error_metrics.MetricInfo is not None
    assert set(error_metrics.__all__) == {
        "ErrorMetrics",
        "MetricInfo",
        "MetricRegistry",
    }
```

- [ ] **Step 3: Verify the export test fails**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_package_api.py -q
```

Expected: collection fails because `error_metrics.ErrorMetrics` is not exported.

- [ ] **Step 4: Add explicit package exports**

Create `error_metrics/__init__.py`:

```python
"""Statistical error metrics for predictions and observations."""

from .core import ErrorMetrics, MetricInfo, MetricRegistry

__all__ = ["ErrorMetrics", "MetricInfo", "MetricRegistry"]
```

- [ ] **Step 5: Add project metadata**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "error-metrics"
version = "0.1.0"
description = "Statistical error metrics for predictions and observations"
readme = "README.md"
requires-python = ">=3.9"
license = { file = "LICENSE" }
authors = [{ name = "Chayan Roy" }]
dependencies = [
    "numpy>=1.20.0",
    "scipy>=1.7.0",
    "statsmodels>=0.13.0",
]

[project.optional-dependencies]
speed = ["bottleneck>=1.3.0"]
test = ["bottleneck>=1.3.0", "pytest>=7"]
dev = ["bottleneck>=1.3.0", "build>=1", "pytest>=7"]

[tool.setuptools.packages.find]
include = ["error_metrics*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Remove `requirements.txt`; Pandas is not imported anywhere, and runtime requirements now have one authoritative location.

- [ ] **Step 6: Run package API and regression tests**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: `32 passed`.

- [ ] **Step 7: Commit the package layout**

```bash
git add error_metrics tests pyproject.toml requirements.txt
git commit -m "feat: add installable package structure"
```

---

### Task 3: Add v2 input validation and optional Bottleneck fallback

**Files:**
- Modify: `error_metrics/core.py`
- Create: `tests/test_v2_robustness.py`

**Interfaces:**
- Consumes: array-like predictions and observations accepted by `ErrorMetrics.__init__`.
- Produces: paired flattened `numpy.ndarray` fields; `ValueError` for mismatched original shapes or no valid pairs; module-level `bn` bound to Bottleneck when available and NumPy otherwise.

- [ ] **Step 1: Write validation tests**

Create `tests/test_v2_robustness.py`:

```python
import subprocess
import sys

import numpy as np
import pytest

from error_metrics import ErrorMetrics


def test_rejects_same_size_arrays_with_different_shapes():
    with pytest.raises(
        ValueError,
        match=r"same shape; got \(2, 2\) and \(4,\)",
    ):
        ErrorMetrics(np.ones((2, 2)), np.ones(4))


def test_rejects_input_with_no_valid_pairs():
    with pytest.raises(ValueError, match="No valid data points"):
        ErrorMetrics([np.nan, np.inf], [1.0, 2.0])


def test_imports_and_calculates_without_bottleneck():
    code = r'''\
import importlib.abc
import sys

class BlockBottleneck(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "bottleneck":
            raise ModuleNotFoundError("blocked for fallback test")
        return None

sys.meta_path.insert(0, BlockBottleneck())
from error_metrics.core import ErrorMetrics, bn
import numpy as np
assert bn is np
assert ErrorMetrics([1, 2], [1, 1]).mean_absolute_error() == 0.5
'''
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
```

- [ ] **Step 2: Verify the new tests fail**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
```

Expected: shape validation and Bottleneck fallback tests fail; the all-invalid test already passes.

- [ ] **Step 3: Implement the fallback and pre-flatten shape check**

Replace the unconditional Bottleneck import with:

```python
import numpy as np

try:
    import bottleneck as bn
except ImportError:
    bn = np
```

At the start of `ErrorMetrics.__init__`, replace immediate flattening with:

```python
predictions = np.asarray(predictions, dtype=float)
observations = np.asarray(observations, dtype=float)
if predictions.shape != observations.shape:
    raise ValueError(
        "predictions and observations must have the same shape; got "
        f"{predictions.shape} and {observations.shape}."
    )
self.predictions = predictions.ravel()
self.observations = observations.ravel()
```

- [ ] **Step 4: Run focused and full tests**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: focused tests pass; full suite reports `35 passed`.

- [ ] **Step 5: Commit validation and fallback behavior**

```bash
git add error_metrics/core.py tests/test_v2_robustness.py
git commit -m "feat: validate inputs and make bottleneck optional"
```

---

### Task 4: Consolidate registry collisions and reject new conflicts

**Files:**
- Modify: `error_metrics/core.py`
- Modify: `tests/test_v2_robustness.py`

**Interfaces:**
- Consumes: `MetricRegistry.register(name, abbreviation, description)` decorators.
- Produces: exactly one canonical registered callable per abbreviation; re-registration by the same qualified method is allowed; a different qualified method raises `ValueError`.

- [ ] **Step 1: Write collision and canonical-registration tests**

Append to `tests/test_v2_robustness.py`:

```python
from error_metrics import MetricRegistry


def test_duplicate_abbreviations_use_documented_scalar_methods():
    assert MetricRegistry.get_metric("nESkew").function.__name__ == "normalized_error_skewness"
    assert MetricRegistry.get_metric("nEKurt").function.__name__ == "normalized_error_kurtosis"
    assert MetricRegistry.get_metric("NMBF").function.__name__ == "nmbf"
    assert MetricRegistry.get_metric("RNMBF").function.__name__ == "rnmbf"


def test_registry_rejects_different_function_for_existing_abbreviation():
    abbreviation = "__test_conflict__"

    @MetricRegistry.register("First", abbreviation)
    def first(self):
        return 1.0

    with pytest.raises(ValueError, match="already registered"):

        @MetricRegistry.register("Second", abbreviation)
        def second(self):
            return 2.0

    MetricRegistry._metrics.pop(abbreviation)


def test_registry_allows_same_qualified_method_to_reregister():
    abbreviation = "__test_reload__"

    def original(self):
        return 1.0

    replacement = lambda self: 2.0
    replacement.__qualname__ = original.__qualname__
    MetricRegistry.register("Original", abbreviation)(original)
    MetricRegistry.register("Replacement", abbreviation)(replacement)
    assert MetricRegistry.get_metric(abbreviation).function is replacement
    MetricRegistry._metrics.pop(abbreviation)
```

- [ ] **Step 2: Verify strict collision behavior fails**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py::test_registry_rejects_different_function_for_existing_abbreviation -q
```

Expected: fails because the second function silently overwrites the first.

- [ ] **Step 3: Consolidate existing duplicate decorators**

Keep the earlier SciPy-backed `normalized_error_skewness` and `normalized_error_kurtosis` definitions and delete their later duplicate method definitions. Keep registry decorators on scalar `nmbf` and `rnmbf`. Retain `normed_mean_bias_factor` and `revised_nmbf` as directly callable compatibility methods, but remove their `NMBF` and `RNMBF` decorators so they no longer overwrite the documented scalar registry entries.

The retained registry mapping must be:

```python
{
    "nESkew": "normalized_error_skewness",
    "nEKurt": "normalized_error_kurtosis",
    "NMBF": "nmbf",
    "RNMBF": "rnmbf",
}
```

- [ ] **Step 4: Implement strict registration**

Inside `MetricRegistry.register`, add before assignment:

```python
if abbreviation in cls._metrics:
    existing = cls._metrics[abbreviation]
    if existing.function.__qualname__ != func.__qualname__:
        raise ValueError(
            f"Metric abbreviation '{abbreviation}' is already registered to "
            f"'{existing.name}' ({existing.function.__qualname__}); cannot also "
            f"register '{name}' ({func.__qualname__}) under the same abbreviation."
        )
```

- [ ] **Step 5: Run focused and full tests**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: all tests pass; registry import does not raise because every abbreviation is unique.

- [ ] **Step 6: Commit registry consolidation**

```bash
git add error_metrics/core.py tests/test_v2_robustness.py
git commit -m "fix: enforce unique metric abbreviations"
```

---

### Task 5: Add shared calculation caches and ordered-data warnings

**Files:**
- Modify: `error_metrics/core.py`
- Modify: `tests/test_v2_robustness.py`

**Interfaces:**
- Consumes: validated `self.predictions`, `self.observations`, `self.N`, and `_n_dropped`.
- Produces: cached properties `_pearson_r: float`, `_ecdf_obs: ECDF`, `_ecdf_pred: ECDF`, `_linreg: tuple[float, float]`; `RuntimeWarning` from MASE and trend accuracy after invalid pairs are dropped.

- [ ] **Step 1: Write cache and warning tests**

Append to `tests/test_v2_robustness.py`:

```python
def test_pearson_calculation_is_cached(monkeypatch):
    calls = 0
    original = np.corrcoef

    def counting_corrcoef(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(np, "corrcoef", counting_corrcoef)
    metrics = ErrorMetrics([1.1, 2.0, 3.2], [1.0, 2.0, 3.0])
    metrics.correlation_coefficient()
    metrics.lccc()
    assert calls == 1


@pytest.mark.parametrize(
    "method_name",
    ["mean_absolute_scaled_error", "trend_accuracy"],
)
def test_time_ordered_metric_warns_after_pairs_are_dropped(method_name):
    metrics = ErrorMetrics([1.0, np.nan, 3.0, 4.0], [1.0, 2.0, 2.5, 4.2])
    with pytest.warns(RuntimeWarning, match="time|trend|ordered"):
        getattr(metrics, method_name)()
```

- [ ] **Step 2: Verify the tests fail**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
```

Expected: cache test reports two calls and warning tests report no warning.

- [ ] **Step 3: Add dropped-pair tracking and cached properties**

Import `cached_property`:

```python
from functools import cached_property
```

In `_preprocess_data`, add:

```python
self._n_dropped = int((~mask).sum())
```

Add these properties to `ErrorMetrics`:

```python
@cached_property
def _pearson_r(self) -> float:
    if self.N < 2:
        return np.nan
    return np.corrcoef(self.predictions, self.observations)[0, 1]

@cached_property
def _ecdf_obs(self) -> ECDF:
    return ECDF(self.observations)

@cached_property
def _ecdf_pred(self) -> ECDF:
    return ECDF(self.predictions)

@cached_property
def _linreg(self) -> Tuple[float, float]:
    x = self.predictions
    y = self.observations
    x_mean = bn.nanmean(x)
    y_mean = bn.nanmean(y)
    denominator = bn.nansum((x - x_mean) ** 2)
    numerator = bn.nansum((x - x_mean) * (y - y_mean))
    b1 = np.nan if denominator == 0 else numerator / denominator
    b0 = y_mean - b1 * x_mean
    ss_total = bn.nansum((y - y_mean) ** 2)
    ss_residual = bn.nansum((y - (b0 + b1 * x)) ** 2)
    r2 = np.nan if ss_total == 0 else 1 - ss_residual / ss_total
    return b1, r2
```

Change `correlation_coefficient` to return `self._pearson_r`. Change KSI, OVER, and Anderson-Darling to use `self._ecdf_obs` and `self._ecdf_pred`. Change `linear_regression` to return `self._linreg`.

- [ ] **Step 4: Warn only in time-ordered metrics**

At the start of `mean_absolute_scaled_error` add:

```python
if self._n_dropped:
    warnings.warn(
        f"MASE assumes evenly-spaced, time-ordered data, but {self._n_dropped} "
        "invalid pair(s) were removed before calculating lags.",
        RuntimeWarning,
        stacklevel=2,
    )
```

At the start of `trend_accuracy` add:

```python
if self._n_dropped:
    warnings.warn(
        f"trend_accuracy fits a trend against sample index, but {self._n_dropped} "
        "invalid pair(s) were removed and the index was compressed.",
        RuntimeWarning,
        stacklevel=2,
    )
```

- [ ] **Step 5: Run focused and full tests**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 6: Commit caches and warnings**

```bash
git add error_metrics/core.py tests/test_v2_robustness.py
git commit -m "perf: cache shared metric calculations"
```

---

### Task 6: Apply v2 safe-division behavior

**Files:**
- Modify: `error_metrics/core.py`
- Modify: `tests/test_v2_robustness.py`

**Interfaces:**
- Consumes: numeric numerator and denominator values.
- Produces: `_safe_divide(numerator: float, denominator: float) -> float`, returning `numpy.nan` when the denominator is exactly zero.

- [ ] **Step 1: Write representative undefined-result tests**

Append to `tests/test_v2_robustness.py`:

```python
def test_safe_divide_returns_nan_for_zero_denominator():
    from error_metrics.core import _safe_divide

    with np.errstate(all="raise"):
        assert np.isnan(_safe_divide(1.0, 0.0))


def test_zero_denominator_metrics_return_nan():
    metrics = ErrorMetrics([0.0, 0.0], [0.0, 0.0])
    with np.errstate(all="ignore"):
        assert np.isnan(metrics.lccc())
        assert np.isnan(metrics.ev())
        assert np.isnan(metrics.nmse())
        assert np.isnan(metrics.coefficient_of_residual_mass())
        assert np.isnan(metrics.efficiency_coefficient())
        assert np.isnan(metrics.coefficient_of_determination())
```

- [ ] **Step 2: Verify the tests fail without raising warnings as errors**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py::test_safe_divide_returns_nan_for_zero_denominator -q
```

Expected: collection fails because `_safe_divide` does not exist.

- [ ] **Step 3: Add the shared helper**

Add near the imports in `error_metrics/core.py`:

```python
def _safe_divide(numerator: float, denominator: float) -> float:
    """Return numerator divided by denominator, or NaN for a zero denominator."""
    if denominator == 0:
        return np.nan
    return numerator / denominator
```

- [ ] **Step 4: Replace v2-covered scalar divisions**

Use `_safe_divide` in these existing methods, preserving every method signature and surrounding formula:

```text
lccc, ev, nmse, coefficient_of_residual_mass,
efficiency_coefficient, mean_absolute_scaled_error,
coefficient_of_determination, mean_bias_difference,
root_mean_square_difference, mean_absolute_difference,
standard_deviation_of_residual, slope_of_best_fit_line,
t_statistic, nash_sutcliffe_efficiency, normalized_nse,
relative_absolute_error, variance_accounted_for,
kling_gupta_efficiency, legates_coefficient_of_efficiency,
ksi, over_metric, nmbf, figure_of_merit,
skill_score_against_climatology, nmaep, rnp, _linreg,
taylor_skill_score, normed_mean_bias_factor, revised_nmbf
```

For example, the transformation pattern is:

```python
return _safe_divide(numerator, denominator)

# For one-minus ratios:
return 1 - _safe_divide(numerator, denominator)

# For percentage ratios:
return 100 * _safe_divide(numerator, denominator)
```

Do not alter element-wise divisions that already mask zero entries or formulas whose documented behavior intentionally returns infinity, such as `interquartile_rmse` with zero IQR.

- [ ] **Step 5: Run focused and full tests**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v2_robustness.py -q
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: all tests pass; existing intentional infinity behavior remains covered.

- [ ] **Step 6: Commit safe division behavior**

```bash
git add error_metrics/core.py tests/test_v2_robustness.py
git commit -m "fix: handle undefined metric divisions consistently"
```

---

### Task 7: Document and verify GitHub installation

**Files:**
- Modify: `README.md`
- Verify: `pyproject.toml`

**Interfaces:**
- Consumes: repository metadata and public package API.
- Produces: documented GitHub installation, wheel and sdist artifacts, clean installed-package smoke test.

- [ ] **Step 1: Update installation and compatibility documentation**

Replace the README installation section with:

````markdown
## Installation

Error Metrics supports Python 3.9 and newer. Install the latest version
directly from GitHub:

```bash
pip install git+https://github.com/chayanroyc/error-metrics.git
```

NumPy, SciPy, and Statsmodels are installed automatically. Bottleneck is an
optional performance optimization:

```bash
pip install "error-metrics[speed] @ git+https://github.com/chayanroyc/error-metrics.git"
```
````

Keep the existing quick start unchanged because it already uses the supported public import.

- [ ] **Step 2: Run the complete suite from the repository**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 3: Build wheel and source distribution**

Run:

```bash
/glade/work/chayan/conda-envs/gpu/bin/python -m build
```

Expected: exits 0 and creates one `.whl` and one `.tar.gz` under `dist/`.

- [ ] **Step 4: Inspect artifact contents**

Run:

```bash
/glade/work/chayan/conda-envs/gpu/bin/python -m zipfile -l dist/error_metrics-0.1.0-py3-none-any.whl
tar -tzf dist/error_metrics-0.1.0.tar.gz
```

Expected: both artifacts contain `error_metrics/__init__.py`, `error_metrics/core.py`, README metadata, and license metadata; neither contains the old root `error_metrics.py`.

- [ ] **Step 5: Install and smoke-test the wheel from a clean target directory**

Run:

```bash
SMOKE_DIR=$(mktemp -d)
/glade/work/chayan/conda-envs/gpu/bin/python -m pip install --no-deps --target "$SMOKE_DIR" dist/error_metrics-0.1.0-py3-none-any.whl
cd /tmp
PYTHONPATH="$SMOKE_DIR" /glade/work/chayan/conda-envs/gpu/bin/python -c "from error_metrics import ErrorMetrics; assert ErrorMetrics([1, 2], [1, 1]).mean_absolute_error() == 0.5"
```

Expected: pip reports `Successfully installed error-metrics-0.1.0`; the smoke test exits 0 with no output.

- [ ] **Step 6: Check the final diff and repository state**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only README changes and ignored build artifacts remain before the documentation commit.

- [ ] **Step 7: Commit documentation**

```bash
git add README.md
git commit -m "docs: add GitHub installation instructions"
```

- [ ] **Step 8: Run final verification from committed HEAD**

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
/glade/work/chayan/conda-envs/gpu/bin/python -m build
git status --short
```

Expected: tests and build exit 0; tracked worktree is clean.
