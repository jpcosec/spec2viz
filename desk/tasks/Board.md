---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-diagram-sync-notation-borra-la-categoria-y-la-nav-del-catalogo-notation-por-vista-en-vistas-yml.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# spec2viz Board

## Purpose

_Explain what this board routes and why it exists._

Enruta el trabajo de spec2viz (specs de diagrama, notacion declarativa, sync al store sldb, catalogo) por los rituales execution, testing y closeout del ciclo de vida de deskops.

## Notes

_Add short operational notes about the current routed set._

Las tasks de 2026-05 (spike D2, goldens PlantUML, renderer antonIA) y las de 2026-10 (vocabulario visual, contrato con graph_ui, atributos de arista, empaquetado, trazabilidad, grafo Python) estan cerradas por closeout commit. No hay tasks abiertas. El catalogo vivo es graph_ui sobre el store sldb; el bundle HTML es el export estatico.

## Task Details

_Generated from the task references above._

- diagram sync --notation borra la categoria y la nav del catalogo; notation por vista en vistas.yml [ready_for_testing] - diagram sync conserva category, nav y desc del catalogo cuando no se le pasan; vistas.yml acepta notation: <nombre|ruta> por vista (ruta relativa al vistas.yml, nombre contra las notaciones del store) y catalog sync lo respeta; notacion inexistente o de otro tipo da error tipado en catalog validate y catalog sync.
