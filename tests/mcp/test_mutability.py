"""The write level is the server's: a call above it fails before anything is evaluated; the
write tools take typed arguments only; no tool writes a Python module."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import copy_digest
from writing import an_atom

READ_TOOLS = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "check_integrity",
}
WRITE_TOOLS = {"propose_changes", "apply_changes"}
#: A change on a rule document that names nothing the store has: evaluating it at all would
#: answer "not registered" or "not a document", not the level.
RULE_CHANGES = [
    {"action": "update", "model": "RuleDoc", "name": "no-such-rule-ir04", "fields": {"severity": "error"}},
    {"action": "create", "model": "RelationTypeDoc", "name": "no-such-type-ir04", "payload": {}},
]


def test_level_0_serves_no_write_tool(mcp) -> None:
    assert {t.name for t in mcp.list_tools()} == READ_TOOLS
    assert "propose_changes" in mcp.error_of("propose_changes", changes=RULE_CHANGES[:1])


def test_level_1_refuses_rules_before_evaluating_anything(content_writer, write_copy: Path) -> None:
    assert {t.name for t in content_writer.list_tools()} == READ_TOOLS | WRITE_TOOLS
    before = copy_digest(write_copy)
    for change in RULE_CHANGES:
        error = content_writer.error_of("propose_changes", changes=[change])
        assert "LevelError" in error and "write level 2" in error and "level 1" in error, error
        assert "register" not in error and "not a document" not in error, error
    assert copy_digest(write_copy) == before


def test_level_1_refuses_to_apply_a_rules_proposal(writer, content_writer) -> None:
    atom = an_atom(writer)
    proposal = writer.call("propose_changes", changes=[
        {"action": "create", "model": "RuleDoc", "name": "rule-ir04-level", "payload": {"title": "x", "subject": f"model <= {atom['model']}", "condition": "true", "severity": "alert", "moment": "on_write", "message": ""}, "path": "desk/lifecycle/rule-ir04-level.md"},
    ])["proposal"]
    assert proposal["level"] == 2
    error = content_writer.error_of("apply_changes", proposal=proposal)
    assert "LevelError" in error and "write level 2" in error, error


def test_level_1_writes_content(content_writer) -> None:
    atom = an_atom(content_writer)
    answer = content_writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": atom["payload"]["title"]}}])
    assert answer["proposal"]["level"] == 1


def test_models_as_code_are_never_served(write_copy: Path) -> None:
    done = subprocess.run([sys.executable, "-m", "specir.mcp.server", "--store", str(write_copy / ".sldb"), "--level", "3"], capture_output=True, text=True, timeout=120)
    assert done.returncode == 2 and "--level" in done.stderr, done.stderr


def test_no_tool_writes_a_python_module(writer, write_copy: Path) -> None:
    assert {t.name for t in writer.list_tools()} == READ_TOOLS | WRITE_TOOLS
    atom = an_atom(writer)
    error = writer.error_of("propose_changes", changes=[{"action": "create", "model": atom["model"], "name": "atom-ir04-module", "payload": atom["payload"], "path": "src/specir/ir04_module.py"}])
    assert "not a Markdown document" in error
    assert not (write_copy / "src").exists()


def test_write_tools_take_typed_arguments_only(writer) -> None:
    schema = next(t for t in writer.list_tools() if t.name == "propose_changes").input_schema
    variants = schema["$defs"]
    actions = set()
    for name in ("CreateDocument", "UpdateDocument", "DeleteDocument", "AssertEdge", "RetractEdge"):
        assert variants[name]["additionalProperties"] is False, name
        actions.add(variants[name]["properties"]["action"]["const"])
    assert actions == {"create", "update", "delete", "assert_edge", "retract_edge"}
    atom = an_atom(writer)
    for change in (
        {"action": "make the atom say something nicer", "model": atom["model"], "name": atom["name"]},
        {"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "x"}, "instructions": "and fix its tags"},
        "update the atom's title",
    ):
        assert "validation error" in writer.error_of("propose_changes", changes=[change]).lower(), change
