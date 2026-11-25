---
subject: model <= AtomAdrDoc
where: status = "accepted"
condition: 'none(^supersedes: status = "accepted")'
severity: error
moment: on_check
message: Ningún atom.adr accepted tiene un reemplazo completo (supersedes) de otro
  atom.adr accepted; el reemplazado queda superseded. El reemplazo parcial
  (partial_supersedes) lo deja accepted y esta regla lo ignora.
---

# Consistencia de supersedes entre atom.adr
