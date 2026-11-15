FILE:desk/tasks/task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar.md
---
sldb:
  by: agent
  at: '2026-11-12T04:40:28Z'
  authority: generated
  via: save_document_payload
id: task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
- task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- src/specir/mcp/write_tools.py
- src/specir/mcp/changes.py
- src/specir/mcp/mutability.py
- tests/mcp/test_write_tools.py
- tests/mcp/test_dry_run.py
- tests/mcp/test_mutability.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar.md
---

# IR04 Escritura validada por MCP: proponer, validar, aplicar

## Rationale

_Explain why this task exists or the business driver behind it._

Un agente que solo lee no desbloquea el modelado. La escritura por MCP tiene que impedir que el modelo quede inconsistente y dejar rastro de quién escribió qué.

## Goal

_Describe the concrete result this task must produce._

Tools MCP de escritura con las que un agente propone, valida y aplica cambios al store, con el mecanismo decidido en la tarea de contrato de escritura.

## Scope

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

Dentro, mutaciones del store que expone el MCP: crear, editar y borrar documentos de modelos ya registrados; afirmar y retirar aristas (RelationDoc); declarar y editar tipos de relación (RelationTypeDoc) y reglas (RuleDoc), que son documentos del store y por eso se escriben como datos. Toda escritura admite ejecución en seco. Fuera: crear o editar clases Python de modelos por MCP. Las clases de modelo se definen como código en el paquete specIR (o en el paquete del proyecto que las declare) y entran al store por el registro de modelos de SLDB; exponer su edición por MCP queda como decisión posterior, condicionada a la tarea de contrato de escritura. Fuera también: síntesis de código de aplicación. En specIR, estas operaciones solo se exponen como tools MCP; no se implementan funciones propias de CRUD ni escrituras directas al filesystem o a índices SLDB. La creación, edición, borrado, validación de modelos, reglas e integridad se delegan en las operaciones existentes de `sldb.api`; si una capacidad falta, se pide extensión al desk SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

Las tools envuelven las operaciones de escritura, prevalidación, reglas y transiciones que la matriz de auditoría marca como existentes en la API pública de SLDB; lo que falte se resuelve en SLDB, no en specIR. Delegación obligatoria por operación: crear documento con `sldb.api.create_document`; editar payload de documento existente con `sldb.api.save_document_payload`; borrar con `sldb.api.delete_document`. RelationDoc, RelationTypeDoc y RuleDoc se escriben como documentos mediante esas mismas funciones con su modelo registrado, no mediante mutación propia del índice de aristas. Los tools MCP convierten argumentos tipados a llamadas API y devuelven sus resultados/errores; no duplican serialización, renderizado, validación de modelo/reglas, mantenimiento de índices, ni borrado de archivos. Para agrupar cambios usa `sldb.api.transaction` cuando corresponda. La ejecución en seco y el contrato de precondición usan mecanismos existentes de SLDB; si la API pública no los ofrece, el nodo no crea una implementación paralela en specIR y deja la brecha solicitada a SLDB.

## Validation

_List the checks required before this task can close._

- Una ejecución en seco devuelve lo que se escribiría y no cambia ningún archivo del store.
- Aplicar un cambio validado sobre un store que cambió después de la validación es rechazado con un error que lo dice.
- Una arista que viola los tipos de origen o destino, la cardinalidad o la condición de su RelationTypeDoc es rechazada antes de escribir.
- Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad de la regla, y la respuesta nombra la regla.
- Ninguna tool de escritura recibe texto libre para interpretar: solo argumentos tipados.
- Cada documento escrito lleva en su procedencia quién y por qué operación se escribió.
- Una tool por encima del nivel de escritura permitido responde error sin evaluar nada.
- No existe ninguna tool que cree o modifique módulos Python.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan contra un store de prueba y un agente completa el ciclo proponer, validar y aplicar sobre un documento y sobre una arista.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:desk/atoms/atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir.md
---
sldb:
  by: agent
  at: '2026-11-15T05:05:58Z'
  authority: generated
  via: save_document_payload
id: atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
title: Principios de seguridad de la superficie MCP de specIR
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- topic:procedencia
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# Principios de seguridad de la superficie MCP de specIR

