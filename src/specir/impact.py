"""Domain impact analysis (IR10): which nodes of the other layers a change to one node reaches, and why.

Nothing here walks the graph: the chains are sldb's explained paths (`sldb.api.graph.graph_path`,
B3), asked once per candidate node over specIR's relation types. specIR adds only the domain
mapping: which nodes count as affected (every specIR node that depends on the changed one, or
that it depends on), what they are called (their type, layer and title), and the provenance of
each hop (`origen`, `verificacion` of the relation's `RelationDoc`, which is specIR's data), with
a path that crosses an `inferido` relation flagged as such.

Read-only, and it proposes no change: the answer says what is affected and the chain that
justifies it, never what to edit."""

from __future__ import annotations

from importlib import resources
from typing import Any, Literal

import sldb.api as api
from sldb.api.graph import graph_path
import yaml

from specir.models.domain import DOMAIN_MODELS, PROVENANCE_FIELDS, SpecIRNodeDoc

ADDRESS = "sldb://document/"
Direction = Literal["dependents", "dependencies"]


def relation_names() -> list[str]:
    """The relation types specIR distributes (`data/relation_types.yaml`): the only edges followed."""
    text = resources.files("specir").joinpath("data", "relation_types.yaml").read_text(encoding="utf-8")
    return [spec["name"] for spec in yaml.safe_load(text)]


def layer_of(model: type[SpecIRNodeDoc]) -> str:
    return model.__semantics__["layer"][0]


def export_id(node: str) -> str:
    """`Model:name` of a node given as `Model:name` or `sldb://document/Model:name`."""
    return node.removeprefix(ADDRESS)


def _edge(store_path: Any, edge: dict[str, Any]) -> dict[str, Any]:
    """One edge of an explained step with the provenance specIR keeps on its RelationDoc."""
    out = {"relation": edge["relation"], "direction": edge["direction"], "sldb_provenance": edge.get("provenance")}
    name = (edge.get("provenance") or {}).get("relation_doc")
    attributes: dict[str, Any] = {}
    if name:
        try:
            payload = api.serialize_document(api.runtime_document(store_path, None, f"RelationDoc/{name}"))["payload"]
            attributes = payload.get("attributes") or {}
        except Exception:  # an edge whose document cannot be read keeps sldb's provenance only
            attributes = {}
    out["relation_doc"] = name
    out.update({field: attributes.get(field) for field in PROVENANCE_FIELDS})
    return out


def _explained(store_path: Any, found: dict[str, Any]) -> dict[str, Any]:
    steps = [{"source": s["source"], "target": s["target"], "edges": [_edge(store_path, e) for e in s["edges"]]} for s in found["steps"]]
    inferred = any(e.get("origen") == "inferido" for s in steps for e in s["edges"])
    return {"nodes": found["path"], "steps": steps, "inferred": inferred}


def affected(store_path: Any, node: str, direction: Direction = "dependents", kinds: list[str] | None = None) -> list[dict[str, Any]]:
    """The specIR nodes affected by a change to `node`, each with the shortest explained path.

    `dependents`: nodes with a chain of relations leading to `node` (the interface above a table);
    `dependencies`: nodes `node` leads to. Ordered by layer of the domain types, then export id."""
    target = f"{ADDRESS}{export_id(node)}"
    relations = relation_names()
    rows = []
    for model in DOMAIN_MODELS:
        if kinds is not None and model.__name__ not in kinds or not api.is_model_registered(store_path, model.__name__):
            continue
        for row in api.select_documents(store_path, {"model": model.__name__}):
            candidate = f"{ADDRESS}{row['export_id']}"
            if candidate == target:
                continue
            source, goal = (candidate, target) if direction == "dependents" else (target, candidate)
            found = graph_path(store_path, source, goal, relations=relations, directed=True, explain=True)
            if not found:
                continue
            payload = api.serialize_document(api.runtime_document(store_path, None, f"{row['model']}/{row['name']}"))["payload"]
            rows.append({"export_id": row["export_id"], "address": candidate, "type": row["model"], "layer": layer_of(model), "title": payload.get("title"), "path": _explained(store_path, found)})
    return rows
