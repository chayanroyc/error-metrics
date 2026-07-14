# Recover Seven v5 Metrics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recover seven v5 metrics in five reviewed slices while preserving all 82 current registry entries and behavior.

**Architecture:** Add the registered methods to `ErrorMetrics` in `error_metrics/core.py` and keep focused coverage in `tests/test_v5_metrics.py`. Do not import v5's constructor policy, metadata, grouping, or general error-handling framework; only SUSE adds a private helper.

**Tech Stack:** Python 3.9+, NumPy, optional Bottleneck, pytest, setuptools, build

## Global Constraints

- Add exactly `MBF`, `RMBF`, `MFB`, `MFE`, `PHI`, `NMAEp`, and `SUSE`.
- Preserve all 82 pre-cycle registry abbreviations and method mappings; finish with exactly 89 unique registrations.
- Preserve every existing public method, formula, abbreviation, return shape, constructor behavior, dependency, and import.
- Leave `FB` and `FAE` unchanged; do not make `FAE` an alias of `MFE`.
- Leave `MSD`, `SB`, `NU`, and `LC` unregistered.
- Reject negative retained inputs locally in MFB/MFE; do not add constructor-level policies.
- Do not add v5 metadata, groups, query APIs, general validation/error handling, or unrelated refactoring.
- Each task ends with focused tests, the complete suite, a separate commit, and review.

## File map

- `error_metrics/core.py`: seven metric methods and `_shannon_entropy` only.
- `tests/test_v5_metrics.py`: recovered-metric and exact inventory tests.

---

### Task 1: Recover MBF and RMBF

**Files:**
- Modify: `error_metrics/core.py`
- Create: `tests/test_v5_metrics.py`

**Interfaces:**
- Consumes: `pred_mean`, `obs_mean`, and `MetricRegistry.register`.
- Produces: `mean_bias_factor() -> float` as `MBF`; `relative_mean_bias_factor() -> float` as `RMBF`.

- [ ] **Step 1: Write failing tests**

Create `tests/test_v5_metrics.py`:

```python
import numpy as np
import pytest

from error_metrics import ErrorMetrics, MetricRegistry


def test_mean_bias_factors_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_bias_factor(), 2.0)
    assert np.isclose(metrics.relative_mean_bias_factor(), 1.0)
    perfect = ErrorMetrics([1.0, 2.0], [1.0, 2.0])
    assert np.isclose(perfect.mean_bias_factor(), 1.0)
    assert np.isclose(perfect.relative_mean_bias_factor(), 0.0)


@pytest.mark.parametrize("predictions,observations", [
    ([0.0, 0.0], [1.0, 2.0]), ([1.0, 2.0], [0.0, 0.0]),
    ([-1.0, -2.0], [1.0, 2.0]), ([1.0, 2.0], [-1.0, -2.0]),
])
def test_mean_bias_factors_require_positive_means(predictions, observations):
    metrics = ErrorMetrics(predictions, observations)
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.mean_bias_factor()
    with pytest.raises(ValueError, match="strictly positive"):
        metrics.relative_mean_bias_factor()


def test_mean_bias_factor_registry_mappings():
    assert MetricRegistry.get_metric("MBF").function.__name__ == "mean_bias_factor"
    assert MetricRegistry.get_metric("RMBF").function.__name__ == "relative_mean_bias_factor"
```

- [ ] **Step 2: Verify RED**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v5_metrics.py -q`.

Expected: missing methods/registry entries fail.

- [ ] **Step 3: Add the methods near NMBF/RNMBF**

```python
@MetricRegistry.register("Mean Bias Factor", "MBF", "Ratio of mean prediction to mean observation")
def mean_bias_factor(self) -> float:
    """Return mean prediction divided by mean observation."""
    if self.pred_mean <= 0 or self.obs_mean <= 0:
        raise ValueError("MBF requires strictly positive prediction and observation means.")
    return float(self.pred_mean / self.obs_mean)

@MetricRegistry.register("Relative Mean Bias Factor", "RMBF", "Absolute deviation of MBF from one")
def relative_mean_bias_factor(self) -> float:
    """Return the absolute deviation of MBF from one."""
    return float(np.abs(self.mean_bias_factor() - 1.0))
