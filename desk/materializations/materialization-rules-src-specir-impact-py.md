---
sldb:
  by: agent
  at: '2026-11-21T01:29:22Z'
  authority: generated
  via: create_document
id: materialization-rules-src-specir-impact-py
title: rules src-specir-impact-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/impact.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules src-specir-impact-py

## Intent

materializa en src/specir/impact.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
