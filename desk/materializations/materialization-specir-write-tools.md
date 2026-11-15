---
sldb:
  by: agent
  at: '2026-11-15T05:28:59Z'
  authority: generated
  via: create_document
id: materialization-specir-write-tools
title: specIR write tools
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
- atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2
target_kind: python_module
target_identity: src/specir/mcp/write_tools.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR write tools

## Intent

propose_changes builds the apply_batch batch with server-filled guards and writes nothing; apply_changes applies it with sldb.api.apply_batch and returns the rejection cause; what SLDB lacks is declared pending with its note.
