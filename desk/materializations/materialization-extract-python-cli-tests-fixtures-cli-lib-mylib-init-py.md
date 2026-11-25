---
sldb:
  by: agent
  at: '2026-11-25T21:12:47Z'
  authority: generated
  via: create_document
id: materialization-extract-python-cli-tests-fixtures-cli-lib-mylib-init-py
title: extract-python-cli tests-fixtures-cli_lib-mylib-__init__-py
source_atoms:
- atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
target_kind: test
target_identity: tests/fixtures/cli_lib/mylib/__init__.py
validation:
- pytest -q tests/test_extract_python_cli.py tests/test_cli_mcp.py tests/test_imports.py
tags:
- system:ir
- topic:extract-python-cli
---

# extract-python-cli tests-fixtures-cli_lib-mylib-__init__-py

## Intent

materializa en tests/fixtures/cli_lib/mylib/__init__.py el atom atom-specir-extract-python-cli-describe-una-libreria-python-con-cli-con-los-tipos-existentes
