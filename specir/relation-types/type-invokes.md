---
name: invokes
direction: directed
cardinality: many_to_many
axis: HOW
source_types:
- InterfaceActionDoc
target_types:
- ApiOperationDoc
condition: ''
---

# Invokes

## Description

The interface action calls the API operation. An action that invokes no operation of the API does nothing the backend knows of.