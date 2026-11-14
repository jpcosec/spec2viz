---
sldb:
  by: agent
  at: '2026-11-14T15:13:45Z'
  authority: generated
  via: create_document
id: materialization-specir-read-tool-tests
title: specIR read tool tests
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: test_file
target_identity: tests/mcp/test_read_tools.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR read tool tests

## Intent

The read tools are checked against this repo's own desk files and the spec2viz store's files, not against literals.
