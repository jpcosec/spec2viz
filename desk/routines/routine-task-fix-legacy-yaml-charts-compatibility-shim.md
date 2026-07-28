---
# routine-xxx
id: routine-task-fix-legacy-yaml-charts-compatibility-shim
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-fix-legacy-yaml-charts-compatibility-shim-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-execution-ready
- operator-task-fix-legacy-yaml-charts-compatibility-shim-activate
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-testing-ready
- operator-task-fix-legacy-yaml-charts-compatibility-shim-ready-for-testing
- checklist-task-fix-legacy-yaml-charts-compatibility-shim-closeout-ready
- operator-task-fix-legacy-yaml-charts-compatibility-shim-close
# Edge identifiers composing the graph
edges:
- edge-task-fix-legacy-yaml-charts-compatibility-shim-execution-to-activate
- edge-task-fix-legacy-yaml-charts-compatibility-shim-activate-to-testing
- edge-task-fix-legacy-yaml-charts-compatibility-shim-testing-to-ready
- edge-task-fix-legacy-yaml-charts-compatibility-shim-ready-to-closeout
- edge-task-fix-legacy-yaml-charts-compatibility-shim-closeout-to-close
- edge-task-fix-legacy-yaml-charts-compatibility-shim-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Fix legacy yaml_charts compatibility shim

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Fix legacy yaml_charts compatibility shim.
