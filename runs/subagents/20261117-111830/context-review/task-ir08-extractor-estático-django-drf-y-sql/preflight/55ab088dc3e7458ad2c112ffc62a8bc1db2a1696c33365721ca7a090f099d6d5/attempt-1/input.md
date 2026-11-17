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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir08-extractor-estático-django-drf-y-sql: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

