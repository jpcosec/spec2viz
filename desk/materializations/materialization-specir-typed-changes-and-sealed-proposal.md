---
sldb:
  by: agent
  at: '2026-11-15T05:29:01Z'
  authority: generated
  via: create_document
id: materialization-specir-typed-changes-and-sealed-proposal
title: specIR typed changes and sealed proposal
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
- atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2
target_kind: python_module
target_identity: src/specir/mcp/changes.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR typed changes and sealed proposal

## Intent

Typed changes (create, update, delete, assert_edge, retract_edge) and the sealed proposal in apply_batch form that apply_changes takes back unchanged.
