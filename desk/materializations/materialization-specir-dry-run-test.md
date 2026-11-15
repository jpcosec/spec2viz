---
sldb:
  by: agent
  at: '2026-11-15T05:29:08Z'
  authority: generated
  via: create_document
id: materialization-specir-dry-run-test
title: specIR dry run test
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
target_kind: test_file
target_identity: tests/mcp/test_dry_run.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR dry run test

## Intent

propose_changes answers what would be written and leaves every file of the copy and the linked stores unchanged.
