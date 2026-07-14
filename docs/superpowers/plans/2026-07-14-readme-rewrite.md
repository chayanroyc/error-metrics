# README Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the stale README with one accurate, navigable guide for package users and contributors, including a verified reference for all 89 registered metrics.

**Architecture:** Keep documentation in one `README.md`, ordered from installation and usage through the complete metric reference and contributor workflow. Treat `MetricRegistry` and `error_metrics/core.py` as sources of truth, with one focused test checking table identity against the live registry without generating prose.

**Tech Stack:** Markdown, Python 3.9+, pytest, setuptools/build, NumPy, public `error_metrics` API.

## Global Constraints

- Do not change metric implementations, validation, registration, or package metadata.
- Document exactly the 89 live entries; exclude unregistered `MSD`, `SB`, `NU`, and `LC` from the table.
- Derive abbreviation, name, method, and description from the registry.
- Verify ranges, ideals, formulas, and parameters against `core.py` and tests; use `Unbounded` or `Context-dependent` when appropriate.
- Do not add a README generator or documentation framework.
- Keep user and contributor guidance in this README and keep examples executable.
- Preserve the three known MSLE warnings as baseline behavior.

---

### Task 1: Rewrite installation, quick start, and public API guidance

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: `ErrorMetrics`, `get_metrics`, `all_metrics`, `MetricRegistry.get_all_metrics`, `phi`, `nmaep`, and `suse`.
- Produces: `Overview`, `Features`, `Installation`, `Quick start`, and `Public API` sections.

- [ ] **Step 1: Record stale claims**

Run `rg -n '40\+|pip install|Quick Start|Advanced Usage|get_metrics|all_metrics' README.md`.

Expected: the outdated count and duplicated usage material appear.

- [ ] **Step 2: Rewrite overview and installation**

State that the package compares paired predictions and observations using 89 registered metrics and requires Python `>=3.9`. Document these exact commands:

```bash
python -m pip install "git+https://github.com/chayanroyc/error-metrics.git"
python -m pip install "error-metrics[speed] @ git+https://github.com/chayanroyc/error-metrics.git"
python -m pip install --upgrade --force-reinstall "git+https://github.com/chayanroyc/error-metrics.git"
```

Name NumPy, SciPy, and Statsmodels as required and Bottleneck as the optional `speed` extra. Do not claim PyPI availability.

- [ ] **Step 3: Add the executable quick start**

```python
from error_metrics import ErrorMetrics

predictions = [1.2, 1.8, 3.2, 3.9, 5.1]
observations = [1.0, 2.0, 3.0, 4.0, 5.0]
metrics = ErrorMetrics(predictions, observations)

print(metrics.mean_absolute_error())
print(metrics.root_mean_squared_error())
print(metrics.get_metrics(["MAE", "RMSE", "MBF"]))
```

Explain that direct calls use method names and registry dispatch uses abbreviations.

- [ ] **Step 4: Document public usage patterns**

Show direct calls, `get_metrics(["MAE", "RMSE"])`, `all_metrics()`, `MetricRegistry.get_all_metrics()`, `phi(bins=10)`, and `nmaep(p=2.0)`. Inspect exact signatures first:

```bash
/glade/work/chayan/conda-envs/gpu/bin/python - <<'PY'
import inspect
from error_metrics import ErrorMetrics
for name in ("get_metrics", "all_metrics", "phi", "nmaep", "suse"):
    print(name, inspect.signature(getattr(ErrorMetrics, name)))
PY
```

- [ ] **Step 5: Smoke-test documented operations**

```bash
/glade/work/chayan/conda-envs/gpu/bin/python - <<'PY'
from error_metrics import ErrorMetrics, MetricRegistry
m = ErrorMetrics([1.2, 1.8, 3.2, 3.9, 5.1], [1, 2, 3, 4, 5])
assert m.mean_absolute_error() >= 0
assert set(m.get_metrics(["MAE", "RMSE", "MBF"])) == {"MAE", "RMSE", "MBF"}
assert len(m.all_metrics()) == len(MetricRegistry.get_all_metrics()) == 89
assert 0 <= m.phi(bins=10) <= 1
assert m.nmaep(p=2.0) >= 0
PY
```

Expected: exit 0.

- [ ] **Step 6: Check and commit**

Run `git diff --check` and `rg -n '40\+|pip install error-metrics$' README.md`.

Expected: clean diff and no stale patterns.

```bash
git add README.md
git commit -m "docs: rewrite package usage guide"
```

---

### Task 2: Add and guard the complete metric reference

**Files:**
- Modify: `README.md`
- Create: `tests/test_readme.py`

**Interfaces:**
- Consumes: `MetricRegistry.get_all_metrics() -> dict[str, MetricInfo]`.
- Produces: a marker-delimited table with columns `Abbreviation`, `Metric`, `Method`, `Purpose`, `Range`, and `Ideal`.

- [ ] **Step 1: Write the failing identity test**

```python
from pathlib import Path

from error_metrics import MetricRegistry

README = Path(__file__).parents[1] / "README.md"
START = "<!-- metric-reference:start -->"
END = "<!-- metric-reference:end -->"


def test_readme_metric_reference_matches_registry():
    text = README.read_text(encoding="utf-8")
    table = text.split(START, 1)[1].split(END, 1)[0]
    documented = {}
    for line in table.splitlines():
        if line.startswith("| `"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            documented[cells[0].strip("`")] = cells[2].strip("`")
    registered = {
        key: info.function.__name__
        for key, info in MetricRegistry.get_all_metrics().items()
    }
    assert documented == registered
