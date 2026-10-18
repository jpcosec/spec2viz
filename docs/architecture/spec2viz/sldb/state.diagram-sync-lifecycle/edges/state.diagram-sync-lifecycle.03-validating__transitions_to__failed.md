---
source_id: SpecNodeDoc:state.diagram-sync-lifecycle.validating
target_id: SpecNodeDoc:state.diagram-sync-lifecycle.failed
relation_type: transitions_to
condition: ''
attributes:
  'on': load() raises
  guard: spec invalid
---

# validating transitions_to failed

## Notes

load() raises [spec invalid]
