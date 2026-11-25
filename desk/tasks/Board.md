---
sldb:
  by: agent
  at: '2026-11-25T05:28:31Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir.md
- desk/tasks/task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar.md
- desk/tasks/task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash.md
- desk/tasks/task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados.md
- desk/tasks/task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml.md
- desk/tasks/task-decision-de-jp-cual-es-el-localizador-de-un-control-en-el-diccionario-de-componentes.md
- desk/tasks/task-decision-de-jp-hasta-donde-llega-el-uso-del-diccionario-en-pruebas-de-ui.md
- desk/tasks/task-decision-de-jp-donde-vive-el-diccionario-de-componentes.md
- desk/tasks/task-decision-de-jp-donde-vive-la-ui-nueva-de-specir-y-como-comparte-con-la-superficie-de-sldb.md
- desk/tasks/task-decision-de-jp-como-llegan-por-http-los-datos-de-specir-a-su-ui.md
- desk/tasks/task-decision-de-jp-que-pasa-con-la-pagina-generada-de-specir-catalog-build.md
- desk/tasks/task-decision-de-jp-en-que-se-escribe-la-ui-nueva-de-specir.md
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

- Sin marcador parity ni dependencia de spec2viz en las pruebas de IR [active] - La descripcion del marcador parity en pyproject.toml dice lo que hace hoy: compara specIR con los goldens congelados de spec2viz (revision 2de1056) en tests/visual/goldens/, sin necesitar spec2viz. Ninguna prueba se salta por falta de spec2viz.
- Las pruebas de tests/test_mcp_extension.py fallan en el setup: el server MCP cierra la conexion al arrancar sobre la copia del store [draft] - Se identifica por que el server muere al arrancar sobre la copia del store de la sesion (fixtures store_copy y build_deskops_copy de tests/conftest.py) y se corrige la causa, de modo que tests/test_mcp_extension.py pase.
- Los nombres de relacion de specIR quedan acotados a 255 bytes con un resumen con hash [draft] - Que edge_name nunca produzca un nombre de mas de 255 bytes, de forma determinista y estable.
- specir ux extract extrae la interfaz de un arbol y avisa de los archivos saltados [draft] - Un comando de CLI que corre extract_frontend y avisa de los archivos que code_facts salto.
- Las operaciones de API de un backend que no es DRF salen de una tabla de rutas declarada en YAML [draft] - Leer un YAML de rutas declaradas y escribir un ApiOperationDoc por entrada con origen 'declarado', para que extract_frontend pueda enlazar invokes.
- Decision de JP: cual es el localizador de un control en el diccionario de componentes [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: hasta donde llega el uso del diccionario en pruebas de UI [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: donde vive el diccionario de componentes [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: donde vive la UI nueva de specIR y como comparte con la superficie de sldb [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: como llegan por HTTP los datos de specIR a su UI [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: que pasa con la pagina generada de specir catalog build [draft] - Registrar la eleccion de JP y su razon.
- Decision de JP: en que se escribe la UI nueva de specIR [draft] - Registrar la eleccion de JP y su razon.