## Answer

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Mecanismos decididos (docs/decisiones/contrato-de-escritura-mcp.md, 2026-11-15): la propuesta es un lote efímero prevalidado que se aplica todo o nada con sldb.api.apply_batch (atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado); la aplicación se protege con guardas expected_source_hash por documento y, en nivel 2, con store_hash atómico (atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2); el nivel de escritura se fija al arrancar el servidor, 0 por defecto (atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor); deshacer es un lote inverso con guardas (atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas). Procedencia decidida (docs/decisiones/procedencia-y-divergencia.md, 2026-11-15): ejes origen y verificacion con la autoridad de SLDB por tabla (atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla); lo desconocido se nombra y el MCP nunca escribe verificado (atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica); anclas de SLDB y divergencia según el origen (atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen).

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:src/specir/mcp/write_tools.py
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

FILE:src/specir/mcp/changes.py
"""The typed changes an agent proposes, and the proposal that carries them to `apply`.

A change is a typed argument, never text the server interprets: one of the actions below,
with the model and name of the document it touches. A proposal is the batch in the form of
`sldb.api.apply_batch` (IR02 D1-A: an ephemeral batch, nothing kept between steps) with the
`expected_source_hash` guard the server filled in for every document it touches (D2-A), and
a seal over that batch so `apply` runs exactly what was proposed.

The seal is an HMAC with a secret of the server process: it only proves the batch came from
`propose_changes` of this process unchanged. It is not a store precondition; the guards are,
and `apply_batch` checks them."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from specir.mcp.mutability import model_level

#: The model of an authored edge (sldb.models.relation_doc).
EDGE_MODEL = "RelationDoc"


class _Change(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateDocument(_Change):
    """Create a document of a registered model."""

    action: Literal["create"]
    model: str = Field(description="A model the store registers.")
    name: str = Field(description="The new document's name, unique in the store.")
    payload: dict[str, Any] = Field(description="Every field of the document, as the model declares it.")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, the model's default directory.")


class UpdateDocument(_Change):
    """Set fields of a tracked document; the rest of its payload stays as it is."""

    action: Literal["update"]
    model: str
    name: str
    fields: dict[str, Any] = Field(description="Dotted field path -> new value (sldb.api.deep_set).")


class DeleteDocument(_Change):
    """Delete a tracked document and its file."""

    action: Literal["delete"]
    model: str
    name: str


class AssertEdge(_Change):
    """Assert an authored edge: a `RelationDoc` source -[relation_type]-> target."""

    action: Literal["assert_edge"]
    name: str = Field(description="The RelationDoc's name, unique in the store.")
    source: str = Field(description="Export id of the source document (`Model:name`, `alias:Model:name` for a linked store).")
    target: str = Field(description="Export id of the target document.")
    relation_type: str = Field(description="The name of a tracked RelationTypeDoc.")
    title: str | None = Field(default=None, description="The RelationDoc's title; omitted, `<source> <relation_type> <target>`.")
    condition: str = Field(default="", description="A predicate for this edge only; empty inherits the type's condition.")
    attributes: dict[str, Any] = Field(default_factory=dict)
    notes: str = Field(default="")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, RelationDoc's default directory.")


class RetractEdge(_Change):
    """Retract an authored edge: delete its `RelationDoc`."""

    action: Literal["retract_edge"]
    name: str = Field(description="The RelationDoc's name.")


Change = Annotated[Union[CreateDocument, UpdateDocument, DeleteDocument, AssertEdge, RetractEdge], Field(discriminator="action")]


def model_of(change: CreateDocument | UpdateDocument | DeleteDocument | AssertEdge | RetractEdge) -> str:
    """The model of the document a change touches."""
    return getattr(change, "model", EDGE_MODEL)


def level_of(changes: list[Any]) -> int:
    """The write level a list of changes needs: the highest of its documents' models."""
    return max((model_level(model_of(c)) for c in changes), default=0)


def edge_payload(change: AssertEdge) -> dict[str, Any]:
    """The `RelationDoc` payload of an asserted edge."""
    return {
        "title": change.title or f"{change.source} {change.relation_type} {change.target}",
        "source_id": change.source,
        "target_id": change.target,
        "relation_type": change.relation_type,
        "condition": change.condition,
        "attributes": change.attributes,
        "notes": change.notes,
    }


