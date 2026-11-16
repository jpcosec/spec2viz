---
sldb:
  by: agent
  at: '2026-11-16T05:05:16Z'
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
references: []
depends_on:
- task-espejo-sldb-sldb-mcp-servidor-mcp-genérico-a
- task-espejo-sldb-apply-batch-devuelve-el-lote-inverso-deshacer
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files: []
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

Una tool MCP undo_changes, montada sobre sldb mcp por el punto de extensión, que deshace los últimos lotes de la sesión reaplicando con sldb.api.apply_batch el lote inverso con guardas que sldb devuelve al aplicar cada uno. Bloqueada hasta que sldb entregue sldb mcp y el lote inverso (tareas espejo de sldb: servidor MCP genérico y lote inverso).

## Scope

_State what is in scope and what is out of scope._

Dentro: la tool undo_changes de dominio sobre sldb mcp, en niveles 1 y 2; reaplicar en orden inverso, con sldb.api.apply_batch, los lotes inversos que sldb devuelve al aplicar cada lote (la pila de la sesión es de sldb mcp); traducir el rechazo de sldb (ConflictError) a stale nombrando el documento. Fuera: construir lotes inversos, calcular guardas o restaurar estado en specIR (es de sldb, decisión de JP 2026-11-15); deshacer entre sesiones; nivel 3. Si sldb no lo entrega, la tarea no se ejecuta: no hay sustituto en specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Esperar a que cierren las tareas espejo del servidor sldb mcp y del lote inverso de apply_batch. Luego registrar undo_changes como extensión de dominio de sldb mcp (build_server con extensions, o --extension modulo:funcion) en el paquete specIR; apply_changes de sldb ya guarda en la sesión el lote inverso. Sin lógica de inversión ni de guardas en specIR, y sin ampliar el servidor MCP propio de specIR, que IR03b retira.

## Validation

_List the checks required before this task can close._

- Con un cliente MCP real sobre una copia montada del store, aplicar un lote de creación, edición y arista y deshacerlo deja la copia idéntica a antes (sha256 de los .md y del store).
- Si un documento del lote cambió después de aplicarlo, el deshacer se rechaza como stale nombrando ese documento y no escribe nada.
- Con nivel 0 la tool no existe; con nivel 1 no deshace un lote que tocó RelationTypeDoc o RuleDoc.
- Una prueba de imports confirma que la reversión pasa solo por sldb.api.apply_batch.

## Done When

_Name the observable condition that makes the task complete._

Un agente por MCP aplica un lote y lo deshace sobre una copia del store real, y el store queda como estaba.
