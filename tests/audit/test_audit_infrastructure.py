import importlib.util
from pathlib import Path
import subprocess
import sys
from copy import deepcopy

from error_metrics import MetricRegistry


ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "audit" / "metrics.yaml"
REPORT_PATH = ROOT / "docs" / "metric-audit.md"
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
        (abbreviation, record["name"], record["method"], record["status"])
        for abbreviation, record in inventory["metrics"].items()
    ] == [
        (
            abbreviation,
            info.name,
            info.function.__name__,
            "pending",
        )
        for abbreviation, info in registry.items()
    ]


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
    assert "metrics.MB.scientific_basis.references.0.year: expected integer" in errors
    assert "metrics.MB.scientific_basis.references.0.extra: unexpected field" in errors
    assert "metrics.MB.findings.0.type: unknown finding type" in errors
    assert "metrics.MB.findings.0.extra: unexpected field" in errors
