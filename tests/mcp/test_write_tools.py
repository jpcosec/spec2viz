"""Propose and apply, called by the real MCP client on the real server at write level 2 over
its own copy of this repo's store. Payloads start from documents the repo tracks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from conftest import REPO, WRITER
from writing import a_valid_edge, an_atom, front_matter, page_items, relation_type_file, tracked

EDGE_PENDING = "edge_validation_before_write"


def apply(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Propose `changes` and apply the proposal exactly as it came back."""
    return session.call("apply_changes", proposal=session.call("propose_changes", changes=changes)["proposal"])


def applied(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    answer = apply(session, changes)
    assert answer["applied"] is True, answer
    return answer


def signed_by_the_writer(answer: dict[str, Any], write_copy: Path, via: str) -> None:
    """Every document written carries who wrote it and through which operation, in the answer and on disk."""
    for document in answer["documents"]:
        assert document["provenance"]["by"] == WRITER and document["provenance"]["via"] == via, document
        on_disk = front_matter(write_copy / document["path"])["sldb"]
        assert on_disk["by"] == WRITER and on_disk["via"] == via, (document["path"], on_disk)


def test_cycle_on_a_document(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    name = "atom-ir04-cycle"
    payload = {**atom["payload"], "id": name, "title": "IR04: el ciclo proponer, validar y aplicar"}
    created = applied(writer, [{"action": "create", "model": atom["model"], "name": name, "payload": payload, "path": f"desk/atoms/{name}.md"}])
    export_id = f"{atom['model']}:{name}"
    assert [d["export_id"] for d in created["documents"]] == [export_id]
    signed_by_the_writer(created, write_copy, "create_document")
    read = writer.call("read_document", ref=export_id)
    assert read["found"] and read["payload"] == payload

    updated = applied(writer, [{"action": "update", "model": atom["model"], "name": name, "fields": {"title": payload["title"] + " (editado)"}}])
    signed_by_the_writer(updated, write_copy, "save_document_payload")
    assert writer.call("read_document", ref=export_id, field="title")["value"] == payload["title"] + " (editado)"

    deleted = applied(writer, [{"action": "delete", "model": atom["model"], "name": name}])
    assert deleted["deleted"] == [read["address"]] and deleted["documents"] == []
    assert writer.call("read_document", ref=export_id)["found"] is False
    assert not (write_copy / read["path"]).exists()


def test_cycle_on_an_edge(writer, write_copy: Path) -> None:
    edge = a_valid_edge("ir04-cycle-edge")
    source, target = (writer.call("read_document", ref=edge[end])["address"] for end in ("source", "target"))

    def targets() -> set[str]:
        return {e["target"] for e in page_items(writer, "neighbors", node=edge["source"], direction="outgoing", relation=edge["relation_type"])}

    assert target not in targets(), "the edge exists already; it would prove nothing"
    asserted = applied(writer, [edge])
    assert asserted["edge_findings"] == [], asserted["edge_findings"]
    signed_by_the_writer(asserted, write_copy, "create_document")
    assert target in targets()
    stored = writer.call("read_document", ref="RelationDoc:ir04-cycle-edge")["payload"]
    assert (stored["source_id"], stored["target_id"], stored["relation_type"]) == (edge["source"], edge["target"], edge["relation_type"])

    applied(writer, [{"action": "retract_edge", "name": "ir04-cycle-edge"}])
    assert target not in targets() and source
    assert not (write_copy / edge["path"]).exists()


def test_a_change_to_a_store_that_moved_since_the_proposal_is_rejected(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    first = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: primera propuesta"}}])
    second = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: segunda propuesta"}}])
    assert writer.call("apply_changes", proposal=second["proposal"])["applied"] is True
    stale = writer.call("apply_changes", proposal=first["proposal"])
    assert stale["applied"] is False and stale["rejected"] == "stale" and stale["document"] == atom["name"]
    assert "changed" in stale["explanation"]
    assert front_matter(write_copy / atom["path"])["title"] == "IR04: segunda propuesta"


def test_an_edited_proposal_is_refused(writer) -> None:
    atom = an_atom(writer)
    proposal = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: sellada"}}])["proposal"]
    proposal["changes"][0]["expected_source_hash"] = None
    assert "propose it again" in writer.error_of("apply_changes", proposal=proposal)


def a_rule(writer, name: str, **fields: Any) -> dict[str, Any]:
    """A RuleDoc change: the repo's first RuleDoc, under a new name with `fields`."""
    rule = tracked(writer, sorted((REPO / "desk" / "lifecycle").glob("rule-*.md"))[0])
    return {"action": "create", "model": "RuleDoc", "name": name, "payload": {**rule["payload"], **fields}, "path": f"desk/lifecycle/{name}.md"}


def test_an_error_rule_refuses_the_change_and_is_named(writer, write_copy: Path) -> None:
    rule = a_rule(writer, "rule-ir04-edges-explain-themselves", title="IR04: an authored edge explains itself", subject="model <= RelationDoc", where="", condition="nonempty(notes)", severity="error", moment="on_write", message="An authored edge explains itself in its notes.")
    applied(writer, [rule])
    try:
        silent = {**a_valid_edge("ir04-edge-without-notes"), "notes": ""}
        refused = apply(writer, [silent])
        assert refused["applied"] is False and refused["rejected"] == "rules"
        assert refused["rules"] == [f"rules/{rule['name']}"] and rule["name"] in refused["explanation"]
        assert refused["findings"][0]["level"] == "error" and refused["findings"][0]["subject"] == "RelationDoc:ir04-edge-without-notes"
        assert not (write_copy / silent["path"]).exists()
    finally:
        applied(writer, [{"action": "delete", "model": "RuleDoc", "name": rule["name"]}])


def test_an_alert_rule_is_reported_by_name(writer) -> None:
    rules = [p for p in (REPO / "desk" / "lifecycle").glob("rule-*.md") if front_matter(p).get("moment") == "on_write" and front_matter(p).get("severity") == "alert" and "pills" in front_matter(p)["condition"]]
    assert rules, "the repo declares no on_write alert about pills"
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("pills")))
    answer = applied(writer, [{"action": "update", "model": task["model"], "name": task["name"], "fields": {"references": []}}])
    codes = {a["code"] for a in answer["alerts"] if a["subject"] == task["export_id"]}
    assert {f"rules/{tracked(writer, p)['name']}" for p in rules} <= codes, answer["alerts"]


def test_an_edge_against_its_relation_type_is_reported(writer) -> None:
    edge = a_valid_edge("ir04-edge-wrong-source")
    allowed = front_matter(relation_type_file(edge["relation_type"]))["source_types"]
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("task_type")))
    assert task["model"] not in allowed
    wrong = {**edge, "source": task["export_id"]}
    proposal = writer.call("propose_changes", changes=[wrong])
    assert any(p["note"].startswith("sldb:") for p in proposal["pending"] if EDGE_PENDING in p["what"] or "RelationTypeDoc" in p["what"])
    answer = writer.call("apply_changes", proposal=proposal["proposal"])
    try:
        assert answer["applied"] is True
        assert any("source_types" in f and task["export_id"] in f for f in answer["edge_findings"]), answer["edge_findings"]
    finally:
        applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])


