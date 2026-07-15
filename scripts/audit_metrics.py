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

COMPLETE_FIELDS = (
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


def validate_inventory(
    inventory: Mapping[str, Any], registry: Mapping[str, Any]
) -> List[str]:
    """Return deterministic validation errors for *inventory*."""
    errors: List[str] = []
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
        if record.get("name") != info.name:
            errors.append(f"{path}.name: does not match registry")
        if record.get("method") != info.function.__name__:
            errors.append(f"{path}.method: does not match registry")

        status = record.get("status")
        if status not in ("pending", "complete"):
            errors.append(f"{path}.status: expected 'pending' or 'complete'")
        if status == "complete":
            for field in COMPLETE_FIELDS:
                if field not in record:
                    errors.append(f"{path}.{field}: missing field")
            if "category" in record and record["category"] not in CATEGORIES:
                errors.append(f"{path}.category: unknown category")
            for field, nested_fields in NESTED_FIELDS.items():
                value = record.get(field)
                if not isinstance(value, dict):
                    if field in record:
                        errors.append(f"{path}.{field}: expected object")
                    continue
                for nested_field in nested_fields:
                    if nested_field not in value:
                        errors.append(
                            f"{path}.{field}.{nested_field}: missing field"
                        )
            references = record.get("scientific_basis", {}).get("references", [])
            if isinstance(references, list):
                for index, reference in enumerate(references):
                    reference_path = f"{path}.scientific_basis.references.{index}"
                    if not isinstance(reference, dict):
                        errors.append(f"{reference_path}: expected object")
                        continue
                    for field in REFERENCE_FIELDS:
                        if field not in reference:
                            errors.append(f"{reference_path}.{field}: missing field")
                    if reference.get("type") not in REFERENCE_TYPES:
                        errors.append(f"{reference_path}.type: unknown source quality")
            findings = record.get("findings", [])
            if isinstance(findings, list):
                for index, finding in enumerate(findings):
                    finding_path = f"{path}.findings.{index}"
                    if not isinstance(finding, dict):
                        errors.append(f"{finding_path}: expected object")
                        continue
                    for field in FINDING_FIELDS:
                        if field not in finding:
                            errors.append(f"{finding_path}.{field}: missing field")
                    if finding.get("type") not in FINDING_TYPES:
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
