---
sldb:
  by: agent
  at: '2026-11-15T23:38:51Z'
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
- task-espejo-sldb-specsync-en-sldb-api-notations-d1
- task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- tests/visual/test_sync_generation_parity.py
- tests/test_imports.py
- tests/visual/test_visual_names.py
- src/specir/visual/__init__.py
- docs/spec2viz/matriz-de-cobertura.md
- pyproject.toml
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

specIR sincroniza un spec al store y genera specs de componentes usando lo que migra a sldb: SpecSync (D1), el generador desde un grafo o un snapshot y desde el AST de Python (D2, que cubre B4). specIR queda como adaptador de dominio y verifica la paridad con spec2viz; no reimplementa nada de eso.

## Scope

_State what is in scope and what is out of scope._

Dentro: la entrada de specIR a SpecSync de sldb (D1) y al generador de spec de componentes de sldb (D2, desde grafo, snapshot y AST de Python); la prueba de paridad con spec2viz sobre los fixtures de sincronización, importación de grafo y generación desde AST, portando a specIR solo lo que sldb no traiga ya con sus propias pruebas; la actualización de las filas de la matriz de cobertura con el modo migrado a sldb. Fuera: escribir SpecSync o el generador en specIR (se migran a sldb, tareas espejo D1 y D2); catálogos; notaciones y paletas; CLI; migración de consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin capa propia en specIR (regla de JP: lo genérico es de sldb y specIR no lo envuelve): los flujos de specIR y sus usuarios llaman directamente a sldb.api.notations (SpecSync, sync_spec, component_spec_from_graph, component_spec_from_python, write_component_spec) o a la CLI sldb notations sync --spec y sldb notations from-graph; specir.visual solo documenta ese uso, como ya hace con load_spec y validate_spec. La paridad se mide con pruebas de specIR en tests/visual/test_sync_generation_parity.py que comparan la salida de sldb con la de spec2viz como oráculo de desarrollo (marca parity, omitidas si spec2viz no está instalado): el store de prueba es un store sldb real creado con sldb.api.init_store en tmp_path; los fixtures de sincronización son los specs válidos del corpus de IR11 (tests/visual/fixtures/spec2viz, copia de tests/fixtures de spec2viz en 2de1056) más los specs ARQ y FLOW del módulo de pruebas test_sldb_sync de spec2viz; el snapshot es el node-link del módulo de pruebas test_graph_import de spec2viz; el paquete Python de fixture es el propio src/specir (código real, sin datos fabricados). tests/test_imports.py prueba que specIR no importa spec2viz y no define SpecSync ni generador de spec. Si el resultado de sldb difiere de spec2viz, la diferencia se declara en la matriz (docs/spec2viz/matriz-de-cobertura.md, filas SV-E01, SV-F01 y SV-F02) o se pide el arreglo por el desk de sldb. D1 y D2 son las tareas espejo task-espejo-sldb-specsync-en-sldb-api-notations-d1 y task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2 (B4 es la fila del generador AST en el plan de migración).

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

Las pruebas anteriores pasan, specIR no define su propio SpecSync ni su propio generador de spec y las filas de sincronización, importación de grafo y generación de la matriz de cobertura tienen su condición de retiro cumplida con el modo migrado a sldb.
