"""The dry run: `propose_changes` answers what would be written and changes no file."""

from __future__ import annotations

from pathlib import Path

from conftest import copy_digest
from writing import a_valid_edge, an_atom, lifecycle_edges, tracked


def test_a_dry_run_answers_what_would_be_written_and_writes_nothing(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    created = {**atom["payload"], "id": "atom-ir04-dry-run", "title": "IR04 dry run"}
    retracted = tracked(writer, lifecycle_edges()[-1])
    changes = [
        {"action": "create", "model": atom["model"], "name": "atom-ir04-dry-run", "payload": created, "path": "desk/atoms/atom-ir04-dry-run.md"},
        {"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": atom["payload"]["title"] + " (IR04)"}},
        a_valid_edge("ir04-dry-run-edge"),
        {"action": "retract_edge", "name": retracted["name"]},
    ]
    before = copy_digest(write_copy)
    answer = writer.call("propose_changes", changes=changes)
    assert copy_digest(write_copy) == before, "the dry run changed a file"
    assert answer["dry_run"] is True and answer["written"] is False

    would = {w["export_id"]: w for w in answer["would_write"]}
    assert set(would) == {f"{atom['model']}:atom-ir04-dry-run", atom["export_id"], "RelationDoc:ir04-dry-run-edge", retracted["export_id"]}
    assert would[f"{atom['model']}:atom-ir04-dry-run"]["payload"] == created
    update = would[atom["export_id"]]
    assert update["action"] == "update" and update["changed_fields"] == ["title"] and update["path"] == atom["path"]
    assert update["payload"] == {**atom["payload"], "title": atom["payload"]["title"] + " (IR04)"}
    edge = would["RelationDoc:ir04-dry-run-edge"]["payload"]
    asserted = a_valid_edge("ir04-dry-run-edge")
    assert (edge["source_id"], edge["target_id"], edge["relation_type"]) == (asserted["source"], asserted["target"], asserted["relation_type"])
    assert would[retracted["export_id"]]["action"] == "delete" and would[retracted["export_id"]]["path"] == retracted["path"]

    batch = {c["id"]: c for c in answer["proposal"]["changes"]}
    for name in (atom["name"], retracted["name"]):
        assert batch[name]["expected_source_hash"], f"the server filled no guard for {name}"
    assert not (write_copy / "desk/atoms/atom-ir04-dry-run.md").exists()
    assert not (write_copy / "desk/lifecycle/ir04-dry-run-edge.md").exists()
    assert (write_copy / retracted["path"]).is_file()
    assert any(p["note"].startswith("sldb:") and "dry run" in p["what"] for p in answer["pending"]), "the missing SLDB dry run is not declared"
