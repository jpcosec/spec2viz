---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-from-graph-proyecta-el-grafo-de-fuente-python-de-sldb-label-y-kind-del-codigo-filtro-por-modulo-rela.md
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

- from-graph proyecta el grafo de fuente Python de sldb: label y kind del codigo, filtro por modulo, relaciones tal cual [draft] - spec2viz diagram from-graph lee del nodo node-link el label (ast.name o ast.module), el kind (semantics.kind declarado; si no, la clase AST: module, class, function...), acepta --module-prefix (repetible) que recorta nodos y deja fuera toda arista o contains con un extremo fuera del alcance, conserva los nombres de relacion tal cual (contains anida, el resto son aristas) y la salida valida con spec2viz diagram validate.
