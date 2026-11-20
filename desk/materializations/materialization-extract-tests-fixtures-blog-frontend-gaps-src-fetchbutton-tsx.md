---
sldb:
  by: agent
  at: '2026-11-20T22:01:32Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-fixtures-blog-frontend-gaps-src-fetchbutton-tsx
title: extract tests-fixtures-blog_frontend_gaps-src-FetchButton-tsx
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/fixtures/blog_frontend_gaps/src/FetchButton.tsx
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-fixtures-blog_frontend_gaps-src-FetchButton-tsx

## Intent

materializa en tests/fixtures/blog_frontend_gaps/src/FetchButton.tsx el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
