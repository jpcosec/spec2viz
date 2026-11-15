"""Projections of the graph to the intermediate representation (IR11).

A diagram of what already exists in the graph is a projection, not a second copy of its entities.
Everything that reads the store is SLDB's public API:

- a projection `ViewDoc` (nodes and relations, no sections) is evaluated by
  `sldb.api.notations.evaluate_projection_view`;
- a composed `ViewDoc` (with sections) is run by `sldb.api.run_view`; its section declarations
  (which relation each row key follows) come from `sldb.api.notations.list_projection_views`;
- a `SpecDoc` with its `SpecNodeDoc` is resolved by `sldb.api.notations.resolve_view`; what the
  resolved view leaves out (the label of each edge, in its `RelationDoc`, and the `contains` of
  each `SpecNodeDoc`) is read with `sldb.api.load_runtime_documents`.

What specIR adds is only the transformation of those results into the nodes and edges of one
diagram type:

- component: the evaluated graph goes through `sldb.api.notations.component_spec_from_graph`
  (D2, the same generator as `sldb notations from-graph`), the spec it returns is validated as
  sldb's `ComponentDiagram` and compiled by specIR's component compiler. Node ids are D2's safe
  ids (`document_<Model>_<name>`), labels are the documents' titles and kinds their models.
- state: the states are the `StateDoc` of the view, the entity is the `DomainEntityDoc` they name
  (`StateDoc.entity`), and every `transitions` edge (a `DomainOperationDoc` that moves the entity
  into a state) is a transition `on` the operation's title. specIR's graph does not say which
  state an operation leaves, so the transition's `from_` is `ANY_STATE`; the initial state is the
  only state no operation leads into, and empty when there is not exactly one.

Nothing here writes to the store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api.notations import (
    component_spec_from_graph,
    evaluate_projection_view,
    list_projection_views,
    node_id,
    resolve_view,
)

from specir.visual.compilers import compile_ir
from specir.visual.exceptions import CompileError
from specir.visual.ir import ComponentEdge, ComponentIR, ComponentNode, StateIR, StateNode, Transition
from specir.visual.spec_models import ComponentDiagram, validate_spec

#: The `from_` of a transition whose source state the graph does not name.
ANY_STATE = "*"
#: The relation D2 nests (`contains: [...]`) instead of drawing.
CONTAINS = "contains"
DOCUMENT = "sldb://document/"
#: What the IR of a SpecDoc lacks against the IR of its YAML, because the store does not keep it.
SPEC_DOC_GAPS = {"StateIR": ("entity",), "ComponentIR": ("style_kinds",)}

Graph = dict[str, Any]


def _store(store: Path | str) -> Path:
    return Path(store)


def _view_payload(store: Path, ref: str) -> dict[str, Any]:
    """The payload of the ViewDoc `ref` (`ViewDoc:<name>` or `<name>`)."""
    name = ref.split(":", 1)[-1]
    for view in list_projection_views(store):
        if view["ref"] == f"ViewDoc:{name}":
            return dict(view["payload"] or {})
    raise CompileError(f"ViewDoc:{name} is not in the store {store}")


def _composed_graph(store: Path, name: str, sections: list[dict[str, Any]], params: dict[str, str] | None) -> Graph:
    """Nodes and edges of a composed view, from `run_view` and the edges its sections declare."""
    result = api.run_view(store, name, params)
    nodes: dict[str, dict[str, Any]] = {}
    edges: set[tuple[str, str, str]] = set()
    for section in sections:
        rows = _rows(result["sections"].get(section["key"], {}))
        for row in rows:
            nodes[node_id(row["model"], row["name"])] = {
                "model": row["model"], "name": row["name"], "title": (row.get("fields") or {}).get("title") or row["name"],
            }
        for declared in section.get("edges") or []:
            key = declared.get("as") or f"{declared['direction']}:{declared['relation']}"
            for row in rows:
                here = node_id(row["model"], row["name"])
                for other in row.get(key) or []:
                    there = other if other.startswith(DOCUMENT) else f"{DOCUMENT}{other}"
                    pair = (here, there) if declared["direction"] == "out" else (there, here)
                    edges.add((*pair, declared["relation"]))
    kept = sorted((s, t, r) for s, t, r in edges if s in nodes and t in nodes)
    return {"title": result["view"], "nodes": nodes, "edges": kept}


def _rows(section: dict[str, Any]) -> list[dict[str, Any]]:
    if "groups" in section:
        return [row for group in section["groups"] for row in group["rows"]]
    return list(section.get("rows") or [])


def view_graph(store: Path | str, ref: str, params: dict[str, str] | None = None) -> Graph:
    """`{title, nodes: {node id: {model, name, title}}, edges: [(source, target, relation)]}` of the
    ViewDoc `ref`, evaluated by SLDB: `run_view` when it has sections, else
    `evaluate_projection_view`. Node ids are SLDB's `sldb://document/<Model>:<name>`."""
    store = _store(store)
    payload = _view_payload(store, ref)
    if payload.get("sections"):
        graph = _composed_graph(store, payload.get("name") or ref.split(":", 1)[-1], payload["sections"], params)
    else:
        result = evaluate_projection_view(store, f"ViewDoc:{ref.split(':', 1)[-1]}")
        graph = {
            "nodes": {n["id"]: {"model": n["model"], "name": n["name"], "title": n["title"], "payload": n.get("payload") or {}} for n in result["nodes"]},
            "edges": sorted((e["source"], e["target"], e["relation_type"]) for e in result["edges"]),
        }
    graph["title"] = payload.get("title") or payload.get("name") or ref
    return graph


