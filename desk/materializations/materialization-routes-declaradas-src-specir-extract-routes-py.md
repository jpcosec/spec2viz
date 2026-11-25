---
sldb:
  by: agent
  at: '2026-11-25T06:38:14Z'
  authority: generated
  via: create_document
id: materialization-routes-declaradas-src-specir-extract-routes-py
title: routes-declaradas src-specir-extract-routes-py
source_atoms:
- atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
target_kind: code
target_identity: src/specir/extract/routes.py
validation:
- pytest -q tests/extract/test_declared_routes.py
tags:
- system:ir
- topic:routes-declaradas
---

# routes-declaradas src-specir-extract-routes-py

## Intent

materializa en src/specir/extract/routes.py el atom atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
