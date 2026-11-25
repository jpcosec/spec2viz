---
subject: model <= PolicyDoc
where: ''
condition: 'any(^rel:governed_by: any(^rel:executes: any(^rel:handled_by: any(^rel:invokes:
  any(^rel:triggers: model <= InterfaceControlDoc)))))'
severity: alert
moment: on_check
message: No interface control reaches an operation this policy governs.
---

# A policy is represented in the interface