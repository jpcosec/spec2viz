---
sldb:
  by: agent
  at: '2026-11-25T15:02:33Z'
  authority: generated
  via: create_document
id: materialization-mcp-delega-src-specir-mcp-extension-py
title: mcp-delega src-specir-mcp_extension-py
source_atoms:
- atom-specir-mcp-delega-en-mcp-extension-y-cli-py-no-importa-sldb-mcp
target_kind: code
target_identity: src/specir/mcp_extension.py
validation:
- pytest -q tests/test_imports.py tests/test_cli_mcp.py
tags:
- system:ir
- topic:mcp-delega
---

# mcp-delega src-specir-mcp_extension-py

## Intent

materializa en src/specir/mcp_extension.py el atom atom-specir-mcp-delega-en-mcp-extension-y-cli-py-no-importa-sldb-mcp
