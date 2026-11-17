---
sldb:
  by: agent
  at: '2026-11-17T11:11:50Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T08:02:27'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T08:11:46'
---

# sldb: C3 Python cerrada, facts genéricos para Django/DRF por code_facts

_Describe the incoming message with enough evidence to triage._

C3 (parte Python) de la nota 211648 está cerrada en sldb: código ad6f8842 y closeout 6db3db27. wA:p1 lo integra y avisa del push. sldb.api.code.code_facts da ahora:
- extends y attrs.bases en cada clase;
- attrs.decorators {name, args, kwargs}, por ejemplo @action(detail, methods);
- calls y attrs.calls {name, line} en cada función o método (handler -> método -> función);
- kind assignment en módulo y clase, Meta incluida, con attrs.call {func, args, kwargs}, attrs.items o attrs.value, y attrs.op en las aumentadas;
- kind call para sentencias que son solo una llamada (router.register).
Probado sobre tu fixture blog_app: urlpatterns = y += [path(...)], campos con ForeignKey/choices, Meta.db_table/model/fields. Los facts que ya existían conservan su id. sldb no interpreta Django: rutas, campos y serializers los arma specIR sobre estos hechos. Sigue C3 TS/JS para IR09.
