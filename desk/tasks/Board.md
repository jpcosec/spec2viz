---
sldb:
  by: agent
  at: '2026-11-25T23:40:03Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de.md
- desk/tasks/task-specir-impact-entrega-para-los-archivos-de-un-cambio-las-decisiones-pills-y-tareas-que-apuntan-a-lo.md
- desk/tasks/task-se-borra-el-registro-del-retiro-de-spec2viz-src-specir-visual-retirement-py-y-el-comando-specir-reti.md
- desk/tasks/task-specir-install-siembra-la-notacion-bpmn-y-una-actividad-con-particiones-se-resuelve-con-eventos-tare.md
- desk/tasks/task-el-modelo-de-specir-tiene-pantalla-y-navegacion-el-extract-las-llena-en-el-frontend-de-ejemplo-y-la.md
- desk/tasks/task-el-diccionario-de-controles-de-sldb-surface-sale-de-specir-extract-con-el-localizador-de-cada-contro.md
- desk/tasks/task-los-exportes-de-texto-leen-la-vista-que-resuelve-sldb-y-se-borra-la-representacion-paralela-de-speci.md
- desk/tasks/task-se-borran-los-renderers-de-html-de-un-diagrama-de-specir-que-reemplaza-el-modo-lector-del-editor-de.md
- desk/tasks/task-una-entidad-del-dominio-tiene-atributos-y-relaciones-con-otras-entidades-el-extract-las-llena-desde.md
- desk/tasks/task-specir-install-siembra-la-composicion-de-la-pantalla-del-catalogo-como-documento-del-store.md
- desk/tasks/task-se-borran-la-pagina-del-catalogo-de-specir-y-catalogannotationsdoc-que-reemplaza-la-composicion-en-s.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# DAG phases: id, tasks, integration
phases: []
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

- un invariante entre piezas se escribe como regla sobre los nodos de specIR, y la regla "graph_ui no depende de pron" falla cuando el código la viola [active] - Un tipo de relación de dependencia entre piezas, extraído del código, y la posibilidad de prohibir una dependencia con una regla sembrada.
- specir impact entrega, para los archivos de un cambio, las decisiones, pills y tareas que apuntan a lo afectado [draft] - Que el impacto de un cambio incluya los documentos de otros stores que apuntan a los nodos afectados, con la vía por la que llega cada uno.
- se borra el registro del retiro de spec2viz, src/specir/visual/retirement.py y el comando specir retirement [draft] - Que specIR no tenga código ni comandos sobre el retiro de spec2viz.
- specir install siembra la notación BPMN, y una actividad con particiones se resuelve con eventos, tareas, compuertas y carriles sin huecos [draft] - Que un proceso guardado como actividad se vea en el editor de grafo con la notación BPMN, declarada como dato.
- el modelo de specIR tiene pantalla y navegación, el extract las llena en el frontend de ejemplo y la notación IFML las muestra [draft] - Que specIR describa una interfaz como pantallas que contienen controles y acciones que navegan entre pantallas.
- el diccionario de controles de sldb/surface sale de specir extract con el localizador de cada control, y una corrida de Playwright dice cuáles encuentra en la página [draft] - Que de una interfaz real salga la lista de sus controles con cómo ubicarlos, y que se pueda comprobar contra la página corriendo.
- los exportes de texto leen la vista que resuelve sldb, y se borra la representación paralela de specir.visual [draft] - Que haya una sola representación de un diagrama, la vista resuelta de sldb, y que los exportes de texto partan de ella.
- se borran los renderers de HTML de un diagrama de specIR, que reemplaza el modo lector del editor de grafo [draft] - Que el HTML de un diagrama salga solo del editor de grafo.
- una entidad del dominio tiene atributos y relaciones con otras entidades, el extract las llena desde los modelos de Django y la notación ORCA las muestra [draft] - Que specIR describa los objetos de un sistema con sus atributos, sus relaciones y lo que se puede hacer con ellos.
- specir install siembra la composición de la pantalla del catálogo como documento del store [draft] - Que la pantalla del catálogo de specIR exista como dato que surface arma, sin interfaz en specIR.
- se borran la página del catálogo de specIR y CatalogAnnotationsDoc, que reemplaza la composición en surface [draft] - Que el catálogo se vea y se exporte solo desde surface.