class BatchChange(BaseModel):
    """One change in the form `sldb.api.apply_batch` takes, plus the model it touches."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="The document name.")
    action: Literal["create", "update", "delete"]
    model: str
    payload: dict[str, Any] | None = None
    path: str | None = None
    expected_source_hash: str | None = Field(default=None, description="The document's source hash when the change was proposed (filled by the server).")

    def batch_form(self) -> dict[str, Any]:
        """The dict `apply_batch` reads (it names the model only on create)."""
        form = {"id": self.id, "action": self.action}
        if self.action == "create":
            form["model"] = self.model
        if self.payload is not None:
            form["payload"] = self.payload
        if self.path is not None:
            form["path"] = self.path
        if self.expected_source_hash is not None:
            form["expected_source_hash"] = self.expected_source_hash
        return form


class Proposal(BaseModel):
    """What `propose_changes` returns and `apply_changes` takes back, unchanged."""

    model_config = ConfigDict(extra="forbid")

    changes: list[BatchChange]
    level: int = Field(description="The write level the batch needs.")
    store_hash: str = Field(description="The store's fingerprint when proposed (informational: no SLDB write accepts it as a precondition yet).")
    seal: str = Field(description="The server's seal over the batch; any edit makes `apply_changes` refuse it.")


class Sealer:
    """Seals and checks proposals with a secret of this server process."""

    def __init__(self) -> None:
        self._key = secrets.token_bytes(32)

    def seal(self, changes: list[BatchChange], level: int, store_hash: str) -> str:
        body = json.dumps({"changes": [c.model_dump(mode="json") for c in changes], "level": level, "store_hash": store_hash}, sort_keys=True, separators=(",", ":"))
        return hmac.new(self._key, body.encode("utf-8"), hashlib.sha256).hexdigest()

    def check(self, proposal: Proposal) -> None:
        if not hmac.compare_digest(proposal.seal, self.seal(proposal.changes, proposal.level, proposal.store_hash)):
            raise ValueError("the proposal is not the one propose_changes returned (edited, or proposed by another server process); propose it again")

FILE:src/specir/mcp/mutability.py
"""The write level the server allows, fixed when it starts (IR02 D3-A).

Levels follow the contract adopted from pron §5 and are cumulative: 0 reads only (the
default, IR03); 1 writes content (documents of registered models and authored edges,
`RelationDoc`); 2 also writes the store's rules as data (`RelationTypeDoc`, `RuleDoc`).
Level 3 (models as Python code) is never served: no tool creates or modifies a Python module.

The level is a server argument, never a tool argument. Every check here reads only the
typed arguments of the call, so a call above the level fails before the store is read."""

from __future__ import annotations

READ, CONTENT, RULES = 0, 1, 2
LEVELS = {READ: "read", CONTENT: "content", RULES: "rules"}
#: Models whose documents are the store's rules: writing them changes what is valid.
RULE_MODELS = frozenset({"RelationTypeDoc", "RuleDoc"})


class LevelError(PermissionError):
    """A call above the write level the server was started with."""


def server_level(value: int) -> int:
    """The level to serve, checked: 0, 1 or 2 (3, models as code, is never served)."""
    if value not in LEVELS:
        raise ValueError(f"write level {value} is not served; choose one of {sorted(LEVELS)} ({', '.join(f'{k}={v}' for k, v in LEVELS.items())})")
    return value


def model_level(model: str) -> int:
    """The level a change to a document of `model` needs."""
    return RULES if model in RULE_MODELS else CONTENT


def require(allowed: int, needed: int, what: str) -> None:
    """Refuse `what` when it needs a level above `allowed`."""
    if needed > allowed:
        raise LevelError(f"{what} needs write level {needed} ({LEVELS[needed]}); this server was started with level {allowed} ({LEVELS[allowed]}). The level is set by the operator (`--level`), not by a tool argument.")

FILE:tests/mcp/test_write_tools.py
"""Propose and apply, called by the real MCP client on the real server at write level 2 over
its own copy of this repo's store. Payloads start from documents the repo tracks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from conftest import REPO, WRITER
from writing import a_valid_edge, an_atom, front_matter, page_items, relation_type_file, tracked

