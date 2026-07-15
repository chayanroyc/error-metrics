import importlib.util
from pathlib import Path
import subprocess
import sys
from copy import deepcopy

from error_metrics import MetricRegistry


ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "audit" / "metrics.yaml"
REPORT_PATH = ROOT / "docs" / "metric-audit.md"
FINDINGS_PATH = ROOT / "docs" / "metric-audit-findings.md"
SCRIPT_PATH = ROOT / "scripts" / "audit_metrics.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_metrics", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_complete_record(info):
    return {
        "status": "complete",
        "name": info.name,
        "method": info.function.__name__,
        "category": "core error",
        "output": {
            "return_shape": "scalar",
            "implemented_range": "unknown",
            "ideal_value": "unknown",
        },
        "implemented_behavior": {
            "formula": "implementation-derived",
            "preprocessing": ["finite paired values"],
            "dependencies": [],
        },
        "parameters": [],
        "edge_cases": {
            "nan_and_infinity": "unknown",
            "zero_inputs_or_denominators": "unknown",
            "negative_inputs": "unknown",
            "constant_series": "unknown",
            "no_data_after_preprocessing": "unknown",
        },
        "scientific_basis": {
            "canonical_definition": "unknown",
            "references": [],
            "known_variants": [],
        },
        "verification": {
            "existing_tests": [],
            "characterization_tests": [],
            "ordinary_case": "unknown",
            "edge_case": "unknown",
        },
        "findings": [],
    }


def validate_single(record):
    audit_metrics = load_audit_module()
    abbreviation, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record["name"] = info.name
    record["method"] = info.function.__name__
    return audit_metrics.validate_inventory(
        {"schema_version": 1, "metrics": {abbreviation: record}},
        {abbreviation: info},
    )


def valid_reference(year):
    return {
        "type": "primary",
        "title": "Source title",
        "authors_or_organization": "Source author",
        "year": year,
        "url_or_doi": "https://example.com/source",
        "supports": "The audited claim.",
    }


def test_inventory_exists_and_uses_schema_version_one():
    assert INVENTORY_PATH.is_file()
    inventory = load_audit_module().load_inventory(INVENTORY_PATH)
    assert inventory["schema_version"] == 1


def test_inventory_matches_live_registry_order_and_identity():
    inventory = load_audit_module().load_inventory(INVENTORY_PATH)
    registry = MetricRegistry.get_all_metrics()

    assert list(inventory["metrics"]) == list(registry)
    assert len(inventory["metrics"]) == 89
    assert [
        (abbreviation, record["name"], record["method"])
        for abbreviation, record in inventory["metrics"].items()
    ] == [
        (
            abbreviation,
            info.name,
            info.function.__name__,
        )
        for abbreviation, info in registry.items()
    ]
    assert {
        record["status"] for record in inventory["metrics"].values()
    } <= {"pending", "complete"}


def test_valid_pending_inventory_has_no_validation_errors():
    audit_metrics = load_audit_module()
    inventory = audit_metrics.load_inventory(INVENTORY_PATH)
    assert audit_metrics.validate_inventory(
        inventory, MetricRegistry.get_all_metrics()
    ) == []


def test_complete_record_reports_each_missing_field_path():
    audit_metrics = load_audit_module()
    registry = MetricRegistry.get_all_metrics()
    abbreviation, info = next(iter(registry.items()))
    inventory = {
        "schema_version": 1,
        "metrics": {
            abbreviation: {
                "status": "complete",
                "name": info.name,
                "method": info.function.__name__,
            }
        },
    }

    errors = audit_metrics.validate_inventory(
        inventory, {abbreviation: info}
    )

    assert errors == [
        f"metrics.{abbreviation}.category: missing field",
        f"metrics.{abbreviation}.output: missing field",
        f"metrics.{abbreviation}.implemented_behavior: missing field",
        f"metrics.{abbreviation}.parameters: missing field",
        f"metrics.{abbreviation}.edge_cases: missing field",
        f"metrics.{abbreviation}.scientific_basis: missing field",
        f"metrics.{abbreviation}.verification: missing field",
        f"metrics.{abbreviation}.findings: missing field",
    ]


