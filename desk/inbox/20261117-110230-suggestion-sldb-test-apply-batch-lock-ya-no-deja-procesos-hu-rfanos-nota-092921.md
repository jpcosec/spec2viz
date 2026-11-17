---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T11:02:30'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: test_apply_batch_lock ya no deja procesos huérfanos (nota 092921)

_Describe the incoming message with enough evidence to triage._

Resuelto en sldb: 665cdba7 (código) y 8acd5670 (closeout). Una fixture mata y espera a los hijos del test, falle o se interrumpa, y el hijo sale solo si la espera de marks/go pasa de 120 s. Probado con assert fallido, SIGINT, timeout y kill -9 al pytest padre: no queda ningún hijo vivo. Gracias por el aviso.
