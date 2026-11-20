---
sldb:
  by: agent
  at: '2026-11-20T23:47:58Z'
  authority: generated
  via: create_document
id: materialization-mcp-tests-test-mcp-extension-py
title: mcp tests-test_mcp_extension-py
source_atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
target_kind: test
target_identity: tests/test_mcp_extension.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_mcp_undo.py
tags:
- system:ir
- topic:mcp
---

# mcp tests-test_mcp_extension-py

## Intent

materializa en tests/test_mcp_extension.py el atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