def component_spec_of(graph: Graph, spec_id: str) -> dict[str, Any]:
    """The component spec of an evaluated view, by D2's `component_spec_from_graph`."""
    nodes = {nid: "document" for nid in graph["nodes"]}
    attrs = {nid: {"label": node["title"], "kind": node["model"]} for nid, node in graph["nodes"].items()}
    relations = sorted({r for _, _, r in graph["edges"]})
    return component_spec_from_graph(
        nodes, graph["edges"], relations=relations, exclude_relations=() if not relations else None,
        spec_id=spec_id, title=graph["title"], source=f"ViewDoc:{spec_id}", attrs=attrs,
    )


def component_from_view(store: Path | str, ref: str, params: dict[str, str] | None = None) -> ComponentIR:
    """The ComponentIR of a ViewDoc: its graph as D2's component spec, validated by sldb and compiled."""
    name = ref.split(":", 1)[-1]
    diagram = ComponentDiagram.model_validate(component_spec_of(view_graph(store, ref, params), name))
    validate_spec(diagram)
    return compile_ir(diagram)


def state_from_view(store: Path | str, ref: str, params: dict[str, str] | None = None) -> StateIR:
    """The StateIR of a ViewDoc that selects StateDoc, their DomainEntityDoc and the
    DomainOperationDoc that lead to them (see the module docstring)."""
    graph = view_graph(store, ref, params)
    nodes = graph["nodes"]
    states = sorted((nid for nid, n in nodes.items() if n["model"] == "StateDoc"), key=lambda nid: nodes[nid]["name"])
    if not states:
        raise CompileError(f"{ref} selects no StateDoc: it is not a state diagram")
    entities = {(nodes[s].get("payload") or {}).get("entity") or _referenced(graph, s) for s in states} - {None, ""}
    if len(entities) != 1:
        raise CompileError(f"{ref}: the states name {len(entities)} entities, a state diagram draws one: {sorted(entities)}")
    entity_id = next(iter(entities))
    entity_id = entity_id if entity_id.startswith(DOCUMENT) else f"{DOCUMENT}{entity_id}"
    entity = nodes[entity_id]["title"] if entity_id in nodes else entity_id[len(DOCUMENT):]
    transitions = [
        Transition(from_=ANY_STATE, to=nodes[t]["name"], on=nodes[s]["title"])
        for s, t, r in graph["edges"] if r == "transitions" and t in states and s in nodes
    ]
    entered = {t.to for t in transitions}
    initial = [nodes[s]["name"] for s in states if nodes[s]["name"] not in entered]
    return StateIR(
        title=graph["title"], entity=entity, initial=initial[0] if len(initial) == 1 else "",
        states=[StateNode(id=nodes[s]["name"], label=nodes[s]["title"]) for s in states],
        transitions=transitions,
    )


