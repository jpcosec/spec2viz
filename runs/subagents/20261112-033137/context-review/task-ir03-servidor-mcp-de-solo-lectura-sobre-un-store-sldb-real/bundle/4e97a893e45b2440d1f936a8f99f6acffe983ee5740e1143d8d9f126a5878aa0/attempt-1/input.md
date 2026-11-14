FILE:desk/tasks/task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real.md
---
sldb:
  by: agent
  at: '2026-11-12T03:25:25Z'
  authority: generated
  via: save_document_payload
id: task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- pyproject.toml
- src/specir/__init__.py
- src/specir/mcp/__init__.py
- src/specir/mcp/server.py
- src/specir/mcp/read_tools.py
- src/specir/mcp/addresses.py
- src/specir/mcp/paging.py
- tests/conftest.py
- tests/mcp/test_read_tools.py
- tests/mcp/test_no_writes.py
- tests/test_imports.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
from_drawer: desk/drawer/tasks/task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real.md
---

# IR03 Servidor MCP de solo lectura sobre un store SLDB real

## Rationale

_Explain why this task exists or the business driver behind it._

El primer hito del proyecto es que un agente explore un store SLDB real por MCP. La lectura no necesita esperar las decisiones de escritura.

## Goal

_Describe the concrete result this task must produce._

Un servidor MCP de solo lectura, en el paquete specIR, con el que un agente descubre modelos, lee documentos, recorre relaciones y resuelve vistas de un store SLDB.

## Scope

_State what is in scope and what is out of scope._

Dentro: servidor MCP por stdio sobre la API pública de SLDB con tools para listar y describir modelos y tipos de relación, leer un documento o un campo, vecinos y recorrido por relación, búsqueda por predicados, resolver una vista (ViewDoc o SpecDoc) a JSON, e integridad del store. Fuera: cualquier escritura, tipos de dominio nuevos, extractores, renderizado de diagramas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Paquete Python specIR con dependencia en structuredLanguageDB y el SDK de MCP como extra opcional; las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes. Store de las pruebas: una copia aislada del store real de este repo, sin registros fabricados. La obtiene un fixture de tests/conftest.py que copia a un directorio temporal de la prueba las carpetas .sldb/, sldb/ y desk/ de la raíz del repo (los documentos reales del desk: atoms, tareas, rituales, reglas y tipos de relación), sin copiar .sldb_cache/. Sobre la copia solo operan herramientas públicas de SLDB: sldb stores update para reconstruir los índices derivados, sldb edges rebuild para el índice de aristas y sldb stores check para comprobar la integridad antes de usarla; el store federado deskops, que el original enlaza por ruta relativa, se vuelve a enlazar en la copia con sldb stores add apuntando a su ruta real, y con el mismo comando se enlaza además el store real de spec2viz (../spec2viz/.sldb respecto de la raíz de este repo); ambos se leen en sitio en solo lectura y las pruebas no escriben en ellos. El servidor bajo prueba es el servidor MCP real, lanzado por stdio y consultado con el cliente del SDK de MCP: no se simulan ni la API de SLDB, ni el servidor, ni el cliente. La prueba de resolución de vistas usa el SpecDoc real class.sldb-models del store federado de spec2viz: primero comprueba que ese documento resuelve desde la federación de la copia y después lo lee y resuelve su vista por las tools del servidor. Si el store de spec2viz o ese documento dejan de existir, la prueba falla con un mensaje que nombra el store y el documento que faltan; no se sustituye por un documento inventado.

## Validation

_List the checks required before this task can close._

