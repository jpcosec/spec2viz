---
sldb:
  by: agent
  at: '2026-11-21T09:27:15Z'
  authority: generated
  via: create_document
id: materialization-retiro-tests-visual-goldens-spec2viz-2de1056-oracle-json
title: retiro tests-visual-goldens-spec2viz-2de1056-oracle-json
source_atoms:
- atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
target_kind: test
target_identity: tests/visual/goldens/spec2viz-2de1056-oracle.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual tests/test_matriz_cobertura_spec2viz.py
tags:
- system:ir
- topic:retiro
---

# retiro tests-visual-goldens-spec2viz-2de1056-oracle-json

## Intent

materializa en tests/visual/goldens/spec2viz-2de1056-oracle.json el atom atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
