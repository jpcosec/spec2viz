---
sldb:
  by: agent
  at: '2026-11-25T03:38:01Z'
  authority: generated
  via: create_document
id: materialization-specir-mcp-tests-test-cli-mcp-py
title: specir-mcp tests-test_cli_mcp-py
source_atoms:
- atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
target_kind: test
target_identity: tests/test_cli_mcp.py
validation:
- pytest -q tests/test_cli_mcp.py
tags:
- system:ir
- topic:specir-mcp
---

# specir-mcp tests-test_cli_mcp-py

## Intent

materializa en tests/test_cli_mcp.py el atom atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
