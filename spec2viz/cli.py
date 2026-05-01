from __future__ import annotations
import sys
from pathlib import Path
import click
from spec2viz import render_to_file, validate, load, json_schema, write_json_schema
from spec2viz.exceptions import Spec2VizError

@click.group()
def main():
    """spec2viz: Transform semantic specs into diagrams."""
    pass

@main.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path))
@click.option("--renderer", "--backend", default=None, help="plantuml | mermaid | vega")
def render(paths: list[Path], out: Path, renderer: str | None):
    """Render diagram YAML files."""
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
        except Spec2VizError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)

@main.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
def validate_cmd(paths: list[Path]):
    """Validate diagram YAML files."""
    for path in paths:
        try:
            diagram = load(path)
            validate(diagram)
            click.echo(f"{path.name}: OK")
        except Spec2VizError as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)

# Aliasing validate_cmd to validate in the group
main.add_command(validate_cmd, name="validate")

@main.command()
@click.option("--type", "diagram_type", default=None, help="Specific diagram type.")
@click.option("--out", type=click.Path(path_type=Path), help="Output path.")
def schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for specs."""
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        import json
        click.echo(json.dumps(json_schema(diagram_type), indent=2))

if __name__ == '__main__':
    main()
