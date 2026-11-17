---
sldb:
  by: agent
  at: '2026-11-17T13:11:31Z'
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
- desk/tasks/task-espejo-sldb-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-c3-de-ir-parte-ts-js-para-ir09.md
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

- IR08 Extractor estático Django/DRF y SQL [draft] - Un mapeo de dominio que, a partir de los facts genéricos de código que da sldb.api.code.code_facts sobre una aplicación Django REST Framework y su esquema SQL de Postgres, produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen. Reparto acordado con sldb (2026-11-16, nota 211648 y sus 4 tareas): sldb publica la sintaxis de forma genérica (clases con extends y attrs.bases, attrs.decorators con args y kwargs, calls y attrs.calls, kind assignment con attrs.call, attrs.items, attrs.value y attrs.op, kind call, y hechos constraint del SQL) y specIR interpreta Django y DRF sobre esos hechos. specIR no lee código: no escribe readers ni parsers.
- IR09 Extractor estático React/TSX y contratos de API [draft] - Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen del código del frontend (TypeScript, TSX y JavaScript, React incluido) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.
- IR10 Reglas semánticas y análisis de impacto [draft] - Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.
- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb [draft] - Verificar desde specIR, con un cliente MCP real sobre sldb mcp y la extensión de dominio de specIR montada, que el undo_changes que sirve sldb mcp deshace los últimos lotes de la sesión, incluidos los que pasan por los validadores de dominio de specIR. sldb decidió (nota de inbox 20261116-232335) que undo_changes y la pila de lotes inversos por sesión son de sldb mcp. specIR no registra la tool ni guarda la pila.
- Espejo sldb: sldb.code publica facts genéricos de TS, TSX, JS y JSX (C3 de IR, parte TS/JS, para IR09) [draft] - Que sldb.api.code.code_facts dé, para TS, TSX, JS y JSX, las llamadas de cada función, componente o hook (fetch, axios, clientes de API y otros símbolos) con su primer argumento literal, y los atributos JSX que ligan un evento a un handler, para que specIR arme los contratos de API de React sin leer código.
