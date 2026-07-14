# Guided README Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the accurate README into a polished, guided first experience that helps visitors understand the package, choose a metric family, and use or extend the API.

**Architecture:** Keep one Markdown README with a layered flow: credible opening, 30-second start, selection guidance, progressive API examples, full guarded reference, then contributor guidance. Preserve the existing registry-backed table contract and verify every displayed result against the live package.

**Tech Stack:** Markdown, Python 3.9+, pytest, NumPy, setuptools/build, public `error_metrics` API.

## Global Constraints

- Do not change runtime code, registry contents, dependencies, version, or package metadata.
- Keep exactly 89 registered reference rows and exclude `MSD`, `SB`, `NU`, and `LC`.
- Preserve the six-cell marker-delimited table contract and `tests/test_readme.py` invariants.
- Use only verified claims, formulas, parameter names, outputs, and badge endpoints.
- Do not claim PyPI availability or use “best” or “most comprehensive.”
- Use one consistent dataset in all user examples.
- Keep user and contributor guidance in one README.
- Keep the README materially shorter than the former 795-line version.
- Preserve three known MSLE warnings as baseline behavior.

---

### Task 1: Build the 30-second opening and metric-selection guide

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: GitHub repository metadata, Python `>=3.9`, MIT license, 89-entry registry, `ErrorMetrics.get_metrics`.
- Produces: centered header/badges, value proposition, contents, 30-second start, selection guide, caution matrix, and text decision flow.

- [ ] **Step 1: Capture the current opening baseline**

Run:

```bash
sed -n '1,110p' README.md
wc -l README.md
```

Expected: accurate installation and API content exists, but no centered header, selection guide, or decision flow.

- [ ] **Step 2: Add the centered header and verified badges**

Use a simple centered `<div align="center">` containing the title and a one-line tagline about choosing and computing error metrics through one API. Add badges for:

- Python `3.9+` using a static shields.io badge;
- `89 metrics` using a static badge;
- `68 tests` using a static badge rather than implying CI status;
- MIT license linked to `LICENSE`.

Use URL-encoded badge labels and alt text. Do not add a logo or claim live build status.

- [ ] **Step 3: Write the value proposition and compact contents**

In two sentences, explain paired predictions/observations, 89 registered metrics, and coverage from common errors through specialized distribution, agreement, and environmental metrics. Add a compact linked list for Quick start, Choosing a metric, API patterns, Metric reference, Important behavior, and Contributing.

- [ ] **Step 4: Create the 30-second start with actual output**

Use this dataset consistently throughout all user examples:

```python
predictions = [1.2, 1.8, 3.2, 3.9, 5.1]
observations = [1.0, 2.0, 3.0, 4.0, 5.0]
```

Show GitHub installation, construct `ErrorMetrics`, and compute `MAE`, `RMSE`, and `MBF` through `get_metrics`. Display the verified output:

```text
{'MAE': 0.16, 'RMSE': 0.17, 'MBF': 1.01}
```

- [ ] **Step 5: Add “Which metric should I use?”**

Create a scannable table with columns `Goal`, `Start with`, and `Tradeoff`. Include exactly these goal groups:

- original-unit error: `MAE`, `RMSE`, `MedAE`;
- scale-independent: `MASE`, `NMAEp`, `iqRMSE`, `NAE`;
- relative/percentage: `MAPE`, `sMAPE`, `MAAPE`, `MPE`;
- bias: `MB`, `MBF`, `RMBF`, `MFB`, `MFE`;
- hydrology/environmental: `NSE`, `KGE`, `KGE2012`, `KGEdp`, `WIA`, `LCE`, `DE`;
- association/agreement: `R`, `SpearmanR`, `KendallTau`, `LCCC`, `dCor`;
- distributions: `KLD`, `PHI`, `SUSE`, `AD`;
- trends/direction: `TAcc`, `PCD`.

Each tradeoff must mention the principal limitation supported by the current implementation or definition.

- [ ] **Step 6: Add cautions and text decision flow**

Add a compact caution table for zeros, negatives, outliers, scale differences, and denominator/positivity restrictions. Recommend robust starting points without declaring universal winners.

Use this decision flow in prose:

```text
Need error in original units? → MAE / RMSE / MedAE
Need cross-scale comparison? → MASE / NMAEp / iqRMSE
Need agreement rather than error size? → LCCC / WIA / dCor
Need distribution similarity? → PHI / SUSE / KLD / AD
Need domain efficiency? → NSE / KGE family / DE
```

- [ ] **Step 7: Verify claims and commit**

Run the 30-second example unchanged with the project Python, then run:

```bash
rg -n 'best|most comprehensive|pypi|build passing' README.md
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_readme.py -q
git diff --check
```

Expected: no unsupported claims, one README test passes, clean diff.

```bash
git add README.md
git commit -m "docs: add guided README opening"
```

---

### Task 2: Create progressive API examples and a navigable reference

**Files:**
- Modify: `README.md`
- Test: `tests/test_readme.py`

