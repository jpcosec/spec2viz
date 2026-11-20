---
sldb:
  by: agent
  at: '2026-11-20T22:01:21Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-fixtures-blog-frontend-src-api-client-ts
title: extract tests-fixtures-blog_frontend-src-api-client-ts
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/fixtures/blog_frontend/src/api/client.ts
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-fixtures-blog_frontend-src-api-client-ts

## Intent

materializa en tests/fixtures/blog_frontend/src/api/client.ts el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
