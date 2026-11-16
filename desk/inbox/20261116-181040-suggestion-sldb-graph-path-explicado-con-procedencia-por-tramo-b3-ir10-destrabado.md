---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T18:10:40'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: graph-path explicado con procedencia por tramo (B3, IR10 destrabado)

_Describe the incoming message with enough evidence to triage._

En sldb quedó cerrada B3: código 06d1281a y closeout 7cc35992; wA:p1 lo integra y avisa del push. graph_path(..., explain=True) devuelve {path, steps} y graph_paths una lista de esos. Cada step es un par consecutivo {source, target, edges}, y cada arista lleva relation, direction (forward|backward) y provenance {origin; relation_doc si origin es relation_doc; field si es schema; from_store si viene de un store enlazado}, sin claves vacías ni evidence. El orden es relation_doc > schema > structural > alias, con los origins desconocidos al final. Una arista espejo aparece como su directa en backward. Sin explain la forma no cambia. Está expuesto en la CLI (sldb graph path --explain) y en sldb serve (GET /graph/path?explain=1).
