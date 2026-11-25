---
sldb:
  by: agent
  at: '2026-11-25T21:14:34Z'
  authority: generated
  via: create_document
id: materialization-extract-python-cli-tests-test-extract-python-cli-py
title: extract-python-cli tests-test_extract_python_cli-py
source_atoms:
- atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
target_kind: test
target_identity: tests/test_extract_python_cli.py
validation:
- pytest -q tests/test_extract_python_cli.py tests/test_cli_mcp.py tests/test_imports.py
tags:
- system:ir
- topic:extract-python-cli
---

# extract-python-cli tests-test_extract_python_cli-py

## Intent

materializa en tests/test_extract_python_cli.py el atom atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
