---
# task-xxx, unique task identifier
id: task-fix-legacy-yaml-charts-compatibility-shim
# draft | active | blocked | closed
status: draft
# Relevant file or doc paths
references: []
# Task identifiers that must complete first
depends_on: []
# Pill identifiers required
pills: []
# Files expected to change
files: []
# Routine identifier for operations
routine: routine-task-fix-legacy-yaml-charts-compatibility-shim
# Checklist identifiers for verification
checklists:
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-execution-ready
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-testing-ready
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-closeout-ready
# Active routine node
current_node: checklist-task-fix-legacy-yaml-charts-compatibility-shim-execution-ready
# Execution history references
history: []
# e.g., system:deskops, topic:cli
tags:
- workspace:desk
- artifact:task
---

# Fix legacy yaml_charts compatibility shim

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Add a top-level compatibility shim so that import yaml_charts works and emits a deprecation warning pointing users to the new spec2viz package.

## Scope

_State what is in scope and what is out of scope._

compat

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -c 'import yaml_charts' succeeds and prints a deprecation warning.

## Done When

_Name the observable condition that makes the task complete._
