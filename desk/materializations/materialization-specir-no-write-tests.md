---
sldb:
  by: agent
  at: '2026-11-14T15:13:47Z'
  authority: generated
  via: create_document
id: materialization-specir-no-write-tests
title: specIR no-write tests
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
target_kind: test_file
target_identity: tests/mcp/test_no_writes.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR no-write tests

## Intent

Calling every read tool leaves the mounted copy, the linked deskops and spec2viz stores and the repo's own store unchanged.
