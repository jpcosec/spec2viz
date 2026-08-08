from __future__ import annotations
import sys
from pathlib import Path
import click
from spec2viz import render_to_file, validate, load, json_schema, write_json_schema
from spec2viz.exceptions import Spec2VizError

@click.group(help="Render semantic diagram specs and deskops architecture registries.")
def main():
    pass

@main.command(short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def render(paths: list[Path], out: Path, renderer: str | None):
    """Render one or more semantic spec files.

    Supported renderers: plantuml, mermaid, vega, d2, antonia-html, json.
    """
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
        except Spec2VizError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)

@main.command(name="validate", short_help="Validate semantic spec files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def validate_cmd(paths: list[Path]):
    """Validate one or more semantic spec files."""
    for path in paths:
        try:
            diagram = load(path)
            validate(diagram)
            click.echo(f"{path.name}: OK")
        except Spec2VizError as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)

@main.command(short_help="Export JSON Schema for semantic specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one diagram type: sequence, state, component, activity, deployment, or matrix.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for all spec types or one diagram type."""
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        import json
        click.echo(json.dumps(json_schema(diagram_type), indent=2))

@main.command(short_help="Build deskops architecture HTML from a vistas registry.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to the vistas.yml registry file.")
@click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write.")
@click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory.")
@click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB.")
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None):
    """Build a deskops architecture HTML bundle from a vistas.yml registry.

    The registry can point at Mermaid, SVG, or HTML vista sources plus an HTML template.
    """
    from spec2viz.deskops import build_deskops
    try:
        build_deskops(config, out, base_dir, atoms_dir)
        click.echo(f"Rendered deskops architecture -> {out}")
    except Exception as exc:
        click.echo(f"Error building deskops: {exc}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
