---
sldb:
  by: agent
  at: '2026-11-21T00:54:59Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir10-reglas-semánticas-y-análisis-de-impacto.md
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
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

Estado al 2026-11-20 (noche): cerradas IR01 a IR09, IR11, IR12, IR13a a IR13j, D1 de IR08 e IR04b (89f8734: deshacer por MCP sobre el lote inverso de sldb, partiendo del trabajo sin commit del intento 2, guardado en runs/subagents/20261120-ir04b-wip/). Queda la tarea de cierre de IR04b (la prueba de identidad compara también el store y no importa módulos internos de sldb), en ejecución. Después, en serie: (2) IR10, sin dependencias abiertas; preflight-2 y bundle-2 aceptados el 2026-11-20 (ya no stale). (3) IR13, gate final de retiro de spec2viz; preflight y bundle nuevos aceptados; va al final porque certifica el conjunto. Inbox en 0. La rama sync/local-20261120 de la sesión de supervisión no se pudo fusionar por CLI (conflicto en el shard del Board); su contenido (dos acks y estas notas) se aplicó con deskops message ack y deskops edit board.

## Task Details

_Generated from the task references above._

- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
