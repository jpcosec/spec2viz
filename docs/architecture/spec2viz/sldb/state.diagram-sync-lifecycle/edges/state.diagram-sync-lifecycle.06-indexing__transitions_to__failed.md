---
source_id: SpecNodeDoc:state.diagram-sync-lifecycle.indexing
target_id: SpecNodeDoc:state.diagram-sync-lifecycle.failed
relation_type: transitions_to
condition: ''
attributes:
  'on': check_edges
  guard: --strict and errors
---

# indexing transitions_to failed

## Notes

check_edges [--strict and errors]
