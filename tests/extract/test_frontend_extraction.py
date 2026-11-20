"""The frontend extractor over tests/fixtures/blog_frontend (IR09), with the backend of
tests/fixtures/blog_app (IR08) extracted in the same store. The fixture has a .tsx (the components),
a .ts (the API client, openapi-fetch style) and a .js (an axios call): one mapping serves them all."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from sldb.api.anchors import check_anchors, check_doc_anchors
from sldb.api.code import code_facts

from conftest import REPO, tree_digest
from extraction import documents, new_project, rules_findings
from test_blog_extraction import anchored_facts

from specir.extract import ExtractionReport, extract, extract_frontend
from specir.install import package_pythonpath
from specir.extract.react_tsx import http_method, normalize

sys.path.insert(0, str(REPO / "tests" / "models"))
from blog import blog_chain  # noqa: E402

FRONTEND = REPO / "tests" / "fixtures" / "blog_frontend"
GAPS = REPO / "tests" / "fixtures" / "blog_frontend_gaps"
INTERFACE = ("InterfaceControlDoc", "InterfaceActionDoc")


@pytest.fixture(scope="module")
def project(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, ExtractionReport]:
    root = new_project(tmp_path_factory.mktemp("frontend"))
    extract(root)
    shutil.copytree(FRONTEND, root / "frontend")
    return root, extract_frontend(root)


@pytest.fixture(scope="module")
def gaps(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, ExtractionReport]:
    """The same frontend plus files whose calls cannot be resolved (a template URL, an endpoint absent from the graph)."""
    root = new_project(tmp_path_factory.mktemp("gaps"))
    extract(root)
    shutil.copytree(FRONTEND, root / "frontend")
    shutil.copytree(GAPS, root / "frontend", dirs_exist_ok=True)
    return root, extract_frontend(root)


def mine(root: Path) -> dict:
    return {k: d for k, d in documents(root).items() if d.model_name in INTERFACE or (d.model_name == "RelationDoc" and d.payload["relation_type"] in ("triggers", "invokes"))}


def golden(model: str) -> list[dict]:
    return [c for b in blog_chain()["batches"] for c in b["changes"] if c.get("model") == model]


def test_the_fixture_has_a_ts_a_tsx_and_a_js_and_they_are_mapped_by_the_same_code() -> None:
    suffixes = {Path(f["path"]).suffix for f in code_facts(FRONTEND)["facts"]}
    assert {".ts", ".tsx", ".js"} <= suffixes
    assert http_method({"name": "client.POST", "first_arg": "/a", "canonical": True}) == http_method({"name": "axios.post", "first_arg": "/a", "canonical": True}) == "POST"


def test_publish_button_triggers_publish_action_that_invokes_the_publish_operation(project) -> None:
    root, _ = project
    found = mine(root)
    (control_id,) = [k for k, d in found.items() if d.model_name == "InterfaceControlDoc"]
    (action_id,) = [k for k, d in found.items() if d.model_name == "InterfaceActionDoc"]
    control, action = found[control_id].payload, found[action_id].payload
    assert (control["title"], control["kind"], control["component"]) == ("PublishButton button", "button", "PublishButton")
    assert (action["title"], action["event"]) == ("handlePublish", "click")
    edges = {(d.payload["source_id"], d.payload["relation_type"], d.payload["target_id"]) for d in found.values() if d.model_name == "RelationDoc"}
    assert (control_id, "triggers", action_id) in edges
    assert (action_id, "invokes", "ApiOperationDoc:api-post-posts-id-publish") in edges
    assert len([e for e in edges if e[1] == "invokes"]) == 1


def test_types_and_relations_are_those_of_the_hand_made_chain(project) -> None:
    root, _ = project
    chain = [c for b in blog_chain()["batches"] for c in b["changes"]]
    want = {(c["source"].split(":")[0], c["relation_type"], c["target"].split(":")[0]) for c in chain if c.get("relation_type") in ("triggers", "invokes")}
    got = {(d.payload["source_id"].split(":")[0], d.payload["relation_type"], d.payload["target_id"].split(":")[0]) for d in mine(root).values() if d.model_name == "RelationDoc"}
    assert want == got
    assert golden("InterfaceControlDoc") and golden("InterfaceActionDoc")
    assert {d.model_name for d in mine(root).values()} >= set(INTERFACE)


def test_every_node_and_edge_has_anchors_with_file_line_and_source_hash_of_the_facts(project) -> None:
    root, _ = project
    held = {d.name: d for d in documents(root).values() if d.model_name == "CodeAnchorDoc"}
    facts = anchored_facts(root)
    for export_id, doc in mine(root).items():
        text = doc.payload.get("description") or doc.payload.get("notes")
        named = set(re.findall(r"\[(anchor-[0-9a-f]{16})\]", text))
        assert named and named <= set(held), export_id
        for name in named:
            fact = facts[held[name].payload["ref"]]
            claim = held[name].payload["claim"]
            assert fact["path"] in claim and fact["source_hash"] in claim and f"líneas {fact['span']['start_line']}-{fact['span']['end_line']}" in claim
        if doc.model_name == "RelationDoc":
            assert {held[n].payload["ref"] for n in named} == set(doc.payload["attributes"]["anchors"])
    assert [r for r in check_anchors(root / ".sldb", package_pythonpath()) if r.state.value != "intact"] == []
    assert check_doc_anchors(root / ".sldb", package_pythonpath()) == []


def test_provenance_is_observed_or_derived_and_never_verified(project) -> None:
    root, _ = project
    for export_id, doc in mine(root).items():
        fields = doc.payload["attributes"] if doc.model_name == "RelationDoc" else doc.payload
        assert fields["verificacion"] == "sin_verificar" and not fields["verificado_por"] and not fields["evidencia"], export_id
        assert fields["origen"] == ("derivado" if doc.model_name == "RelationDoc" else "observado"), export_id
    invokes = next(d for d in mine(root).values() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "invokes")
    assert "http-call-resolves-to-api-operation" in invokes.payload["notes"]


def test_a_non_literal_url_creates_no_relation_and_is_a_declared_gap(gaps) -> None:
    root, report = gaps
    assert any("src/api/search.ts:4" in n and "axios.get" in n and "hueco declarado" in n for n in report.not_derived), report.not_derived
    assert not any("search" in k for k, d in mine(root).items() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "invokes")


def test_a_fetch_with_a_literal_url_is_a_declared_gap_and_leaves_no_undeclared_action(gaps) -> None:
    root, report = gaps
    assert any("src/api/fetcher.ts:2" in n and "fetch" in n and "hueco declarado" in n for n in report.not_derived), report.not_derived
    docs = mine(root)
    action = [k for k, d in docs.items() if d.model_name == "InterfaceActionDoc" and d.payload["title"] == "handleLoad"]
    assert action
    assert not [d for d in docs.values() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "invokes" and d.payload["source_id"] in action]


def test_a_call_to_an_endpoint_absent_from_the_graph_is_a_breach_and_invents_nothing(gaps) -> None:
    root, report = gaps
    assert any("src/api/legacy_archive.js:4" in n and "axios.delete" in n and "brecha" in n for n in report.not_derived), report.not_derived
    assert not [d for d in documents(root).values() if d.model_name == "ApiOperationDoc" and "archive" in d.payload["route"]]
    invokes = [d for d in mine(root).values() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "invokes"]
    assert len(invokes) == 1


def test_the_relations_pass_edges_and_rules_checks(project) -> None:
    root, _ = project
    done = subprocess.run([str(Path(sys.executable).with_name("sldb")), "edges", "check", "--store", ".sldb"], cwd=root, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert [f for f in rules_findings(root) if f["level"] == "error"] == []


def test_a_second_run_leaves_the_store_identical(tmp_path) -> None:
    root = new_project(tmp_path)
    extract(root)
    shutil.copytree(FRONTEND, root / "frontend")
    first = extract_frontend(root)
    before = tree_digest(root / ".sldb", root / "specir")
    second = extract_frontend(root)
    assert tree_digest(root / ".sldb", root / "specir") == before
    assert second.created == [] and second.changed == [] and sorted(second.unchanged) == sorted(first.created)


def test_the_route_comparison_follows_the_rules_of_the_brief() -> None:
    assert normalize("/posts/{pk}/publish/?x=1") == normalize("/posts/{id}/publish") == ("posts", "{}", "publish")
    assert normalize("/posts/1/publish") != normalize("/posts/{id}/publish")
    assert http_method({"name": "fetch", "first_arg": "/a", "canonical": True}) is None
    assert http_method({"name": "axios.get", "first_arg": None, "canonical": True}) is None
    assert http_method({"name": "axios.get", "first_arg": "/a", "canonical": False}) is None
    assert http_method({"name": "api.helper", "first_arg": "/a", "canonical": True}) is None


def test_the_frontend_reads_no_code_itself() -> None:
    forbidden = re.compile(r"tree_sitter|import ast|from ast|pglast|read_bytes|read_text|sldb\.code\b|spec2viz")
    path = REPO / "src" / "specir" / "extract" / "react_tsx.py"
    assert not forbidden.search(path.read_text(encoding="utf-8"))
