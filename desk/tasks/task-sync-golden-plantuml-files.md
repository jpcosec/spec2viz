---
# task-xxx, unique task identifier
id: task-sync-golden-plantuml-files
# draft | active | blocked | closed
status: active
# Relevant file or doc paths
references: []
# Task identifiers that must complete first
depends_on: []
# Pill identifiers required
pills: []
# Files expected to change
files: []
# Routine identifier for operations
routine: routine-task-sync-golden-plantuml-files
# Checklist identifiers for verification
checklists:
- checklist-task-sync-golden-plantuml-files-execution-ready
- checklist-task-sync-golden-plantuml-files-testing-ready
- checklist-task-sync-golden-plantuml-files-closeout-ready
# Active routine node
current_node: checklist-task-sync-golden-plantuml-files-testing-ready
# Execution history references
history:
- operator-task-sync-golden-plantuml-files-activate
# e.g., system:deskops, topic:cli
tags:
- workspace:desk
- artifact:task
---

# Sync golden PlantUML files

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.

## Scope

_State what is in scope and what is out of scope._

fixtures

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._