```

- [ ] **Step 4: Verify GREEN and regression safety**

Run focused test above, then `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`.

Expected: all pass; only three pre-existing MSLE warnings.

- [ ] **Step 5: Commit**

```bash
git add error_metrics/core.py tests/test_v5_metrics.py
git commit -m "feat: add mean bias factor metrics"
```

---

### Task 2: Recover MFB and MFE

**Files:** Modify `error_metrics/core.py`, `tests/test_v5_metrics.py`

**Interfaces:** Produces `mean_fractional_bias() -> float` as `MFB` and `mean_fractional_error() -> float` as `MFE`; neither mutates stored arrays.

- [ ] **Step 1: Append failing tests**

```python
def test_mean_fractional_metrics_match_hand_calculation():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.mean_fractional_bias(), 2.0 / 3.0)
    assert np.isclose(metrics.mean_fractional_error(), 2.0 / 3.0)


def test_mean_fractional_metrics_handle_identical_zero_pair():
    metrics = ErrorMetrics([0.0, 1.0], [0.0, 1.0])
    assert metrics.mean_fractional_bias() == 0.0
    assert metrics.mean_fractional_error() == 0.0


def test_mean_fractional_metrics_reject_negatives_without_mutation():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    pred, obs = metrics.predictions.copy(), metrics.observations.copy()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_bias()
    with pytest.raises(ValueError, match="nonnegative"):
        metrics.mean_fractional_error()
    assert np.array_equal(metrics.predictions, pred)
    assert np.array_equal(metrics.observations, obs)


def test_existing_fb_fae_and_new_registry_mappings_are_distinct():
    metrics = ErrorMetrics([-0.5, 2.0], [1.0, 1.0])
    assert np.isclose(metrics.fb(), -8.0 / 3.0)
    assert np.isclose(metrics.fae(), 10.0 / 3.0)
    mappings = {k: v.function.__name__ for k, v in MetricRegistry.get_all_metrics().items()}
    assert {k: mappings[k] for k in ("MFB", "MFE", "FB", "FAE")} == {
        "MFB": "mean_fractional_bias", "MFE": "mean_fractional_error",
        "FB": "fb", "FAE": "fae",
    }
```

- [ ] **Step 2: Verify RED**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v5_metrics.py -q`; expect the new tests to fail while Task 1 remains green.

- [ ] **Step 3: Add methods after `fae`**

```python
@MetricRegistry.register("Mean Fractional Bias", "MFB", "Pointwise mean fractional bias")
def mean_fractional_bias(self) -> float:
    """Return pointwise mean fractional bias for nonnegative data."""
    if np.any(self.predictions < 0) or np.any(self.observations < 0):
        raise ValueError("MFB requires nonnegative predictions and observations.")
    denominator = self.predictions + self.observations
    ratio = np.divide(2.0 * self.diff, denominator, out=np.zeros_like(self.diff), where=denominator != 0)
    return float(bn.nanmean(ratio))

@MetricRegistry.register("Mean Fractional Error", "MFE", "Pointwise mean fractional absolute error")
def mean_fractional_error(self) -> float:
    """Return pointwise mean fractional absolute error for nonnegative data."""
    if np.any(self.predictions < 0) or np.any(self.observations < 0):
        raise ValueError("MFE requires nonnegative predictions and observations.")
    denominator = self.predictions + self.observations
    ratio = np.divide(2.0 * np.abs(self.diff), denominator, out=np.zeros_like(self.diff), where=denominator != 0)
    return float(bn.nanmean(ratio))
```

- [ ] **Step 4: Run focused and complete suites**

Run the focused command above, then `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`; expect green with only the three pre-existing MSLE warnings.

- [ ] **Step 5: Commit**

```bash
git add error_metrics/core.py tests/test_v5_metrics.py
git commit -m "feat: add mean fractional metrics"
```

---

### Task 3: Recover PHI

**Files:** Modify `error_metrics/core.py`, `tests/test_v5_metrics.py`

**Interfaces:** Produces `phi(n_bins: int = 10) -> float` as `PHI`, bounded `[0, 1]`.

- [ ] **Step 1: Append failing tests**

```python
def test_phi_identical_and_separated_histograms():
    assert ErrorMetrics([0, 1, 2], [0, 1, 2]).phi(3) == 1.0
    assert ErrorMetrics([0, 0], [10, 10]).phi(2) == 0.0


def test_phi_bounds_validation_and_registry():
    metrics = ErrorMetrics([0, 1, 3], [0, 2, 3])
    assert 0.0 <= metrics.phi(3) <= 1.0
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.phi(invalid)
    assert MetricRegistry.get_metric("PHI").function.__name__ == "phi"
```

