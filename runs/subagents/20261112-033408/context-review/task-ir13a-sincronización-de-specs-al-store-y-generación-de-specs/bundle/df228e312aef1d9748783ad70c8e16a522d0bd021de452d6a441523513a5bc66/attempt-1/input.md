FILE:desk/tasks/task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs.md
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

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Cómo se acredita la cobertura de una capacidad de spec2viz.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad de spec2viz se considera cubierta solo cuando la prueba o golden correspondiente de spec2viz pasa contra specIR, o cuando su fila de la matriz de cobertura declara un reemplazo con una prueba equivalente que pasa.

## Why

_Explain why this context matters for safe execution._

El objetivo es retirar spec2viz; declarar paridad sin prueba dejaría funcionalidades perdidas al retirarlo.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre o reemplace una capacidad de spec2viz, y al evaluar el gate de retiro.

## Where

_Name the files, surfaces, or scope this pill applies to._

tests/visual/ en specIR; como referencia de solo lectura, spec2viz/tests/ y la matriz docs/spec2viz/matriz-de-cobertura.md.

## How

_Describe the correct way to apply this guidance._

Portar los fixtures y golden de spec2viz a tests/ de specIR y ejecutarlos; registrar en la matriz, por fila, la prueba que acredita la cobertura.

## How Not

_Describe the shortcut or failure mode to avoid._

No declarar una fila como cubierta porque otra herramienta la sustituya de hecho; no descartar una capacidad por falta de uso; no modificar un golden para que la prueba pase.

FILE:desk/atoms/atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:35Z'
  authority: generated
  via: create_document
id: atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
title: specIR reemplaza a spec2viz y cubre todas sus funciones
five_wh_one_plus: when
tags:
- system:specir
- system:spec2viz
- topic:migracion
---

# specIR reemplaza a spec2viz y cubre todas sus funciones

## Answer

spec2viz nació aparte porque SLDB no tenía grafos; ahora los tiene. specIR incorporará la capa visual y debe cubrir todas las funcionalidades de spec2viz; cuando las cubra, spec2viz se retira. Ninguna funcionalidad se da por descartada porque otra herramienta la sustituya de hecho: cada una se cubre migrándola tal cual, reemplazándola por otra arquitectura o experiencia con resultado equivalente, o exponiendo desde specIR lo que ya vive en SLDB. En los tres casos specIR responde por el camino de retiro. No es un consumidor permanente de spec2viz. Decisión del dueño del proyecto, 2026-11-11.

FILE:desk/atoms/atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:instruccion
Cold-bundle de la tarea task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Sincronizar un spec con specIR deja en un store de prueba los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización.
- Volver a sincronizar tras quitar un elemento del spec borra su SpecNodeDoc y sus RelationDoc.
- Una relación de tipo no builtin crea su RelationTypeDoc y el índice de aristas valida después de sincronizar.
- La compilación desde grafo produce, sobre el fixture de snapshot de spec2viz, un spec de componentes que valida y es equivalente al de spec2viz, o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz.
- La generación desde AST produce, sobre un paquete Python de fixture, un spec de componentes equivalente al de spec2viz.
- El paquete no importa spec2viz.

