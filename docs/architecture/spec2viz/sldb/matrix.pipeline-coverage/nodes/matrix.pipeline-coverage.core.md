---
id: matrix.pipeline-coverage.core
spec: SpecDoc:matrix.pipeline-coverage
element: core
kind: core
collection: components
refs: []
atom_refs: []
contains:
- SpecNodeDoc:matrix.pipeline-coverage.loader
- SpecNodeDoc:matrix.pipeline-coverage.validator
- SpecNodeDoc:matrix.pipeline-coverage.compilers
- SpecNodeDoc:matrix.pipeline-coverage.renderers
- SpecNodeDoc:matrix.pipeline-coverage.linters
data:
  stages:
    render:
    - load
    - validate
    - compile
    - render
---

# core

## Description
