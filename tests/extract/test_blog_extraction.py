"""The extractor over tests/fixtures/blog_app (IR08): what it writes, with what provenance, and what
a second run or a change of the code does."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
import yaml

import sldb.api as api
from sldb.api.anchors import check_anchors, check_doc_anchors
from sldb.api.code import code_facts

from conftest import REPO, tree_digest
from extraction import BACKEND_AND_DATA, documents, extracted, new_project, rules_findings, triples

from specir.extract import ExtractionReport, extract
from specir.extract import write as writer
from specir.extract.django_drf import interpret
from specir.extract.facts import Facts
from specir.install import package_pythonpath

GOLDEN = yaml.safe_load((REPO / "tests" / "fixtures" / "blog_chain.yaml").read_text(encoding="utf-8"))
GOLDEN_RELATIONS = {"handled_by", "executes", "governed_by", "writes", "persisted_in"}


@pytest.fixture(scope="module")
def project(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, ExtractionReport]:
    root = new_project(tmp_path_factory.mktemp("extract"))
    return root, extract(root)


def golden_model(ref: str) -> str:
    return ref.split(":")[0]


def test_it_extracts_the_nodes_and_relations_of_the_hand_made_chain(project) -> None:
    root, _ = project
    golden = [c for b in GOLDEN["batches"] for c in b["changes"]]
    nodes = [c for c in golden if c.get("model") in BACKEND_AND_DATA]
    edges = [c for c in golden if c.get("relation_type") in GOLDEN_RELATIONS]
    found = [d for d in extracted(root).values() if d.model_name in BACKEND_AND_DATA]
    for model in BACKEND_AND_DATA:
        want = sorted(n["payload"]["title"] for n in nodes if n["model"] == model)
        got = sorted(d.payload["title"] for d in found if d.model_name == model)
        assert len(got) == len(want), (model, want, got)
    assert {(golden_model(e["source"]), e["relation_type"], golden_model(e["target"])) for e in edges} == triples(root)
    titles = {d.payload["title"] for d in found}
    assert {"POST /posts/{id}/publish", "posts", "Post", "Draft", "Published", "can_publish", "PostViewSet.publish", "Post.publish"} <= titles


def test_the_route_is_made_from_register_and_action(project) -> None:
    root, _ = project
    (route,) = [d for d in extracted(root).values() if d.model_name == "ApiOperationDoc"]
    assert (route.payload["method"], route.payload["route"], route.payload["origen"]) == ("POST", "/posts/{id}/publish", "derivado")
    assert "drf-router-register-action" in route.payload["description"]
    handler = documents(root)["HandlerDoc:handler-postviewset-publish"]
    assert (handler.payload["symbol"], handler.payload["origen"]) == ("PostViewSet.publish", "observado")


def test_the_tables_columns_and_keys_come_from_the_sql_facts(project) -> None:
    root, _ = project
    table = documents(root)["TableDoc:table-posts"].payload
    assert table["columns"] == ["id", "title", "body", "status", "published_at", "author_id"]
    assert "id bigint PK identity" in table["description"]
    assert "foreign_key posts_author_id_099b8aca_fk_auth_user_id (author_id) -> auth_user (id)" in table["description"]
    assert table["origen"] == "observado" and table["desconocidos"] == {"schema_name": "el SQL leído no dice el esquema de la tabla"}
    constraint = next(f for f in code_facts(root, ["sql"])["facts"] if f["kind"] == "constraint")
    assert constraint["attrs"]["constraint_type"] == "foreign_key" and constraint["attrs"]["references"] == {"table": "auth_user", "columns": ["id"]}


def test_the_transition_without_a_fact_is_reported_as_not_derived(project) -> None:
    root, report = project
    assert not any(d.payload.get("relation_type") == "transitions" for d in extracted(root).values() if d.model_name == "RelationDoc")
    assert any("transitions" in item and "Post.publish" in item for item in report.not_derived), report.not_derived
    assert any("rutas CRUD" in item for item in report.not_derived)


def anchored_facts(root: Path) -> dict[str, dict]:
    return {f"code:{f['path']}::" + ("" if f["id"] == f["attrs"]["module"] else f["id"].removeprefix(f["attrs"]["module"] + ".")): f for f in code_facts(root)["facts"]}


def test_every_node_and_edge_names_anchors_with_file_line_and_source_hash(project) -> None:
    root, _ = project
    held = {d.name: d for d in documents(root).values() if d.model_name == "CodeAnchorDoc"}
    facts = anchored_facts(root)
    assert held
    for doc in held.values():
        fact = facts[doc.payload["ref"]]
        assert f"líneas {fact['span']['start_line']}-{fact['span']['end_line']}" in doc.payload["claim"]
        assert fact["source_hash"] in doc.payload["claim"] and fact["path"] in doc.payload["claim"]
        assert doc.payload["seen"] == fact["fingerprints"]
    for export_id, doc in extracted(root).items():
        text = doc.payload.get("description") or doc.payload.get("notes")
        named = set(re.findall(r"\[(anchor-[0-9a-f]{16})\]", text))
        assert named and named <= set(held), export_id
        if doc.model_name == "RelationDoc":
            assert {held[n].payload["ref"] for n in named} == set(doc.payload["attributes"]["anchors"]), export_id
    assert [r for r in check_anchors(root / ".sldb", package_pythonpath()) if r.state.value != "intact"] == []
    assert check_doc_anchors(root / ".sldb", package_pythonpath()) == []


def test_provenance_is_observed_or_derived_and_never_verified(project) -> None:
    root, _ = project
    for export_id, doc in extracted(root).items():
        fields = doc.payload["attributes"] if doc.model_name == "RelationDoc" else doc.payload
        assert fields["origen"] in ("observado", "derivado"), export_id
        assert fields["verificacion"] == "sin_verificar" and not fields["verificado_por"] and not fields["evidencia"], export_id
        if doc.model_name == "RelationDoc":
            assert fields["origen"] == "derivado"


def test_relations_pass_their_relation_types_and_the_rules(project) -> None:
    root, _ = project
    done = subprocess.run([str(Path(__import__("sys").executable).with_name("sldb")), "edges", "check", "--store", ".sldb"], cwd=root, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert [f for f in rules_findings(root) if f["level"] == "error"] == []


def test_a_second_run_leaves_the_store_identical(tmp_path) -> None:
    root = new_project(tmp_path)
    first = extract(root)
    before = tree_digest(root / ".sldb", root / "specir")
    second = extract(root)
    assert tree_digest(root / ".sldb", root / "specir") == before
    assert second.created == [] and second.changed == [] and sorted(second.unchanged) == sorted(first.created)


def edit(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_a_changed_file_flags_its_nodes_and_never_overwrites_a_verified_one(tmp_path) -> None:
    root = new_project(tmp_path)
    extract(root)
    store, pythonpath = root / ".sldb", package_pythonpath()
    verified = {"verificacion": "verificado", "verificado_por": "human:jp", "evidencia": "revisado a mano"}
    policy = documents(root)["PolicyDoc:policy-can-publish"]
    api.save_document_payload(store, "PolicyDoc", policy.name, {**policy.payload, **verified}, pythonpath)
    edge = documents(root)["RelationDoc:edge-op-post-publish--governed_by--policy-can-publish"]
    api.save_document_payload(store, "RelationDoc", edge.name, {**edge.payload, "attributes": {**edge.payload["attributes"], **verified}}, pythonpath)
    kept = {k: documents(root)[k].payload for k in ("PolicyDoc:policy-can-publish", "RelationDoc:edge-op-post-publish--governed_by--policy-can-publish")}

    edit(root, "blog/models.py", 'return user == post.author or user.has_perm("blog.change_post")', 'return user == post.author or user.is_staff')
    report = extract(root)

    assert set(report.changed) == {"PolicyDoc:policy-can-publish", "RelationDoc:edge-op-post-publish--governed_by--policy-can-publish"}
    assert report.created == []
    assert "TableDoc:table-posts" in report.unchanged and "ApiOperationDoc:api-post-posts-id-publish" in report.unchanged
    after = documents(root)
    for key, payload in kept.items():
        assert after[key].payload == payload, key
        fields = payload.get("attributes") or payload
        assert fields["verificacion"] == "verificado" and fields["verificado_por"] == "human:jp"


def test_a_changed_file_updates_what_was_not_verified(tmp_path) -> None:
    root = new_project(tmp_path)
    extract(root)
    edit(root, "blog/models.py", '    """Publish the post: it becomes visible to readers."""\n', "")
    edit(root, "blog/models.py", "        self.published_at = timezone.now()\n", "        self.published_at = timezone.now()\n        self.status = self.Status.PUBLISHED\n")
    report = extract(root)
    assert "DomainOperationDoc:op-post-publish" in report.changed
    assert "TableDoc:table-posts" in report.unchanged
    assert [r for r in check_anchors(root / ".sldb", package_pythonpath()) if r.state.value != "intact"] == []


def test_an_anchor_that_does_not_match_stops_everything_before_writing(tmp_path) -> None:
    root = new_project(tmp_path)
    stale = interpret(Facts(code_facts(root)["facts"]))
    edit(root, "blog/models.py", "def can_publish(user, post: Post) -> bool:", "def can_publish(user, post: Post, extra=None) -> bool:")
    before = tree_digest(root / ".sldb", root / "specir")
    with pytest.raises(ValueError, match=r"code:blog/models\.py::"):
        writer.write_plan(root / ".sldb", root, package_pythonpath(), list(stale.nodes.values()), list(stale.edges.values()), [])
    assert tree_digest(root / ".sldb", root / "specir") == before


def test_the_extractor_reads_no_code_itself() -> None:
    forbidden = re.compile(r"tree_sitter|import ast|from ast|pglast|sldb\.code\b|import pron|spec2viz")
    for path in sorted((REPO / "src" / "specir" / "extract").glob("*.py")):
        assert not forbidden.search(path.read_text(encoding="utf-8")), path


def test_a_function_of_the_project_without_a_policy_signal_is_reported_not_dropped(tmp_path) -> None:
    root = new_project(tmp_path)
    models = (root / "blog" / "models.py").read_text(encoding="utf-8").replace("can_publish", "ensure_publishable")
    (root / "blog" / "models.py").write_text(models, encoding="utf-8")
    report = extract(root)
    assert not [d for d in extracted(root).values() if d.model_name == "PolicyDoc"]
    assert not any(d.payload.get("relation_type") == "governed_by" for d in extracted(root).values() if d.model_name == "RelationDoc")
    assert any("ensure_publishable" in item and "sin señal de política" in item for item in report.not_derived), report.not_derived


def test_the_predicate_convention_is_named_in_what_it_creates(project) -> None:
    root, _ = project
    edge = documents(root)["RelationDoc:edge-op-post-publish--governed_by--policy-can-publish"]
    assert "convención de specIR" in edge.payload["notes"] and "can_/is_/has_/may_" in edge.payload["notes"]


def test_a_relation_the_new_plan_no_longer_produces_is_flagged_and_kept(tmp_path) -> None:
    root = new_project(tmp_path)
    extract(root)
    writes = "RelationDoc:edge-op-post-publish--writes--table-posts"
    assert writes in documents(root)
    edit(root, "blog/models.py", '        self.save(update_fields=["status", "published_at"])\n', "")
    before = documents(root)[writes].payload
    report = extract(root)
    assert writes in report.changed, report
    assert writes in documents(root) and documents(root)[writes].payload == before
