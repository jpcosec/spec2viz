FILE:desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
---
sldb:
  by: agent
  at: '2026-11-17T14:08:19Z'
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

Esperar a que cierre el espejo task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión. Después, escribir las pruebas en un archivo de prueba nuevo bajo tests/, dedicado al deshacer, usando los fixtures de tests/conftest.py (mount_copy, store_copy y la sesión mcp) contra el sldb mcp real. Sin mocks. La única lógica nueva en specIR, si hace falta, es la que su extensión necesite para que el deshacer pase por sus validadores; ni inversión ni guardas.

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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

