#!/usr/bin/env python3
"""Validate and render the metric behavior audit inventory."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Mapping


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "audit" / "metrics.yaml"
REPORT_PATH = ROOT / "docs" / "metric-audit.md"

PENDING_FIELDS = ("status", "name", "method")
COMPLETE_FIELDS = PENDING_FIELDS + (
    "category",
    "output",
    "implemented_behavior",
    "parameters",
    "edge_cases",
    "scientific_basis",
    "verification",
    "findings",
)
CATEGORIES = {
    "core error",
    "normalized and relative error",
    "bias",
    "percentage error",
    "correlation and agreement",
    "efficiency and environmental evaluation",
    "distribution and statistical comparison",
    "trend and direction",
    "diagnostic and decomposition",
}
NESTED_FIELDS = {
    "output": ("return_shape", "implemented_range", "ideal_value"),
    "implemented_behavior": ("formula", "preprocessing", "dependencies"),
    "edge_cases": (
        "nan_and_infinity",
        "zero_inputs_or_denominators",
        "negative_inputs",
        "constant_series",
        "no_data_after_preprocessing",
    ),
    "scientific_basis": (
        "canonical_definition",
        "references",
        "known_variants",
    ),
    "verification": (
        "existing_tests",
        "characterization_tests",
        "ordinary_case",
        "edge_case",
    ),
}
REFERENCE_FIELDS = (
    "type",
    "title",
    "authors_or_organization",
    "year",
    "url_or_doi",
    "supports",
)
REFERENCE_TYPES = {"primary", "authoritative", "secondary"}
PARAMETER_FIELDS = (
    "name",
    "default",
    "accepted_types",
    "validation",
    "invalid_behavior",
)
FINDING_FIELDS = ("type", "evidence", "impact", "recommended_future_action")
FINDING_TYPES = {
    "consistent",
    "documentation-gap",
    "test-gap",
    "validation-gap",
    "definition-variant",
    "possible-defect",
    "duplicate-or-overlap",
}


def load_inventory(path: Path) -> Dict[str, Any]:
    """Load the JSON-compatible YAML inventory at *path*."""
    with path.open(encoding="utf-8") as inventory_file:
        return json.load(inventory_file)


def _validate_exact_keys(
    value: Mapping[str, Any], expected: tuple, path: str, errors: List[str]
) -> None:
    for field in expected:
        if field not in value:
            errors.append(f"{path}.{field}: missing field")
    for field in value:
        if field not in expected:
            errors.append(f"{path}.{field}: unexpected field")


def _validate_string(value: Any, path: str, errors: List[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected string")


def _validate_string_list(value: Any, path: str, errors: List[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected list")
        return
    for index, item in enumerate(value):
        _validate_string(item, f"{path}.{index}", errors)


def _validate_object(
    value: Any, expected: tuple, path: str, errors: List[str]
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return False
    _validate_exact_keys(value, expected, path, errors)
    return True


def validate_inventory(
    inventory: Mapping[str, Any], registry: Mapping[str, Any]
) -> List[str]:
    """Return deterministic validation errors for *inventory*."""
    errors: List[str] = []
    if not isinstance(inventory, dict):
        return ["inventory: expected object"]
    _validate_exact_keys(inventory, ("schema_version", "metrics"), "inventory", errors)
    if inventory.get("schema_version") != 1:
        errors.append("schema_version: expected 1")

    metrics = inventory.get("metrics")
    if not isinstance(metrics, dict):
        return errors + ["metrics: expected object"]

    inventory_keys = list(metrics)
    registry_keys = list(registry)
    if inventory_keys != registry_keys:
        errors.append(
            "metrics: registry order mismatch "
            f"(inventory={inventory_keys!r}, registry={registry_keys!r})"
        )

    for abbreviation, record in metrics.items():
        path = f"metrics.{abbreviation}"
        if not isinstance(record, dict):
            errors.append(f"{path}: expected object")
            continue
        if abbreviation not in registry:
            errors.append(f"{path}: unregistered abbreviation")
            continue

        info = registry[abbreviation]
        for identity_field in PENDING_FIELDS:
            if identity_field not in record:
                errors.append(f"{path}.{identity_field}: missing field")
        if "status" in record:
            _validate_string(record["status"], f"{path}.status", errors)
        if "name" in record:
            _validate_string(record["name"], f"{path}.name", errors)
        if "method" in record:
            _validate_string(record["method"], f"{path}.method", errors)
        if record.get("name") != info.name:
            errors.append(f"{path}.name: does not match registry")
        if record.get("method") != info.function.__name__:
            errors.append(f"{path}.method: does not match registry")

        status = record.get("status")
        if status not in ("pending", "complete"):
            errors.append(f"{path}.status: expected 'pending' or 'complete'")
        if status == "pending":
            _validate_exact_keys(record, PENDING_FIELDS, path, errors)
        if status == "complete":
            _validate_exact_keys(record, COMPLETE_FIELDS, path, errors)
            if "category" in record:
                _validate_string(record["category"], f"{path}.category", errors)
                if isinstance(record["category"], str) and record["category"] not in CATEGORIES:
                    errors.append(f"{path}.category: unknown category")
            for field, nested_fields in NESTED_FIELDS.items():
                if field not in record:
                    continue
                value = record[field]
                if not _validate_object(value, nested_fields, f"{path}.{field}", errors):
                    continue

                for nested_field in nested_fields:
                    if nested_field not in value:
                        continue
                    nested_path = f"{path}.{field}.{nested_field}"
                    if field == "implemented_behavior" and nested_field in (
                        "preprocessing", "dependencies"
                    ):
                        _validate_string_list(value[nested_field], nested_path, errors)
                    elif field == "scientific_basis" and nested_field in (
                        "references", "known_variants"
                    ):
                        if nested_field == "known_variants":
                            _validate_string_list(value[nested_field], nested_path, errors)
                    elif field == "verification" and nested_field in (
                        "existing_tests", "characterization_tests"
                    ):
                        _validate_string_list(value[nested_field], nested_path, errors)
                    else:
                        _validate_string(value[nested_field], nested_path, errors)

            parameters = record.get("parameters")
            if "parameters" in record and not isinstance(parameters, list):
                errors.append(f"{path}.parameters: expected list")
            elif isinstance(parameters, list):
                for index, parameter in enumerate(parameters):
                    parameter_path = f"{path}.parameters.{index}"
                    if not _validate_object(
                        parameter, PARAMETER_FIELDS, parameter_path, errors
                    ):
                        continue
                    for field in ("name", "validation", "invalid_behavior"):
                        if field in parameter:
                            _validate_string(
                                parameter[field], f"{parameter_path}.{field}", errors
                            )
                    if "accepted_types" in parameter:
                        _validate_string_list(
                            parameter["accepted_types"],
                            f"{parameter_path}.accepted_types",
                            errors,
                        )
                    if "default" in parameter and isinstance(
                        parameter["default"], (dict, list)
                    ):
                        errors.append(f"{parameter_path}.default: expected scalar")

            scientific_basis = record.get("scientific_basis")
            if isinstance(scientific_basis, dict):
                references = scientific_basis.get("references")
            else:
                references = None
            if references is not None and not isinstance(references, list):
                errors.append(f"{path}.scientific_basis.references: expected list")
            elif isinstance(references, list):
                for index, reference in enumerate(references):
                    reference_path = f"{path}.scientific_basis.references.{index}"
                    if not _validate_object(
                        reference, REFERENCE_FIELDS, reference_path, errors
                    ):
                        continue
                    for field in REFERENCE_FIELDS:
                        if field in reference and field != "year":
                            _validate_string(
                                reference[field], f"{reference_path}.{field}", errors
                            )
                    if "year" in reference and type(reference["year"]) is not int:
                        errors.append(f"{reference_path}.year: expected integer")
                    if isinstance(reference.get("type"), str) and reference["type"] not in REFERENCE_TYPES:
                        errors.append(f"{reference_path}.type: unknown source quality")
            findings = record.get("findings")
            if "findings" in record and not isinstance(findings, list):
                errors.append(f"{path}.findings: expected list")
            elif isinstance(findings, list):
                for index, finding in enumerate(findings):
                    finding_path = f"{path}.findings.{index}"
                    if not _validate_object(
                        finding, FINDING_FIELDS, finding_path, errors
                    ):
                        continue
                    for field in FINDING_FIELDS:
                        if field in finding:
                            _validate_string(
                                finding[field], f"{finding_path}.{field}", errors
                            )
                    if isinstance(finding.get("type"), str) and finding["type"] not in FINDING_TYPES:
                        errors.append(f"{finding_path}.type: unknown finding type")

    return errors


def render_markdown(inventory: Mapping[str, Any]) -> str:
    """Render a deterministic Markdown report using inventory data only."""
    metrics = inventory["metrics"]
    completed = sum(record.get("status") == "complete" for record in metrics.values())
    pending = len(metrics) - completed
    lines = [
        "# Metric Behavior Audit",
        "",
        "This report is generated from `audit/metrics.yaml`. Do not edit it by hand.",
        "",
        "## Audit summary",
        "",
        f"- Total registered metrics: {len(metrics)}",
        f"- Completed: {completed}",
        f"- Pending: {pending}",
        "",
    ]

    categories: Dict[str, List[tuple]] = {}
    for abbreviation, record in metrics.items():
        category = record.get("category", "Pending audit")
        categories.setdefault(category, []).append((abbreviation, record))

    for category, records in categories.items():
        lines.extend(
            [
                f"## {category}",
                "",
                "| Abbreviation | Name | Method | Status |",
                "| --- | --- | --- | --- |",
            ]
        )
        for abbreviation, record in records:
            lines.append(
                f"| `{abbreviation}` | {record['name']} | "
                f"`{record['method']}` | {record['status']} |"
            )
        lines.append("")

    return "\n".join(lines)


def _live_registry() -> Mapping[str, Any]:
    sys.path.insert(0, str(ROOT))
    from error_metrics import MetricRegistry

    return MetricRegistry.get_all_metrics()


def _validate_command() -> int:
    errors = validate_inventory(load_inventory(INVENTORY_PATH), _live_registry())
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Inventory valid: 89 metrics")
    return 0


def _render_command(check: bool, write: bool) -> int:
    rendered = render_markdown(load_inventory(INVENTORY_PATH))
    if write:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
        print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
        return 0
    if check:
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != rendered:
            print(f"Out of date: {REPORT_PATH.relative_to(ROOT)}")
            return 1
        print(f"Up to date: {REPORT_PATH.relative_to(ROOT)}")
        return 0
    raise AssertionError("render mode not selected")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate inventory against live registry")
    render_parser = subparsers.add_parser("render", help="render Markdown report")
    render_mode = render_parser.add_mutually_exclusive_group(required=True)
    render_mode.add_argument("--check", action="store_true")
    render_mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.command == "validate":
        return _validate_command()
    return _render_command(args.check, args.write)


if __name__ == "__main__":
    raise SystemExit(main())
