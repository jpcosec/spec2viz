---
sldb:
  by: agent
  at: '2026-11-20T22:01:13Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-extract-test-frontend-extraction-py
title: extract tests-extract-test_frontend_extraction-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/extract/test_frontend_extraction.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-extract-test_frontend_extraction-py

## Intent

materializa en tests/extract/test_frontend_extraction.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
