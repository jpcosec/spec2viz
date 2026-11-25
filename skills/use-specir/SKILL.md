---
name: use-specir
description: Use when declaring and extracting diagram content with specIR (spec classes, notations, specs from code or text), exporting a spec to PlantUML, Mermaid, D2 or BPMN XML, linting or exporting the schema of specs, or choosing an exporter, with specIR's `specir` command and its Python API (`specir.visual`). specIR declares and extracts; it does not draw and has no interface of its own: a diagram is seen and edited in graph_ui's notation view. What is generic (syncing specs, notations, palettes and catalogs into a store, generating specs from a graph or from Python, resolving views, serving) is sldb's and is used with the `sldb` command directly.
---

# Use specIR (declares and extracts)

specIR declares and extracts: it owns the diagram content (notations, spec classes) and the extraction
from code and text exports. It does not draw and it has no interface of its own (decided 2026-11-25, see
`docs/decisiones/paridad-por-capacidades.md`). It replaces spec2viz by capabilities, not by code: each
capability is proved by an acceptance test of what it does, never by identical output. sldb owns
everything generic; specIR never wraps it.

## Where a diagram is seen or edited

A diagram is a `SpecDoc` or a `ViewDoc` in an sldb store with its notation. To see it or edit it, go to
graph_ui's notation view (`UIs/graph_ui`, view `specs/notation`). Do not build a renderer, a page or a
viewer in specIR. Static HTML or SVG is only for embedding inline.

Capability state, from that decision (2026-11-25):

- Seeing any of the 8 diagram types with its notation: met in graph_ui's notation view.
- Validating a spec and syncing it to the store: met, in sldb.
- Exporting to PlantUML, Mermaid, D2 or BPMN XML: met, in specIR (`specir diagram render`).
- Opening a node to see its document, atoms and references; annotating a diagram or a node; editing from
  the diagram: missing (decided 2026-11-25, not executed). Do not describe them as done.

Use this skill when the task touches:

- exporting a diagram spec to a text format (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json)
- validating a spec, linting exported mermaid, or exporting the JSON Schema of specs or diagram stores
- building the legacy catalog HTML from a `vistas.yml` registry (retiring, see below)
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
| Export (render to a text format), lint, schema of a spec | `specir diagram render`, `specir diagram lint`, `specir diagram schema` | |
| Validate a spec, a notation or a palette | `sldb notations validate <name\|path> [--json]` (specIR has no validate command) | |
| Legacy catalog HTML (retiring: decided 2026-11-25, not executed) | `specir catalog build` | |
| Catalog schema | `specir catalog schema` | |
| Sync a spec into a store | `sldb notations sync --spec` | a specIR command |
| Sync a notation or a palette | `sldb notations sync --notation`, `sldb notations sync --palette` | a specIR command |
| Sync or check a catalog | `sldb notations sync --catalog`, `sldb notations sync --catalog --check` | a specIR command |
| Spec from a graph, a store or Python | `sldb notations from-graph` (`--snapshot`, `--store`, `--python`) | a specIR command |
| List notations, palettes, views | `sldb notations list` | a specIR command |
| Resolve a spec's view | `sldb notations view` | a specIR command |
| Serve a store over HTTP | `sldb serve` (the store has one door: sldb's API; the move to fastmcp is decided 2026-11-25, not executed) | a specIR server |
| See or edit a diagram | graph_ui notation view (`UIs/graph_ui`, `specs/notation`) | a specIR page or renderer |
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

- `diagram`: `render`, `lint`, `schema`
- `catalog`: `build`, `schema`
- top level: `about`, and the aliases `render`, `lint`, `schema`, `build`
- MCP: `specir mcp --store <project store>` starts sldb's MCP server with specIR's tools loaded (same as `sldb mcp --extension specir.mcp_extension:register`). Mounting specIR's tools on sldb's own server once its API is on fastmcp is decided 2026-11-25, not executed.

Core commands (canonical form):

```bash
sldb notations validate <spec.yml>
specir diagram render <spec.yml> --out <dir>
specir diagram render <spec.yml> --out <dir> --renderer mermaid
specir diagram lint <rendered.mmd>
specir diagram schema --type sequence --out <schema.json>
specir catalog schema --out <store.schema.json>
specir catalog build --config <vistas.yml> --out <out.html>
specir catalog build --config <vistas.yml> --out <out.html> --atoms-dir <atoms> --atoms-tag <tag> --strict-atoms
```

`--backend` is an alias of `--renderer`. A rendered text projection starts with a provenance header
that names its spec and `sldb notations validate`: never edit it by hand, re-render it.

## Renderer contract

The nine renderer names (`RENDERER_MAP` in `src/specir/visual/renderers/__init__.py`):

- `plantuml`, `mermaid`, `vega`, `d2`, `antonia-html`, `tree`, `graph`, `bpmn`, `json`

The default per type: class `mermaid`; sequence, state, activity and deployment `plantuml`; component
`graph`; matrix `vega`; reflection `json`. `bpmn` writes `<stem>.bpmn` and `<stem>.bpmn.html` (offline
viewer). Do not document a renderer list that disagrees with `RENDERER_MAP`.

## Flow to the legacy catalog HTML

```
sldb notations validate -> specir diagram render -> specir diagram lint -> specir catalog build -> HTML
```

### Real mermaid engine (mmdc)

`specir diagram lint` (and `lint_mermaid`/`assert_mermaid_ok`) adds a pass with the real mermaid parser
when mermaid-cli is available; without it only the regex heuristics run, and the tests that need the
engine skip. The binary is `mmdc` on the PATH, or the one `SPECIR_MMDC` points to (`SPEC2VIZ_MMDC`
still works); `SPECIR_MMDC=0` turns the engine pass off.

On this machine mermaid-cli lives outside any repo, in `/mnt/ssd/herramientas/mermaid-cli` (npm install
with `PUPPETEER_SKIP_DOWNLOAD=1`, no bundled Chromium). Its `mmdc` there is a wrapper that runs the system
Chrome (`/usr/bin/google-chrome`, `PUPPETEER_EXECUTABLE_PATH`) headless with `puppeteer-config.json`,
puts the Chrome profile in a temporary `/dev/shm/irjp-mmdc.*` directory that it deletes on exit, and caps
each render with `timeout` (`MMDC_TIMEOUT`, 55 s by default):

```bash
export SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc
specir diagram lint <rendered.mmd>
```

And into a store, with sldb:

```bash
sldb notations sync --spec <spec.yml> --store <.sldb>
sldb notations sync --catalog <vistas.yml> --check --store <.sldb>
sldb notations sync --catalog <vistas.yml> --store <.sldb>
sldb notations from-graph --python <src_dir> --output <spec.yml>
sldb notations view <spec_id> --store <.sldb>
```

Legacy `specir catalog build` (and the alias `specir build`):

- input: a `vistas.yml` registry or a hierarchical diagram-store config (`project.yml`)
- output: one self-contained HTML file
- sources: template and view files resolved against `--base-dir` or the config directory
- `--atoms-dir`: W5H1 atom markdown files injected as `window.ATOMS_DB`; atoms are matched to diagram
  elements by sldb (`sldb.api.matching`)

## Catalog page and its annotations (retiring)

`specir catalog build` still writes the legacy catalog HTML, and `CatalogAnnotationsDoc` still exists.
Both are retired once capabilities 1 to 4 and 6 are met (decided 2026-11-25, not executed). Do not build
new work on them: annotating a diagram or a node belongs to graph_ui and the text editor, and that is
not built yet (decided 2026-11-25, not executed).

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
`assert_mermaid_ok`, `render_catalog`, `AnnotationsTarget` (tied to the retiring catalog) and the errors `Spec2VizError`,
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
