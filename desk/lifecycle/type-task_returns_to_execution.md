---
name: task_returns_to_execution
direction: directed
cardinality: many_to_many
axis: HOW
source_types:
- RitualDoc
target_types:
- RitualDoc
condition: ''
---

# Task returns to execution

## Description

A task that cannot finish testing goes back to the execution ritual, by hand, with a reason.
