---
id: matrix.pipeline-coverage.cli
spec: SpecDoc:matrix.pipeline-coverage
element: cli
kind: boundary
collection: components
refs: []
atom_refs: []
contains: []
data:
  stages:
    render:
    - load
    - validate
    - compile
    - render
    - lint
    sync:
    - extract
    - notation
    - write
    - index
    - view
---

# cli.py

## Description
