---
sldb:
  by: agent
  at: '2026-11-14T15:13:36Z'
  authority: generated
  via: create_document
id: materialization-specir-read-tools-over-sldb-api
title: specIR read tools over sldb api
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: source_file
target_identity: src/specir/mcp/read_tools.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR read tools over sldb api

## Intent

Each read tool wraps the sldb.api operation the IR01 audit marks available (registry, select_documents, runtime_document, edges_from/edges_to, collect_neighborhood_by_direction, run_view, resolve_view, check_store/check_edges) and answers JSON with stable addresses.
