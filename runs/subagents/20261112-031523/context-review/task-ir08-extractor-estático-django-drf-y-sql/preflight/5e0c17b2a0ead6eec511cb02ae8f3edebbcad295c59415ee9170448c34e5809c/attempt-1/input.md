FILE:desk/tasks/task-ir08-extractor-estático-django-drf-y-sql.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:19Z'
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
- src/specir/extract/__init__.py
- src/specir/extract/provenance.py
- src/specir/extract/django_drf.py
- src/specir/extract/sql_schema.py
- tests/extract/test_django_drf.py
- tests/extract/test_sql_schema.py
- tests/extract/test_idempotencia.py
- tests/fixtures/blog_backend/manage.py
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

Un extractor estático que, a partir de una aplicación Django REST Framework y su esquema SQL, produce documentos y relaciones de los tipos de dominio de specIR, cada uno con su evidencia de origen.

## Scope

_State what is in scope and what is out of scope._

Dentro: lectura estática (AST y metadatos, sin ejecutar la aplicación) de rutas y vistas, serializers y sus campos, modelos Django con sus relaciones, y tablas, columnas y claves del esquema SQL; producción de operaciones de API, handlers, entidades de dominio, tablas y las relaciones entre ellos; procedencia por nodo y relación con archivo, línea y hash del fragmento fuente, en la taxonomía decidida en la tarea de procedencia; idempotencia: extraer dos veces el mismo código no cambia el store.
Fuera: frontend; análisis en tiempo de ejecución; reglas de negocio que no se deducen del código, que quedan como desconocidas o marcadas como inferidas; análisis de impacto; cualquier parche al código.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de extracción en el paquete specIR que escribe por la API pública de SLDB con las mismas operaciones validadas que la superficie MCP de escritura; anclas de código de SLDB para ligar cada nodo a su fuente, si la tarea de procedencia lo decide así; fixture: una aplicación Django REST Framework real y pequeña, la del blog de ejemplo, versionada en el repo de specIR.

## Validation

_List the checks required before this task can close._

- Sobre el fixture de la aplicación del blog, el extractor produce los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano, con los mismos tipos y relaciones.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente, y su procedencia en la taxonomía canónica.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación del árbol del store).
- Modificar un archivo fuente del fixture y volver a extraer señala los nodos anclados a ese archivo como cambiados, sin borrar hechos validados por una persona.
- Ningún nodo inferido queda con procedencia de observado o validado.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes.
- El módulo no importa pron ni spec2viz, ni módulos de SLDB fuera de sldb.api.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre el fixture y el grafo de backend y datos del blog se obtiene sin poblarlo a mano.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir08-extractor-estático-django-drf-y-sql: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

