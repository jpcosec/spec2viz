"""IR10: specIR's cross-layer rules and its impact analysis, through the real `sldb mcp` server
(tools `specir_rules` and `specir_impact`) over the blog store (tests/models/blog.py).

Each rule has a seeded gap: an element of the complete blog chain is removed (or added unbound)
through the MCP write tools, the rule engine of sldb reports it with its severity, the rule and the
document, and the element is restored. The complete chain reports nothing."""

from __future__ import annotations

from typing import Any

import pytest
from blog import apply, blog_chain, changes_of
from conftest import REPO, served, tree_digest

OWN = "rule-specir-"


def every(session, tool: str, **arguments: Any) -> list[dict[str, Any]]:
    answer = session.call(tool, limit=200, **arguments)
    assert not answer["truncated"], answer
    return answer["items"]


def findings(session) -> list[tuple[str, str, str]]:
    return [(f["severity"], f["rule"], f["subject"]) for f in every(session, "specir_rules")]


def node(model: str) -> dict[str, Any]:
    return next(c for c in changes_of("nodes") if c["model"] == model)


def named(name: str) -> dict[str, Any]:
    return next(c for c in changes_of("nodes") if c["name"] == name)


def edge(name: str) -> dict[str, Any]:
    return next(c for c in changes_of("edges") if c["name"] == name)


def delete(change: dict[str, Any]) -> dict[str, Any]:
    return {"action": "delete", "model": "RelationDoc" if change["action"] == "assert_edge" else change["model"], "name": change["name"]}


#: rule, severity, the subject it reports, and the element of the chain whose absence seeds the gap.
GAPS = [
    ("rule-specir-control-triggers-an-action", "alert", "InterfaceControlDoc:publish-button", "publish-action"),
    ("rule-specir-action-invokes-an-api-operation", "error", "InterfaceActionDoc:publish-action", "publish-post-endpoint"),
    ("rule-specir-api-operation-is-handled", "alert", "ApiOperationDoc:publish-post-endpoint", "publish-handler"),
    ("rule-specir-handler-executes-a-domain-operation", "alert", "HandlerDoc:publish-handler", "publish-post"),
    ("rule-specir-entity-is-persisted", "alert", "DomainEntityDoc:post", "posts"),
    ("rule-specir-policy-reaches-the-interface", "alert", "PolicyDoc:can-publish", "publish-button"),
]


def test_the_complete_chain_has_no_findings(blog) -> None:
    assert findings(blog) == []
    answer = blog.call("specir_rules")
    assert answer["total"] == 0 and answer["explanation"]


@pytest.mark.parametrize(("rule", "severity", "subject", "removed"), GAPS, ids=[g[0] for g in GAPS])
def test_a_seeded_gap_is_reported_with_its_severity_rule_and_document(blog, rule, severity, subject, removed) -> None:
    change = named(removed)
    assert apply(blog, [delete(change)])["applied"] is True
    try:
        reported = [f for f in every(blog, "specir_rules") if f["rule"] == rule]
        assert [(f["severity"], f["subject"]) for f in reported] == [(severity, subject)], reported
        assert reported[0]["path"] and reported[0]["what"] and reported[0]["address"] == f"sldb://document/{subject}"
        assert [f["rule"] for f in every(blog, "specir_rules", severity=severity)].count(rule) == 1
    finally:
        assert apply(blog, [change])["applied"] is True
    assert findings(blog) == []


def test_an_interface_field_the_serializer_lacks_is_reported(blog) -> None:
    field = {"action": "create", "model": "InterfaceFieldDoc", "name": "title-input", "path": "blog/interface/title-input.md",
             "payload": {"title": "title input", "origen": "declarado", "description": "The title the editor shows."}}
    api_field = {"action": "create", "model": "ApiFieldDoc", "name": "post-title", "path": "blog/api/post-title.md",
                 "payload": {"title": "post title", "origen": "declarado", "description": "The title the serializer carries."}}
    bound = {"action": "assert_edge", "name": "title-input-bound-to-post-title", "path": "blog/edges/title-input-bound-to-post-title.md",
             "source": "InterfaceFieldDoc:title-input", "target": "ApiFieldDoc:post-title", "relation_type": "bound_to",
             "attributes": {"origen": "declarado", "verificacion": "sin_verificar"}}
    assert apply(blog, [field])["applied"] is True
    try:
        assert findings(blog) == [("error", "rule-specir-interface-field-is-served", "InterfaceFieldDoc:title-input")]
        assert apply(blog, [api_field, bound])["applied"] is True
        assert findings(blog) == []
    finally:
        apply(blog, [delete(bound), delete(api_field), delete(field)])
    assert findings(blog) == []


CHAIN = ["InterfaceControlDoc:publish-button", "InterfaceActionDoc:publish-action", "ApiOperationDoc:publish-post-endpoint",
         "HandlerDoc:publish-handler", "DomainOperationDoc:publish-post", "TableDoc:posts"]
RELATIONS = ["triggers", "invokes", "handled_by", "executes", "writes"]


