---
sldb:
  by: agent
  at: '2026-11-15T15:46:11Z'
  authority: generated
  via: save_document_payload
id: materialization-specir-blog-chain-fixture
title: specIR blog chain fixture
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
- atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica
target_kind: data_file
target_identity: tests/fixtures/blog_chain.yaml
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR blog chain fixture

## Intent

The publish-a-post chain of the example blog (fundamentos §4) as MCP write batches: every element declarado, unknowns null and named, reusable by later tasks.
