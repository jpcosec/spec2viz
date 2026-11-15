"""specIR's tools on the MCP server of sldb: `sldb mcp --store <project>/.sldb --extension specir.mcp_extension:register`.

The server, its levels, its paging, its guard and its signal log are sldb's (`sldb.mcp`); specIR
adds only what is its own, over its domain types (`specir.models.domain`, IR06):

- `specir_types` (every level, read-only): the domain types, the layer of each, and whether the
  store registers it and how many documents it tracks.
- `specir_nodes` (every level, read-only): the specIR nodes of the store with their provenance
  (IR05 D1-B), filtered by type, layer, origen and verificacion, as a page.
- From level 1, `propose_changes` refuses a change that writes `verificacion: verificado` (IR05
  D2-E: an agent does not verify through the MCP; only a human outside it or a deterministic
  check does). sldb's own write tools are served unchanged otherwise: the extension serves
  `propose_changes` and `apply_changes` from one `WriteTools` of sldb, so the proposal it seals
  is the one `apply_changes` accepts.

This is the only module of specIR that reaches `sldb.mcp`; the rest uses `sldb.api` alone.
"""

from __future__ import annotations

from typing import Any, Literal

import sldb.api as api
from sldb.mcp.changes import AssertEdge, Change, CreateDocument, UpdateDocument
from sldb.mcp.paging import DEFAULT_LIMIT, page
from sldb.mcp.registry import PROPOSES, READ_ONLY, WRITES
from sldb.mcp.write import WriteTools

from specir.models.domain import DOMAIN_MODELS, PROVENANCE_FIELDS, Origen, SpecIRNodeDoc, Verificacion

KINDS = {model.__name__: model for model in DOMAIN_MODELS}
VERIFIES = "an agent does not write verificacion: verificado through the MCP; only a human outside the MCP or a deterministic check verifies (IR05 D2-E)"


def layer_of(model: type[SpecIRNodeDoc]) -> str:
    return model.__semantics__["layer"][0]


def own_fields(model: type[SpecIRNodeDoc]) -> list[str]:
    """The fields a type adds to the provenance and the title and description every node has."""
    return [name for name in model.model_fields if name not in SpecIRNodeDoc.model_fields]


def claims_verified(change: Any) -> bool:
    """Whether a change writes `verificacion: verificado` on a node or in an edge's attributes."""
    if isinstance(change, CreateDocument):
        written = [change.payload, change.payload.get("attributes") or {}]
    elif isinstance(change, UpdateDocument):
        fields = change.fields
        written = [fields, fields.get("attributes") or {}, {"verificacion": fields.get("attributes.verificacion")}]
    elif isinstance(change, AssertEdge):
        written = [change.attributes]
    else:
        return False
    return any(isinstance(values, dict) and values.get("verificacion") == "verificado" for values in written)


class DomainTools:
    """The read tools of specIR over the store of a server context."""

    def __init__(self, context: Any) -> None:
        self.store_path = context.store_path

    def _registered(self) -> list[type[SpecIRNodeDoc]]:
        return [model for model in DOMAIN_MODELS if api.is_model_registered(self.store_path, model.__name__)]

    def specir_types(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """specIR's domain types (one per kind of element a software system is described with,
        from the interface control down to the table): the layer of each, its own fields, and
        whether this store registers it and how many documents it tracks."""
        registered = set(self._registered())
        rows = []
        for model in DOMAIN_MODELS:
            tracked = len(api.select_documents(self.store_path, {"model": model.__name__})) if model in registered else 0
            summary = (model.__doc__ or "").strip().split("\n")[0]
            rows.append({"type": model.__name__, "layer": layer_of(model), "description": summary, "fields": own_fields(model), "registered": model in registered, "documents": tracked})
        explanation = None if registered else "the store does not register specIR's domain types; `python -m specir.install --store <store>` installs them"
        return {**page(rows, offset, limit), **({"explanation": explanation} if explanation else {})}

    def specir_nodes(
        self,
        kind: str | None = None,
        layer: Literal["interface", "api", "backend", "domain", "data"] | None = None,
        origen: Origen | None = None,
        verificacion: Verificacion | None = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """The specIR nodes of this store with their provenance (origen, verificacion,
        verificado_por, evidencia, desconocidos), filtered by domain type (`kind`, e.g. ApiOperationDoc),
        `layer`, `origen` and `verificacion`, as a page ordered by type and path."""
        if kind is not None and kind not in KINDS:
            return {**page([], offset, limit), "explanation": f"{kind!r} is not a domain type of specIR; specir_types lists them", "signal": {"class": "unknown_model", "name": kind, "candidates": sorted(KINDS)}}
        models = [m for m in self._registered() if kind in (None, m.__name__) and layer in (None, layer_of(m))]
        where = " and ".join(f'{name} = "{value}"' for name, value in (("origen", origen), ("verificacion", verificacion)) if value)
        rows = []
        for model in models:
            for row in api.select_documents(self.store_path, {"model": model.__name__, **({"where": where} if where else {})}):
                document = api.serialize_document(api.runtime_document(self.store_path, None, f"{row['model']}/{row['name']}"))
                payload = document["payload"]
                provenance = {name: payload.get(name) for name in PROVENANCE_FIELDS}
                rows.append({"export_id": row["export_id"], "address": f"sldb://document/{row['export_id']}", "type": row["model"], "layer": layer_of(model), "title": payload.get("title"), "path": row["path"], **provenance})
        explanation = None
        if not rows:
            explanation = "the store does not register specIR's domain types" if not self._registered() else "no specIR node matches these filters"
        return page(rows, offset, limit, explanation)


def register(server: Any, context: Any) -> None:
    """Register specIR's tools on a server of `sldb mcp` (the `--extension` contract of sldb)."""
    tools = DomainTools(context)
    server.add_tool(tools.specir_types, annotations=READ_ONLY)
    server.add_tool(tools.specir_nodes, annotations=READ_ONLY)
    if context.level < 1:
        return
    writes = WriteTools(context.store_path, context.level, context.actor)

    def propose_changes(changes: list[Change]) -> dict[str, Any]:
        for change in changes:
            if claims_verified(change):
                raise ValueError(f"{change.name}: {VERIFIES}")
        return writes.propose_changes(changes)

    propose_changes.__doc__ = f"{writes.propose_changes.__doc__} specIR: {VERIFIES}."
    for name in ("propose_changes", "apply_changes"):
        server.remove_tool(name)
    server.add_tool(propose_changes, annotations=PROPOSES)
    server.add_tool(writes.apply_changes, annotations=WRITES)
