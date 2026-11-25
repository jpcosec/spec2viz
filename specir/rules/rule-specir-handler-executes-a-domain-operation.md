---
subject: model <= HandlerDoc
where: ''
condition: 'any(rel:executes: model <= DomainOperationDoc)'
severity: alert
moment: on_check
message: The handler reaches no domain operation.
---

# A handler executes a domain operation