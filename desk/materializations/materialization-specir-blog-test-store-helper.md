---
sldb:
  by: agent
  at: '2026-11-15T15:34:40Z'
  authority: generated
  via: create_document
id: materialization-specir-blog-test-store-helper
title: specIR blog test store helper
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: test_module
target_identity: tests/models/blog.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR blog test store helper

## Intent

Builds the blog test store with sldb stores init and specir install and populates it only through the MCP write tools.
