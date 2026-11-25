---
sldb:
  by: agent
  at: '2026-11-25T21:12:25Z'
  authority: generated
  via: create_document
id: materialization-extract-python-cli-src-specir-extract-python-cli-py
title: extract-python-cli src-specir-extract-python_cli-py
source_atoms:
- atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
target_kind: code
target_identity: src/specir/extract/python_cli.py
validation:
- pytest -q tests/test_extract_python_cli.py tests/test_cli_mcp.py tests/test_imports.py
tags:
- system:ir
- topic:extract-python-cli
---

# extract-python-cli src-specir-extract-python_cli-py

## Intent

materializa en src/specir/extract/python_cli.py el atom atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
