FILE:desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
---
sldb:
  by: agent
  at: '2026-11-17T14:35:02Z'
  authority: generated
  via: save_document_payload
id: task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-232335-suggestion-sldb-responde-ir04b-undo-changes-mensaje-de-notationspec-ir13e-y-regresi-n-de-b2.md
depends_on:
- task-espejo-sldb-sldb-mcp-servidor-mcp-genérico-a
- task-espejo-sldb-apply-batch-devuelve-el-lote-inverso-deshacer
- task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- src/specir/mcp_extension.py
- tests/conftest.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

IR02 decidió (D4) que el deshacer del MCP es un lote inverso con guardas para los últimos lotes de la sesión en niveles 1 y 2, pero IR04 dejó el deshacer fuera de su alcance y ninguna tarea lo cubre.

## Goal

_Describe the concrete result this task must produce._

Verificar desde specIR, con un cliente MCP real sobre sldb mcp y la extensión de dominio de specIR montada, que el undo_changes que sirve sldb mcp deshace los últimos lotes de la sesión, incluidos los que pasan por los validadores de dominio de specIR. sldb decidió (nota de inbox 20261116-232335) que undo_changes y la pila de lotes inversos por sesión son de sldb mcp. specIR no registra la tool ni guarda la pila.

## Scope

_State what is in scope and what is out of scope._

Dentro: pruebas de specIR que, sobre una copia montada del store, aplican lotes por MCP con la extensión de specIR montada y los deshacen con el undo_changes de sldb mcp; comprobar que el store queda como antes, que un lote stale se rechaza sin escribir, y que los niveles 0 y 1 se respetan. Si hace falta algo en la extensión de specIR para que el deshacer pase por sus validadores, se agrega en src/specir/mcp_extension.py. Fuera: registrar undo_changes en specIR, guardar la pila o construir lotes inversos, porque todo eso es de sldb mcp; deshacer entre sesiones; nivel 3. Si sldb mcp no sirve undo_changes, la tarea no se ejecuta.

## Implementation Path

_Outline the expected implementation route or affected surface._

Esperar a que cierre el espejo task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión. Después, escribir las pruebas en un archivo de prueba nuevo bajo tests/, dedicado al deshacer, usando los fixtures de tests/conftest.py (mount_copy, store_copy y la sesión mcp) contra el sldb mcp real. Sin mocks. La única lógica nueva en specIR, si hace falta, es la que su extensión necesite para que el deshacer pase por sus validadores; ni inversión ni guardas. Precisiones (preflight-1 y bundle-1): (a) los tres espejos de depends_on están cerrados (undo_changes en sldb d0ee07a3/02ea724e, en origin). (b) Niveles de sldb mcp, en sldb/src/sldb/mcp/mutability.py: 0 read, 1 content y 2 rules (RelationTypeDoc y RuleDoc); el 3 no se sirve. Se prueban 0, 1 y 2: con 2 se deshace un lote que tocó RelationTypeDoc o RuleDoc. (c) La copia escribible es la de mount_copy de tests/conftest.py, con su sesión MCP de escritura arrancada con el nivel de cada caso; el store_copy de solo lectura no sirve. La huella es tree_digest de la copia. (d) Las tools y respuestas son las de sldb mcp: apply_changes y undo_changes(steps), con rechazo {applied: false, rejected: stale, document, written: false}. Revertir el cambio ajeno es aplicar otro lote que devuelve el documento a su contenido anterior. (e) Hoy src/specir/mcp_extension.py no registra validadores de lote (add_batch_validator): lo que se comprueba es que tras undo_changes el store pasa sldb rules check y sldb edges check, y se deja escrito como aserción y en result-summary.md. Si el deshacer deja reglas rotas, es un hallazgo para sldb. (f) Cuenta como implementación propia una def, una tool registrada o una estructura que guarde lotes; las menciones en docstrings y las llamadas a la tool de sldb no cuentan. (g) La prueba va en un módulo nuevo de la carpeta de pruebas, llamado test_mcp_undo; deskops graph missing se corre desde la raíz de IR.

## Validation

_List the checks required before this task can close._