def test_complete_record_reports_missing_nested_field_paths():
    audit_metrics = load_audit_module()
    abbreviation, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = {
        "status": "complete",
        "name": info.name,
        "method": info.function.__name__,
        "category": "core error",
        "output": {},
        "implemented_behavior": {},
        "parameters": [],
        "edge_cases": {},
        "scientific_basis": {},
        "verification": {},
        "findings": [],
    }

    errors = audit_metrics.validate_inventory(
        {"schema_version": 1, "metrics": {abbreviation: record}},
        {abbreviation: info},
    )

    assert f"metrics.{abbreviation}.output.return_shape: missing field" in errors
    assert f"metrics.{abbreviation}.implemented_behavior.formula: missing field" in errors
    assert f"metrics.{abbreviation}.edge_cases.nan_and_infinity: missing field" in errors
    assert f"metrics.{abbreviation}.scientific_basis.references: missing field" in errors
    assert f"metrics.{abbreviation}.verification.ordinary_case: missing field" in errors


def test_renderer_matches_committed_report():
    audit_metrics = load_audit_module()
    inventory = audit_metrics.load_inventory(INVENTORY_PATH)
    assert audit_metrics.render_markdown(inventory) == REPORT_PATH.read_text()


def test_renderer_emits_a_complete_anchored_section_for_every_metric():
    audit_metrics = load_audit_module()
    inventory = audit_metrics.load_inventory(INVENTORY_PATH)
    rendered = audit_metrics.render_markdown(inventory)

    assert rendered.count('<a id="metric-') == 89
    assert '<a id="metric-mb"></a>\n### `MB` — Mean Bias' in rendered
    assert "#### Scientific basis" in rendered
    canonical_definition = inventory["metrics"]["MB"]["scientific_basis"][
        "canonical_definition"
    ]
    assert canonical_definition in rendered
    assert "[Reassessment of the Interagency Workgroup" in rendered
    assert "https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1004TD4.TXT" in rendered
    assert "Some fields define bias with observation minus prediction" in rendered
    assert "mean(predictions) - mean(observations)" in rendered
    assert "tests/audit/test_characterization_batch_1.py::" in rendered
    assert "Document the prediction-minus-observation convention" in rendered


def test_renderer_includes_parameters_output_and_all_edge_case_labels():
    rendered = load_audit_module().render_markdown(
        load_audit_module().load_inventory(INVENTORY_PATH)
    )

    assert (
        '<a id="metric-mase"></a>\n### `MASE` — Mean Absolute Scaled Error'
        in rendered
    )
    assert (
        "| `m` | `1` | any runtime object | "
        "None; the parameter is never inspected."
    ) in rendered
    assert "- Return shape: scalar" in rendered
    for label in (
        "NaN and infinity",
        "Zero inputs or denominators",
        "Negative inputs",
        "Constant series",
        "No data after preprocessing",
    ):
        assert f"- {label}:" in rendered


def test_final_inventory_is_complete_and_characterized():
    inventory = load_audit_module().load_inventory(INVENTORY_PATH)
    records = inventory["metrics"].values()

    assert len(inventory["metrics"]) == 89
    assert all(record["status"] == "complete" for record in records)
    assert all(record["verification"]["ordinary_case"].strip() for record in records)
    assert all(record["verification"]["edge_case"].strip() for record in records)
    assert all(record["verification"]["characterization_tests"] for record in records)


def test_final_inventory_has_references_or_explicit_unknown_explanations():
    inventory = load_audit_module().load_inventory(INVENTORY_PATH)

    for abbreviation, record in inventory["metrics"].items():
        basis = record["scientific_basis"]
        has_reference = bool(basis["references"])
        explicit_unknown = (
            "unknown" in basis["canonical_definition"].lower()
            and len(basis["canonical_definition"].split()) > 1
        )
        assert has_reference or explicit_unknown, abbreviation


def test_final_inventory_uses_every_controlled_finding_type():
    audit_metrics = load_audit_module()
    inventory = audit_metrics.load_inventory(INVENTORY_PATH)
    observed = {
        finding["type"]
        for record in inventory["metrics"].values()
        for finding in record["findings"]
    }

    assert observed == audit_metrics.FINDING_TYPES


def test_synthesis_reports_are_deterministic_and_committed():
    audit_metrics = load_audit_module()
    inventory = audit_metrics.load_inventory(INVENTORY_PATH)

    first_audit = audit_metrics.render_markdown(inventory)
    second_audit = audit_metrics.render_markdown(inventory)
    first_findings = audit_metrics.render_findings_markdown(inventory)
    second_findings = audit_metrics.render_findings_markdown(inventory)

    assert first_audit == second_audit == REPORT_PATH.read_text()
    assert first_findings == second_findings == FINDINGS_PATH.read_text()
    assert "| `possible-defect` | 16 | High |" in first_audit
    assert "| High | 16 |" in first_findings
    assert "requires separate approval" in first_findings


