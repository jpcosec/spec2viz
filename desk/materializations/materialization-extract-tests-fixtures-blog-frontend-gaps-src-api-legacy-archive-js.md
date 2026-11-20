---
sldb:
  by: agent
  at: '2026-11-20T22:01:43Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-fixtures-blog-frontend-gaps-src-api-legacy-archive-js
title: extract tests-fixtures-blog_frontend_gaps-src-api-legacy_archive-js
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/fixtures/blog_frontend_gaps/src/api/legacy_archive.js
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-fixtures-blog_frontend_gaps-src-api-legacy_archive-js

## Intent

materializa en tests/fixtures/blog_frontend_gaps/src/api/legacy_archive.js el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
