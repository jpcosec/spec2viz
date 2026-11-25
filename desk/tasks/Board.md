---
sldb:
  by: agent
  at: '2026-11-25T21:21:29Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de.md
- desk/tasks/task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid.md
- desk/tasks/task-specir-impact-entrega-para-los-archivos-de-un-cambio-las-decisiones-pills-y-tareas-que-apuntan-a-lo.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb
tags: []
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

- un invariante entre piezas se escribe como regla sobre los nodos de specIR, y la regla "graph_ui no depende de pron" falla cuando el código la viola [draft] - Un tipo de relación de dependencia entre piezas, extraído del código, y la posibilidad de prohibir una dependencia con una regla sembrada.
- una capacidad del dominio declara para quién es y cuál es su prueba de aceptación, y las ocho capacidades de specIR quedan cargadas así en su store [draft] - Que una capacidad sea un nodo de specIR con destinatario y con su prueba de aceptación enlazada, y que una regla exija esa prueba.
- specir impact entrega, para los archivos de un cambio, las decisiones, pills y tareas que apuntan a lo afectado [draft] - Que el impacto de un cambio incluya los documentos de otros stores que apuntan a los nodos afectados, con la vía por la que llega cada uno.
