---
sldb:
  by: agent
  at: '2026-11-25T17:50:09Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage.md
- desk/tasks/task-u9-anclajes-muestra-la-fuente-con-lineas-y-el-fragmento-resaltado-el-selector-su-estado-y-los-nodos.md
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

- U5: las notas sobre una receta o un nodo se guardan en el store por POST /save y no en localStorage [draft] - Notas sobre la receta o el nodo, guardadas en el store de sldb (como las anotaciones de spec2viz, pero en el store), con lista, alta y edicion.
- U9: Anclajes muestra la fuente con lineas y el fragmento resaltado, el selector, su estado y los nodos que se apoyan [draft] - La pestana Anclajes: para un CodeAnchorDoc, la fuente con numeros de linea y el fragmento resaltado; a la derecha el selector, el estado (vigente o cambiado) y los nodos y relaciones de specIR que se apoyan en el.
