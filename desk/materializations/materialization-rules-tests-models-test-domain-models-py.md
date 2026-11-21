---
sldb:
  by: agent
  at: '2026-11-21T01:29:38Z'
  authority: generated
  via: create_document
id: materialization-rules-tests-models-test-domain-models-py
title: rules tests-models-test_domain_models-py
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
target_kind: test
target_identity: tests/models/test_domain_models.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_rules_and_impact.py
tags:
- system:ir
- topic:rules
---

# rules tests-models-test_domain_models-py

## Intent

materializa en tests/models/test_domain_models.py el atom atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
