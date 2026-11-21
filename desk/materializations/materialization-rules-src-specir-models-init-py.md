---
sldb:
  by: agent
  at: '2026-11-21T01:29:30Z'
  authority: generated
  via: create_document
id: materialization-rules-src-specir-models-init-py
title: rules src-specir-models-__init__-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/models/__init__.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules src-specir-models-__init__-py

## Intent

materializa en src/specir/models/__init__.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
