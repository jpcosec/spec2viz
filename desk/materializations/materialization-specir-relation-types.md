---
sldb:
  by: agent
  at: '2026-11-15T15:34:33Z'
  authority: generated
  via: create_document
id: materialization-specir-relation-types
title: specIR relation types
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
target_kind: data_file
target_identity: src/specir/data/relation_types.yaml
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR relation types

## Intent

The eight relation types of the cross-layer chain (triggers, invokes, handled_by, executes, governed_by, transitions, writes, persisted_in) as RelationTypeDoc payloads: data of the store, checked by SLDB's edge index.
