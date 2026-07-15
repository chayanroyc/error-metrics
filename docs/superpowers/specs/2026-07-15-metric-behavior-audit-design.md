# Metric Behavior Audit Design

## Goal

Create a comprehensive, evidence-backed audit of all 89 registered metrics
without changing runtime behavior, registry contents, or the public API. The
audit will record what the package currently implements, compare it with
canonical definitions, characterize edge cases, and identify risks that should
inform a separately approved standardization phase.

## Scope

Phase 1 is observation and documentation only. It will:

- inventory every registered metric;
- characterize existing behavior with tests;
- verify scientific definitions against primary literature or authoritative
  technical sources;
- distinguish implemented behavior from canonical definitions;
- classify discrepancies, validation gaps, overlaps, and test gaps;
- produce a prioritized, non-binding proposal for later work.

Phase 1 will not fix metric behavior, change preprocessing, add validation,
register methods, rename methods, alter return types, or refactor `core.py`.

## Artifacts

### Machine-readable inventory

`audit/metrics.yaml` will contain one record per registered abbreviation. YAML
is the reviewed source for the audit and future metadata work.

### Human-readable audit

`docs/metric-audit.md` will be deterministically generated from the YAML and
organized by metric family. It will summarize definitions, behavior, sources,
coverage, findings, and recommended future action.

### Validation and characterization

Focused audit tooling and tests will:

- validate the YAML schema;
- require exact identity correspondence with the live 89-entry registry;
- validate reference/source fields;
- generate Markdown deterministically;
- characterize ordinary, ideal, and edge behavior without asserting that a
  questionable behavior is scientifically correct.

## Metric Record Schema

Each YAML record is keyed by registered abbreviation and contains the following
fields.

### Identity

- `name`: registered full name;
- `method`: registered Python method name;
- `category`: one controlled metric-family value.

### Output

- `return_shape`: scalar, tuple with named components, or array shape;
- `implemented_range`: range actually supported by the implementation;
- `ideal_value`: ideal target where one exists, otherwise an explicit
  context-dependent or unknown value.

### Implementation

- `implemented_formula`: a precise mathematical or algorithmic description;
- `preprocessing`: assumptions introduced by constructor or method processing;
- `dependencies`: non-standard numerical/statistical routines used by the
  method.

### Parameters

For every public parameter:

- name;
- default;
- accepted types observed in code;
- actual validation;
- behavior for invalid values.

Use an explicit empty list for methods without parameters.

### Edge cases

Every record covers:

- NaN and infinity behavior;
- zero inputs and zero denominators;
- negative inputs;
- constant series;
- no data remaining after common preprocessing.

Behavior inherited uniformly from construction may cite a shared preprocessing
contract, but metric-specific consequences remain explicit.

### Scientific basis

- `canonical_definition`: the definition supported by primary or authoritative
  sources;
- `references`: stable source identifiers with title, authors or organization,
  year where available, URL or DOI, and the claim the source supports;
- `known_variants`: materially different definitions that explain legitimate
  implementation choices.

Prefer original papers, standards, official technical documentation, or
maintainer documentation. Secondary summaries are permitted only when no
primary or authoritative source can be located, and must be labeled as such.
Unknown facts are recorded as `unknown` with an explanation rather than
inferred.

### Verification

- existing tests covering the method;
- new characterization tests;
- at least one hand-calculated ordinary case;
- at least one relevant edge case.

### Findings

Every metric has zero or more findings using only these controlled types:

- `consistent`;
- `documentation-gap`;
- `test-gap`;
- `validation-gap`;
- `definition-variant`;
- `possible-defect`;
- `duplicate-or-overlap`.

Each finding contains evidence, impact, and a non-binding recommended future
action. `consistent` is used only when the audited implementation, tests, and
canonical definition agree on the claims examined.

## Categories

The initial controlled category set is:

- core error;
- normalized and relative error;
- bias;
- percentage error;
- correlation and agreement;
- efficiency and environmental evaluation;
- distribution and statistical comparison;
- trend and direction;
- diagnostic and decomposition.

A metric receives one primary category even when it could reasonably appear in
several guides. Category changes discovered during audit are YAML/documentation
decisions, not registry changes.

## Batch Process

Audit metrics in registry order in batches of 8–12. Each batch is independently
reviewable and follows this sequence:

1. Export live registry identities.
2. Read every complete implementation and relevant existing test.
3. Add characterization cases for ordinary, ideal, and relevant edge inputs.
4. Research canonical definitions using primary or authoritative sources.
5. Complete the YAML records with explicit citations and findings.
6. Generate the corresponding Markdown content.
7. Run schema, registry-correspondence, characterization, and deterministic
   generation tests.
8. Obtain independent scientific/spec and quality review before starting the
   next batch.

No batch may ingest all remaining metrics at once. Findings are documented, not
fixed, during audit execution.

## Durable Progress

An ignored execution ledger records:

- completed abbreviations;
- commit range and review status for each batch;
- primary sources used;
- unresolved source or interpretation questions;
- cumulative finding counts.

The live registry, committed YAML, and ledger must agree before another batch
begins. This prevents skipped or duplicate audits across long sessions.

## Research Integrity

Each reference must support a specific audit claim. Formula and interpretation
claims should use primary sources whenever available. The audit must distinguish
source-backed facts from implementation-derived observations and reviewer
inferences. Quoted text is unnecessary; formulas and definitions should be
paraphrased with citations.

When several canonical variants exist, the audit records them rather than
selecting one silently. A mismatch is classified as `definition-variant` unless
evidence supports the stronger `possible-defect` classification.

## Success Criteria

Phase 1 is complete when:

- all 89 live registered metrics have schema-complete YAML records;
- every record has at least one ordinary hand-calculated characterization and
  one relevant edge characterization;
- canonical definitions cite primary or authoritative sources where available;
- unknown and disputed facts are explicit;
- registry and YAML identities match exactly with no omissions or extras;
- Markdown generation is deterministic and reproduces the committed report;
- findings are summarized by type and priority;
- full package and audit test suites pass;
- no runtime, registry, dependency, or public-API behavior changes appear in
  the phase diff;
- the report includes a prioritized Phase 2 proposal requiring separate user
  approval.
