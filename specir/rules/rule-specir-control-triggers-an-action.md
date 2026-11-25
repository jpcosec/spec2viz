---
subject: model <= InterfaceControlDoc
where: ''
condition: 'any(rel:triggers: model <= InterfaceActionDoc)'
severity: alert
moment: on_check
message: The interface control triggers no interface action.
---

# An interface control triggers an action