def test_validate_cli_runs_from_repository_root():
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH, "validate"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Inventory valid: 89 metrics\n"


def test_validator_is_total_for_non_object_scientific_basis():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = valid_complete_record(info)
    record["scientific_basis"] = []
    assert "metrics.MB.scientific_basis: expected object" in validate_single(record)


def test_validator_rejects_wrong_container_and_leaf_types():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = valid_complete_record(info)
    record["output"]["return_shape"] = []
    record["implemented_behavior"]["preprocessing"] = "none"
    record["parameters"] = {}
    record["scientific_basis"]["references"] = {}
    record["verification"]["existing_tests"] = "none"
    record["findings"] = {}
    errors = validate_single(record)
    assert "metrics.MB.output.return_shape: expected string" in errors
    assert "metrics.MB.implemented_behavior.preprocessing: expected list" in errors
    assert "metrics.MB.parameters: expected list" in errors
    assert "metrics.MB.scientific_basis.references: expected list" in errors
    assert "metrics.MB.verification.existing_tests: expected list" in errors
    assert "metrics.MB.findings: expected list" in errors


def test_validator_rejects_extra_pending_complete_and_nested_fields():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    pending = {
        "status": "pending",
        "name": info.name,
        "method": info.function.__name__,
        "category": "core error",
    }
    assert "metrics.MB.category: unexpected field" in validate_single(pending)

    complete = valid_complete_record(info)
    complete["extra"] = True
    complete["output"]["extra"] = True
    errors = validate_single(complete)
    assert "metrics.MB.extra: unexpected field" in errors
    assert "metrics.MB.output.extra: unexpected field" in errors


def test_validator_enforces_parameter_contract_and_item_types():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = valid_complete_record(info)
    record["parameters"] = [
        {
            "name": "m",
            "default": 1,
            "accepted_types": ["int"],
            "validation": "positive",
            "invalid_behavior": "raises ValueError",
            "extra": "no",
        },
        "not an object",
    ]
    errors = validate_single(record)
    assert "metrics.MB.parameters.0.extra: unexpected field" in errors
    assert "metrics.MB.parameters.1: expected object" in errors

    missing = deepcopy(record["parameters"][0])
    del missing["validation"]
    missing["accepted_types"] = [1]
    record["parameters"] = [missing]
    errors = validate_single(record)
    assert "metrics.MB.parameters.0.validation: missing field" in errors
    assert "metrics.MB.parameters.0.accepted_types.0: expected string" in errors


def test_validator_enforces_reference_finding_and_controlled_labels():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = valid_complete_record(info)
    record["category"] = "other"
    record["scientific_basis"]["references"] = [{
        "type": "blog",
        "title": "Title",
        "authors_or_organization": "Author",
        "year": "2020",
        "url_or_doi": "https://example.com",
        "supports": "claim",
        "extra": True,
    }]
    record["findings"] = [{
        "type": "bug",
        "evidence": "evidence",
        "impact": "impact",
        "recommended_future_action": "action",
        "extra": True,
    }]
    errors = validate_single(record)
    assert "metrics.MB.category: unknown category" in errors
    assert "metrics.MB.scientific_basis.references.0.type: unknown source quality" in errors
    assert (
        "metrics.MB.scientific_basis.references.0.year: "
        "expected integer or 'unknown'"
    ) in errors
    assert "metrics.MB.scientific_basis.references.0.extra: unexpected field" in errors
    assert "metrics.MB.findings.0.type: unknown finding type" in errors
    assert "metrics.MB.findings.0.extra: unexpected field" in errors


def test_valid_complete_record_has_no_validation_errors():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    record = valid_complete_record(info)
    record["scientific_basis"]["references"] = [valid_reference(2000)]
    assert validate_single(record) == []


def test_reference_year_accepts_integer_or_exact_unknown():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    for year in (2000, "unknown"):
        record = valid_complete_record(info)
        record["scientific_basis"]["references"] = [valid_reference(year)]
        assert validate_single(record) == []


def test_reference_year_rejects_other_strings_null_and_bool():
    _, info = next(iter(MetricRegistry.get_all_metrics().items()))
    for year in ("2000", "Unknown", None, True):
        record = valid_complete_record(info)
        record["scientific_basis"]["references"] = [valid_reference(year)]
        assert (
            "metrics.MB.scientific_basis.references.0.year: "
            "expected integer or 'unknown'"
        ) in validate_single(record)
