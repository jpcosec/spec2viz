---
sldb:
  by: agent
  at: '2026-11-20T20:52:54Z'
  authority: generated
  via: create_document
id: materialization-extract-src-specir-extract-write-py
title: extract src-specir-extract-write-py
source_atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
target_kind: code
target_identity: src/specir/extract/write.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_blog_extraction.py
tags:
- system:ir
- topic:extract
---

# extract src-specir-extract-write-py

## Intent

materializa en src/specir/extract/write.py el atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