- Con un cliente MCP real sobre una copia montada del store, aplicar un lote de creación, edición y arista y deshacerlo con undo_changes deja la copia idéntica a antes (sha256 de los .md y del store).
- Si un documento del lote cambió después de aplicarlo, undo_changes responde applied false, rejected stale y document con ese documento, sin escribir nada, y el lote sigue en la pila (un undo_changes posterior, una vez revertido el cambio ajeno, lo deshace).
- Con nivel 0 no hay herramientas de escritura ni undo_changes; con nivel 1 no se deshace un lote que tocó RelationTypeDoc o RuleDoc (si sldb mcp lo permitiera, es un hallazgo para sldb: se registra y la tarea se detiene, no se implementa en specIR).
- Si el lote deshecho pasó por los validadores de dominio de specIR (add_batch_validator), se comprueba qué hace undo_changes con ellos (sldb lo aplica con sldb.api.apply_batch directo) y el resultado queda escrito; si el deshacer deja el store en un estado que esos validadores rechazarían, es un hallazgo para sldb.
- specIR no define undo_changes ni guarda lotes inversos: grep -nE "undo_changes|inverse" src/specir no encuentra una implementación propia.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Un agente por MCP aplica un lote y lo deshace con el undo_changes de sldb mcp, con la extensión de specIR montada, sobre una copia del store real, y el store queda como estaba; specIR no implementa el deshacer.

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

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

FILE:desk/atoms/atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas.md
---
sldb:
  by: agent
  at: '2026-11-17T14:09:44Z'
  authority: generated
  via: save_document_payload
id: atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
title: El deshacer del MCP es un lote inverso con guardas
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# El deshacer del MCP es un lote inverso con guardas

## Answer

El deshacer del MCP lo sirve sldb mcp con su tool undo_changes (sldb d0ee07a3, closeout 02ea724e). Cada apply_changes que se aplica apila su lote inverso, el que devuelve sldb.api.apply_batch, en una pila de la sesión del servidor, en memoria. undo_changes(steps) reaplica esos inversos del más reciente al más antiguo con las guardas expected_source_hash del estado que dejó la aplicación. Si alguien escribió después, responde rejected stale con el documento, no escribe nada y el lote queda en la pila; si no hay nada que deshacer, responde nothing_to_undo. Cubre los últimos lotes de la sesión en niveles 1 y 2; el nivel 3 no se sirve, y la historia durable es git. specIR no registra la tool, no guarda la pila ni construye inversos: con su extensión montada, solo verifica que el deshacer funciona (IR04b). Enmiendas: 2026-11-15 (JP), construir el lote inverso es de sldb; 2026-11-16 (nota de sldb 232335), la pila y la tool también son de sldb mcp.

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

FILE:src/specir/mcp_extension.py
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

