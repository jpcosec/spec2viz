---
sldb:
  by: agent
  at: '2026-11-21T01:29:14Z'
  authority: generated
  via: create_document
id: materialization-rules-src-specir-data-relation-types-yaml
title: rules src-specir-data-relation_types-yaml
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/data/relation_types.yaml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules src-specir-data-relation_types-yaml

## Intent

materializa en src/specir/data/relation_types.yaml el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
