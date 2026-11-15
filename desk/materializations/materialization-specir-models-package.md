---
sldb:
  by: agent
  at: '2026-11-15T15:34:28Z'
  authority: generated
  via: create_document
id: materialization-specir-models-package
title: specIR models package
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
target_kind: python_module
target_identity: src/specir/models/__init__.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR models package

## Intent

The public names of specIR's domain models and the provenance check they share.
