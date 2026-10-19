# Changelog

## Unreleased - 2026-10-17

- Style, all optional and backward compatible (unstyled notations sync and resolve exactly as before):
  - builtin shapes are now a closed list (`SHAPES`) with new `cylinder`, `queue`, `cloud`, `package` and
    `note`; glyphs take optional `kind` (a palette kind), `fill`, `stroke` and `icon`, links an optional
    `color`; colors are a palette token or a `#rrggbb` hex, icons come from the palette's declared set
    (Lucide names as exported by lucide-react 0.577.0, never URLs)
  - an accessible default palette (`spec2viz/palettes/default.yml`, a `PaletteDoc` in the store) for
    database, queue, storage, gateway, auth, backend, frontend, client and external: strokes >= 3:1
    against the light and dark backgrounds, text >= 4.5:1 on every fill, and a distinct (shape, icon) per
    kind so hue is never the only cue; `spec2viz palette list|validate|sync`
  - `style.kinds` of a spec is wired: neutral `fill`/`stroke`/`icon` keys are validated, stored in the
    `SpecDoc` and drawn by mermaid as `classDef` (component, activity, deployment); renderer blocks such as
    `plantuml:` keep working as before
  - one precedence, in `spec2viz.styling.resolve_style`: notation glyph > spec `style.kinds` > notation
    palette, per property; `resolve_view` returns each node's resolved `style`, each link's `color`, the
    view's `palette` and a resolved `legend` (glyphs, links, kinds)
  - `resolve_documents(store, notation, doc_refs, relation_refs=..., spec_style=...)`: the same output for
    documents of any model, public (for `ViewDoc` evaluation)
  - `notation validate` reports `UnknownShapeError`, `UnknownKindError`, `InvalidColorError` and
    `UnknownIconError`; contract §13 and §14 in `docs/notation-contract.md`
- `resolve_view` interpolates a glyph's `keyword` like its label (`«{kind}»` -> `«database»`) and drops it
  when nothing is left (`«»`); before, the template reached the render contract literally. A test walks the
  resolved view of every diagram type and fails on any unresolved `{placeholder}`
- `vistas.yml`: optional `notation:` per view (a path relative to the `vistas.yml`, a builtin name or a
  `NotationDoc` in the store); `catalog sync` uses it, without it the builtin of the type as before. New
  `catalog validate`; both report `UnknownNotationError` / `NotationMismatchError` (typed
  `ValidationError`s), and `catalog sync` writes nothing when a view fails
- `diagram sync` (with or without `--notation`) no longer wipes the `category`, `nav` and `summary` that
  `catalog sync` gave a spec: without catalog metadata the existing values are kept
- Activity sync: the step named in `start:` no longer becomes the initial node. Every activity gets its own
  initial pseudonode (`__initial`, drawn with the `start` glyph) that flows by `next` to the start step, which
  keeps its own glyph (an action box, or a decision diamond). Likewise, when `end:` names a real step, that
  step keeps its glyph and flows to a final pseudonode (`__final`); `end: end` stays the final node itself.
  `resolve_view` honours an explicit `label: ""` on a glyph (initial, final, merge) instead of falling back
  to `{title}`, so those glyphs no longer show a stray "start"/"end" label
- Deployment specs: nodes nest (a node `contains` nodes and artifacts at any depth, one parent per node,
  no cycles, unique ids across nodes and artifacts); a connection takes `kind: communication` (default;
  node -> node, or artifact -> artifact as before), `deploy` («deploy», artifact -> node) or `manifest`
  («manifest», artifact -> node or artifact), plus an optional `label`. Unknown ids raise
  `UnknownReferenceError`, a disallowed end raises `EndpointKindError`, cycles and duplicates raise
  `StructureError`. Mermaid, PlantUML and d2 draw nested subgraphs/containers and dashed «deploy» and
  «manifest»; the sync emits `deploy` and `manifest` relations and the `deployment` notation draws them.
  d2 now addresses contained elements by their container path (edges used to create stray duplicates)
