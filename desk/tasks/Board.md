---
sldb:
  by: agent
  at: '2026-11-25T03:00:25Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir.md
- desk/tasks/task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca.md
- desk/tasks/task-plan-probar-uis-con-graph-ui-como-diccionario-de-componentes-y-una-forma-comoda-de-usar-specir-ahi.md
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

- Sin marcador parity ni dependencia de spec2viz en las pruebas de IR [draft] - La descripcion del marcador parity en pyproject.toml dice lo que hace hoy: compara specIR con los goldens congelados de spec2viz (revision 2de1056) en tests/visual/goldens/, sin necesitar spec2viz. Ninguna prueba se salta por falta de spec2viz.
- specir mcp: el punto de entrada propio de specIR levanta el server MCP de sldb con su extension ya cargada [draft] - 'specir mcp --store <ruta> [--level N] [--actor A]' arranca sldb.mcp.server.serve con specir.mcp_extension:register cargada; 'specir mcp --help' lo explica; las tools specir_* aparecen.
- Plan: probar UIs con graph_ui como diccionario de componentes y una forma comoda de usar specIR ahi [draft] - Un plan en desk/drawer/plans/graph-ui-diccionario-de-componentes/ que diga: que es el diccionario de componentes (que componente de graph_ui es que nodo de la capa UX de specIR), como se genera (extractor React de specIR sobre graph_ui), como se usa para probar UIs (que prueba lee el diccionario: auto_user_test, flujos, controles esperados), la ergonomia (comando o tool MCP de specIR), y el DAG de tareas chicas con depends_on para implementarlo. Decisiones abiertas como task.decision para JP.
