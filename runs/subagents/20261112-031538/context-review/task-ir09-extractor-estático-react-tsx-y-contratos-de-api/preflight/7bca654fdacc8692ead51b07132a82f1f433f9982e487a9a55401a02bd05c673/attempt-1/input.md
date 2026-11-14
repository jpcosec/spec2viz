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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir09-extractor-estático-react-tsx-y-contratos-de-api: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

