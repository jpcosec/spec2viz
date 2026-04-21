from __future__ import annotations
import json
import sys
from pathlib import Path

import click

from spec2viz import json_schema, load, render_to_file, write_json_schema
from spec2viz.validator import validate as _validate
from spec2viz.exceptions import Spec2VizError


@click.group()
def main():
    pass


@main.command("validate")
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def validate_cmd(path: Path):
    """Validate a diagram YAML file."""
    try:
        diagram = load(path)
        _validate(diagram)
        click.echo(f"OK: {path.name}")
    except Spec2VizError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


@main.command("render")
@click.argument(
    "paths", nargs=-1, type=click.Path(exists=True, path_type=Path), required=True
)
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path))
@click.option("--renderer", "--backend", default=None, help="plantuml | vega | mermaid")
def render_cmd(paths: tuple[Path, ...], out: Path, renderer: str | None):
    """Render one or more diagram YAML files."""
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} → {output}")
        except Spec2VizError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)


@main.command("schema")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="sequence | state | component | activity | deployment | component_view_matrix",
)
@click.option("--out", type=click.Path(path_type=Path), default=None)
def schema_cmd(diagram_type: str | None, out: Path | None):
    """Export the JSON Schema for one diagram type or the full spec union."""
    try:
        if out is not None:
            output = write_json_schema(out, diagram_type=diagram_type)
            click.echo(f"Wrote schema to {output}")
            return

        click.echo(json.dumps(json_schema(diagram_type), indent=2))
    except (Spec2VizError, ValueError) as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
