---
# routine-xxx
id: routine-task-add-render-antonia-html-command
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-add-render-antonia-html-command-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-add-render-antonia-html-command-execution-ready
- operator-task-add-render-antonia-html-command-activate
- checklist-task-add-render-antonia-html-command-testing-ready
- operator-task-add-render-antonia-html-command-ready-for-testing
- checklist-task-add-render-antonia-html-command-closeout-ready
- operator-task-add-render-antonia-html-command-close
# Edge identifiers composing the graph
edges:
- edge-task-add-render-antonia-html-command-execution-to-activate
- edge-task-add-render-antonia-html-command-activate-to-testing
- edge-task-add-render-antonia-html-command-testing-to-ready
- edge-task-add-render-antonia-html-command-ready-to-closeout
- edge-task-add-render-antonia-html-command-closeout-to-close
- edge-task-add-render-antonia-html-command-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add render-antonia-html command

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add render-antonia-html command.
