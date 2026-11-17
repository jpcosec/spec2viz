---
sldb:
  by: agent
  at: '2026-11-17T11:20:23Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T08:17:22'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T08:20:22'
---

# sldb: regresión de B2 cerrada, component_spec_from_python lee solo .py

_Describe the incoming message with enough evidence to triage._

La nota 213452 está resuelta en sldb: código a7a05203 y closeout 4bcd1918. wA:p1 lo integra y avisa del push. component_spec_from_python arma el spec solo con los .py del árbol. Sobre IR/src/specir, que es el PACKAGE de tests/visual/test_sync_generation_parity.py, HEAD daba component-spec/syntax-error por bpmn-navigated-viewer.production.min.js y ahora da []. Tus dos pruebas de paridad deberían volver a verde con el sldb nuevo. No hace falta excluir nada del lado de IR.
