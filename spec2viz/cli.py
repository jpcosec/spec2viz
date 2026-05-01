from __future__ import annotations
import json
import sys
from pathlib import Path

import click

from spec2viz import json_schema, load, render_to_file, write_json_schema
from spec2viz.validator import validate as _validate
from spec2viz.exceptions import Spec2VizError

_EXAMPLES_DIR = Path(__file__).parent.parent / "examples"

_TYPES = {
    "sequence": "Message flow between participants",
    "state": "State machine with transitions",
    "component": "Component graph with relationships",
    "activity": "Flowchart / activity diagram",
    "deployment": "Deployment nodes and artifacts",
    "component_view_matrix": "Component × stage matrix",
}

_TYPE_TO_DIR = {
    "sequence": "sequence",
    "state": "state",
    "component": "component",
    "activity": "activity",
    "deployment": "deployment",
    "component_view_matrix": "matrix",
}


@click.group()
def main():
    """Turn semantic YAML specs into diagrams (PlantUML, Mermaid, Vega).

    Run 'spec2viz types' to see all supported diagram types and their structure.
    Run 'spec2viz examples <type>' to get a ready-to-edit YAML starter file.
    """


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
@click.option("--renderer", "--backend", default=None, help="plantuml (default) | mermaid | vega")
def render_cmd(paths: tuple[Path, ...], out: Path, renderer: str | None):
    """Render one or more diagram YAML files.

    Default backend is plantuml, producing .puml files.
    Use --backend mermaid for .mmd files, --backend vega for .json files.

    \b
    Examples:
      spec2viz render diagram.yml
      spec2viz render diagram.yml --backend mermaid --out out/
      spec2viz render *.yml --out out/
    """
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


@main.command("types")
@click.argument("diagram_type", required=False)
def types_cmd(diagram_type: str | None):
    """List supported diagram types, or show the YAML structure for one type.

    \b
    Examples:
      spec2viz types
      spec2viz types sequence
    """
    if diagram_type is None:
        click.echo("Supported diagram types:\n")
        for name, desc in _TYPES.items():
            click.echo(f"  {name:<26} {desc}")
        click.echo("\nRun 'spec2viz types <type>' to see its YAML structure.")
        click.echo("Run 'spec2viz examples <type>' to get a ready-to-edit starter file.")
        return

    dir_name = _TYPE_TO_DIR.get(diagram_type)
    if dir_name is None:
        click.echo(f"Error: unknown type '{diagram_type}'. Run 'spec2viz types' to list valid types.", err=True)
        sys.exit(1)
    example_path = _EXAMPLES_DIR / dir_name / "example.yml"

    click.echo(f"# YAML structure for type: {diagram_type}\n")
    click.echo(example_path.read_text())


@main.command("examples")
@click.argument("diagram_type")
@click.option("--out", type=click.Path(path_type=Path), default=None, help="Write to file instead of stdout")
def examples_cmd(diagram_type: str, out: Path | None):
    """Print a ready-to-edit YAML example for a diagram type.

    \b
    Examples:
      spec2viz examples sequence
      spec2viz examples state > my-state.yml
      spec2viz examples component --out diagram.yml
    """
    example_path = _EXAMPLES_DIR / diagram_type.replace("_", "") / "example.yml"
    if not example_path.exists():
        example_path = _EXAMPLES_DIR / diagram_type / "example.yml"

    if not example_path.exists():
        click.echo(f"Error: unknown type '{diagram_type}'. Run 'spec2viz types' to list valid types.", err=True)
        sys.exit(1)

    content = example_path.read_text()
    if out is not None:
        out.write_text(content)
        click.echo(f"Wrote example to {out}")
    else:
        click.echo(content, nl=False)
