---
sldb:
  by: agent
  at: '2026-11-25T14:55:37Z'
  authority: generated
  via: create_document
id: materialization-specir-workspace-tests-conftest-py
title: specir-workspace tests-conftest-py
source_atoms:
- atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace
target_kind: test
target_identity: tests/conftest.py
validation:
- pytest -q tests/test_workspace_env.py
tags:
- system:ir
- topic:specir-workspace
---

# specir-workspace tests-conftest-py

## Intent

materializa en tests/conftest.py el atom atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace
