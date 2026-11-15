---
sldb:
  by: agent
  at: '2026-11-15T15:34:44Z'
  authority: generated
  via: create_document
id: materialization-specir-domain-model-tests
title: specIR domain model tests
source_atoms:
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
- atom-omg-es-referencia-conceptual-no-dependencia
- atom-specir-depende-solo-de-la-api-pública-de-sldb
target_kind: test_module
target_identity: tests/models/test_domain_models.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR domain model tests

## Intent

The domain models live in the specIR package, redefine no SLDB visual model, validate the IR05 taxonomy, and install registers them by SLDB's registry idempotently.