EDGE_PENDING = "edge_validation_before_write"


def apply(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Propose `changes` and apply the proposal exactly as it came back."""
    return session.call("apply_changes", proposal=session.call("propose_changes", changes=changes)["proposal"])


def applied(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    answer = apply(session, changes)
    assert answer["applied"] is True, answer
    return answer


def signed_by_the_writer(answer: dict[str, Any], write_copy: Path, via: str) -> None:
    """Every document written carries who wrote it and through which operation, in the answer and on disk."""
    for document in answer["documents"]:
        assert document["provenance"]["by"] == WRITER and document["provenance"]["via"] == via, document
        on_disk = front_matter(write_copy / document["path"])["sldb"]
        assert on_disk["by"] == WRITER and on_disk["via"] == via, (document["path"], on_disk)


def test_cycle_on_a_document(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    name = "atom-ir04-cycle"
    payload = {**atom["payload"], "id": name, "title": "IR04: el ciclo proponer, validar y aplicar"}
    created = applied(writer, [{"action": "create", "model": atom["model"], "name": name, "payload": payload, "path": f"desk/atoms/{name}.md"}])
    export_id = f"{atom['model']}:{name}"
    assert [d["export_id"] for d in created["documents"]] == [export_id]
    signed_by_the_writer(created, write_copy, "create_document")
    read = writer.call("read_document", ref=export_id)
    assert read["found"] and read["payload"] == payload

    updated = applied(writer, [{"action": "update", "model": atom["model"], "name": name, "fields": {"title": payload["title"] + " (editado)"}}])
    signed_by_the_writer(updated, write_copy, "save_document_payload")
    assert writer.call("read_document", ref=export_id, field="title")["value"] == payload["title"] + " (editado)"

    deleted = applied(writer, [{"action": "delete", "model": atom["model"], "name": name}])
    assert deleted["deleted"] == [read["address"]] and deleted["documents"] == []
    assert writer.call("read_document", ref=export_id)["found"] is False
    assert not (write_copy / read["path"]).exists()


def test_cycle_on_an_edge(writer, write_copy: Path) -> None:
    edge = a_valid_edge("ir04-cycle-edge")
    source, target = (writer.call("read_document", ref=edge[end])["address"] for end in ("source", "target"))

    def targets() -> set[str]:
        return {e["target"] for e in page_items(writer, "neighbors", node=edge["source"], direction="outgoing", relation=edge["relation_type"])}

    assert target not in targets(), "the edge exists already; it would prove nothing"
    asserted = applied(writer, [edge])
    assert asserted["edge_findings"] == [], asserted["edge_findings"]
    signed_by_the_writer(asserted, write_copy, "create_document")
    assert target in targets()
    stored = writer.call("read_document", ref="RelationDoc:ir04-cycle-edge")["payload"]
    assert (stored["source_id"], stored["target_id"], stored["relation_type"]) == (edge["source"], edge["target"], edge["relation_type"])

    applied(writer, [{"action": "retract_edge", "name": "ir04-cycle-edge"}])
    assert target not in targets() and source
    assert not (write_copy / edge["path"]).exists()


def test_a_change_to_a_store_that_moved_since_the_proposal_is_rejected(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    first = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: primera propuesta"}}])
    second = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: segunda propuesta"}}])
    assert writer.call("apply_changes", proposal=second["proposal"])["applied"] is True
    stale = writer.call("apply_changes", proposal=first["proposal"])
    assert stale["applied"] is False and stale["rejected"] == "stale" and stale["document"] == atom["name"]
    assert "changed" in stale["explanation"]
    assert front_matter(write_copy / atom["path"])["title"] == "IR04: segunda propuesta"


def test_an_edited_proposal_is_refused(writer) -> None:
    atom = an_atom(writer)
    proposal = writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "IR04: sellada"}}])["proposal"]
    proposal["changes"][0]["expected_source_hash"] = None
    assert "propose it again" in writer.error_of("apply_changes", proposal=proposal)


def a_rule(writer, name: str, **fields: Any) -> dict[str, Any]:
    """A RuleDoc change: the repo's first RuleDoc, under a new name with `fields`."""
    rule = tracked(writer, sorted((REPO / "desk" / "lifecycle").glob("rule-*.md"))[0])
    return {"action": "create", "model": "RuleDoc", "name": name, "payload": {**rule["payload"], **fields}, "path": f"desk/lifecycle/{name}.md"}


def test_an_error_rule_refuses_the_change_and_is_named(writer, write_copy: Path) -> None:
    rule = a_rule(writer, "rule-ir04-edges-explain-themselves", title="IR04: an authored edge explains itself", subject="model <= RelationDoc", where="", condition="nonempty(notes)", severity="error", moment="on_write", message="An authored edge explains itself in its notes.")
    applied(writer, [rule])
    try:
        silent = {**a_valid_edge("ir04-edge-without-notes"), "notes": ""}
        refused = apply(writer, [silent])
        assert refused["applied"] is False and refused["rejected"] == "rules"
        assert refused["rules"] == [f"rules/{rule['name']}"] and rule["name"] in refused["explanation"]
        assert refused["findings"][0]["level"] == "error" and refused["findings"][0]["subject"] == "RelationDoc:ir04-edge-without-notes"
        assert not (write_copy / silent["path"]).exists()
    finally:
        applied(writer, [{"action": "delete", "model": "RuleDoc", "name": rule["name"]}])


def test_an_alert_rule_is_reported_by_name(writer) -> None:
    rules = [p for p in (REPO / "desk" / "lifecycle").glob("rule-*.md") if front_matter(p).get("moment") == "on_write" and front_matter(p).get("severity") == "alert" and "pills" in front_matter(p)["condition"]]
    assert rules, "the repo declares no on_write alert about pills"
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("pills")))
    answer = applied(writer, [{"action": "update", "model": task["model"], "name": task["name"], "fields": {"references": []}}])
    codes = {a["code"] for a in answer["alerts"] if a["subject"] == task["export_id"]}
    assert {f"rules/{tracked(writer, p)['name']}" for p in rules} <= codes, answer["alerts"]


