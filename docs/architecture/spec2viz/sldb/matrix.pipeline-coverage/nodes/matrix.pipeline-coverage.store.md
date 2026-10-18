---
id: matrix.pipeline-coverage.store
spec: SpecDoc:matrix.pipeline-coverage
element: store
kind: core
collection: components
refs: []
atom_refs: []
contains:
- SpecNodeDoc:matrix.pipeline-coverage.sldb_sync
- SpecNodeDoc:matrix.pipeline-coverage.notation
- SpecNodeDoc:matrix.pipeline-coverage.notation_view
- SpecNodeDoc:matrix.pipeline-coverage.sldb_models
data:
  stages:
    sync:
    - extract
    - notation
    - write
    - index
    - view
---

# store layer

## Description
