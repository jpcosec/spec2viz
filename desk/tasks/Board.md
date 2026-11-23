---
sldb:
  by: agent
  at: '2026-11-23T18:03:09Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar.md
- desk/tasks/task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo.md
- desk/tasks/task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita.md
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

Estado al 2026-11-21 (09:40 UTC): IR13, gate de retiro de spec2viz. specir retirement check (con --path de deskops, UIs/graph_ui, pron, sldb y spec2viz/.sldb) da 0 dependencias en sldb, deskops, pron, graph_ui e IR. Quedan 19 en el store spec2viz/.sldb (G5) y la fila SV-A17, que depende de él. Cerradas hoy: filas de validate (3d0a436, closeout 9c343b9) y oráculos de paridad congelados en goldens (c47111d, closeout 3bbc758); el script de grabación quedó en /mnt/ssd/proyectos/SLDB_1/reports/spec2viz-goldens/. Espera a JP la task.decision 'JP decide: declarar el retiro de spec2viz, sacar spec2viz/.sldb del universo del comprobador y archivar el repo' (acta, puntos 2 y 8, más la declaración).

## Task Details

_Generated from the task references above._

- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- JP decide: declarar el retiro de spec2viz, sacar spec2viz/.sldb del universo del comprobador y archivar el repo spec2viz [draft] - JP confirma (o cambia) tres cosas. 1) Sacar spec2viz/.sldb del inventario de la matriz (el universo del comprobador) y acreditar SV-A17 con G5, para que specir retirement check dé rc 0. 2) Hacer los cambios del momento del retiro (acta, punto 8): BPMN con exporter='specir' y targetNamespace de specir, clave de localStorage del catálogo de specir con migración de spec2viz.catalog.annotations.v1, y goldens nuevos. 3) Declarar el retiro en docs/spec2viz/acta-de-retiro.md y archivar el repo spec2viz (GitHub archive y su desk). Con la confirmación, 1 y 2 se despachan como tareas de IR (IR13), y 3 lo hace quien JP diga.
- Cambios del momento del retiro de spec2viz: BPMN con exporter y targetNamespace de specir, clave de localStorage del catalogo de specir con migracion y goldens nuevos [draft] - El BPMN que emite specir lleva exporter='specir' y un targetNamespace de specir; la pagina del catalogo usa una clave de localStorage de specir y migra al cargar las anotaciones guardadas con spec2viz.catalog.annotations.v1 (sin perderlas y sin volver a escribir la clave vieja); los goldens afectados se regeneran con el comando del repo y quedan revisados en el diff.
- specir retirement check da rc 0: spec2viz/.sldb sale del inventario de la matriz y SV-A17 se acredita con G5 opcion A [draft] - specir retirement check (con los --path de deskops, UIs/graph_ui, pron, sldb y el resto del universo, sin spec2viz/.sldb) sale con rc 0; docs/spec2viz/matriz-de-cobertura.md acredita SV-A17 citando G5 opcion A (16-nov) y el acta registra el punto 2 hecho con fecha y commit.
