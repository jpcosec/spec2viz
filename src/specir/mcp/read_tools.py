"""The read operations of the specIR MCP server, as plain functions over `sldb.api`.

Each method is a thin adapter: it calls the operation the IR01 audit marks as available
(docs/auditoria/sldb-api-frente-a-mcp.md), shapes the answer as JSON with the stable address
of every document, and pages every set. A question about something the store does not
declare answers an empty set (or `found: false`) with an `explanation`, not an opaque error.

Nothing here writes, keeps an edge index, traverses the graph or parses a predicate:
neighbours come from `edges_from`/`edges_to`, the multi-hop neighbourhood from
`sldb.api.graph.collect_neighborhood_by_direction` (it walks every relation type of the
index in the given direction; no per-hop relation filter), predicates from
`select_documents`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api import graph

from specir.mcp.addresses import (
    addressed_row,
    document_address,
    model_address,
    node_or_document,
    relation_type_address,
    row_alias,
)
from specir.mcp.paging import DEFAULT_LIMIT, page

#: The directions `collect_neighborhood_by_direction` understands; any other value would be
#: read by SLDB as "both", so it is refused here instead.
NEIGHBORHOOD_DIRECTIONS = ("outgoing", "incoming", "both")
#: One-hop neighbours: `edges_from` (outgoing) or `edges_to` (incoming).
NEIGHBOR_DIRECTIONS = ("outgoing", "incoming")


class ReadTools:
    """The read surface over one SLDB store (its linked stores read through it)."""

    def __init__(self, store: str | Path) -> None:
        location = api.open_store(Path(store), mode="readonly")
        self.store_path = location.store_path
        self.project_root = location.project_root

    # -- models and relation types -------------------------------------------------------

    def list_models(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Every model the store registers (its own and the inherited ones)."""
        entries = api.registered_models(self.store_path)
        items = [
            {"address": model_address(e.name), "name": e.name, "model_ref": e.model_ref, "origin": e.origin, "version": e.version, "family": e.family, "semantics": list(e.semantics)}
            for e in entries
        ]
        return page(items, offset, limit, None if items else "the store registers no model")

    def describe_model(self, model: str, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """A model's contract (fields with their types) and a page of its tracked documents."""
        if not api.is_model_registered(self.store_path, model):
            return {"found": False, "model": model, "explanation": f"the store does not register a model named {model!r}; list_models names the ones it does"}
        description = api.describe_model(self.store_path, model).model_dump(mode="json")
        documents = [{"address": document_address(f"{description['name']}:{d['name']}"), **d} for d in description.pop("documents")]
        return {
            "found": True,
            "address": model_address(description["name"]),
            **description,
            "documents": page(documents, offset, limit, None if documents else f"the store tracks no document of {model}"),
        }

    def list_relation_types(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The relation types of the edge index (this store's and its linked stores')."""
        nodes = api.edge_nodes_of_type(self.store_path, "relation_type")
        items = [{"address": n.id, "name": api.bare(n.id), **n.semantics} for n in nodes]
        return page(items, offset, limit, None if items else "the edge index declares no relation type")

    def describe_relation_type(self, name: str) -> dict[str, Any]:
        """One relation type: its endpoints, direction, cardinality and description."""
        node = api.edge_node(self.store_path, relation_type_address(name))
        if node is None:
            return {"found": False, "name": name, "explanation": f"the edge index declares no relation type {name!r}; list_relation_types names the ones it does"}
        return {"found": True, "address": node.id, "name": api.bare(node.id), **node.semantics}

    # -- documents ----------------------------------------------------------------------------

    def read_document(self, ref: str, field: str | None = None) -> dict[str, Any]:
        """A document by `[alias:]Model:name` (or name, `Model/name`, tracked path): its payload,
        or the value of one dotted `field` path."""
        rows = api.select_documents(self.store_path, {"ref": ref})
        if not rows:
            return {"found": False, "ref": ref, "explanation": f"the store tracks no document named {ref!r} (a linked store's document is written `alias:Model:name`)"}
        if len(rows) > 1:
            return {"found": False, "ref": ref, "explanation": f"{ref!r} names {len(rows)} documents; use one of their export ids", "candidates": [r["export_id"] for r in rows]}
        row = rows[0]
        alias = row_alias(row)
        target = f"{row['model']}/{row['name']}" if alias is None else f"{alias}:{row['model']}/{row['name']}"
        document = api.serialize_document(api.runtime_document(self.store_path, None, target))
        answer = {
            "found": True,
            "address": document_address(row["export_id"]),
            "export_id": row["export_id"],
            "store": alias or "local",
            "model": document["model_name"],
            "name": document["id"],
            "path": document["path"],
            "version": document["version"],
            "semantic_tags": document["semantic_tags"],
            "provenance": document["provenance"],
        }
        if field is None:
            return {**answer, "payload": document["payload"]}
        try:
            value = api.deep_get(document["payload"], field)
        except (KeyError, IndexError, TypeError, ValueError) as error:
            return {**answer, "found": False, "field": field, "explanation": f"{row['export_id']} has no field {field!r} ({error}); its top-level fields are {sorted(document['payload'])}"}
        return {**answer, "field": field, "value": value}

    def select_documents(
        self,
        model: str | None = None,
        where: str | None = None,
        ref: str | None = None,
        prefix: str | None = None,
        path_glob: str | None = None,
        include_linked: bool = False,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """The documents a selector names (keys combined by conjunction; `where` is a predicate
        of SLDB's rules language over the payload projection)."""
        selector = {k: v for k, v in {"model": model, "where": where, "ref": ref, "prefix": prefix, "path_glob": path_glob}.items() if v}
        rows = [addressed_row(r) for r in api.select_documents(self.store_path, {**selector, "include_linked": include_linked})]
        if rows:
            return page(rows, offset, limit)
        if model and not api.is_model_registered(self.store_path, model):
            return page([], offset, limit, f"the store does not register a model named {model!r}; list_models names the ones it does (a linked store's model needs include_linked)")
        return page([], offset, limit, f"no document matches {selector or 'an empty selector'}")

    # -- graph --------------------------------------------------------------------------------

    def neighbors(self, node: str, direction: str = "outgoing", relation: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The edges leaving (`outgoing`, `edges_from`) or reaching (`incoming`, `edges_to`) a
        document (`[alias:]Model:name`) or any node id (`sldb://...`), optionally of one relation type."""
        if direction not in NEIGHBOR_DIRECTIONS:
            raise ValueError(f"direction must be one of {NEIGHBOR_DIRECTIONS}, not {direction!r}")
        address = node_or_document(node)
        missing = self._undeclared(address, relation)
        if missing:
            return {"node": address, "direction": direction, "relation": relation, **page([], offset, limit, missing)}
        read = api.edges_from if direction == "outgoing" else api.edges_to
        edges = [e.model_dump(mode="json") for e in read(self.store_path, address, relation)]
        explanation = None if edges else f"{address} has no {direction} edge" + (f" of relation {relation!r}" if relation else "")
        return {"node": address, "direction": direction, "relation": relation, **page(edges, offset, limit, explanation)}

    def neighborhood(self, node: str, direction: str = "outgoing", depth: int = 1, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The node ids within `depth` hops of `node` in one direction, seeds excluded. Every
        relation type of the index is walked; no relation filter applies per hop."""
        if direction not in NEIGHBORHOOD_DIRECTIONS:
            raise ValueError(f"direction must be one of {NEIGHBORHOOD_DIRECTIONS}, not {direction!r}")
        if depth < 1:
            raise ValueError(f"depth must be >= 1, not {depth}")
        address = node_or_document(node)
        missing = self._undeclared(address, None)
        if missing:
            return {"node": address, "direction": direction, "depth": depth, **page([], offset, limit, missing)}
        nodes = sorted(graph.collect_neighborhood_by_direction(self.store_path, {address}, depth, direction))
        explanation = None if nodes else f"no node lies within {depth} {direction} hop(s) of {address}"
        return {"node": address, "direction": direction, "depth": depth, **page(nodes, offset, limit, explanation)}

    def _undeclared(self, address: str, relation: str | None) -> str | None:
        """Why a graph question names something the store does not declare, or None."""
        if api.edge_node(self.store_path, address) is None:
            return f"the edge index has no node {address}"
        if relation and api.edge_node(self.store_path, relation_type_address(relation)) is None:
            return f"the edge index declares no relation type {relation!r}; list_relation_types names the ones it does"
        return None

    # -- views --------------------------------------------------------------------------------

    def list_views(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The views the store can resolve: composed ViewDocs (by name), projection ViewDocs and
        SpecDocs (by export id), local and linked."""
        items: list[dict[str, Any]] = [{"kind": "composed", "view": v["name"], **v} for v in api.list_views(self.store_path)]
        items += [{"kind": "projection", "view": v["ref"], "address": document_address(v["ref"])} for v in api.list_projection_views(self.store_path)]
        items += [{"kind": "spec", "view": r["export_id"], **addressed_row(r)} for r in api.select_documents(self.store_path, {"model": "SpecDoc", "include_linked": True})]
        return page(items, offset, limit, None if items else "the store holds no ViewDoc and no SpecDoc")

    def resolve_view(self, view: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        """A view resolved to JSON: a composed ViewDoc by name (`run_view`), a projection ViewDoc
        (`evaluate_projection_view`) or a SpecDoc according to its notation (`resolve_view`)."""
        if view in {v["name"] for v in api.list_views(self.store_path)}:
            return {"found": True, "kind": "composed", "view": view, "result": api.run_view(self.store_path, view, params)}
        rows = api.select_documents(self.store_path, {"ref": view})
        if len(rows) != 1:
            why = "names no composed view and no document" if not rows else f"names {len(rows)} documents"
            return {"found": False, "view": view, "explanation": f"{view!r} {why}; list_views names the views the store can resolve"}
        row = rows[0]
        store = self._store_of(row_alias(row))
        base = {"found": True, "view": view, "address": document_address(row["export_id"]), "export_id": row["export_id"]}
        if row["model"] == "SpecDoc":
            return {**base, "kind": "spec", "result": api.resolve_view(store, f"SpecDoc:{row['name']}")}
        if row["model"] == "ViewDoc":
            return {**base, "kind": "projection", "result": api.evaluate_projection_view(store, f"ViewDoc:{row['name']}")}
        return {"found": False, "view": view, "export_id": row["export_id"], "explanation": f"{row['export_id']} is a {row['model']}, not a ViewDoc or a SpecDoc"}

    def _store_of(self, alias: str | None) -> Path:
        """The store a document lives in: this one, or the linked store recorded under `alias`."""
        if alias is None:
            return self.store_path
        link = next((link for link in api.store_links(self.store_path) if link["name"] == alias), None)
        if link is None or link.get("status") != "ok":
            raise ValueError(f"the linked store {alias!r} is not readable: {link}")
        return Path(link["resolved"])

    # -- integrity ------------------------------------------------------------------------------

    def check_integrity(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The store's integrity check (`check_store`) and the edge index's (`check_edges`):
        verdicts and counts, with the errors and alerts as one page of findings.

        The verdict covers this store's own edges (`include_linked=False`); the federated
        index is reported apart, as `linked_edges`: its findings are the linked stores' to fix.
        """
        report = api.check_store(self.store_path, self.project_root)
        edges = api.check_edges(self.store_path, include_linked=False)
        federated = api.check_edges(self.store_path, include_linked=True)
        findings = list(report["errors"]) + list(report["alerts"]) + [{"level": "error", "code": "edges/invalid", "what": e} for e in edges.errors]
        summary = {k: (len(v) if isinstance(v, list) else v) for k, v in report.items()}
        return {
            "ok": bool(report["ok"]) and edges.ok,
            "store": summary,
            "edges": {"ok": edges.ok, **_counts(edges)},
            "linked_edges": _counts(federated),
            "findings": page(findings, offset, limit, None if findings else "the store and its edge index report no error and no alert"),
        }


def _counts(report: Any) -> dict[str, int]:
    """The size of each list of an `EdgeCheckReport`."""
    return {k: len(v) for k, v in report.model_dump().items() if isinstance(v, list)}
