---
id: task-ir10-reglas-semanticas-y-analisis-de-impacto
status: deferred
summary: 'Candidata diferida: reglas RuleDoc que detectan cadenas interfaz, API, operación
  y datos rotas, y una operación de impacto con evidencia y severidad.'
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:impacto
current_node: ''
history: []
references: []
depends_on:
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-ir08-extractor-estatico-django-drf-y-sql
- task-ir09-extractor-estatico-react-tsx-y-contratos-api
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR10 Reglas semánticas y análisis de impacto

## Rationale

_Explain why this task exists or the business driver behind it._

Candidata diferida. Tener el grafo no basta: el agente necesita que el sistema le diga qué se rompe cuando cambia un campo, un endpoint o una regla, y con qué evidencia. Es el criterio de éxito 4 de los fundamentos.

## Goal

_Describe the concrete result this task must produce._

Un conjunto de reglas RuleDoc que detectan brechas entre capas y una operación de análisis de impacto, expuesta por MCP, que devuelve los elementos afectados por un cambio con el camino que lo justifica.

## Scope

_State what is in scope and what is out of scope._

Dentro: reglas RuleDoc, distribuidas por specIR como documentos, para cadenas rotas interfaz, API, operación, datos: acción sin operación de API, campo de interfaz ausente del serializer, operación sin handler, entidad sin persistencia, política sin representación en la interfaz; cada hallazgo con severidad, regla que lo produce y evidencia; operación de impacto: dado un nodo (campo, endpoint, regla, tabla), los nodos afectados en las demás capas con el camino de relaciones que lo explica y la procedencia de cada tramo; tool MCP de solo lectura para ambas.
Fuera: proponer parches o cambios de código; aplicar correcciones al grafo; reglas que requieran ejecutar la aplicación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.code (el tipo se asigna al autorar la tarea activa con deskops add task --task-type; en una candidata diferida task_type queda vacío). Las reglas se escriben en el lenguaje de reglas de SLDB y se evalúan con sus operaciones públicas de reglas; el impacto se calcula con las operaciones públicas de recorrido del grafo de SLDB. Si el lenguaje de reglas no alcanza para alguna brecha, la carencia se resuelve en SLDB, no con lógica paralela en specIR.

## Validation

_List the checks required before this task can close._

- Por cada regla hay un store de prueba con la brecha sembrada y la evaluación la reporta con su severidad, la regla y los documentos implicados.
- Sobre el grafo completo del blog sin brechas sembradas, las reglas no reportan hallazgos.
- Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton entre los afectados, con el camino completo de relaciones.
- Cada tramo del camino devuelto lleva su procedencia, y un camino que pasa por una relación inferida se señala como tal.
- Las tools de reglas e impacto no escriben en el store (comparación del árbol antes y después).
- Ninguna respuesta incluye un parche ni una modificación propuesta.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y un agente puede responder por MCP qué partes de la interfaz afecta un cambio en un campo, un endpoint o una regla del blog.
