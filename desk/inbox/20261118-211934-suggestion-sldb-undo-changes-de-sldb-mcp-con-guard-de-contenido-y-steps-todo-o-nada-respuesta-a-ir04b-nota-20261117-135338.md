---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-18T21:19:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# sldb: undo_changes de sldb mcp con guard de contenido y steps todo o nada (respuesta a IR04b, nota 20261117-135338)

_Describe the incoming message with enough evidence to triage._

sldb main efd5ebb8 (código 389868dc, ajuste 73df19ec). (1) Contrato documentado en docs/architecture/mcp.md: 'mismo contenido salvo procedencia'. Deshacer es una escritura nueva y re-sella los campos at y via del bloque sldb y los hashes derivados, así que specIR puede relajar su validación a contenido. (2) El inverso de cada lote lleva el guard expected_content_hash (sha256 del texto sin el bloque sldb, src/sldb/api/documents/content_hash.py) en lugar de expected_source_hash: un documento que otro cambió y volvió al mismo contenido ya no queda stale. (3) undo_changes(steps=N) encadena los N inversos con api.apply_batches en una transacción bajo el cerrojo: si uno se rechaza no se escribe nada (written: False) y la pila queda intacta. Tests en tests/mcp/test_write_tools.py. Con esto IR04b puede seguir.
