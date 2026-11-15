"""The write operations of the specIR MCP server: propose, then apply, through `sldb.api`.

`propose_changes` turns typed changes into a batch in the form of `sldb.api.apply_batch`
with the `expected_source_hash` guard of every document it touches (IR02 D1-A, D2-A) and
writes nothing: it is the dry run, and answers what would be written. `apply_changes` hands
that same batch to `apply_batch`, which prevalidates it (shape, registered model, payload
round-trip under the model, guards, free destination) and applies it whole or not at all,
running the store's `on_write` RuleDocs on every document. A rejection comes back with its
cause: the document that changed since the proposal, or the rules that refused it.

Nothing here validates, renders, serializes, keeps an index or touches a file: every check
is SLDB's. What SLDB does not offer yet is not substituted; it is listed in `PENDING` with
the note that asks SLDB for it, and every answer says so."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api.actor import set_actor

from specir.mcp.addresses import document_address
from specir.mcp.changes import (
    EDGE_MODEL,
    AssertEdge,
    BatchChange,
    CreateDocument,
    DeleteDocument,
    Proposal,
    RetractEdge,
    Sealer,
    UpdateDocument,
    edge_payload,
    model_of,
)
from specir.mcp.mutability import CONTENT, model_level, require, server_level

#: Who signs the provenance of what this server writes (IR05 D1-B: an agent writes `authored`
#: as `agent:<id>`); `--actor` names the agent.
DEFAULT_ACTOR = "agent:specir-mcp"

#: What SLDB does not offer yet, and the note that asks for it. Nothing replaces it in specIR.
PENDING = {
    "dry_run": {
        "what": "a public dry run of apply_batch: propose_changes answers what would be written, but the prevalidation (model round-trip, guards, on_write rules, edge types) runs only when apply_changes calls apply_batch",
        "note": "sldb:20261115-022430-suggestion-specir-dry-run-p-blico-de-apply-batch",
    },
    "edge_validation_before_write": {
        "what": "an edge checked against its RelationTypeDoc (source and target types, cardinality, condition) before the RelationDoc is written: SLDB checks it only in check_edges, after the write, so apply_changes reports the violation instead of refusing it",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
    "store_hash_precondition": {
        "what": "the store's fingerprint as an atomic precondition of apply_batch (level 2): only the per-document guards protect the apply",
        "note": "sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp",
    },
    "guards_in_transaction": {
        "what": "the guards re-checked inside apply_batch's transaction, or a store write lock: a concurrent writer between prevalidation and write is not detected",
        "note": "sldb:20261115-022444-suggestion-specir-guardas-de-apply-batch-bajo-el-cerrojo-del-store",
    },
    "on_write_alerts": {
        "what": "the on_write alerts of a write in apply_batch's answer: SLDB hands them only to in-process listeners, so apply_changes re-reads them with rules_check, which cannot take a document that is not a node of the edge index (a RelationDoc) as subject; those alerts are not reported",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
}


def claims_verified(change: Any) -> bool:
    """Whether a change writes `verificacion: verificado` on a node or in an edge's attributes
    (IR05 D2-E: the MCP is not a surface that verifies)."""
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


class WriteTools:
    """The write surface over one SLDB store, at the level the server was started with."""

    def __init__(self, store: str | Path, level: int, actor: str | None = None) -> None:
        self.level = server_level(level)
        location = api.open_store(Path(store))
        self.store_path = location.store_path
        self.project_root = location.project_root
        self.actor = actor or DEFAULT_ACTOR
        set_actor(self.actor)
        self.sealer = Sealer()

    # -- propose (the dry run) -----------------------------------------------------------

    def propose_changes(self, changes: list[CreateDocument | UpdateDocument | DeleteDocument | AssertEdge | RetractEdge]) -> dict[str, Any]:
        """The batch these changes become, with the server's guards, and what it would write.
        Nothing is written."""
        self._require(changes, "propose_changes")
        if not changes:
            raise ValueError("propose at least one change")
        for change in changes:
            if claims_verified(change):
                raise ValueError(f"{change.name}: an agent does not write verificacion: verificado through the MCP; only a human outside the MCP or a deterministic check verifies (IR05 D2-E)")
        for change in changes:
            path = getattr(change, "path", None)
            if path is not None and not path.endswith(".md"):
                raise ValueError(f"{change.name}: {path!r} is not a Markdown document; no tool writes code or any other file")
        fingerprint = api.store_fingerprint(self.store_path)
        batch = [self._batch_change(change, fingerprint) for change in changes]
        level = max(model_level(c.model) for c in batch)
        proposal = Proposal(changes=batch, level=level, store_hash=fingerprint.store_hash, seal=self.sealer.seal(batch, level, fingerprint.store_hash))
        return {
            "dry_run": True,
            "written": False,
            "proposal": proposal.model_dump(mode="json"),
            "would_write": [self._would_write(c) for c in batch],
            "checked_on_apply": "apply_batch prevalidates the whole batch (shape, registered model, payload round-trip, guards, free destination) and runs the on_write RuleDocs; nothing is written if any check fails",
            "pending": [PENDING["dry_run"], *self._edge_pending(batch), *self._level_pending(level)],
        }

    def _batch_change(self, change: Any, fingerprint: Any) -> BatchChange:
        model, name = model_of(change), change.name
        if isinstance(change, (CreateDocument, AssertEdge)):
            if not api.is_model_registered(self.store_path, model):
                raise ValueError(f"{model} is not a model this store registers; list_models names them")
            payload = change.payload if isinstance(change, CreateDocument) else edge_payload(change)
            return BatchChange(id=name, action="create", model=model, payload=payload, path=change.path)
        hashes = fingerprint.documents.get(f"{model}:{name}")
        if hashes is None:
            raise ValueError(f"{model}:{name} is not a document of this store (a linked store's documents are not written through it)")
        if isinstance(change, UpdateDocument):
            payload = copy.deepcopy(api.runtime_document(self.store_path, None, f"{model}/{name}").payload)
            for path, value in change.fields.items():
                api.deep_set(payload, path, value, create=True)
            return BatchChange(id=name, action="update", model=model, payload=payload, expected_source_hash=hashes.source_hash)
        return BatchChange(id=name, action="delete", model=model, expected_source_hash=hashes.source_hash)

    def _would_write(self, change: BatchChange) -> dict[str, Any]:
        export_id = f"{change.model}:{change.id}"
        row = {"action": change.action, "export_id": export_id, "address": document_address(export_id), "model": change.model}
        if change.action == "create":
            return {**row, "path": change.path, "payload": change.payload}
        status = api.doc_status(self.store_path, f"{change.model}/{change.id}")
        row = {**row, "path": status.path, "expected_source_hash": change.expected_source_hash}
        if change.action == "delete":
            return row
        before = api.runtime_document(self.store_path, None, f"{change.model}/{change.id}").payload
        changed = sorted(k for k in set(before) | set(change.payload or {}) if before.get(k) != (change.payload or {}).get(k))
        return {**row, "payload": change.payload, "changed_fields": changed}

    # -- apply ---------------------------------------------------------------------------

    def apply_changes(self, proposal: Proposal) -> dict[str, Any]:
        """Apply a proposal with `sldb.api.apply_batch`: whole, or nothing and the cause."""
        require(self.level, max([CONTENT, *(model_level(c.model) for c in proposal.changes)]), "apply_changes")
        self.sealer.check(proposal)
        try:
            report = api.apply_batch(self.store_path, [c.batch_form() for c in proposal.changes])
        except api.ConflictError as error:
            return self._rejected("stale", f"the store changed after the proposal was made: {error} Read it again and propose anew.", document=error.ref)
        except Exception as error:  # SLDB's refusals come back with their cause; anything else is a tool error
            if not type(error).__module__.startswith("sldb."):
                raise
            findings = [f.as_dict() for f in getattr(error, "findings", [])]
            if findings:
                rules = sorted({f["code"] for f in findings})
                return self._rejected("rules", f"refused by {', '.join(rules)}: {error}", findings=findings, rules=rules)
            return self._rejected(type(error).__name__, str(error))
        written = [c for c in proposal.changes if c.action != "delete"]
        return {
            "applied": True,
            "saved": list(report.saved),
            "documents": [self._written(c) for c in written],
            "deleted": [document_address(f"{c.model}:{c.id}") for c in proposal.changes if c.action == "delete"],
            "alerts": self._on_write_alerts(written),
            "edge_findings": self._edge_findings([c for c in written if c.model == EDGE_MODEL]),
            "pending": [*self._edge_pending(proposal.changes), *self._level_pending(proposal.level), PENDING["guards_in_transaction"], PENDING["on_write_alerts"]],
        }

    def _rejected(self, cause: str, explanation: str, **detail: Any) -> dict[str, Any]:
        return {"applied": False, "rejected": cause, "explanation": explanation, "written": False, **detail}

    def _written(self, change: BatchChange) -> dict[str, Any]:
        document = api.serialize_document(api.runtime_document(self.store_path, None, f"{change.model}/{change.id}"))
        export_id = f"{change.model}:{change.id}"
        return {"export_id": export_id, "address": document_address(export_id), "path": document["path"], "version": document["version"], "provenance": document["provenance"]}

    def _on_write_alerts(self, written: list[BatchChange]) -> list[dict[str, Any]]:
        """The alerts of the `on_write` RuleDocs on what was written (an error would have refused
        the batch), each naming its rule (`rules/<RuleDoc name>`). Only documents that are nodes
        of the edge index can be a rule subject for `rules_check` (see PENDING["on_write_alerts"])."""
        on_write = {f"rules/{r['name']}" for r in api.select_documents(self.store_path, {"model": "RuleDoc", "where": 'moment = "on_write"', "include_linked": True})}
        subjects = [f"{c.model}/{c.id}" for c in written if api.edge_node(self.store_path, document_address(f"{c.model}:{c.id}")) is not None]
        if not on_write:
            return []
        found = (f.as_dict() for subject in subjects for f in api.rules_check(self.store_path, subject))
        return [f for f in found if f["code"] in on_write and f["level"] == "alert"]

    def _edge_findings(self, edges: list[BatchChange]) -> list[str]:
        """The edge index's violations about the edges just written (SLDB checks edges only
        after the write: see PENDING["edge_validation_before_write"])."""
        if not edges:
            return []
        errors = api.check_edges(self.store_path, include_linked=False).errors
        marks = [m for c in edges for m in self._edge_marks(c)]
        return [e for e in errors if any(all(part in e for part in mark) for mark in marks)]

    @staticmethod
    def _edge_marks(change: BatchChange) -> list[tuple[str, ...]]:
        """How SLDB's edge check names this edge: by its RelationDoc, as `source -[type]-> target`,
        or, for cardinality, as its source with that type's targets or its target with its sources."""
        payload = change.payload or {}
        source, target, relation = document_address(payload.get("source_id", "")), document_address(payload.get("target_id", "")), payload.get("relation_type", "")
        return [(f"relation '{change.id}'",), (f"{source} -[{relation}]-> {target}",), (f"{source} has ", f"'{relation}' targets"), (f"{target} has ", f"'{relation}' sources")]

    @staticmethod
    def _edge_pending(changes: list[BatchChange]) -> list[dict[str, str]]:
        return [PENDING["edge_validation_before_write"]] if any(c.model == EDGE_MODEL and c.action == "create" for c in changes) else []

    @staticmethod
    def _level_pending(level: int) -> list[dict[str, str]]:
        return [PENDING["store_hash_precondition"]] if level > CONTENT else []

    def _require(self, changes: list[Any], tool: str) -> None:
        """Refuse before reading the store: the tool's level, then each change's model's."""
        require(self.level, CONTENT, tool)
        for change in changes:
            require(self.level, model_level(model_of(change)), f"{tool} on {model_of(change)}:{change.name}")
