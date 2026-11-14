FILE:desk/tasks/task-ir09-extractor-estático-react-tsx-y-contratos-de-api.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:20Z'
  authority: generated
  via: save_document_payload
id: task-ir09-extractor-estático-react-tsx-y-contratos-de-api
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:extractores
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- src/specir/extract/react_tsx.py
- src/specir/extract/api_contracts.py
- tests/extract/test_react_tsx.py
- tests/extract/test_api_contracts.py
- tests/fixtures/blog_frontend/package.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
from_drawer: desk/drawer/tasks/task-ir09-extractor-estatico-react-tsx-y-contratos-api.md
---

# IR09 Extractor estático React/TSX y contratos de API

## Rationale

_Explain why this task exists or the business driver behind it._

El problema que motiva specIR es la pérdida de coherencia cuando un cambio atraviesa la interfaz. Sin extraer la interfaz, el grafo no puede decir qué controles dependen de un endpoint, un campo o una regla.

## Goal

_Describe the concrete result this task must produce._

Un extractor estático que, a partir de código React (JSX y TSX) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen.

## Scope

_State what is in scope and what is out of scope._

Dentro: lectura estática de componentes y sus propiedades, controles, acciones (handlers de eventos), estados locales declarados y llamadas HTTP; contratos de API disponibles (por ejemplo OpenAPI) para resolver a qué operación corresponde cada llamada; producción de controles, acciones, estados y las relaciones triggers e invokes hacia operaciones de API; evidencia de origen por nodo y relación con archivo, línea y hash; idempotencia.
Fuera: observación del DOM o de eventos en ejecución; comportamiento dinámico que no se deduce del código, que no se afirma: se marca como inferido o se deja como desconocido; generación o modificación de código de interfaz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de extracción en el paquete specIR; el analizador de JSX y TSX se elige en la tarea activa y queda aislado detrás del módulo; los vínculos a backend se resuelven contra las operaciones de API que ya están en el grafo (pobladas a mano o por el extractor de backend); fixture: el frontend React del blog de ejemplo.

## Validation

_List the checks required before this task can close._

- Sobre el fixture del blog, el extractor produce PublishButton, PublishAction y su relación con la operación de API de publicar, con los tipos de la tarea de tipos de dominio.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente.
- Una llamada HTTP cuya URL no se resuelve estáticamente produce una relación marcada como inferida o un hueco declarado, nunca una relación observada.
- Una llamada a un endpoint que no existe en el grafo queda registrada como brecha, no se descarta ni se inventa la operación.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre el fixture y la mitad de interfaz de la cadena de publicar un post se obtiene sin poblarla a mano.

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

FILE:instruccion
Cold-bundle de la tarea task-ir09-extractor-estático-react-tsx-y-contratos-de-api: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Sobre el fixture del blog, el extractor produce PublishButton, PublishAction y su relación con la operación de API de publicar, con los tipos de la tarea de tipos de dominio.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente.
- Una llamada HTTP cuya URL no se resuelve estáticamente produce una relación marcada como inferida o un hueco declarado, nunca una relación observada.
- Una llamada a un endpoint que no existe en el grafo queda registrada como brecha, no se descarta ni se inventa la operación.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc.

