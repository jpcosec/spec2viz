---
sldb:
  by: agent
  at: '2026-11-15T22:20:27Z'
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
- desk/tasks/task-ir11-compiladores-y-proyecciones-de-spec2viz.md
- desk/tasks/task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz.md
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs.md
- desk/tasks/task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos.md
- desk/tasks/task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual.md
- desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
- desk/tasks/task-espejo-sldb-apply-batch-devuelve-el-lote-inverso-deshacer.md
- desk/tasks/task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2.md
- desk/tasks/task-espejo-sldb-graph-path-y-graph-paths-explicados-b3.md
- desk/tasks/task-espejo-sldb-specsync-en-sldb-api-notations-d1.md
- desk/tasks/task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2.md
- desk/tasks/task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4.md
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
- IR09 Extractor estático React/TSX y contratos de API [draft] - Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen de código React (JSX y TSX) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.
- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.
- IR11 Compiladores y proyecciones de spec2viz [draft] - specIR compila todos los tipos de diagrama que compila spec2viz y produce diagramas tanto desde un spec autorado como desde una proyección del grafo, según el contrato decidido en la tarea de cobertura.
- IR12 Renderers, linter y recursos estáticos de spec2viz [draft] - specIR produce todos los formatos de salida de spec2viz a partir de la representación intermedia, con paridad verificable, y distribuye los recursos que esos formatos necesitan.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- IR13a Sincronización de specs al store y generación de specs [draft] - specIR sincroniza un spec al store y genera specs de componentes usando lo que migra a sldb: SpecSync (D1), el generador desde un grafo o un snapshot y desde el AST de Python (D2, que cubre B4). specIR queda como adaptador de dominio y verifica la paridad con spec2viz; no reimplementa nada de eso.
- IR13b Catálogos, anotaciones y emparejamiento de átomos [draft] - specIR construye, sincroniza, valida y sirve catálogos de diagramas con anotaciones, y empareja átomos con elementos de diagrama usando sldb.api.matching (D4); el catálogo se sirve con sldb serve si alcanza. specIR conserva solo la parte visual del catálogo.
- IR13d CLI, API Python y habilidad de agente de la capa visual [draft] - specIR ofrece un comando, una API Python pública y una habilidad de agente que cubren cada entrada pública de spec2viz.
- IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb [draft] - Una tool MCP undo_changes, montada sobre sldb mcp por el punto de extensión, que deshace los últimos lotes de la sesión reaplicando con sldb.api.apply_batch el lote inverso con guardas que sldb devuelve al aplicar cada uno. Bloqueada hasta que sldb entregue sldb mcp y el lote inverso (tareas espejo de sldb: servidor MCP genérico y lote inverso).
- Espejo sldb: apply_batch devuelve el lote inverso (deshacer) [draft] - Disponer en sldb del lote inverso con guardas en el resultado de apply_batch, base del deshacer por MCP.
- Espejo sldb: readers y facts TSX, TS y SQL (B2) [draft] - Disponer en sldb de los readers y facts de TSX, TS y SQL con anclas sobre tree-sitter, que specIR mapea a su dominio.
- Espejo sldb: graph_path y graph_paths explicados (B3) [draft] - Disponer en sldb de caminos explicados en el recorrido del grafo, con la procedencia de cada tramo, para el impacto de specIR.
- Espejo sldb: SpecSync en sldb.api.notations (D1) [draft] - Disponer en sldb de la sincronización de specs al store junto a NotationSync y PaletteSync.
- Espejo sldb: generador de spec desde grafo y AST (D2) [draft] - Disponer en sldb del generador de spec de componentes desde un grafo y desde el AST de Python.
- Espejo sldb: emparejamiento de átomos en sldb.api.matching (D4) [draft] - Disponer en sldb del emparejamiento de átomos con elementos de diagrama, explícito y difuso.
