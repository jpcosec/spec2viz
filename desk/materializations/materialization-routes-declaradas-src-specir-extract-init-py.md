---
sldb:
  by: agent
  at: '2026-11-25T06:38:03Z'
  authority: generated
  via: create_document
id: materialization-routes-declaradas-src-specir-extract-init-py
title: routes-declaradas src-specir-extract-__init__-py
source_atoms:
- atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
target_kind: code
target_identity: src/specir/extract/__init__.py
validation:
- pytest -q tests/extract/test_declared_routes.py
tags:
- system:ir
- topic:routes-declaradas
---

# routes-declaradas src-specir-extract-__init__-py

## Intent

materializa en src/specir/extract/__init__.py el atom atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
