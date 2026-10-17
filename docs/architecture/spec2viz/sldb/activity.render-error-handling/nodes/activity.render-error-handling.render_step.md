---
id: activity.render-error-handling.render_step
spec: SpecDoc:activity.render-error-handling
element: render_step
kind: decision
refs: []
atom_refs: []
contains: []
data:
  branches:
    ok: write_output
    RenderError: catch_error
---

# render(ir, renderer): dispatch to backend

## Description
