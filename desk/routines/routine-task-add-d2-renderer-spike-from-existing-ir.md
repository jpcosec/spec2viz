---
# routine-xxx
id: routine-task-add-d2-renderer-spike-from-existing-ir
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-add-d2-renderer-spike-from-existing-ir-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-add-d2-renderer-spike-from-existing-ir-execution-ready
- operator-task-add-d2-renderer-spike-from-existing-ir-activate
- checklist-task-add-d2-renderer-spike-from-existing-ir-testing-ready
- operator-task-add-d2-renderer-spike-from-existing-ir-ready-for-testing
- checklist-task-add-d2-renderer-spike-from-existing-ir-closeout-ready
- operator-task-add-d2-renderer-spike-from-existing-ir-close
# Edge identifiers composing the graph
edges:
- edge-task-add-d2-renderer-spike-from-existing-ir-execution-to-activate
- edge-task-add-d2-renderer-spike-from-existing-ir-activate-to-testing
- edge-task-add-d2-renderer-spike-from-existing-ir-testing-to-ready
- edge-task-add-d2-renderer-spike-from-existing-ir-ready-to-closeout
- edge-task-add-d2-renderer-spike-from-existing-ir-closeout-to-close
- edge-task-add-d2-renderer-spike-from-existing-ir-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add D2 renderer spike from existing IR

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add D2 renderer spike from existing IR.
