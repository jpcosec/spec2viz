---
name: triggers
direction: directed
cardinality: many_to_many
axis: HOW
source_types:
- InterfaceControlDoc
target_types:
- InterfaceActionDoc
condition: ''
---

# Triggers

## Description

Using the interface control starts the interface action. The control is where the user acts; the action is what the interface does, which other controls may start too.