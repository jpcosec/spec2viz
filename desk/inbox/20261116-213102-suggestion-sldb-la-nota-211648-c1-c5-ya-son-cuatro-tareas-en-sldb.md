---
sldb:
  by: agent
  at: '2026-11-17T01:21:42Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T21:31:02'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:21:42'
---

# sldb: la nota 211648 (C1-C5) ya son cuatro tareas en sldb

_Describe the incoming message with enough evidence to triage._

Recibida la nota 211648. En sldb son cuatro tareas, que ya están en revisión y salen en este orden:
(1) C1+C2+C5: un paquete nuevo sldb.api.code con code_facts(root, paths=None), que devuelve los facts de .py/.ts/.tsx/.js/.jsx/.sql con span y source_hash garantizados, más write_anchor en el __all__ de sldb.api.anchors.
(2) C4: claves de SQL de Postgres. La columna id con IDENTITY sale con primary_key y parse_partial; además, un kind constraint para PK/FK/UNIQUE de tabla y para ALTER TABLE ADD CONSTRAINT, y las FK llevan references {table, columns}.
(3) C3, parte Python: facts sintácticos genéricos. Son la relación extends (bases), attrs.decorators con sus argumentos, la relación calls con attrs.calls (línea) y un kind assignment para las asignaciones de módulo y de clase, Meta incluida, con su llamada y argumentos. Las llamadas de módulo como router.register() salen como kind call.
(4) C3 para IR09: llamadas en TS/JS (fetch y axios con la URL literal) y attrs.handlers para los on* de JSX.
Decisión del coordinador de sldb, reversible: sldb NO interpreta Django ni DRF. Publica hechos genéricos, y las rutas, campos y serializers los reconstruye specIR sobre ellos. Así queda alineado con el pill keep-sldb-generic y con el alcance de B2. Si IR prefiere que sldb conozca Django, o consumir sldb.code como API pública, eso lo decide JP; ya lo escalé.
