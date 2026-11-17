---
sldb:
  by: agent
  at: '2026-11-16T23:09:03Z'
  authority: generated
  via: save_document_payload
id: task-ir13i-corregir-en-el-acta-el-estado-de-g5-y-la-fila-de-ir-tras-cerrar-la-federación-de-las-pruebas-m
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
- runs/subagents/deskops-t-fb41c88d0a4a/result-summary.md
depends_on:
- task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13i Corregir en el acta el estado de G5 y la fila de IR tras cerrar la federación de las pruebas MCP

## Rationale

_Explain why this task exists or the business driver behind it._

El ejecutor y el tester de IR13h (runs/subagents/deskops-e-5d20e77cfc47 y deskops-t-fb41c88d0a4a) señalaron que el acta de retiro sigue diciendo que task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a está bloqueada, aunque se cerró en IR (código b16aab7, closeout 4f1e108) después de que deskops quitara su enlace al store de spec2viz (421d6a27, closeout 74ffdb63). También señalaron que la fila de IR en Consumidores todavía menciona la federación de spec2viz/.sldb en tests/conftest.py, que b16aab7 eliminó.

## Goal

_Describe the concrete result this task must produce._

El acta de retiro deja de afirmar cosas que ya no son ciertas sobre G5 y sobre las pruebas de IR.

## Scope

_State what is in scope and what is out of scope._

Dentro, solo en docs/spec2viz/acta-de-retiro.md: (1) la fila G5 del gate deja de listar como pendiente en IR la federación de las pruebas, que pasa a resuelta citando b16aab7 y 4f1e108; sigue pendiente quitar spec2viz/.sldb del universo del comprobador al declarar el retiro y archivar el store con el repo; (2) el punto de G5 de Lo que falta se corrige igual; (3) la fila de IR en Consumidores deja de mencionar la federación de spec2viz/.sldb en tests/conftest.py y conserva el resto (los oráculos de paridad en pruebas). Fuera: la matriz; una corrida nueva del comprobador, porque el recuento no cambia; declarar el retiro; tocar código o pruebas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer el acta completa y los informes de IR13h citados en Why. Para verificar: git merge-base --is-ancestor 4f1e108 HEAD sale con rc 0 en IR, y grep -nE 'spec2viz' tests/conftest.py no muestra ninguna ruta al store real de spec2viz. Si algo falla, no se corrige el acta: se anota y se reporta. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo docs/spec2viz/acta-de-retiro.md.
- grep -n 'bloqueada' docs/spec2viz/acta-de-retiro.md no muestra la tarea de federación como bloqueada.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

La fila G5, el punto de G5 de Lo que falta y la fila de IR en Consumidores describen el estado real: la federación de las pruebas está cerrada y lo que queda de G5 es retirar el store del universo y archivarlo.
