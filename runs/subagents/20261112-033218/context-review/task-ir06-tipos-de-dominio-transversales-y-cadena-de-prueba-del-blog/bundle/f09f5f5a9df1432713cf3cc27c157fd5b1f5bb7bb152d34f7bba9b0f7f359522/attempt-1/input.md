FILE:desk/tasks/task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:18Z'
  authority: generated
  via: save_document_payload
id: task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:modelado
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar
- task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- src/specir/models/__init__.py
- src/specir/models/domain.py
- src/specir/data/relation_types.yaml
- src/specir/data/rules.yaml
- src/specir/install.py
- tests/models/test_domain_models.py
- tests/models/test_blog_chain.py
- tests/fixtures/blog_chain.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-omg-es-referencia-conceptual-no-dependencia
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog.md
---

# IR06 Tipos de dominio transversales y cadena de prueba del blog

## Rationale

_Explain why this task exists or the business driver behind it._

La tesis de specIR es que un grafo tipado conecta interfaz, API, operación y datos sin duplicar objetos. Hay que demostrarla en un caso pequeño antes de construir extractores o análisis sobre ella.

## Goal

_Describe the concrete result this task must produce._

Los tipos de dominio transversales de specIR y un store de prueba con la cadena de publicar un post del blog de ejemplo (React, Django REST Framework, PostgreSQL), recorrible por MCP.

## Scope

_State what is in scope and what is out of scope._

Dentro: (1) clases Python de modelo, definidas en el paquete specIR como subclases del documento base de SLDB, para control de interfaz, acción, operación de API, handler, operación de dominio, política, estado, entidad de dominio y tabla; (2) tipos de relación como documentos RelationTypeDoc que specIR distribuye e instala en un store: triggers, invokes, handled_by, executes, governed_by, transitions, writes, persisted_in; (3) invariantes entre capas como documentos RuleDoc que specIR distribuye, por ejemplo que toda acción de interfaz invoque una operación de API existente; (4) un store de prueba poblado por MCP con la cadena de publicar un post. Frontera: las clases de modelo son código de specIR; los tipos de relación y las reglas son datos del store; el MCP escribe datos y no clases. Fuera: extractores automáticos, análisis de impacto, síntesis.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de modelos dentro del paquete specIR, registrado en el store por el mecanismo de registro de modelos de SLDB, como hace deskops con los suyos; documentos builtin de RelationTypeDoc y RuleDoc instalados por un comando de specIR; población del store de prueba con las tools de escritura.

## Validation

_List the checks required before this task can close._

- Por MCP se recorre PublishButton, PublishAction, endpoint, handler, PublishPost y tabla, en ambos sentidos.
- Una relación entre tipos no permitidos (por ejemplo un control de interfaz que escribe directo en una tabla) es rechazada por su RelationTypeDoc.
- Quitar del store de prueba la operación de API que una acción invoca hace que la evaluación de reglas reporte el RuleDoc incumplido.
- Dos vistas distintas (una de estados y una de componentes) muestran la misma entidad Post y el store contiene un solo documento para ella.
- Cada nodo y relación lleva la procedencia de la taxonomía canónica decidida.
- Las clases de modelo viven en el paquete specIR y ningún modelo de vocabulario visual de SLDB se redefine.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y la cadena del blog queda como store de prueba reutilizable por las tareas posteriores.

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

FILE:desk/atoms/atom-entidad-aparición-proyección-y-notación-son-cosas-distintas.md
---
sldb:
  by: agent
  at: '2026-11-12T00:48:14Z'
  authority: generated
  via: save_document_payload
id: atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
title: Identidad semántica, aparición, proyección, notación y formato de autoría son
  cosas distintas
five_wh_one_plus: what
tags:
- system:specir
- topic:identidad
- topic:proyecciones
- layer:modelo
provenance: fundamentos_modelado_semantico_mcp.md
---

# Identidad semántica, aparición, proyección, notación y formato de autoría son cosas distintas

## Answer

La fuente semántica de specIR es el grafo tipado de SLDB. Se distinguen cinco cosas: (1) entidad semántica, lo que existe en el dominio o sistema (Post, PublishPost, POST /posts/{id}/publish), con una sola identidad en el grafo; (2) aparición, la presencia de esa entidad en una vista o diagrama; (3) proyección, el criterio que selecciona y organiza elementos y relaciones del grafo para una finalidad; (4) notación, las reglas para dibujarlos, que no redefinen su identidad ni su significado; (5) formato de autoría, el archivo en que alguien escribe o intercambia un diagrama. El YAML de spec de spec2viz es un formato de autoría e intercambio, válido al menos mientras dure la paridad con spec2viz: lo que declara entra al grafo y no constituye una segunda identidad. Dos diagramas pueden mostrar el mismo objeto sin duplicarlo. Si el YAML se conserva como formato permanente es una decisión pendiente, incluida en la candidata de cobertura de spec2viz.

FILE:desk/atoms/atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:30Z'
  authority: generated
  via: create_document
id: atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
title: 'Por qué existe specIR: coherencia entre capas para agentes de código'
five_wh_one_plus: why
tags:
- system:specir
- topic:motivacion
provenance: fundamentos_modelado_semantico_mcp.md
---

# Por qué existe specIR: coherencia entre capas para agentes de código

## Answer

Los agentes de código generan bien componentes aislados (un componente React, un endpoint Django, un modelo SQL) pero pierden coherencia cuando un cambio atraviesa varias capas, porque interacciones, estados, datos, permisos y operaciones están dispersos entre archivos y tecnologías sin una representación común. specIR existe para darles un modelo semántico tipado, inspeccionable y modificable del sistema completo; no para generar mejores pantallas a partir de prompts.

FILE:desk/atoms/atom-omg-es-referencia-conceptual-no-dependencia.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:37Z'
  authority: generated
  via: create_document
id: atom-omg-es-referencia-conceptual-no-dependencia
title: OMG es referencia conceptual, no dependencia
five_wh_one_plus: how_not
tags:
- system:specir
- topic:omg
- topic:metamodelos
provenance: fundamentos_modelado_semantico_mcp.md
---

# OMG es referencia conceptual, no dependencia

## Answer

specIR toma de los estándares OMG (MOF, UML, IFML, OCL, QVT, DI) conceptos de metamodelado, conformidad, restricciones y separación entre modelo y representación, y los implementa con los contratos de SLDB. No adopta EMF, Sirius ni GLSP como runtime, no implementa UML completo y no afirma conformidad con ningún estándar mientras no existan transformaciones y validaciones probadas contra su especificación.

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
Cold-bundle de la tarea task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Por MCP se recorre PublishButton, PublishAction, endpoint, handler, PublishPost y tabla, en ambos sentidos.
- Una relación entre tipos no permitidos (por ejemplo un control de interfaz que escribe directo en una tabla) es rechazada por su RelationTypeDoc.
- Quitar del store de prueba la operación de API que una acción invoca hace que la evaluación de reglas reporte el RuleDoc incumplido.
- Dos vistas distintas (una de estados y una de componentes) muestran la misma entidad Post y el store contiene un solo documento para ella.
- Cada nodo y relación lleva la procedencia de la taxonomía canónica decidida.
- Las clases de modelo viven en el paquete specIR y ningún modelo de vocabulario visual de SLDB se redefine.

