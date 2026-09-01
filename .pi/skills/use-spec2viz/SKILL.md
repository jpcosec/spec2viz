---
name: use-spec2viz
description: Use when working on this repository's spec2viz CLI, renderers, semantic spec workflows, schema export, or catalog/deskops architecture HTML build flow.
---

# Use spec2viz

Use this skill when the task touches:

- `spec2viz` CLI commands
- renderer selection or output extensions
- semantic spec validation or schema export
- `vistas.yml` registry or diagram-store rendering into catalog HTML
- examples and help text for spec2viz workflows

## Fast orientation

Run `about` first to see where diagrams live and the full flow to HTML:

```bash
python -m spec2viz.cli about
```

## Mandatory read route

Read these first:
1. `README.md`
2. `spec2viz/cli.py`
3. `spec2viz/__init__.py`
4. `spec2viz/renderers/__init__.py`
5. `spec2viz/deskops.py` when the task involves `catalog build`

## CLI taxonomy

The CLI is grouped into two domains, with legacy top-level aliases kept for compatibility:

- `diagram` — semantic diagram specs: `generate`, `render`, `lint`, `validate`, `schema`
- `catalog` — HTML bundles and diagram stores: `build`, `schema`, `serve`
- top-level `about`, plus legacy aliases: `render`, `validate`, `lint`, `schema`, `build`

Start with help:

```bash
python -m spec2viz.cli --help
python -m spec2viz.cli diagram --help
python -m spec2viz.cli catalog --help
```

Core commands (canonical form):

```bash
python -m spec2viz.cli diagram validate <spec.yml>
python -m spec2viz.cli diagram render <spec.yml> --out <dir>
python -m spec2viz.cli diagram lint <rendered.mmd>
python -m spec2viz.cli diagram schema --out <schema.json>
python -m spec2viz.cli catalog build --config <vistas.yml> --out <out.html>
python -m spec2viz.cli catalog serve --html <out.html> --port 8000
```

The installed console script `spec2viz ...` maps to the same commands and is the
form used by downstream build scripts (e.g. `software/infra/build.sh` in AntonIA).

## Renderer contract

Supported renderer names (`DIAGRAM_RENDERERS` in `spec2viz/cli.py`, `RENDERER_MAP`
in `spec2viz/renderers/__init__.py`):

- `plantuml`
- `mermaid`
- `vega`
- `d2`
- `antonia-html`
- `tree`
- `graph`
- `json`

Do not document a renderer list that disagrees with `RENDERER_MAP`.

## Full flow to HTML

```
diagram validate  ->  diagram render (mermaid)  ->  diagram lint  ->  catalog build  ->  HTML
```

`catalog build` (and its legacy alias `build`) is the catalog/architecture HTML path:

- input: a `vistas.yml` registry or a hierarchical diagram-store config
- output: one HTML file
- sources: template plus vista files resolved relative to `--base-dir` or the config directory
- `--atoms-dir`: markdown W5H1 atom files whose payload is injected into the page

Atom injection detail: the build always writes `window.ATOMS_DB = {}`,
`window.ATOMS_BY_VIEW`, and `window.COVERAGE_BY_VIEW` into the page. A consumer
repo may post-process the HTML to populate `window.ATOMS_DB` from its own atoms
(see `parse_atoms` in `spec2viz/deskops.py`, used by `software/infra/build.sh`).

## Validation

For CLI or help changes, run:

```bash
python -m spec2viz.cli --help
python -m spec2viz.cli about
python -m spec2viz.cli diagram render --help
python -m spec2viz.cli catalog build --help
pytest -q
```

## Anti-drift rule

Keep these aligned:

- `README.md`
- command help in `spec2viz/cli.py`
- supported renderers in `spec2viz/renderers/__init__.py`
- build behavior in `spec2viz/deskops.py`
- `about` output paths vs the real `examples/` tree