def test_an_edge_against_its_relation_type_is_reported(writer) -> None:
    edge = a_valid_edge("ir04-edge-wrong-source")
    allowed = front_matter(relation_type_file(edge["relation_type"]))["source_types"]
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("task_type")))
    assert task["model"] not in allowed
    wrong = {**edge, "source": task["export_id"]}
    proposal = writer.call("propose_changes", changes=[wrong])
    assert any(p["note"].startswith("sldb:") for p in proposal["pending"] if EDGE_PENDING in p["what"] or "RelationTypeDoc" in p["what"])
    answer = writer.call("apply_changes", proposal=proposal["proposal"])
    try:
        assert answer["applied"] is True
        assert any("source_types" in f and task["export_id"] in f for f in answer["edge_findings"]), answer["edge_findings"]
    finally:
        applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])


def test_cardinality_and_condition_of_a_declared_type_are_reported(writer) -> None:
    base = tracked(writer, relation_type_file(a_valid_edge("x")["relation_type"]))
    name = "ir04_one_to_one"
    declared = {"action": "create", "model": "RelationTypeDoc", "name": f"type-{name}", "path": f"desk/lifecycle/type-{name}.md", "payload": {**base["payload"], "name": name, "title": "IR04 one to one", "cardinality": "one_to_one", "target_types": []}}
    applied(writer, [declared])
    first, second = a_valid_edge("ir04-card-1"), a_valid_edge("ir04-card-2")
    # Two targets for one source under a one_to_one type, the second with a condition that does not parse.
    edges = [{**first, "relation_type": name}, {**second, "relation_type": name, "target": first["source"], "condition": "status = "}]
    try:
        findings = applied(writer, edges)["edge_findings"]
        assert any(f"has 2 '{name}' targets but cardinality is one_to_one" in f for f in findings), findings
        assert any("condition does not parse" in f for f in findings), findings
    finally:
        applied(writer, [{"action": "retract_edge", "name": e["name"]} for e in edges] + [{"action": "delete", "model": "RelationTypeDoc", "name": f"type-{name}"}])


