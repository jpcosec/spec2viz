FILE:desk/tasks/task-ir08-extractor-estático-django-drf-y-sql.md
---
sldb:
  by: agent
  at: '2026-11-17T11:18:08Z'
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
- task-espejo-sldb-sldb-api-expone-los-facts-de-código-que-necesitan-los-extractores-c1-c5
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

Un mapeo de dominio que, a partir de los facts genéricos de código que da sldb.api.code.code_facts sobre una aplicación Django REST Framework y su esquema SQL de Postgres, produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen. Reparto acordado con sldb (2026-11-16, nota 211648 y sus 4 tareas): sldb publica la sintaxis de forma genérica (clases con extends y attrs.bases, attrs.decorators con args y kwargs, calls y attrs.calls, kind assignment con attrs.call, attrs.items, attrs.value y attrs.op, kind call, y hechos constraint del SQL) y specIR interpreta Django y DRF sobre esos hechos. specIR no lee código: no escribe readers ni parsers.

## Scope

_State what is in scope and what is out of scope._

Dentro: interpretar en specIR, sobre los facts genéricos de sldb, las convenciones de Django y DRF: rutas (urlpatterns con path() y +=, router.register, @action con detail y methods), viewsets y sus handlers, serializers (bases ModelSerializer, Meta.model y Meta.fields), modelos (bases models.Model, campos con ForeignKey y choices, Meta.db_table, TextChoices como estados) y llamadas entre símbolos (handler -> método -> función); y el SQL de Postgres del fixture (tablas, columnas y hechos constraint primary_key, foreign_key y unique con references). Mapear todo eso a operaciones de API, handlers, entidades, estados, tablas y sus relaciones; procedencia por nodo y relación con archivo, línea (span) y source_hash, tomada de code_facts y de las anclas de sldb (write_anchor) y traducida a la taxonomía de la tarea de procedencia; idempotencia. Fuera: leer o parsear código (tree-sitter, ast, regex sobre fuentes, pglast directo); otros dialectos SQL; frontend (IR09); análisis en tiempo de ejecución; reglas de negocio que no se deducen del código, que quedan desconocidas o marcadas como inferidas; análisis de impacto (IR10); cambios en tests/fixtures/blog_app salvo lo que pida la Validation 5 dentro de una copia temporal. Si falta un fact genérico en sldb, se pide por el desk de sldb y la tarea se detiene; no se reimplementa en specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo specir.extract que consume solo la API pública de sldb: sldb.api.code.code_facts para los facts con span y source_hash, sldb.api.anchors.write_anchor para las anclas y apply_batch para crear documentos y relaciones. La interpretación de Django y DRF es una tabla de reglas de specIR sobre los facts genéricos (bases, decoradores, assignment, call, calls), sin tree-sitter, ast ni parsers propios. El SQL del fixture está en el dialecto de Postgres (indicación de JP del 2026-11-16) y sus claves llegan como hechos constraint, que sldb lee con pglast cuando está el extra postgres: el extra test de [project.optional-dependencies] en pyproject.toml pasa a pedir structuredLanguageDB[mcp,code,postgres], y el .venv de IR se actualiza con él. Fixture: tests/fixtures/blog_app (commit ad51a0f), la app DRF real del blog con su SQL generado por sqlmigrate de Django 6.1.3. sldb mínimo en origin main: C1, C2 y C5 en 3dc9a526, C4 en 691a0e89 y C3 de Python en ad6f8842. Depende de las tareas de procedencia y de tipos de dominio y de los espejos B2 y C1–C5. Adjudicaciones del preflight-3. (1) Tipos y procedencia: los de src/specir/models/domain.py, src/specir/data/relation_types.yaml y docs/decisiones/procedencia-y-divergencia.md (IR05, D1-B). Lo que el extractor lee tal cual de un fact (un símbolo, una ruta de path(), una tabla o columna) es origen observado; lo que arma una regla de specIR sobre facts observados (la ruta de router.register más @action, handled_by, executes, governed_by, transitions, writes, persisted_in) es origen derivado. Archivo, línea y source_hash van en anclas escritas con sldb.api.anchors.write_anchor sobre el fact de code_facts: una por fact observado y, en lo derivado, una por cada fact fuente de la regla; el source_hash es el del fact, y si el ancla escrita no coincide con él el extractor falla. El campo evidencia queda vacío, como fija src/specir/models/domain.py para sin_verificar; la regla que derivó un nodo o relación se nombra en su descripción. El extractor nunca produce inferido ni declarado, y siempre deja verificacion sin_verificar. (2) Hecho validado por una persona = documento o relación con verificacion verificado (o refutado) y verificado_por. Al re-extraer, el extractor no los borra ni sobrescribe esos campos; si su ancla cambió, lo informa como cambiado y nada más. Señalar cambiados = el informe de la extracción lista los nodos y relaciones cuyas anclas da como changed sldb.api check_anchors (o check_doc_anchors). (3) Comprobación de sldb: cada commit nombrado es ancestro de origin/main de sldb, y sldb.api.code.code_facts sobre tests/fixtures/blog_app da los facts de C1 a C4 (lo midió el tester de sldb: 33 facts con span y source_hash). (4) Reglas de mapeo sobre el fixture: ApiOperationDoc de router.register(prefix, PostViewSet) en blog/urls.py más el decorador action(detail=True, methods=[post]) del método publish; HandlerDoc = PostViewSet.publish, observado porque es un símbolo leído tal cual; executes hacia el DomainOperationDoc Post.publish, por los calls del handler; governed_by hacia el PolicyDoc can_publish, porque Post.publish la llama y su resultado decide un raise (si los facts no dan la condición, la regla usa solo la llamada y lo dice en la descripción); StateDoc por cada miembro de la clase TextChoices Post.Status; transitions de Post.publish hacia PUBLISHED solo si un fact de assignment lo muestra, y si no, no se crea y el informe que devuelve la extracción la lista como no derivada (desconocidos es solo para campos propios nulos de un nodo, según domain.py); DomainEntityDoc Post por su base models.Model; persisted_in hacia TableDoc posts por Meta.db_table; writes de Post.publish hacia posts por su llamada a save. La Validation 6 se lee con (1): ningún nodo o relación extraído queda con origen inferido ni con verificacion distinta de sin_verificar.

