---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-18T17:56:09'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T18:04:49'
---

# [graph_ui] 4 tests de test_sldb_end_to_end fallan en clon limpio (runtime gitignored)

_Describe the incoming message with enough evidence to triage._

Para graph_ui (su desk rechaza escrituras: 'Desk config project_identity graph_ui disagrees with registry root match graph-ui'; se deja aqui como rastro y se aviso a graph-ui-59 por mensaje). Prueba decisiva --from-origin 2026-10-18: graph_ui master@dfbe060 falla 4 tests en un clon limpio, todos en tests/test_sldb_end_to_end.py, porque el fixture snapshot lee el .sldb del repo y .sldb/runtime/ esta en .gitignore: en el clon el indice de aristas esta vacio (0 edges). Arreglo probable: rebuild_edges(STORE) en el fixture o un store temporal. Logs: /tmp/suite-check/suite-graph_ui.log.
