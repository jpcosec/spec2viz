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
