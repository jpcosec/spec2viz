---
id: activity.render-error-handling.load_step
spec: SpecDoc:activity.render-error-handling
element: load_step
kind: decision
refs: []
atom_refs: []
contains: []
data:
  branches:
    ok: validate_step
    ParseError: catch_error
---

# load(path): YAML parse + Pydantic validate

## Description
