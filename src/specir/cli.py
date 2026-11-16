"""The `specir` command: the visual layer's CLI, with the taxonomy of spec2viz's (IR13d).

- `diagram` (render, validate, lint, schema) and `catalog` (schema) are IR12's groups
  (`specir.visual.commands`); this module mounts them and adds `catalog build` (IR13b's page, with
  the option to save its annotations through `sldb serve`), the top-level aliases `render`,
  `validate`, `lint`, `schema` and `build`, and `about`.
- What spec2viz's CLI did that is sldb's has no command here, by design (JP: no wrapper over sldb's
  CLI or API): syncing a spec, a notation, a palette or a catalog (`sldb notations sync --spec`,
  `--notation`, `--palette`, `--catalog [--check]`), generating a spec from a graph or from Python
  (`sldb notations from-graph`), listing notations and palettes (`sldb notations list`), resolving a
  view (`sldb notations view`) and serving the catalog's annotations (`sldb serve`). The table is
  `docs/spec2viz/correspondencia-cli.md`.
- `diagram validate` (and `validate`) runs sldb's `load_spec`/`validate_spec` and redefines
  nothing: sldb has no command that validates a spec yet (SV-K16); when it has one, it goes."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from specir.visual.commands import (
    DIAGRAM_RENDERERS,
    _lint_paths,
    _render_paths,
    _validate_paths,
    _write_schema,
    catalog,
    diagram,
)

#: The top-level aliases, each with the group command it stands for (spec2viz's legacy commands).
ALIASES = {"render": "diagram render", "validate": "diagram validate", "lint": "diagram lint", "schema": "diagram schema",
           "build": "catalog build"}


@click.group(
    help=(
        "specIR CLI: semantic diagram specs -> diagrams -> catalog HTML.\n\n"
        "\b\nTaxonomy:\n"
        "- diagram: semantic diagram specs (render, validate, lint, schema)\n"
        "- catalog: HTML bundles and hierarchical diagram stores (build, schema)\n\n"
        "Top-level aliases (render, validate, lint, schema, build) remain available for compatibility.\n\n"
        "Syncing specs, notations, palettes and catalogs into a store, generating specs from a graph "
        "or from Python, resolving views and serving annotations are sldb's: use `sldb notations ...` "
        "and `sldb serve` directly."
    )
)
@click.version_option(package_name="specir", prog_name="specir")
def main():
    pass


main.add_command(diagram)
main.add_command(catalog)


@main.command("about", short_help="Where diagrams live and how the flow reaches HTML.")
def about():
    """Point to where the diagrams live and the full spec -> HTML flow, with sldb's commands for the store."""
    from sldb.api.notations import find_store

    cwd = Path.cwd()
    store = find_store(cwd)
    click.echo("specir — semantic specs -> diagrams -> catalog HTML (specIR's visual layer over sldb)\n")

    click.echo("Where the diagrams live:")
    click.echo("  spec files       : YAML specs (`type:` one of the eight diagram types) next to their vistas.yml")
    click.echo(f"  store            : {store if store else f'no .sldb store above {cwd}'}")
    click.echo("  specs in a store : SpecDoc documents (`sldb notations list --store <.sldb>`)")
    click.echo("  catalog config   : a vistas.yml registry or a project.yml / diagram-store config\n")

    click.echo("Flow to HTML:")
    click.echo("  1. specir diagram validate <spec.yml>")
    click.echo("  2. specir diagram render   <spec.yml> --out <dir>")
    click.echo("  3. specir diagram lint     <rendered.mmd>")
    click.echo("  4. specir catalog build    --config <vistas.yml> --out <out.html>")
    click.echo("     (build alias = catalog build; --atoms-dir injects window.ATOMS_DB)\n")

    click.echo("Into the store (sldb, used directly):")
    click.echo("  sldb notations sync --spec <spec.yml> --store <.sldb>")
    click.echo("  sldb notations sync --catalog <vistas.yml> [--check] --store <.sldb>")
    click.echo("  sldb notations from-graph --python <src_dir> | --store <.sldb> | --snapshot <graph.json>")
    click.echo("  sldb notations view <SpecDoc id> --store <.sldb>\n")

    click.echo("Save a built catalog's annotations (replaces spec2viz's `catalog serve`):")
    click.echo("  sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>")
    click.echo("  sldb serve --store <.sldb> --cors --port 8765")
    click.echo("  specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765")


# ── catalog build and its alias ─────────────────────────────────────────────────────────────────


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...],
                   strict_atoms: bool, annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    from specir.visual.catalog import AnnotationsTarget, build_catalog

    target = AnnotationsTarget(server=sldb_url or "", doc=annotations_doc or "") if (annotations or sldb_url or annotations_doc) else None
    try:
        build_catalog(config, out, base_dir, atoms_dir, list(atoms_tags) or None, strict_atoms, target)
        click.echo(f"Rendered catalog -> {out}")
    except Exception as exc:
        click.echo(f"Error building catalog: {exc}", err=True)
        sys.exit(1)


def _catalog_build_options(function):
    options = [
        click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config."),
        click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write."),
        click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory."),
        click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB."),
        click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms."),
        click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning)."),
        click.option("--annotations", is_flag=True, help="Save the page's annotations in an sldb store through `sldb serve`; the server and the document can also come from the page URL (`?sldb=<url>&annotations=<id>`)."),
        click.option("--sldb-url", default=None, help="Base URL of `sldb serve --cors` that keeps the annotations (implies --annotations)."),
        click.option("--annotations-doc", default=None, help="Id of the CatalogAnnotationsDoc that holds them (implies --annotations). Default: derived from the catalog's name."),
    ]
    for option in reversed(options):
        function = option(function)
    return function


@catalog.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
                  annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
          annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


# ── the other top-level aliases ─────────────────────────────────────────────────────────────────


@main.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option("--renderer", "--backend", type=click.Choice(DIAGRAM_RENDERERS), default=None, help="Force a renderer instead of using the spec type default.")
def render(paths: list[Path], out: Path, renderer: str | None):
    """Legacy alias for `diagram render`."""
    _render_paths(paths, out, renderer)


@main.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def validate_cmd(paths: list[Path]):
    """Legacy alias for `diagram validate`."""
    _validate_paths(paths)


@main.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def lint_cmd(paths: list[Path]):
    """Legacy alias for `diagram lint`."""
    _lint_paths(paths)


@main.command("schema", short_help="Export JSON Schema for semantic specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Legacy schema entrypoint for diagram specs and diagram stores."""
    _write_schema(diagram_type, out)


__all__ = ["ALIASES", "main"]


if __name__ == "__main__":
    main()
