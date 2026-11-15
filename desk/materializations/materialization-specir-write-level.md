---
sldb:
  by: agent
  at: '2026-11-15T05:29:04Z'
  authority: generated
  via: create_document
id: materialization-specir-write-level
title: specIR write level
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor
target_kind: python_module
target_identity: src/specir/mcp/mutability.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR write level

## Intent

The write level is fixed when the server starts, 0 by default; a call above it is refused from its typed arguments before the store is read; level 3 (models as code) is never served.