- [ ] **Step 2: Verify RED**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v5_metrics.py -q`; expect PHI tests to fail and prior slices to pass.

- [ ] **Step 3: Add PHI near distributional metrics**

```python
@MetricRegistry.register("Percentage of Histogram Intersection", "PHI", "Histogram-overlap distribution similarity")
def phi(self, n_bins: int = 10) -> float:
    """Return normalized histogram intersection as a fraction in [0, 1]."""
    if isinstance(n_bins, bool) or not isinstance(n_bins, int) or n_bins < 1:
        raise ValueError("n_bins must be an integer >= 1")
    edges = np.histogram_bin_edges(np.concatenate((self.predictions, self.observations)), bins=n_bins)
    pred_counts, _ = np.histogram(self.predictions, bins=edges)
    obs_counts, _ = np.histogram(self.observations, bins=edges)
    pred_probability = pred_counts / pred_counts.sum()
    obs_probability = obs_counts / obs_counts.sum()
    return float(np.sum(np.minimum(pred_probability, obs_probability)))
```

- [ ] **Step 4: Run focused and complete suites**

Run the focused command above, then `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`; expect green with only the three pre-existing MSLE warnings.

- [ ] **Step 5: Commit**

```bash
git add error_metrics/core.py tests/test_v5_metrics.py
git commit -m "feat: add histogram intersection metric"
```

---

### Task 4: Recover NMAEp

**Files:** Modify `error_metrics/core.py`, `tests/test_v5_metrics.py`

**Interfaces:** Produces `nmaep(p: float = 1.0) -> float` as `NMAEp`.

- [ ] **Step 1: Append failing tests**

```python
def test_nmaep_matches_p1_p2_hand_calculations():
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    assert np.isclose(metrics.nmaep(1.0), 1.0)
    assert np.isclose(metrics.nmaep(2.0), np.sqrt(2.5) / 1.5)


@pytest.mark.parametrize("p", [0.0, -1.0, np.inf, -np.inf, np.nan])
def test_nmaep_validation(p):
    metrics = ErrorMetrics([2.0, 4.0], [1.0, 2.0])
    with pytest.raises(ValueError, match="finite and > 0"):
        metrics.nmaep(p)


def test_nmaep_zero_mean_and_registry():
    with pytest.raises(ValueError, match="observation mean is zero"):
        ErrorMetrics([1, 2], [-1, 1]).nmaep()
    assert MetricRegistry.get_metric("NMAEp").function.__name__ == "nmaep"
```

- [ ] **Step 2: Verify RED**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v5_metrics.py -q`; expect NMAEp tests to fail and prior slices to pass.

- [ ] **Step 3: Add NMAEp near normalized errors**

```python
@MetricRegistry.register("Normalized Mean Absolute p-Error", "NMAEp", "Lp-norm accuracy normalized by mean observation")
def nmaep(self, p: float = 1.0) -> float:
    """Return generalized absolute p-error normalized by mean observation."""
    if not np.isfinite(p) or p <= 0:
        raise ValueError("p must be finite and > 0")
    if self.obs_mean == 0:
        raise ValueError("NMAEp is undefined when the observation mean is zero.")
    lp_norm = bn.nanmean(np.abs(self.diff) ** p) ** (1.0 / p)
    return float(lp_norm / np.abs(self.obs_mean))
```

- [ ] **Step 4: Run focused and complete suites**

Run the focused command above, then `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`; expect green with only the three pre-existing MSLE warnings.

- [ ] **Step 5: Commit**

```bash
git add error_metrics/core.py tests/test_v5_metrics.py
git commit -m "feat: add normalized p-error metric"
```

---

### Task 5: Recover SUSE and prove the exact superset

**Files:** Modify `error_metrics/core.py`, `tests/test_v5_metrics.py`

**Interfaces:** Produces `_shannon_entropy(data, edges) -> float`, `suse(n_bins: int = 10) -> float` as `SUSE`, and the exact 89-entry invariant.

- [ ] **Step 1: Append failing SUSE tests**

```python
def test_suse_behavior_validation_and_registry():
    assert ErrorMetrics([0, 1, 2, 3], [0, 1, 2, 3]).suse(4) == 0.0
    value = ErrorMetrics([0, 0, 0, 3], [0, 1, 2, 3]).suse(4)
    assert value > 0.0 and np.isfinite(value)
    metrics = ErrorMetrics([0, 1], [0, 1])
    for invalid in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="integer >= 1"):
            metrics.suse(invalid)
    assert MetricRegistry.get_metric("SUSE").function.__name__ == "suse"
```

