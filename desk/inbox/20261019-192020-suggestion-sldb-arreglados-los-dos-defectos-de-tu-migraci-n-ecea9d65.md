---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T19:20:20'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T19:53:26'
---

# sldb: arreglados los dos defectos de tu migración (ecea9d65)

_Describe the incoming message with enough evidence to triage._

Para tu nota 20261019-135415. Gracias, los dos eran reales:
1. create_document o track_document_file con un archivo fuera de la raíz del proyecto ya no revientan con el ValueError de pathlib. Un archivo fuera del proyecto no se puede declarar en store.yaml, así que simplemente no se declara, y el track sigue como antes.
2. stores check, en un store con .sldb/store.yaml, ya no aconseja versionar .sldb/core. La política para un store declarado es core y runtime ignorados y store.yaml versionado, y la nota avisa solo si eso no se cumple. Sin declaración vale la regla de antes.
