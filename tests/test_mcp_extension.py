"""specIR on the MCP server of sldb: the real `sldb mcp --extension specir.mcp_extension:register`,
reached by the real MCP client over stdio, over an isolated copy of this repo's store (with a
session copy of the deskops store linked, and a temporary specs store built from this repo's spec fixture
linked as `spec2viz`). At level 0 there is no write tool, and reading through every tool, sldb's
and specIR's, changes no file of any store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from sldb.api import extract_document_payload

from conftest import REPO, WORKSPACE, copy_digest, linked_stores, tree_digest

#: sldb's read surface (sldb.mcp.registry.READ_TOOLS) and its signal log.
SLDB_READ = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "check_integrity", "list_signals",
}
SLDB_WRITE = {"propose_changes", "apply_changes"}
#: specIR's own tools (specir.mcp_extension).
DOMAIN = {"specir_types", "specir_nodes"}
SPEC_STORE = "spec2viz"
SPEC = "class.sldb-models"


def every_page(mcp, tool: str, limit: int = 50, **arguments: Any) -> list[Any]:
    """Every item of a paged answer, following `next_offset`."""
    items: list[Any] = []
    offset: int | None = 0
    while offset is not None:
        answer = mcp.call(tool, offset=offset, limit=limit, **arguments)
        items += answer["items"]
        offset = answer["next_offset"]
    return items


def test_the_server_of_sldb_serves_its_tools_and_specirs(mcp) -> None:
    tools = {t.name: t for t in mcp.list_tools()}
    assert set(tools) == SLDB_READ | DOMAIN
    for name in DOMAIN:
        assert tools[name].description and tools[name].output_schema is not None, name
        assert tools[name].annotations.read_only_hint is True, name


def test_at_level_0_no_write_tool_exists(mcp) -> None:
    assert not SLDB_WRITE & {t.name for t in mcp.list_tools()}
    answer = mcp.portal.call(lambda: mcp.client.call_tool("propose_changes", {"changes": []}))
    assert answer.is_error is False and answer.structured_content["signal"] == "unknown_tool", answer


def test_specir_types_over_a_store_without_them(mcp) -> None:
    from specir.models import DOMAIN_MODELS

    answer = mcp.call("specir_types")
    assert [r["type"] for r in answer["items"]] == [m.__name__ for m in DOMAIN_MODELS]
    assert not any(r["registered"] for r in answer["items"]) and "specir.install" in answer["explanation"]
    nodes = mcp.call("specir_nodes")
    assert nodes["total"] == 0 and nodes["explanation"]


def test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server(mcp, spec_store: Path) -> None:
    store = spec_store
    indexed = store / "core" / "documents" / "SpecDoc" / f"{SPEC}.yaml"
    assert indexed.is_file(), f"the {SPEC_STORE} store has no SpecDoc {SPEC}: {indexed}"
    export_id = f"{SPEC_STORE}:SpecDoc:{SPEC}"
    assert export_id in {v["view"] for v in every_page(mcp, "list_views") if v["kind"] == "spec"}
    entry = yaml.safe_load(indexed.read_text(encoding="utf-8").split("\n---", 1)[0])
    document = mcp.call("read_document", ref=export_id)
    assert document["found"] and document["store"] == SPEC_STORE and document["address"] == f"sldb://document/{export_id}"
    assert document["path"] == entry["path"] and document["version"] == entry["content_hash"]
    assert (store.parent / entry["path"]).is_file()
    #: The payload sldb extracts from the temporary store itself (the document's front matter also
    #: carries sldb's provenance block `sldb:`, which is not a field of the payload).
    expected = extract_document_payload(store, None, SPEC)
    assert expected["id"] == SPEC
    for key, value in expected.items():
        assert document["payload"][key] == value, key


def test_the_deskops_store_linked_is_the_session_copy(store_copy: Path, federated: dict[str, Path]) -> None:
    linked = linked_stores(store_copy)
    assert linked["deskops"] == federated["deskops"].resolve()
    assert not linked["deskops"].is_relative_to(WORKSPACE.resolve()), linked["deskops"]


def test_no_store_linked_from_the_mounted_copy_leads_out_of_the_session_temp(store_copy: Path, tmp_path_factory) -> None:
    """Every store reachable through the store_index links (transitively) is a session copy,
    so the server never reaches a real store of the workspace through federation."""
    temp = tmp_path_factory.getbasetemp().resolve()
    seen: dict[Path, str] = {}
    pending = [store_copy.resolve()]
    while pending:
        project = pending.pop()
        for name, store in linked_stores(project).items():
            assert store.is_relative_to(temp) and not store.is_relative_to(WORKSPACE.resolve()), f"{project}: {name} -> {store}"
            assert (store / "core").is_dir(), f"{project}: {name} -> {store} does not resolve"
            if store not in seen:
                seen[store] = name
                pending.append(store.parent)
    assert "deskops" in seen.values()


def test_reading_through_every_tool_leaves_every_store_untouched(mcp, store_copy: Path, spec_store: Path, federated: dict[str, Path], copy_digest_before: dict[str, str], original_digest: dict[str, str]) -> None:
    task = mcp.call("select_documents", model="TaskDoc", limit=1)["items"][0]["export_id"]
    calls = [
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
        ("resolve_view", {"view": f"{SPEC_STORE}:SpecDoc:{SPEC}"}),
        ("resolve_view", {"view": "board"}),
        ("check_integrity", {}),
        ("list_signals", {}),
        ("specir_types", {}),
        ("specir_nodes", {"layer": "api"}),
    ]
    for tool, arguments in calls:
        mcp.call(tool, **arguments)
    assert {tool for tool, _ in calls} == {t.name for t in mcp.list_tools()}
    after = copy_digest(store_copy, spec_store, federated)
    changed = sorted(path for path in set(copy_digest_before) | set(after) if copy_digest_before.get(path) != after.get(path))
    assert not changed, f"reading wrote to: {changed}"
    now = tree_digest(REPO / ".sldb", REPO / "desk")
    moved = sorted(path for path in set(original_digest) | set(now) if original_digest.get(path) != now.get(path))
    assert not moved, f"the repo's own store changed during the tests: {moved}"
