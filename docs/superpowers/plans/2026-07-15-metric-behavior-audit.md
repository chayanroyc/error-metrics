# Metric Behavior Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a comprehensive, source-backed behavioral audit and characterization baseline for all 89 registered metrics without changing package behavior.

**Architecture:** Store reviewed records in `audit/metrics.yaml` using JSON-compatible YAML, validate and render them with a standard-library Python tool, and add characterization tests in fixed registry-order batches. Seed identity-only pending records mechanically, then complete 9–10 records per independently researched and reviewed batch.

**Tech Stack:** Python 3.9+, standard-library `json`, Markdown, pytest, NumPy/SciPy/Statsmodels, primary scientific literature and authoritative technical documentation.

## Global Constraints

- Do not modify `error_metrics/core.py`, registry contents, dependencies, version, public API, or runtime behavior.
- `audit/metrics.yaml` is valid YAML 1.2 expressed as deterministic JSON, requiring no new parser dependency.
- Audit exactly the 89 live registered abbreviations in registry order; exclude unregistered `MSD`, `SB`, `NU`, and `LC`.
- Separate `implemented_behavior` from `canonical_definition`; never silently treat a literature variant as a defect.
- Every completed record includes identity, output, implementation, parameters, five edge-case fields, scientific basis, verification, findings, and recommended future action.
- Unknown facts use `"unknown"` plus an explanation; do not guess.
- Each reference identifies the claim it supports and prefers primary literature or authoritative documentation.
- Each completed metric receives one hand-calculated ordinary characterization and one relevant edge characterization.
- Characterization tests lock current behavior; they do not endorse questionable behavior.
- Findings use only `consistent`, `documentation-gap`, `test-gap`, `validation-gap`, `definition-variant`, `possible-defect`, or `duplicate-or-overlap`.
- Audit batches contain no more than 10 metrics and require independent scientific/spec plus quality review before the next batch.
- Use the `research` skill for source work in every metric batch.
- Preserve the three known MSLE warnings as baseline behavior.

## Record Contract

Every entry under top-level `metrics` has this exact shape when complete:

```json
{
  "status": "complete",
  "name": "registered name",
  "method": "registered_method",
  "category": "controlled category",
  "output": {"return_shape": "scalar", "implemented_range": "...", "ideal_value": "..."},
  "implemented_behavior": {"formula": "...", "preprocessing": ["..."], "dependencies": ["..."]},
  "parameters": [],
  "edge_cases": {
    "nan_and_infinity": "...",
    "zero_inputs_or_denominators": "...",
    "negative_inputs": "...",
    "constant_series": "...",
    "no_data_after_preprocessing": "..."
  },
  "scientific_basis": {
    "canonical_definition": "...",
    "references": [{"type": "primary", "title": "...", "authors_or_organization": "...", "year": 2000, "url_or_doi": "...", "supports": "..."}],
    "known_variants": []
  },
  "verification": {"existing_tests": ["..."], "characterization_tests": ["..."], "ordinary_case": "...", "edge_case": "..."},
  "findings": [{"type": "consistent", "evidence": "...", "impact": "...", "recommended_future_action": "..."}]
}
```

Pending skeleton entries contain only `status`, `name`, and `method`. The validator rejects missing complete-record fields once `status` is `complete`.

---

### Task 1: Audit schema, registry skeleton, validator, and renderer

**Files:**
- Create: `audit/metrics.yaml`
- Create: `audit/references.md`
- Create: `scripts/audit_metrics.py`
- Create: `docs/metric-audit.md`
- Create: `tests/audit/test_audit_infrastructure.py`

**Interfaces:**
- Produces: `load_inventory(path) -> dict`, `validate_inventory(inventory, registry) -> list[str]`, and `render_markdown(inventory) -> str`.
- Produces CLI: `python scripts/audit_metrics.py validate` and `python scripts/audit_metrics.py render --check|--write`.

