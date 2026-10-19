---
id: matrix.pipeline-coverage
diagram_type: component_view_matrix
version: '0.1'
spec_path: docs/architecture/spec2viz/matrix-pipeline-coverage.yml
sha256: 567459cbdb716573e763dfc941437ec2d708cef4cf4657a644a36aa70155815b
notation: NotationDoc:component-view-matrix
category: Arquitectura de Módulos
nav: Matriz
summary: Qué módulos participan en cada etapa del pipeline de render y del sync al
  store. Piloto de la notación component-view-matrix (grilla) para graph_ui.
nodes:
- SpecNodeDoc:matrix.pipeline-coverage.render__load
- SpecNodeDoc:matrix.pipeline-coverage.render__validate
- SpecNodeDoc:matrix.pipeline-coverage.render__compile
- SpecNodeDoc:matrix.pipeline-coverage.render__render
- SpecNodeDoc:matrix.pipeline-coverage.render__lint
- SpecNodeDoc:matrix.pipeline-coverage.sync__extract
- SpecNodeDoc:matrix.pipeline-coverage.sync__notation
- SpecNodeDoc:matrix.pipeline-coverage.sync__write
- SpecNodeDoc:matrix.pipeline-coverage.sync__index
- SpecNodeDoc:matrix.pipeline-coverage.sync__view
- SpecNodeDoc:matrix.pipeline-coverage.cli
- SpecNodeDoc:matrix.pipeline-coverage.core
- SpecNodeDoc:matrix.pipeline-coverage.loader
- SpecNodeDoc:matrix.pipeline-coverage.validator
- SpecNodeDoc:matrix.pipeline-coverage.compilers
- SpecNodeDoc:matrix.pipeline-coverage.renderers
- SpecNodeDoc:matrix.pipeline-coverage.linters
- SpecNodeDoc:matrix.pipeline-coverage.store
- SpecNodeDoc:matrix.pipeline-coverage.sldb_sync
- SpecNodeDoc:matrix.pipeline-coverage.notation
- SpecNodeDoc:matrix.pipeline-coverage.notation_view
- SpecNodeDoc:matrix.pipeline-coverage.sldb_models
---

# Module coverage across the render pipeline

## Description

Which spec2viz modules take part in each stage of the two pipelines: rendering a spec to a file and syncing it into the sldb store. Rows are modules (nested by package), columns are the stages of each view; a cell is `occupies`. Piloto de la notación `component-view-matrix` (layout grid) para graph_ui.
