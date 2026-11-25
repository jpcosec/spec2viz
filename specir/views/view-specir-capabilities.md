---
id: view-specir-capabilities
name: view-specir-capabilities
nodes: []
relations: []
direction: both
notation: ''
layout: {}
params: []
sections:
- key: capabilities
  select:
    model: CapabilityDoc
  fields:
  - title
  - audience
  edges:
  - relation: accepted_by
    direction: out
    as: test
  group_by: ''
  group_order: []
  rules: []
  transitions: null
- key: tests
  select:
    model: MaterializationContractDoc
    path_glob: specir/capabilities/*
  fields:
  - title
  - target_identity
  - source_atoms
  edges: []
  group_by: ''
  group_order: []
  rules: []
  transitions: null
---

# Capabilities of the domain, who they are for and their acceptance test

## Description