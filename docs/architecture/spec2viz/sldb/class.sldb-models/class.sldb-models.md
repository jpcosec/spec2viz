---
id: class.sldb-models
diagram_type: class
version: '0.1'
spec_path: /home/jp/proyectos/SLDB_1/spec2viz/docs/architecture/spec2viz/class-sldb-models.yml
sha256: a2f5a48cac111910ae7f77822e901b32d168337625c236b1b5ccc2dc8b6a4990
notation: NotationDoc:uml-class
category: Modelos de Estado
nav: Store
summary: 'Clases de los documentos que spec2viz escribe en el store: el spec como
  namespace (SpecDoc, SpecNodeDoc, RelationDoc) y la notación declarativa (NotationDoc,
  GlyphDoc, LinkDoc). Sincronizado con la notación uml-class.'
nodes:
- SpecNodeDoc:class.sldb-models.StructuredNLDoc
- SpecNodeDoc:class.sldb-models.SpecDoc
- SpecNodeDoc:class.sldb-models.SpecNodeDoc
- SpecNodeDoc:class.sldb-models.RelationDoc
- SpecNodeDoc:class.sldb-models.NotationDoc
- SpecNodeDoc:class.sldb-models.GlyphDoc
- SpecNodeDoc:class.sldb-models.LinkDoc
- SpecNodeDoc:class.sldb-models.RelationTypeDoc
---

# spec2viz documents in the sldb store

## Description

The documents spec2viz writes into an sldb store: a spec as a namespace (SpecDoc, SpecNodeDoc, RelationDoc) and the declarative visual vocabulary that says how to draw it (NotationDoc, GlyphDoc, LinkDoc). This spec is itself synced with the `uml-class` notation, so a surface such as graph_ui draws it from the store.
