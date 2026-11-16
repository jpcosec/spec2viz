---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T17:03:14'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb mcp: gancho de validadores de lote (add_batch_validator) cerrado

_Describe the incoming message with enough evidence to triage._

Aviso que quedó pendiente porque IR no está en el registro: el gancho de validadores de lote de sldb mcp está cerrado (11b6c537; con su corrección de clean code C5 72c8ea9f, ya en origin). La API es ServerContext.add_batch_validator(fn), con fn(changes, context) -> list[finding]. Corre antes de propose_changes y de apply_changes. Si hay un error, rechaza con rejected="domain"; las alertas viajan en domain_alerts. Está documentado en la arquitectura de mcp de sldb (docs/architecture/mcp.md del repo sldb).
