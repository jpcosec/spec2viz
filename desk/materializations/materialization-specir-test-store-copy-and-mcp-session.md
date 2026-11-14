---
sldb:
  by: agent
  at: '2026-11-14T15:13:43Z'
  authority: generated
  via: create_document
id: materialization-specir-test-store-copy-and-mcp-session
title: specIR test store copy and MCP session
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: test_file
target_identity: tests/conftest.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR test store copy and MCP session

## Intent

The tests mount an isolated copy of this repo's real store with the public sldb CLI, link deskops and spec2viz in place, and drive the real server over stdio with the real MCP client.
