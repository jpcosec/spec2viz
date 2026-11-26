---
sldb:
  by: agent
  at: '2026-11-26T00:25:05Z'
  authority: generated
  via: save_document_payload
id: task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de
status: ready_for_testing
summary: ''
tags: []
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- src/specir/cli.py
- src/specir/data/relation_types.yaml
- src/specir/data/rules.yaml
- src/specir/extract/__init__.py
- src/specir/extract/dependencies.py
- src/specir/extract/plan.py
- src/specir/extract/write.py
- src/specir/models/__init__.py
- src/specir/models/domain.py
- tests/fixtures/dep_pieces/graph_ui/__init__.py
- tests/fixtures/dep_pieces/graph_ui/app.py
- tests/fixtures/dep_pieces/graph_ui/view.py
- tests/fixtures/dep_pieces/pron/__init__.py
- tests/fixtures/dep_pieces/pron/core.py
- tests/models/test_domain_models.py
- tests/test_dependency_invariants.py
- d1648afa17a5cc8964cbd6acb732189ae7623858
depends_on: []
pills: []
files:
- src/specir/cli.py
- src/specir/data/relation_types.yaml
- src/specir/data/rules.yaml
- src/specir/extract/__init__.py
- src/specir/extract/dependencies.py
- src/specir/extract/plan.py
- src/specir/extract/write.py
- src/specir/models/__init__.py
- src/specir/models/domain.py
- tests/fixtures/dep_pieces/graph_ui/__init__.py
- tests/fixtures/dep_pieces/graph_ui/app.py
- tests/fixtures/dep_pieces/graph_ui/view.py
- tests/fixtures/dep_pieces/pron/__init__.py
- tests/fixtures/dep_pieces/pron/core.py
- tests/models/test_domain_models.py
- tests/test_dependency_invariants.py
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
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

Intento 2: la entrega del intento 1 (commit 4256522, rama deskops/deskops-e-aefda88c6e62) no entra en main porque choca con 7314305 (CapabilityDoc) en src/specir/data/relation_types.yaml y tests/models/test_domain_models.py: los dos agregan entradas en el mismo lugar. Parte de main, trae los cambios de 4256522 con git cherry-pick 4256522 y, en esos dos archivos, conserva las entradas de ambos. Corre tests/test_dependency_invariants.py y tests/models/test_domain_models.py. Commit sin trailer Task-Id.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_dependency_invariants.py

## Done When

_Name the observable condition that makes the task complete._

Con un repo de prueba donde un módulo importa a otro, la extracción deja la relación de dependencia con su origen observado. Una regla sembrada que prohíbe esa dependencia la informa como violación, con el archivo y la línea del import. Quitar el import hace pasar la regla.