```

- [ ] **Step 2: Verify red**

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_readme.py -q`.

Expected: FAIL because the marker-delimited table is absent.

- [ ] **Step 3: Export registry identity fields**

```bash
/glade/work/chayan/conda-envs/gpu/bin/python - <<'PY'
from error_metrics import MetricRegistry
for key, info in MetricRegistry.get_all_metrics().items():
    print(f"{key}\t{info.name}\t{info.function.__name__}\t{info.description}")
PY
```

Expected: 89 lines. Use these first four fields verbatim except required Markdown escaping.

- [ ] **Step 4: Audit range and ideal in batches**

Process registry-order batches of no more than 15 methods. For each batch run `rg -n 'def (METHOD_ONE|METHOD_TWO|METHOD_THREE)\b|@MetricRegistry.register' error_metrics/core.py tests`, then read every complete method and relevant test.

Use interval notation only where supported, `Unbounded` for signed outputs without finite limits, `[0, ∞)` only for guaranteed nonnegative outputs, and `Context-dependent` where no universal target exists. Record essential restrictions in Purpose. Do not add the four unregistered methods.

- [ ] **Step 5: Replace the old catalog with the exact table**

```markdown
<!-- metric-reference:start -->
| Abbreviation | Metric | Method | Purpose | Range | Ideal |
| --- | --- | --- | --- | --- | --- |
| `MB` | Mean Bias | `mean_bias` | Mean signed prediction error | Unbounded | `0` |
<!-- remaining live registry rows in registry order -->
<!-- metric-reference:end -->
```

Every data row must begin with a backticked abbreviation and contain exactly six cells. Remove the superseded category catalog.

- [ ] **Step 6: Add focused interpretation**

Explain common absolute/squared errors and the seven recovered metrics using these verified formulas:

```text
MBF   mean(predictions) / mean(observations)
RMBF  abs(MBF - 1)
MFB   mean(2 * (predictions - observations) / (predictions + observations))
MFE   mean(2 * abs(predictions - observations) / (predictions + observations))
PHI   sum(min(prediction histogram probability, observation histogram probability))
NMAEp mean(abs(predictions - observations) ** p) ** (1 / p) / abs(mean(observations))
SUSE  abs(H(predictions) - H(observations)) / max(H(predictions), H(observations), 1)
```

State: positive means for MBF/RMBF; nonnegative paired inputs for MFB/MFE; integer `bins >= 1` for PHI/SUSE; finite `p > 0` and nonzero observation mean for NMAEp. Define `H` as natural-log Shannon entropy of histogram probabilities.

- [ ] **Step 7: Verify green and commit**

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_readme.py tests/test_v5_metrics.py -q
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
git diff --check
```

Expected: focused tests pass; full suite has 68 passing tests and only three known MSLE warnings.

```bash
git add README.md tests/test_readme.py
git commit -m "docs: add complete metric reference"
```

---

### Task 3: Finish contributor guidance and release verification

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: `MetricRegistry.register(name, abbreviation, description)`, pytest, and `python -m build`.
- Produces: validation, performance, development, adding-metrics, contributing, citation, and license sections.

- [ ] **Step 1: Replace stale behavior guidance**

Verify constructor and NaN behavior with `sed -n '1,180p' error_metrics/core.py` and `rg -n 'bottleneck|ValueError|isfinite|nanmean|nanmedian' error_metrics/core.py | head -80`.

Document only verified behavior: inputs become one-dimensional float arrays; shapes must match; individual metrics may add positivity, denominator, or parameter restrictions; NaN handling is metric-specific; Bottleneck is optional.

- [ ] **Step 2: Add current contributor examples**

Include a scalar decorator example:

```python
@MetricRegistry.register("Mean Signed Cubic Error", "MSCE", "Mean cubed residual")
def mean_signed_cubic_error(self) -> float:
    return float(np.nanmean((self.predictions - self.observations) ** 3))
```

Include a parameterized decorator example:

```python
@MetricRegistry.register("Threshold Exceedance Rate", "TER", "Fraction above a threshold")
def threshold_exceedance_rate(self, threshold: float = 1.0) -> float:
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("threshold must be finite and >= 0")
    return float(np.nanmean(np.abs(self.predictions - self.observations) > threshold))
```

State that each metric needs direct calculation/validation tests and a registry mapping or dispatch test. Do not add these example metrics to the package.

- [ ] **Step 3: Add development and project sections**

Document:

```bash
python -m pip install -e ".[dev]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
python -m build
```

Keep concise contributing, citation, and MIT license sections. Do not invent a DOI, code of conduct, PyPI command, or release cadence.

- [ ] **Step 4: Execute README examples**

Copy each executable user Python block unchanged into `/tmp/readme-example.py` and run `PYTHONPATH=. /glade/work/chayan/conda-envs/gpu/bin/python /tmp/readme-example.py`. Exclude contributor fragments that intentionally define example methods. Expected: every user example exits 0 and printed results agree with prose.

- [ ] **Step 5: Run final verification**

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
/glade/work/chayan/conda-envs/gpu/bin/python -m build
rg -n '40\+|TODO|TBD|pip install error-metrics$' README.md
git diff --check
git status --short
```

Expected: 68 tests pass with only the three known warnings; wheel and sdist build; no stale claims/placeholders; only `README.md` is pending for this task.

- [ ] **Step 6: Commit and request whole-change review**

```bash
git add README.md
git commit -m "docs: complete contributor guide"
```

Review from the parent of Task 1 through `HEAD` for design coverage, all 89 identities, defensible ranges/ideals, executable examples, both audiences, unchanged package behavior/metadata, full tests, and successful artifact build.
