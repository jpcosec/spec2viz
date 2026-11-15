---
sldb:
  by: agent
  at: '2026-11-15T05:29:06Z'
  authority: generated
  via: create_document
id: materialization-specir-write-tool-tests
title: specIR write tool tests
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
- atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2
target_kind: test_file
target_identity: tests/mcp/test_write_tools.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR write tool tests

## Intent

Propose and apply over a copy of the real store: document and edge cycles, stale proposals rejected, rules named by severity, provenance, edge violations reported, strict xfail for pre-write edge validation.
