from pathlib import Path

from error_metrics import MetricRegistry

README = Path(__file__).parents[1] / "README.md"
START = "<!-- metric-reference:start -->"
END = "<!-- metric-reference:end -->"
FAMILIES_START = "| Family | Relevant abbreviations |"


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


def test_readme_metric_reference_matches_registry():
    text = README.read_text(encoding="utf-8")
    table = text.split(START, 1)[1].split(END, 1)[0]
    rows = [line for line in table.splitlines() if line.startswith("| `")]
    cells = [
        [cell.strip() for cell in row.strip("|").split("|")]
        for row in rows
    ]
    abbreviations = [row[0].strip("`") for row in cells]
    documented = {
        row[0].strip("`"): row[2].strip("`")
        for row in cells
    }
    registered = [
        (key, info.function.__name__)
        for key, info in MetricRegistry.get_all_metrics().items()
    ]

    assert len(rows) == 89
    assert all(len(row) == 6 for row in cells)
    assert len(abbreviations) == len(set(abbreviations))
    assert abbreviations == [key for key, _ in registered]
    assert documented == dict(registered)


def test_readme_metric_families_partition_registry():
    text = README.read_text(encoding="utf-8")
    table = text.split(FAMILIES_START, 1)[1].split("\n\n", 1)[0]
    abbreviations = [
        token.strip("`")
        for line in table.splitlines()[2:]
        for token in line.split("|")[2].strip().split(", ")
    ]

    assert len(abbreviations) == len(set(abbreviations))
    assert set(abbreviations) == set(MetricRegistry.get_all_metrics())
