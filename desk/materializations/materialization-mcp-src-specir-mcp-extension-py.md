---
sldb:
  by: agent
  at: '2026-11-20T23:47:54Z'
  authority: generated
  via: create_document
id: materialization-mcp-src-specir-mcp-extension-py
title: mcp src-specir-mcp_extension-py
source_atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
target_kind: code
target_identity: src/specir/mcp_extension.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_mcp_undo.py
tags:
- system:ir
- topic:mcp
---

# mcp src-specir-mcp_extension-py

## Intent

materializa en src/specir/mcp_extension.py el atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
