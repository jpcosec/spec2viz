FILE:desk/tasks/task-ir10-reglas-semánticas-y-análisis-de-impacto.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:37Z'
  authority: generated
  via: save_document_payload
id: task-ir10-reglas-semánticas-y-análisis-de-impacto
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:impacto
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-ir08-extractor-estático-django-drf-y-sql
- task-ir09-extractor-estático-react-tsx-y-contratos-de-api
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- src/specir/data/layer_rules.yaml
- src/specir/impact.py
- src/specir/mcp/impact_tools.py
- tests/rules/test_layer_rules.py
- tests/test_impact.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir10-reglas-semanticas-y-analisis-de-impacto.md
---

# IR10 Reglas semánticas y análisis de impacto

## Rationale

_Explain why this task exists or the business driver behind it._

Tener el grafo no basta: el agente necesita que el sistema le diga qué se rompe cuando cambia un campo, un endpoint o una regla, y con qué evidencia. Es el criterio de éxito 4 de los fundamentos.

## Goal

_Describe the concrete result this task must produce._

Un conjunto de reglas RuleDoc que detectan brechas entre capas y una operación de análisis de impacto, expuesta por MCP, que devuelve los elementos afectados por un cambio con el camino que lo justifica.

## Scope

_State what is in scope and what is out of scope._

Dentro: reglas RuleDoc, distribuidas por specIR como documentos, para cadenas rotas interfaz, API, operación, datos: acción sin operación de API, campo de interfaz ausente del serializer, operación sin handler, entidad sin persistencia, política sin representación en la interfaz; cada hallazgo con severidad, regla que lo produce y evidencia; operación de impacto: dado un nodo (campo, endpoint, regla, tabla), los nodos afectados en las demás capas con el camino de relaciones que lo explica y la procedencia de cada tramo; tool MCP de solo lectura para ambas.
Fuera: proponer parches o cambios de código; aplicar correcciones al grafo; reglas que requieran ejecutar la aplicación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las reglas se escriben en el lenguaje de reglas de SLDB y se evalúan con sus operaciones públicas de reglas; el impacto se calcula con las operaciones públicas de recorrido del grafo de SLDB. Si el lenguaje de reglas no alcanza para alguna brecha, la carencia se resuelve en SLDB, no con lógica paralela en specIR.

## Validation

_List the checks required before this task can close._

- Por cada regla hay un store de prueba con la brecha sembrada y la evaluación la reporta con su severidad, la regla y los documentos implicados.
- Sobre el grafo completo del blog sin brechas sembradas, las reglas no reportan hallazgos.
- Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton entre los afectados, con el camino completo de relaciones.
- Cada tramo del camino devuelto lleva su procedencia, y un camino que pasa por una relación inferida se señala como tal.
- Las tools de reglas e impacto no escriben en el store (comparación del árbol antes y después).
- Ninguna respuesta incluye un parche ni una modificación propuesta.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y un agente puede responder por MCP qué partes de la interfaz afecta un cambio en un campo, un endpoint o una regla del blog.

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

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

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

FILE:desk/atoms/atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir.md
---
sldb:
  by: agent
  at: '2026-11-12T00:48:16Z'
  authority: generated
  via: save_document_payload
id: atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
title: Principios de seguridad de la superficie MCP de specIR
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- topic:procedencia
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# Principios de seguridad de la superficie MCP de specIR

## Answer

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Son principios, no mecanismos: cómo se representa una propuesta, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido y qué taxonomía de procedencia se usa están pendientes de decisión en las candidatas de contrato de escritura y de procedencia.

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
Cold-bundle de la tarea task-ir10-reglas-semánticas-y-análisis-de-impacto: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Por cada regla hay un store de prueba con la brecha sembrada y la evaluación la reporta con su severidad, la regla y los documentos implicados.
- Sobre el grafo completo del blog sin brechas sembradas, las reglas no reportan hallazgos.
- Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton entre los afectados, con el camino completo de relaciones.
- Cada tramo del camino devuelto lleva su procedencia, y un camino que pasa por una relación inferida se señala como tal.
- Las tools de reglas e impacto no escriben en el store (comparación del árbol antes y después).
- Ninguna respuesta incluye un parche ni una modificación propuesta.

