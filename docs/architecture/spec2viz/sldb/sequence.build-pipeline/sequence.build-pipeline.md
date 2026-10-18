---
id: sequence.build-pipeline
diagram_type: sequence
version: '0.1'
spec_path: docs/architecture/spec2viz/sequence-build-pipeline.yml
sha256: 134a3eed8644fac271ca09479538118725d43bee17abfe69c36dc37d53a1fbc2
notation: NotationDoc:uml-sequence
category: Pipelines de Ejecución
nav: Build
summary: 'Traza completa para spec2viz build: CLI → Deskops → parse_atoms() → render_deskops()
  → write_text().'
nodes:
- SpecNodeDoc:sequence.build-pipeline.User
- SpecNodeDoc:sequence.build-pipeline.CLI
- SpecNodeDoc:sequence.build-pipeline.Deskops
- SpecNodeDoc:sequence.build-pipeline.AtomParser
- SpecNodeDoc:sequence.build-pipeline.AtomsDir
- SpecNodeDoc:sequence.build-pipeline.VistasYML
- SpecNodeDoc:sequence.build-pipeline.Template
- SpecNodeDoc:sequence.build-pipeline.Disk
---

# Deskops Build Pipeline Call Chain

## Description