- Las pruebas corren con un cliente MCP real contra el servidor real lanzado por stdio sobre la copia aislada del store de este repo; cada tool devuelve JSON estructurado y, por cada documento, su dirección estable.
- Los documentos que devuelven las tools existen en el store original con el mismo id y contenido (comparación contra los archivos de desk/ del repo).
- Todo conjunto llega paginado, con su total y una marca cuando quedó cortado; se prueba sobre el modelo con más documentos del store.
- El SpecDoc real class.sldb-models del store de spec2viz resuelve desde la federación de la copia, y las tools de lectura y de resolución de vistas lo devuelven con el mismo contenido que tiene en ../spec2viz/.sldb; si el store o el documento faltan, la prueba falla nombrando cuál falta.
- Montar la copia y ejecutar todas las tools de lectura no modifica ningún archivo de la copia ni de los stores federados de deskops y de spec2viz (comparación del árbol antes y después).
- El store original del repo no cambia durante las pruebas (comparación del árbol de .sldb/ y desk/ antes y después).
- Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación, no un error opaco.
- Una prueba de imports comprueba que el paquete no importa pron, spec2viz, ni módulos de SLDB fuera de sldb.api.
- Ninguna prueba crea documentos de contenido inventado ni sustituye la API de SLDB, el servidor o el cliente por un doble.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre la copia aislada del store real de este repo y un agente conectado al servidor recorre ese store sin escribir en él.

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

FILE:desk/atoms/atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:31Z'
  authority: generated
  via: create_document
id: atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
title: El consumidor principal de specIR es un agente por MCP
five_wh_one_plus: for_whom
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# El consumidor principal de specIR es un agente por MCP

## Answer

El consumidor principal es un agente de código conectado por MCP (Model Context Protocol). La edición y la inspección gráfica son complementarias: sirven para que una persona revise, discuta y corrija los modelos. Por eso el primer producto es el servidor MCP y toda operación debe ser invocable por un agente antes que por una interfaz gráfica.

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

FILE:desk/atoms/atom-specir-no-depende-de-pron-adopta-contratos-no-código.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:33Z'
  authority: generated
  via: create_document
id: atom-specir-no-depende-de-pron-adopta-contratos-no-código
title: 'specIR no depende de pron: adopta contratos, no código'
five_wh_one_plus: how_not
tags:
- system:specir
- system:pron
- topic:dependencias
---

# specIR no depende de pron: adopta contratos, no código

## Answer

specIR no usa pron como base ni como dependencia: ningún import de pron y ninguna entrada suya en las dependencias del paquete. De la superficie MCP de pron (pron/source/spec/14-superficie-mcp.md) se pueden adoptar contratos reimplementados sobre SLDB: direcciones por URI, paginación con total y truncated, selectores que solo resuelven lo que el store declara, dry_run en toda escritura, niveles de mutabilidad y cero texto libre en el camino de la escritura. No se adoptan las formas, el léxico, las sesiones de diálogo ni el concepto de mundo. Decisión del dueño del proyecto, 2026-11-11: pron está desactualizado y no funciona bien como base.

FILE:instruccion
Cold-bundle de la tarea task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Las pruebas corren con un cliente MCP real contra el servidor real lanzado por stdio sobre la copia aislada del store de este repo; cada tool devuelve JSON estructurado y, por cada documento, su dirección estable.
- Los documentos que devuelven las tools existen en el store original con el mismo id y contenido (comparación contra los archivos de desk/ del repo).
- Todo conjunto llega paginado, con su total y una marca cuando quedó cortado; se prueba sobre el modelo con más documentos del store.
- El SpecDoc real class.sldb-models del store de spec2viz resuelve desde la federación de la copia, y las tools de lectura y de resolución de vistas lo devuelven con el mismo contenido que tiene en ../spec2viz/.sldb; si el store o el documento faltan, la prueba falla nombrando cuál falta.
- Montar la copia y ejecutar todas las tools de lectura no modifica ningún archivo de la copia ni de los stores federados de deskops y de spec2viz (comparación del árbol antes y después).
- El store original del repo no cambia durante las pruebas (comparación del árbol de .sldb/ y desk/ antes y después).
- Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación, no un error opaco.
- Una prueba de imports comprueba que el paquete no importa pron, spec2viz, ni módulos de SLDB fuera de sldb.api.
- Ninguna prueba crea documentos de contenido inventado ni sustituye la API de SLDB, el servidor o el cliente por un doble.

