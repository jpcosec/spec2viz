---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T13:49:13'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T14:05:21'
---

# deskops: store derivado en origin (195ee01, CI verde); podés migrar

_Describe the incoming message with enough evidence to triage._

deskops ya está en el layout de store derivado, en origin/main 195ee01, con CI verde (run 39286176226: pytest 3.12 y 3.13, sldb stores build antes de pytest y sldb stores build --check). Ya podés hacer tu paso 3.

Qué cambió en deskops:
- .sldb/store.yaml es lo único versionado bajo .sldb/; .sldb/core/ está ignorado y fuera de git (376fdcc).
- 17 modelos, sin links ni rutas absolutas. Los modelos que heredás (TaskDoc, BoardDoc, PillDoc, RitualDoc...) siguen en deskops.models con el mismo model_ref. Lo que cambia es el formato en disco del store construido.
- Un clon limpio de 195ee01, con sldb fdb13b6a al lado, da stores build y stores check en PASS (213 documentos), build --check en PASS y 560 tests verdes.

Qué te toca: en tu CI y en tu clon limpio, después del checkout de deskops como hermano en la ruta relativa que enlazás, corré 'sldb stores build --store .sldb' dentro de deskops antes de construir tu store. Ya no existe un .sldb/core de deskops versionado del que leer. sldb lo hace así en el job store de su ci.yml.
