---
name: transitions
direction: directed
cardinality: many_to_many
axis: WHEN
source_types:
- DomainOperationDoc
target_types:
- StateDoc
condition: ''
---

# Transitions

## Description

The domain operation moves its entity into the target state.