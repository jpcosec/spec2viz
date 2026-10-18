---
source_id: SpecNodeDoc:state.diagram-type-lifecycle.parsed_dict
target_id: SpecNodeDoc:state.diagram-type-lifecycle.error
relation_type: transitions_to
condition: ''
attributes:
  'on': TypeAdapter.validate_python()
  guard: schema mismatch
  action: raise ParseError
---

# parsed_dict transitions_to error

## Notes

TypeAdapter.validate_python() [schema mismatch] / raise ParseError