- Activity specs: optional `partition` per step (UML swimlanes: one lane per partition in mermaid
  subgraphs, PlantUML `|lane|` and d2 containers), `kind: merge` (a diamond like `decision`, with no
  branches) and optional `notes` per step (a UML note joined to its step). The builtin `activity`
  notation gains a `merge` glyph; `data.partition` and `data.notes` travel in each `SpecNodeDoc`.
  Specs without these fields render exactly as before
- Typed validation errors, all subclasses of `ValidationError`: `UnknownReferenceError`,
  `EndpointKindError`, `StructureError`, `UnknownKindError`, `InvalidColorError`, `UnknownIconError`,
  `UnknownShapeError`
- Sync: an activity `start`/`end` that names a terminal node rather than a step (`end: end`, as in
  `examples/activity`) is materialized as a `SpecNodeDoc`, so `next: end` edges resolve and draw with `activity.end`;
  deployment connections are always the `connects` relation, with the protocol in `attributes` and as the
  label (`{data.protocol}` in the deployment notation), instead of one relation type per protocol string.
  Re-syncing a deployment spec replaces its old per-protocol RelationDocs; the old RelationTypeDocs stay.
- `tools/suite-check.sh`: before the suites, builds each derived store from its `.sldb/store.yaml` (`sldb stores build`
  + `stores check`, in dependency order; pron with `make world` on clones) and records `store:<repo>`; the
  default report goes to `~/.cache/suite-check/run-<date>` so it survives a reboot
- The store is derived and out of git (sldb `derived-store-boundary.md`): `.sldb/store.yaml` declares it,
  `.sldb/core/` is ignored and rebuilt with `sldb stores build`; CI's `store` job checks out deskops as a
  sibling and runs `sldb stores build --check`
- `ViewDoc` (`spec2viz.sldb_models`): the portable projection-grammar view (nodes as `{model, where}`,
  relations, direction, optional notation and layout override), registered in the store with the other
  spec2viz models; graph_ui evaluates and writes it; `layout.style` (`layered`, `rings`) and `ring_field`
  are recognized layout parameters (contract §12)
- `tools/suite-check.sh`: default matrix 3.12,3.13 (`--pythons` without a list), each pytest in its own
  `mktemp` `--basetemp`, venvs pruned per column, e2e repo and origin clones removed on exit (`SUITE_KEEP=1`)
- Python floor raised to 3.12 (`requires-python >=3.12`, classifiers 3.12 and 3.13, CI matrix 3.12/3.13),
  shared by the whole SLDB_1 suite; no 3.10/3.11 compatibility shims existed in the code
- `tools/suite-check.sh`: a repo whose `requires-python` does not cover the interpreter is marked SKIP
  (with the declared range) instead of FAIL, together with its suite and the e2e steps that need it
- fix(catalog build): a vista whose `src` is a Vega JSON (`diagram render --renderer vega`) is embedded as a
  Vega board (the bundle loads vega-embed on demand) instead of being linted as Mermaid and failing the
  build; `.puml`, `.d2` and other text sources are shown as they are; only `.mmd` is linted. Messages
  say "catalog", not "deskops"
