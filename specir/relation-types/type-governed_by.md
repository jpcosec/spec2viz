---
name: governed_by
direction: directed
cardinality: many_to_many
axis: WHY
source_types:
- DomainOperationDoc
target_types:
- PolicyDoc
condition: ''
---

# Governed by

## Description

The domain operation may run only as the policy allows.