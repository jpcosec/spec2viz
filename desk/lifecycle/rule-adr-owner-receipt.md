---
subject: model <= AtomAdrDoc
where: ''
condition: 'any(^subject: kind = "owner" and verdict = "accepted" and anchor_state
  = "intact")'
severity: error
moment: on_check
message: Un atom.adr lleva un recibo owner aceptado e intacto cuyo sujeto es el ADR
  (deskops review record --kind owner; solo el owner lo dispone accepted).
---

# Recibo de owner de atom.adr
