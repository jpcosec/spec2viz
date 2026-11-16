FILE:desk/tasks/task-ir08-extractor-estático-django-drf-y-sql.md
---
sldb:
  by: agent
  at: '2026-11-16T20:04:24Z'
  authority: generated
  via: save_document_payload
id: task-ir08-extractor-estático-django-drf-y-sql
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:extractores
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir08-extractor-estatico-django-drf-y-sql.md
---

# IR08 Extractor estático Django/DRF y SQL

## Rationale

_Explain why this task exists or the business driver behind it._

La cadena del blog se puebla a mano en la tarea de tipos de dominio; para trabajar sobre sistemas existentes el grafo tiene que salir del código. El backend y los datos son la mitad más determinista de esa extracción y fijan el formato de procedencia que usará el resto.

## Goal

_Describe the concrete result this task must produce._

Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen de una aplicación Django REST Framework y de su esquema SQL (sldb/code y los readers de la tarea espejo B2), produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.

## Scope

_State what is in scope and what is out of scope._

Dentro: mapeo de los facts de sldb (rutas y vistas, serializers y sus campos, modelos Django y sus relaciones, tablas, columnas y claves del esquema SQL en el dialecto de Postgres, que es el que se usa) a operaciones de API, handlers, entidades de dominio, tablas y las relaciones entre ellos; la procedencia por nodo y relación con archivo, línea y hash del fragmento, tomada de las anclas de sldb y traducida a la taxonomía de la tarea de procedencia; idempotencia: mapear dos veces el mismo código no cambia el store. Fuera: leer o analizar código (es de sldb: readers, facts y anclas); otros dialectos SQL; frontend; análisis en tiempo de ejecución; reglas de negocio que no se deducen del código, que quedan como desconocidas o marcadas como inferidas; análisis de impacto; cualquier parche al código. Si un reader o un fact no existe en sldb, se pide por el desk de sldb y no se reimplementa en specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de mapeo en el paquete specIR (specir.extract) que consume solo la API pública de sldb: los facts y anclas de sldb/code sobre el código del fixture, y las operaciones validadas de escritura de sldb (apply_batch) para crear documentos y relaciones. Sin tree-sitter, ast ni parsers propios en specIR. El SQL apunta al dialecto de Postgres (indicación de JP del 2026-11-16): el esquema del fixture está escrito en ese dialecto y se lee con el reader SQL de sldb de la tarea espejo B2. Fixture: una aplicación Django REST Framework real y pequeña, la del blog de ejemplo, versionada en el repo de specIR. Depende de la tarea espejo B2 (readers y facts de TS, TSX, JS y SQL de sldb) y de las tareas de procedencia y de tipos de dominio.

## Validation

_List the checks required before this task can close._

- Sobre el fixture de la aplicación del blog, el extractor produce los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano, con los mismos tipos y relaciones.
- El esquema SQL del fixture está en el dialecto de Postgres, y sus tablas, columnas y claves llegan al grafo a partir de los facts del reader SQL de sldb.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente, y su procedencia en la taxonomía canónica.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación del árbol del store).
- Modificar un archivo fuente del fixture y volver a extraer señala los nodos anclados a ese archivo como cambiados, sin borrar hechos validados por una persona.
- Ningún nodo inferido queda con procedencia de observado o validado.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes.
- El módulo no importa pron ni spec2viz, ni módulos de SLDB fuera de sldb.api.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre el fixture, el grafo de backend y datos del blog se obtiene sin poblarlo a mano y specIR no contiene ningún lector de código propio: solo el mapeo de los facts de sldb a sus tipos de dominio.

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
  at: '2026-11-15T05:05:58Z'
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

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Mecanismos decididos (docs/decisiones/contrato-de-escritura-mcp.md, 2026-11-15): la propuesta es un lote efímero prevalidado que se aplica todo o nada con sldb.api.apply_batch (atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado); la aplicación se protege con guardas expected_source_hash por documento y, en nivel 2, con store_hash atómico (atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2); el nivel de escritura se fija al arrancar el servidor, 0 por defecto (atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor); deshacer es un lote inverso con guardas (atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas). Procedencia decidida (docs/decisiones/procedencia-y-divergencia.md, 2026-11-15): ejes origen y verificacion con la autoridad de SLDB por tabla (atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla); lo desconocido se nombra y el MCP nunca escribe verificado (atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica); anclas de SLDB y divergencia según el origen (atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen).

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
Cold-bundle de la tarea task-ir08-extractor-estático-django-drf-y-sql: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Sobre el fixture de la aplicación del blog, el extractor produce los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano, con los mismos tipos y relaciones.
- El esquema SQL del fixture está en el dialecto de Postgres, y sus tablas, columnas y claves llegan al grafo a partir de los facts del reader SQL de sldb.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente, y su procedencia en la taxonomía canónica.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación del árbol del store).
- Modificar un archivo fuente del fixture y volver a extraer señala los nodos anclados a ese archivo como cambiados, sin borrar hechos validados por una persona.
- Ningún nodo inferido queda con procedencia de observado o validado.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes.
- El módulo no importa pron ni spec2viz, ni módulos de SLDB fuera de sldb.api.

