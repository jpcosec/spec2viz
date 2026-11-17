---
sldb:
  by: agent
  at: '2026-11-17T12:30:55Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T09:24:38'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T09:30:51'
---

# sldb: undo_changes servido por sldb mcp (IR04b)

_Describe the incoming message with enough evidence to triage._

La nota 184421 está resuelta en sldb: código d0ee07a3 y closeout 02ea724e. wA:p1 lo integra y avisa del push. sldb mcp sirve la tool undo_changes. Cada apply_changes exitoso apila su lote inverso en una pila por sesión del servidor, en memoria. undo_changes(steps=1) deshace del más reciente al más antiguo con las guardas de apply_batch y responde así:
- stale (sin escribir) si alguien escribió entre medio, y el lote queda en la pila;
- con steps>1 se detiene en el primer fallo y devuelve undone, written y remaining;
- nothing_to_undo si no hay nada que deshacer.
El contenido vuelve igual. La procedencia sldb.by/at/via registra al actor que deshizo. IR04b se reduce a verificarlo desde specIR.
