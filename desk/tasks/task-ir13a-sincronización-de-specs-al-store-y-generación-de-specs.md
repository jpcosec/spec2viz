---
sldb:
  by: agent
  at: '2026-11-12T01:25:43Z'
  authority: generated
  via: save_document_payload
id: task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
- task-ir11-compiladores-y-proyecciones-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/sync.py
- src/specir/visual/graph_import.py
- src/specir/visual/generate_python.py
- tests/visual/test_sync.py
- tests/visual/test_graph_import.py
- tests/visual/test_generate_python.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13a Sincronización de specs al store y generación de specs

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. La sincronización es lo que conecta un diagrama autorado con el grafo de SLDB, y las dos formas de generar un spec (desde el grafo y desde el AST de Python) son las que usan hoy los repos para documentar su arquitectura.

## Goal

_Describe the concrete result this task must produce._

specIR materializa un spec en el store y genera specs de componentes desde un grafo y desde código Python, con el mismo resultado que spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: sincronización de un spec al store como SpecDoc, SpecNodeDoc y RelationDoc, con creación del RelationTypeDoc que falte y borrado de los documentos que salieron del spec; compilación de un grafo de store o de un snapshot a un spec de componentes; generación de un spec de componentes desde el AST de Python. Cada pieza se migra tal cual o se reemplaza, según el modo que le asigne la matriz de cobertura.
Fuera: catálogos; notaciones y paletas; CLI; migración de consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulos src/specir/visual/sync.py, graph_import.py y generate_python.py sobre los modelos y compiladores de la tarea de compiladores, escribiendo por la API pública de SLDB. Paridad medida portando a tests/visual/ las pruebas de spec2viz de sincronización, importación de grafo y generación desde AST.

## Validation

_List the checks required before this task can close._

- Sincronizar un spec con specIR deja en un store de prueba los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización.
- Volver a sincronizar tras quitar un elemento del spec borra su SpecNodeDoc y sus RelationDoc.
- Una relación de tipo no builtin crea su RelationTypeDoc y el índice de aristas valida después de sincronizar.
- La compilación desde grafo produce, sobre el fixture de snapshot de spec2viz, un spec de componentes que valida y es equivalente al de spec2viz, o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz.
- La generación desde AST produce, sobre un paquete Python de fixture, un spec de componentes equivalente al de spec2viz.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de sincronización, importación de grafo y generación de la matriz de cobertura tienen su condición de retiro cumplida.
