---
sldb:
  by: agent
  at: '2026-11-14T15:13:30Z'
  authority: generated
  via: create_document
id: materialization-specir-package-declaration
title: specIR package declaration
source_atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
target_kind: config_file
target_identity: pyproject.toml
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR package declaration

## Intent

pyproject declares specIR with structuredLanguageDB as its only SLDB dependency and the MCP SDK as the optional mcp extra; no pron or spec2viz dependency.