## Validation

_List the checks required before this task can close._

- Sobre tests/fixtures/blog_app, el extractor produce los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano (tests/models/test_blog_chain.py), con los mismos tipos y relaciones, incluidas POST /posts/{id}/publish desde router.register y @action(detail=True, methods=[post]), handled_by, executes hacia Post.publish, governed_by por can_publish, los estados de Status y persisted_in por Meta.db_table.
- Las tablas, columnas y claves del SQL de Postgres del fixture (PK id con IDENTITY y la FK de author_id por ALTER TABLE ADD CONSTRAINT) llegan al grafo desde los hechos constraint de code_facts, con el extra postgres instalado.
- Cada nodo y relación extraído lleva archivo, línea y source_hash de code_facts, y su procedencia en la taxonomía canónica.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación del árbol del store).
- Modificar un archivo fuente en una copia temporal del fixture y volver a extraer señala como cambiados los nodos anclados a ese archivo, sin borrar ni sobrescribir documentos o relaciones con verificacion verificado.
- Ningún nodo o relación extraído queda con origen inferido o declarado, ni con verificacion distinta de sin_verificar.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes.
- grep -rnE "tree_sitter|import ast|from ast|pglast|sldb\\.code\\b|import pron|spec2viz" src/specir/extract no devuelve nada, y TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py sale con rc 0.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider con las pruebas nuevas del extractor y tests/models/test_blog_chain.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

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
- Sobre tests/fixtures/blog_app, el extractor produce los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano (tests/models/test_blog_chain.py), con los mismos tipos y relaciones, incluidas POST /posts/{id}/publish desde router.register y @action(detail=True, methods=[post]), handled_by, executes hacia Post.publish, governed_by por can_publish, los estados de Status y persisted_in por Meta.db_table.
- Las tablas, columnas y claves del SQL de Postgres del fixture (PK id con IDENTITY y la FK de author_id por ALTER TABLE ADD CONSTRAINT) llegan al grafo desde los hechos constraint de code_facts, con el extra postgres instalado.
- Cada nodo y relación extraído lleva archivo, línea y source_hash de code_facts, y su procedencia en la taxonomía canónica.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación del árbol del store).
- Modificar un archivo fuente en una copia temporal del fixture y volver a extraer señala como cambiados los nodos anclados a ese archivo, sin borrar ni sobrescribir documentos o relaciones con verificacion verificado.
- Ningún nodo o relación extraído queda con origen inferido o declarado, ni con verificacion distinta de sin_verificar.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes.
- grep -rnE "tree_sitter|import ast|from ast|pglast|sldb\\.code\\b|import pron|spec2viz" src/specir/extract no devuelve nada, y TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py sale con rc 0.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider con las pruebas nuevas del extractor y tests/models/test_blog_chain.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