@pytest.mark.xfail(strict=True, reason="SLDB checks an edge against its RelationTypeDoc only after the write (check_edges); asked by note, see PENDING['edge_validation_before_write']")
def test_an_edge_against_its_relation_type_is_refused_before_writing(writer, write_copy: Path) -> None:
    edge = a_valid_edge("ir04-edge-refused")
    task = tracked(writer, next(p for p in sorted((REPO / "desk" / "tasks").glob("task-*.md")) if front_matter(p).get("task_type")))
    wrong = {**edge, "source": task["export_id"]}
    answer = apply(writer, [wrong])
    try:
        assert answer["applied"] is False and not (write_copy / wrong["path"]).exists()
    finally:
        if answer["applied"]:
            applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])

FILE:tests/mcp/test_dry_run.py
"""The dry run: `propose_changes` answers what would be written and changes no file."""

from __future__ import annotations

from pathlib import Path

from conftest import copy_digest
from writing import a_valid_edge, an_atom, lifecycle_edges, tracked


def test_a_dry_run_answers_what_would_be_written_and_writes_nothing(writer, write_copy: Path) -> None:
    atom = an_atom(writer)
    created = {**atom["payload"], "id": "atom-ir04-dry-run", "title": "IR04 dry run"}
    retracted = tracked(writer, lifecycle_edges()[-1])
    changes = [
        {"action": "create", "model": atom["model"], "name": "atom-ir04-dry-run", "payload": created, "path": "desk/atoms/atom-ir04-dry-run.md"},
        {"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": atom["payload"]["title"] + " (IR04)"}},
        a_valid_edge("ir04-dry-run-edge"),
        {"action": "retract_edge", "name": retracted["name"]},
    ]
    before = copy_digest(write_copy)
    answer = writer.call("propose_changes", changes=changes)
    assert copy_digest(write_copy) == before, "the dry run changed a file"
    assert answer["dry_run"] is True and answer["written"] is False

    would = {w["export_id"]: w for w in answer["would_write"]}
    assert set(would) == {f"{atom['model']}:atom-ir04-dry-run", atom["export_id"], "RelationDoc:ir04-dry-run-edge", retracted["export_id"]}
    assert would[f"{atom['model']}:atom-ir04-dry-run"]["payload"] == created
    update = would[atom["export_id"]]
    assert update["action"] == "update" and update["changed_fields"] == ["title"] and update["path"] == atom["path"]
    assert update["payload"] == {**atom["payload"], "title": atom["payload"]["title"] + " (IR04)"}
    edge = would["RelationDoc:ir04-dry-run-edge"]["payload"]
    asserted = a_valid_edge("ir04-dry-run-edge")
    assert (edge["source_id"], edge["target_id"], edge["relation_type"]) == (asserted["source"], asserted["target"], asserted["relation_type"])
    assert would[retracted["export_id"]]["action"] == "delete" and would[retracted["export_id"]]["path"] == retracted["path"]

    batch = {c["id"]: c for c in answer["proposal"]["changes"]}
    for name in (atom["name"], retracted["name"]):
        assert batch[name]["expected_source_hash"], f"the server filled no guard for {name}"
    assert not (write_copy / "desk/atoms/atom-ir04-dry-run.md").exists()
    assert not (write_copy / "desk/lifecycle/ir04-dry-run-edge.md").exists()
    assert (write_copy / retracted["path"]).is_file()
    assert any(p["note"].startswith("sldb:") and "dry run" in p["what"] for p in answer["pending"]), "the missing SLDB dry run is not declared"

