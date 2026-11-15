---
sldb:
  by: agent
  at: '2026-11-15T15:34:30Z'
  authority: generated
  via: create_document
id: materialization-specir-install-command
title: specIR install command
source_atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: python_module
target_identity: src/specir/install.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR install command

## Intent

A thin adapter over sldb.api that registers specIR's models with add_model, SLDB's relation, rule and view models when missing, and seeds the relation types and rules as managed document seeds with scaffold_store; idempotent.