- [ ] Write failing tests asserting the inventory file exists, top-level `schema_version == 1`, registry order/identity is exact, invalid complete records report missing field paths, and renderer output equals committed `docs/metric-audit.md`.
- [ ] Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/audit/test_audit_infrastructure.py -q`; expect failure because artifacts do not exist.
- [ ] Implement `scripts/audit_metrics.py` with standard-library `json`, `pathlib`, and `argparse`. Import the live registry only for validation; rendering consumes inventory data only.
- [ ] Mechanically export all 89 live identities as pending entries in registry order. Do not fill scientific fields in this task.
- [ ] Create `audit/references.md` explaining source-quality labels (`primary`, `authoritative`, `secondary`) and citation requirements.
- [ ] Generate `docs/metric-audit.md` with an audit summary, pending/completed counts, category sections, and a deterministic row per identity.
- [ ] Run infrastructure tests, `python scripts/audit_metrics.py validate`, `python scripts/audit_metrics.py render --check`, full pytest, and `git diff --check`; expect infrastructure green and 71 total tests with three known warnings.
- [ ] Commit with `git commit -m "audit: add metric inventory infrastructure"`.

---

## Batch Protocol

Every Tasks 2–10 implementer must execute these exact steps for only its listed abbreviations:

1. Read each complete method, decorators/helpers it calls, and all relevant tests.
2. Use the `research` skill to locate primary or authoritative sources and save batch research at `docs/research/metric-audit-batch-N.md` with claim-level links.
3. Write characterization tests first in `tests/audit/test_characterization_batch_N.py`; demonstrate failures caused only by missing audit assertions/helpers, not by changing runtime expectations.
4. Add ordinary hand calculations and edge cases that assert the current implementation exactly or with explicit numerical tolerances.
5. Replace only the batch's pending YAML records with complete records matching the Record Contract.
6. Run `python scripts/audit_metrics.py validate` and `python scripts/audit_metrics.py render --write`.
7. Run the batch test, all audit tests, full pytest, renderer `--check`, and `git diff --check`.
8. Confirm no diff under `error_metrics/` or `pyproject.toml`.
9. Commit YAML, generated Markdown, research, and characterization tests together.

Each batch report must list sources, hand calculations, observed surprises, finding counts, and exact test output. Reviewers check scientific support and current-behavior fidelity separately.

---

### Task 2: Batch 1 — foundational errors and association

**Metrics:** `MB`, `MAE`, `MedAE`, `RMSE`, `R`, `SpearmanR`, `KendallTau`, `LCCC`, `EV`, `NMSE`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-1.md`; create `tests/audit/test_characterization_batch_1.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Include hand calculations distinguishing signed, absolute, squared, rank, concordance, explained-variance, and normalized-square behavior.
- [ ] Characterize constant-series correlation/agreement behavior and NMSE zero-mean denominators.
- [ ] Verify exactly 10 complete and 79 pending records.
- [ ] Commit with `git commit -m "audit: characterize foundational metrics"`.

### Task 3: Batch 2 — relative, scaled, percentage, and fit metrics

**Metrics:** `CRM`, `RE`, `EC`, `MASE`, `MAAPE`, `A10`, `CI`, `ME`, `R2`, `MNB`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-2.md`; create `tests/audit/test_characterization_batch_2.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize zero observations, constant observations, MASE parameter behavior, regression-fit failures, and array versus scalar returns.
- [ ] Verify exactly 20 complete and 69 pending records.
- [ ] Commit with `git commit -m "audit: characterize relative and fit metrics"`.

### Task 4: Batch 3 — normalized and fractional bias metrics

**Metrics:** `MNAE`, `FB`, `FAE`, `MFB`, `MFE`, `MAGE`, `GMB`, `FAC2`, `MBD`, `RMSD`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-3.md`; create `tests/audit/test_characterization_batch_3.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize zero pairs, negative inputs, geometric positivity, FAC2 boundaries, and differences among FB/FAE/MFB/MFE.
- [ ] Verify exactly 30 complete and 59 pending records.
- [ ] Commit with `git commit -m "audit: characterize fractional bias metrics"`.

### Task 5: Batch 4 — residual diagnostics and efficiency

**Metrics:** `MAD`, `SD`, `SBF`, `U95`, `TS`, `NSE`, `NNSE`, `RAE`, `VAF`, `RSE`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-4.md`; create `tests/audit/test_characterization_batch_4.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize degrees-of-freedom parameters, constant series, regression slope failure, uncertainty formulas, and efficiency denominators.
- [ ] Verify exactly 40 complete and 49 pending records.
- [ ] Commit with `git commit -m "audit: characterize diagnostic efficiency metrics"`.

### Task 6: Batch 5 — environmental efficiency and histogram comparison

**Metrics:** `KGE`, `KGE2012`, `KGEdp`, `DE`, `LME`, `LCEf`, `WIA`, `WIAr`, `LCE`, `KSI`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-5.md`; create `tests/audit/test_characterization_batch_5.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Source original papers for each named efficiency variant; distinguish KGE component definitions explicitly.
- [ ] Characterize constant/zero-mean series, denominator failure, KSI grid behavior, and tuple/component returns.
- [ ] Verify exactly 50 complete and 39 pending records.
- [ ] Commit with `git commit -m "audit: characterize environmental efficiency metrics"`.

### Task 7: Batch 6 — distributions, moments, and bias factors

**Metrics:** `PHI`, `SUSE`, `OVER`, `IQR`, `STD`, `nESkew`, `nEKurt`, `MBF`, `RMBF`, `NMBF`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-6.md`; create `tests/audit/test_characterization_batch_6.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize histogram bin validation and entropy variants, constant distributions, moment normalization, and positive/negative mean restrictions.
- [ ] Verify exactly 60 complete and 29 pending records.
- [ ] Commit with `git commit -m "audit: characterize distributions and bias factors"`.

### Task 8: Batch 7 — composite, decomposition, and percentage metrics

**Metrics:** `RNMBF`, `CPI`, `RED`, `FoM`, `MSDdec`, `SS`, `AD`, `KLD`, `MPE`, `MAPE`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-7.md`; create `tests/audit/test_characterization_batch_7.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize CPI dependencies, tuple decomposition, climatology denominators, AD/KLD ordering and normalization, and percentage behavior at zero.
- [ ] Verify exactly 70 complete and 19 pending records.
- [ ] Commit with `git commit -m "audit: characterize composite and percentage metrics"`.

### Task 9: Batch 8 — probabilistic, trend, agreement, and regression metrics

**Metrics:** `sMAPE`, `CRPS`, `TAcc`, `U2`, `BM`, `dCor`, `lambda`, `iqRMSE`, `SMA`, `RNP`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-8.md`; create `tests/audit/test_characterization_batch_8.py`.

