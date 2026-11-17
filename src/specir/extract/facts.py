"""Reading the generic facts of `sldb.api.code.code_facts`: indexes and the small helpers the
rules share. Nothing here reads code; it reads facts."""

from __future__ import annotations

import json
from typing import Any

Fact = dict[str, Any]


def literal(text: Any) -> str | None:
    """The value of a string literal as a fact shows it (`'posts'`), else None."""
    if isinstance(text, str) and len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    return None


def literal_list(text: Any) -> list[str] | None:
    """The string items of a list literal as a fact shows it (`['post']`), else None."""
    if not isinstance(text, str):
        return None
    try:
        items = json.loads(text.replace("'", '"'))
    except ValueError:
        return None
    return items if isinstance(items, list) and all(isinstance(i, str) for i in items) else None


def last(name: str) -> str:
    return name.rsplit(".", 1)[-1]


class Facts:
    """The facts of a tree, indexed by id, by container and by owner."""

    def __init__(self, facts: list[Fact]) -> None:
        self.all = facts
        self.by_id = {f["id"]: f for f in facts}
        self.children: dict[str, list[Fact]] = {}
        for fact in facts:
            for relation in fact.get("relations", []):
                if relation["type"] == "contained-in":
                    self.children.setdefault(relation["target"], []).append(fact)

    def of_kind(self, *kinds: str) -> list[Fact]:
        return [f for f in self.all if f["kind"] in kinds]

    def members(self, fact: Fact, *kinds: str) -> list[Fact]:
        return [f for f in self.children.get(fact["id"], []) if not kinds or f["kind"] in kinds]

    def member(self, fact: Fact, name: str, *kinds: str) -> Fact | None:
        return next((f for f in self.members(fact, *kinds) if last(f["qualified_name"]) == name), None)

    def bases(self, fact: Fact) -> list[str]:
        return list(fact["attrs"].get("bases") or [])

    def classes(self, name: str) -> list[Fact]:
        return [f for f in self.of_kind("class") if f["qualified_name"] == name]

    def functions(self, module: str, name: str) -> list[Fact]:
        return [f for f in self.of_kind("function") if f["attrs"].get("module") == module and f["qualified_name"] == name]

    def owner(self, fact: Fact) -> Fact | None:
        parents = [r["target"] for r in fact.get("relations", []) if r["type"] == "contained-in"]
        return self.by_id.get(parents[0]) if parents else None