FILE:tests/mcp/test_mutability.py
"""The write level is the server's: a call above it fails before anything is evaluated; the
write tools take typed arguments only; no tool writes a Python module."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import copy_digest
from writing import an_atom

READ_TOOLS = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "check_integrity",
}
WRITE_TOOLS = {"propose_changes", "apply_changes"}
#: A change on a rule document that names nothing the store has: evaluating it at all would
#: answer "not registered" or "not a document", not the level.
RULE_CHANGES = [
    {"action": "update", "model": "RuleDoc", "name": "no-such-rule-ir04", "fields": {"severity": "error"}},
    {"action": "create", "model": "RelationTypeDoc", "name": "no-such-type-ir04", "payload": {}},
]


def test_level_0_serves_no_write_tool(mcp) -> None:
    assert {t.name for t in mcp.list_tools()} == READ_TOOLS
    assert "propose_changes" in mcp.error_of("propose_changes", changes=RULE_CHANGES[:1])


def test_level_1_refuses_rules_before_evaluating_anything(content_writer, write_copy: Path) -> None:
    assert {t.name for t in content_writer.list_tools()} == READ_TOOLS | WRITE_TOOLS
    before = copy_digest(write_copy)
    for change in RULE_CHANGES:
        error = content_writer.error_of("propose_changes", changes=[change])
        assert "LevelError" in error and "write level 2" in error and "level 1" in error, error
        assert "register" not in error and "not a document" not in error, error
    assert copy_digest(write_copy) == before


def test_level_1_refuses_to_apply_a_rules_proposal(writer, content_writer) -> None:
    atom = an_atom(writer)
    proposal = writer.call("propose_changes", changes=[
        {"action": "create", "model": "RuleDoc", "name": "rule-ir04-level", "payload": {"title": "x", "subject": f"model <= {atom['model']}", "condition": "true", "severity": "alert", "moment": "on_write", "message": ""}, "path": "desk/lifecycle/rule-ir04-level.md"},
    ])["proposal"]
    assert proposal["level"] == 2
    error = content_writer.error_of("apply_changes", proposal=proposal)
    assert "LevelError" in error and "write level 2" in error, error


def test_level_1_writes_content(content_writer) -> None:
    atom = an_atom(content_writer)
    answer = content_writer.call("propose_changes", changes=[{"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": atom["payload"]["title"]}}])
    assert answer["proposal"]["level"] == 1


def test_models_as_code_are_never_served(write_copy: Path) -> None:
    done = subprocess.run([sys.executable, "-m", "specir.mcp.server", "--store", str(write_copy / ".sldb"), "--level", "3"], capture_output=True, text=True, timeout=120)
    assert done.returncode == 2 and "--level" in done.stderr, done.stderr


def test_no_tool_writes_a_python_module(writer, write_copy: Path) -> None:
    assert {t.name for t in writer.list_tools()} == READ_TOOLS | WRITE_TOOLS
    atom = an_atom(writer)
    error = writer.error_of("propose_changes", changes=[{"action": "create", "model": atom["model"], "name": "atom-ir04-module", "payload": atom["payload"], "path": "src/specir/ir04_module.py"}])
    assert "not a Markdown document" in error
    assert not (write_copy / "src").exists()


def test_write_tools_take_typed_arguments_only(writer) -> None:
    schema = next(t for t in writer.list_tools() if t.name == "propose_changes").input_schema
    variants = schema["$defs"]
    actions = set()
    for name in ("CreateDocument", "UpdateDocument", "DeleteDocument", "AssertEdge", "RetractEdge"):
        assert variants[name]["additionalProperties"] is False, name
        actions.add(variants[name]["properties"]["action"]["const"])
    assert actions == {"create", "update", "delete", "assert_edge", "retract_edge"}
    atom = an_atom(writer)
    for change in (
        {"action": "make the atom say something nicer", "model": atom["model"], "name": atom["name"]},
        {"action": "update", "model": atom["model"], "name": atom["name"], "fields": {"title": "x"}, "instructions": "and fix its tags"},
        "update the atom's title",
    ):
        assert "validation error" in writer.error_of("propose_changes", changes=[change]).lower(), change

FILE:instruccion
Cold-bundle de la tarea task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Una ejecución en seco devuelve lo que se escribiría y no cambia ningún archivo del store.
- Aplicar un cambio validado sobre un store que cambió después de la validación es rechazado con un error que lo dice.
- Una arista que viola los tipos de origen o destino, la cardinalidad o la condición de su RelationTypeDoc es rechazada antes de escribir.
- Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad de la regla, y la respuesta nombra la regla.
- Ninguna tool de escritura recibe texto libre para interpretar: solo argumentos tipados.
- Cada documento escrito lleva en su procedencia quién y por qué operación se escribió.
- Una tool por encima del nivel de escritura permitido responde error sin evaluar nada.
- No existe ninguna tool que cree o modifique módulos Python.

