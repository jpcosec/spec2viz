import click
from pathlib import Path
from spec2viz import render_to_file
from spec2viz.exceptions import Spec2VizError

@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path))
@click.option("--renderer", "--backend", default=None, help="plantuml (default) | mermaid | vega")
def render(path: Path, out: Path, renderer: str | None):
    """Render a diagram YAML file."""
    try:
        output = render_to_file(path, out=out, renderer=renderer)
        click.echo(f"Rendered {path.name} → {output}")
    except Spec2VizError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    render()