- [ ] Execute the Batch Protocol for exactly these 10 metrics.
- [ ] Characterize zeros, short/constant series, parameter `c`, distance matrices, regression fit failures, IQR zero, and tuple component meanings.
- [ ] Verify exactly 80 complete and 9 pending records.
- [ ] Commit with `git commit -m "audit: characterize probabilistic and regression metrics"`.

### Task 10: Batch 9 — summary, logarithmic, normalized, ranking, and direction metrics

**Metrics:** `TSS`, `MEAN`, `MEDIAN`, `CRMSE`, `MSLE`, `NMAEp`, `NAE`, `Gini`, `PCD`

**Files:** modify inventory/report; create `docs/research/metric-audit-batch-9.md`; create `tests/audit/test_characterization_batch_9.py`.

- [ ] Execute the Batch Protocol for exactly these 9 metrics.
- [ ] Characterize tuple summary returns, centered errors, MSLE negative-domain warnings, NMAEp `p`, NAE denominators, Gini ordering, and PCD short/flat series.
- [ ] Verify exactly 89 complete and 0 pending records.
- [ ] Commit with `git commit -m "audit: characterize final metric batch"`.

---

### Task 11: Final synthesis and Phase 2 proposal

**Files:**
- Modify: `docs/metric-audit.md`
- Create: `docs/metric-audit-findings.md`
- Modify: `tests/audit/test_audit_infrastructure.py`

**Interfaces:**
- Consumes: 89 complete inventory records and all batch research/characterization tests.
- Produces: finding counts by type/priority, overlap groups, unresolved source questions, and a non-binding ordered Phase 2 proposal.

- [ ] Add failing tests requiring zero pending records, all controlled finding types, at least one reference per metric or an explicit unknown explanation, ordinary and edge characterization fields, and deterministic generation.
- [ ] Run audit infrastructure test; expect failures for any incomplete synthesis fields.
- [ ] Generate summary tables by category and finding type without editing individual scientific conclusions silently.
- [ ] Create `docs/metric-audit-findings.md` grouping possible defects, definition variants, validation gaps, overlaps, test gaps, and documentation gaps with evidence links back to metric records.
- [ ] Rank Phase 2 proposals by scientific risk, compatibility impact, and implementation dependency; label every proposal as requiring separate approval.
- [ ] Run `python scripts/audit_metrics.py validate`, renderer write/check twice, all audit tests, full pytest, and `git diff --check`.
- [ ] Verify no phase diff under `error_metrics/` or `pyproject.toml`; verify 89 complete records and no unregistered abbreviations.
- [ ] Build wheel and sdist and inspect that audit files do not accidentally become runtime package modules.
- [ ] Commit with `git commit -m "audit: synthesize metric behavior findings"` and request whole-branch scientific/spec plus code-quality review.
