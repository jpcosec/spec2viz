---
sldb:
  by: agent
  at: '2026-11-17T01:22:12Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T17:19:15'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:22:10'
---

# sldb serve: fuga de memoria de list_views cerrada

_Describe the incoming message with enough evidence to triage._

Aviso para IR: La fuga de memoria de sldb serve/list_views (nota de graph_ui 20261116-101851) está cerrada en sldb: código 901f5361, closeout b0e4f649, sin pushear todavía (lo integra y pushea wA:p1). list_views lee solo los shards ViewDoc de cada store de la federación transitiva, sin componer el índice federado. compose_edge_index compone una sola vez por clave aunque lleguen peticiones concurrentes en frío. En tests/test_mindmap_deskops.py::test_real_advance_stale_origin_and_types de graph_ui, el RSS máximo pasó de 2,24 GB (falla con el 502) a 104 MB (pasa en 18 s). Para tomarlo, actualiza tu sldb cuando wA:p1 pushee.
