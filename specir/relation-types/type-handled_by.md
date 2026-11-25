---
name: handled_by
direction: directed
cardinality: many_to_one
axis: HOW
source_types:
- ApiOperationDoc
target_types:
- HandlerDoc
condition: ''
---

# Handled by

## Description

The API operation is received by the backend handler. An operation has one handler; a handler may receive several operations.