- [ ] **Step 2: Verify RED**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_v5_metrics.py -q`; expect SUSE tests to fail and Tasks 1–4 to pass.

- [ ] **Step 3: Add helper and SUSE near PHI**

```python
@staticmethod
def _shannon_entropy(data: np.ndarray, edges: np.ndarray) -> float:
    counts, _ = np.histogram(data, bins=edges)
    probabilities = counts / counts.sum()
    probabilities = probabilities[probabilities > 0]
    return float(-np.sum(probabilities * np.log(probabilities)))

@MetricRegistry.register("Scaled and Unscaled Shannon Entropy Difference", "SUSE", "Entropy-based variability similarity")
def suse(self, n_bins: int = 10) -> float:
    """Return the maximum scaled or unscaled Shannon entropy difference."""
    if isinstance(n_bins, bool) or not isinstance(n_bins, int) or n_bins < 1:
        raise ValueError("n_bins must be an integer >= 1")
    common = np.histogram_bin_edges(np.concatenate((self.predictions, self.observations)), bins=n_bins)
    scaled = abs(self._shannon_entropy(self.predictions, common) - self._shannon_entropy(self.observations, common))
    pred_edges = np.histogram_bin_edges(self.predictions, bins=n_bins)
    obs_edges = np.histogram_bin_edges(self.observations, bins=n_bins)
    unscaled = abs(self._shannon_entropy(self.predictions, pred_edges) - self._shannon_entropy(self.observations, obs_edges))
    return float(max(scaled, unscaled))
```

- [ ] **Step 4: Append exact inventory test**

```python
BASELINE_ABBREVIATIONS = {
    "MB", "MAE", "MedAE", "RMSE", "R", "SpearmanR", "KendallTau", "LCCC", "EV", "NMSE", "CRM", "RE", "EC", "MASE", "MAAPE", "A10", "CI", "ME", "R2", "MNB", "MNAE", "FB", "FAE", "MAGE", "GMB", "FAC2", "MBD", "RMSD", "MAD", "SD", "SBF", "U95", "TS", "NSE", "NNSE", "RAE", "VAF", "RSE", "KGE", "KGE2012", "KGEdp", "DE", "LME", "LCEf", "WIA", "WIAr", "LCE", "KSI", "OVER", "IQR", "STD", "nESkew", "nEKurt", "NMBF", "RNMBF", "CPI", "RED", "FoM", "MSDdec", "SS", "AD", "KLD", "MPE", "MAPE", "sMAPE", "CRPS", "TAcc", "U2", "BM", "dCor", "lambda", "iqRMSE", "SMA", "RNP", "TSS", "MEAN", "MEDIAN", "CRMSE", "MSLE", "NAE", "Gini", "PCD",
}
BASELINE_MAPPINGS = {
    "MB": "mean_bias", "MAE": "mean_absolute_error", "MedAE": "median_absolute_error", "RMSE": "root_mean_squared_error", "R": "correlation_coefficient", "SpearmanR": "spearman_r", "KendallTau": "kendall_tau", "LCCC": "lccc", "EV": "ev", "NMSE": "nmse", "CRM": "coefficient_of_residual_mass", "RE": "relative_error", "EC": "efficiency_coefficient", "MASE": "mean_absolute_scaled_error", "MAAPE": "mean_arctangent_absolute_percentage_error", "A10": "a10_index", "CI": "confidence_index", "ME": "max_error", "R2": "coefficient_of_determination", "MNB": "mean_normalized_bias", "MNAE": "mean_normalized_absolute_error", "FB": "fb", "FAE": "fae", "MAGE": "mean_absolute_gross_error", "GMB": "geometric_mean_bias", "FAC2": "factor_of_observations2", "MBD": "mean_bias_difference", "RMSD": "root_mean_square_difference", "MAD": "mean_absolute_difference", "SD": "standard_deviation_of_residual", "SBF": "slope_of_best_fit_line", "U95": "uncertainty_95", "TS": "t_statistic", "NSE": "nash_sutcliffe_efficiency", "NNSE": "normalized_nse", "RAE": "relative_absolute_error", "VAF": "variance_accounted_for", "RSE": "residual_standard_error", "KGE": "kling_gupta_efficiency", "KGE2012": "modified_kling_gupta_efficiency", "KGEdp": "kling_gupta_efficiency_double_prime", "DE": "diagnostic_efficiency", "LME": "liu_model_efficiency", "LCEf": "least_squares_combined_efficiency", "WIA": "willmotts_index_of_agreement", "WIAr": "refined_index_of_agreement", "LCE": "legates_coefficient_of_efficiency", "KSI": "ksi", "OVER": "over_metric", "IQR": "IQR", "STD": "STD", "nESkew": "normalized_error_skewness", "nEKurt": "normalized_error_kurtosis", "NMBF": "nmbf", "RNMBF": "rnmbf", "CPI": "cpi", "RED": "red", "FoM": "figure_of_merit", "MSDdec": "msd_decomposition", "SS": "skill_score_against_climatology", "AD": "anderson_darling_distance", "KLD": "kullback_leibler_divergence", "MPE": "mean_percentage_error", "MAPE": "mean_absolute_percentage_error", "sMAPE": "symmetric_mean_absolute_percentage_error", "CRPS": "continuous_ranked_probability_score", "TAcc": "trend_accuracy", "U2": "theils_u2", "BM": "berry_mielke_score", "dCor": "distance_correlation", "lambda": "duveiller_agreement_coefficient", "iqRMSE": "interquartile_rmse", "SMA": "sma_metrics", "RNP": "rnp", "TSS": "taylor_skill_score", "MEAN": "meann", "MEDIAN": "mediann", "CRMSE": "centered_root_mean_square", "MSLE": "mean_squared_logarithmic_error", "NAE": "normalized_absolute_error", "Gini": "gini_coefficient", "PCD": "prediction_of_change_in_direction",
}
RECOVERED_MAPPINGS = {"MBF": "mean_bias_factor", "RMBF": "relative_mean_bias_factor", "MFB": "mean_fractional_bias", "MFE": "mean_fractional_error", "PHI": "phi", "NMAEp": "nmaep", "SUSE": "suse"}


