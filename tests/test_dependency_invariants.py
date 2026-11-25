"""A dependency between pieces is data (`depends_on`, extracted from the imports of the code facts) and an
architecture invariant is a seeded rule over it: tests/fixtures/dep_pieces has two packages, graph_ui
and pron, and the rule `graph_ui does not depend on pron` fails when the code imports one from the other."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent / "extract"))

from conftest import REPO  # noqa: E402
from extraction import documents, rules_findings  # noqa: E402

from specir.extract import extract_dependencies  # noqa: E402
from specir.install import package_pythonpath  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "dep_pieces"
RULE = "rule-specir-graph-ui-does-not-depend-on-pron"


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    from conftest import sldb

    root = tmp_path / "dep_pieces"
    shutil.copytree(FIXTURE, root, ignore=shutil.ignore_patterns("__pycache__"))
    sldb("stores", "init", "--path", str(root), cwd=root)
    done = subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root / ".sldb")], cwd=root, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return root


def edges(root: Path) -> dict[str, dict]:
    return {d.name: d.payload for d in documents(root).values() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "depends_on"}


def violations(root: Path) -> list[dict]:
    return [f for f in rules_findings(root) if f.get("code") == f"rules/{RULE}"]


def test_no_import_no_edge_and_the_rule_holds(project):
    report = extract_dependencies(project)
    assert {d.payload["title"] for d in documents(project).values() if d.model_name == "PieceDoc"} == {"graph_ui", "pron"}
    assert not edges(project) and not report.not_derived
    assert not violations(project)


def test_an_import_leaves_the_edge_observed_with_its_site_and_the_rule_reports_it(project):
    view = project / "graph_ui" / "view.py"
    view.write_text(view.read_text() + "\nfrom pron.core import run\n")
    report = extract_dependencies(project)
    [edge] = edges(project).values()
    assert (edge["source_id"], edge["target_id"]) == ("PieceDoc:piece-graph-ui", "PieceDoc:piece-pron")
    assert edge["attributes"]["origen"] == "observado" and edge["attributes"]["verificacion"] == "sin_verificar"
    assert edge["attributes"]["sitios"] == ["graph_ui/view.py (línea desconocida)"]
    assert edge["attributes"]["anchors"]
    assert any("línea del import de pron" in n and n.startswith("desconocido:") for n in report.not_derived)
    [finding] = violations(project)
    assert finding["level"] == "error" and finding["subject"] == "PieceDoc:piece-graph-ui" and "pron" in finding["what"]
    again = extract_dependencies(project)
    assert not again.created and not again.changed and not again.retired


def test_removing_the_import_makes_the_rule_pass(project):
    view = project / "graph_ui" / "view.py"
    original = view.read_text()
    view.write_text(original + "\nfrom pron.core import run\n")
    extract_dependencies(project)
    assert violations(project)
    view.write_text(original)
    report = extract_dependencies(project)
    assert len(report.retired) == 1 and not edges(project)
    assert not violations(project)


def test_relative_imports_stay_inside_the_piece_and_nested_and_conditional_ones_count(project):
    app = project / "graph_ui" / "app.py"  # already `from . import view`: relative, no edge
    extract_dependencies(project)
    assert not edges(project)
    app.write_text(app.read_text() + "\n\ndef late():\n    import pron\n    return pron\n\n\nif __debug__:\n    from pron import core\n")
    extract_dependencies(project)
    [edge] = edges(project).values()
    assert edge["attributes"]["sitios"] == ["graph_ui/app.py (línea desconocida)"]


def test_a_dependency_the_rule_does_not_forbid_is_not_reported(project):
    (project / "pron" / "core.py").write_text("import graph_ui\n")
    extract_dependencies(project)
    assert [e["title"] for e in edges(project).values()] == ["pron depends_on graph_ui"]
    assert not violations(project)
