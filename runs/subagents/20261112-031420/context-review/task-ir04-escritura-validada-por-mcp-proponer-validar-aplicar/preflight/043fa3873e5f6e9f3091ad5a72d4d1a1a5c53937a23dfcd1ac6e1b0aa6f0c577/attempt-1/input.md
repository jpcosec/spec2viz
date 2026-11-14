FILE:desk/tasks/task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:17Z'
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

Dentro, mutaciones del store que expone el MCP: crear, editar y borrar documentos de modelos ya registrados; afirmar y retirar aristas (RelationDoc); declarar y editar tipos de relación (RelationTypeDoc) y reglas (RuleDoc), que son documentos del store y por eso se escriben como datos. Toda escritura admite ejecución en seco. Fuera: crear o editar clases Python de modelos por MCP. Las clases de modelo se definen como código en el paquete specIR (o en el paquete del proyecto que las declare) y entran al store por el registro de modelos de SLDB; exponer su edición por MCP queda como decisión posterior, condicionada a la tarea de contrato de escritura. Fuera también: síntesis de código de aplicación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las tools envuelven las operaciones de escritura, prevalidación, reglas y transiciones que la matriz de auditoría marca como existentes en la API pública de SLDB; lo que falte se resuelve en SLDB, no en specIR.

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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

