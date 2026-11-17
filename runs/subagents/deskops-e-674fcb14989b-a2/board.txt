---
sldb:
  by: agent
  at: '2026-11-17T15:55:42Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir09-extractor-estático-react-tsx-y-contratos-de-api.md
- desk/tasks/task-ir10-reglas-semánticas-y-análisis-de-impacto.md
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
- desk/tasks/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# IR Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for IR.

## Notes

_Add short operational notes about the current routed set._

Diecisiete tareas de specIR autoradas desde el drawer, todas en borrador: ninguna se ha ejecutado. Dos ramas: MCP y modelado (IR01 a IR06, IR08 a IR10) y cobertura y retiro de spec2viz (IR07, IR11, IR12, IR13a a IR13d, IR13). Las dependencias están en el campo depends_on de cada tarea.

## Task Details

_Generated from the task references above._

- IR09 Extractor estático React/TSX y contratos de API [draft] - Un mapeo de dominio que, sobre los facts genéricos que sldb.api.code.code_facts da del frontend (TS, TSX, JS y JSX: attrs.calls con name canónico, first_arg y canonical, y attrs.handlers con element, attribute y handler), produce los elementos de interfaz del grafo de specIR (InterfaceControlDoc, InterfaceActionDoc) y los vincula con triggers e invokes a las operaciones de API que ya hay en el grafo, con anclas por fact. Reparto acordado con sldb (nota 211648 y C3 TS en 0590ed11/3b3c51fe): sldb publica la sintaxis de forma genérica y specIR interpreta React, fetch y axios sobre esos hechos. specIR no lee código.
- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb [draft] - Verificar desde specIR, con un cliente MCP real sobre sldb mcp y la extensión de dominio de specIR montada, que el undo_changes que sirve sldb mcp deshace los últimos lotes de la sesión, incluidos los que pasan por los validadores de dominio de specIR. sldb decidió (nota de inbox 20261116-232335) que undo_changes y la pila de lotes inversos por sesión son de sldb mcp. specIR no registra la tool ni guarda la pila.
- specir.extract obtiene el source_hash por sldb.api en vez de leer los bytes del fuente (D1 del tester de IR08) [draft] - Que specir.extract compruebe que el ancla corresponde al fact sin leer ningún archivo fuente: el source_hash sale de sldb.api (por ejemplo, un code_facts de la ruta justo antes de escribir, comparado con el fact del plan), o se pide a sldb que record_anchor lo devuelva.
