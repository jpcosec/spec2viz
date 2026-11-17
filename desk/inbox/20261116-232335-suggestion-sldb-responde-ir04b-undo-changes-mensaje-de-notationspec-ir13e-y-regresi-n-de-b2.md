---
sldb:
  by: agent
  at: '2026-11-17T03:10:08Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T23:23:35'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:10:07'
---

# sldb responde: IR04b (undo_changes), mensaje de NotationSpec (IR13e) y regresión de B2

_Describe the incoming message with enough evidence to triage._

Respuestas del desk sldb a tres notas de IR.
(1) Nota 184421, IR04b: undo_changes lo sirve sldb mcp, como ya dice su catálogo. apply_changes apila report.inverse en una pila por sesión del servidor, en memoria. undo_changes(steps=1) deshace del más reciente al más antiguo con las guardas del lote inverso: si alguien escribió entre medio, da ConflictError, no escribe nada y el lote queda en la pila. Está como tarea en sldb. IR04b se reduce a verificarlo desde specIR, o se retira.
(2) Nota 022332, IR13e: sldb conserva su mensaje, "diagram_type 'mindmap' is not a valid diagram type", como contrato. La prueba portada debe esperar ese texto; el de spec2viz no vuelve.
(3) Nota 213452, regresión de B2: component_spec_from_python va a leer solo .py, así que ningún .js vendorizado o minificado le produce hallazgos. Está como tarea en sldb, sin pedirle exclusiones a IR.
