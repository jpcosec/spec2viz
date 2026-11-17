---
sldb:
  by: agent
  at: '2026-11-17T11:10:55Z'
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

Un mapeo de dominio que, a partir de los hechos que los readers de sldb extraen del código del frontend (TypeScript, TSX y JavaScript, React incluido) y de los contratos de API disponibles, produce los elementos de interfaz del grafo de specIR y los vincula a las operaciones de backend, con evidencia de origen. specIR no escribe extractores: mapea hechos de sldb a su dominio.

## Scope

_State what is in scope and what is out of scope._

Dentro: mapeo de los facts de sldb sobre archivos TS, TSX y JS del frontend (componentes y propiedades, controles, handlers de eventos, estados locales declarados, llamadas HTTP) a controles, acciones, estados y las relaciones triggers e invokes hacia operaciones de API; resolución de cada llamada contra los contratos de API disponibles (por ejemplo OpenAPI) y contra las operaciones ya presentes en el grafo; evidencia de origen por nodo y relación con archivo, línea y hash, tomada de las anclas de sldb; idempotencia. Fuera: leer o analizar código TS, TSX o JS (es de sldb: readers y facts, tarea espejo B2); observación del DOM o de eventos en ejecución; comportamiento dinámico que no se deduce del código, que no se afirma: se marca como inferido o se deja como desconocido; generación o modificación de código de interfaz. Si un reader o un fact no existe en sldb, se pide por el desk de sldb y no se reimplementa en specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de mapeo en el paquete specIR (specir.extract) que consume solo la API pública de sldb: los facts y anclas del reader de frontend de sldb/code y las operaciones validadas de escritura de sldb. Ese reader se apoya en TypeScript (indicación de JP del 2026-11-16: es fácil y cubre todo el frontend), así que da facts de archivos TS, TSX y JS con la misma forma, y el mapeo no distingue por extensión. Sin analizador propio de TS, TSX, JSX ni JS en specIR. Los vínculos a backend se resuelven contra las operaciones de API que ya están en el grafo (pobladas a mano o por el mapeo de backend). Fixture: el frontend React del blog de ejemplo. Depende de la tarea espejo B2.

## Validation

_List the checks required before this task can close._

- Sobre el fixture del blog, el extractor produce PublishButton, PublishAction y su relación con la operación de API de publicar, con los tipos de la tarea de tipos de dominio.
- Los facts de archivos .ts, .tsx y .js del fixture se mapean con el mismo código, sin ramas por extensión; si el fixture no tiene alguna de esas extensiones, la prueba lo declara en vez de suponerlo.
- Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente.
- Una llamada HTTP cuya URL no se resuelve estáticamente produce una relación marcada como inferida o un hueco declarado, nunca una relación observada.
- Una llamada a un endpoint que no existe en el grafo queda registrada como brecha, no se descarta ni se inventa la operación.
- Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.
- Las relaciones extraídas pasan la validación de sus RelationTypeDoc.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre el fixture, la mitad de interfaz de la cadena de publicar un post se obtiene sin poblarla a mano y specIR no contiene ningún analizador propio de TS, TSX, JSX ni JS.
