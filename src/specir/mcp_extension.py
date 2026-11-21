"""specIR's tools on the MCP server of sldb: `sldb mcp --store <project>/.sldb --extension specir.mcp_extension:register`.

The server, its levels, its paging, its guard and its signal log are sldb's (`sldb.mcp`); specIR
adds only what is its own, over its domain types (`specir.models.domain`, IR06):

- `specir_types` (every level, read-only): the domain types, the layer of each, and whether the
  store registers it and how many documents it tracks.
- `specir_nodes` (every level, read-only): the specIR nodes of the store with their provenance
  (IR05 D1-B), filtered by type, layer, origen and verificacion, as a page.
- `specir_rules` (every level, read-only): the findings of specIR's cross-layer rules (IR10:
  broken chains between interface, API, operation and data), evaluated by sldb's rule engine
  (`sldb.api.rules_check`), each with its severity, the rule that produced it and the document.
- `specir_impact` (every level, read-only): the nodes of the other layers a change to one node
  (a field, an endpoint, a rule, a table) affects, each with the explained path sldb gives
  (`sldb.api.graph.graph_path`) and the provenance of every hop; a path through an `inferido`
  relation says so. It proposes no change.
- From level 1, a batch validator (`context.add_batch_validator` of sldb) refuses a change that
  writes `verificacion: verificado` (IR05 D2-E: an agent does not verify through the MCP; only a
  human outside it or a deterministic check does). sldb runs it on `propose_changes` (over the
  typed changes: a tool error naming IR05 D2-E) and on `apply_changes` (over the proposal's batch
  changes: a `domain` rejection), nothing written either way; the description of `propose_changes` says the rule. The write tools, their proposal and the undo of the session
  are sldb's, served unchanged: this module creates none of them.

This is the only module of specIR that reaches `sldb.mcp`; the rest uses `sldb.api` alone.
"""

from __future__ import annotations

from typing import Any, Literal

import sldb.api as api
from sldb.mcp.changes import AssertEdge, BatchChange, CreateDocument, UpdateDocument
from sldb.mcp.paging import DEFAULT_LIMIT, page
from sldb.mcp.registry import READ_ONLY

from specir.impact import affected, export_id
from specir.models.domain import DOMAIN_MODELS, PROVENANCE_FIELDS, Origen, SpecIRNodeDoc, Verificacion

RULE_PREFIX = "rules/rule-specir-"
KINDS = {model.__name__: model for model in DOMAIN_MODELS}
VERIFIES = "an agent does not write verificacion: verificado through the MCP; only a human outside the MCP or a deterministic check verifies (IR05 D2-E)"


def layer_of(model: type[SpecIRNodeDoc]) -> str:
    return model.__semantics__["layer"][0]


def own_fields(model: type[SpecIRNodeDoc]) -> list[str]:
    """The fields a type adds to the provenance and the title and description every node has."""
    return [name for name in model.model_fields if name not in SpecIRNodeDoc.model_fields]


def _says_verified(values: Any) -> bool:
    return isinstance(values, dict) and values.get("verificacion") == "verificado"


def _payload_verified(payload: dict[str, Any] | None) -> bool:
    return _says_verified(payload) or _says_verified((payload or {}).get("attributes"))


def claims_verified(change: Any, store_path: Any = None) -> bool:
    """Whether a change writes `verificacion: verificado` on a node or in an edge's attributes.

    It reads the typed changes of `propose_changes` and the `BatchChange`s of `apply_changes`. A
    batch update carries the whole payload, so it claims it only if the stored document is not
    verified already (a human's verification stays; editing another field of it is not a claim)."""
    if isinstance(change, CreateDocument):
        return _payload_verified(change.payload)
    if isinstance(change, UpdateDocument):
        fields = change.fields
        return _payload_verified(fields) or fields.get("attributes.verificacion") == "verificado"
    if isinstance(change, AssertEdge):
        return _says_verified(change.attributes)
    if isinstance(change, BatchChange) and change.action in ("create", "update"):
        if not _payload_verified(change.payload):
            return False
        if change.action == "update" and store_path is not None:
            current = api.serialize_document(api.runtime_document(store_path, None, f"{change.model}/{change.id}"))["payload"]
            return not _payload_verified(current)
        return True
    return False


