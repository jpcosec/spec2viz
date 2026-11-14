---
sldb:
  by: agent
  at: '2026-11-14T15:13:32Z'
  authority: generated
  via: create_document
id: materialization-specir-package-root
title: specIR package root
source_atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
target_kind: source_file
target_identity: src/specir/__init__.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:mcp
- topic:materialization
---

# specIR package root

## Intent

The specIR package root states that specIR reaches SLDB only through sldb.api and imports neither pron nor spec2viz.
