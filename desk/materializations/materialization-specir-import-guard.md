---
sldb:
  by: agent
  at: '2026-11-14T15:13:49Z'
  authority: generated
  via: create_document
id: materialization-specir-import-guard
title: specIR import guard
source_atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
target_kind: test_file
target_identity: tests/test_imports.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR import guard

## Intent

The import guard fails when specIR imports pron, spec2viz or an SLDB module outside sldb.api.
