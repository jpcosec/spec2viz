---
sldb:
  by: agent
  at: '2026-11-25T01:09:58Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa.md
- desk/tasks/task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir.md
- desk/tasks/task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca.md
- desk/tasks/task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y.md
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

- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- Goldens de la capa visual capturados de spec2viz una sola vez, y las pruebas de paridad pasan a compararse contra esos goldens [draft] - Las salidas de referencia que hoy calcula spec2viz se guardan como goldens versionados bajo tests/visual/goldens/, y las pruebas de paridad comparan specIR contra esos archivos en vez de importar spec2viz.
- Sin marcador parity ni dependencia de spec2viz en las pruebas de IR [draft] - pyproject.toml ya no declara el marcador parity, tests/conftest.py y tests/visual no importan ni nombran spec2viz como dependencia, y el script de captura queda borrado o documentado como historico.
- specir mcp: el punto de entrada propio de specIR levanta el server MCP de sldb con su extension ya cargada [draft] - 'specir mcp --store <ruta> [--level N] [--actor A]' arranca sldb.mcp.server.serve con specir.mcp_extension:register cargada; 'specir mcp --help' lo explica; las tools specir_* aparecen.
- El acta de retiro dice que spec2viz continua como IR en jpcosec/specir (rama legacy con su historia) y marca hecho el punto 9 [draft] - docs/spec2viz/acta-de-retiro.md registra el cambio: spec2viz no queda archivado sino que continua como IR en jpcosec/specir (main = IR, legacy = historia de spec2viz); el punto 9 queda marcado como hecho con esta salvedad, con fecha y la decision de JP.
- Plan: probar UIs con graph_ui como diccionario de componentes y una forma comoda de usar specIR ahi [draft] - Un plan en desk/drawer/plans/graph-ui-diccionario-de-componentes/ que diga: que es el diccionario de componentes (que componente de graph_ui es que nodo de la capa UX de specIR), como se genera (extractor React de specIR sobre graph_ui), como se usa para probar UIs (que prueba lee el diccionario: auto_user_test, flujos, controles esperados), la ergonomia (comando o tool MCP de specIR), y el DAG de tareas chicas con depends_on para implementarlo. Decisiones abiertas como task.decision para JP.
