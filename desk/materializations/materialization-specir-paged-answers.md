---
sldb:
  by: agent
  at: '2026-11-14T15:13:41Z'
  authority: generated
  via: create_document
id: materialization-specir-paged-answers
title: specIR paged answers
source_atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
target_kind: source_file
target_identity: src/specir/mcp/paging.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR paged answers

## Intent

Every set an agent receives comes as one page with its total, a truncated mark and the next offset, and an empty set carries an explanation.
