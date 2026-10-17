# Changelog

## Unreleased - 2026-10-17

- declarative visual vocabulary: `NotationDoc`, `GlyphDoc` and `LinkDoc` (`spec2viz.sldb_models`) say how a
  diagram type is drawn (glyph per model + `where` predicate, link per relation with `draw`
  line|nest|lane|cell|axis, line and terminals); builtin notations `uml-class` and `statechart` in
  `spec2viz/notations/`; `spec2viz notation list|validate|sync`; `diagram sync` syncs the diagram type's
  notation with the spec (`--notation NAME|PATH|none`) and `SpecDoc.notation` references it; `SpecNodeDoc.data`
  carries the rest of the element (attributes, methods, guards, `initial`) for compartments; the read
  contract for surfaces such as graph_ui is in `docs/notation-contract.md`; `spec2viz notation view`
  (`notation_view.resolve_view`) is its one interpreter and returns the drawable view of a spec as JSON
- `spec2viz diagram sync`: a spec becomes a namespace over the sldb store (`SpecDoc`, one `SpecNodeDoc`
  per element, one `RelationDoc` per edge, missing `RelationTypeDoc`s created); stale documents of a
  previous sync are deleted and the edge index rebuilt and checked; `--strict` fails on unresolved
  `refs:`/`atoms:` or index errors
- `spec2viz diagram from-graph`: compiles an sldb graph (node-link snapshot or `--store`) into a
  component spec with node-type/model/relation filters; `contains` becomes nesting
- the catalog panel lists the sldb relations of every ref and atom (`edges_from`/`edges_to` through
  `sldb.api`, structural edges left out); `structuredLanguageDB>=0.1.6`
- added `refs: [Model:name]` to every spec element (component, deployment, class, activity, state,
  sequence): references to sldb documents, resolved at `catalog build` and listed in the element panel
- the catalog atom resolver uses only the public `sldb.api` surface (`load_runtime_documents`,
  `open_store`, `store_links`); `structuredLanguageDB>=0.1.3` is now a declared dependency
- the architecture bundle uses the built-in template; the stale `docs/architecture/template.html`
  override is gone and the Mermaid projections are regenerated from their specs
- sequence renderers emit one block per run of consecutive messages sharing a `group`; `;` is escaped
  in Mermaid messages; the antonIA HTML escapes the Mermaid source

## 0.2.0 - 2026-05-01

Defined the semantic IR reflection contract and enforcement artifact shape.

- added `ReflectionDiagram`, `ReflectionIR`, and `EnforcementArtifact` models in `spec2viz/models/reflection.py`
- implemented `SemanticMetadata` with 6-dimensional (6D) model support (Who, What, Where, When, How, Why)
- updated `DiagramType` enum to include the new `reflection` diagram type
- exposed `ReflectionDiagram` through the top-level `spec2viz.models` package

## 0.1.0 - 2026-04-22

Initial packaged `spec2viz` release and rename from `yaml-charts`.

- renamed the project, import path, and primary CLI from `yaml-charts` / `yaml_charts` to `spec2viz`
- added packaging metadata, a real `README.md`, checked-in examples, and install verification
- added compatibility shims for legacy `yaml_charts` imports and the `yaml-charts` command with deprecation warnings
- added JSON Schema export through the Python API and `spec2viz schema`
- added descriptions for every Pydantic field so generated schemas and docs carry semantic guidance
- added packaging and example regression tests to keep docs, examples, and shipped behavior aligned

### Migration Notes

- use `spec2viz` instead of `yaml-charts`
- use `import spec2viz` instead of `import yaml_charts`
- regenerate any editor integrations or schema references with `spec2viz schema`
- treat the legacy name as deprecated compatibility only
