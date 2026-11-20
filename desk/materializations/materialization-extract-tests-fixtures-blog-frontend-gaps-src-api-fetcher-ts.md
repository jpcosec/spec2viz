---
sldb:
  by: agent
  at: '2026-11-20T22:01:40Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-fixtures-blog-frontend-gaps-src-api-fetcher-ts
title: extract tests-fixtures-blog_frontend_gaps-src-api-fetcher-ts
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/fixtures/blog_frontend_gaps/src/api/fetcher.ts
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-fixtures-blog_frontend_gaps-src-api-fetcher-ts

## Intent

materializa en tests/fixtures/blog_frontend_gaps/src/api/fetcher.ts el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
