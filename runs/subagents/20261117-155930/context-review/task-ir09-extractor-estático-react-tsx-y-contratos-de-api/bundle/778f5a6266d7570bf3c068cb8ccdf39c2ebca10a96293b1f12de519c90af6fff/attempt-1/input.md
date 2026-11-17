FILE:desk/tasks/task-ir09-extractor-estático-react-tsx-y-contratos-de-api.md
---
sldb:
  by: agent
  at: '2026-11-17T15:59:25Z'
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
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2
- task-espejo-sldb-sldb-api-expone-los-facts-de-código-que-necesitan-los-extractores-c1-c5
- task-espejo-sldb-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-c3-de-ir-parte-ts-js-para-ir09
- task-ir08-extractor-estático-django-drf-y-sql
- task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester
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
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
from_drawer: desk/drawer/tasks/task-ir09-extractor-estatico-react-tsx-y-contratos-api.md
---

# IR09 Extractor estático React/TSX y contratos de API

## Rationale

_Explain why this task exists or the business driver behind it._

El problema que motiva specIR es la pérdida de coherencia cuando un cambio atraviesa la interfaz. Sin extraer la interfaz, el grafo no puede decir qué controles dependen de un endpoint, un campo o una regla.

## Goal

_Describe the concrete result this task must produce._

Un mapeo de dominio que, sobre los facts genéricos que sldb.api.code.code_facts da del frontend (TS, TSX, JS y JSX: attrs.calls con name canónico, first_arg y canonical, y attrs.handlers con element, attribute y handler), produce los elementos de interfaz del grafo de specIR (InterfaceControlDoc, InterfaceActionDoc) y los vincula con triggers e invokes a las operaciones de API que ya hay en el grafo, con anclas por fact. Reparto acordado con sldb (nota 211648 y C3 TS en 0590ed11/3b3c51fe): sldb publica la sintaxis de forma genérica y specIR interpreta React, fetch y axios sobre esos hechos. specIR no lee código.

## Scope

_State what is in scope and what is out of scope._

Dentro: interpretar en specIR, sobre los facts genéricos de sldb, los componentes React y sus handlers JSX (attrs.handlers: onClick y similares, hacia una función del componente), las llamadas HTTP (attrs.calls canónicas a fetch, axios.<método> o un cliente de API, con first_arg literal como URL) y su resolución contra las ApiOperationDoc que ya están en el grafo (las de IR08, por método y ruta normalizada); InterfaceControlDoc por elemento con handler, InterfaceActionDoc por handler, triggers control -> acción e invokes acción -> operación; anclas con archivo, línea y source_hash del fact; idempotencia; un fixture de frontend React real y mínimo del blog en tests/fixtures/blog_frontend, con el botón de publicar que llama a POST /posts/{id}/publish, escrito en TSX y con al menos un .ts y un .js si el caso lo pide. Fuera: leer o parsear código (tree-sitter, ast, regex sobre fuentes, lectura de bytes de fuentes); observación del DOM o de eventos en ejecución; OpenAPI (no hay contratos de API en el fixture); generación de código de interfaz; cambios en specir.extract de backend salvo lo que el frontend comparta (helpers de anclas y escritura). Si falta un fact genérico en sldb, se pide por el desk de sldb y la tarea se detiene.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de frontend dentro de specir.extract que reutiliza sus helpers de anclas, procedencia y escritura (write_anchor, apply_batch, el informe creados, sin cambios, cambiados y no derivados de IR08) y consume solo sldb.api. Procedencia según IR05 (docs/decisiones/procedencia-y-divergencia.md) y src/specir/models/domain.py: lo leído tal cual de un fact es observado (el control, el handler) y lo armado por regla es derivado (triggers, invokes); nunca inferido ni declarado; siempre sin_verificar; evidencia vacía; la regla se nombra en la descripción. Las llamadas con canonical false, sin first_arg literal o con una URL que no casa con ninguna ApiOperationDoc del grafo no crean relación: van a not_derived con su motivo (hueco declarado o brecha hacia un endpoint ausente). La comprobación de anclas no lee bytes de fuentes (ver la tarea de seguimiento D1 de IR08): usa solo sldb.api. Pruebas en tests/extract/. El grafo de backend lo da la extracción de IR08 sobre tests/fixtures/blog_app en el mismo store de prueba. sldb mínimo en origin main: C3 TS en 0590ed11. Dependencias: IR05, IR06, espejos B2, C1–C5 y C3 TS. Precisiones (preflight-3, coordinador): (a) El fixture tiene un .tsx (el componente PublishButton, que dibuja un <button onClick={handlePublish}>; el control se nombra por el componente y el elemento, y la acción por el handler; la prueba compara tipos y relaciones con tests/models/blog.py, no los nombres), un .ts (el cliente de API) y un .js (una llamada HTTP más), los tres obligatorios. (b) sldb da first_arg solo si es un string o un template sin ${...} (sldb/src/sldb/code/ts_calls.py); una URL con ${id} da first_arg None. Por eso el cliente de API del fixture sigue el patrón de openapi-fetch: client.POST("/posts/{id}/publish", { params: { path: { id } } }), con la ruta como literal con {param}. (c) Es llamada HTTP una llamada canónica cuyo último segmento del nombre es un verbo HTTP (get, post, put, patch, delete, sin distinguir mayúsculas; axios.post, client.POST) con first_arg literal que empieza por /; el método sale del nombre. fetch(...) va a not_derived porque el método no está en los facts. Ninguna otra llamada es HTTP. (d) Si el handler llama a una función del proyecto (por ejemplo publishPost del .ts) en lugar de llamar al cliente directamente, se sigue por su nombre canónico a la única función de los facts del frontend con ese nombre, un solo nivel; si no es única o no existe, va a not_derived. (e) La ruta se compara con la de las ApiOperationDoc del grafo tal como las escribe IR08: sin barra final ni query, segmento a segmento, y cualquier {x} casa con cualquier {y}. Más de una coincidencia va a not_derived. (f) not_derived es la lista de strings con archivo:línea y motivo que ya usa write_plan de src/specir/extract/write.py; los helpers son los de src/specir/extract/plan.py y write.py, que se reutilizan sin cambiar su firma.

