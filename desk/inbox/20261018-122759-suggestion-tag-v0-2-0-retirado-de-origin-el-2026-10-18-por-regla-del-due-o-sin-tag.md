---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-18T12:27:59'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Tag v0.2.0 retirado de origin el 2026-10-18 por regla del dueño: sin tag

_Describe the incoming message with enough evidence to triage._

Tag v0.2.0 retirado de origin el 2026-10-18 por regla del dueño: sin tags, releases ni PyPI hasta que sldb, deskops, spec2viz y graph_ui esten integrados y testeados juntos. Pendiente: re-crear el tag (git tag -a v0.2.0 en el commit que corresponda, o v0.3.0 si la seccion Unreleased del CHANGELOG se promueve) y publicar, cuando el coordinador lo autorice. El workflow .github/workflows/tests.yml sigue corriendo en tags v*.