def test_cardinality_and_condition_of_a_declared_type_are_reported(writer) -> None:
    base = tracked(writer, relation_type_file(a_valid_edge("x")["relation_type"]))
    name = "ir04_one_to_one"
    declared = {"action": "create", "model": "RelationTypeDoc", "name": f"type-{name}", "path": f"desk/lifecycle/type-{name}.md", "payload": {**base["payload"], "name": name, "title": "IR04 one to one", "cardinality": "one_to_one", "target_types": []}}
    applied(writer, [declared])
    first, second = a_valid_edge("ir04-card-1"), a_valid_edge("ir04-card-2")
    # Two targets for one source under a one_to_one type, the second with a condition that does not parse.
    edges = [{**first, "relation_type": name}, {**second, "relation_type": name, "target": first["source"], "condition": "status = "}]
    try:
        findings = applied(writer, edges)["edge_findings"]
        assert any(f"has 2 '{name}' targets but cardinality is one_to_one" in f for f in findings), findings
        assert any("condition does not parse" in f for f in findings), findings
    finally:
        applied(writer, [{"action": "retract_edge", "name": e["name"]} for e in edges] + [{"action": "delete", "model": "RelationTypeDoc", "name": f"type-{name}"}])


@pytest.mark.xfail(strict=True, reason="SLDB checks an edge against its RelationTypeDoc only after the write (check_edges); asked by note, see PENDING['edge_validation_before_write']")
def test_an_edge_against_its_relation_type_is_refused_before_writing(writer, write_copy: Path) -> None:
    edge = a_valid_edge("ir04-edge-refused")
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("task_type")))
    wrong = {**edge, "source": task["export_id"]}
    answer = apply(writer, [wrong])
    try:
        assert answer["applied"] is False and not (write_copy / wrong["path"]).exists()
    finally:
        if answer["applied"]:
            applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])