FILE:tests/conftest.py
"""Fixtures of the specIR tests: an isolated copy of this repo's real store, mounted with
SLDB's public CLI, and the real MCP server of sldb (`sldb mcp`) with specIR's extension
(`specir.mcp_extension:register`) over stdio, driven by the real MCP client.

Nothing is fabricated: the copy holds this repo's `.sldb/`, `sldb/` and `desk/` as they
are, plus every `runs/subagents/*/run.md` at its own relative path. The store linked as `deskops`
is not the real one: it is a copy of deskops's `.sldb/` and git-tracked files, taken once per
session (`deskops_copy`), with its links to other stores removed (or, where sldb refuses, pointed
at copies of those stores), so other desks writing to deskops during the run neither move the
digest nor are read by the server; it is only read. The store linked as `spec2viz` is not spec2viz's: it is a new sldb store
in a temporary directory, built with `sldb.api` from a spec fixture of this repo
(`spec_store`), and also only read."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parent
COPIED = (".sldb", "sldb", "desk")
#: The store registers RunDocs, which live outside `.sldb/` and `desk/`.
RUN_DOCS = "runs/subagents/*/run.md"
#: The git-tracked files of each store copy, listed once when the copy was made.
TRACKED: dict[Path, list[str]] = {}
#: The spec synced into the temporary specs store (`spec_store`), at the same relative path
#: under that store's project as under the fixture root.
SPEC_FIXTURES = REPO / "tests" / "visual" / "fixtures" / "spec2viz"
SPEC_FIXTURE = "docs/architecture/spec2viz/class-sldb-models.yml"
CACHE = ".sldb_cache"
TOOL_TIMEOUT = 300
#: specIR's tools on the server of sldb (`sldb mcp --extension`).
EXTENSION = "specir.mcp_extension:register"


def tree_digest(*roots: Path) -> dict[str, str]:
    """sha256 of every file under `roots` (caches left out: they are regenerable)."""
    digest: dict[str, str] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file() and CACHE not in path.parts:
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def copy_store_project(source: Path, root: Path) -> Path:
    """Copy a store's project: `<source>/.sldb/` (cache left out) and the files `git ls-files`
    lists in `source`, into `root`; its `.sldb` path. The list is taken once, here."""
    listed = subprocess.run(["git", "-C", str(source), "ls-files", "-z"], check=True, capture_output=True).stdout.decode()
    tracked = [rel for rel in listed.split("\0") if rel]
    shutil.copytree(source / ".sldb", root / ".sldb", ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    for rel in tracked:
        origin = source / rel
        target = root / rel
        if rel.startswith(".sldb/") or CACHE in Path(rel).parts or not (origin.is_file() or origin.is_symlink()):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target, follow_symlinks=False)
    store = root / ".sldb"
    TRACKED[store] = tracked
    return store


def linked_stores(root: Path) -> dict[str, Path]:
    """The stores the store_index of the project at `root` links, by name, resolved from `root`."""
    index = yaml.safe_load((root / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    return {link["name"]: (root / link["path"]).resolve() for link in index.get("stores") or []}


def remove_link(root: Path, name: str) -> subprocess.CompletedProcess:
    """`sldb stores remove <name>` on the store of the project at `root` (sldb refuses it while
    a model there is inherited from that store), then `sldb stores declare --write` so the
    store's declaration (`.sldb/store.yaml`) drops the link too and no rebuild brings it back."""
    sldb_cli = str(Path(sys.executable).with_name("sldb"))
    removed = subprocess.run([sldb_cli, "stores", "remove", name, "--store", ".sldb"], cwd=root, capture_output=True, text=True)
    if removed.returncode != 0:
        return removed
    return subprocess.run([sldb_cli, "stores", "declare", "--write", "--store", ".sldb"], cwd=root, capture_output=True, text=True)


