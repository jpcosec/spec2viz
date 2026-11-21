---
sldb:
  by: agent
  at: '2026-11-21T01:29:46Z'
  authority: generated
  via: create_document
id: materialization-rules-tests-test-mcp-extension-py
title: rules tests-test_mcp_extension-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/test_mcp_extension.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules tests-test_mcp_extension-py

## Intent

materializa en tests/test_mcp_extension.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
