---
sldb:
  by: agent
  at: '2026-11-14T15:13:13Z'
  authority: generated
  via: create_document
id: materialization-specir-mcp-read-server-over-stdio
title: specIR MCP read server over stdio
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: source_file
target_identity: src/specir/mcp/server.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR MCP read server over stdio

## Intent

specir-mcp serves the read tools of one SLDB store over stdio as read-only MCP tools with structured JSON answers, so an agent explores the store without writing to it.