def build_deskops_copy(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A copy of the deskops store, made once, that does not lead out of `<tmp>`: `<tmp>/deskops`
    (`copy_store_project`) with its links removed by `sldb stores remove`. A link sldb refuses to
    remove is served by a copy of that store at `<tmp>/<name>`, so its links back to `../deskops`
    resolve to the copy, and that copy's links leading out of `<tmp>` are removed; if sldb refuses
    that too, the test fails. Its `.sldb` path."""
    source = WORKSPACE / "deskops"
    if not (source / ".sldb" / "core").is_dir():
        pytest.fail(f"the deskops store is missing: {source / '.sldb'}")
    base = tmp_path_factory.mktemp("deskops-copy").resolve()
    root = base / "deskops"
    store = copy_store_project(source, root)
    pending = [root]
    while pending:
        project = pending.pop()
        for name, linked in linked_stores(project).items():
            if linked.is_relative_to(base) and (linked / "core").is_dir():
                continue
            removed = remove_link(project, name)
            if removed.returncode == 0:
                continue
            if project != root:
                pytest.fail(f"sldb refused to remove the link {name} -> {linked} of the copy {project}, which leads out of {base} ({removed.returncode}):\n{removed.stdout}\n{removed.stderr}")
            copied = base / name
            if copied.exists() or not (linked / "core").is_dir():
                pytest.fail(f"sldb refused to remove the link {name} -> {linked} of the deskops copy and it cannot be copied to {copied} ({removed.returncode}):\n{removed.stdout}\n{removed.stderr}")
            copy_store_project(linked.parent, copied)
            if linked_stores(root)[name] != (copied / ".sldb").resolve():
                pytest.fail(f"the link {name} of the deskops copy does not resolve to its copy {copied}")
            pending.append(copied)
    return store


@pytest.fixture(scope="session")
def deskops_copy(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The `.sldb` of the session's copy of the deskops store (`build_deskops_copy`)."""
    return build_deskops_copy(tmp_path_factory)


@pytest.fixture(scope="session")
def federated(deskops_copy: Path) -> dict[str, Path]:
    """The stores linked by alias in every mounted copy, besides the specs store: the deskops copy."""
    return {"deskops": deskops_copy}


def federated_digest(federated: dict[str, Path]) -> dict[str, str]:
    """The linked stores' `.sldb/` trees and the documents they track (the files of each store's
    project that git listed when the copy was made, read in the copy, outside the cache)."""
    digest = tree_digest(*federated.values())
    for store in federated.values():
        root = store.parent
        for rel in TRACKED[store]:
            path = root / rel
            if path.is_file() and path.suffix == ".md" and CACHE not in path.parts:
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def sldb(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run the public `sldb` CLI of this environment; fail the test with its output on error."""
    command = [str(Path(sys.executable).with_name("sldb")), *args]
    done = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        pytest.fail(f"{' '.join(args)} failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
    return done


def spec_store_digest(spec_store: Path) -> dict[str, str]:
    """The specs store's `.sldb/` tree and the documents of its project (not a git repo, so
    every `.md` under it, outside the cache)."""
    digest = tree_digest(spec_store)
    for path in sorted(spec_store.parent.rglob("*.md")):
        if path.is_file() and CACHE not in path.parts:
            digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def build_spec_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A new sldb store, outside any mounted copy, with the SpecDoc of this repo's spec fixture
    synced by `sldb.api` (as tests/visual/test_notations_parity.py does); its `.sldb` path."""
    from sldb.api import init_store
    from sldb.api.notations import SpecSync

    project = tmp_path_factory.mktemp("spec-store")
    spec = project / SPEC_FIXTURE
    spec.parent.mkdir(parents=True)
    shutil.copy2(SPEC_FIXTURES / SPEC_FIXTURE, spec)
    init_store(project)
    store = project / ".sldb"
    SpecSync(store).sync(spec)
    return store


@pytest.fixture(scope="session")
def spec_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The `.sldb` of the temporary specs store linked as `spec2viz` in every mounted copy."""
    return build_spec_store(tmp_path_factory)


@pytest.fixture(scope="session")
def original_digest() -> dict[str, str]:
    """This repo's `.sldb/` and `desk/` before any test ran."""
    return tree_digest(REPO / ".sldb", REPO / "desk")


def mount_copy(tmp_path_factory: pytest.TempPathFactory, name: str, spec_store: Path, federated: dict[str, Path]) -> Path:
    """The project root of a new isolated copy of this repo's store, mounted and checked, with
    the `federated` stores (the deskops copy) and the specs store `spec_store` (as `spec2viz`) linked."""
    for alias, store in federated.items():
        if not (store / "core").is_dir():
            pytest.fail(f"the {alias} store is missing: {store}")
    root = tmp_path_factory.mktemp(name) / "IR"
    root.mkdir()
    for name in COPIED:
        shutil.copytree(REPO / name, root / name, ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    for run_doc in sorted(REPO.glob(RUN_DOCS)):
        target = root / run_doc.relative_to(REPO)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(run_doc, target)
    sldb("stores", "add", str(federated["deskops"]), "--name", "deskops", "--replace", "--store", ".sldb", cwd=root)
    sldb("stores", "add", str(spec_store), "--name", "spec2viz", "--store", ".sldb", cwd=root)
    sldb("stores", "update", "--store", ".sldb", cwd=root)
    sldb("edges", "rebuild", "--store", ".sldb", cwd=root)
    sldb("stores", "check", "--store", ".sldb", cwd=root)
    return root


def copy_digest(root: Path, spec_store: Path, federated: dict[str, Path]) -> dict[str, str]:
    """A mounted copy and the linked stores (the `federated` copies and the specs store), file by file."""
    return {**tree_digest(*(root / name for name in COPIED)), **federated_digest(federated), **spec_store_digest(spec_store)}


@pytest.fixture(scope="session")
def store_copy(tmp_path_factory: pytest.TempPathFactory, original_digest: dict[str, str], spec_store: Path, federated: dict[str, Path]) -> Path:
    """The copy the read tools are served from; nothing writes to it."""
    return mount_copy(tmp_path_factory, "specir-store", spec_store, federated)


class McpSession:
    """The real MCP client, connected over stdio to the real `sldb mcp` server, driven from sync tests."""

    def __init__(self, portal: Any, client: Any) -> None:
        self.portal = portal
        self.client = client

    def list_tools(self) -> list[Any]:
        return self.portal.call(self.client.list_tools).tools

    def call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        """The tool's structured JSON answer; a tool error fails the test with its message."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        if result.is_error:
            pytest.fail(f"{tool}({arguments}) failed: {result.content}")
        return result.structured_content

    def error_of(self, tool: str, **arguments: Any) -> str:
        """The error text of a call that must fail."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        assert result.is_error, f"{tool}({arguments}) did not fail: {result.structured_content}"
        return " ".join(getattr(c, "text", "") for c in result.content)


@pytest.fixture(scope="session")
def copy_digest_before(store_copy: Path, spec_store: Path, federated: dict[str, Path]) -> dict[str, str]:
    """The mounted copy and the linked stores before the server reads them."""
    return copy_digest(store_copy, spec_store, federated)


@contextmanager
def served(root: Path, *options: str) -> Iterator[McpSession]:
    """A session with `python -m sldb mcp --store <root>/.sldb --extension specir.mcp_extension:register
    <options>`, launched by stdio."""
    from anyio.from_thread import start_blocking_portal
    from mcp import Client, StdioServerParameters

    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "sldb", "mcp", "--store", str(root / ".sldb"), "--extension", EXTENSION, *options],
        cwd=str(root),
        env={**os.environ},
    )
    with start_blocking_portal() as portal:
        with portal.wrap_async_context_manager(Client(params, read_timeout_seconds=TOOL_TIMEOUT)) as client:
            yield McpSession(portal, client)