- the catalog's coverage-by-view projection drops its kgdb wording: `build_coverage_by_view(items,
  snapshot_path=...)` (`kgdb_snapshot_path` stays as an alias), warning scope `snapshot`; sldb no longer
  writes the `knowledge_graph.kg.json` it reads, so without one the projection is empty with a warning
- fix: the wildcard link (`relation: "*"`) no longer writes a `relation_type` reference to a
  `RelationTypeDoc` that does not exist (`sldb edges unresolved --local` reported 3 dangling refs)
- `diagram from-graph` projects sldb's Python source graph (`sldb selfdoc python-sync`): Python nodes take
  their label from the code (`ast.name` / `ast.module`) and their kind from the declared `semantics.kind`
  or the AST class (module, class, function, variable, external); `--module-prefix` (repeatable) scopes
  the projection to a module and what hangs from it without leaving a dangling edge or nesting; relation
  names are copied as they come (`load_node_link_graph` returns the declared node attributes)
- `tools/suite-check.sh`: integrated check of the SLDB_1 suite without deploying: a clean venv with
  sldb, pron, deskops, spec2viz and graph_ui installed editable from their checkouts (no kgdb), every
  repo's pytest, and an end-to-end flow (deskops init -> task -> closeout commit; spec2viz diagram sync,
  notation sync and notation view against that store; graph_ui serving it with /api/schema, /api/graph
  and /api/notation/view at 200 and parity with spec2viz's view); prints a step x result table;
  `--from-origin` clones every repo's main branch from origin and tests the clones, reporting each HEAD;
  `--pythons A,B,C` runs the whole check once per interpreter (uv or PATH) and prints a step x Python
  matrix; the review-workbench node toolchain of graph_ui (npm ci, vitest, tsc, lint) is part of the run
- provenance header: every rendered text projection (`.mmd`, `.puml`, `.d2`) starts with a comment
  naming the spec it was generated from and the validate command to run before re-rendering; goldens
  and the architecture projections regenerated (`spec2viz.provenance_header`)
- sequence fragments: `notation view` derives each fragment's `kind` from the operator that opens the
  message `group` (`alt`, `loop`, `opt`, `par`, `break`, `critical`, `neg`, `ref`, `seq`, `strict`) and
  keeps the rest as `label`; pilot `sequence.sync-pipeline` (loop and alt over three participants)
- edge attributes: `diagram sync` keeps what a RelationDoc had no field for (class multiplicities and
  label, transition `on`/`guard`/`action`, message `kind`/`group`/`message`, deployment `protocol`,
  activity `branch`, matrix `view`/`stage`) in `RelationDoc.attributes` when the installed sldb has it
  (>= 0.1.11); `notes` of a transition reads `event [guard] / action`; `LinkDoc.source_label` and
  `target_label` templates (uml-class rotulates multiplicities); `notation view` exposes `data`,
  `source_label`/`target_label` per link and `fragments` (runs of messages sharing a `group`); the
  contract fixes how lanes and grids are ordered (§8c) and adds the `matrix.pipeline-coverage` pilot
- packaging: version aligned with this changelog (0.2.0), `structuredLanguageDB>=0.1.11` as the one
  declared range (`StructuredNLDoc` imported from `sldb.api`, `RelationDoc.attributes` written), `mmdc` (mermaid-cli) documented as the optional external engine of `diagram lint`
- spec2viz runs on graph_ui: one builtin notation per diagram type (`component`, `deployment`,
  `uml-sequence`, `activity`, `component-view-matrix`, `reflection` join `uml-class` and `statechart`),
  a `relation: "*"` wildcard link for free relations, `spec2viz catalog sync` syncs every spec of a
  `vistas.yml` with its notation and writes `category`/`nav`/`summary` into the `SpecDoc` (the catalog
  is the list of SpecDocs by category); `SpecNodeDoc.collection`; activity (`next`, `branch`),
  component_view_matrix (`occupies` cells, stages as elements) and reflection edges are synced;
  sequence message kinds become `sends`/`sends_async`/`returns` with their `condition`; RelationDoc
  names carry the edge position (`<spec>.<nn>-...`) and the view lists links in spec order; the HTML
  bundle is now the static export
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
  `sldb.api`, structural edges left out)
- added `refs: [Model:name]` to every spec element (component, deployment, class, activity, state,
  sequence): references to sldb documents, resolved at `catalog build` and listed in the element panel
- the catalog atom resolver uses only the public `sldb.api` surface (`load_runtime_documents`,
  `open_store`, `store_links`); `structuredLanguageDB` is a declared dependency (now `>=0.1.11`)
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
