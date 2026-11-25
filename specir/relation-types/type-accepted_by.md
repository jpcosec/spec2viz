---
name: accepted_by
direction: directed
cardinality: many_to_many
axis: WHY
source_types:
- CapabilityDoc
target_types:
- MaterializationContractDoc
condition: ''
---

# Accepted by

## Description

The materialization contract names the test that accredits the capability (target_identity `<path>::<test name>`). A capability is met when that test passes; no field says so.