**Interfaces:**
- Consumes: the Task 1 dataset, direct methods, abbreviation dispatch, parameterized methods with `n_bins`/`p`, `MetricRegistry`, and tuple-valued metrics.
- Produces: three progressive workflows, actual outputs, family guideposts, unchanged exact 89-row table identity.

- [ ] **Step 1: Write a failing structure assertion**

Extend `tests/test_readme.py` with:

```python
def test_readme_has_guided_sections():
    text = README.read_text(encoding="utf-8")
    for heading in (
        "## Quick start",
        "## Which metric should I use?",
        "## API patterns",
        "## Metric families",
        "## Complete metric reference",
    ):
        assert heading in text
```

Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_readme.py -q`.

Expected: FAIL until the final progressive/reference heading structure exists.

- [ ] **Step 2: Write progressive workflow one: direct call**

Using the shared dataset, show `metrics.mean_absolute_error()` and its actual unrounded float result `0.15999999999999998`. Explain that direct methods return raw floating-point values.

- [ ] **Step 3: Write workflow two: abbreviation dispatch**

Show `metrics.get_metrics(["MAE", "RMSE", "MBF"])` and output `{'MAE': 0.16, 'RMSE': 0.17, 'MBF': 1.01}`. Explain default two-decimal rounding and `round_factor` without inventing per-metric keyword dispatch.

- [ ] **Step 4: Write workflow three: parameters and discovery**

Show executable calls to `metrics.phi(n_bins=5)`, `metrics.nmaep(p=2.0)`, and registry inspection. Print only stable, verified values or structural facts. Explain that parameterized metrics are normally called directly because `get_metrics` does not accept arbitrary metric-specific keywords.

- [ ] **Step 5: Demonstrate tuple-valued output**

Inspect `sma_metrics` and `rnp` behavior and choose one stable example. Show its real return shape and label its components from the implementation. Do not claim `get_metrics` converts tuple components into separate keys.

- [ ] **Step 6: Add metric-family guideposts**

Before the full table, add a compact family index mapping each family to the relevant abbreviations. Families must include core error, normalized/relative, bias, correlation/agreement, efficiency/environmental, distribution/statistical, percentage, trend/direction, and diagnostic/decomposition.

Keep the complete reference as one uninterrupted table between the existing markers. Do not insert headings or non-data rows inside it.

- [ ] **Step 7: Execute every user example**

Copy executable blocks unchanged into temporary scripts and run them with:

```bash
PYTHONPATH=. /glade/work/chayan/conda-envs/gpu/bin/python /tmp/readme-example.py
```

Expected: exit 0 and every displayed output matches.

- [ ] **Step 8: Verify table invariants and commit**

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest tests/test_readme.py tests/test_v5_metrics.py -q
git diff --check
```

Expected: 24 focused tests pass; table test still proves 89 rows, six cells, uniqueness, order, and method identity.

```bash
git add README.md tests/test_readme.py
git commit -m "docs: add progressive metric guidance"
```

---

### Task 3: Tighten contributor path and verify the complete README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: existing behavior/caution content, `MetricRegistry.register`, editable dev install, pytest, build.
- Produces: compact behavior notes, one complete contributor example, checklist, citation/license, release-ready README.

- [ ] **Step 1: Consolidate important behavior callouts**

Keep concise callouts for pairwise non-finite removal, matching input shapes, metric-specific positivity/nonnegativity, zero denominators, parameter validation, scale sensitivity, and outliers. Verify each statement against `core.py`; remove duplicate explanations elsewhere.

- [ ] **Step 2: Reduce contributor examples to one complete example**

Retain one scalar metric example showing method, decorator, description, NumPy computation, direct calculation test, validation if applicable, and registry mapping test. Remove the second parameterized contributor example because user-facing parameterized calls already cover that concept. Clearly state the example is not part of the installed registry.

- [ ] **Step 3: Add the contribution checklist**

Use a five-item checklist: implement method, register identity, define restrictions, add direct/validation/dispatch tests, run full tests and build. Retain exact development commands:

```bash
python -m pip install -e ".[dev]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
python -m build
```

- [ ] **Step 4: Verify all examples and outputs**

Execute each runnable user block unchanged. Inspect all displayed output against actual results. Contributor fragments that require placement inside the class are reviewed structurally but excluded from execution.

- [ ] **Step 5: Run final tests, size check, and build**

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /glade/work/chayan/conda-envs/gpu/bin/python -m pytest -q
wc -l README.md
/glade/work/chayan/conda-envs/gpu/bin/python -m build
git diff --check
git status --short
```

Expected: 69 tests pass with only three known MSLE warnings; README stays below 795 lines; wheel and sdist build and include README; only README is pending for this task.

- [ ] **Step 6: Commit and request whole-branch review**

```bash
git add README.md
git commit -m "docs: polish contributor path"
```

The final reviewer must verify first-30-second comprehension, selection tradeoffs, live outputs/signatures, all 89 table claims and invariants, caution accuracy, contributor usability, no runtime/metadata changes, test evidence, README size, and successful artifacts.
