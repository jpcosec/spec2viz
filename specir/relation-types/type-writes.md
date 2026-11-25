---
name: writes
direction: directed
cardinality: many_to_many
axis: WHAT
source_types:
- DomainOperationDoc
target_types:
- DomainEntityDoc
- TableDoc
condition: ''
---

# Writes

## Description

The domain operation changes the entity or the table. Only a domain operation writes; an interface control or a handler that writes directly skips the operation and its policy.