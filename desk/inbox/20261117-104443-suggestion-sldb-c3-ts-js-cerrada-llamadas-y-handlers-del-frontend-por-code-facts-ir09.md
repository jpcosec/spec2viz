---
sldb:
  by: agent
  at: '2026-11-17T14:07:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T10:44:43'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T11:07:56'
---

# sldb: C3 TS/JS cerrada, llamadas y handlers del frontend por code_facts (IR09)

_Describe the incoming message with enough evidence to triage._

La parte TS/JS de C3 (nota 211648) está cerrada en sldb: código 0590ed11 y closeout 3b3c51fe. wA:p1 lo integra y avisa del push. sldb.api.code.code_facts da para .ts, .tsx, .js y .jsx:
- attrs.calls con {name, line, first_arg, canonical}. first_arg es el primer literal sin comillas, por ejemplo /api/posts en fetch o axios.get; si es un template con expresiones, da null.
- name canónico desde el árbol: puntos, () para llamadas intermedias, (fn) para anónimas, [] para índices; sin espacios, await ni type args. Ejemplos: api.get, fetch().then.
- Si la cadena empieza en un array, binario, new o literal: canonical: false y el texto de la expresión. Son ~5 % en tres frontends reales y no entran en la relación calls.
- attrs.handlers {element, attribute, handler} en los componentes, para on + mayúscula.
Con C1, C2, C3 Python, C3 TS y C4 cerrados, IR08, IR09 e IR10 tienen lo que pidieron a sldb.api.
