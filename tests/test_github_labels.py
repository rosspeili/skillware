"""Validate .github/labels.json matches repository label policy."""

import json
import re
from pathlib import Path

LABELS_PATH = Path(__file__).resolve().parent.parent / ".github" / "labels.json"
HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")

REQUIRED_LABELS = {
    "bug",
    "documentation",
    "enhancement",
    "good first issue",
    "help wanted",
    "skill request",
    "skill upgrade",
    "core framework",
    "cli",
    "examples",
    "testing",
    "packaging",
    "ci",
    "security",
    "discussion",
    "question",
    "wontfix",
}


def _load_labels() -> list[dict]:
    return json.loads(LABELS_PATH.read_text(encoding="utf-8"))


def test_labels_json_exists_and_is_array():
    labels = _load_labels()
    assert isinstance(labels, list)
    assert len(labels) >= len(REQUIRED_LABELS)


def test_required_labels_present():
    names = {entry["name"] for entry in _load_labels()}
    missing = REQUIRED_LABELS - names
    assert not missing, f"Missing labels in labels.json: {sorted(missing)}"


def test_label_entries_well_formed():
    names: set[str] = set()
    for entry in _load_labels():
        name = entry.get("name")
        color = entry.get("color", "")
        description = entry.get("description", "")
        assert name and isinstance(name, str)
        assert name not in names, f"Duplicate label: {name}"
        names.add(name)
        assert HEX_COLOR.match(color), f"Bad color for {name}: {color!r}"
        assert description and isinstance(description, str)


def test_rfc_template_labels_exist():
    """Issue template 05_rfc.yml references discussion and core framework."""
    names = {entry["name"] for entry in _load_labels()}
    assert "discussion" in names
    assert "core framework" in names
