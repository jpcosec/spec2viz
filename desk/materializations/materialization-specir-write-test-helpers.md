---
sldb:
  by: agent
  at: '2026-11-15T05:29:12Z'
  authority: generated
  via: create_document
id: materialization-specir-write-test-helpers
title: specIR write test helpers
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
target_kind: test_file
target_identity: tests/mcp/writing.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR write test helpers

## Intent

Helpers that read the repo's own documents (atoms, lifecycle RelationDocs, RelationTypeDocs) through the tools, as the starting payloads of the write tests.
