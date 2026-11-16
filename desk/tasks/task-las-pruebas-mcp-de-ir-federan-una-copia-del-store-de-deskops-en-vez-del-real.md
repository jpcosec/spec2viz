---
sldb:
  by: agent
  at: '2026-11-16T21:42:49Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real
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
- task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/conftest.py
- tests/test_mcp_extension.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las pruebas MCP de IR federan una copia del store de deskops en vez del real

## Rationale

_Explain why this task exists or the business driver behind it._

tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched digiere el store real de deskops (FEDERATED en tests/conftest.py). Cualquier agente que escriba en deskops mientras corre la suite completa de IR la hace fallar sin relación con la tarea que se prueba. Le pasó tres veces seguidas al tester de IR13g (runs/subagents/deskops-t-e9062210030f, corridas 1 a 3), y antes al de la federación. Así, la suite de IR no da verde mientras deskops trabaja.

## Goal

_Describe the concrete result this task must produce._

La suite completa de IR es reproducible con independencia de lo que hagan otros desks: las pruebas MCP enlazan y digieren una copia del store de deskops tomada al inicio de la sesión, no el store real.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/conftest.py y tests/test_mcp_extension.py. El fixture que enlaza deskops copia su store (y lo que haga falta para que sus enlaces resuelvan) a un directorio temporal de sesión, y la prueba de untouched digiere esa copia. Se conserva la cobertura de leer a través de un store federado. Fuera: cambiar deskops o sldb; la tarea de federación de spec2viz, que ya cambia esos archivos y va primero.

## Implementation Path

_Outline the expected implementation route or affected surface._

Empezar cuando esté integrada task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a, que toca los mismos archivos. Seguir su patrón: build_spec_store construye un store temporal y el digest cubre ese store temporal. Si copiar el store de deskops rompe la resolución de sus enlaces a sldb, pron o scion, se detiene y se reporta.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y sin skipped.
- Con una escritura simulada en una copia desechable del store de deskops durante la prueba, la prueba de untouched sigue pasando, porque no mira el store real.
- Suite completa una vez bajo flock /dev/shm/sldb1-tests.lock con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas MCP de IR no leen ni digieren el store real de deskops y la suite completa da verde aunque deskops escriba durante la corrida.
