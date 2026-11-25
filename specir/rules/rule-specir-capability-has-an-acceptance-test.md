---
subject: model <= CapabilityDoc
where: ''
condition: 'any(rel:accepted_by: model <= MaterializationContractDoc)'
severity: error
moment: on_check
message: The capability has no materialization to a test that accredits it.
---

# A capability has an acceptance test