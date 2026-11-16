---
sldb:
  by: agent
  at: '2026-11-16T21:46:54Z'
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
- desk/tasks/task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2.md
- desk/tasks/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a.md
- desk/tasks/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real.md
- desk/tasks/task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4.md
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
- Espejo sldb: readers y facts TSX, TS y SQL (B2) [draft] - Disponer en sldb de los readers y facts de TSX, TS y SQL con anclas sobre tree-sitter, que specIR mapea a su dominio.
- Las pruebas de MCP dejan de federar el store real spec2viz/.sldb (G5, opción A) [draft] - Las pruebas de IR siguen probando la lectura de una spec de un store enlazado a través del servidor MCP, pero contra un store de specs que se construye en un directorio temporal a partir de una fixture que ya está en IR, sin leer ni enlazar ../spec2viz/.sldb.
- Las pruebas MCP de IR federan una copia del store de deskops en vez del real [draft] - La suite completa de IR es reproducible con independencia de lo que hagan otros desks: las pruebas MCP enlazan y digieren una copia del store de deskops tomada al inicio de la sesión, no el store real.
- IR13h Registrar en el acta que deskops ya no depende de spec2viz y actualizar G4 [draft] - El acta registra a deskops como resuelto, con sus commits, y trae una corrida nueva del comprobador. La línea de G4 de la matriz refleja los consumidores que de verdad quedan.
