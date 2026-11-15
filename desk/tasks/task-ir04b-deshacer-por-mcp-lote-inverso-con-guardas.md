---
sldb:
  by: agent
  at: '2026-11-15T15:32:35Z'
  authority: generated
  via: save_document_payload
id: task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
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

# IR04b Deshacer por MCP: lote inverso con guardas

## Rationale

_Explain why this task exists or the business driver behind it._

IR02 decidió (D4) que el deshacer del MCP es un lote inverso con guardas para los últimos lotes de la sesión en niveles 1 y 2, pero IR04 dejó el deshacer fuera de su alcance y ninguna tarea lo cubre.

## Goal

_Describe the concrete result this task must produce._

Una tool MCP de deshacer que, para un lote aplicado en la sesión, construye y aplica su lote inverso con sldb.api.apply_batch, protegido por guardas, y rechaza diciéndolo si el store cambió desde entonces.

## Scope

_State what is in scope and what is out of scope._

Dentro: registrar en memoria de la sesión del servidor el lote aplicado y el estado previo de lo que tocó; tool undo_changes disponible en niveles 1 y 2 que deshace los últimos lotes de la sesión en orden inverso; guardas expected_source_hash sobre el estado posterior al lote; rechazo stale nombrando el documento que cambió. Fuera: deshacer entre sesiones o tras reiniciar el servidor (git queda como historia durable), deshacer de nivel 3, cualquier mecanismo de reversión propio fuera de apply_batch.

## Implementation Path

_Outline the expected implementation route or affected surface._

Ampliar src/specir/mcp/write_tools.py y changes.py de IR04. El lote inverso se arma con las mismas formas tipadas de propose_changes y se aplica con apply_batch; specIR no escribe archivos ni restaura bytes. Si sldb publica un deshacer nativo (nota sldb:20261114-074447, fila 11 de IR01), se usa ese y esta tool queda como adaptador.

## Validation

_List the checks required before this task can close._

- Con un cliente MCP real sobre una copia montada del store, aplicar un lote de creación, edición y arista y deshacerlo deja la copia idéntica a antes (sha256 de los .md y del store).
- Si un documento del lote cambió después de aplicarlo, el deshacer se rechaza como stale nombrando ese documento y no escribe nada.
- Con nivel 0 la tool no existe; con nivel 1 no deshace un lote que tocó RelationTypeDoc o RuleDoc.
- Una prueba de imports confirma que la reversión pasa solo por sldb.api.apply_batch.

## Done When

_Name the observable condition that makes the task complete._

Un agente por MCP aplica un lote y lo deshace sobre una copia del store real, y el store queda como estaba.
