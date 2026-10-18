---
id: state.diagram-sync-lifecycle
diagram_type: state
version: '0.1'
spec_path: docs/architecture/spec2viz/state-diagram-sync-lifecycle.yml
sha256: 0ea759e01651a2bfde16765db45b2fab97b3b6e834cedbfd52906c9e8cf70abf
notation: NotationDoc:statechart
category: Modelos de Estado
nav: Sync
summary: 'Estados de `spec2viz diagram sync`: el trabajo contra el store es un estado
  compuesto (validar, escribir, indexar) y un fallo sale de él. Piloto de la notación
  statechart con nest.'
nodes:
- SpecNodeDoc:state.diagram-sync-lifecycle.idle
- SpecNodeDoc:state.diagram-sync-lifecycle.syncing
- SpecNodeDoc:state.diagram-sync-lifecycle.validating
- SpecNodeDoc:state.diagram-sync-lifecycle.writing
- SpecNodeDoc:state.diagram-sync-lifecycle.indexing
- SpecNodeDoc:state.diagram-sync-lifecycle.synced
- SpecNodeDoc:state.diagram-sync-lifecycle.failed
---

# Ciclo de un `diagram sync`

## Description

Estados por los que pasa `spec2viz diagram sync` sobre un spec: el trabajo contra el store es un estado compuesto (validar, escribir, indexar) y un fallo de validación sale de él directamente. Piloto de la notación `statechart` con `nest` y una transición que cruza el borde del contenedor.
