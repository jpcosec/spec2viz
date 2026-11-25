---
sldb:
  by: agent
  at: '2026-11-25T22:49:14Z'
  authority: generated
  via: create_document
id: task-el-diccionario-de-controles-de-sldb-surface-sale-de-specir-extract-con-el-localizador-de-cada-contro
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# el diccionario de controles de sldb/surface sale de specir extract con el localizador de cada control, y una corrida de Playwright dice cuáles encuentra en la página

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo E3, y desk/drawer/plans/graph-ui-diccionario-de-componentes/ (decisiones D2 a D6, que siguen vigentes). JP decidió probarlo sobre sldb/surface (React 18 con TSX y build), sin esperar la migración de graph_ui. A InterfaceControlDoc le falta cómo encontrar el control en la página, que es lo que una prueba necesita.

## Goal

_Describe the concrete result this task must produce._

Que de una interfaz real salga la lista de sus controles con cómo ubicarlos, y que se pueda comprobar contra la página corriendo.

## Scope

_State what is in scope and what is out of scope._

Dentro: el localizador en InterfaceControlDoc (data-testid, nombre accesible y rol); el mapeo en extract/; un chequeo que abre la página y marca cada control como encontrado o no, guardando el resultado en el campo de verificación. Fuera: escribir pruebas de flujo, tocar sldb/surface, y sacar del código lo que sldb no entrega.

## Implementation Path

_Outline the expected implementation route or affected surface._

El localizador depende de un hecho que sldb todavía no da: los atributos estáticos del elemento que tiene el handler (tarea en borrador en el desk de sldb). Verificar primero si ya está. Si no, esta tarea entrega el campo, el mapeo probado sobre un fixture con ese hecho y el chequeo, y deja dicho cuántos controles de sldb/surface quedan sin localizador. No leer los archivos TSX desde specIR para suplirlo. Los datos van en el store del proyecto probado.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/extract/test_control_locator.py
- python -m pytest -q tests/extract/test_control_check_playwright.py

## Done When

_Name the observable condition that makes the task complete._

specir ux extract sobre sldb/surface escribe los controles sin error y el informe dice cuántos tienen localizador y cuántos no. El chequeo, contra la página de surface levantada, deja cada control con localizador como verificado o refutado, y no toca los que no tienen. Un control cuyo localizador no existe en la página queda refutado.
