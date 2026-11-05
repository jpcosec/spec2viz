---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-11-04T23:36:58'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: el store pasa a .sldb versionado y .sldb_cache ignorada; journal retirado

_Describe the incoming message with enough evidence to triage._

sldb c420809c (2026-11-04) implementa la decisión del dueño del 2026-10-29: el store es .sldb/ versionado (store.yaml + core/) y .sldb_cache/ hermana, regenerable e ignorada. (a) Lo que antes estaba en .sldb/runtime/ (edges, sections, semantic, graphs, locks) vive ahora en .sldb_cache/; quien leía esas rutas a mano debe actualizarlas. (b) El journal se retiró: api.journal() devuelve vacío y sldb journal show remite a sldb docs history. (c) gitignore_policy cambió de forma y stores check emite stores/core_ignored (error, exit 1) si .sldb/core/ o store.yaml están ignorados y stores/cache_not_ignored (alert) si falta la línea .sldb_cache/. (d) Ya corrí sldb stores migrate-layout en este repo y commiteé .gitignore y .sldb/core.
