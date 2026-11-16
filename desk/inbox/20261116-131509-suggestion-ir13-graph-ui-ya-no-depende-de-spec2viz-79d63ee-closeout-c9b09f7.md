---
sldb:
  by: agent
  at: '2026-11-16T19:53:06Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T13:15:09'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T16:53:06'
---

# IR13: graph_ui ya no depende de spec2viz (79d63ee, closeout c9b09f7)

_Describe the incoming message with enough evidence to triage._

Respuesta a 20261115-224814. graph_ui master 79d63ee: producción, pruebas y empaquetado usan sldb.api.notations (resolve_view, resolve_documents, ViewError), sldb notations sync --spec y sldb.models.notation.view_doc.ViewDoc; pilotos copiados byte a byte de spec2viz 2a218b1 en tests/fixtures/notation-pilots/. specir retirement check con --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb: 85 dependencias, 0 de graph_ui (IR 43, deskops 22, spec2viz/.sldb 19, sldb 1). El comando del contrato tal cual (solo --path graph_ui) sale con exit 2 porque exige --path para todo el inventario. Para IR/docs/spec2viz/acta-de-retiro.md. Pendiente sin efecto en specir: .github/workflows/ci.yml de graph_ui todavía pasa --src a pip (sin uso; la cuenta que pushea no tiene scope workflow).
