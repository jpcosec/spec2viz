---
sldb:
  by: agent
  at: '2026-11-25T22:00:36Z'
  authority: generated
  via: save_document_payload
id: task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# un invariante entre piezas se escribe como regla sobre los nodos de specIR, y la regla "graph_ui no depende de pron" falla cuando el código la viola

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): lo que tiene que cumplirse entre varias piezas es de specIR, que ya siembra invariantes entre capas como RuleDoc (src/specir/data/rules.yaml). Pero sus diez tipos de relación (data/relation_types.yaml) describen el flujo de una aplicación (triggers, invokes, handled_by...) y ninguno dice que una pieza depende de otra, así que un invariante de arquitectura como "graph_ui no depende de pron" (ADR de sldb pron-is-archived.md) hoy vive en un guardrail en prosa que nada comprueba.

## Goal

_Describe the concrete result this task must produce._

Un tipo de relación de dependencia entre piezas, extraído del código, y la posibilidad de prohibir una dependencia con una regla sembrada.

## Scope

_State what is in scope and what is out of scope._

Dentro: data/relation_types.yaml, data/rules.yaml, el extractor que produce la relación a partir de los imports que entregan los hechos de código de sldb. Fuera: los nodos de un repo de Python (decisión aparte), invariantes que no sean de dependencia.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer sldb/docs/architecture/rules.md y rules-language.md, y cómo src/specir/extract/facts.py lee los hechos de código. La regla se escribe en el lenguaje de reglas de sldb; si le falta un predicado, se pide por el inbox de sldb y no se resuelve en specIR.

Aclaraciones de la revisión: Va después de la tarea del extractor (specir extract describe una librería de Python): parte de main cuando esté integrada. Todo en specIR (/mnt/ssd/proyectos/SLDB_1/IR). Pieza = paquete Python de primer nivel de un repo. Relación: tipo depends_on en data/relation_types.yaml de specIR, de pieza a pieza, sacada de los imports absolutos de los hechos de código de sldb (los relativos quedan dentro de la pieza; los condicionales cuentan). Regla en el lenguaje de reglas de sldb, sembrada en data/rules.yaml de specIR: 'graph_ui no depende de pron', con el archivo y la línea del import en el hallazgo. tests/test_dependency_invariants.py se crea con un fixture de dos paquetes. Si falta un predicado, nota a sldb por inbox y la tarea entrega el tipo y el extractor y deja la regla como pendiente explicada en result-summary. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_dependency_invariants.py

## Done When

_Name the observable condition that makes the task complete._

Con un repo de prueba donde un módulo importa a otro, la extracción deja la relación de dependencia con su origen observado. Una regla sembrada que prohíbe esa dependencia la informa como violación, con el archivo y la línea del import. Quitar el import hace pasar la regla.
