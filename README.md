# spec2viz

`spec2viz` turns semantic YAML specifications into diagrams and charts.

It is meant for teams that want to author structured specs once and render them into outputs such as PlantUML, Mermaid, and Vega.

Within the `hum-ecosystem`, `spec2viz` is the human-watchable rendering layer over canonical `specYaml` semantics. Renderer hints may exist, but semantic truth belongs upstream in `specyaml/`.

## What It Does

- validates diagram specs with Pydantic models
- compiles semantic specs into renderer-agnostic IR
- renders class, sequence, state, component, activity, deployment, and matrix views
- supports both a Python API and a CLI

## Install

spec2viz needs Python 3.12 or newer (the whole SLDB_1 suite shares that floor; 3.10 reaches end of life
in October 2026).

```bash
python3 -m pip install .
```

For local development:

```bash
python3 -m pip install -e .[dev]
```

External, optional: `mmdc` (the [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) binary,
`npm install -g @mermaid-js/mermaid-cli`). `spec2viz diagram lint` uses it as the real Mermaid engine
when it is on `PATH` and falls back to the regex pass when it is not; rendering never needs it.
Reading or writing an sldb store (`diagram sync`, `catalog sync`, `notation ...`, the catalog's atom
and edge panels) needs `structuredLanguageDB>=0.1.11`, which is a declared dependency.

## CLI

Class diagrams support structured attributes, method signatures, protocols/records,
and UML relationships. See [the class diagram schema and workflow](docs/CLASS_DIAGRAMS.md).

Inspect the available commands:

```bash
spec2viz --help
spec2viz diagram --help
spec2viz catalog --help
```

Diagram commands:

```bash
spec2viz diagram validate tests/fixtures/sequence.create-quotation.yml
spec2viz diagram render tests/fixtures/sequence.create-quotation.yml --out out
spec2viz diagram render tests/fixtures/state.quotation.yml --backend mermaid --out out
spec2viz diagram render examples/component/example.yml --renderer d2 --out out
spec2viz diagram render examples/reflection/example.enforcement.yml --renderer json --out out
spec2viz diagram schema --type sequence --out sequence.schema.json
```

Legacy aliases still work:

```bash
spec2viz validate tests/fixtures/sequence.create-quotation.yml
spec2viz render tests/fixtures/sequence.create-quotation.yml --out out
spec2viz schema --type sequence --out sequence.schema.json
```

Supported renderers:

- `plantuml`
- `mermaid`
- `vega`
- `d2`
- `antonia-html`
- `json`

Catalog commands build a deskops architecture HTML bundle from a legacy `vistas.yml` registry or a hierarchical diagram store:

```bash
spec2viz catalog build --config examples/fixtures/vistas.yml --out out/architecture.html
spec2viz catalog build --config examples/fixtures/vistas.yml --out out/architecture.html --base-dir examples/fixtures --atoms-dir desk/atoms
spec2viz catalog build --config catalog.yml --out out/catalog.html
spec2viz catalog build --config examples/catalog/project.yml --out out/catalog.html
spec2viz catalog schema --out diagram-store.schema.json
```

### Linking atoms to diagram elements

Elements may declare which atoms (`desk/atoms`, by `id`) explain them with an optional `atoms: [atom-id, ...]` list
on component/deployment nodes (and deployment artifacts), activity steps, state states, class definitions and
sequence participants:

```yaml
data:
  states:
    - id: nueva
      label: "4 Nueva"
      atoms: [atom-estado-nueva, atom-plazo-48h]
```

`catalog build` resolves the ids against the loaded atoms (`--atoms-dir` or the sldb store) and embeds a
label/id -> atoms map (`window.ATOMS_EXPLICIT`; the SVG is not annotated because Mermaid offers no robust hook for that).
In the browser a node with explicit atoms shows exactly those (all of them) and skips fuzzy text matching;
nodes without `atoms` fall back to the fuzzy matcher (exact title/alias, contained phrase, or 2+ shared tokens).
An unknown id is a build warning; `--strict-atoms` makes it an error. When every element of a view declares
atoms, the other atoms are not embedded for that view. `--atoms-tag <tag>` (repeatable) limits the fuzzy pool by tag.

Elements may also point at any sldb document with `refs: [Model:name, ...]` (`alias:Model:name` for a
document of a linked store), for example a task or a code symbol:

```yaml
    renderers:
      label: Renderer Dispatch
      refs: [TaskDoc:task-sync-golden-plantuml-files, PythonSymbolDoc:python-spec2viz-renderers]
```

`catalog build` resolves each ref against the sldb store discovered for the view (public `sldb.api`) and
lists them in the element panel with model, title, path and a short summary. An unknown ref is a warning,
or an error with `--strict-atoms`. A ref without the `Model:` part is rejected at validation time.

Every ref and atom in the panel also lists its sldb relations (`edges_from`/`edges_to` through
`sldb.api`): the authored and declared edges in both directions, without the structural ones the index
derives from sections, tags and fields. A store without an edge index gets one warning and no relations.

### The spec as a namespace over the sldb store

