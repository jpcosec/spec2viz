---
sldb:
  by: agent
  at: '2026-11-14T15:13:38Z'
  authority: generated
  via: create_document
id: materialization-specir-stable-addresses
title: specIR stable addresses
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: source_file
target_identity: src/specir/mcp/addresses.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR stable addresses

## Intent

Every document, model and relation type an agent receives carries the SLDB node id (sldb://document/<export id>) minted by sldb.api, never by specIR.