@pytest.fixture(scope="session")
def mcp(store_copy: Path, copy_digest_before: dict[str, str]) -> Iterator[McpSession]:
    """The read-only server (level 0, the default) over the read copy."""
    with served(store_copy) as session:
        yield session


#: Who writes the blog chain (IR06); every node and edge of it must carry it.
BLOG_WRITER = "agent:specir-ir06-blog"


@pytest.fixture(scope="session")
def blog_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A new project with an SLDB store and specIR installed (tests/models/blog.py), empty."""
    from blog import new_blog_project

    return new_blog_project(tmp_path_factory.mktemp("specir-blog") / "blog")


@pytest.fixture(scope="session")
def blog(blog_root: Path) -> Iterator[McpSession]:
    """The server at write level 1 over the blog store, after it wrote the chain of
    tests/fixtures/blog_chain.yaml (its answers in `blog.populated`)."""
    from blog import populate

    with served(blog_root, "--level", "1", "--actor", BLOG_WRITER) as session:
        session.populated = populate(session)
        yield session

FILE:instruccion
Cold-bundle de la tarea task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Con un cliente MCP real sobre una copia montada del store, aplicar un lote de creación, edición y arista y deshacerlo con undo_changes deja la copia idéntica a antes (sha256 de los .md y del store).
- Si un documento del lote cambió después de aplicarlo, undo_changes responde applied false, rejected stale y document con ese documento, sin escribir nada, y el lote sigue en la pila (un undo_changes posterior, una vez revertido el cambio ajeno, lo deshace).
- Con nivel 0 no hay herramientas de escritura ni undo_changes; con nivel 1 no se deshace un lote que tocó RelationTypeDoc o RuleDoc (si sldb mcp lo permitiera, es un hallazgo para sldb: se registra y la tarea se detiene, no se implementa en specIR).
- Si el lote deshecho pasó por los validadores de dominio de specIR (add_batch_validator), se comprueba qué hace undo_changes con ellos (sldb lo aplica con sldb.api.apply_batch directo) y el resultado queda escrito; si el deshacer deja el store en un estado que esos validadores rechazarían, es un hallazgo para sldb.
- specIR no define undo_changes ni guarda lotes inversos: grep -nE "undo_changes|inverse" src/specir no encuentra una implementación propia.
- deskops graph missing --root . sale con rc 0.