def test_registry_is_exact_89_metric_superset():
    registry = MetricRegistry.get_all_metrics()
    mappings = {key: info.function.__name__ for key, info in registry.items()}
    assert len(BASELINE_ABBREVIATIONS) == 82
    assert set(BASELINE_MAPPINGS) == BASELINE_ABBREVIATIONS
    assert {key: mappings[key] for key in BASELINE_MAPPINGS} == BASELINE_MAPPINGS
    assert {key: mappings[key] for key in RECOVERED_MAPPINGS} == RECOVERED_MAPPINGS
    assert len(registry) == len(set(registry)) == 89
    assert not {"MSD", "SB", "NU", "LC"} & registry.keys()
```

- [ ] **Step 5: Run focused and complete suites**

Run the focused command above, then `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`; expect green, exactly 89 registrations, and only the three pre-existing MSLE warnings.

- [ ] **Step 6: Commit**

```bash
git add error_metrics/core.py tests/test_v5_metrics.py
git commit -m "feat: add entropy similarity metric"
```

---

### Task 6: Verify packaged artifacts

**Files:** Verify `pyproject.toml`, `error_metrics/__init__.py`, `error_metrics/core.py`, `tests/test_v5_metrics.py`

**Interfaces:** Consumes the 89-metric package; produces verified wheel/sdist and clean-target `MBF` smoke result.

- [ ] **Step 1: Run the complete suite**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q`; expect all tests green with only the three pre-existing MSLE warnings.

- [ ] **Step 2: Build artifacts**

```bash
/glade/work/chayan/conda-envs/gpu/bin/python -m build
```

Expected: wheel and sdist are created; isolated build may require network approval.

- [ ] **Step 3: Inspect artifacts**

```bash
/glade/work/chayan/conda-envs/gpu/bin/python -m zipfile -l dist/error_metrics-0.1.0-py3-none-any.whl
tar -tzf dist/error_metrics-0.1.0.tar.gz
```

Expected: package modules present and no root `error_metrics.py`.

- [ ] **Step 4: Clean-target smoke test**

```bash
SMOKE_DIR=$(mktemp -d)
/glade/work/chayan/conda-envs/gpu/bin/python -m pip install --no-deps --target "$SMOKE_DIR" dist/error_metrics-0.1.0-py3-none-any.whl
cd /tmp
PYTHONPATH="$SMOKE_DIR" /glade/work/chayan/conda-envs/gpu/bin/python -c "from error_metrics import ErrorMetrics; assert ErrorMetrics([2, 4], [1, 2]).mean_bias_factor() == 2.0"
```

- [ ] **Step 5: Run `git diff --check` and `git status --short`; expect a clean tracked tree.**
