# Guided README Redesign

## Goal

Turn the accurate README into an excellent first experience for both package
users and contributors. A new visitor should understand within 30 seconds that
the package offers broad metric coverage, helps them choose an appropriate
metric, and exposes those metrics through one consistent Python API.

The redesign must improve persuasion, navigation, metric selection, examples,
and presentation without weakening the existing technical reference.

## Voice and Presentation

Use a hybrid tone: scientifically credible, precise, and restrained, while
remaining direct and approachable for developers. Establish credibility through
verifiable behavior rather than unsupported superlatives.

Use clean Markdown only:

- a centered title and concise tagline;
- a small badge row for verifiable claims only;
- clear heading hierarchy;
- a compact table of contents;
- short callouts where restrictions matter.

Do not introduce a logo, generated imagery, custom HTML layouts beyond the
simple centered header/badge block, or new maintained visual assets. Do not
claim PyPI availability or describe the package as the best or most
comprehensive library.

## Opening Experience

The README opening will contain:

1. Project title and a concise scientific/developer-oriented tagline.
2. Badges for Python support, tests, license, and the verified metric count.
3. A two-sentence value proposition covering 89 registered metrics, paired
   predictions and observations, and a consistent API for common and
   specialized analysis.
4. A compact contents list.
5. A 30-second start with GitHub installation and one multi-metric example.
6. The example's actual output so the return shape is immediately clear.

Only badge endpoints that truthfully represent the repository without new CI
configuration may be used. If test-status truth cannot be obtained from an
existing workflow, use a static test-count badge rather than implying live CI.

## Metric Selection Guide

Place a practical “Which metric should I use?” guide before the full reference.
It will map common goals to candidate metrics and state their primary tradeoffs:

- original-unit error: `MAE`, `RMSE`, `MedAE`;
- scale-independent comparison: `MASE`, `NMAEp`, `iqRMSE`, `NAE`;
- relative or percentage error: `MAPE`, `sMAPE`, `MAAPE`, `MPE`;
- bias direction or magnitude: `MB`, `MBF`, `RMBF`, `MFB`, `MFE`;
- hydrology and environmental evaluation: `NSE`, KGE variants, `WIA`, `LCE`,
  `DE`;
- association or agreement: `R`, `SpearmanR`, `KendallTau`, `LCCC`, `dCor`;
- distribution comparison: `KLD`, `PHI`, `SUSE`, `AD`;
- trend or directional evaluation: `TAcc`, `PCD`.

Add a caution guide for zeros, negative values, outliers, denominator
restrictions, and metrics with positivity requirements. Recommendations must be
framed as starting points with tradeoffs, never as universally correct choices.
A compact text-based decision flow will direct readers toward a family and then
the complete reference.

## Examples and API Progression

Use one consistent dataset throughout user-facing examples. Present three
progressive workflows:

1. Call one metric directly by Python method name.
2. Calculate a selected group through registered abbreviations.
3. Pass parameters to specialized metrics and inspect the registry.

Show actual output for dictionary-returning and tuple-valued behavior. Every
executable example and displayed output must be verified against the current
package. Use live parameter names such as `n_bins` and `p`.

## Metric Reference

Retain all 89 registered metrics and the existing machine-checkable reference
contract. The documentation test must continue to enforce:

- exactly 89 physical rows;
- exactly six cells per row;
- unique abbreviations;
- registry order;
- exact abbreviation-to-method identity.

Improve scanability by introducing metric-family guideposts around the
reference while preserving a single marker-delimited table that the test can
parse. Shorten purpose text where category notes carry the necessary context.
Keep ranges and ideal values conservative and implementation-backed.

`MSD`, `SB`, `NU`, and `LC` remain excluded because they are not registered.

## Interpretation and Cautions

Keep formulas only when they distinguish similar metrics or materially help
interpretation. Add concise callouts for:

- non-finite input-pair filtering;
- positive or nonnegative input requirements;
- zero-denominator behavior;
- parameter validation;
- sensitivity to scale and outliers.

Do not imply universal NaN handling beyond the verified constructor behavior or
universal suitability for any scientific domain.

## Contributor Path

Keep contributor guidance in the README as a compact closing path:

1. Local development setup.
2. Anatomy of a metric: method, decorator registration, validation, and tests.
3. One complete minimal metric example.
4. Contribution checklist.
5. Test and artifact-build commands.
6. Citation and license.

Remove the second parameterized contributor example unless it teaches behavior
that the complete example and public parameterized-metric examples do not cover.
Do not add the example metric to the package.

## Verification and Success Criteria

The redesign is complete when:

- a visitor can understand the package and run an example within 30 seconds;
- the selection guide helps readers choose a metric family before the full
  reference;
- all claims, outputs, formulas, and parameter names match the live package;
- all 89 registered metrics remain documented and guarded;
- user examples execute successfully;
- the README remains materially shorter and easier to navigate than the former
  795-line version;
- the full test suite passes with only the three known MSLE warnings;
- wheel and sdist artifacts build successfully and include the README;
- runtime code, registry contents, dependencies, and package metadata remain
  unchanged.
