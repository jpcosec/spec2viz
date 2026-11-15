"""The chain "publish a post" of the example blog, written by the MCP write tools to a new store
with specIR installed, and read back through the MCP (tests/models/blog.py builds it)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from blog import apply, blog_chain, changes_of
from conftest import BLOG_WRITER

#: The chain of fundamentos §4 the validation names: control, action, endpoint, handler,
#: operation and table, with the relation type of each hop.
CHAIN = [
    "InterfaceControlDoc:publish-button", "triggers",
    "InterfaceActionDoc:publish-action", "invokes",
    "ApiOperationDoc:publish-post-endpoint", "handled_by",
    "HandlerDoc:publish-handler", "executes",
    "DomainOperationDoc:publish-post", "writes",
    "TableDoc:posts",
]
TITLES = ["PublishButton", "PublishAction", "POST /posts/{id}/publish", "publish handler", "PublishPost", "posts"]
ORIGENES = {"observado", "derivado", "inferido", "declarado"}
VERIFICACIONES = {"sin_verificar", "verificado", "refutado"}
INVOKE_RULE = "rules/rule-specir-action-invokes-an-api-operation"
EDGE_RULE = "rules/rule-specir-edges-carry-their-provenance"


def address(session, export_id: str) -> str:
    return session.call("read_document", ref=export_id)["address"]


def hops() -> list[tuple[str, str, str]]:
    return [(CHAIN[i], CHAIN[i + 1], CHAIN[i + 2]) for i in range(0, len(CHAIN) - 1, 2)]


def ends(session, node: str, direction: str, relation: str) -> set[str]:
    key = "target" if direction == "outgoing" else "source"
    return {e[key] for e in session.call("neighbors", node=node, direction=direction, relation=relation)["items"]}


def test_the_chain_is_walked_both_ways_through_the_mcp(blog) -> None:
    nodes = CHAIN[::2]
    assert [blog.call("read_document", ref=n)["payload"]["title"] for n in nodes] == TITLES
    for source, relation, target in hops():
        assert ends(blog, source, "outgoing", relation) == {address(blog, target)}, (source, relation)
        assert ends(blog, target, "incoming", relation) == {address(blog, source)}, (target, relation)
    # From the table back to the button, one hop at a time, by what the index answers only.
    node = address(blog, CHAIN[-1])
    for source, relation, _ in reversed(hops()):
        (node,) = ends(blog, node, "incoming", relation)
        assert node == address(blog, source)


def rules_findings(blog_root) -> list[dict[str, Any]]:
    """What SLDB's rule evaluation reports over the blog store (`sldb rules check`, its on_check
    rules). Its exit code is 1 when a rule fails, so it is read whatever the code."""
    command = [str(Path(sys.executable).with_name("sldb")), "rules", "check", "--store", ".sldb", "--format", "json"]
    done = subprocess.run(command, cwd=blog_root, capture_output=True, text=True)
    assert done.stdout.strip(), done.stderr
    answer = json.loads(done.stdout)
    return answer["findings"] if isinstance(answer, dict) else answer


def test_removing_the_invoked_api_operation_breaks_its_rule(blog, blog_root) -> None:
    endpoint = next(c for c in changes_of("nodes") if c["model"] == "ApiOperationDoc")
    assert not [f for f in rules_findings(blog_root) if f["code"] == INVOKE_RULE]
    removed = apply(blog, [{"action": "delete", "model": endpoint["model"], "name": endpoint["name"]}])
    assert removed["applied"] is True, removed
    try:
        broken = [f for f in rules_findings(blog_root) if f["code"] == INVOKE_RULE]
        assert [(f["level"], f["subject"]) for f in broken] == [("error", "InterfaceActionDoc:publish-action")], broken
    finally:
        restored = apply(blog, [endpoint])
        assert restored["applied"] is True, restored
    assert not [f for f in rules_findings(blog_root) if f["code"] == INVOKE_RULE]


def test_two_views_show_the_one_post(blog) -> None:
    post = address(blog, "DomainEntityDoc:post")
    shown = {}
    for view in ("ViewDoc:post-states", "ViewDoc:publish-components"):
        answer = blog.call("resolve_view", view=view)
        assert answer["found"] and answer["kind"] == "projection", answer
        shown[view] = {n["id"]: n for n in answer["result"]["nodes"]}
    states, components = shown.values()
    assert post in states and post in components
    assert {n["model"] for n in states.values()} != {n["model"] for n in components.values()}
    assert states[post]["payload"] == components[post]["payload"]
    posts = blog.call("select_documents", where='title = "Post"')["items"]
    assert [p["export_id"] for p in posts] == ["DomainEntityDoc:post"], posts


def blog_documents(session) -> list[dict[str, Any]]:
    """Every document of the chain, read through the MCP."""
    written = [c for b in blog_chain()["batches"] for c in b["changes"]]
    refs = [f"{c['model']}:{c['name']}" if "model" in c else f"RelationDoc:{c['name']}" for c in written]
    return [session.call("read_document", ref=ref) for ref in refs]


def test_every_node_and_edge_carries_the_decided_provenance(blog) -> None:
    documents = blog_documents(blog)
    nodes = [d for d in documents if d["model"] not in ("RelationDoc", "ViewDoc")]
    edges = [d for d in documents if d["model"] == "RelationDoc"]
    assert len(nodes) == 10 and len(edges) == 8
    for document in documents:
        assert document["found"] and document["provenance"]["by"] == BLOG_WRITER, document
    for node in nodes:
        payload = node["payload"]
        assert payload["origen"] in ORIGENES and payload["verificacion"] in VERIFICACIONES, node["export_id"]
        # declarado is authored (IR05 D1-B table); what is unknown is null and named.
        assert node["provenance"]["authority"] == "authored", node["export_id"]
        for field in payload["desconocidos"]:
            assert payload.get(field) is None, (node["export_id"], field)
    for edge in edges:
        attributes = edge["payload"]["attributes"]
        assert attributes["origen"] in ORIGENES and attributes["verificacion"] in VERIFICACIONES, edge["export_id"]


@pytest.mark.xfail(strict=True, reason="An edge is a RelationDoc, whose model's authority is generated; SLDB lets no write set authored (IR04 note sldb:20261115-022655, point 4)")
def test_a_declared_edge_is_authored(blog) -> None:
    edges = [d for d in blog_documents(blog) if d["model"] == "RelationDoc"]
    assert {e["provenance"]["authority"] for e in edges} == {"authored"}


def test_an_edge_without_its_provenance_is_refused_by_the_rule(blog) -> None:
    edge = {**changes_of("edges")[0], "name": "ir06-edge-without-provenance", "path": "blog/edges/ir06-edge-without-provenance.md", "attributes": {}}
    refused = apply(blog, [edge])
    assert refused["applied"] is False and refused["rejected"] == "rules" and refused["rules"] == [EDGE_RULE], refused
    assert blog.call("read_document", ref=f"RelationDoc:{edge['name']}")["found"] is False


def test_an_agent_does_not_verify_through_the_mcp(blog) -> None:
    edge = {**changes_of("edges")[0], "name": "ir06-self-verified", "attributes": {"origen": "inferido", "verificacion": "verificado", "verificado_por": "human:jp", "evidencia": "x"}}
    for change in (
        {"action": "update", "model": "DomainEntityDoc", "name": "post", "fields": {"verificacion": "verificado", "verificado_por": "human:jp", "evidencia": "x"}},
        {"action": "update", "model": "RelationDoc", "name": changes_of("edges")[0]["name"], "fields": {"attributes.verificacion": "verificado"}},
        edge,
    ):
        assert "IR05 D2-E" in blog.error_of("propose_changes", changes=[change]), change
    assert blog.call("read_document", ref="DomainEntityDoc:post")["payload"]["verificacion"] == "sin_verificar"


def test_a_relation_between_types_not_allowed_is_reported_by_its_relation_type(blog) -> None:
    wrong = {"action": "assert_edge", "name": "ir06-button-writes-table", "path": "blog/edges/ir06-button-writes-table.md",
             "source": "InterfaceControlDoc:publish-button", "target": "TableDoc:posts", "relation_type": "writes",
             "attributes": {"origen": "declarado", "verificacion": "sin_verificar"}}
    answer = apply(blog, [wrong])
    try:
        assert answer["applied"] is True, answer
        assert any("source_types" in f and "publish-button" in f for f in answer["edge_findings"]), answer["edge_findings"]
        integrity = blog.call("check_integrity")
        assert integrity["ok"] is False and any("publish-button" in f["what"] for f in integrity["findings"]["items"]), integrity
    finally:
        assert apply(blog, [{"action": "retract_edge", "name": wrong["name"]}])["applied"] is True
    assert blog.call("check_integrity")["ok"] is True


@pytest.mark.xfail(strict=True, reason="SLDB checks an edge against its RelationTypeDoc only after the write (check_edges); asked by note sldb:20261115-022655 (IR04), see write_tools.PENDING['edge_validation_before_write']")
def test_a_relation_between_types_not_allowed_is_refused_before_writing(blog) -> None:
    wrong = {"action": "assert_edge", "name": "ir06-button-writes-table-refused", "path": "blog/edges/ir06-button-writes-table-refused.md",
             "source": "InterfaceControlDoc:publish-button", "target": "TableDoc:posts", "relation_type": "writes",
             "attributes": {"origen": "declarado", "verificacion": "sin_verificar"}}
    answer = apply(blog, [wrong])
    try:
        assert answer["applied"] is False
    finally:
        if answer["applied"]:
            apply(blog, [{"action": "retract_edge", "name": wrong["name"]}])
