"""The read tools, called by the real MCP client on the real server over the isolated copy of
this repo's store. Expected values come from the repo's own files (front matter of desk/
documents, the spec2viz store's files), never from literals that restate the answer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from conftest import FEDERATED, REPO

TOOLS = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "check_integrity",
}
SPEC_STORE = "spec2viz"
SPEC = "class.sldb-models"


def front_matter(path: Path) -> dict[str, Any]:
    """The YAML front matter of a Markdown document."""
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no front matter"
    return yaml.safe_load(text.split("\n---", 1)[0][4:]) or {}


def every_page(mcp, tool: str, limit: int = 50, **arguments: Any) -> list[Any]:
    """Every item of a paged answer, following `next_offset`."""
    items: list[Any] = []
    offset: int | None = 0
    while offset is not None:
        answer = mcp.call(tool, offset=offset, limit=limit, **arguments)
        items += answer["items"]
        offset = answer["next_offset"]
    return items


def one_document(mcp, path: str) -> dict[str, Any]:
    """The selected row of the document tracked at `path` (relative to the project root)."""
    rows = mcp.call("select_documents", path_glob=path)["items"]
    assert len(rows) == 1, f"{path}: {rows}"
    return rows[0]


def routed_task() -> Path:
    """The first code task routed on the board that binds pills (a closed task leaves desk/tasks/)."""
    return next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("pills") and front_matter(p).get("task_type") == "task.code")


@pytest.fixture(scope="module")
def task(mcp) -> dict[str, Any]:
    """A routed TaskDoc, as the store selects it from its path."""
    return one_document(mcp, str(routed_task().relative_to(REPO)))


def test_tools_are_the_read_surface_and_read_only(mcp) -> None:
    tools = {tool.name: tool for tool in mcp.list_tools()}
    assert set(tools) == TOOLS
    for tool in tools.values():
        assert tool.annotations.read_only_hint is True and tool.annotations.destructive_hint is False, tool.name
        assert tool.output_schema is not None, f"{tool.name} returns no structured JSON"


def test_list_models_is_the_store_registry(mcp, store_copy: Path) -> None:
    index = yaml.safe_load((store_copy / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    models = every_page(mcp, "list_models", limit=7)
    assert {m["name"] for m in index["models"]} <= {m["name"] for m in models}
    assert all(m["address"] == f"sldb://model/{m['name']}" for m in models)
    described = mcp.call("describe_model", model="TaskCodeDoc")
    assert described["found"] and described["address"] == "sldb://model/TaskCodeDoc"
    fields = {f["name"]: f["annotation"] for f in described["fields"]}
    task_file = front_matter(routed_task())
    assert {"id", "status", "pills", "files"} <= set(fields) and set(task_file) - {"sldb"} <= set(fields) | {"task_type"}


@pytest.mark.parametrize("model", ["TaskDoc", "AtomDoc", "PillDoc", "RitualDoc"])
def test_documents_are_the_repo_documents(mcp, model: str) -> None:
    rows = every_page(mcp, "select_documents", model=model)
    assert rows, f"no {model} selected"
    for row in rows:
        assert row["address"] == f"sldb://document/{row['export_id']}"
        original = REPO / row["path"]
        assert original.is_file(), f"{row['export_id']} is not a file of the repo: {row['path']}"
        document = mcp.call("read_document", ref=row["export_id"])
        assert document["found"] and document["address"] == row["address"]
        assert document["name"] == row["name"] and document["path"] == row["path"]
        written = front_matter(original)
        if "id" in written:
            assert written["id"] == document["payload"]["id"] == document["name"]
        shared = (set(written) & set(document["payload"])) - {"sldb"}
        assert shared, f"{row['export_id']}: no field in common with {row['path']}"
        for key in shared:
            assert document["payload"][key] == written[key], f"{row['export_id']}.{key}"


def test_read_one_field(mcp, task: dict[str, Any]) -> None:
    written = front_matter(REPO / task["path"])
    answer = mcp.call("read_document", ref=task["export_id"], field="pills")
    assert answer["found"] and answer["value"] == written["pills"]
    assert answer["address"] == task["address"]


def test_largest_model_comes_paged(mcp) -> None:
    totals = {m["name"]: mcp.call("select_documents", model=m["name"], limit=1)["total"] for m in every_page(mcp, "list_models")}
    largest = max(totals, key=totals.get)
    total = totals[largest]
    assert total > 50, f"the largest model {largest} has only {total} documents"
    seen: list[str] = []
    offset: int | None = 0
    while offset is not None:
        answer = mcp.call("select_documents", model=largest, offset=offset, limit=50)
        assert answer["total"] == total and len(answer["items"]) <= 50
        assert answer["truncated"] == (offset + 50 < total)
        seen += [row["export_id"] for row in answer["items"]]
        assert all((REPO / row["path"]).is_file() for row in answer["items"])
        offset = answer["next_offset"]
    assert len(seen) == len(set(seen)) == total
    first = mcp.call("select_documents", model=largest, limit=1)
    assert first["truncated"] and first["next_offset"] == 1 and len(first["items"]) == 1


def test_select_by_predicate(mcp) -> None:
    active = every_page(mcp, "select_documents", model="TaskDoc", where='status = "active"')
    written = [p for p in (REPO / "desk" / "tasks").glob("task-*.md") if front_matter(p).get("status") == "active"]
    assert {row["path"] for row in active} == {str(p.relative_to(REPO)) for p in written}
    assert "predicate" in mcp.error_of("select_documents", model="TaskDoc", where="status = ")


def test_neighbors_by_relation(mcp, task: dict[str, Any]) -> None:
    written = front_matter(REPO / task["path"])
    edges = every_page(mcp, "neighbors", node=task["export_id"], direction="outgoing", relation="references")
    assert edges and all(e["relation"] == "references" and e["source"] == task["address"] for e in edges)
    pills = {one_document(mcp, path)["address"] for path in written["pills"]}
    assert pills <= {e["target"] for e in edges if e["metadata"].get("field") == "pills"}
    board = one_document(mcp, "desk/tasks/Board.md")
    incoming = every_page(mcp, "neighbors", node=task["export_id"], direction="incoming", relation="contains")
    assert board["address"] in {e["source"] for e in incoming}
    assert all(e["target"] == task["address"] for e in incoming)


def test_neighborhood_by_direction(mcp, task: dict[str, Any]) -> None:
    targets = {e["target"] for e in every_page(mcp, "neighbors", node=task["export_id"], direction="outgoing")}
    one_hop = set(every_page(mcp, "neighborhood", node=task["export_id"], direction="outgoing", depth=1))
    two_hops = set(every_page(mcp, "neighborhood", node=task["export_id"], direction="outgoing", depth=2, limit=500))
    assert one_hop == targets - {task["address"]}
    assert one_hop < two_hops
    sources = {e["source"] for e in every_page(mcp, "neighbors", node=task["export_id"], direction="incoming")}
    assert set(every_page(mcp, "neighborhood", node=task["export_id"], direction="incoming", depth=1)) == sources - {task["address"]}
    assert "direction" in mcp.error_of("neighborhood", node=task["export_id"], direction="sideways")


def test_relation_types(mcp) -> None:
    types = every_page(mcp, "list_relation_types", limit=5)
    names = {t["name"] for t in types}
    assert all(t["address"] == f"sldb://relation_type/{t['name']}" for t in types)
    lifecycle = {front_matter(p)["name"] for p in (REPO / "desk" / "lifecycle").glob("type-*.md")}
    assert lifecycle and lifecycle <= names
    for name in lifecycle:
        described = mcp.call("describe_relation_type", name=name)
        written = front_matter(next(p for p in (REPO / "desk" / "lifecycle").glob("type-*.md") if front_matter(p)["name"] == name))
        assert described["found"] and described["direction"] == written["direction"]


def test_undeclared_answers_empty_with_explanation(mcp, task: dict[str, Any]) -> None:
    for tool, arguments in [
        ("select_documents", {"model": "NoSuchModelDoc"}),
        ("select_documents", {"model": "TaskDoc", "where": 'status = "no-such-status"'}),
        ("neighbors", {"node": task["export_id"], "relation": "no_such_relation"}),
        ("neighbors", {"node": "TaskCodeDoc:no-such-task"}),
        ("neighborhood", {"node": "TaskCodeDoc:no-such-task", "direction": "both"}),
    ]:
        answer = mcp.call(tool, **arguments)
        assert answer["items"] == [] and answer["total"] == 0 and not answer["truncated"], (tool, arguments)
        assert answer["explanation"], (tool, arguments)
    for tool, arguments in [
        ("read_document", {"ref": "TaskCodeDoc:no-such-task"}),
        ("read_document", {"ref": task["export_id"], "field": "no_such_field"}),
        ("describe_model", {"model": "NoSuchModelDoc"}),
        ("describe_relation_type", {"name": "no_such_relation"}),
        ("resolve_view", {"view": "no-such-view"}),
        ("resolve_view", {"view": task["export_id"]}),
    ]:
        answer = mcp.call(tool, **arguments)
        assert answer["found"] is False and answer["explanation"], (tool, arguments)


def test_spec_view_from_the_spec2viz_federation(mcp) -> None:
    store = FEDERATED[SPEC_STORE]
    indexed = store / "core" / "documents" / "SpecDoc" / f"{SPEC}.yaml"
    assert store.is_dir(), f"the {SPEC_STORE} store is missing: {store}"
    assert indexed.is_file(), f"the {SPEC_STORE} store has no SpecDoc {SPEC}: {indexed}"
    export_id = f"{SPEC_STORE}:SpecDoc:{SPEC}"
    listed = every_page(mcp, "list_views")
    assert export_id in {v["view"] for v in listed if v["kind"] == "spec"}, f"SpecDoc {SPEC} does not resolve from the federation of the copy ({SPEC_STORE} store)"
    entry = yaml.safe_load(indexed.read_text(encoding="utf-8").split("\n---", 1)[0])
    written = front_matter(store.parent / entry["path"])
    document = mcp.call("read_document", ref=export_id)
    assert document["found"], f"SpecDoc {SPEC} does not resolve from the {SPEC_STORE} store: {document}"
    assert document["address"] == f"sldb://document/{export_id}" and document["store"] == SPEC_STORE
    assert document["path"] == entry["path"] and document["version"] == entry["content_hash"]
    for key, value in written.items():
        assert document["payload"][key] == value, key
    view = mcp.call("resolve_view", view=export_id)
    assert view["found"] and view["kind"] == "spec" and view["address"] == document["address"]
    resolved = view["result"]
    assert resolved["spec"] == f"SpecDoc:{SPEC}" and resolved["diagram_type"] == written["diagram_type"]
    assert resolved["notation"] == written["notation"] and resolved["title"] == document["payload"]["title"]
    assert [node["doc"] for node in resolved["nodes"]] == written["nodes"]


def test_composed_view(mcp) -> None:
    composed = [v for v in every_page(mcp, "list_views") if v["kind"] == "composed"]
    board = next(v for v in composed if v["view"] == "board")
    answer = mcp.call("resolve_view", view=board["view"])
    assert answer["found"] and answer["kind"] == "composed"
    sections = answer["result"]["sections"]
    assert set(sections) == set(board["sections"])
    rows = sections["board"]["rows"]
    written = front_matter(REPO / rows[0]["path"])
    assert rows[0]["fields"]["tasks"] == written["tasks"]


def test_check_integrity(mcp) -> None:
    answer = mcp.call("check_integrity", limit=10)
    assert answer["ok"] is True and answer["store"]["errors"] == 0 and answer["edges"]["errors"] == 0
    assert answer["store"]["checked"] > 0
    findings = answer["findings"]
    assert findings["total"] == answer["store"]["errors"] + answer["store"]["alerts"] + answer["edges"]["errors"]
    assert len(findings["items"]) == min(10, findings["total"]) and findings["truncated"] == (findings["total"] > 10)
