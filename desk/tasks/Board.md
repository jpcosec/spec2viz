---
sldb:
  by: agent
  at: '2026-11-15T15:49:34Z'
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
- desk/tasks/task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro.md
- desk/tasks/task-ir10-reglas-semánticas-y-análisis-de-impacto.md
- desk/tasks/task-ir11-compiladores-y-proyecciones-de-spec2viz.md
- desk/tasks/task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz.md
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs.md
- desk/tasks/task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos.md
- desk/tasks/task-ir13c-notaciones-y-paletas-expuestas-desde-specir.md
- desk/tasks/task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual.md
- desk/tasks/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas.md
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

- IR08 Extractor estático Django/DRF y SQL [draft] - Un extractor estático que, a partir de una aplicación Django REST Framework y su esquema SQL, produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen.
- IR09 Extractor estático React/TSX y contratos de API [draft] - Un extractor estático que, a partir de código React (JSX y TSX) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen.
- IR07 Cobertura completa de spec2viz: matriz, fuente de verdad del diagrama y gate de retiro [draft] - Una matriz de cobertura de todas las capacidades de spec2viz, con modo y condición de retiro por fila; la decisión sobre el papel del YAML de spec frente al grafo; y un gate comprobable de migración y retiro. Es un plan de cobertura: no declara nada como ya migrado.
- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc que detectan brechas entre capas y una operación de análisis de impacto, expuesta por MCP, que devuelve los elementos afectados por un cambio con el camino que lo justifica.
- IR11 Compiladores y proyecciones de spec2viz [draft] - specIR compila todos los tipos de diagrama que compila spec2viz y produce diagramas tanto desde un spec autorado como desde una proyección del grafo, según el contrato decidido en la tarea de cobertura.
- IR12 Renderers, linter y recursos estáticos de spec2viz [draft] - specIR produce todos los formatos de salida de spec2viz a partir de la representación intermedia, con paridad verificable, y distribuye los recursos que esos formatos necesitan.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- IR13a Sincronización de specs al store y generación de specs [draft] - specIR materializa un spec en el store y genera specs de componentes desde un grafo y desde código Python, con el mismo resultado que spec2viz.
- IR13b Catálogos, anotaciones y emparejamiento de átomos [draft] - specIR construye, sincroniza, valida y sirve catálogos de diagramas, con anotaciones y con los átomos emparejados a cada elemento, cubriendo lo que hace spec2viz.
- IR13c Notaciones y paletas expuestas desde specIR [draft] - specIR expone las operaciones de notaciones y paletas de spec2viz delegando en la API pública de SLDB, sin redefinir sus modelos.
- IR13d CLI, API Python y habilidad de agente de la capa visual [draft] - specIR ofrece un comando, una API Python pública y una habilidad de agente que cubren cada entrada pública de spec2viz.
- IR04b Deshacer por MCP: lote inverso con guardas [draft] - Una tool MCP de deshacer que, para un lote aplicado en la sesión, construye y aplica su lote inverso con sldb.api.apply_batch, protegido por guardas, y rechaza diciéndolo si el store cambió desde entonces.
