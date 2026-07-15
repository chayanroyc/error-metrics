import importlib.util
from pathlib import Path
import subprocess
import sys

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
