---
sldb:
  by: agent
  at: '2026-11-15T05:29:10Z'
  authority: generated
  via: create_document
id: materialization-specir-write-level-tests
title: specIR write level tests
source_atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor
target_kind: test_file
target_identity: tests/mcp/test_mutability.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR write level tests

## Intent

Level 0 serves no write tool, level 1 refuses rules before evaluating, level 3 is refused at startup, arguments are typed only, no tool writes a Python module.
