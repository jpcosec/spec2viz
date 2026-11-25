---
subject: model <= InterfaceActionDoc
where: ''
condition: 'any(rel:invokes: model <= ApiOperationDoc)'
severity: error
moment: on_check
message: An interface action invokes no existing API operation.
---

# An interface action invokes an operation of the API