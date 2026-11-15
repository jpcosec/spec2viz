---
sldb:
  by: agent
  at: '2026-11-15T15:34:42Z'
  authority: generated
  via: create_document
id: materialization-specir-blog-chain-tests
title: specIR blog chain tests
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
- atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica
target_kind: test_module
target_identity: tests/models/test_blog_chain.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR blog chain tests

## Intent

The IR06 validation over the blog store through the MCP: both-way walk, the relation type's verdict on a forbidden edge, the broken rule when the API operation is removed, two views of one Post, and the provenance of every node and edge.
