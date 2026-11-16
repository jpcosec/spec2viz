---
name: use-specir
description: Use when rendering, validating, linting or exporting the schema of semantic diagram specs, building the HTML catalog of diagrams (vistas.yml or diagram-store), or choosing a renderer, with specIR's `specir` command and its Python API (`specir.visual`). Replaces use-spec2viz. What is generic (syncing specs, notations, palettes and catalogs into a store, generating specs from a graph or from Python, resolving views, serving annotations) is sldb's and is used with the `sldb` command directly.
---

# Use specIR (visual layer)

specIR is the visual layer and domain mapping over SLDB stores. It replaces spec2viz: same diagram
types, same renderers, same catalog page. sldb owns everything generic; specIR never wraps it.

Use this skill when the task touches:

- rendering a diagram spec (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json)
- validating a spec, linting rendered mermaid, or exporting the JSON Schema of specs or diagram stores
- building the catalog HTML from a `vistas.yml` registry or a `project.yml` / diagram-store config
- saving the catalog's annotations in an sldb store
- the Python API `specir.visual` (compile, render, render to file, schema, lint, catalog)

## Fast orientation

Run `about` first: it shows the store above the current directory and the whole flow to HTML,
including the sldb commands for the store.

```bash
specir about
specir --help
specir diagram --help
specir catalog --help
```

`python -m specir.cli` is the same command when the script is not on `PATH`.

## Who owns what

| Need | Use | Not |
|---|---|---|
| Render, lint, schema of a spec | `specir diagram render`, `specir diagram lint`, `specir diagram schema` | |
| Validate a spec | `specir diagram validate` (calls sldb's `load_spec` and `validate_spec`; provisional until sldb has its own command) | |
| Catalog HTML | `specir catalog build` | |
| Catalog schema | `specir catalog schema` | |
| Sync a spec into a store | `sldb notations sync --spec` | a specIR command |
| Sync a notation or a palette | `sldb notations sync --notation`, `sldb notations sync --palette` | a specIR command |
| Sync or check a catalog | `sldb notations sync --catalog`, `sldb notations sync --catalog --check` | a specIR command |
| Spec from a graph, a store or Python | `sldb notations from-graph` (`--snapshot`, `--store`, `--python`) | a specIR command |
| List notations, palettes, views | `sldb notations list` | a specIR command |
| Resolve a spec's view | `sldb notations view` | a specIR command |
| Serve the catalog's annotations | `sldb serve` | spec2viz's catalog serve |
| Load and validate a spec in Python | `sldb.api.notations.load_spec`, `validate_spec` | a specIR re-export |

If sldb lacks something generic, write it to sldb's inbox (`deskops message send --to sldb`); do not
add it to specIR.

## Mandatory read route

1. `docs/spec2viz/correspondencia-cli.md`: every spec2viz command and its equivalent.
2. `src/specir/cli.py`: the command, the aliases and `about`.
3. `src/specir/visual/__init__.py`: the public Python API.
4. `src/specir/visual/renderers/__init__.py`: `RENDERER_MAP`, `EXT_MAP`, `DEFAULT_RENDERER`.
5. `src/specir/visual/catalog/build.py` when the task involves the catalog.

## CLI taxonomy

- `diagram`: `render`, `validate`, `lint`, `schema`
- `catalog`: `build`, `schema`
- top level: `about`, and the aliases `render`, `validate`, `lint`, `schema`, `build`

Core commands (canonical form):

```bash
specir diagram validate <spec.yml>
specir diagram render <spec.yml> --out <dir>
specir diagram render <spec.yml> --out <dir> --renderer mermaid
specir diagram lint <rendered.mmd>
specir diagram schema --type sequence --out <schema.json>
specir catalog schema --out <store.schema.json>
specir catalog build --config <vistas.yml> --out <out.html>
specir catalog build --config <vistas.yml> --out <out.html> --atoms-dir <atoms> --atoms-tag <tag> --strict-atoms
```

`--backend` is an alias of `--renderer`. A rendered text projection starts with a provenance header
that names its spec and `specir diagram validate`: never edit it by hand, re-render it.

## Renderer contract

The nine renderer names (`RENDERER_MAP` in `src/specir/visual/renderers/__init__.py`):

- `plantuml`, `mermaid`, `vega`, `d2`, `antonia-html`, `tree`, `graph`, `bpmn`, `json`

The default per type: class `mermaid`; sequence, state, activity and deployment `plantuml`; component
`graph`; matrix `vega`; reflection `json`. `bpmn` writes `<stem>.bpmn` and `<stem>.bpmn.html` (offline
viewer). Do not document a renderer list that disagrees with `RENDERER_MAP`.

## Full flow to HTML

```
specir diagram validate -> specir diagram render -> specir diagram lint -> specir catalog build -> HTML
```

And into a store, with sldb:

```bash
sldb notations sync --spec <spec.yml> --store <.sldb>
sldb notations sync --catalog <vistas.yml> --check --store <.sldb>
sldb notations sync --catalog <vistas.yml> --store <.sldb>
sldb notations from-graph --python <src_dir> --output <spec.yml>
sldb notations view <spec_id> --store <.sldb>
```

`specir catalog build` (and the alias `specir build`):

- input: a `vistas.yml` registry or a hierarchical diagram-store config (`project.yml`)
- output: one self-contained HTML file
- sources: template and view files resolved against `--base-dir` or the config directory
- `--atoms-dir`: W5H1 atom markdown files injected as `window.ATOMS_DB`; atoms are matched to diagram
  elements by sldb (`sldb.api.matching`)

## Catalog annotations (replaces spec2viz's catalog serve)

The page saves its annotations in a `CatalogAnnotationsDoc` of an sldb store, through `sldb serve`:

```bash
sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>
sldb serve --store <.sldb> --cors --port 8765
specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765
```

`--annotations-doc <id>` fixes the document id; `--annotations` alone embeds the saver and the page
takes the server from its URL (`?sldb=<url>&annotations=<id>`).

## Python API

```python
from sldb.api.notations import load_spec, validate_spec
from specir.visual import compile_ir, render, render_to_file, json_schema, lint_mermaid, build_catalog

diagram = load_spec("spec.yml")
validate_spec(diagram)
text = render(compile_ir(diagram), "mermaid")
path = render_to_file("spec.yml", out="build", renderer="plantuml")
```

`specir.visual` also exports the IR dataclasses, the compilers, `RENDERER_MAP`, `EXT_MAP`,
`DEFAULT_RENDERER`, `with_provenance`, `provenance_header`, `provenance_text`, `write_json_schema`,
`assert_mermaid_ok`, `render_catalog`, `AnnotationsTarget` and the errors `Spec2VizError`,
`CompileError` and `RenderError`.

## Validation

For CLI, help or skill changes, run:

```bash
specir --help
specir about
specir diagram render --help
specir catalog build --help
```

and the tests of the files you touched, one file at a time, for example
`tests/visual/test_cli.py`, `tests/visual/test_api.py` and `tests/visual/test_packaging.py`.

## Anti-drift rule

Keep these aligned:

- `docs/spec2viz/correspondencia-cli.md`
- command help in `src/specir/cli.py` and `src/specir/visual/commands.py`
- renderers in `src/specir/visual/renderers/__init__.py`
- this skill: every command it names must exist (checked by `tests/visual/test_cli.py`)
