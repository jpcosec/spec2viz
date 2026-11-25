---
sldb:
  by: agent
  at: '2026-11-25T22:45:56Z'
  authority: generated
  via: create_document
id: task-se-borra-el-registro-del-retiro-de-spec2viz-src-specir-visual-retirement-py-y-el-comando-specir-reti
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# se borra el registro del retiro de spec2viz, src/specir/visual/retirement.py y el comando specir retirement

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo R1. spec2viz se declaró retirado el 2026-11-23. El módulo que auditaba ese retiro (344 líneas) y el grupo de comandos retirement de cli.py (línea 186) ya no tienen qué auditar. Es legado.

## Goal

_Describe the concrete result this task must produce._

Que specIR no tenga código ni comandos sobre el retiro de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/visual/retirement.py, el grupo retirement de src/specir/cli.py, sus pruebas, su mención en la ayuda y en la skill. Fuera: docs/spec2viz/ (queda como acta histórica) y cualquier otro comando.

## Implementation Path

_Outline the expected implementation route or affected surface._

Buscar con grep toda importación y mención de retirement antes de borrar. Si otra pieza usa una función del módulo, se detiene y se informa; no se mueve la función a otro lado sin decirlo.

## Validation

_List the checks required before this task can close._

- ! test -e src/specir/visual/retirement.py
- ! grep -rn 'visual.retirement' src tests
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

No existe src/specir/visual/retirement.py, specir --help no lista retirement, ningún archivo de src/ ni de tests/ importa specir.visual.retirement, y la suite pasa.