def test_the_status_column_of_posts_reaches_the_publish_button_with_its_whole_path(blog) -> None:
    answer = blog.call("specir_impact", node="TableDoc:posts", field="status", limit=100)
    assert answer["changed"] == {"node": "TableDoc:posts", "field": "status", "direction": "dependents"}
    by_id = {r["export_id"]: r for r in answer["items"]}
    button = by_id["InterfaceControlDoc:publish-button"]
    assert (button["type"], button["layer"], button["title"]) == ("InterfaceControlDoc", "interface", "PublishButton")
    path = button["path"]
    assert [n.removeprefix("sldb://document/") for n in path["nodes"]] == CHAIN
    assert [e["relation"] for s in path["steps"] for e in s["edges"]] == RELATIONS
    # Every layer above the table is reached, and the policy (which the table does not feed) is not.
    assert {r["layer"] for r in answer["items"]} == {"interface", "api", "backend", "domain"}
    assert "PolicyDoc:can-publish" not in by_id and "TableDoc:posts" not in by_id
    assert [r["export_id"] for r in every(blog, "specir_impact", node="TableDoc:posts", layer="interface")] == ["InterfaceActionDoc:publish-action", "InterfaceControlDoc:publish-button"]


def test_every_hop_carries_its_provenance_and_an_inferred_one_is_flagged(blog) -> None:
    for item in blog.call("specir_impact", node="TableDoc:posts", limit=100)["items"]:
        assert item["path"]["inferred"] is False
        for step in item["path"]["steps"]:
            for e in step["edges"]:
                assert e["relation_doc"] and e["sldb_provenance"]["origin"] == "relation_doc"
                assert (e["origen"], e["verificacion"]) == ("declarado", "sin_verificar")
    archive = {"action": "create", "model": "InterfaceControlDoc", "name": "archive-button", "path": "blog/interface/archive-button.md",
               "payload": {"title": "ArchiveButton", "origen": "inferido", "kind": "button", "description": "Seen next to PublishButton."}}
    inferred = {"action": "assert_edge", "name": "archive-button-triggers-publish-action", "path": "blog/edges/archive-button-triggers-publish-action.md",
                "source": "InterfaceControlDoc:archive-button", "target": "InterfaceActionDoc:publish-action", "relation_type": "triggers",
                "attributes": {"origen": "inferido", "verificacion": "sin_verificar", "evidencia": ""}}
    assert apply(blog, [archive, inferred])["applied"] is True
    try:
        by_id = {r["export_id"]: r for r in blog.call("specir_impact", node="TableDoc:posts", limit=100)["items"]}
        assert by_id["InterfaceControlDoc:archive-button"]["path"]["inferred"] is True
        assert by_id["InterfaceControlDoc:publish-button"]["path"]["inferred"] is False
        hop = by_id["InterfaceControlDoc:archive-button"]["path"]["steps"][0]["edges"][0]
        assert hop["origen"] == "inferido" and hop["relation"] == "triggers"
    finally:
        apply(blog, [delete(inferred), delete(archive)])


def test_impact_reads_endpoints_and_policies_in_both_directions(blog) -> None:
    endpoint = every(blog, "specir_impact", node="ApiOperationDoc:publish-post-endpoint")
    assert {r["export_id"] for r in endpoint} == {"InterfaceActionDoc:publish-action", "InterfaceControlDoc:publish-button"}
    policy = every(blog, "specir_impact", node="PolicyDoc:can-publish")
    assert "InterfaceControlDoc:publish-button" in {r["export_id"] for r in policy}
    below = every(blog, "specir_impact", node="ApiOperationDoc:publish-post-endpoint", direction="dependencies")
    assert {r["export_id"] for r in below} >= {"HandlerDoc:publish-handler", "DomainOperationDoc:publish-post", "TableDoc:posts"}


def test_impact_answers_an_unknown_node_or_field_without_failing(blog) -> None:
    assert blog.call("specir_impact", node="TableDoc:nope")["signal"] == "unknown_document"
    assert blog.call("specir_impact", node="Nothing:x")["signal"] == "unknown_model"
    assert blog.call("specir_impact", node="TableDoc:posts", field="ghost")["signal"] == "unknown_field"


def banned_keys(value: Any, path: str = "") -> list[str]:
    found = []
    if isinstance(value, dict):
        for key, inner in value.items():
            if key in {"fix", "patch", "diff", "proposal", "suggestion", "changes"}:
                found.append(f"{path}.{key}")
            found += banned_keys(inner, f"{path}.{key}")
    elif isinstance(value, list):
        for i, inner in enumerate(value):
            found += banned_keys(inner, f"{path}[{i}]")
    return found


def test_rules_and_impact_write_nothing_and_propose_nothing(blog, blog_root) -> None:
    gap = named("publish-handler")
    assert apply(blog, [delete(gap)])["applied"] is True
    try:
        before = tree_digest(blog_root)
        answers = [blog.call("specir_rules", limit=200), blog.call("specir_impact", node="TableDoc:posts", field="status", limit=200),
                   blog.call("specir_impact", node="PolicyDoc:can-publish", direction="dependencies", limit=200)]
        assert answers[0]["total"] >= 1 and answers[1]["total"] >= 1
        assert tree_digest(blog_root) == before
        assert [banned_keys(a) for a in answers] == [[], [], []]
        assert not any("fix" in f for f in answers[0]["items"])
    finally:
        assert apply(blog, [gap])["applied"] is True


def test_specir_walks_no_graph_of_its_own() -> None:
    source = "\n".join(p.read_text(encoding="utf-8") for p in (REPO / "src" / "specir").rglob("*.py") if "visual" not in p.parts)
    for forbidden in ("networkx", "import heapq", "deque", "def bfs", "def dfs", "def find_path", "neighbors("):
        assert forbidden not in source, forbidden
    assert "graph_path(" in source
