---
sldb:
  by: agent
  at: '2026-11-14T15:13:34Z'
  authority: generated
  via: create_document
id: materialization-specir-mcp-package
title: specIR MCP package
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: source_file
target_identity: src/specir/mcp/__init__.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR MCP package

## Intent

The specir.mcp package exposes the read tools as thin MCP adapters over sldb.api, with no own edge index, traversal or predicate parser.