def change_name(change: Any) -> str:
    return getattr(change, "name", None) or getattr(change, "id", "")


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

    def specir_rules(self, severity: Literal["error", "alert"] | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """The findings of specIR's cross-layer rules over this store (a control that triggers no
        action, an action that invokes no operation, an interface field the serializer lacks, an
        operation without handler, an entity without table, a policy no control reaches), as a page.
        Each has its `severity`, the `rule` that produced it, the `subject` document and its path,
        and what is missing. sldb's engine evaluates them; nothing is written and nothing is proposed."""
        if not any(api.is_model_registered(self.store_path, model.__name__) for model in DOMAIN_MODELS):
            return {**page([], offset, limit), "explanation": "the store does not register specIR's domain types; `python -m specir.install --store <store>` installs them"}
        rows = []
        for finding in api.rules_check(self.store_path):
            if not finding.code.startswith(RULE_PREFIX) or severity not in (None, finding.level):
                continue
            rows.append({"severity": finding.level, "rule": finding.code.removeprefix("rules/"), "subject": finding.subject, "address": f"sldb://document/{finding.subject}", "path": finding.document, "what": finding.what})
        rows.sort(key=lambda r: (r["severity"], r["rule"], r["subject"]))
        return page(rows, offset, limit, None if rows else "no specIR rule reports a finding")

    def specir_impact(
        self,
        node: str,
        field: str | None = None,
        direction: Literal["dependents", "dependencies"] = "dependents",
        layer: Literal["interface", "api", "backend", "domain", "data"] | None = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """The specIR nodes a change to `node` (`Model:name`, e.g. TableDoc:posts, ApiOperationDoc:...,
        PolicyDoc:...) affects, in the other layers: with `direction` dependents (default) the nodes
        whose chain of relations leads to it (the interface above a table or an endpoint),
        with dependencies the nodes it leads to. `field` names the changed field or column of the
        node (a column of a TableDoc, a field of the document) and must exist. Each affected node
        carries the explained path from sldb: every hop with its relation, direction and
        provenance (origen, verificacion, evidencia); `inferred` is true when a hop is `inferido`.
        It reports what is affected and why, never a change to make."""
        ref = export_id(node)
        model_name = ref.split(":", 1)[0]
        if model_name not in KINDS or not api.is_model_registered(self.store_path, model_name):
            return {**page([], offset, limit), "explanation": f"{node!r} is not a node of a specIR type registered in this store; specir_nodes lists them", "signal": {"class": "unknown_model", "name": model_name, "candidates": sorted(KINDS)}}
        try:
            payload = api.serialize_document(api.runtime_document(self.store_path, None, ref.replace(":", "/", 1)))["payload"]
        except Exception:
            return {**page([], offset, limit), "explanation": f"the store has no document {ref}; specir_nodes lists the nodes", "signal": {"class": "unknown_document", "name": ref}}
        if field is not None and field not in (payload.get("columns") or []) and field not in payload:
            return {**page([], offset, limit), "explanation": f"{ref} has no field or column {field!r}", "signal": {"class": "unknown_field", "name": field}}
        rows = [r for r in affected(self.store_path, ref, direction) if layer in (None, r["layer"])]
        rows.sort(key=lambda r: (len(r["path"]["steps"]), r["layer"], r["export_id"]))
        answer = page(rows, offset, limit, None if rows else f"no node of another layer {'depends on' if direction == 'dependents' else 'is reached from'} {ref}")
        return {"changed": {"node": ref, "field": field, "direction": direction}, **answer}


def register(server: Any, context: Any) -> None:
    """Register specIR's tools on a server of `sldb mcp` (the `--extension` contract of sldb)."""
    tools = DomainTools(context)
    server.add_tool(tools.specir_types, annotations=READ_ONLY)
    server.add_tool(tools.specir_nodes, annotations=READ_ONLY)
    server.add_tool(tools.specir_rules, annotations=READ_ONLY)
    server.add_tool(tools.specir_impact, annotations=READ_ONLY)
    if context.level < 1:
        return

    def verification_is_not_written(changes: list[Any], validating: Any) -> list[dict[str, Any]]:
        """sldb's `BatchValidator`: one error finding per change that writes `verificacion: verificado`.

        In `propose_changes` sldb hands it the typed changes: the proposal is refused as a tool
        error that names IR05 D2-E. In `apply_changes` it hands it the batch changes: a `domain`
        rejection with the findings, nothing written."""
        findings = [
            {"code": "specir_agent_verifies", "level": "error", "what": f"{change_name(change)}: {VERIFIES}", "subject": change_name(change)}
            for change in changes
            if claims_verified(change, validating.store_path)
        ]
        if findings and not any(isinstance(change, BatchChange) for change in changes):
            raise ValueError("; ".join(f["what"] for f in findings))
        return findings

    context.add_batch_validator(verification_is_not_written)
    # The tool stays sldb's (one WriteTools, one undo stack); only its description says the rule.
    try:
        tool = server._tool_manager.get_tool("propose_changes")
    except AttributeError:  # pragma: no cover - a server without the tool manager keeps sldb's description
        tool = None
    if tool is not None:
        tool.description = f"{tool.description} specIR: {VERIFIES}."
