# README Rewrite Design

## Goal

Rewrite the README as the single entry point for both package users and
contributors. It must accurately describe the current installable GitHub
package, its public API, and all 89 registered metrics without preserving stale
or duplicated documentation from the older script.

This is a documentation change. It must not change package behavior.

## Audience

The README serves two audiences in one document:

- users installing the package, selecting metrics, and calling the public API;
- contributors adding, registering, documenting, and testing metrics.

User-facing material comes first. Contributor guidance follows the metric
reference and operational guidance.

## Document Structure

The rewritten README will contain these sections:

1. Project summary and an accurate feature snapshot.
2. Installation from GitHub, including the optional `speed` dependency and an
   upgrade command.
3. A minimal, executable quick start using `ErrorMetrics`.
4. Public API guidance covering direct method calls, `get_metrics(...)`,
   `all_metrics()`, `MetricRegistry`, and parameterized metrics.
5. A complete reference table for all 89 registered metrics.
6. Detailed guidance for commonly used metrics and the seven recovered metrics:
   `MBF`, `RMBF`, `MFB`, `MFE`, `PHI`, `NMAEp`, and `SUSE`.
7. Input validation, NaN behavior, and parameter errors.
8. Performance and optional Bottleneck support.
9. Testing and local development.
10. Adding and registering a metric.
11. Contributing, citation, and license.

Repeated category-by-category prose will be removed when the reference table
already communicates the same information.

## Metric Reference

The live registry is authoritative for each registered metric's abbreviation,
full name, Python method, and description. The reference table will include:

- abbreviation;
- metric name;
- Python method;
- short purpose;
- output range;
- ideal value.

Ranges, ideal values, formulas, and parameter requirements are not present in
registry metadata. They must therefore be checked against `error_metrics/core.py`
and the tests. The README will use `unbounded`, `context-dependent`, or similarly
qualified wording when a universal range or ideal value does not exist. It must
not invent precise bounds unsupported by the implementation.

The four existing methods `MSD`, `SB`, `NU`, and `LC` remain absent from the
registered-metric table because they are intentionally not registered in this
release.

## Examples and Detailed Guidance

Examples must execute against the current public package. They will demonstrate:

- constructing `ErrorMetrics` from predictions and observations;
- calling common metrics directly;
- dispatching registered metrics by abbreviation;
- inspecting the registry;
- passing parameters to metrics that require them.

Detailed prose will focus on common metrics and the seven newly recovered
metrics. It will complement the table with formulas, interpretation, and
important domain restrictions rather than repeat every table cell.

## Contributor Workflow

The contributor section will describe one current workflow:

1. Add the method to `ErrorMetrics`.
2. Register it with `MetricRegistry.register(...)`.
3. Define validation and numerical edge cases.
4. Add direct-method and registry-dispatch tests.
5. Run the full test suite and build artifacts.

It will include one minimal scalar example and one parameterized example.
Internal details unnecessary to extending the registry will be omitted.

## Verification

The documentation work is complete when:

- every one of the 89 live registry abbreviations appears in the metric table;
- every documented method and example matches the current public API;
- executable examples pass against the local package;
- the full test suite passes;
- package artifacts still build successfully;
- a narrowly scoped documentation test checks that all registered
  abbreviations remain represented in the README.

The documentation test will prevent omissions but will not generate or rewrite
the README. This keeps prose and interpretation reviewable while giving registry
coverage an automated guardrail.

## Scope Boundaries

This work will not:

- change metric implementations, validation, registration, or package metadata;
- register `MSD`, `SB`, `NU`, or `LC`;
- introduce a README generator or a new documentation framework;
- split contributor guidance into another document;
- add speculative metrics, APIs, or release promises.
