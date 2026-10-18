---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cabecera-de-trazabilidad-en-las-proyecciones-generadas-mermaid-plantuml-d2.md
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



## Notes

_Add short operational notes about the current routed set._

- Add D2 renderer spike from existing IR [draft] - Prove that spec2viz can target D2 as an additional outward renderer without changing semantic models or compiler behavior.
- Sync golden PlantUML files [draft] - Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.

## Task Details

_Generated from the task references above._

- Cabecera de trazabilidad en las proyecciones generadas (Mermaid, PlantUML, D2) [ready_for_testing] - diagram render antepone a cada salida de texto una linea de comentario con la ruta del spec y el comando de validacion, en la sintaxis de comentario del renderer (%% en Mermaid, ' en PlantUML, # en D2); los goldens y el lint de Mermaid siguen en verde.
