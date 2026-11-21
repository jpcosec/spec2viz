---
sldb:
  by: agent
  at: '2026-11-21T09:27:33Z'
  authority: generated
  via: create_document
id: materialization-retiro-tests-visual-test-catalog-parity-py
title: retiro tests-visual-test_catalog_parity-py
source_atoms:
- atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
target_kind: test
target_identity: tests/visual/test_catalog_parity.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual tests/test_matriz_cobertura_spec2viz.py
tags:
- system:ir
- topic:retiro
---

# retiro tests-visual-test_catalog_parity-py

## Intent

materializa en tests/visual/test_catalog_parity.py el atom atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
