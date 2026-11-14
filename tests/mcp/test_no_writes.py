"""Reading through the server writes nothing: not the mounted copy, not the linked deskops and
spec2viz stores, not this repo's own store."""

from __future__ import annotations

from pathlib import Path

from conftest import COPIED, REPO, federated_digest, tree_digest


def test_every_read_tool_leaves_every_store_untouched(mcp, store_copy: Path, copy_digest_before: dict[str, str], original_digest: dict[str, str]) -> None:
    called = set()
    task = mcp.call("select_documents", model="TaskDoc", limit=1)["items"][0]["export_id"]
    for tool, arguments in [
        ("list_models", {}),
        ("describe_model", {"model": "TaskDoc"}),
        ("list_relation_types", {}),
        ("describe_relation_type", {"name": "references"}),
        ("read_document", {"ref": task}),
        ("read_document", {"ref": task, "field": "status"}),
        ("select_documents", {"model": "AtomDoc", "include_linked": True}),
        ("neighbors", {"node": task, "direction": "outgoing"}),
        ("neighbors", {"node": task, "direction": "incoming"}),
        ("neighborhood", {"node": task, "direction": "both", "depth": 2}),
        ("list_views", {}),
        ("resolve_view", {"view": "spec2viz:SpecDoc:class.sldb-models"}),
        ("resolve_view", {"view": "board"}),
        ("check_integrity", {}),
    ]:
        mcp.call(tool, **arguments)
        called.add(tool)
    assert called == {tool.name for tool in mcp.list_tools()}
    after = {**tree_digest(*(store_copy / name for name in COPIED)), **federated_digest()}
    changed = sorted(path for path in set(copy_digest_before) | set(after) if copy_digest_before.get(path) != after.get(path))
    assert not changed, f"reading wrote to: {changed}"
    now = tree_digest(REPO / ".sldb", REPO / "desk")
    moved = sorted(path for path in set(original_digest) | set(now) if original_digest.get(path) != now.get(path))
    assert not moved, f"the repo's own store changed during the tests: {moved}"