## Validation

_List the checks required before this task can close._

- Sobre tests/fixtures/blog_frontend, con el backend de tests/fixtures/blog_app extraído en el mismo store, el extractor produce PublishButton (InterfaceControlDoc), PublishAction (InterfaceActionDoc), triggers entre ellos e invokes hacia la ApiOperationDoc POST /posts/{id}/publish, con los tipos y relaciones de tests/models/blog.py.
- Los facts de .ts, .tsx y .js del fixture se mapean con el mismo código, sin ramas por extensión; si el fixture no tiene alguna de esas extensiones, la prueba lo declara.
- Cada nodo y relación extraído lleva anclas con archivo, línea y source_hash iguales a los de code_facts, origen observado o derivado y verificacion sin_verificar.
- Una llamada HTTP con URL no literal (template con expresiones o canonical false) no crea relación y queda en not_derived como hueco declarado.
- Una llamada a un endpoint que no existe en el grafo queda en not_derived como brecha, sin inventar la operación.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.
- Las relaciones extraídas pasan sldb edges check y sldb rules check sin hallazgos de nivel error.
- grep -rnE "tree_sitter|import ast|from ast|pglast|read_bytes|read_text|sldb\\.code\\b|spec2viz" src/specir/extract no devuelve nada nuevo respecto de lo que deja la tarea de seguimiento D1.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/extract tests/models/test_blog_chain.py tests/test_imports.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre el fixture, la mitad de interfaz de la cadena de publicar un post se obtiene sin poblarla a mano y specIR no contiene ningún analizador propio de TS, TSX, JSX ni JS.

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
- Sobre tests/fixtures/blog_frontend, con el backend de tests/fixtures/blog_app extraído en el mismo store, el extractor produce PublishButton (InterfaceControlDoc), PublishAction (InterfaceActionDoc), triggers entre ellos e invokes hacia la ApiOperationDoc POST /posts/{id}/publish, con los tipos y relaciones de tests/models/blog.py.
- Los facts de .ts, .tsx y .js del fixture se mapean con el mismo código, sin ramas por extensión; si el fixture no tiene alguna de esas extensiones, la prueba lo declara.
- Cada nodo y relación extraído lleva anclas con archivo, línea y source_hash iguales a los de code_facts, origen observado o derivado y verificacion sin_verificar.
- Una llamada HTTP con URL no literal (template con expresiones o canonical false) no crea relación y queda en not_derived como hueco declarado.
- Una llamada a un endpoint que no existe en el grafo queda en not_derived como brecha, sin inventar la operación.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.
- Las relaciones extraídas pasan sldb edges check y sldb rules check sin hallazgos de nivel error.
- grep -rnE "tree_sitter|import ast|from ast|pglast|read_bytes|read_text|sldb\\.code\\b|spec2viz" src/specir/extract no devuelve nada nuevo respecto de lo que deja la tarea de seguimiento D1.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/extract tests/models/test_blog_chain.py tests/test_imports.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

