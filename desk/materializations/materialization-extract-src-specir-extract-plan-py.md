---
sldb:
  by: agent
  at: '2026-11-20T22:01:06Z'
  authority: generated
  via: create_document
id: materialization-extract-src-specir-extract-plan-py
title: extract src-specir-extract-plan-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/extract/plan.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract src-specir-extract-plan-py

## Intent

materializa en src/specir/extract/plan.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
