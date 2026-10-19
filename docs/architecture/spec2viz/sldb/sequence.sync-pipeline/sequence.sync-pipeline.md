---
id: sequence.sync-pipeline
diagram_type: sequence
version: '0.1'
spec_path: docs/architecture/spec2viz/sequence-sync-pipeline.yml
sha256: 2b8cb82c31c1c66d7068413e368fda143efe4b000fad92d3cdbee42cfd985dc0
notation: NotationDoc:uml-sequence
category: Pipelines de Ejecución
nav: Sync
summary: 'Qué llama a qué cuando `spec2viz diagram sync` escribe un spec al store:
  un loop por spec y un alt según el tipo de diagrama tenga notación. Piloto de fragmentos
  de secuencia para graph_ui.'
nodes:
- SpecNodeDoc:sequence.sync-pipeline.User
- SpecNodeDoc:sequence.sync-pipeline.CLI
- SpecNodeDoc:sequence.sync-pipeline.SpecSync
- SpecNodeDoc:sequence.sync-pipeline.Loader
- SpecNodeDoc:sequence.sync-pipeline.NotationSync
- SpecNodeDoc:sequence.sync-pipeline.StoreAPI
---

# diagram sync call chain

## Description

What calls what when `spec2viz diagram sync` writes a spec into the sldb store: one loop per spec, and inside it an alt depending on whether the diagram type has a builtin notation. Piloto de fragmentos de secuencia (`group` con operador loop/alt) para graph_ui.
