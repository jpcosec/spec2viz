---
sldb:
  by: agent
  at: '2026-11-21T01:29:26Z'
  authority: generated
  via: create_document
id: materialization-rules-src-specir-mcp-extension-py
title: rules src-specir-mcp_extension-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: code
target_identity: src/specir/mcp_extension.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules src-specir-mcp_extension-py

## Intent

materializa en src/specir/mcp_extension.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
