---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-add-d2-renderer-spike-from-existing-ir.md
- desk/tasks/task-fix-legacy-yaml-charts-compatibility-shim.md
- desk/tasks/task-sync-golden-plantuml-files.md
- desk/tasks/task-add-render-antonia-html-command.md
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
- Fix legacy yaml_charts compatibility shim [draft] - Add a top-level compatibility shim so that import yaml_charts works and emits a deprecation warning pointing users to the new spec2viz package.
- Sync golden PlantUML files [draft] - Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.

## Task Details

_Generated from the task references above._

- Add D2 renderer spike from existing IR [draft] - Prove that spec2viz can target D2 as an additional outward renderer without changing semantic models or compiler behavior.
- Fix legacy yaml_charts compatibility shim [draft] - Add a top-level compatibility shim so that import yaml_charts works and emits a deprecation warning pointing users to the new spec2viz package.
- Sync golden PlantUML files [draft] - Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.
- Add render-antonia-html command [active] - Triage and resolve the inbox message promoted from `desk/inbox/20260727-204635-suggestion-add-render-antonia-html-command.md`.
