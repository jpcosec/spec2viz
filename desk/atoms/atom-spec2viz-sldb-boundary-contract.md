---
id: atom-spec2viz-sldb-boundary-contract
title: Spec2viz SLDB Boundary Contract
five_wh_one_plus: how
tags:
- system:spec2viz
- system:sldb
- topic:boundary
- topic:adr
provenance: README.md
---

# Spec2viz SLDB Boundary Contract

## Answer

Frontera entre spec2viz y sldb. sldb es dueño de los documentos Markdown estructurados, StructuredNLDoc, el marcado reversible, el store .sldb, los indices y el indice de aristas; spec2viz es dueño de los specs de diagrama (BaseDiagram), la IR, los renderers, sus modelos de store (SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc) y la resolucion de vistas. spec2viz habla con el store solo por la superficie publica sldb.api, para leer (load_runtime_documents, edges_from, edges_to, load_edge_index, where_matches) y para escribir sus propios documentos (add_model, create_document, save_document_payload, delete_document, rebuild_edges, check_edges). Nunca edita un .md del store a mano ni toca documentos de otros modelos; lo que un spec referencia (refs, atoms) se valida con doc_exists y se reporta.
