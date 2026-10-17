---
id: state.diagram-type-lifecycle
diagram_type: state
version: '0.1'
spec_path: /home/jp/proyectos/SLDB_1/spec2viz/docs/architecture/spec2viz/state-diagram-type-lifecycle.yml
sha256: b098076c99190b30bd30153b6d993e954da261dca36c0c0e871f5072387cb120
notation: NotationDoc:statechart
category: Modelos de Estado
nav: Lifecycle
summary: 'Máquina de estados de un archivo YAML: Raw → Dict → DiagramModel → Validated
  → IR → Output, con transiciones de error.'
nodes:
- SpecNodeDoc:state.diagram-type-lifecycle.raw_yaml
- SpecNodeDoc:state.diagram-type-lifecycle.parsed_dict
- SpecNodeDoc:state.diagram-type-lifecycle.validated_model
- SpecNodeDoc:state.diagram-type-lifecycle.semantically_valid
- SpecNodeDoc:state.diagram-type-lifecycle.compiled_ir
- SpecNodeDoc:state.diagram-type-lifecycle.rendered_output
- SpecNodeDoc:state.diagram-type-lifecycle.error
---

# Diagram Spec Lifecycle

## Description
