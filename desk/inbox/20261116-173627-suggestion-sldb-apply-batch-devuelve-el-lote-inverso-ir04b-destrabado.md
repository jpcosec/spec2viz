---
sldb:
  by: agent
  at: '2026-11-17T01:22:05Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T17:36:27'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:22:03'
---

# sldb: apply_batch devuelve el lote inverso (IR04b destrabado)

_Describe the incoming message with enough evidence to triage._

En sldb quedó cerrada la tarea del lote inverso (inbox 20261115-123855). Código 83c60239 y closeout 56df0b6a; wA:p1 lo integra y avisa del push. BatchReport.inverse trae el lote que deshace lo aplicado: create->delete, update->update con el payload previo, delete->create, move->move de vuelta y track<->untrack. Cada paso lleva expected_source_hash del estado nuevo, salvo el track inverso de un untrack. Deshacer es apply_batch(store, report.inverse): deja payloads e índice como antes y bytes iguales en documentos canónicos; la procedencia sldb.by/at/via puede cambiar. Si alguien escribió entre medio, el inverso se rechaza con ConflictError (o SLDBStoreError si el documento fue recreado) sin escritura parcial. undo_changes del MCP de IR puede exponerlo directamente.
