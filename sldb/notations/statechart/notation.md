---
id: statechart
name: statechart
diagram_type: state
level: both
projection: all
layout:
  kind: graph
  direction: LR
markers:
- id: initial
  shape: filled-circle
  model: SpecNodeDoc
  where: has(initial)
glyphs:
- GlyphDoc:statechart.composite
- GlyphDoc:statechart.state
links:
- LinkDoc:statechart.substate
- LinkDoc:statechart.transition
---

# Statechart

## Description
