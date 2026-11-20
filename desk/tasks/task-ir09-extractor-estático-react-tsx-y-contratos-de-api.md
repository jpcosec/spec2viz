---
sldb:
  by: agent
  at: '2026-11-20T22:00:58Z'
  authority: generated
  via: save_document_payload
id: task-ir09-extractor-estático-react-tsx-y-contratos-de-api
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:extractores
- host:robocop2
current_node: ritual-testing
history:
- task_activates
- 'task_returns_to_execution: Tester exec-deskops-t-e2a621a70a51-testing FALLA sobre
  6a9bbdd por la precisión (c) de la tarea: un fetch canónico con URL literal no queda
  declarado en not_derived y puede dejar una acción sin invokes (y una regla de nivel
  error). Lo demás pasa (43 passed, 2 xfailed en tests/extract, tests/models/test_blog_chain.py
  y tests/test_imports.py). Intento 2: tratar como hueco cualquier llamada cuyo último
  segmento sea fetch (que _is_hole sea true para fetch), con su motivo en not_derived,
  y agregar una prueba con un fetch de URL literal (en blog_frontend_gaps o en tests/extract/test_frontend_extraction.py)
  que verifique que va a not_derived y que no queda una acción sin invokes sin declarar.
  Commit solo de tus archivos con ''git commit -- <rutas>'' desde tu worktree.'
- task_activates
references:
- src/specir/extract/__init__.py
- src/specir/extract/plan.py
- src/specir/extract/react_tsx.py
- tests/extract/test_frontend_extraction.py
- tests/fixtures/blog_frontend/src/PublishButton.tsx
- tests/fixtures/blog_frontend/src/api/client.ts
- tests/fixtures/blog_frontend/src/api/legacy.js
- tests/fixtures/blog_frontend_gaps/src/ArchiveButton.tsx
- tests/fixtures/blog_frontend_gaps/src/FetchButton.tsx
- tests/fixtures/blog_frontend_gaps/src/SearchBox.tsx
- tests/fixtures/blog_frontend_gaps/src/api/fetcher.ts
- tests/fixtures/blog_frontend_gaps/src/api/legacy_archive.js
- tests/fixtures/blog_frontend_gaps/src/api/search.ts
- 6121f69f9da3b924875991a2f432886ad58e2a02
- 6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76
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
files:
- src/specir/extract/__init__.py
- src/specir/extract/plan.py
- src/specir/extract/react_tsx.py
- tests/extract/test_frontend_extraction.py
- tests/fixtures/blog_frontend/src/PublishButton.tsx
- tests/fixtures/blog_frontend/src/api/client.ts
- tests/fixtures/blog_frontend/src/api/legacy.js
- tests/fixtures/blog_frontend_gaps/src/ArchiveButton.tsx
- tests/fixtures/blog_frontend_gaps/src/FetchButton.tsx
- tests/fixtures/blog_frontend_gaps/src/SearchBox.tsx
- tests/fixtures/blog_frontend_gaps/src/api/fetcher.ts
- tests/fixtures/blog_frontend_gaps/src/api/legacy_archive.js
- tests/fixtures/blog_frontend_gaps/src/api/search.ts
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
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
