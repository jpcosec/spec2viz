---
sldb:
  by: agent
  at: '2026-11-21T06:48:01Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac.md
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

Estado al 2026-11-21 (mañana): IR13, gate de retiro de spec2viz. specir retirement check (con --path de deskops, UIs/graph_ui, pron, sldb y spec2viz/.sldb) da 62 dependencias: 43 de IR, que son los oráculos de paridad en tests/visual, y 19 del store spec2viz/.sldb (G5, se archiva con el repo). sldb, deskops, pron y graph_ui ya no cuentan: el gen_golden de sldb se retiró en cfa6477b (sldb origin 64c810b0). Cerrada la tarea de las filas de validate (3d0a436, closeout 9c343b9): SV-K16, K21, K26 y K29 pasan a sldb notations validate y se retiran specir diagram validate y specir validate. Solo queda abierta SV-A17 (G5). En ejecución: la tarea que congela los oráculos de paridad en goldens (acta, punto 6). Después quedan las decisiones de JP: sacar spec2viz/.sldb del universo del comprobador y archivar spec2viz (puntos 2 y 8 del acta), y declarar el retiro.

## Task Details

_Generated from the task references above._

- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- Las pruebas de paridad de IR comparan contra goldens congelados de spec2viz y dejan de importarlo (acta, punto 6) [draft] - Ningún archivo de IR importa ni invoca spec2viz: specir retirement check no lista dependencias de IR. Cada comparación con spec2viz en vivo pasa a comparar contra un golden versionado en tests/visual/goldens/, grabado desde spec2viz (el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz, con su commit en el nombre del archivo, como los spec2viz-2de1056*.json) con un script de grabación que vive fuera de tests/ (en runs/<run>/, que el comprobador no audita), y la prueba carga el golden sin importar spec2viz. Si un caso ya está cubierto por un golden existente, la prueba en vivo se borra. La cobertura de la paridad no baja: los casos que hoy pasan con spec2viz instalado siguen comprobados. tests/test_matriz_cobertura_spec2viz.py deja de importar spec2viz.cli (usa el golden o una lista congelada de comandos).
