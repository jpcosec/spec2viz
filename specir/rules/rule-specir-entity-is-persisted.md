---
subject: model <= DomainEntityDoc
where: ''
condition: 'any(rel:persisted_in: model <= TableDoc)'
severity: alert
moment: on_check
message: The domain entity is persisted in no table.
---

# A domain entity is persisted