`spec2viz diagram sync <spec.yml> [--store .sldb] [--out DIR] [--strict]` writes a spec into the store so
its elements are addressable documents:

- `SpecDoc:<spec id>` carries the YAML path and SHA-256 and references its nodes.
- `SpecNodeDoc:<spec id>.<element>` per element (node, state, step, class, participant), with its
  `refs:`, `atoms:` and `contains:`; the index turns those into `references` and `contains` edges.
- One `RelationDoc` per spec edge, typed with the spec relation (`uses`, `loads(path)` -> `loads_path`);
  a relation the store does not know gets its `RelationTypeDoc` in `sldb/relation_types/`.

Documents of a previous sync that left the spec are deleted; the edge index is rebuilt and checked.
Any document can then point at a diagram element (`refs: [SpecNodeDoc:arq.core]`, a RelationDoc, a
`__references__` field) and `sldb graph neighborhood SpecNodeDoc:arq.core` walks the whole thing. The
catalog shows those edges back on the element. `--strict` fails when a `refs:`/`atoms:` target does not
exist or the index reports an error. The models live in `spec2viz.sldb_models`, so spec2viz must be
installed where the store is read.

The reverse direction is `spec2viz diagram from-graph <snapshot.json> | --store .sldb [--out spec.yml]`:
it compiles an sldb edge index (a `sldb graph snapshot save` JSON or the store itself) into a component
spec, filtering by node type, model and relation (`--node-type`, `--model`, `--relation`,
`--exclude-relation`, `--drop-isolated`); `contains` edges become nesting. It also projects sldb's Python
source graph (`.sldb/runtime/graphs/python-source.graph.json`, written by `sldb selfdoc python-sync`): nodes
are labelled from the code and typed from their declared `semantics.kind` or AST class, and
`--module-prefix sldb.selfdoc` keeps one module and what hangs from it, with no dangling edge or nesting:

```bash
spec2viz diagram from-graph .sldb/runtime/graphs/python-source.graph.json \
  --node-type python_module --node-type python_symbol --module-prefix sldb.selfdoc --out selfdoc.yml
spec2viz diagram validate selfdoc.yml
```

### The notation as data: how a spec is drawn

How a diagram type is drawn is not a table inside a renderer but three kinds of store document, the
declarative visual vocabulary a surface such as graph_ui reads to draw the spec live:

- `NotationDoc:<name>`: diagram type, level (`types`, `instances`, `both`), layout (`kind`, `direction`),
  markers (the initial pseudostate) and the ordered list of its glyphs and links.
- `GlyphDoc:<name>.<glyph>`: how a document looks. A `model` plus a `where` predicate in the
  `sldb find --where` grammar (`kind = "interface"`, `nonempty(contains)`), then `shape`, `label`
  template (`{title}`), `keyword` (`«interface»`), `compartments` (`data.attributes`) and `function`.
  The first glyph whose predicate holds wins; the last one has no predicate and is the default.
- `LinkDoc:<name>.<link>`: how a relation looks. `relation` (and `relation_type`, a reference to its
  `RelationTypeDoc`), `draw` (`line`, `nest`, `lane`, `cell`, `axis`), `line` (`solid`, `dashed`,
  `dotted`), `source_end`/`target_end` terminals (`hollow-triangle`, `filled-diamond`, `open-arrow`...)
  and a `label` template over the RelationDoc (`{notes}`).

spec2viz ships one notation per diagram type in `spec2viz/notations/` (`uml-class`, `statechart`,
`component`, `deployment`, `uml-sequence`, `activity`, `component-view-matrix`, `reflection`; a
`relation: "*"` link draws the free relations of component, deployment and reflection specs);
`spec2viz notation list` shows
them, `spec2viz notation validate <name|path>` checks a notation's grammar (ids, enumerations, a default
glyph per model, relations the diagram type emits, `where` predicates) and `spec2viz notation sync
<name|path> --store .sldb` writes it under `sldb/notations/<name>/`. `diagram sync` syncs the diagram
type's builtin notation together with the spec (`--notation NAME|PATH|none` to override) and
`SpecDoc.notation` references it. `SpecNodeDoc.data` carries the rest of each element (attributes,
methods, guards, `initial: true` on the initial state), which is where compartments and predicates read
from. The read contract for surfaces is in `docs/notation-contract.md`, and its one interpreter is
`spec2viz notation view <spec id> --store .sldb` (`spec2viz.notation_view.resolve_view`): the JSON view of
a spec with the glyph, markers, label and compartments of every node and the link of every relation,
which a surface such as graph_ui serves and draws without re-implementing the rules.

**The catalog runs on graph_ui.** `spec2viz catalog sync --config docs/architecture/vistas.yml --store .sldb`
syncs every spec of the registry with its notation and writes the registry's `category`, `nav` and
`desc` into each `SpecDoc`; graph_ui lists the specs by category and draws each one from `notation view`.
`catalog build` still produces the HTML bundle, now as the static export of the same data.

Hierarchical stores can aggregate other stores and legacy `vistas.yml` leaves, then expose one filtered HTML catalog by category, type, project, and tags.

