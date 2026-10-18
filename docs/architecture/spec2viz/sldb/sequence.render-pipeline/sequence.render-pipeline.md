---
id: sequence.render-pipeline
diagram_type: sequence
version: '0.1'
spec_path: /home/jp/proyectos/SLDB_1/spec2viz/docs/architecture/spec2viz/sequence-render-pipeline.yml
sha256: c40e669f30daccc49eee59d8bf31ec3a28ba7e8c7cdfef70dc9f934717736773
notation: NotationDoc:uml-sequence
category: Pipelines de Ejecución
nav: Render
summary: 'Traza completa de llamadas para spec2viz render: CLI → Facade → load() →
  validate() → compile_ir() → render() → write_text().'
nodes:
- SpecNodeDoc:sequence.render-pipeline.User
- SpecNodeDoc:sequence.render-pipeline.CLI
- SpecNodeDoc:sequence.render-pipeline.Facade
- SpecNodeDoc:sequence.render-pipeline.Loader
- SpecNodeDoc:sequence.render-pipeline.Validator
- SpecNodeDoc:sequence.render-pipeline.Compiler
- SpecNodeDoc:sequence.render-pipeline.Renderer
- SpecNodeDoc:sequence.render-pipeline.Disk
---

# Render Pipeline Call Chain

## Description