def _referenced(graph: Graph, state: str) -> str | None:
    """The DomainEntityDoc a state references (its `references` edge), when the payload lacks it."""
    return next((t for s, t, r in graph["edges"] if s == state and r == "references"), None)


def _spec_documents(store: Path, view: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """What `resolve_view` leaves out and the store keeps: the `notes` of each RelationDoc the view
    names (the spec's edge label) and the `contains` of each SpecNodeDoc, as element ids."""
    links = {link["doc"].split(":", 1)[-1] for link in view["links"] if link.get("doc")}
    nodes = {node["doc"].split(":", 1)[-1]: node["element"] for node in view["nodes"]}
    prefix = f"SpecNodeDoc:{view['spec'].split(':', 1)[-1]}."
    notes: dict[str, Any] = {}
    contains: dict[str, list[str]] = {}
    for document in api.load_runtime_documents(store, None, include_linked=False):
        payload = document.payload or {}
        if document.model_name == "RelationDoc" and document.name in links:
            notes[document.name] = payload.get("notes")
        elif document.model_name == "SpecNodeDoc" and document.name in nodes:
            contains[nodes[document.name]] = [ref[len(prefix):] if ref.startswith(prefix) else ref for ref in payload.get("contains") or []]
    return notes, contains


def from_spec_doc(store: Path | str, spec_ref: str) -> ComponentIR | StateIR:
    """The IR of a SpecDoc and its SpecNodeDoc, from `resolve_view` (component and state specs).

    It equals the IR compiled from the spec's YAML except in what SpecSync (sldb, D1) does not keep
    in the store: a state spec's `entity` and a spec's `style.kinds` are fields of the spec, not
    elements, and the SpecDoc has neither. So the StateIR of a SpecDoc has an empty `entity` and
    its ComponentIR an empty `style_kinds` (`SPEC_DOC_GAPS`)."""
    store = _store(store)
    view = resolve_view(store, spec_ref)
    kind = view["diagram_type"]
    if kind not in ("component", "state"):
        raise CompileError(f"{view['spec']} is a `{kind}` spec; specIR materializes component and state SpecDoc")
    elements = {n["doc"]: n["element"] for n in view["nodes"]}
    notes, contains = _spec_documents(store, view)
    links = [
        (elements[link["source"]], elements[link["target"]], link)
        for link in sorted(view["links"], key=lambda l: l["order"]) if link["relation"] != CONTAINS
    ]
    if kind == "component":
        nodes = [
            ComponentNode(id=n["element"], label=n["title"] or n["element"], kind=n["kind"],
                          contains=contains.get(n["element"], []), href=(n.get("data") or {}).get("href"))
            for n in view["nodes"]
        ]
        edges = [
            ComponentEdge(from_=source, to=target, relation=link["relation"], label=notes.get(link["doc"].split(":", 1)[-1]) or None)
            for source, target, link in links
        ]
        return ComponentIR(title=view["title"], nodes=nodes, edges=edges)
    transitions = [
        Transition(from_=source, to=target, on=(link.get("data") or {}).get("on", ""),
                   guard=(link.get("data") or {}).get("guard"), action=(link.get("data") or {}).get("action"))
        for source, target, link in links
    ]
    initial = next((n["element"] for n in view["nodes"] if (n.get("data") or {}).get("initial")), "")
    states = [StateNode(id=n["element"], label=n["title"], contains=contains.get(n["element"]) or None) for n in view["nodes"]]
    return StateIR(title=view["title"], entity="", initial=initial, states=states, transitions=transitions)


__all__ = [
    "ANY_STATE", "SPEC_DOC_GAPS", "component_from_view", "component_spec_of", "from_spec_doc", "state_from_view", "view_graph",
]
