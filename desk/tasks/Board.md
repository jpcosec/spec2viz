---
sldb:
  by: agent
  at: '2026-11-17T03:07:04Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir08-extractor-estático-django-drf-y-sql.md
- desk/tasks/task-ir09-extractor-estático-react-tsx-y-contratos-de-api.md
- desk/tasks/task-ir10-reglas-semánticas-y-análisis-de-impacto.md
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
- desk/tasks/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real.md
- desk/tasks/task-espejo-sldb-sldb-api-expone-los-facts-de-código-que-necesitan-los-extractores-c1-c5.md
- desk/tasks/task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión.md
- desk/tasks/task-espejo-sldb-component-spec-from-python-lee-solo-py-regresión-de-b2-que-rompe-2-pruebas-de-ir.md
- desk/tasks/task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s.md
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

- IR08 Extractor estático Django/DRF y SQL [draft] - Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen de una aplicación Django REST Framework y de su esquema SQL (sldb/code y los readers de la tarea espejo B2), produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.
- IR09 Extractor estático React/TSX y contratos de API [draft] - Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen del código del frontend (TypeScript, TSX y JavaScript, React incluido) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.
- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb [draft] - Una tool MCP undo_changes, montada sobre sldb mcp por el punto de extensión, que deshace los últimos lotes de la sesión reaplicando con sldb.api.apply_batch el lote inverso con guardas que sldb devuelve al aplicar cada uno. Bloqueada hasta que sldb entregue sldb mcp y el lote inverso (tareas espejo de sldb: servidor MCP genérico y lote inverso).
- Las pruebas MCP de IR federan una copia del store de deskops en vez del real [draft] - La suite completa de IR es reproducible con independencia de lo que hagan otros desks: las pruebas MCP enlazan y digieren una copia del store de deskops tomada al inicio de la sesión, no el store real.
- Espejo sldb: sldb.api expone los facts de código que necesitan los extractores (C1–C5) [draft] - Que sldb.api exponga los facts de código con sus anclas, span y hash, incluidos los de Django/DRF y las claves del SQL de Postgres, para que specIR mapee sin leer código.
- Espejo sldb: sldb mcp sirve undo_changes con la pila de lotes inversos de la sesión [draft] - Que sldb mcp sirva undo_changes, para que IR04b lo verifique desde specIR.
- Espejo sldb: component_spec_from_python lee solo .py (regresión de B2 que rompe 2 pruebas de IR) [draft] - Que la suite completa de IR vuelva a verde sin exclusiones del lado de IR.
- IR13j La prueba portada de notaciones espera el mensaje de sldb para un diagram_type desconocido y SV-H01 queda acreditada [draft] - El caso de mindmap de test_invalid_notations_are_rejected pasa esperando el mensaje de sldb, sin xfail, y SV-H01 queda acreditada si ese era su único faltante.
