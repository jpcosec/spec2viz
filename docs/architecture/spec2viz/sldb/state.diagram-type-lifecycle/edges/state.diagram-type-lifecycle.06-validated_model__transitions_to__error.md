---
source_id: SpecNodeDoc:state.diagram-type-lifecycle.validated_model
target_id: SpecNodeDoc:state.diagram-type-lifecycle.error
relation_type: transitions_to
condition: ''
attributes:
  'on': validate()
  guard: broken refs
  action: raise ValidationError
---

# validated_model transitions_to error

## Notes

validate() [broken refs] / raise ValidationError
