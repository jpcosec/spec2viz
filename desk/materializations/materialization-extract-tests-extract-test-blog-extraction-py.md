---
sldb:
  by: agent
  at: '2026-11-20T20:52:57Z'
  authority: generated
  via: create_document
id: materialization-extract-tests-extract-test-blog-extraction-py
title: extract tests-extract-test_blog_extraction-py
source_atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
target_kind: test
target_identity: tests/extract/test_blog_extraction.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_blog_extraction.py
tags:
- system:ir
- topic:extract
---

# extract tests-extract-test_blog_extraction-py

## Intent

materializa en tests/extract/test_blog_extraction.py el atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