Minimal `project.yml` / diagram-store shape:

```yaml
diagram_store:
  kind: diagram-store
  template: template.html
  title: Repo Diagram Catalog
  brand_name: Repo Diagram Catalog
  brand_subtitle: Visor transversal de diagramas del repo Example
  project_name: projects/example
  stores:
    - path: projects/example/docs/vistas.yml
      project: projects/example
      tags:
        - domain:crm
```

Template rule for new projects:

- keep `template: template.html` in the catalog config
- do **not** create `template.html` locally unless you want an explicit override
- when the file is absent, spec2viz falls back to the built-in template at `spec2viz/templates/default.html`
- when the file exists, spec2viz now prints a warning that a local override is active

## PlantUML Kind Styling

Component specs can now carry renderer-specific color overrides in YAML. This keeps purpose in the semantic `kind` field while letting PlantUML choose how each kind should look.

```yaml
id: architecture.example
title: Example Architecture
type: component
version: "0.1"
style:
  kinds:
    core:
      plantuml:
        background: "#D8ECFF"
        border: "#4C78A8"
        font: "#16324F"
    boundary:
      plantuml:
        background: "#FCECC9"
        border: "#D4A73C"
        font: "#5E450B"
data:
  nodes:
    App:
      kind: core
    Api:
      kind: boundary
```

Notes:

- this currently applies to PlantUML rendering for `component` diagrams
- `kind` stays semantic; the `style.kinds` block is only a renderer hint
- if you omit `style.kinds`, PlantUML falls back to the built-in palette for `core`, `boundary`, and `database`

Export the JSON Schema for all supported specs or one diagram/store type:

```bash
spec2viz schema > spec2viz.schema.json
spec2viz schema --type sequence --out sequence.schema.json
spec2viz schema --type diagram-store --out diagram-store.schema.json
```

## Python API

```python
from spec2viz import compile_ir, load, render, validate

diagram = load("tests/fixtures/sequence.create-quotation.yml")
validate(diagram)
ir = compile_ir(diagram)
output = render(ir)
```

Write rendered output directly to disk:

```python
from spec2viz import render_to_file

path = render_to_file("tests/fixtures/matrix.quotation-view.yml", out="out")
print(path)
```

Generate JSON Schema for editor integration or documentation:

```python
from spec2viz import json_schema, write_json_schema

schema = json_schema("sequence")
write_json_schema("sequence.schema.json", diagram_type="sequence")
```

## Examples

Sample source specs and rendered outputs live under `examples/`.

- `examples/sequence/example.yml`
- `examples/state/example.yml`
- `examples/component/example.yml`
- `examples/activity/example.yml`
- `examples/deployment/example.yml`
- `examples/matrix/example.yml`
- `examples/schema/spec2viz.schema.json`
- `examples/schema/sequence.schema.json`

Refresh the checked-in schema examples when the models change:

```bash
spec2viz schema --out examples/schema/spec2viz.schema.json
spec2viz schema --type sequence --out examples/schema/sequence.schema.json
```

## Validation and Tests

`tools/suite-check.sh [--fresh] [--skip-install] [--skip-suites] [--skip-e2e]` runs the integrated check of
the whole SLDB_1 suite from a clean venv (`SUITE_VENV`, default `/tmp/suite-venv`; `SUITE_PYTHON`,
default `/usr/bin/python3`; checkouts under `SLDB1_ROOT`): installs sldb, pron, deskops, spec2viz and
graph_ui editable from their checkouts, runs each repo's tests (`SUITE_REPOS` narrows the list), then an
end-to-end flow across deskops, spec2viz and graph_ui, and prints a step x result table. Logs land in
`SUITE_REPORT` (default `/tmp/suite-check`). `--from-origin` clones each repo's main branch from its origin
(shallow, into `SUITE_CLONES`) and tests those clones instead of the working checkouts: that is the run that
decides a deploy. `--pythons [3.12,3.13]` (that list is the default) repeats install, suites and e2e once per interpreter
(found or installed with `uv python`, else `pythonX.Y`), prints a step x Python table and removes each venv
when its column ends; every pytest runs with its own `--basetemp` under `mktemp`, and the e2e repo and the
origin clones are removed on exit (`SUITE_KEEP=1` keeps them); the node toolchain of
graph_ui's review-workbench (`npm ci`, vitest, tsc, architecture lint) runs once per run (`--skip-node`
to leave it out). It never tags or publishes anything.

Run the full suite:

```bash
pytest -q
```

Validate packaged installation behavior:

```bash
python3 -m pip install --force-reinstall .
spec2viz --help
```

## Migration From `yaml-charts`

The project was renamed from `yaml-charts` / `yaml_charts` to `spec2viz`.

- preferred import path: `spec2viz`
- preferred CLI command: `spec2viz`
- legacy imports under `yaml_charts` still resolve with a deprecation warning
- legacy CLI `yaml-charts` still works as a compatibility shim and prints a migration notice

New code should use `spec2viz` everywhere.
