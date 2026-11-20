---
sldb:
  by: agent
  at: '2026-11-20T22:01:09Z'
  authority: generated
  via: create_document
id: materialization-extract-src-specir-extract-react-tsx-py
title: extract src-specir-extract-react_tsx-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/extract/react_tsx.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract src-specir-extract-react_tsx-py

## Intent

materializa en src/specir/extract/react_tsx.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
