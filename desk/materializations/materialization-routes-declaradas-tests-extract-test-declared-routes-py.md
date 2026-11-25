---
sldb:
  by: agent
  at: '2026-11-25T06:38:25Z'
  authority: generated
  via: create_document
id: materialization-routes-declaradas-tests-extract-test-declared-routes-py
title: routes-declaradas tests-extract-test_declared_routes-py
source_atoms:
- atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
target_kind: test
target_identity: tests/extract/test_declared_routes.py
validation:
- pytest -q tests/extract/test_declared_routes.py
tags:
- system:ir
- topic:routes-declaradas
---

# routes-declaradas tests-extract-test_declared_routes-py

## Intent

materializa en tests/extract/test_declared_routes.py el atom atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
