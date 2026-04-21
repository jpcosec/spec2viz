from __future__ import annotations
import sys
from pathlib import Path

import click

from yaml_charts import load, render_to_file
from yaml_charts.validator import validate as _validate
from yaml_charts.exceptions import YamlChartsError


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
    except YamlChartsError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


@main.command("render")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path))
@click.option("--renderer", "--backend", default=None, help="plantuml | vega | mermaid")
def render_cmd(paths: tuple[Path, ...], out: Path, renderer: str | None):
    """Render one or more diagram YAML files."""
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} → {output}")
        except YamlChartsError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)
