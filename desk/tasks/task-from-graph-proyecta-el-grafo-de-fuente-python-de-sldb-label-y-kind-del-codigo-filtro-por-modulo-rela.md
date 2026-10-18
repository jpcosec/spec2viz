---
id: task-from-graph-proyecta-el-grafo-de-fuente-python-de-sldb-label-y-kind-del-codigo-filtro-por-modulo-rela
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- 8207dfe
- tests/test_graph_import.py
- desk/atoms/atom-proyeccion-del-grafo-de-fuente-python-de-sldb.md
depends_on: []
pills: []
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# from-graph proyecta el grafo de fuente Python de sldb: label y kind del codigo, filtro por modulo, relaciones tal cual

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb-04 en el inbox (2026-10-18): sldb publica .sldb/runtime/graphs/python-source.graph.json (python_module, python_symbol, python_external; contains, imports, references) y la seccion 5 de su spec de docstrings deja la proyeccion del lado de spec2viz. Hoy from-graph lo lee pero etiqueta con el node id, tipa con el node_type y no filtra por alcance.

## Goal

_Describe the concrete result this task must produce._

spec2viz diagram from-graph lee del nodo node-link el label (ast.name o ast.module), el kind (semantics.kind declarado; si no, la clase AST: module, class, function...), acepta --module-prefix (repetible) que recorta nodos y deja fuera toda arista o contains con un extremo fuera del alcance, conserva los nombres de relacion tal cual (contains anida, el resto son aristas) y la salida valida con spec2viz diagram validate.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/graph_import.py (loader node-link con schema.semantics/ast, node attrs, filtro por prefijo), spec2viz/cli.py (--module-prefix), tests/test_graph_import.py, README, CHANGELOG. OUT: cambios en sldb; que sldb emita el spec.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_graph_import.py -q

## Done When

_Name the observable condition that makes the task complete._

from-graph sobre python-source.graph.json con --module-prefix sldb.selfdoc produce un spec component que valida, con labels del codigo, kinds declarados o AST, sin contains ni aristas colgando; tests verdes.
