"""The render, lint and schema commands of the visual layer, migrated from `spec2viz.cli`.

`diagram render|lint|schema` and `catalog schema` keep spec2viz's arguments, options (`--renderer`
with its alias `--backend` and its nine values) and output. `diagram validate` runs sldb's
`load_spec`/`validate_spec` (D3) and is the command the provenance header of a projection names
(SV-K16: sldb has no command that validates a spec yet; when it has one, this one goes).
The `specir` command is `specir.cli` (IR13d): it mounts these two groups, adds `catalog build`, the
top-level aliases and `about`. The helpers `_render_paths`, `_validate_paths`, `_lint_paths` and
`_write_schema` are what a group command and its top-level alias share."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from sldb.api.notations import load_spec, validate_spec

from specir.visual.exceptions import Spec2VizError
from specir.visual.notation_style import NotationError
from specir.visual.render_file import render_to_file
from specir.visual.renderers import RENDERER_MAP
from specir.visual.schema import json_schema, write_json_schema

#: The values of `--renderer`, in spec2viz's order (the keys of the render dispatch).
DIAGRAM_RENDERERS = ["plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json"]
assert set(DIAGRAM_RENDERERS) == set(RENDERER_MAP)

#: What a spec, a render or a lint can fail with: specIR's visual errors and sldb's notation errors.
ERRORS = (Spec2VizError, NotationError)


def _render_paths(paths: list[Path], out: Path, renderer: str | None):
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
            if renderer == "bpmn":
                click.echo(f"Rendered {path.name} -> {output.with_name(output.name + '.html')}")
        except ERRORS as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)


def _validate_paths(paths: list[Path]):
    for path in paths:
        try:
            validate_spec(load_spec(path))
            click.echo(f"{path.name}: OK")
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)


def _lint_paths(paths: list[Path]):
    """Lint mermaid text files (.mmd) or render specs to mermaid then lint."""
    from specir.visual.compilers import compile_ir
    from specir.visual.lint_mermaid import lint_mermaid
    from specir.visual.renderers import render

    had_issue = False
    for path in paths:
        try:
            if path.suffix == ".mmd":
                text = path.read_text(encoding="utf-8")
            else:
                text = render(compile_ir(load_spec(path)), "mermaid")
            problems = lint_mermaid(text)
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            had_issue = True
            continue
        if problems:
            had_issue = True
            click.echo(f"{path.name}: {len(problems)} issue(s)", err=True)
            for p in problems:
                click.echo(f"  - {p}", err=True)
        else:
            click.echo(f"{path.name}: OK")
    if had_issue:
        sys.exit(1)


def _write_schema(diagram_type: str | None, out: Path | None):
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        click.echo(json.dumps(json_schema(diagram_type), indent=2))


@click.group(help="Work with semantic diagram specs.")
def diagram():
    pass


@click.group(help="Work with diagram catalogs, vistas registries, and hierarchical stores.")
def catalog():
    pass


@diagram.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(DIAGRAM_RENDERERS),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def diagram_render(paths: list[Path], out: Path, renderer: str | None):
    """Render one or more semantic diagram spec files."""
    _render_paths(paths, out, renderer)


@diagram.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def diagram_validate(paths: list[Path]):
    """Validate one or more semantic diagram spec files."""
    _validate_paths(paths)


@diagram.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def diagram_lint(paths: list[Path]):
    """Lint .mmd files, or render specs to mermaid and lint the result."""
    _lint_paths(paths)


@diagram.command("schema", short_help="Export JSON Schema for semantic diagram specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def diagram_schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for all diagram spec types or one diagram type."""
    _write_schema(diagram_type, out)


@catalog.command("schema", short_help="Export JSON Schema for hierarchical diagram stores.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def catalog_schema(out: Path | None):
    """Export JSON Schema for diagram-store / project.yml configs."""
    _write_schema("diagram-store", out)


__all__ = ["DIAGRAM_RENDERERS", "ERRORS", "catalog", "diagram"]
