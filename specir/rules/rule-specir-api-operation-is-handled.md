---
subject: model <= ApiOperationDoc
where: ''
condition: 'any(rel:handled_by: model <= HandlerDoc)'
severity: alert
moment: on_check
message: No handler receives this API operation.
---

# An API operation has a handler