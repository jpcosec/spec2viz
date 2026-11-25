---
sldb:
  by: agent
  at: '2026-11-25T03:37:56Z'
  authority: generated
  via: create_document
id: materialization-specir-mcp-src-specir-cli-py
title: specir-mcp src-specir-cli-py
source_atoms:
- atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
target_kind: code
target_identity: src/specir/cli.py
validation:
- pytest -q tests/test_cli_mcp.py
tags:
- system:ir
- topic:specir-mcp
---

# specir-mcp src-specir-cli-py

## Intent

materializa en src/specir/cli.py el atom atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
