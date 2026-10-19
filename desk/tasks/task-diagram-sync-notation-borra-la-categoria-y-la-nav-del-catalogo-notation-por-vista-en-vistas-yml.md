---
id: task-diagram-sync-notation-borra-la-categoria-y-la-nav-del-catalogo-notation-por-vista-en-vistas-yml
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
- 8a16775
- tests/test_catalog_notation.py
- 'verificado en graph_ui: los seis specs bajo sus categorias tras diagram sync --notation'
depends_on: []
pills: []
files: []
task_type: bug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# diagram sync --notation borra la categoria y la nav del catalogo; notation por vista en vistas.yml

## Rationale

_Explain why this task exists or the business driver behind it._

Reporte visual del 2026-10-19: resincronizar un spec con diagram sync --notation deja el SpecDoc sin category/nav (sale en SIN CATEGORIA). Ademas vistas.yml no deja elegir la notacion por vista, asi que hay que correr diagram sync --notation despues de cada catalog sync.

## Goal

_Describe the concrete result this task must produce._

diagram sync conserva category, nav y desc del catalogo cuando no se le pasan; vistas.yml acepta notation: <nombre|ruta> por vista (ruta relativa al vistas.yml, nombre contra las notaciones del store) y catalog sync lo respeta; notacion inexistente o de otro tipo da error tipado en catalog validate y catalog sync.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/sldb_sync.py, spec2viz/cli.py (catalog validate/sync), tests, docs. OUT: graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_sldb_sync.py -q

## Done When

_Name the observable condition that makes the task complete._

Tests en verde: diagram sync --notation conserva el catalogo; una vista con notation propia sincroniza con ella; errores tipados para notacion inexistente o de otro tipo.
