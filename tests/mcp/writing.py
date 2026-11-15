"""What the write tests share: real documents of this repo to change, read through the tools.

Every payload starts from a document the repo tracks (an atom, a RelationDoc of its lifecycle,
a RelationTypeDoc), read with `read_document`; a test changes only what it is about."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from conftest import REPO


def front_matter(path: Path) -> dict[str, Any]:
    """The YAML front matter of a Markdown document."""
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no front matter"
    return yaml.safe_load(text.split("\n---", 1)[0][4:]) or {}


def tracked(session, path: Path) -> dict[str, Any]:
    """The document the store tracks at `path` (a file of this repo), read in full."""
    rows = session.call("select_documents", path_glob=str(path.relative_to(REPO)))["items"]
    assert len(rows) == 1, f"{path}: {rows}"
    return session.call("read_document", ref=rows[0]["export_id"])


def an_atom(session) -> dict[str, Any]:
    """The first atom of the repo, read."""
    return tracked(session, sorted((REPO / "desk" / "atoms").glob("atom-*.md"))[0])


def lifecycle_edges() -> list[Path]:
    """The repo's authored edges (RelationDocs of desk/lifecycle/), the ones with a source type."""
    return sorted(p for p in (REPO / "desk" / "lifecycle").glob("*.md") if {"source_id", "target_id", "relation_type"} <= set(front_matter(p)))


def relation_type_file(name: str) -> Path:
    """The RelationTypeDoc of the repo named `name`."""
    return next(p for p in (REPO / "desk" / "lifecycle").glob("type-*.md") if front_matter(p)["name"] == name)


def a_valid_edge(name: str) -> dict[str, Any]:
    """A new edge the repo's own lifecycle types allow: the first RelationDoc's source and
    relation type, towards the target of another RelationDoc (a target the type admits)."""
    first, *others = [front_matter(p) for p in lifecycle_edges()]
    declared = front_matter(relation_type_file(first["relation_type"]))
    assert declared["cardinality"] == "many_to_many", declared
    target = next(o["target_id"] for o in others if o["target_id"] != first["target_id"])
    assert not declared.get("target_types") or target.split(":")[0] in declared["target_types"], (target, declared)
    return {"action": "assert_edge", "name": name, "source": first["source_id"], "target": target, "relation_type": first["relation_type"], "notes": "Asserted by the IR04 tests.", "path": f"desk/lifecycle/{name}.md"}


def page_items(session, tool: str, **arguments: Any) -> list[Any]:
    """Every item of a paged answer."""
    items: list[Any] = []
    offset: int | None = 0
    while offset is not None:
        answer = session.call(tool, offset=offset, limit=500, **arguments)
        items += answer["items"]
        offset = answer["next_offset"]
    return items
