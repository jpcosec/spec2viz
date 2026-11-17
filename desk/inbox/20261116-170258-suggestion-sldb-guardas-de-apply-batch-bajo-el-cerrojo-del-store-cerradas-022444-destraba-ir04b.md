---
sldb:
  by: agent
  at: '2026-11-17T01:22:24Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T17:02:58'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:22:21'
---

# sldb: guardas de apply_batch bajo el cerrojo del store cerradas (022444), destraba IR04b

_Describe the incoming message with enough evidence to triage._

La tarea de sldb 022444 está cerrada: código f8ad9000, closeout 38b891a0, integrada por wA:p1 sobre origin 8bbfed68 (el push lo avisa el integrador). apply_batch toma store_lock(store, wait=True) alrededor de la prevalidación y de toda la transacción. update pasa expected_source_hash/expected a tx.update. delete, move y untrack quedan cubiertos porque la prevalidación corre bajo el mismo cerrojo. StoreIOLock es reentrante por proceso. Si dos procesos usan el mismo guarda, uno escribe y el otro recibe ConflictError sin escritura parcial. Las excepciones no cambian: ConflictError para un guarda obsoleto y SLDBStoreError busy sin wait. Limitación: la exclusión es por proceso, no por hilo. Sigue la tarea del lote inverso (apply_batch devuelve report.inverse), que es lo que pide IR04b; la despacho ahora.
