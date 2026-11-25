---
name: executes
direction: directed
cardinality: many_to_many
axis: HOW
source_types:
- HandlerDoc
target_types:
- DomainOperationDoc
condition: ''
---

# Executes

## Description

The handler runs the domain operation. The operation is the capability; the handler is one of the ways to reach it.