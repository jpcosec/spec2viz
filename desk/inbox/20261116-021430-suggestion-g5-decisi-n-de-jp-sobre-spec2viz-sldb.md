---
sldb:
  by: agent
  at: '2026-11-16T10:40:47Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T02:14:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T07:40:46'
---

# G5: decisión de JP sobre spec2viz/.sldb

_Describe the incoming message with enough evidence to triage._

Decisión de JP del 2026-11-16 (transmitida por el supervisor): opción A. El store spec2viz/.sldb se archiva junto con el repo spec2viz cuando specir retirement check dé 0; no se reapuntan sus 7 modelos a sldb.models.notation. Registro en spec2viz: atom atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo (desk/atoms/) y la task.decision task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a. Para IR, según el acta: anotarlo en G5 de IR/docs/spec2viz/acta-de-retiro.md, quitar spec2viz/.sldb del universo del comprobador al declarar el retiro y cambiar la federación del store en IR/tests/conftest.py:24 y :80 y IR/tests/test_mcp_extension.py:24 por un fixture.
