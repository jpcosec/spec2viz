---
subject: model <= InterfaceFieldDoc
where: ''
condition: 'any(rel:bound_to: model <= ApiFieldDoc)'
severity: error
moment: on_check
message: The interface field is bound to no API field; the serializer does not carry
  it.
---

# An interface field is an attribute of the API