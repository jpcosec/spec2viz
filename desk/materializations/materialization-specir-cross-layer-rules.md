---
sldb:
  by: agent
  at: '2026-11-15T15:34:35Z'
  authority: generated
  via: create_document
id: materialization-specir-cross-layer-rules
title: specIR cross-layer rules
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
target_kind: data_file
target_identity: src/specir/data/rules.yaml
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR cross-layer rules

## Intent

The cross-layer invariants as RuleDoc payloads evaluated by SLDB: an interface action invokes an API operation, and the alerts of the chain, plus the on_write rule that every specIR edge declares its provenance.
